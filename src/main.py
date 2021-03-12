import cv2
from managers import CaptureManager, WindowManager
from filters import BlurFilter, EdgeDetectionFilter
from eventsHandler import EventsHandler
from faceDetector import detect_face
import os
from prepareImg import get_face_recognition_model


class Main:
    def __init__(self):
        self._windowManager = WindowManager('app',
                                            self.listen_keyboard)
        self._captureManager = CaptureManager(cv2.VideoCapture(0),
                                              self._windowManager,
                                              True)
        self._blurFilter = BlurFilter()
        self._blurFilterOn = False
        self._edgeDetectionFilterOn = False
        self._edgeDetectionFilter = EdgeDetectionFilter()
        self._filtersTrigger = {
            'edgeDetectionFilter': False,
            'blurFilter': False,
        }
        self._eventsHandler = EventsHandler(self._captureManager,
                                            self._windowManager,
                                            self._blurFilter,
                                            self._edgeDetectionFilter,
                                            self._filtersTrigger)

    def run(self):
        self._windowManager.create_window()
        model = get_face_recognition_model()
        while self._windowManager.is_window_created:
            self._captureManager.enter_frame()
            frame = self._captureManager.frame
            #self._captureManager.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            frame = detect_face(frame, model)

            self._windowManager.process_events()
            self._eventsHandler.execute_events()

            self._captureManager.exit_frame()

    def listen_keyboard(self, keycode):
        if keycode == 32:
            self._captureManager.write_image('/home/johny/Documents/python3/screenshot.png')
        elif keycode == 9:
            if not self._captureManager.is_writing_video:
                print('start recording')
                self._captureManager.start_writing_video(os.path.join('/home/johny/Documents/python3/screencast.avi'))
            else:
                self._captureManager.stop_writing_video()
                print('stop recording')
        elif keycode == 27:
            self._windowManager.destroy_window()

        elif keycode == ord('b'):  # blur filter
            self._filtersTrigger['blurFilter'] = not self._filtersTrigger['blurFilter']

        elif keycode == ord('e'):  # edge filter
            self._filtersTrigger['edgeDetectionFilter'] = not self._filtersTrigger['edgeDetectionFilter']


if __name__ == '__main__':
    Main().run()
