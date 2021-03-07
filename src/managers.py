import numpy as np
import cv2
import time


class CaptureManager(object):
    def __init__(self, capture, preview_window_manager=None, should_mirror_preview=False):
        self.previewWindowManager = preview_window_manager
        self.shouldMirrorPreview = should_mirror_preview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def is_writing_image(self):
        return self._imageFilename is not None

    @property
    def is_writing_video(self):
        return self._videoFilename is not None

    def enter_frame(self):
        assert not self._enteredFrame
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exit_frame(self):
        if self._frame is None:
            self._enteredFrame = False
            return

        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            time_elapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / time_elapsed
        self._framesElapsed += 1

        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirrored_frame = np.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirrored_frame)
            else:
                self.previewWindowManager.show(self._frame)

        if self.is_writing_image:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None

        self._write_video_frame()

        self._frame = None
        self._enteredFrame = False

    def write_image(self, filename):
        self._imageFilename = filename

    def start_writing_video(self, filename, encoding=cv2.VideoWriter_fourcc('I', '4', '2', '0')):
        self._videoFilename = filename
        self._videoEncoding = encoding

    def stop_writing_video(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFilename, self._videoEncoding, fps, size)

        self._videoWriter.write(self._frame)


class WindowManager:
    def __init__(self, window_name, keypress_callback=None):
        self.keypressCallback = keypress_callback
        self._windowName = window_name
        self._isWindowCreated = False

    @property
    def is_window_created(self):
        return self._isWindowCreated

    def create_window(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroy_window(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def process_events(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypressCallback(keycode)
