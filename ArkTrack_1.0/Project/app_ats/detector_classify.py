import cv2
from ultralytics import YOLO

# Loading YOLOv8 model for Object Classification
model = YOLO('yolov8n.pt')

# Function to generate frames with motion detection
def gen_identify_frames():
    camera = cv2.VideoCapture("/Users/oxon/Downloads/testvideo.mp4")  # Use webcam

    detected_objects = []  # List to store detected objects and their confidences

    while camera.isOpened():
        check, frame_1 = camera.read()
        check, frame_2 = camera.read()

        if not check:
            break

        frame_diff = cv2.absdiff(frame_1, frame_2)
        grayscale = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        gaus_blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        _, threshold = cv2.threshold(gaus_blur, 15, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(threshold, None, iterations=5)
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        is_motion_detected = False
        new_detected_objects = []

        for contour in contours:
            if cv2.contourArea(contour) < 8000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            is_motion_detected = True

            # Crop the detected motion area for object detection
            motion_area = frame_1[y:y+h, x:x+w]

            # Perform object detection using YOLOv8
            results = model(motion_area)

            # Collect detection results
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()

                for box, conf, cls in zip(boxes, confs, classes):
                    x1, y1, x2, y2 = map(int, box)
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    cv2.rectangle(frame_1, (x + x1, y + y1), (x + x2, y + y2), (255, 0, 0), 2)
                    cv2.putText(frame_1, label, (x + x1, y + y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    new_detected_objects.append(label)

        if is_motion_detected:
            detection_status = "MOTION DETECTED"
            text_color = (0, 0, 255)
        else:
            detection_status = "STABLE"
            text_color = (217, 10, 10)

        # Update detected objects if there are new detections
        if new_detected_objects:
            detected_objects = new_detected_objects
        else:
            # Keep the previous detected objects if no new detection
            detected_objects = detected_objects

        # Display detection status
        cv2.putText(frame_1, "LIVE STATUS: {}".format(detection_status), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, text_color, 2)

        # Display detected objects
        y_offset = 80  # Starting y position for the text
        for obj in detected_objects:
            cv2.putText(frame_1, obj, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            y_offset += 20

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
