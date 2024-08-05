# myapp/motion_detection.py
import cv2

def generate_motion_frames():
    camera = cv2.VideoCapture(0)  # Initialize the camera here
    last_frame_1 = None
    last_frame_2 = None
    
    while True:
        check, current_frame = camera.read()
        if not check:
            break

        if last_frame_2 is not None:
            motion_frame = cv2.bitwise_xor(cv2.absdiff(current_frame, last_frame_1), cv2.absdiff(last_frame_1, last_frame_2))

            # Encode the motion frame as JPEG
            ret, buffer = cv2.imencode('.jpg', motion_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        last_frame_2 = last_frame_1
        last_frame_1 = current_frame

    camera.release()  # Release the camera resource when done
