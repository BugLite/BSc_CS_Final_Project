# Import openCV library
import cv2

# Function that sets up the live feed
def live_feed():
    # VideoCapture(0) - Captures video from webcam
    camera = cv2.VideoCapture(0)
    

    while camera.isOpened():
        # Check if frames are read successfully
        check, frame = camera.read()
        
        # Incase of unsuccessful read break the code
        if not check:
            break

        # Display the applied motion detection footage in window
        cv2.imshow('Live Feed', frame)
       
        # Exit window is 'Spacebar' is pressed
        if cv2.waitKey(100) == 32:
            break
    
    # Release memory and close windows    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    live_feed()
