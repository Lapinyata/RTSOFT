import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
import time
from collections import deque


def moving_average(x,n):   #weighted moving average function
    # n - smoothing order
    ret = np.cumsum(x, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def smoothing(queue):      #trajectory smoothing function
    list_x = []     # list of x-coordinates of every center-point
    list_y = []     # list of y-coordinates of every center-point
    list_of_center_points = list(queue)

    #Loop (see below) that  fills lists of x/y coordinates
    for center_point in list_of_center_points:
        list_x = np.append(list_x, list(center_point)[0])
        list_y = np.append(list_y, list(center_point)[1])

    x_avg = moving_average(list_x, min([len(list_x),8]))
    y_avg = moving_average(list_y, min([len(list_y),8]))

    queue_of_avg = deque(maxlen=100)

    for i in range(0,len(x_avg)):
        queue_of_avg.append((int(x_avg[i]), int(y_avg[i])))

    return queue_of_avg

def trajectory_drowing(queue):
    for i in range(1,len(queue)):
                cv2.line(frame, queue[i - 1], queue[i], (0,255,0), 3)
    cv2.imshow('_X_', frame)

if __name__ == "__main__":

    queue = deque(maxlen=100)   # something like list that allows us to add/delete element from start or from end
    capture = cv2.VideoCapture('test.MOV')

    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("MAIN") #client creation
    client.connect(mqttBroker)  #connect with broker(localhost)

    counter = 0
    while capture.isOpened():
       
        ret, frame = capture.read()

        #resizing image
        img = frame
        scale_percent = 60
        w = int(img.shape[1] * scale_percent / 100)
        h = int(img.shape[0] * scale_percent / 100)
        dim = (w, h) 
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        frame = resized

        #getting contours of image
        blurred_frame = cv2.GaussianBlur(frame, (5,5), 0) #Gaussian blur
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
        lower_color = np.array([38, 86, 0])
        upper_color = np.array([121, 255,255])
        mask=cv2.inRange(hsv, lower_color, upper_color)
        contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #in that loop (see below) squares are built, their centers are determined and 
        #these centers are entered into deque 
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10000:
                x,y,w,h = cv2.boundingRect(contour) #function that get some info about minimal rectangle border of image
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,200,200),2) # draw rectangles
                center=(int(x+w/2),int(y+h/2)) # count center
                queue.appendleft(center) # add center to track 

        queue_of_avg = smoothing(queue)
        trajectory_drowing(queue_of_avg)

        counter += 1
        if counter % 10 == 0:
            x_avg = list(queue_of_avg[0])[0]
            y_avg = list(queue_of_avg[0])[1]
            message = json.dumps({"x":x_avg, "y": y_avg})
            client.publish("TEST", message)

        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()