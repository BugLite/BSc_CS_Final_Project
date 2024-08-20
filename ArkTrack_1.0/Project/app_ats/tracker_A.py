# import all required libraries 
import cv2
import time
from ultralytics import YOLO
from app_ats.spit_screen import identifyArea, drawLines
from app_ats.motion_recorder import record_videos
from app_ats.alerts import send_alert_mail

# recording count for video IDs
recording_id = 1
# load the Yolov8(n) model for Object Classification
model = YOLO('yolov8n.pt')

# primary motion detection function
def gen_frames(intellisense_active = False):
    global recording_id
    camera = cv2.VideoCapture(0)  # Webcam initialised

    # motion detection/recording settings
    min_motion_duration = 2  # minimum duration of detected movement to trigger recording (2 seconds)
    max_recording_duration = 20  # maximum duration for each recording (20 seconds)

    motion_spotted = False
    motion_start_time = None
    recording = False
    frames_list = []

    # store model classification and confidence
    object_detected = []
    
    # capture frames for comparison (ret1/ret2)
    while camera.isOpened():
        ret1, frame_1 = camera.read()
        ret2, frame_2 = camera.read()

        # ensure frames read successfully
        if not (ret1 and ret2):
            break

        # apply frame differentiation algorithm
        frame_diff = cv2.absdiff(frame_1, frame_2)
        grayscale = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        gaus_blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        _, threshold = cv2.threshold(gaus_blur, 15, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(threshold, None, iterations=5)
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # set up motion detection flag
        new_object_detected = []
        is_motion_detected = False
        screen_status = "STABLE" # default status signal

        for contour in contours:
            if cv2.contourArea(contour) < 8000:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            is_motion_detected = True #set flag to True when signficant movement detected
            
            if intellisense_active:
                # specify the area of motion for model
                motion_area = frame_1[y:y+h, x:x+w]
                # run the model on the motion area only
                results = model(motion_area)

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
        
        # Update detected objects if there are new detections
        if new_object_detected:
            object_detected = new_object_detected
        else:
            # Keep the previous detected objects if no new detection
            object_detected = object_detected[-10:]  # Limit to last 10 detections
        
        # Display detected objects
        y_offset = 80  # Starting y position for the text
        for obj in object_detected:
            cv2.putText(frame_1, obj, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            y_offset += 20

        # draw quadrant lines on the frame for region identification
        drawLines(frame_1)

        # display the detection status on the frame
        detection_status = f"MOTION DETECTED in {screen_status}" if is_motion_detected else "STABLE"
        cv2.putText(frame_1, f"STATUS: {detection_status}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

        # store frames if recording is activated
        if recording:
            frames_list.append(frame_1)

            # disable recording after maximum recording duration reached
            if time.time() - recording_start_time >= max_recording_duration:
                recording = False
                print(f"Recording stopped")

                # save the recording as 'captured_video'
                captured_video = record_videos(frames_list, recording_id, frame_1.shape, max_recording_duration)
                recording_id += 1

                # notify user via an alert email
                send_alert_mail(captured_video)

        # encode frame as JPEG format for streaming
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
