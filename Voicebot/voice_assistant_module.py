import os
import time

import requests
import speech_recognition as sr
from dotenv import load_dotenv

import Voicebot.voicebotengine as voicebotengine
import TTSapi as ts
import gpio as gpio
from Voicebot.voicebotengine import Speech_Queue as Speech_Queue
import threading
import sounddevice  # imported to remove warnings
from queue import Queue

from sql_module import show_value_as_bool, add_row_to_voicebot_results

active_state = threading.Event()
Timeout_Queue = Queue()



class VoiceAssistant:
    def __init__(self):
        load_dotenv()
        self.mic = sr.Microphone(device_index=int(os.getenv('DEVICE_INDEX'))) # leave blank to use default microphone, or specify the device index to use a specific microphone
        self.pause_threshold = float(os.getenv('PAUSE_THRESHOLD'))
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

    def request_voicebot_api(self, message):
        """requests query and returns response, confidence score, intent tag, and audio file"""
        url = 'http://192.168.80.4:5000/voicebot'
        url = 'http://127.0.0.1:5000/voicebot'

        # Prepare the data payload
        data = {
            'message': message  # The message sent by the client
        }

        try:
            # Send the POST request to the Flask endpoint with the message data
            result = requests.post(url, json=data)

            # Check if the request was successful
            if result.status_code == 200:
                # Parse the JSON response
                response_data = result.json()
                response = response_data['response']
                confidence_score = response_data['confidence_score']
                intent_tag = response_data['intent_tag']
                audio_file_url = response_data.get('audio_file_url')  # URL to download the audio file

                # Print the received response, confidence score, intent tag, and audio URL
                print('Response:', response)
                print('Confidence Score:', confidence_score)
                print('Intent Tag:', intent_tag)
                print('Audio File URL:', audio_file_url)

                # Optionally download the audio file
                if audio_file_url:
                    audio_response = requests.get(audio_file_url)
                    if audio_response.status_code == 200:
                        with open("output.mp3", "wb") as f:
                            f.write(audio_response.content)
                        print("Audio file downloaded successfully.")
                    else:
                        print("Failed to download the audio file.")

                return response, confidence_score, intent_tag, audio_file_url

            else:
                print(f'Error: Received status code {result.status_code}')
                return None, None, None, None

        except Exception as e:
            print(f'An error occurred: {e}')
            return None, None, None, None

    def voice_assistant_tap_to_speak(self, callback):
        """Handle a single voice interaction for tap-to-speak mode."""
        print("Current mic being used:", self.mic)
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = self.pause_threshold
        recognizer.operation_timeout = self.operation_timeout
        recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        error_code = None
        response, confidence_score, intent_tag, text = None, None, None, None

        state = show_value_as_bool("admin_control", "RamiBot_Return", "ID", 1)

        if state:
            print("Voice assistant deactivated")
            callback('deactivated', None, None)
            return

        print("Tap-to-speak mode activated")

        try:
            with self.mic as source:
                # Adjust for ambient noise
                print("Adjusting for ambient noise")
                recognizer.adjust_for_ambient_noise(source, duration=.5)  # Adjust the duration as needed

                # Record time from here
                start_time = time.time()

                # Audio confirmation that the voice assistant is active
                ts.play_audio_file('audio/activate.wav')
                print('Speak now')
                text = self.listen_to_command(recognizer, source)
                print("Audio received to text: " + text)

                # Process the main command
                response, confidence_score, intent_tag, audio_url = self.request_voicebot_api(text)
                end_time = time.time()  # End time after the function execution
                execution_time = end_time - start_time  # Calculate the execution time

                if response:
                    callback('success', text, response)
                    print(f"The voice_assistant_tap_to_speak function took {execution_time} seconds to execute")
                    ts.play_audio_file("output.mp3")
                    ts.play_audio_file("audio/deactivate.wav")  # Sound to indicate that the interaction is over

        except sr.RequestError:
            error_code = "RequestError: Could not request results from Google Speech Recognition service."
            print(error_code)
            ts.speak("The APC network blocked me again! Tell I T R O to fix it.")
            callback('error', error_code, None)

        except sr.UnknownValueError:
            error_code = "UnknownValueError: Unable to recognize speech."
            print(error_code)
            ts.speak("Sorry, I couldn't hear you.")
            callback('error', error_code, None)

        except sr.WaitTimeoutError:
            error_code = "TimeoutError: The user took too long to respond."
            print(error_code)
            ts.speak("Sorry, I couldn't hear you.")
            callback('error', error_code, None)

        except AssertionError:
            error_code = "AssertionError: User clicked the button while the bot was still speaking."
            print(error_code)
            ts.speak("Hey! I was still speaking.")
            callback('error_wait', error_code, None)

        finally:
            if 'end_time' in locals():
                execution_time = end_time - start_time  # Calculate the execution time
            print("tap_to_speak function end. logging in results to database")

            # Log the results to the database
            add_row_to_voicebot_results(response_time=execution_time,
                                        intent_recognized=intent_tag,
                                        confidence_score=confidence_score,
                                        transcribed_text=text,
                                        bot_response=response,
                                        query_time=time.strftime("%H:%M:%S"),
                                        query_date=time.strftime("%Y-%m-%d"),
                                        error_code=error_code)


if __name__ == "__main__":
    #get a list of available microphones and their index
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    ts.play_audio_file_async('audio/activate.wav')
    ts.play_audio_file_async('audio/deactivate.wav')

