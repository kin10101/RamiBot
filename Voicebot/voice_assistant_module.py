import sys
import speech_recognition as sr
import Voicebot.voicebotengine as voicebotengine
import pygtts as ts
import gpio as gpio
from Voicebot.voicebotengine import Speech_Queue as Speech_Queue
import threading
import sounddevice # import this to remove warnings
from queue import Queue

from sql_module import show_value_as_bool

active_state = threading.Event()
Transcription_Queue = Queue()
Timeout_Queue = Queue()

class VoiceAssistant:
    def __init__(self):
        self.mic = sr.Microphone(device_index=6)
        self.pause_threshold = .8
        self.energy_threshold = 3500
        self.operation_timeout = 5000
        self.dynamic_energy_threshold = False
        self.listen_timeout = 3
        self.phrase_time_limit = 5
        self.wake_word_variations = [
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
            "hey siri",
            "hello"
        ]

    def listen_to_command(self, recognizer, source):

        audio = recognizer.listen(source=source, timeout=self.listen_timeout, phrase_time_limit=self.phrase_time_limit)
        text = recognizer.recognize_google(audio)
        return text.lower()

    def handle_command(self, text, context):
        try:
            if text is not None:
                response = voicebotengine.handle_request(text, context)
                if response is not None:
                    return response
        except Exception as e:
            print(f"Error handling command: {e}")

    def voice_assistant_loop(self):
        """if in idle screen, only listen for wakeword. if in active state, listen for any other convo."""

        print("Current mic being used: ", self.mic)
        context = [""]  # need to remove this
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = self.pause_threshold
        recognizer.energy_threshold = self.energy_threshold
        recognizer.operation_timeout = self.operation_timeout
        recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        while True:
            state = show_value_as_bool("admin_control", "RamiBot_Return", "ID", 1)
            # if ramibotreturn is set to 1, voice assistant is deactivated
            if state:
                print("voice assistant deactivated")
                pass
            # if ramibotreturn is set to 0, voice assistant is activated
            elif not state:
                if not active_state.is_set():  # while active state is not set (roaming, idle screen), listen for wake word.
                    print("wakeword listening active")
                    try:
                        with self.mic as source:
                            print('speak now')

                            text = self.listen_to_command(recognizer, source)
                            print("Audio received to text: " + text)

                            if any(variation in text for variation in self.wake_word_variations):  # if wake word detected
                                print('Wake word detected. Now listening...')


                                gpio.set_gpio_pin(4, 1)  # set GPIO pin to HIGH to stop the motor wheel from moving

                                # greet user
                                ts.play_audio_file('audio/activate.wav')
                                Speech_Queue.put("greetscreen")
                                wake_word_response = voicebotengine.get_from_json("GEN hello")
                                ts.speak(wake_word_response)

                    except sr.RequestError:
                        print("Could not request results from google Speech Recognition service")
                    except sr.UnknownValueError:
                        print("Wake word detected but unable to recognize speech")
                    except sr.WaitTimeoutError:
                        print("Timeout error while waiting for speech input")

                if active_state.is_set():  # while active state is set (rami stopped, gui active)
                    print("conversation mode active")
                    with self.mic as source:
                        text2 = None
                        response2 = None

                        while active_state.is_set():  # listen until something is heard from the user
                            print("SAY SOMETHING!!!")

                            try:
                                text2 = self.listen_to_command(recognizer, source)
                                Transcription_Queue.put(text2)
                                Timeout_Queue.put("stop")
                                print("Received command: " + text2)
                            except:
                                text2 = None
                                pass
                            # generate a response from the chatbot
                            if text2 is not None:
                                try:
                                    response2 = self.handle_command(text2, context)
                                except:
                                    response2 = None
                                    pass

                            if response2 is not None:
                                ts.speak(response2)
                                ts.play_audio_file("audio/deactivate.wav")  # sound to indicate that the conversation is over
                                Timeout_Queue.put("start")
                                break
                            if not active_state.is_set():
                                break

    def run_once(self):
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = self.pause_threshold
        recognizer.energy_threshold = self.energy_threshold
        recognizer.operation_timeout = self.operation_timeout
        recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold

        print("Current mic being used: ", self.mic)
        context = [""]  # need to remove this

        if gpio.read_gpio_pin(17) == 0:
            print("voice assistant activated")
            with self.mic as source:
                print('speak now')
                try:
                    text = self.listen_to_command(recognizer, source)
                    print("Audio received to text: " + text)
                    response = self.handle_command(text, context)
                    if response is not None:
                        ts.speak(response)

                except sr.UnknownValueError:
                    print("Unable to recognize speech")
                except sr.WaitTimeoutError:
                    print("Timeout error while waiting for speech input")
        else:
            print("voice assistant deactivated")

if __name__ == "__main__":
    Voicebot = VoiceAssistant()
    # Voicebot.voice_assistant_loop()


    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

