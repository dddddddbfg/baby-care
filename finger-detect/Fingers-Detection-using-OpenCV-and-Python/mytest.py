import numpy as np
import cv2


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
windowName = "Fingertip detection"
minH = 0
maxH = 30
minS = 30
maxS = 90
minV = 0
maxV = 190
cv2.namedWindow(windowName)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    # Get hands in HSV vision
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    hsv = cv2.inRange(hsv, np.array([minH, minS, minV]), np.array([maxH, maxS, maxV]))

    # Blur
    blurSize = 3
    elementSize = 3
    # cv2.medianBlur(hsv, hsv, blurSize)
    # element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 2 * elementSize + 1,
    # 2 * elementSize + 1, (elementSize, elementSize))
    # cv2.dilate(hsv, hsv, element)
    cv2.imshow(windowName, hsv)

    if cv2.waitKey(30) >= 0:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
