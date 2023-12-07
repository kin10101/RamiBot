import Voicebot.voicebotengine as voicebotengine
import Voicebot.mimictts as tts
import datetime
from datetime import datetime
import Voicebot.vb_train_model as vb_train_model

def sing():
    print("singing")
    tts.playAudioFile("audio/Asia Pacific College - Alma Mater Hymn Short Ver.wav")


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


def train_bot():
    running = bool
    # train the bot with the new intents
    tts.speak("Starting training phase. please wait for a while...")
    vb_train_model.train_bot()
    tts.speak("please restart for the changes to take effect")
    return running is False


command_mappings = {
    "FN_sing": sing,
    "FN_current_time": get_time,
    "FN_current_date": get_date,
    "FN_update": train_bot,


}

