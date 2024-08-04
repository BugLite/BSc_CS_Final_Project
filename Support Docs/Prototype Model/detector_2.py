# Import openCV library
import cv2
import pygame

# Initialize pygame
pygame.init()

# Function to detect motion
def generate_motion_frames(camera):
    # Initialise last frame variables
    last_frame_1 = None
    last_frame_2 = None
    
    # Check if webcam is correctly being read else break the code
    while True:
        check, current_frame = camera.read()
        # Incase of unsuccessful read break the code
        if not check:
            break

        # If two consecutive frames are available then calculate Motion Frames
        if last_frame_2 is not None:
            # Bitwise XOR operation (cv2.bitwise_xor()) is applied between these two absolute difference frames. 
            motion_frame = cv2.bitwise_xor(cv2.absdiff(current_frame, last_frame_1), cv2.absdiff(last_frame_1, last_frame_2))
            # The resulting motion frame is yielded, allowing the calling code to access it.
            yield motion_frame

        # Update previous frames
        last_frame_2 = last_frame_1
        last_frame_1 = current_frame

# Function to play the beep sound
def play_beep():
    pygame.mixer.music.load("/Users/oxon/Documents/FP Prototype/beep.mp3")
    pygame.mixer.music.play()

# Function to run the motion detector
def apply_motion_detection():
    # VideoCapture(0) - Captures video from webcam
    camera = cv2.VideoCapture(0)

    # Loop over all generated (yilded) motion frames
    for motion_frames in generate_motion_frames(camera):
        cv2.putText(motion_frames, "Press Spacebar to Exit! ", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        # Display the applied motion detection footage in window
        cv2.imshow("Detector_2 Live Feed", motion_frames)

        # Check if motion is detected (you can use any threshold)
        # if cv2.countNonZero(cv2.cvtColor(motion_frames, cv2.COLOR_BGR2GRAY)) > 20:
            # Play beep sound if motion is detected
            # play_beep()

        # Exit window is 'Spacebar' is pressed
        if cv2.waitKey(100) == 32:
            break

    # Release memory and close windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    apply_motion_detection()
