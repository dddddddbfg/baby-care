import numpy as np
import math
import cv2


def motion_detect(origin, frame_gray, prev_frame_gray):

    if prev_frame_gray is not None:
        diff = cv2.absdiff(prev_frame_gray, frame_gray)
        diff_binary = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY_INV)[1]
        # dilation
        diff_binary = cv2.dilate(diff_binary, None, iterations=2)
        # print(get_rectangle(diff_binary))

        cv2.imshow("diff", diff_binary)

        x1, y1, x2, y2 = (len(origin[0]), len(origin), 0, 0)
        (_, cnts, _) = cv2.findContours(diff_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        for contour in cnts:
            if cv2.contourArea(contour) < 500 or cv2.contourArea(contour) >= 30600:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)

            x1 = min(x, x1)
            y1 = min(y, y1)
            x2 = max(x + w, x2)
            y2 = max(y + h, y2)
        if x2 != 0:
            cv2.rectangle(origin, (x1, y1), (x2, y2), (0, 255, 0), 3)
            print(x1, y1, x2, y2)
            return (x1, y1, x2, y2)


if __name__ is '__main__':
    cap = cv2.VideoCapture(0)

    prev_frame_gray = None
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # frame = cv2.resize(frame, (256, 256))

        frame_gray = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)  # blur image to reduce noise and increase accuracy

        motion_detect(frame, frame_gray, prev_frame_gray)

        cv2.imshow("frame", frame)

        prev_frame_gray = frame_gray

        # ops
        key = cv2.waitKey(30) & 0xff
        if key == ord('q'):  # quit
            break
        elif key == ord(' '):  # pause or continue
            while cv2.waitKey(30) & 0xff != ord(' '):
                pass

    cap.release()
    cv2.destroyAllWindows()