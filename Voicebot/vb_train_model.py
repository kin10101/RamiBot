import json
import pickle
import random

import nltk
import numpy as np
import keras
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer

"""uncomment for first install"""
# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download("stopwords")


def train_bot():
    lemmatizer = WordNetLemmatizer()

    intents = json.loads(open('../Integrated/voicebotintents.json').read())

    words = []
    classes = []
    documents = []

    ignore_punctuation = ['!', '?', '.', ',']
    stop_words = nltk.corpus.stopwords.words('english')

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_punctuation and stop_words]
    words = sorted(set(words))

    classes = sorted(set(classes))

    pickle.dump(words, open('../Integrated/words.pkl', 'wb'))
    pickle.dump(classes, open('../Integrated/classes.pkl', 'wb'))

    training = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    # Define the model
    model = keras.Sequential(
        [
            keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(len(train_y[0]), activation='softmax')
        ]
    )
    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)

    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    print(model.summary())  # print model summary

    # Train the model with validation data
    hist = model.fit(
        np.array(train_x), np.array(train_y),
        epochs=150, batch_size=5, verbose=2
    )
    model.save('../Integrated/voicebot_model.h5')

    print('done training')

if __name__ == '__main__':
    # Run the training function
    train_bot()