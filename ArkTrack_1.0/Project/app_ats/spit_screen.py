import cv2

def identifyArea(frame, x, y):
    # dimensions of frame
    frameHeight, frameWidth, _ = frame.shape
    # defining the center of the frames
    centerScreen_x, centerScreen_y = frameWidth // 2, frameHeight // 2

    # Determine the quadrant
    if x < centerScreen_x and y < centerScreen_y:
        detected_area = "Top Left"
    elif x >= centerScreen_x and y < centerScreen_y:
        detected_area = "Top Right"
    elif x < centerScreen_x and y >= centerScreen_y:
        detected_area = "Bottom Left"
    elif x > centerScreen_x and y >= centerScreen_y:
        detected_area = "Bottom Right"
    elif x == centerScreen_x and y == centerScreen_y:
        detected_area = "Center"

    return detected_area

def drawLines(frame):
    # dimensions of frame
    frameHeight, frameWidth, _ = frame.shape
    # defining the center of the frames
    centerScreen_x, centerScreen_y = frameWidth // 2, frameHeight // 2

    # Draw the quadrant lines
    cv2.line(frame, (centerScreen_x, 0), (centerScreen_x, frameHeight), (255, 255, 255), 1)
    cv2.line(frame, (0, centerScreen_y), (frameWidth, centerScreen_y), (255, 255, 255), 1)
