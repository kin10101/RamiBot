import sys

import speech_recognition as sr

import serialModule
import voicebotengine
import mimictts as ts

WAKE_WORD = 'hello rami'
WAKE_WORD_VARIATIONS = [
    "hello ram",
    "hello mommy",
    "hello romy",
    "hello run",
    "hello robi",
    "hello ron",
    "hiram",
    "hey rami",
    "rami",
    "hey ronnie",
    "jeremy",
    "hi rami",
    "hi ronnie",
    "hello remy"
]


def handle_command(text, context):
    try:
        if text is not None:
            response = voicebotengine.handle_request(text, context)
            if response is not None:
                return response
    except:
        pass


def get_wake_word():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.pause_threshold = 0.8
        r.energy_threshold = 10000
        r.dynamic_energy_threshold = True

        audio = r.listen(source)
        text = r.recognize_google(audio)
        return text.lower()


def test_assistant():
    context = [""]

    while True:
        wakeword_detected = False
        try:
            print('speak now')

            # record audio from microphone
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.pause_threshold = 0.8
                r.energy_threshold = 9000
                r.operation_timeout = 5000
                r.dynamic_energy_threshold = True

                audio = r.listen(source=source, timeout=5, phrase_time_limit=8)
                print("listening now")

                # transcribe audio input
                text = r.recognize_google(audio)
                text = text.lower()
                print("Audio received to text: " + text)


                # check wake word
                if any(variation in text for variation in WAKE_WORD_VARIATIONS):
                    wakeword_detected = True
                    wake_word_response = voicebotengine.get_from_json("GEN hello")
                    ts.speak(wake_word_response)
                    print('Wake word detected. Now listening...')
                    ts.playAudioFile('audio/activate.wav')

                    serialModule.sendSerialMessage('S')


                    # listen for the command after wake word is detected
                    audio = r.listen(source=source, timeout=5, phrase_time_limit=8)
                    text = r.recognize_google(audio, language='english')
                    text = text.lower()
                    print("Recieved command: " + text)

                    # generate a response from the chatbot
                    response = handle_command(text, context)
                    if response:
                        ts.speak(response)

                    ts.playAudioFile("audio/deactivate.wav")  # sound to indicate that the conversation is over
                    serialModule.sendSerialMessage('R')


        except sr.RequestError:
            print("Could not request results from google Speech Recognition service")
        except sr.UnknownValueError:
            if wakeword_detected is True:
                ts.playAudioFile('audio/deactivate.wav') #sound to indicate that the wake word was not detected
                print("Wake word detected")

            print("Unable to recognize speech")
        except sr.WaitTimeoutError:
            print("Timeout error while waiting for speech input")
        except KeyboardInterrupt:
            ts.speak("Goodbye")
            sys.exit()
