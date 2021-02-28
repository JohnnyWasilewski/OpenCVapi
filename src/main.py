import cv2
from managers import CaptureManager, WindowManager
from filters import BlurFilter, EdgeDetectionFilter
from eventsHandler import EventsHandler
import os

class main():
    def __init__(self):
        self._windowManager = WindowManager('app',
                                            self.listenKeybord)
        self._captureManager = CaptureManager(cv2.VideoCapture(0),
                                              self._windowManager,
                                              True)
        self._blurFilter = BlurFilter()
        self._blurFilterOn = False
        self._edgeDetectionFilterOn = False
        self._edgeDetectionFilter = EdgeDetectionFilter()
        self._eventsHandler = EventsHandler(self._captureManager,
                                            self._windowManager,
                                            self._blurFilter,
                                            self._edgeDetectionFilter)

    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
#            self._captureManager.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            self._windowManager.processEvents()
#            self._eventsHandler().executeEvents()
            if self._edgeDetectionFilterOn:
                frame = self._captureManager.frame
                self._captureManager.frame = self._edgeDetectionFilter.apply(src=frame)
            if self._blurFilterOn:
                a = self._captureManager.frame
                self._captureManager.frame = self._blurFilter.apply(src=a)

            self._captureManager.exitFrame()
            # TODO dadac rogi losia
    def listenKeybord(self, keycode):
        if keycode == 32:
            self._captureManager.writeImage('/home/johny/Documents/python3/screenshot.png')
        elif keycode == 9:
            if not self._captureManager.isWritingVideo:
                print('start recording')
                self._captureManager.startWritingVideo(os.path.join('/home/johny/Documents/python3/screencast.avi'))
            else:
                self._captureManager.stopWritingVideo()
                print('stop recording')
        elif keycode == 27:
            self._windowManager.destroyWindow()

        elif keycode == ord('b'):  # blur filter
            self._blurFilterOn = not self._blurFilterOn

        elif keycode == ord('e'): # edge filter
            self._edgeDetectionFilterOn = not self._edgeDetectionFilterOn

if __name__ == '__main__':
    main().run()