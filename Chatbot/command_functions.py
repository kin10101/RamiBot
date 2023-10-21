import chatbot
import datetime
from datetime import datetime
import train_model


def test_func():
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
    train_model.train_bot()
    return running is False


# convert to a json file afterwards



def edit_intent():
    intent_tag = input("Enter the tag of the intent you want to edit: ")
    new_responses = input("Enter new responses for the intent (separated by |): ").split('|')
    addintent.edit_intent("chatbotintents.json", intent_tag, new_responses)


command_mappings = {
    "FN_current_time": get_time,
    "FN_current_date": get_date,
    "FN_update": train_bot,

}

