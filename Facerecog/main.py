import random
from datetime import datetime
import re

from smb.SMBConnection import SMBConnection
import sql_module

from deepface import DeepFace
import cv2
import pandas as pd


RamiDB = sql_module.connect()
cur = RamiDB.cursor()

voiceTrig = 0
motorTrig = 0

backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'fastmtcnn','retinaface', 'mediapipe','yolov8','yunet','centerface',]
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace","GhostFaceNet",]
metrics = ["cosine", "euclidean", "euclidean_l2"]

global user_nickname
global unknown_user
global result_text
global lower_conf
global great_user
global video
lower_conf = False
great_user = False
global person_identified
global person_detected


#start of face recognition module--------------------------------------------------------------------------------------
def realtime_face_recognition():
    global person_identified
    global person_detected
    video = cv2.VideoCapture(0)
    # Define a video capture object
    global x, y, w, h
    path = "/home/rami/PycharmProjects/RamiBot/Facerecog/datasets50"
    while True:
        # Capture the video frame by frame
        ret, frame = video.read()

        try:
            # Perform face recognition on the captured frame
            # Find faces and identify people using a specific model and distance metric
            detections = DeepFace.extract_faces(img_path=frame, detector_backend=backends[8])
            if detections:
                print("face detected")
                person_detected = True
                people = DeepFace.find(img_path=frame, db_path=path, model_name=models[2], distance_metric=metrics[2], detector_backend=backends[8],enforce_detection=False, threshold=0.6)
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
                            name = person['identity'][0].split("/")[1]
                            returnName1(str(name), person_identified)
                            cv2.putText(frame, name, (x, y), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

        except Exception as e:
            person_detected = False
            #print(f"An error occurred: {e}")


        #Display the resulting frame
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 960, 720)
        # cv2.imshow('frame', frame)

        # Check if the 'q' button is pressed to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Release the video capture object and close all windows
    video.release()
    # cv2.destroyAllWindows()

#end of face recognition module----------------------------------------------------------------------------------------

#other modules---------------------------------------------------------------------------------------------------------
def insertToDB(ID_Num, nickname, Last_Name, Given_name, MI, Proffesion):

    try:
        # Check if the user with the given ID_Num already exists in the database
        user_query = f"SELECT ID_Number FROM ramibot_faces WHERE ID_Number = {ID_Num}"
        cur.execute(user_query)
        existing_user = cur.fetchone()

        if existing_user:
            print("User already in the database")

        else:
            # User doesn't exist, so insert the new record
            new_user = "INSERT INTO ramibot_faces (ID_Number, nickname, Last_Name, Given_Name, MI, Profession) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (ID_Num, nickname, Last_Name, Given_name, MI, Proffesion)
            cur.execute(new_user, values)
            RamiDB.commit()
            print(cur.rowcount, "Upload to DB")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if RamiDB:
            RamiDB.close()


def returnName1(ID_Num,person_identified):
    global user_nickname
    global unknown_user
    global result_text
    global lower_conf
    check_id = "SELECT * FROM ramibot_faces"
    cur.execute(check_id)
    res = cur.fetchall()
    greeting = get_time_of_day_greeting()
    unknown_user = greet_new_user()
    #threshold = 50

    temp = False
    lower_conf = False
    for x in res:
        if ID_Num in x:
            check_name = f"SELECT nickname FROM ramibot_faces WHERE ID_Number = '{ID_Num}'"
            cur.execute(check_name)
            nickname = cur.fetchmany()
            temp = True

    if temp:
        # Extract the name from the fetched result
        nickname = nickname[0][0] if nickname else ""

        # Remove non-alphabetic characters from the name using regex
        if isinstance(nickname, str):
            nickname = re.sub(r'[^a-zA-Z\s]', '', nickname)
        else:
            # Handle the case where name is not a string (e.g., raise an exception or handle it appropriately)
            pass

        if person_detected:
            lower_conf = True
            result_text = greet_new_user()
            print(f"person not in db")

        if person_identified:
            result_text = f"{greeting}, {nickname}!"
            user_nickname = nickname
            print(f"Recognized: {nickname} (ID: {ID_Num})")
            time_stamp(ID_Num)
            lower_conf = False

    else:
        lower_conf = True
        result_text = greet_new_user()
        print(f"lower_conf: {lower_conf}")
        print("User not exist")


def get_time_of_day_greeting():
    # Get the current hour
    current_hour = datetime.now().hour

    # Determine the time of day and return a greeting message
    if 6 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def greet_new_user():
    random_num = random.randint(1,5)
    if random_num == 1:
        return "Hello there, I'm Rami bot!"
    elif random_num == 2:
        return "Hello friend! my name is Rami bot!"
    elif random_num == 3:
        return "Good day, I'm Rami bot!"
    elif random_num == 4:
        return "Hi there, I'm Rami bot!"
    elif random_num == 5:
        return "Greetings, I'm Rami bot!"


def time_stamp(ID_Num):

    global greet_user

    new_user = f"INSERT INTO greeted_users (ID_Number) VALUES ({ID_Num})"
    cur.execute(new_user)
    uploaded = cur.rowcount
    current_time = datetime.now()
    print(uploaded, f"timestamp uploaded to db with cur_time {current_time}")

    if uploaded == 1:
        user_query = f"SELECT time_stamp FROM greeted_users WHERE ID_Number = {ID_Num} ORDER BY id LIMIT 1"
        cur.execute(user_query)
        last_update = cur.fetchone()
        print(f"last update: {last_update}")
        if last_update:
                last_update = last_update[0]
                time_difference = (current_time-last_update).total_seconds()
                print(f"time difference: {time_difference}")
                if time_difference > 86400:
                    greet_user = True
                    cur.execute(f"DELETE FROM greeted_users WHERE ID_Number = {ID_Num}")
                else:
                    greet_user = False
                    print("already greeted within the day")
    else:
        print("user not in db")


def samba_connection(folder_path):
    server_name = '192.168.80.4'
    share_name = 'sambashare'
    username = 'apc-airlab'
    password = 'APC_Airlab_2023!'
    #folder_path = 'RamiBot/datasets50'

    try:
        # Establish a connection to the Samba share
        conn = SMBConnection(username, password, '', server_name, use_ntlm_v2=True)
        conn.connect(server_name, 445)
        print("Connection established")

        # List files and directories in the folder
        files_in_folder = conn.listPath(share_name, folder_path)
        return  files_in_folder

    except Exception as e:
        print(f"An error occurred: {e}")



