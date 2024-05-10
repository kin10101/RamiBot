import random
import mysql.connector
from datetime import datetime
import re
from smb.SMBConnection import SMBConnection
#import Voicebot.pygtts as pygtts

RamiDB = mysql.connector.connect(
    host = "airhub-soe.apc.edu.ph",
    user = "marj",
    passwd = 'RAMIcpe211',
    database = "ramibot",
    autocommit  = True
    )

# RamiDB = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     passwd = '',
#     database = "ramibot",
#     port = "3306",
#     autocommit  = True
#     )

cur = RamiDB.cursor()
#engine = pyttsx3.init()
voiceTrig = 0
motorTrig = 0
global user_nickname
global unknown_user
global result_text
global lower_conf
lower_conf = False

identified_list = []

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


def returnName1(ID_Num,result):
    global user_nickname
    global unknown_user
    global result_text
    global lower_conf
    check_id = "SELECT * FROM ramibot_faces"
    cur.execute(check_id)
    res = cur.fetchall()
    greeting = get_time_of_day_greeting()
    unknown_user = greet_new_user()
    threshold = 50

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

        # Convert the recognition result to text
        if result > threshold:
            result_text = f"{greeting}, {nickname}!"
            user_nickname = nickname
            print(f"Recognized: {nickname} (ID: {ID_Num})")
            time_stamp(ID_Num, result_text)

            #compares 3 items in the list
            # identified_list.append(user_nickname) #adds nickname to the list
            # if identified_list.count(user_nickname) == 3: #identifies if nickname is iterated 3 times
            #     return True
        else:
            lower_conf = True
            result_text = greet_new_user()
            print(f"Recognition confidence ({result}) is below the threshold. Unknown. name : {nickname}")

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
                if time_difference > 500:
                    #pygtts.speak(f'{result_text}')
                    cur.execute(f"DELETE FROM greeted_users WHERE ID_Number = {ID_Num}")
                else:
                    print("already greeted an hour ago")
    else:
        print("user not in db")


def samba_connection(path_file):
    global conn

    # Define the server details
    server_name = "192.168.80.4"  # Replace with the Samba server's IP address
    share_name = "sambashare"
    username = "apc-airlab"
    password = "APC_Airlab_2023!"

    # Create an SMB connection object
    conn = SMBConnection(username, password, "pysmb-client", server_name, use_ntlm_v2=True)

    try:
        # Connect to the Samba server
        print("Connecting to Samba server...")
        conn.connect(server_name, 445)

        print("Connected to Samba server")

        # List files in the share
        files = conn.listPath(share_name, path_file)

        for file in files:
            print(file.filename)

        # You can perform other operations like reading files, writing files, etc. here

    except Exception as e:
        print("Error:", e)


def close_samba_connection():

    # Disconnect from the Samba server
    print("Closing connection...")
    conn.close()





