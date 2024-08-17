import cv2
import time
import ffmpeg
import numpy as np
import os
from datetime import timedelta
from django.utils.timezone import now
from app_ats.models import RecordedVideo
from django.conf import settings
from django.core.mail import send_mail

# Define the directory where you want to save the recordings
save_directory = os.path.join(settings.MEDIA_ROOT, 'recordings')
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
    video_file_name = None
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
            if not motion_detected:
                motion_detected = True
                motion_start_time = time.time()
            elif time.time() - motion_start_time >= min_motion_duration and not recording:
                recording = True
                recording_start_time = time.time()
                video_file_name = os.path.join(save_directory, f'recording_{recording_count}.mp4')
                recording_count += 1
                print(f"Recording started: {video_file_name}")
        else:
            motion_detected = False
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
                print(f"Recording stopped: {video_file_name}")
                # Saving video using ffmpeg
                out = ffmpeg.input('pipe:', framerate=20, format='rawvideo', pix_fmt='bgr24', s=f'{frame_1.shape[1]}x{frame_1.shape[0]}')
                out = ffmpeg.output(out, video_file_name, pix_fmt='yuv420p')
                out = ffmpeg.overwrite_output(out)
                out.run(input=np.concatenate(frames_list, axis=0).tobytes())
                frames_list = []

                # Save video metadata to the database
                captured_video = RecordedVideo.objects.create(
                    title=os.path.basename(video_file_name),
                    # file path is relative to 'MEDIA_ROOT' in Database
                    file_path=os.path.relpath(video_file_name, start=settings.MEDIA_ROOT),
                    duration=timedelta(seconds=max_recording_duration),
                    recorded_timestamp=now()
                )
                print(f"Video saved and metadata stored: {video_file_name}")

                # Send an email notification
                send_mail(
                    subject='Motion Detected',
                    message=f"Motion Detected\nRecording Title: {captured_video.title}\nTimestamp: {captured_video.recorded_timestamp}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['hyder.devop@gmail.com'],
                    fail_silently=False,
                )
                print("Email notification sent.")

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
