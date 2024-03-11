import sys
import speech_recognition as sr
import Voicebot.voicebotengine as voicebotengine
import Voicebot.pygtts as ts
import gpio as gpio
from queue import Queue, Empty


class VoiceAssistant:
    def __init__(self):
        self.pause_threshold = .8
        self.energy_threshold = 1800
        self.operation_timeout = 5000
        self.dynamic_energy_threshold = True
        self.listen_timeout = 3
        self.phrase_time_limit = 5
        self.gpio_pin = 17
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
            "hey siri"
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

    def activate_on_wake_word(self):
        context = [""]
        recognizer = sr.Recognizer()
        try:
            print('speak now')
            with sr.Microphone() as source:
                # recognizer.adjust_for_ambient_noise(source)
                print("listening for wake word")

                # transcribe audio input
                text = self.listen_to_command(recognizer, source)
                print("Audio received to text: " + text)

                # check wake word
                if any(variation in text for variation in self.wake_word_variations):
                    ts.play_audio_file('audio/activate.wav')
                    print('Wake word detected. Now listening...')
                    ts.play_audio_file('audio/activate.wav')

                    # open a new instance of the microphone
            with sr.Microphone() as source:
                print("Microphone reopened. Listening for command after wake word...")

                # listen for the command after wake word is detected
                text = self.listen_to_command(recognizer, source)
                print("Received command: " + text)

                response = self.handle_command(text, context)
                if response:
                    ts.speak(response, lang='en')

                ts.play_audio_file("audio/deactivate.wav")  # sound to indicate that the conversation is over

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
        except sr.UnknownValueError:
            print("Wake word detected but unable to recognize speech")
        except sr.WaitTimeoutError:
            print("Timeout error while waiting for speech input")
        except KeyboardInterrupt:
            ts.speak("Goodbye")
            sys.exit()

    # def activate_on_wake_word(self):
    #     context = [""]
    #     recognizer = sr.Recognizer()
    #
    #     try:
    #         print('speak now')
    #         with sr.Microphone() as source:
    #             print("listening for wake word")
    #
    #             # transcribe audio input
    #             text = self.listen_to_command(recognizer, source)
    #             print("Audio received to text: " + text)
    #
    #             # check wake word
    #             if any(variation in text for variation in self.wake_word_variations):
    #                 print('Wake word detected. Now listening...')
    #                 ts.play_audio_file('audio/activate.wav')
    #
    #                 # listen for the command after wake word is detected
    #                 text = self.listen_to_command(recognizer, source)
    #                 print("Received command: " + text)
    #
    #                 response = self.handle_command(text, context)
    #                 if response:
    #                     ts.speak(response, lang='en')
    #
    #                 ts.play_audio_file("audio/deactivate.wav")  # sound to indicate that the conversation is over
    #
    #     except sr.RequestError:
    #         print("Could not request results from google Speech Recognition service")
    #     except sr.UnknownValueError:
    #         print("Wake word detected but unable to recognize speech")
    #     except sr.WaitTimeoutError:
    #         print("Timeout error while waiting for speech input")
    #     except KeyboardInterrupt:
    #         ts.speak("Goodbye")
    #         sys.exit()

    def activate_on_button_press(self):
        '''activate when button is pressed in the GUI'''
        context = [""]
        recognizer = sr.Recognizer()

        try:
            print('speak now')
            with sr.Microphone() as source:

                print("listening for command")
                # ts.play_audio_file('audio/activate.wav')

                # listen for the command
                text = self.listen_to_command(recognizer, source)
                print("Received command: " + text)

                response = self.handle_command(text, context)
                if response:
                    ts.speak(response, lang='en')

                ts.play_audio_file("audio/deactivate.wav")  # sound to indicate that the conversation is over

        except sr.RequestError:
            print("Could not request results from google Speech Recognition service")
        except sr.UnknownValueError:
            print("Wake word detected but unable to recognize speech")
        except sr.WaitTimeoutError:
            print("Timeout error while waiting for speech input")
        except KeyboardInterrupt:
            ts.speak("Goodbye")
            sys.exit()

    def voice_assistant_loop(self):
        '''continuously listen for wake word and commands'''
        global wakeword_detected
        context = [""]

        recognizer = sr.Recognizer()
        recognizer.pause_threshold = self.pause_threshold
        recognizer.energy_threshold = self.energy_threshold
        recognizer.operation_timeout = self.operation_timeout
        recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold

        while True:
            wakeword_detected = False
            try:
                with sr.Microphone() as source:
                    print('speak now')
                    # transcribe audio input
                    text = self.listen_to_command(recognizer, source)
                    print("Audio received to text: " + text)

                    # check wake word
                    if any(variation in text for variation in self.wake_word_variations):
                        wakeword_detected = True
                        print('Wake word detected. Now listening...')

            except sr.RequestError:
                print("Could not request results from google Speech Recognition service")
            except sr.UnknownValueError:
                if wakeword_detected is True:
                    ts.play_audio_file('audio/deactivate.wav')  # sound to indicate that the wake word was not detected
                    print("Wake word detected but unable to recognize speech")
            except sr.WaitTimeoutError:
                print("Timeout error while waiting for speech input")

            if wakeword_detected is True:
                ts.play_audio_file('audio/activate.wav')
                wake_word_response = voicebotengine.get_from_json("GEN hello")
                # tts(wake_word_response, 'en')
                ts.speak(wake_word_response)

                with sr.Microphone() as source:

                    gpio.set_gpio_pin(4, 1)  # set GPIO pin to HIGH to stop the motor wheel from moving
                    text2 = None
                    response2 = None
                    while True:
                        # listen for the command after wake word is detected
                        try:
                            text2 = self.listen_to_command(recognizer, source)
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
                            ts.speak(response2, lang='en')

                            wakeword_detected = False
                            ts.play_audio_file(
                                "audio/deactivate.wav")  # sound to indicate that the conversation is over
                            break


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.voice_assistant_loop()
