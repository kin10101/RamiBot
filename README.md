# RamiBot - Asia Pacific College Robotic Concierge

# Table of Contents
1. [Introduction](#introduction)    
2. [Installation](#installation)
3. [Model Training](#model-training)
4. [Usage](#usage)
5. [Acknowledgements](#acknowledgements)
<!-- TOC -->

# Introduction
RamiBot is a robotic concierge that is designed to assist students and faculty members of Asia Pacific College. 
It is capable of answering frequently asked questions, providing information about the school, and assisting users in navigating the campus building.
This repository contains the source code for the software side of the RamiBot project. 

The project is divided into four main modules:
1. __Chatbot Module__ - A chatbot that can answer frequently asked questions and provide information about the school.
2. __Speech Recognition Module__ - A voice recognition module that allows users to interact with the chatbot using voice commands. extension of the chatbot module.
3. __Face Recognition Module__ - A face recognition module that allows the chatbot to recognize and greet a user if the bot sees a user's face.
4. __GUI Module__ - A graphical user interface that allows users to interact with Rami through a touch screen interface. The Kivy framework is used to create the GUI.

## Chatbot Module
a rule-based chatbot that uses a bag-of-words model to classify user input into different intents. 
The chatbot is trained on a dataset of intents and responses, and uses the NLTK library for natural language processing.
Keras is used to create the neural network model that classifies user input into intents. It is a probabilistic model that uses the softmax activation function to output the probability of how close the users input is to an intent category.
The intent with the highest probability is then used to generate a response to the user.

## Voice Recognition Module
An extension of the chatbot module that allows users to interact with the chatbot using voice commands. 
Uses faster-whisper to convert the user's speech to text. 
The module uses the SpeechRecognition .
The voice recognition module is trained on the same dataset of intents and responses as the chatbot module, and uses the same neural network model to classify user input into intents.

# Installation
Program is deployed on debian 12. A Linux OS is recommended to run this however, it can also run on Windows albeit with some workarounds when installing cmake.

- Requires python 3.8 or higher. 3.11 was used for this project.
- Requires connection to the internet to access the Google speech recognition API (contact ITRO if connection gets blocked)
- Must be connected to the school network for the app to run because resources are hosted on the school server


To install all dependencies needed by the project, run  the following command:
```
    pip install -r requirements.txt
```

Here are the list of core dependencies needed by the project:

#### For Chatbot Module:
- nltk
- numpy
- tensorflow
- keras
- pickle
- json

#### For Voice Recognition Module:
- speech_recognition
- pyaudio

#### For GUI Module:
- kivy
- kivymd

#### For Face Recognition Module:
- opencv-python
- deepface


# Model Training
### Intent Classifier Model
To train the voicebot model, run the following python module under the Voicebot package:
```
    vb_train_model.py
```
for first installations, you may need to download these nltk packages to run the module:
```
    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
```
### Modifying the training data
The training data used for both the chatbot and voicebot features are stored in a JSON file format with the following structure:
```json
{
  "intents": 
  [
        {
            "tag": "RAMI credits",
            "patterns": [
                "Who made you",
                " who developed you",
                " who programmed you",
                " who created ramibot"
            ],
            "responses": [
                "I was created by a team consisting of Computer and Electronic Engineering students from the School of Engineering Department. They collaborated to design and develop me combining their expertise in programming and artificial intelligence. Together they brought me to life as your robot assistant."
            ],
            "navigate_to": "image_info",
            "source_image": "The_Ramibot_Team"
        }
  ]
}
```
tag: is an identifier for the intent

patterns: contains the phrases that a user might say and this is the words that the model is being trained on. It is recommended to write only unique keywords that are distinct from other intent tags to avoid wrong outputs.

responses: are the actual responses that RamiBot will give to the user if this intent is classified as the best match

navigate_to: is the screen that the GUI will navigate to if this intent is classified as the best match

src_img: is the image path of the image that will be displayed on the screen if this intent is classified as the best match. 

# Usage
To run the program, navigate to the Integrated package directory and run the file GUIdev.py
```
    python GUIdev.py
```

### Modifying GUI elements
GUI navigation is done through a list of buttons that either navigate to another screen with another list of buttons or 
to another screen that navigates to a screen holding an image.

Modifying the list involves changing a column in the button list table inside the mysql server that is used by the project.
Do note that the column item in the table is going to be the name of the button that will be displayed on the screen.


# Acknowledgements
This project was a PBL project by the Computer and Electronic Engineering students of Asia Pacific College.
