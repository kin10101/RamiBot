import random
import mysql.connector
from datetime import datetime, timedelta
import pyttsx3
import re
#from Voicebot import pygtts

RamiDB = mysql.connector.connect(
    host = "airhub-soe.apc.edu.ph",
    user = "marj",
    passwd = 'RAMIcpe211',
    database = "ramibot",
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
    unknown_user = greet_new_user()
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
            print(f"Recognized: {name} (ID: {ID_Num})")
            time_stamp(ID_Num, result_text)
            if name == "None":
                unknown = f"{unknown_user}"
                #pygtts.text_to_speech(unknown)
                engine.say(unknown)
            else:
                pass
        else:
            print(f"Recognition confidence ({result}) is below the threshold. Unknown.")

    else:
        print("User not exist")

def get_time_of_day_greeting():
    # Get the current hour
    current_hour = datetime.now().hour

    # Determine the time of day and return a greeting message
    if 6 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def greet_new_user():
    random_num = random.randint(1,5)
    if random_num == 1:
        return "Hello, I'm Ramibot!"
    elif random_num == 2:
        return "Kamusta, Ako si Ramibot!"
    elif random_num == 3:
        return "Hi, I'm Ramibot!"
    elif random_num == 4:
        return "What up, I'm Ramibot!"
    elif random_num == 5:
        return "Whatcha doin, I'm Ramibot!"

def time_stamp(ID_Num, result_text):
    new_user = f"INSERT INTO greeted_users (ID_Number) VALUES ({ID_Num})"
    cur.execute(new_user)
    uploaded = cur.rowcount
    current_time = datetime.now()
    print(uploaded, f"timestamp uploaded to db with cur_time {current_time}")

    if uploaded == 1:
        #check if timestamp is greater than 30
        user_query = f"SELECT time_stamp FROM greeted_users WHERE ID_Number = {ID_Num} ORDER BY id LIMIT 1"
        cur.execute(user_query)
        last_update = cur.fetchone()
        print(f"last update: {last_update}")
        if last_update:
                last_update = last_update[0]
                time_difference = (current_time-last_update).total_seconds()
                print(f"time difference: {time_difference}")
                if time_difference > 3600:
                    #pygtts.text_to_speech(result_text)
                    engine.say(reslut_text)
                    cur.execute(f"DELETE FROM greeted_users WHERE ID_Number = {ID_Num}")
                else:
                    print("already greeted an hour ago")
    else:
        print("user not in db")







