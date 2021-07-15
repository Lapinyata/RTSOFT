import cv2 as cv
import numpy as np
import lanes

video = cv.VideoCapture("test_driving3.mp4")

if not video.isOpened():
    print("error while opening the video")

cv.waitKey(1)

while video.isOpened():
    _, frame = video.read()

    #cv.namedWindow("_X_", cv.WINDOW_NORMAL)
    #cv.resizeWindow("_X_",640,360)
    copy_img = np.copy(frame)
    try:
        frame = lanes.canny(frame)
        frame = lanes.mask(frame)
        lines = cv.HoughLinesP(frame, 2, np.pi/180, 100, np.array([()]), minLineLength=20, maxLineGap=5)
        averaged_lines = lanes.average_slope_intercept(frame, lines)
        line_image = lanes.display_lines(copy_img, averaged_lines)
        combo = cv.addWeighted(copy_img, 0.8, line_image, 0.5, 1)
        cv.imshow('_X_', combo)
    except:
        pass

    if cv.waitKey(1) & 0xFF ==ord('q'):
        break
video.release()
cv.destroyAllWindows()