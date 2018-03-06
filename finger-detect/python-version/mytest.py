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


def gray(frame):
    frame_gray = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)  # blur image to reduce noise and increase accuracy
    return frame_gray


def rgb2hsv(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    hsv = cv2.GaussianBlur(hsv, (21, 21), 0)  # blur image to reduce noise and increase accuracy
    return hsv


def blur(frame):
    blur_size = 3
    element_size = 3
    hsv = cv2.medianBlur(frame, blur_size)
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * element_size + 1, 2 * element_size + 1),
                                        (element_size, element_size))
    return cv2.dilate(hsv, element)


def calculate_center(contour):
    m = cv2.moments(contour)
    cx = int(m['m10'] / m['m00'])
    cy = int(m['m01'] / m['m00'])
    center = (cx, cy)
    return center


def add_contour(origin, frame, p1, p2):
    # todo
    if p1 is None and p2 is None:
        return None, None

    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_id = 0
    max_area = 0
    max_center = None
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > max_area:
            center = calculate_center(contours[i])
            if p1[0] <= center[0] <= p2[0] and p1[1] <= center[1] <= p2[1]:
                max_id = i
                max_area = cv2.contourArea(contours[i])
                max_center = center

    if max_area < 1000 or max_center is None:
        return None, None

    cv2.drawContours(origin, contours, max_id, (0, 255, 0), 1)

    return contours[max_id], max_center

#
# def add_center(origin, contour):
#     # find the center
#     m = cv2.moments(contour)
#     cx = int(m['m10'] / m['m00'])
#     cy = int(m['m01'] / m['m00'])
#     center = (cx, cy)
#     return center


def finger(origin, contour):  # not good
    # finger detect
    hull = cv2.convexHull(contour, returnPoints=False)

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

    # draw finger tips
    for p in fingertips:
        cv2.circle(origin, p, 5, [255, 0, 0])

    return fingertips


def motion_detect(origin, frame_gray, prev_frame_gray):
    if prev_frame_gray is None:
        return None, None

    diff = cv2.absdiff(prev_frame_gray, frame_gray)
    diff_binary = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY_INV)[1]
    # dilation
    diff_binary = cv2.dilate(diff_binary, None, iterations=2)

    x1, y1, x2, y2 = (len(origin[0]), len(origin), 0, 0)
    cv2.imshow('diff_binary', diff_binary)
    (_, cnts, _) = cv2.findContours(diff_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

    for contour in cnts:
        if cv2.contourArea(contour) < 300 or cv2.contourArea(contour) >= 30600:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)

        x1 = min(x, x1)
        y1 = min(y, y1)
        x2 = max(x + w, x2)
        y2 = max(y + h, y2)

    if x2 != 0:
        cv2.rectangle(origin, (x1, y1), (x2, y2), (0, 255, 0), 3)
        print(x1, y1, x2, y2)
        return (x1, y1), (x2, y2)

    return None, None


def add_tip(tips, to_add):
    for tip in tips:
        dis = distance2(tip, to_add)
        if dis < 500:
            # tips.remove(tip)
            # tips.append(((tip[0] + to_add[0]) / 2, (tip[1] + to_add[1]) / 2))
            return

    tips.append(to_add)


def distance2(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return x * x + y * y


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def blank_img(height, width):
    ret = np.zeros((height, width, 3), np.uint8)
    ret[:, :] = WHITE
    return ret


def cam(cap):
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    ret_img = blank_img(height, width)
    start = False
    prev_center = None
    prev_frame_gray = None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

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
                cv2.imwrite(str(random.random()) + '.jpg', ret_img)
                ret_img = blank_img(height, width)

            else:
                start = True
        elif key >= 0:
            break

        # Get hands in HSV vision
        frame_hsv = rgb2hsv(frame)

        frame_binary = cv2.inRange(frame_hsv, np.array([minH, minS, minV]), np.array([maxH, maxS, maxV]))

        # Blur
        frame_binary_blur = blur(frame_binary)

        frame_gray = gray(frame)
        # print(frame_gray)
        # print(prev_frame_gray)
        p1, p2 = motion_detect(frame, frame_gray, prev_frame_gray)

        # Find hand contour
        contour, center = add_contour(frame, frame_binary_blur, p1, p2)
        cv2.circle(frame, center, 7, (255, 0, 255), -1)
        if contour is not None:
            fingertips = finger(frame, contour)

            # # use center to draw a picture
            # center = add_center(frame, contour)

            if start and prev_center is not None and distance2(prev_center, center) < 2 << 20:
                cv2.line(ret_img, center, prev_center, BLACK, 5)
            prev_center = center

        # add center in drawing image
        show_img = np.copy(ret_img)
        cv2.circle(show_img, prev_center, 3, color=(255, 255, 0), thickness=5)

        # record prev gray frame
        prev_frame_gray = frame_gray

        cv2.imshow("return img", show_img)
        cv2.imshow("blurred", frame_binary_blur)
        cv2.imshow("origin image", frame)

    # When everything done, release the capture
    cap.release()


# def img():
#     image = cv2.imread("test-data/good.jpg")
#     p1 = binary(image)
#     p2 = blur(p1)
#     contour = add_contour(image, p2)
#     if contour is not None:
#         fingertips = finger(image, contour)
#
#     cv2.imshow(windowName1, p2)
#     cv2.circle(image, (10, 10), 3, (0, 0, 0), 5)
#     cv2.imshow("origin image", image)
#     cv2.waitKey(0)


def is_acute_angle(l1, l2):
    return (l1[0] * l2[0] + l1[1] * l2[1]) > 0


cam(cv2.VideoCapture(0))
# img()
cv2.destroyAllWindows()
