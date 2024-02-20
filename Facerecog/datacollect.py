import cv2
import os
import Facerecog.main as m
import datetime
import shutil
import time
from main import cur

global user_id
global user_dir
global increment
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")


# Initialize count as a class variable


def add_to_db(id_num, nickname, last_name, given_name, middle_initial, profession):
    global user_dir
    global user_id
    # add to database
    m.insertToDB(id_num, nickname, last_name, given_name, middle_initial, profession)
    user_dir = os.path.join("datasets", id_num)
    user_id = id_num
    # Check if the user directory already exists
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    pass


def generate_visitor_id():
    global increment
    # Get the current year
    current_year = datetime.datetime.now().year

    increment = increment + 1

    # Create the visitor ID by combining the components
    visitor_id = f'{current_year}9{increment:05d}'

    user_query = f"SELECT ID_Number FROM ramibot_faces WHERE ID_Number = {visitor_id}"
    cur.execute(user_query)
    existing_user = cur.fetchone()

    if existing_user:
        increment = increment + 1
        visitor_id = f'{current_year}9{increment:05d}'

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
