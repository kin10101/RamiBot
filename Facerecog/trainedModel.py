import cv2
import main as m

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

facedetect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")
count = 0
currentID = 0

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
        currentID = serial

        if conf > 80:

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

            #greet user with voice
            m.returnName1(str(serial), conf)


        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

    frame = cv2.resize(frame, (640, 480))
    cv2.imshow('frame', frame)

    k = cv2.waitKey(1)

    if k == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

