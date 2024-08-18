import cv2
import time
from app_ats.motion_recorder import record_videos
from app_ats.alerts import send_alert_mail


# ------------------------------------------------------------------- 
# script.py > script.py (functions) > views.py > urls.py > web.html
# -------------------------------------------------------------------


# Track recording count for titling videos
recording_id = 1

# Primary motion detection function
def gen_frames():
    global recording_id
    camera = cv2.VideoCapture(0)  # Use webcam

    # Variables for motion detection and recording
    motion_spotted = False
    motion_start_time = None
    recording = False
    recording_start_time = None
    max_recording_duration = 20  # Recording duration in seconds
    min_motion_duration = 2  # Minimum motion duration to start recording

    frames_list = []
    detected_area = None

    while camera.isOpened():
        check, frame_1 = camera.read()
        check, frame_2 = camera.read()

        if not check:
            break

        # Get the dimensions of the frame
        height, width, _ = frame_1.shape

        # Define the center points to divide the frame into four parts
        center_x, center_y = width // 2, height // 2

        frame_diff = cv2.absdiff(frame_1, frame_2)
        grayscale = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        gaus_blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        _, threshold = cv2.threshold(gaus_blur, 15, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(threshold, None, iterations=5)
        contour, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        is_motion_detected = False

        for contours in contour:
            if cv2.contourArea(contours) < 8000:
                continue
            (x, y, w, h) = cv2.boundingRect(contours)
            cv2.rectangle(frame_1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            is_motion_detected = True

            # Determine the quadrant
            if x < center_x and y < center_y:
                detected_area = "Top Left"
            elif x >= center_x and y < center_y:
                detected_area = "Top Right"
            elif x < center_x and y >= center_y:
                detected_area = "Bottom Left"
            elif x == center_x and y == center_y:
                detected_area = "Center"

        if is_motion_detected:
            if not motion_spotted:
                motion_spotted = True
                motion_start_time = time.time()
            elif time.time() - motion_start_time >= min_motion_duration and not recording:
                recording = True
                recording_start_time = time.time()
                frames_list = []
                print(f"Recording started")
        else:
            motion_spotted = False
            motion_start_time = None

        detection_status = f"MOTION DETECTED in {detected_area}" if is_motion_detected else "STABLE"

        # Draw the detection status at the top-left corner
        cv2.putText(frame_1, f"STATUS: {detection_status}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

        # Draw the quadrant lines
        cv2.line(frame_1, (center_x, 0), (center_x, height), (255, 255, 255), 1)
        cv2.line(frame_1, (0, center_y), (width, center_y), (255, 255, 255), 1)

        # Store frames if recording
        if recording:
            frames_list.append(frame_1)

            # Stop recording after max_recording_duration seconds
            if time.time() - recording_start_time >= max_recording_duration:
                recording = False
                print(f"Recording stopped")

                # function to capture/record videos
                captured_video = record_videos(frames_list, recording_id, frame_1.shape, max_recording_duration)
                recording_id += 1

                # function to send email
                send_alert_mail(captured_video)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
