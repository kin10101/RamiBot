import json

# Load the JSON data
with open('/home/rami/PycharmProjects/RamiBot/Integrated/intents.json') as f:
    data = json.load(f)

# Iterate over the intents


def find_missing_value(value):
    for intent in data['intents']:
        # Check if the 'patterns' key is missing
        if value not in intent:
            # Print the tag of the intent
            print(f"The intent '{intent['tag']}' does not contain '{value}'")

def list_all_tags():
    for intent in data['intents']:
        print(intent['tag'])


if __name__ == "__main__":
    find_missing_value('patterns')
    list_all_tags()