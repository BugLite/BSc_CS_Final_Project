import cv2
from app_ats.quadrant import drawLines

def camera():
    camera = cv2.VideoCapture(0)
    print(f"Camera feed activated!")

    while True:
        check, frame = camera.read()

        if not check:
            break

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as part of a streaming response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
