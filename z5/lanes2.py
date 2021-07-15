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
    if lines is not None:
        i = 1
        for x1, y1, x2, y2 in lines:
            if i==1:
                cv.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 8)
                i+=1
            else:
                cv.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 8)
                #pts = np.array([[[pl[0], pl[1]],[pl[2],pl[3]],[x2,y2],[x1,y1]]], dtype=np.int32)
                #cv.fillPoly(line_image, pts, (202,255,191), lineType=8, shift=0, offset=None)
    return line_image


def mask(image):      #функция, накладывающая маску на изображение для того, чтобы машины в соседнем ряду (и прочее) не мешали обработке
    height = image.shape[0]
    polygons = np.array([(250, height//1.7), (640-250, height//1.7), (570, 300), (100, 300)])  #640 x 360
    mask = np.zeros_like(image)
    cv.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image
