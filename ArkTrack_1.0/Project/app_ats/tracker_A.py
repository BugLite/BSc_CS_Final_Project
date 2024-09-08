# import all required libraries 
import cv2
import time
from ultralytics import YOLO
from app_ats.quadrant import identifyArea, drawLines
from app_ats.recorder import record_videos
from app_ats.notify import send_email_alert

# recording count for video IDs
recording_id = 1
# loading the Yolov8(n) - nano model for Object Classification task
model = YOLO('yolov8n.pt')

# primary motion detection (frame-differencing) function
def gen_frames(intellisense_active = False):
    """
    The `gen_frames` function is the primariy surveillance architecture, that runs an effective frame diffencing and object 
    classification model. The function runs the Object Classification model (referred to as 'IntelliSense') only when the User enables
    it on their system. The Tracker A script furthermore, integrates several core functionalities from the project including the email
    and video recording functions and integrates them to create an optimized, clean and modular surveillance system. 
    """

    global recording_id
    camera = cv2.VideoCapture(0)  # Webcam initialised

    # motion detection/recording settings
    min_motion_duration = 2  
    max_recording_duration = 20
    motion_spotted = False
    motion_start_time = None
    recording = False
    frames_list = []

    # store model classification and confidence metrics
    object_detected = []
    # defined frame rate
    frame_rate = 20
    
    # capturing frames for comparison (ret1/ret2)
    while camera.isOpened():
        ret1, frame_1 = camera.read()
        ret2, frame_2 = camera.read()

        # verifying loop breaks if frames are not read successfully
        if not (ret1 and ret2):
            break

        # applying frame differencing algorithm
        frame_diff = cv2.absdiff(frame_1, frame_2)
        grayscale = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        gaus_blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        _, threshold = cv2.threshold(gaus_blur, 15, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(threshold, None, iterations=5)
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # setting up motion detection checks
        new_object_detected = []
        is_motion_detected = False
        screen_status = "STABLE" # setting the default status signal

        for contour in contours:
            if cv2.contourArea(contour) < 8000: # defined threshold to determine movement intensity
                continue

            x, y, w, h = cv2.boundingRect(contour)
            is_motion_detected = True # setting flag to True when signficant movement detected
            
            if intellisense_active:
                # specifying the area of motion for model
                motion_area = frame_1[y:y+h, x:x+w]
                # runing the model on the motion area only
                results = model(motion_area)
                
                # Yolov8n model definition
                for classification in results:
                    boxes = classification.boxes.xyxy.cpu().numpy()
                    confs = classification.boxes.conf.cpu().numpy()
                    classes = classification.boxes.cls.cpu().numpy()

                for box, conf, cls in zip(boxes, confs, classes):
                    x1, y1, x2, y2 = map(int, box)
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    cv2.rectangle(frame_1, (x + x1, y + y1), (x + x2, y + y2), (255, 0, 0), 2)
                    cv2.putText(frame_1, label, (x + x1, y + y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    new_object_detected.append(label)
                
            else:
                cv2.rectangle(frame_1, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # identify the region of motion in frame
            screen_status = identifyArea(frame_1, x, y)
            break

        # if motion is detected, check if recording trigger activated
        if is_motion_detected:
            if not motion_spotted:
                motion_spotted = True
                motion_start_time = time.time()
            elif time.time() - motion_start_time >= min_motion_duration and not recording:
                recording = True
                frames_list = []
                recording_start_time = time.time()
                print(f"Recording started")
        else:
            motion_spotted = False
            motion_start_time = None
        
        # updating the classified objects list if there are new detections
        if new_object_detected:
            object_detected = new_object_detected
        else:
            # limiting the number of objects classifications in the array to 10
            object_detected = object_detected[-10:]
        
        # displaying the classified labels on screen
        y_offset = 80
        for obj in object_detected:
            cv2.putText(frame_1, obj, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            y_offset += 20

        # drawing quadrant lines on the frame for region identification
        drawLines(frame_1)

        # displaying the detection status on the frame
        detection_status = f"MOTION DETECTED in {screen_status}" if is_motion_detected else "STABLE"
        cv2.putText(frame_1, f"STATUS: {detection_status}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

        # storing the frames if recording is triggered
        if recording:
            frames_list.append(frame_1)

            # disable recording once the maximum recording duration has been reached
            if time.time() - recording_start_time >= max_recording_duration:
                recording = False
                print(f"Recording stopped")

                # saving the recording as 'captured_video'
                captured_video = record_videos(frames_list, recording_id, frame_1.shape, max_recording_duration, frame_rate)
                recording_id += 1

                # notifying the user via an alert email
                send_email_alert(captured_video)

        # encode frame as JPEG format for web-based streaming
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
