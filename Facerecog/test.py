from deepface import DeepFace
import cv2
import pandas as pd
from Facerecog.main import returnName1

# List of available backends, models, and distance metrics
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'fastmtcnn','retinaface', 'mediapipe','yolov8','yunet','centerface',]
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace","GhostFaceNet",]
metrics = ["cosine", "euclidean", "euclidean_l2"]
global person_identified
global person_detected

# uncomment if you want to test the module
#vid = cv2.VideoCapture(1)

#path = main.samba_connection("/RamiBot/datasets50")
#path = "https://192.168.80.4/RamiBot/datasets50"

def realtime_face_recognition(vid):
    global person_identified
    global person_detected
    # Define a video capture object
    global x, y, w, h

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read()

        try:
            # Perform face recognition on the captured frame
            # Find faces and identify people using a specific model and distance metric
            detections = DeepFace.extract_faces(img_path=frame, detector_backend=backends[8])
            if detections:
                print("face detected")
                person_detected = True
                people = DeepFace.find(img_path=frame, db_path='datasets50/', model_name=models[2], distance_metric=metrics[2], detector_backend=backends[8],enforce_detection=False, threshold=0.6)
                #print(f"people: {people}")
                if people:
                    for person in people:
                        person_identified = True
                        # Retrieve the coordinates of the face bounding box
                        # Ensure that person['source_x'], person['source_y'], etc. are Series
                        if isinstance(person['source_x'], pd.Series):
                            x = person['source_x'].iloc[0]
                            y = person['source_y'].iloc[0]
                            w = person['source_w'].iloc[0]
                            h = person['source_h'].iloc[0]

                            # Draw a rectangle around the face
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                            # Get the person's name and display it on the image
                            name = person['identity'][0].split("/")[-1].split("\\")[0]
                            returnName1(str(name), person_identified)
                            cv2.putText(frame,name, (x, y), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

        except:
            person_detected = False

        #Display the resulting frame
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 960, 720)
        cv2.imshow('frame', frame)

        # Check if the 'q' button is pressed to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Release the video capture object and close all windows
    vid.release()
    cv2.destroyAllWindows()

# Perform real-time face recognition using the webcam
#realtime_face_recognition(vid)