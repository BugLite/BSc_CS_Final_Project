import cv2

def gen_frames():
    camera = cv2.VideoCapture(0)  # Use webcam

    while camera.isOpened():
        check, frame_1 = camera.read()
        check, frame_2 = camera.read()

        if not check:
            break

        # Get the dimensions of the frame
        height, width, _ = frame_1.shape

        # Define the center points to divide the frame into four parts
        center_x, center_y = width // 2, height // 2

        # Calculate the difference between two consecutive frames
        frame_diff = cv2.absdiff(frame_1, frame_2)
        grayscale = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        gaus_blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        _, threshold = cv2.threshold(gaus_blur, 15, 255, cv2.THRESH_BINARY)
        dilation = cv2.dilate(threshold, None, iterations=5)
        contour, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        is_motion_detected = False
        detected_area = ""

        for contours in contour:
            if cv2.contourArea(contours) < 8000:
                continue

            # Draw rectangle around the detected motion
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
            elif x >= center_x and y >= center_y:
                detected_area = "Bottom Right"

        if is_motion_detected:
            detection_status = f"MOTION DETECTED in {detected_area}"
            text_color = (0, 0, 255)
        else:
            detection_status = "STABLE"
            text_color = (217, 10, 10)

        cv2.putText(frame_1, "LIVE STATUS: {}".format(detection_status), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, text_color, 2)

        # Draw the quadrant lines
        cv2.line(frame_1, (center_x, 0), (center_x, height), (255, 255, 255), 1)
        cv2.line(frame_1, (0, center_y), (width, center_y), (255, 255, 255), 1)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame_1)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
    cv2.destroyAllWindows()
