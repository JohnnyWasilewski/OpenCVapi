import cv2


def detect_face(frame, model):
    face_detect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_detect.detectMultiScale(gray)
    face_recognition_model = model
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        roi = gray[x:(x+w), y:(y+h)]
        try:
            roi = cv2.resize(roi, (250, 250), cv2.INTER_LINEAR)
            pred = face_recognition_model.predict(roi)
            #if pred[1] > 0.7:
            frame = cv2.putText(frame, "JAN", (x, y-20))
        except:
            continue

    return frame, model
