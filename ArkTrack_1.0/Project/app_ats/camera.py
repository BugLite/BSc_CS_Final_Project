import cv2

def camera():
    """
    Function `camera` provides web-based streaming capability for the surveillance system.
    """
    camera = cv2.VideoCapture(0) # initialising webcam 
    
    while True:
        # capturing video frames
        captured, frame = camera.read() 
    
        # exit loop if frame not 'captured' successfully
        if not captured:
            break

        # encoding the captured frames as JPEG images
        ret, buffer = cv2.imencode('.jpg', frame)
        # converting the encoded JPEG images to bytes format
        frame = buffer.tobytes()

        # yeilding the encoded frames for web-based streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
