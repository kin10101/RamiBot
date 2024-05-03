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
global low_conf

def turn_off_camera(video):
    video.release()


def face_recognition(video):
    global confidence_result
    global running
    global low_conf

    low_conf = False
    running = True
    while running:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray)
        faces = facedetect.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors= 8, minSize=(60, 60))
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray_eq[y:y + h, x:x + w])
            confidence_result = conf
            print(f"confidence level: {confidence_result} for id number {str(serial)}")

            if conf > 50:

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

                #greet user with voice
                res = m.returnName1(str(serial), conf)
                print(f"{res}")
                video.release()
                running = False

                return confidence_result
                # if res is True:
                #     return confidence_result
                # else:
                #     pass

            else:
                print("unrecognized")

                m.result_text = m.greet_new_user()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

        k = cv2.waitKey(1)

        if k == ord("q"):
            break

    video.release()
    #cv2.destroyAllWindows()



