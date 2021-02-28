import os
import cv2

class EventsHandler():
    def __init__(self, captureManager, windowManager, blurFilter, edgeDetectionFilter, keypressCallback = None):
        self._captureManager = captureManager
        self._windowManager = windowManager
        self._blurFilter = blurFilter
        self._edgeDetectionFilter = edgeDetectionFilter

        self._blurFilterOn = False
        self._edgeDetectionFilterOn = False
        self._keypressCallback = keypressCallback




