import cv2
import numpy as np

capture = cv2.VideoCapture('test.MOV')
while capture.isOpened():

    ret, frame =capture.read()

    img = frame
    scale_percent = 60
    w = int(img.shape[1] * scale_percent / 100)
    h = int(img.shape[0] * scale_percent / 100)
    dim = (w, h) 
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    frame = resized

    blurred_frame = cv2.GaussianBlur(frame, (5,5), 0) #Gaussian blur 

    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([38, 86, 0])
    upper_color = np.array([121, 255,255])
    mask=cv2.inRange(hsv, lower_color, upper_color)
    contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            cv2.drawContours(frame,contour,-1,(0,255,0),3)

    cv2.imshow('',frame)
    if cv2.waitKey(30) & 0xFF ==ord('q'):
        break
capture.release()
cv2.destroyAllWindows()