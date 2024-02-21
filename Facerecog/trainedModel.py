import cv2
from Facerecog import main as m

facedetect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

recognizer = cv2.face.LBPHFaceRecognizer.create()

#RPI
recognizer.read("/home/rami/PycharmProjects/RamiBot/Facerecog/Trainer.yml")

#laptop
#recognizer.read("D:\RamiBot Project\RamibotReal\Facerecog\Trainer.yml")
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
        gray_eq = cv2.equalizeHist(gray)
        faces = facedetect.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=8, minSize=(30, 30))
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray_eq[y:y + h, x:x + w])
            confidence_result = conf

            if conf > 90:

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

        k = cv2.waitKey(1)

        if k == ord("q"):
            break

    video.release()
    #cv2.destroyAllWindows()



