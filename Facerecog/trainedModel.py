import cv2
from Facerecog import main as m

facedetect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("/home/rami/PycharmProjects/RamiBot/Facerecog/Trainer.yml")
count = 0
currentID = 0
global confidence_result

def face_recognition(video):
    global confidence_result
    global running
    running = True
    while running:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            currentID = serial
            confidence_result = conf
            if conf > 70:

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

                #greet user with voice
                m.returnName1(str(serial), conf)
                video.release()
                running = False

                return confidence_result




            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

        #frame = cv2.resize(frame, (640, 480))
        #cv2.imshow('frame', frame)

        k = cv2.waitKey(1)

        if k == ord("q"):
            break

    video.release()
    #cv2.destroyAllWindows()n



