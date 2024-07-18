import random
import json
import pickle
import string

import keras
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

import TTS
from Voicebot import voicecommand_functions
from queue import Queue

Speech_Queue = Queue()
Image_Queue = Queue()

# Load data
lemmatizer = WordNetLemmatizer()

intents = json.loads(open('../Integrated/intents.json').read())
words = pickle.load(open('../Integrated/words.pkl', 'rb'))
classes = pickle.load(open('../Integrated/classes.pkl', 'rb'))
model = keras.models.load_model('../Integrated/voicebot_model.h5')

# Get dict command mappings
intent_methods = voicecommand_functions.command_mappings

ERROR_THRESHOLD = 0.5  # Acceptable limit to output the response. Adjust if necessary

def clean_up_sentence(sentence):
    """Tokenize, remove punctuation, and lemmatize the sentence."""
    stop_words = set(nltk.corpus.stopwords.words('english'))
    ignore_punctuation = ['!', '?', '.', ',', ' ', '-']

    # Tokenize the sentence
    sentence_words = nltk.word_tokenize(sentence)

    # Remove punctuation and stop words, then lemmatize
    sentence_words = [
        lemmatizer.lemmatize(word.lower())
        for word in sentence_words
        if word not in stop_words and word not in string.punctuation and word not in ignore_punctuation
    ]

    print("sentence words:", sentence_words)

    return sentence_words

def bag_of_words(sentence):
    """Create a bag of words from the sentence."""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence, error_threshold=ERROR_THRESHOLD):
    """Predict the intent of the sentence."""
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]

    results = [[i, r] for i, r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)  # sort by strength of probability
    return_list = []

    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    if not return_list:
        return_list.append({'intent': 'Fallback unknown', 'probability': '1'})

    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    result = get_from_json("Fallback unknown")  # default response if no intent is found

    for i in list_of_intents:
        if i['tag'] == tag:

            if 'function' in i:
                result = "running function..."  # remove this line before deployment. should run a function instead of returning a string
                # intent_methods[i['function']]()  # call the function
                # refactor to use intent_methods
                break

            if 'source_image' in i:
                Image_Queue.put(i['source_image'])
                print("VOICEBOT PLACED AN ITEM TO CHANGE IMAGE")

            if 'navigate_to' in i:
                Speech_Queue.put(i['navigate_to'])
                print("VOICEBOT PLACED AN ITEM IN SCREEN QUEUE")

            if 'responses' in i and i['responses']:
                result = random.choice(i['responses'])  # Gets a random response from the given list
                break

    return result


def handle_request(message):
    """Determine whether the predicted intent corresponds to a custom command function
    or a standard response and return the appropriate output."""
    predicted_intents = predict_class(message)
    print("PREDICTED INTENTS", predicted_intents)

    # Print the confidence score of the predicted intent
    confidence_score = predicted_intents[0]['probability']
    print(f"Confidence score: {confidence_score}")

    # Get the intent tag
    intent_tag = predicted_intents[0]['intent']
    print(f"Intent tag: {intent_tag}")

    check_response = get_response(predicted_intents, intents)

    if intent_tag in intent_methods.keys():  # if predicted intent is mapped to a function
        intent_methods[intent_tag]()  # call the function

    return check_response, confidence_score, intent_tag


def get_tag(message):
    tag = predict_class(message)
    return tag


def get_from_json(tag, filename='intents.json'):
    """Get response from JSON file based on the provided tag."""
    try:
        with open(filename) as file:
            intents_json = json.load(file)

        list_of_intents = intents_json.get('intents', [])

        for intent in list_of_intents:
            if intent.get('tag') == tag:
                responses = intent.get('responses', [])
                return random.choice(responses)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")

    return None


def peek(queue):
    if not queue.empty():
        # Get the item at the front of the queue
        item = queue.queue[0]
        print("Item at front of queue:", item)
    else:
        print("Queue is empty")


def run_chatbot():
    """Run chatbot by using the command line."""
    print("testing cb")
    running = True
    while running:
        peek(Speech_Queue)

        try:
            message = input("")  # get input
            if message == "stop":
                print('input received')

            response, confidence_score, intent_tag = handle_request(message)  # get response from request()

            if response:  # if response is not empty
                TTS.speak_async(response)
                print(response)

        except Exception as e:
            response = e
            pass


if __name__ == "__main__":

    run_chatbot()
