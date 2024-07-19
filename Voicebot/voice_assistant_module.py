import os
import sys
import time

import speech_recognition as sr
import Voicebot.voicebotengine as voicebotengine
import TTS as ts
import gpio as gpio
from Voicebot.voicebotengine import Speech_Queue as Speech_Queue
import threading
import sounddevice  # import this to remove warnings
from queue import Queue

from sql_module import show_value_as_bool, add_row_to_voicebot_results

active_state = threading.Event()
Transcription_Queue = Queue()
Timeout_Queue = Queue()


class VoiceAssistant:
    def __init__(self):
        self.mic = sr.Microphone(device_index=os.getenv('DEVICE_INDEX')) # leave blank to use default microphone, or specify the device index to use a specific microphone
        self.pause_threshold = float(os.getenv('PAUSE_THRESHOLD'))
        self.energy_threshold = int(os.getenv('ENERGY_THRESHOLD'))
        self.operation_timeout = int(os.getenv('OPERATION_TIMEOUT'))
        self.dynamic_energy_threshold = os.getenv('DYNAMIC_ENERGY_THRESHOLD') == 'True'
        self.listen_timeout = int(os.getenv('LISTEN_TIMEOUT'))
        self.phrase_time_limit = int(os.getenv('PHRASE_TIME_LIMIT'))

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

    def handle_command(self, text):
        try:
            if text is not None:
                response, confidence_score, intent_tag = voicebotengine.handle_request(text)
                if response is not None:
                    return response, confidence_score, intent_tag
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

    def voice_assistant_tap_to_speak(self, callback):
        """Handle a single voice interaction for tap-to-speak mode."""

        print("Current mic being used: ", self.mic)
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = self.pause_threshold
        recognizer.energy_threshold = self.energy_threshold
        recognizer.operation_timeout = self.operation_timeout
        recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        error_code = None

        state = show_value_as_bool("admin_control", "RamiBot_Return", "ID", 1)

        if state:
            print("Voice assistant deactivated")
            callback('deactivated', None, None)
            return

        print("Tap-to-speak mode activated")
        #Timeout_Queue.put("stop")  # stop the idle screen timer

        try:
            with self.mic as source:
                # record time from here
                start_time = time.time()

                # audio confirmation that the voice assistant is active
                ts.play_audio_file('audio/activate.wav')

                # greet = voicebotengine.get_from_json("GEN hello")
                # ts.speak(greet)
                print('Speak now')
                text = self.listen_to_command(recognizer, source)
                print("Audio received to text: " + text)

                # Process the main command
                response, confidence_score, intent_tag = self.handle_command(text)  # Empty context
                end_time = time.time()  # End time after the function execution
                execution_time = end_time - start_time  # Calculate the execution time

                if response is not None:
                    callback('success', text, response)
                    print(f"The voice_assistant_tap_to_speak function took {execution_time} seconds to execute")

                    ts.speak(response)
                    ts.play_audio_file("audio/deactivate.wav")  # Sound to indicate that the interaction is over

        except sr.RequestError:
            end_time = time.time()  # End time after the function execution
            callback('error', "Could not request results from Google Speech Recognition service", None)
            print("Could not request results from Google Speech Recognition service")
            ts.speak("the APC network blocked me again! tell I T R O to fix it.")
            error_code = "RequestError: Could not request results from Google Speech Recognition service."

        except sr.UnknownValueError:
            end_time = time.time()  # End time after the function execution

            callback('error', "Unable to recognize speech", None)
            print("Unable to recognize speech")
            ts.speak("sorry, I couldn't hear you.")
            #ts.play_audio_file("audio/jp_couldnt_hear.mp3")
            error_code = "UnknownValueError: Unable to recognize speech."

        except sr.WaitTimeoutError:
            end_time = time.time()  # End time after the function execution

            callback('error', "Unable to recognize speech", None)
            print("Timeout error while waiting for speech input")
            ts.speak("sorry, I couldn't hear you.")
            error_code = "TimeoutError: the user took too long to respond."

        except AssertionError as e:
            end_time = time.time()  # End time after the function execution

            callback('error_wait', "Hey! I was still speaking!", None)
            print("Microphone is already in use")
            ts.speak("Hey! i was still speaking.")
            error_code = "AssertionError: User clicked the button while the bot was still speaking."

        finally:
            print("tap_to_speak function end. logging in results to database")
            execution_time = end_time - start_time  # Calculate the execution time

            # log results to database
            add_row_to_voicebot_results(response_time=execution_time,
                                        intent_recognized=intent_tag,
                                        confidence_score=confidence_score,
                                        transcribed_text=text,
                                        bot_response=response,
                                        query_time=time.strftime("%H:%M:%S"),
                                        query_date=time.strftime("%Y-%m-%d"),
                                        error_code=error_code)

if __name__ == "__main__":
    # get a list of available microphones and their index
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

