import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

import voicecommand_functions

# Load data
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('eventintents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Get dict command mappings
intent_methods = voicecommand_functions.command_mappings


def clean_up_sentence(sentence):
    """Tokenize and lemmatize the sentence."""
    stop_words = nltk.corpus.stopwords.words('english')

    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words if word not in stop_words]

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


def predict_class(sentence):
    """Predict the intent of the sentence."""
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.7  # Acceptable limit to output the response. Adjust if necessary
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)  # sort by strength of probability
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    if not return_list:
        return_list.append({'intent': 'FB Unknown', 'probability': '1'})

    return return_list


def get_response(intents_list, intents_json, context):
    """Get a response based on the predicted intent."""
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = None
    for i in list_of_intents:
        if i['tag'] == tag:

            if 'context_filter' in i and i['context_filter'] not in context:
                continue

            if 'context_set' in i:  # set context
                context[0] = i['context_set']

            if 'function' in i:
                result = "running function..."

            if not i:
                result = "sorry, I am not yet capable of responding to that"
                continue

            result = random.choice(i['responses'])  # Gets a random response from the given list
            break

    if result is None:
        result = "sorry, I am not yet capable of responding to that"

    return result


def handle_request(message, context):
    """Determine whether the predicted intent corresponds to a custom command function
    or a standard response and return the appropriate output."""
    predicted_intents = predict_class(message)
    print("PREDICTED INTENTS", predicted_intents)
    check_response = get_response(predicted_intents, intents, context)

    if not predicted_intents:
        response = "sorry, I am not yet capable of responding to that"

    elif predicted_intents[0]['intent'] in intent_methods.keys():  # if predicted intent is mapped to a function
        intent_methods[predicted_intents[0]['intent']]()  # call the function

    else:
        response = check_response

    if response is None:
        response = "sorry, I am not yet capable of responding to that response"
    return response


def get_tag(message):
    tag = predict_class(message)
    return tag


def run_chatbot():
    """Run chatbot by using the command line."""
    print("testing cb")
    context = [""]
    running = True
    while running:
        print(context)

        try:
            message = input("")  # get input
            if message == "stop":
                print('input received')

            response = handle_request(message, context)  # get response from request()

            if response:  # if response is not empty
                print(response)

        except Exception as e:
            response = e
            pass
