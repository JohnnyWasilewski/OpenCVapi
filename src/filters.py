import numpy as np
import cv2


class Filters:
    def __init__(self, kernel):
        self._kernel = kernel

    def apply(self, src):
        return cv2.filter2D(src=src, ddepth=-1, kernel=self._kernel)


class BlurFilter(Filters):
    def __init__(self):
        kernel = np.array([[1, 1, 1], [1, 8, 1], [1, 1, 1]])
        super().__init__(kernel)


class EdgeDetectionFilter(Filters):
    def __init__(self):
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        super().__init__(kernel)
