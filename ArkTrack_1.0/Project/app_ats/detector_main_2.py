import cv2
import time
import numpy as np
import os

# Define the directory where you want to save the recordings
save_directory = "/Users/oxon/Documents/ArkTrack System/Recordings"
os.makedirs(save_directory, exist_ok=True)

# Track recording count
recording_count = 1

def gen_frames():
    global recording_count
    camera = cv2.VideoCapture(0)  # Use webcam

    # Variables for motion detection and recording
    motion_detected = False
    motion_start_time = None
    recording = False
    recording_start_time = None
    max_recording_duration = 20  # Recording duration in seconds
    min_motion_duration = 2  # Minimum motion duration to start recording

    frames_list = []
    video_writer = None
    video_file_name = None

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
        contour, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        is_motion_detected = False

        for contours in contour:
            if cv2.contourArea(contours) < 8000:
                continue
            (x, y, w, h) = cv2.boundingRect(contours)
            cv2.rectangle(frame_1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            is_motion_detected = True

        if is_motion_detected:
            if not motion_detected:
                motion_detected = True
                motion_start_time = time.time()
            elif time.time() - motion_start_time >= min_motion_duration and not recording:
                recording = True
                recording_start_time = time.time()
                video_file_name = os.path.join(save_directory, f'recording_{recording_count}.mp4')
                recording_count += 1
                print(f"Recording started: {video_file_name}")
                
                # Initialize VideoWriter
                height, width, _ = frame_1.shape
                video_writer = cv2.VideoWriter(video_file_name, cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))
        else:
            motion_detected = False
            motion_start_time = None

        # Store frames if recording
        if recording:
            video_writer.write(frame_1)

            # Stop recording after max_recording_duration seconds
            if time.time() - recording_start_time >= max_recording_duration:
                recording = False
                print(f"Recording stopped: {video_file_name}")
                video_writer.release()
                video_writer = None

        detection_status = "MOTION DETECTED" if is_motion_detected else "STABLE"
        cv2.putText(frame_1, f"STATUS: {detection_status}", (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()

