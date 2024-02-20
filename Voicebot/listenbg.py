import speech_recognition as sr

# Function to handle the recognized speech
def handle_speech(recognizer, audio):
    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Create a recognizer instance
recognizer = sr.Recognizer()

# Create a microphone instance
microphone = sr.Microphone()

# Start listening in the background
stop_listening = recognizer.listen_in_background(microphone, handle_speech)

# Keep the program running indefinitely
while True:
    pass
