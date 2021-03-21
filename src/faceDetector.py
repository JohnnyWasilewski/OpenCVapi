import cv2
import os
import numpy as np


def detect_face(frame, model):
    face_detect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_detect.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        roi = gray[x:(x+w), y:(y+h)]
        try:
            roi = cv2.resize(roi, (250, 250), cv2.INTER_LINEAR)
            pred = model.predict(roi)
            if pred[1] < 8000:
                frame = cv2.putText(frame, "JAN", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2)
        except Exception:
            continue

    return frame


def get_face_recognition_model():
    x = []
    for file in os.listdir('data'):
        x.append(np.array(cv2.imread(os.path.join('data', file), cv2.IMREAD_GRAYSCALE)))

    y = [0] * len(x)
    model = cv2.face.EigenFaceRecognizer_create()
    model.train(np.array(x), np.array(y))
    return model

