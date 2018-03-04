import cv2
import time

capture = cv2.VideoCapture(0)

num = 0;  
while True:
    # Capture frame-by-frame
    ret, frame = capture.read()
    cv2.imshow('frame', frame)

    key = cv2.waitKey(10)  
    if key == 27:  
        break  
    if key == ord(' '):  
        num = num+1  
        filename = "frmaes_%s.jpg" % num  
        cv2.imwrite(filename,frame)  


capture.release() 
cv2.destroyAllWindows() 