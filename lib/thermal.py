import board
import busio
import adafruit_mlx90640
import numpy as np
import cv2

# Sources:
# https://answers.opencv.org/question/210645/detection-of-people-from-above-with-thermal-camera/
# https://www.learnopencv.com/blob-detection-using-opencv-python-c/
# https://github.com/thequicketsystem/people-counting-visual/

IMG_WIDTH, IMG_HEIGHT = 32, 24
TEMP_MIN, TEMP_MAX = 6, 20

SCALE_FACTOR = 10

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

## Blob detection parameters
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0;
params.maxThreshold = 255;

# Filter by Area.
params.filterByArea = True
params.minArea = 600
params.maxArea = 8000

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

f = [0] * (IMG_WIDTH * IMG_HEIGHT)

def get_frame_data() -> int:
    try:
        mlx.getFrame(f)
    except ValueError:
        pass

    temp_data = np.array(f).reshape((IMG_HEIGHT, IMG_WIDTH))

    temp_data = cv2.resize(temp_data, dsize=(IMG_WIDTH * SCALE_FACTOR, IMG_HEIGHT * SCALE_FACTOR))
    temp_data = cv2.normalize(temp_data, temp_data, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # drops temps that are too cold
    _, temp_data = cv.threshold(temp_data, 80, 255, cv.THRESH_TOZERO)

    # smoothes image and reduces noise while preserving edges
    temp_data = cv2.bilateralFilter(temp_data, 9, 150, 150)

    kernel = np.ones((5,5), np.uint8)

    temp_data = cv2.erode(temp_data, kernel, iterations = 1)
    temp_data = cv2.dilate(temp_data, kernel, iterations = 1)

    temp_data = cv2.morphologyEx(temp_data, cv2.MORPH_CLOSE, kernel)

    temp_data = cv2.bitwise_not(temp_data)

    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(temp_data)

    count = len(keypoints)

    # Draw circles around blobs and display count on screen
    temp_data_with_keypoints = cv2.drawKeypoints(temp_data, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Draw count of blobs inside circle and outside circle, as well as the circle itself
    cv2.putText(temp_data_with_keypoints, f"count: {count}", (10, (IMG_HEIGHT * SCALE_FACTOR) - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow("The Quicket System Demo", temp_data_with_keypoints)
    cv2.waitKey(1)

    return(count)

def get_best_of_x(x: int) -> int:
    return max([get_frame_data() for i in range(x)])
