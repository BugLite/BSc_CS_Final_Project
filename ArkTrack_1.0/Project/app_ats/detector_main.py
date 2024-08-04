import cv2

# Function to play the beep sound (TBC)

# Function to generate frames with motion detection
def gen_frames():
    camera = cv2.VideoCapture(0)  # Use webcam

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
            detection_status = "MOTION DETECTED"
            text_color = (0, 0, 255)
        else:
            detection_status = "STABLE"
            text_color = (217, 10, 10)

        cv2.putText(frame_1, "LIVE STATUS: {}".format(detection_status), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, text_color, 2)
        cv2.putText(frame_1, "Press Spacebar to Exit!", (10, 90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
