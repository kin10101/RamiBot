import json
import pickle
import random

import matplotlib.pyplot as plt
import nltk
import numpy as np
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer
from keras.utils import plot_model

"""uncomment for first install"""
# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download("stopwords")


def train_bot():
    lemmatizer = WordNetLemmatizer()

    intents = json.loads(open('intents.json').read())

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

    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

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

    # Split the dataset into training, validation, and test sets
    split_ratio = 0.8
    num_samples = len(training)
    train_size = int(split_ratio * num_samples)
    train_data = training[:train_size]
    remaining_data = training[train_size:]
    validation_size = len(remaining_data) // 2
    validation_data = remaining_data[:validation_size]
    test_data = remaining_data[validation_size:]

    train_x = list(train_data[:, 0])
    train_y = list(train_data[:, 1])
    validation_x = list(validation_data[:, 0])
    validation_y = list(validation_data[:, 1])
    test_x = list(test_data[:, 0])
    test_y = list(test_data[:, 1])

    # Define the model
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)

    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    print(model.summary()) # print model summary

    # Train the model with validation data
    hist = model.fit(
        np.array(train_x), np.array(train_y),
        validation_data=(np.array(validation_x), np.array(validation_y)),
        epochs=200, batch_size=5, verbose=2
    )
    model.save('chatbot_model.h5', hist)

    print('done training')

    # call the plot_history function to plot accuracy and loss
    plot_history(hist)
    visualize_model(model)

    # Evaluate the model with test data
    test_loss, test_accuracy = model.evaluate(np.array(test_x), np.array(test_y), verbose=0)
    print(f'Test Loss: {test_loss}, Test Accuracy: {test_accuracy}')


def plot_history(history):
    """Visualize training and validation graphs"""
    # Plot training accuracy and validation accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

    # Plot training loss and validation loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()


def visualize_model(model):
    """Visualize the model layers"""
    plot_model(model, to_file='model_layers.png', show_shapes=False, show_layer_names=True)



