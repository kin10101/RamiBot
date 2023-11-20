import random
import mysql.connector
import datetime
import pyttsx3
import re
from Voicebot import pygtts

#RamiDB = mysql.connector.connect(
    #host = "192.168.80.4",
    #user = "marj",
    #passwd = 'RAMIcpe211',
    #database = "ramibot",
    #port = "1000",
    #autocommit  = True
    #)

RamiDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = '',
    database = "ramibot",
    port = "3306",
    autocommit  = True
    )

cur = RamiDB.cursor()
engine = pyttsx3.init()

def insertToDB(ID_Num):
    # Check if the user with the given ID_Num already exists in the database
    user_query = f"SELECT ID_Number FROM ramibot_faces WHERE ID_Number = {ID_Num}"
    cur.execute(user_query)
    existing_user = cur.fetchone()

    if existing_user:
        print("User already in the database")

    else:
        # User doesn't exist, so insert the new record
        new_user = f"INSERT INTO ramibot_faces (ID_Number, Last_Name, Given_Name, MI) VALUES ({ID_Num}, NULL, NULL, NULL)"
        cur.execute(new_user)
        print(cur.rowcount, "Upload to DB")

    cur.close()


def returnName1(ID_Num,result):
    check_id = "SELECT * FROM ramibot_faces"
    cur.execute(check_id)
    res = cur.fetchall()
    greeting = get_time_of_day_greeting()
    threshold = 70

    temp = False
    for x in res:
        if ID_Num in x:
            check_name = f"SELECT Given_Name FROM ramibot_faces WHERE ID_Number = '{ID_Num}'"
            cur.execute(check_name)
            name = cur.fetchmany()
            temp = True

    if temp:
        # Extract the name from the fetched result
        name = name[0][0] if name else ""

        # Remove non-alphabetic characters from the name using regex
        if isinstance(name, str):
            name = re.sub(r'[^a-zA-Z\s]', '', name)
        else:
            # Handle the case where name is not a string (e.g., raise an exception or handle it appropriately)
            pass

        # Convert the recognition result to text
        if result > threshold:
            result_text = f"'{greeting}', '{name}'"
            pygtts.text_to_speech(result_text)
            time_stamp(ID_Num)
            print(f"Recognized: {name} (ID: {ID_Num})")
        else:
            print(f"Recognition confidence ({result}) is below the threshold. Unknown.")

    else:
        print("User not exist")

def get_time_of_day_greeting():
    # Get the current hour
    current_hour = datetime.datetime.now().hour

    # Determine the time of day and return a greeting message
    if 6 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def greet_new_user():
    random_num = random.randint(1,5)

def time_stamp(ID_Num):
    new_user = f"INSERT INTO greeted_user (user_id) VALUES ({ID_Num})"
    cur.execute(new_user)
    print(cur.rowcount, "Upload to DB")

