import cv2
import numpy as np

img = cv2.imread('D:/Downloads/las.png')


def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp

def countWhitePixels(img):
    img = cv2.resize(img, (640, 480))  # RESIZE
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 168])
    upper_white = np.array([172, 111, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white) 
    white_pixels = np.sum(img == 255)
    imgThres = mask_white
    h, w, c = img.shape
    points = [[100, 100], [w-100, 100], [w//2-50, h-100], [w//2+50, h-100]]  # Define specific points for warp transformation
    imgWarp = warpImg(imgThres, points, w, h)
    white_pixels = np.sum(imgWarp == 255)
    if white_pixels > 40000:
        print("1")
        return 1
    else:
        print("0")
        return 0
    




# Perform thresholding to convert the image to binary




# Count the white pixels



# Print "1" if the white pixel count is above a certain threshold









