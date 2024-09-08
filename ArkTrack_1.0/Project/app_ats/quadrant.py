import cv2

def identifyArea(frame, x, y):
    """
    The `identifyArea` function is constructed to help determine the position of a detected object on screen.
    The positions can include - Top left, Top right, Bottom left, Bottom right and Center
    """
    # extracting the dimensions of frame
    frameHeight, frameWidth, _ = frame.shape
    # defining the center of the frames
    centerScreen_x, centerScreen_y = frameWidth // 2, frameHeight // 2

    # determining the location of object on screen
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
    else:
        # default case
        detected_area = "Unkown"

    return detected_area

def drawLines(frame):
    """
    The `drawLines` functions simply draws an x/y axis lines on screen to split into 4 quadrants.
    """
    # extracting the dimensions of frame
    frameHeight, frameWidth, _ = frame.shape
    # defining the center of the frames
    centerScreen_x, centerScreen_y = frameWidth // 2, frameHeight // 2

    # drawing the quadrant lines to screen
    cv2.line(frame, (centerScreen_x, 0), (centerScreen_x, frameHeight), (255, 255, 255), 1)
    cv2.line(frame, (0, centerScreen_y), (frameWidth, centerScreen_y), (255, 255, 255), 1)
