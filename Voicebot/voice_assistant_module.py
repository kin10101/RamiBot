import sys
import speech_recognition as sr
import Voicebot.voicebotengine as voicebotengine
import Voicebot.pygtts as ts


# Constants
PAUSE_THRESHOLD = 0.8
ENERGY_THRESHOLD = 2000
OPERATION_TIMEOUT = 5000
DYNAMIC_ENERGY_THRESHOLD = True
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 8

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
    "hello remy",
    "hey siri"
]

def listen_to_command(recognizer, source):
    audio = recognizer.listen(source=source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
    text = recognizer.recognize_google(audio)
    return text.lower()

def handle_command(text, context):
    try:
        if text is not None:
            response = voicebotengine.handle_request(text, context)
            if response is not None:
                return response
    except:
        pass


def activate_on_wake_word():
    context = [""]
    recognizer = sr.Recognizer()

    try:
        print('speak now')
        with sr.Microphone() as source:
            print("listening for wake word")

            # transcribe audio input
            text = listen_to_command(recognizer, source)
            print("Audio received to text: " + text)

            # check wake word
            if any(variation in text for variation in WAKE_WORD_VARIATIONS):
                print('Wake word detected. Now listening...')
                ts.playAudioFile('audio/activate.wav')

                # listen for the command after wake word is detected
                text = listen_to_command(recognizer, source)
                print("Received command: " + text)

                response = handle_command(text, context)
                if response:
                    ts.speak(response, lang='en')

                ts.playAudioFile("audio/deactivate.wav")  # sound to indicate that the conversation is over

    except sr.RequestError:
        print("Could not request results from google Speech Recognition service")
    except sr.UnknownValueError:
        print("Wake word detected but unable to recognize speech")
    except sr.WaitTimeoutError:
        print("Timeout error while waiting for speech input")
    except KeyboardInterrupt:
        ts.speak("Goodbye")
        sys.exit()

def activate_on_click():
    context = [""]
    recognizer = sr.Recognizer()

    try:
        print('speak now')
        ts.playAudioFile('audio/activate.wav')
        with sr.Microphone() as source:
            print("listening now")

            # transcribe audio input
            text = listen_to_command(recognizer, source)
            print("Audio received to text: " + text)

            response = handle_command(text, context)
            if response:
                ts.speak(response, lang='en')

            ts.playAudioFile("audio/deactivate.wav")  # sound to indicate that the conversation is over

    except sr.RequestError:
        print("Could not request results from google Speech Recognition service")
    except sr.UnknownValueError:
            print("Wake word detected but unable to recognize speech")
    except sr.WaitTimeoutError:
        print("Timeout error while waiting for speech input")
    except KeyboardInterrupt:
        ts.speak("Goodbye")
        sys.exit()


def voice_assistant_loop():
    '''continuously listen for wake word and commands'''
    context = [""]

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = PAUSE_THRESHOLD
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.operation_timeout = OPERATION_TIMEOUT
    recognizer.dynamic_energy_threshold = DYNAMIC_ENERGY_THRESHOLD


    while True:
        wakeword_detected = False

        try:
            print('speak now')

            with sr.Microphone() as source:
                print("listening now")

                # transcribe audio input
                text = listen_to_command(recognizer, source)
                print("Audio received to text: " + text)

                # check wake word
                if any(variation in text for variation in WAKE_WORD_VARIATIONS):
                    wakeword_detected = True

                    wake_word_response = voicebotengine.get_from_json("GEN_hello")
                    # tts(wake_word_response, 'en')
                    # ts.speak(wake_word_response)

                    print('Wake word detected. Now listening...')
                    ts.playAudioFile('audio/activate.wav')

                    # serialModule.sendSerialMessage('2')

                    # listen for the command after wake word is detected
                    text = listen_to_command(recognizer, source)
                    print("Received command: " + text)


                    # generate a response from the chatbot
                    response = handle_command(text, context)
                    if response:
                        ts.speak(response, lang='en')

                    ts.playAudioFile("audio/deactivate.wav")  # sound to indicate that the conversation is over
                    # serialModule.sendSerialMessage('1')

        except sr.RequestError:
            print("Could not request results from google Speech Recognition service")
        except sr.UnknownValueError:
            if wakeword_detected is True:
                ts.playAudioFile('audio/deactivate.wav')  # sound to indicate that the wake word was not detected
                print("Wake word detected but unable to recognize speech")
        except sr.WaitTimeoutError:
            print("Timeout error while waiting for speech input")
        except KeyboardInterrupt:
            ts.speak("Goodbye")
            sys.exit()
