import cv2


class BackgroundProcessing:
    def __init__(self):
        self.mog2 = cv2.createBackgroundSubtractorMOG2()
        self.knn = cv2.createBackgroundSubtractorKNN()

    def apply_knn(self, frame):
        front = self.mog2.apply(frame)
        cv2.imshow("s", front)
