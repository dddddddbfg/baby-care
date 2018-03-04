import numpy as np
import cv2

import random

windowName1 = "binary"
minH = 7
maxH = 26
minS = 25
maxS = 100
minV = 145
maxV = 255
cv2.namedWindow(windowName1)


def nothing(value):
    pass


cv2.createTrackbar("maxH", windowName1, maxH, 255, nothing)
cv2.createTrackbar("minH", windowName1, minH, 255, nothing)
cv2.createTrackbar("maxS", windowName1, maxS, 255, nothing)
cv2.createTrackbar("minS", windowName1, minS, 255, nothing)
cv2.createTrackbar("maxV", windowName1, maxV, 255, nothing)
cv2.createTrackbar("minV", windowName1, minV, 255, nothing)


def binary(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    hsv = cv2.inRange(hsv, np.array([minH, minS, minV]), np.array([maxH, maxS, maxV]))
    return hsv


def blur(frame):
    blur_size = 3
    element_size = 3
    hsv = cv2.medianBlur(frame, blur_size)
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * element_size + 1, 2 * element_size + 1),
                                        (element_size, element_size))
    return cv2.dilate(hsv, element)


def add_contour(origin, frame):
    _, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_id = 0
    max_area = 0
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > max_area:
            max_id = i
            max_area = cv2.contourArea(contours[i])
    if max_area < 1000:
        return None, None
    cv2.drawContours(origin, contours, max_id, (0, 255, 0), 1)

    M = cv2.moments(contours[max_id])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    center = (cx, cy)
    cv2.circle(origin, center, 7, (255, 0, 255), -1)

    return contours[max_id], center


def finger(origin, contour):
    # finger detect
    hull = cv2.convexHull(contour, returnPoints=False)
    # print(cv2.isContourConvex(hull), len(hull))

    defects = cv2.convexityDefects(contour, hull)
    fingertips = []
    for i in range(len(defects)):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        cv2.line(origin, start, end, [0, 0, 255], 2)
        if is_acute_angle((start[0] - far[0], start[1] - far[1]),
                          (end[0] - far[0], end[1] - far[1])):
            add_tip(fingertips, start)
            add_tip(fingertips, end)
            # if len(fingertips) is 0 or distance2(fingertips[len(fingertips) - 1], start) < 100:
            #     fingertips.append(start)
            # fingertips.append(end)

    # draw finger tips
    for p in fingertips:
        cv2.circle(origin, p, 5, [255, 0, 0])

    return fingertips


# cv2.drawContours(origin, hull, -1, (0, 0, 255), 3)


def add_tip(tips, toadd):
    for tip in tips:
        dis = distance2(tip, toadd)
        if dis < 500:
            return

    tips.append(toadd)


def distance2(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return x * x + y * y


def cam(cap):
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    ret_img = np.zeros((height, width, 3), np, np.uint8)
    start = False
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # update HSV
        global maxH, minH, maxV, minV, maxS, minS
        maxH = cv2.getTrackbarPos('maxH', windowName1)
        minH = cv2.getTrackbarPos('minH', windowName1)
        maxV = cv2.getTrackbarPos('maxV', windowName1)
        minV = cv2.getTrackbarPos('minV', windowName1)
        maxS = cv2.getTrackbarPos('maxS', windowName1)
        minS = cv2.getTrackbarPos('minS', windowName1)

        # get key and react
        key = cv2.waitKey(30)
        if key & 0xFF == ord(' '):
            # cv2.imwrite(str(random.random()) + '.jpg', frame)
            if start:
                start = False

            else:
                start = True
        elif key >= 0:
            break

        # Get hands in HSV vision
        hsv = binary(frame)

        # Blur
        hsv2 = blur(hsv)

        # Find finger
        contour, center = add_contour(frame, hsv2)
        if contour is not None:
            fingertips = finger(frame, contour)

        cv2.imshow("binary", hsv)
        cv2.imshow("blurred", hsv2)
        cv2.imshow("origin image", frame)


    # When everything done, release the capture
    cap.release()


def img():
    image = cv2.imread("test-data/good.jpg")
    p1 = binary(image)
    p2 = blur(p1)
    contour = add_contour(image, p2)
    if contour is not None:
        fingertips = finger(image, contour)

    cv2.imshow(windowName1, p2)
    cv2.imshow("origin image", image)
    cv2.waitKey(0)


def is_acute_angle(l1, l2):
    return (l1[0] * l2[0] + l1[1] * l2[1]) > 0


cam(cv2.VideoCapture(1))

cv2.destroyAllWindows()
