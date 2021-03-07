class EventsHandler():
    def __init__(self, capture_manager, window_manager, blur_filter, edge_detection_filter, filters_trigger):
        self._captureManager = capture_manager
        self._windowManager = window_manager
        self._blurFilter = blur_filter
        self._edgeDetectionFilter = edge_detection_filter

        self._blurFilterOn = False
        self._edgeDetectionFilterOn = False
        self._filtersTrigger = filters_trigger

    def execute_events(self):
        if self._filtersTrigger['edgeDetectionFilter']:
            frame = self._captureManager.frame
            self._captureManager.frame = self._edgeDetectionFilter.apply(src=frame)
        if self._filtersTrigger['blurFilter']:
            a = self._captureManager.frame
            self._captureManager.frame = self._blurFilter.apply(src=a)
