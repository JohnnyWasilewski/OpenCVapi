import cv2
from managers import CaptureManager, WindowManager
from eventsHandler import EventsHandler


class Main:
    def __init__(self):
        self._windowManager = WindowManager('app')
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, True)
        self._eventsHandler = EventsHandler(self._captureManager, self._windowManager)

    def run(self):
        self._windowManager.create_window()
        while self._windowManager.is_window_created:
            self._captureManager.enter_frame()
            self._eventsHandler.process_events()
            self._captureManager.exit_frame()


if __name__ == '__main__':
    Main().run()
