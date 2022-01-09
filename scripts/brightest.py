import cv2

image = cv2.imread("dark_light_spot_83503_2560x1600.jpeg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

print(maxLoc)
