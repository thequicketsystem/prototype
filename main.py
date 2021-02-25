# THERMAL IMAGING DEPENDENCIES
import board
import busio
import adafruit_mlx90640
import numpy as np
import cv2
from math import sqrt

# SETUP
# ily preston xoxo

## THERMAL IMAGING SETUP
IMG_WIDTH, IMG_HEIGHT = 32, 24
TEMP_MIN, TEMP_MAX = 6, 20

SCALE_FACTOR = 10

# set up circle dimesions to simulate RFID reader detection area
circleR  = (IMG_WIDTH * SCALE_FACTOR) // 3
circleX, circleY = (IMG_WIDTH * SCALE_FACTOR) // 2, (IMG_HEIGHT * SCALE_FACTOR)  // 2

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

f = [0] * (IMG_WIDTH * IMG_HEIGHT)

while True:
    temp_data = np.empty([IMG_WIDTH, IMG_HEIGHT])

    try:
        mlx.getFrame(f)
    except ValueError:
        continue

    for y in range(IMG_HEIGHT):
        for x in range(IMG_WIDTH):
            temp_data[x, y] = f[y * IMG_WIDTH + x]  

    temp_data = cv2.resize(temp_data, dsize=(IMG_WIDTH * SCALE_FACTOR, IMG_HEIGHT * SCALE_FACTOR))
    temp_data = cv2.normalize(temp_data, temp_data, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    colorized_temp_data = cv2.applyColorMap(temp_data, cv2.COLORMAP_JET)

    temp_data = cv2.bilateralFilter(temp_data, 9, 150, 150)

    kernel = np.ones((5,5), np.uint8)

    temp_data = cv2.erode(temp_data, kernel, iterations = 1)
    temp_data = cv2.dilate(temp_data, kernel, iterations = 1)

    temp_data = cv2.morphologyEx(temp_data, cv2.MORPH_CLOSE, kernel)

    temp_data = cv2.bitwise_not(temp_data)

    # Blob detection
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 0;
    params.maxThreshold = 255;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 500
    params.maxArea = 2000

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.01

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(temp_data)

    # Determine which blobs are inside the circle and which are outside
    insideReaderRange = 0
    outsideReaderRange = 0

    for kp in keypoints:
        d = sqrt(pow(kp.pt[0] - circleX, 2) + pow(kp.pt[1] - circleY, 2))
        if d < circleR:
            insideReaderRange += 1
        else:
            outsideReaderRange += 1

