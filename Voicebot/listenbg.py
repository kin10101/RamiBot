import speech_recognition as sr

# Create a recognizer instance
recognizer = sr.Recognizer()

# Callback function to handle recognized speech
def callback(recognizer, audio):
    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to start listening in the background
def listen_in_background():
    with sr.Microphone() as source:
        print("Please speak something...")

        # Start listening in the background
        stop_listening = recognizer.listen_in_background(source, callback)

        # Keep the program running
        while True:
            pass

# Call the function to start listening in the background
listen_in_background()
