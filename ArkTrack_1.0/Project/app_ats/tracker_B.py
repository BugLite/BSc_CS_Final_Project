import cv2

def generate_motion_frames():
    """
    The `generate_motion_frames` function is the secondary motion detection and tracking algorithm based off the background subtraction methods.
    The function uses the BitwiseXOR technique to separate an object from the background effectively highlighting the subject against a dark black
    background. This function does not include additional features such as recording or alerts since it's primary goal is to run in-support of the
    original Tracker A surveillance feed.
    """
    
    # initializing webcam
    camera = cv2.VideoCapture(0)
    # intializing frames
    last_frame_1 = None
    last_frame_2 = None
    
    # capturing and storing frames
    while True:
        check, current_frame = camera.read()
        if not check:
            break

        # applying the bitwiseXOR algorithm
        if last_frame_2 is not None:
            motion_frame = cv2.bitwise_xor(cv2.absdiff(current_frame, last_frame_1), cv2.absdiff(last_frame_1, last_frame_2))

            # encoding the motion frames as JPEG
            ret, buffer = cv2.imencode('.jpg', motion_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        last_frame_2 = last_frame_1
        last_frame_1 = current_frame

    camera.release()
