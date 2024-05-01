import pygtts as tts
import datetime
from datetime import datetime

def sing():
    print("singing")
    tts.play_audio_file("audio/Asia Pacific College - Alma Mater Hymn Short Ver.wav")


def run_func():
    print("running function")
    pass


def get_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    tts.speak("it is currently " + current_time)
    print("")


def get_date():
    now = datetime.now()
    current_day = now.strftime("%A %B %d")
    day_of_week = now.strftime("%A")
    tts.speak("Today is " + current_day)


def navigateToFaceScanning():
    print("navigating to face scanning")

command_mappings = {
    "FN_sing": sing,
    "FN_current_time": get_time,
    "FN_current_date": get_date,
    "FN_nav_to_face_scanning": navigateToFaceScanning


}

