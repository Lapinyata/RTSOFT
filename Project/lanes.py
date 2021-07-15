import cv2 as cv
import numpy as np


def canny(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    blur = cv.GaussianBlur(img, (5,5), 0)
    return cv.Canny(blur, 50, 150)

def make_coordinates(image, line_parameters):   #функция, задающая координаты прямой
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):     #функция усреднения линий
    left_fit = []
    right_fit = []
    while lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
        left_fit_average = np.average(left_fit, axis=0)
        left_line = make_coordinates(image, left_fit_average)
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinates(image, right_fit_average)
        return np.array([left_line, right_line])

def display_lines(image, lines):    #функция, отображающая линии
    line_image = np.zeros_like(image)
    y_g = 300
    x_g = 100
    if lines is not None:
        dots = list()
        for x1, y1, x2, y2 in lines:
            cv.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 4)
            a1 = y1-y2
            b1 = x2-x1
            c1 = a1*x1 + b1*y1
            a2 = y_g-y_g
            b2 = x_g+440-x_g
            c2 = a2*x_g + b2*y_g
            det = a1*b2 - a2*b1
            if det==0:
                print("error")
            else:
                x1 = (b2*c1-b1*c2)/det
                y1 = (a1*c2-a2*c1)/det
                dots.append(int(x1))
                dots.append(int(y1))
                #x = int(x1)
                #y = int(y1)
                #cv.circle(line_image, (x,y), 10, (255,0, 0), -1)
        cv.line(line_image, (x_g, y_g), (x_g + 100, y_g), (0, 255, 0), 4)
        cv.line(line_image, (x_g + 100, y_g), (x_g + 180 , y_g), (0, 255, 255), 4)
        cv.line(line_image, (x_g + 180, y_g), (x_g + 260, y_g), (0, 0, 255), 4)
        cv.line(line_image, (x_g + 260, y_g), (x_g + 340, y_g), (0, 255, 255), 4)
        cv.line(line_image, (x_g + 340, y_g), (x_g + 440, y_g), (0, 255, 0), 4)
        cv.circle(line_image, (dots[0],dots[1]), 7, (255,36, 4), -1) 
        cv.circle(line_image, (dots[2],dots[3]), 7, (255,36, 4), -1)
        if (dots[0]>(x_g+100))and(dots[0]<=x_g+180):
            cv.line(line_image, (x_g + 200, y_g-250), (x_g + 230 , y_g-280), (0, 255, 255), 10)
            cv.line(line_image, (x_g + 200, y_g-250), (x_g + 230 , y_g-220), (0, 255, 255), 10)
        elif (dots[0]>(x_g+180))and(dots[0]<=x_g+260):
            cv.line(line_image, (x_g + 190, y_g-250), (x_g + 220 , y_g-280), (0, 0, 255), 10)
            cv.line(line_image, (x_g + 190, y_g-250), (x_g + 220 , y_g-220), (0, 0, 255), 10)
            cv.line(line_image, (x_g + 210, y_g-250), (x_g + 240 , y_g-280), (0, 0, 255), 10)
            cv.line(line_image, (x_g + 210, y_g-250), (x_g + 240 , y_g-220), (0, 0, 255), 10)
        elif (dots[2]>=(x_g+260))and(dots[2]<x_g+340):
            cv.line(line_image, (x_g + 200, y_g-280), (x_g + 230 , y_g-250), (0, 255, 255), 10)
            cv.line(line_image, (x_g + 200, y_g-220), (x_g + 230 , y_g-250), (0, 255, 255), 10)
        elif (dots[2]>(x_g+180))and(dots[2]<=x_g+260):
            cv.line(line_image, (x_g + 190, y_g-280), (x_g + 220 , y_g-250), (0, 0, 255), 10)
            cv.line(line_image, (x_g + 190, y_g-220), (x_g + 220 , y_g-250), (0, 0, 255), 10)
            cv.line(line_image, (x_g + 210, y_g-280), (x_g + 240 , y_g-250), (0, 0, 255), 10)
            cv.line(line_image, (x_g + 210, y_g-220), (x_g + 240 , y_g-250), (0, 0, 255), 10)
    return line_image


def mask(image):      #функция, накладывающая маску на изображение для того, чтобы машины в соседнем ряду (и прочее) не мешали обработке
    height = image.shape[0]
    polygons = np.array([(250, height//1.7), (640-250, height//1.7), (570, 300), (100, 300)])  #640 x 360
    mask = np.zeros_like(image)
    cv.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image