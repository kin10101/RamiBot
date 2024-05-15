import cv2
import os
import Facerecog.main as m
import datetime
import shutil
import time
# from main import cur

global user_id
global user_dir
global increment
increment = 0
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
#computer marj
path = "D:\RamiBot Project\RamibotReal\Facerecog\datasets50"

#path = "/home/rami/PycharmProjects/RamiBot/Facerecog/datasets50"

# Initialize count as a class variable


def add_to_db(id_num, nickname, last_name, given_name, middle_initial, profession):
    global user_dir
    global user_id
    # add to database
    m.insertToDB(id_num, nickname, last_name, given_name, middle_initial, profession)
    user_dir = os.path.join(path, id_num)
    user_id = id_num
    # Check if the user directory already exists
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    pass


def generate_visitor_id():
    current_year = datetime.datetime.now().year

    # Initialize the increment counter
    increment = 0

    while True:
        # Increment the counter
        increment += 1

        # Generate the visitor ID
        visitor_id = f'{current_year}9{increment:05d}'

        # Check if the visitor ID exists in the database
        user_query = f"SELECT ID_Number FROM ramibot_faces WHERE ID_Number = '{visitor_id}'"
        m.cur.execute(user_query)
        existing_user = m.cur.fetchone()

        # If the visitor ID does not exist, break out of the loop
        if existing_user is None:
            break

    return visitor_id


def clear_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate over the files and subfolders in the specified folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # Check if the item is a file and remove it
            if os.path.isfile(item_path):
                os.remove(item_path)
            # If it's a subfolder, remove it recursively
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        print(f"Contents of {folder_path} cleared successfully.")
    else:
        print(f"The specified folder {folder_path} does not exist.")


def sleeping():
    time.sleep(10)
