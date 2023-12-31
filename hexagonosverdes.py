import cv2
import numpy as np

def detect_green_hexagon(image):
    image= cv2.imread('image.jpg')
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper thresholds for green color
    lower_green = np.array([50, 100, 100])  # Adjust these values as per your requirement
    upper_green = np.array([70, 255, 255])

    # Create a mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over the contours and find hexagons
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)

        # If the contour has 6 sides (hexagon), the aspect ratio is close to 1, and the area is within a certain range, print "hexagon"
        if len(approx) == 6:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            area = cv2.contourArea(contour)
            if 0.9 <= aspect_ratio <= 1.1 and 1000 <= area <= 5000:
                return 1
            else:
                return 0










