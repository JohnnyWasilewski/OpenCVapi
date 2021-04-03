from filters import BlurFilter, EdgeDetectionFilter
from faceDetector import detect_face, get_face_recognition_model
from backgroundProcessing import BackgroundProcessing
import cv2
import os


class EventsHandler:
    def __init__(self, capture_manager, window_manager):
        self._captureManager = capture_manager
        self._windowManager = window_manager
        self._eventsTrigger = {
            'edgeDetectionFilter': False,
            'blurFilter': False,
            'detectFace': False,
            'background': False,
        }
        self._face_model = get_face_recognition_model()
        self._blurFilter = BlurFilter()
        self._edgeDetectionFilter = EdgeDetectionFilter()
        self._backgroundProcessing = BackgroundProcessing()

    def process_events(self):
        self._get_events()
        self._execute_events()

    def _execute_events(self):
        frame = self._captureManager.frame
        if self._eventsTrigger['edgeDetectionFilter']:
            frame = self._edgeDetectionFilter.apply(src=frame)
        if self._eventsTrigger['blurFilter']:
            frame = self._blurFilter.apply(src=frame)
        if self._eventsTrigger['detectFace']:
            frame = detect_face(frame=frame, model=self._face_model)
        if self._eventsTrigger['background']:
            frame = self._backgroundProcessing.apply_background_detector(frame)

    def _get_events(self):
        keycode = cv2.waitKey(1)
        if keycode != -1:
            keycode &= 0xFF
            self._listen_keyboard(keycode)

    def _listen_keyboard(self, keycode):
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

        elif keycode == ord('1'):
            self._eventsTrigger['blurFilter'] = not self._eventsTrigger['blurFilter']

        elif keycode == ord('2'):
            self._eventsTrigger['edgeDetectionFilter'] = not self._eventsTrigger['edgeDetectionFilter']

        elif keycode == ord('4'):
            self._eventsTrigger['detectFace'] = not self._eventsTrigger['detectFace']

        elif keycode == ord('5'):
            self._eventsTrigger['background'] = not self._eventsTrigger['background']
            if not self._eventsTrigger['background']:
                cv2.destroyWindow("background")