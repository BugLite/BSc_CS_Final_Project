# Import openCV library
import cv2
import pygame

# Initialize pygame
pygame.init()

# Function to play the beep sound
def play_beep():
    pygame.mixer.music.load("/Users/oxon/Documents/CM3070 Final Project/FP Midterm/FP Prototype/beep.mp3")
    pygame.mixer.music.play()

# Fuction to detect motion
def motion_detect():
    # VideoCapture(0) - Captures video from webcam
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        # Check if frames are read successfully
        check, frame_1 = camera.read()
        check, frame_2 = camera.read()

        # Incase of unsuccessful read break the code
        if not check:
            break

        # Calculating the Frame Difference using cv2.absdiff()   
        frame_diff = cv2.absdiff(frame_1, frame_2)
        # Converting from absolute difference image to grayscale using cv2.cvtColor
        grayscale = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        # Applying GaussianBlur Blur using cv2.GaussianBlur()
        gaus_blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        # Applying a Threshold using cv2.threshold()
        _, threshold = cv2.threshold(gaus_blur, 15, 255, cv2.THRESH_BINARY)
        # Adjust the number of dilation iterations using cv2.dilate()
        dilation = cv2.dilate(threshold, None, iterations=5)
        # Finding contours in the webcam feed using cv2.findContours()
        contour, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Set to False by default in case of no movements detected
        is_motion_detected = False

        # Draw rectangles and Display status if movement is detected
        for contours in contour:
            if cv2.contourArea(contours) < 8000:
                continue
            (x,y,w,h) = cv2.boundingRect(contours)
            # Draw Rectangles around detected objects
            cv2.rectangle(frame_1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            # Flag set to Truew
            is_motion_detected = True
        
        # Status messages if Motion detected
        if is_motion_detected:
            detection_status = "MOTION DETECTED"
            text_color = (0, 0, 255)
            # Play beep sound if motion is detected
            # play_beep()
        else:
            detection_status = "STABLE"
            text_color = (217, 10, 10)

        # Text displays
        cv2.putText(frame_1, "LIVE STATUS: {}".format(detection_status), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, text_color, 2)
        cv2.putText(frame_1, "Press Spacebar to Exit! ", (10, 90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

        # Display the applied motion detection footage in window
        cv2.imshow("Detector_1 Live Feed", frame_1)

        # Exit window is 'Spacebar' is pressed
        if cv2.waitKey(100) == 32:
            break
    
    # Release memory and close windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    motion_detect()