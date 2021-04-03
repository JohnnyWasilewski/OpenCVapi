import cv2
import numpy as np


class BackgroundProcessing:
    def __init__(self):
        self._mog2 = cv2.createBackgroundSubtractorMOG2()
        self._knn = cv2.createBackgroundSubtractorKNN()

    def apply_background_detector(self, frame):
        mog2 = self._mog2.apply(frame)
        knn = self._knn.apply(frame)
        backgrounds = np.hstack((mog2, knn))
        cv2.imshow("background", backgrounds)
        # return frame[knn]
