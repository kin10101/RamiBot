import time

from Facerecog import trainedModel
from Facerecog import main

import Voicebot.pygtts as pygtts
import gpio

import cv2
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
import Facerecog.datacollect as DataCollector
import os
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition

import threading
from queue import Queue, Empty

Window.size = (1920, 1080)
Window.fullscreen = True
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
global count


class VoiceAssistant:
    def __init__(self):
        self.pause_threshold = .8
        self.energy_threshold = 2000
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
                print("listening for wake word")

                # transcribe audio input
                text = self.listen_to_command(recognizer, source)
                print("Audio received to text: " + text)

                # check wake word
                if any(variation in text for variation in self.wake_word_variations):

                    source.stop()  # stop recording to close the microphone

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

    def activate_on_button_press(self):
        '''activate when button is pressed in the GUI'''
        context = [""]
        recognizer = sr.Recognizer()

        try:
            print('speak now')
            with sr.Microphone() as source:
                print("listening for command")
                # ts.playAudioFile('audio/activate.wav')

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


class MainApp(MDApp):
    face_count = 0
    add_user_flag = 0
    global user_ID
    global start

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texture = None
        self.camera = None
        self.frame_count = None
        self.frame_rate = None
        self.num_images_to_capture = 50
        self.current_image_count = 0
        self.detect = None
        self.image = None

    def build(self):
        global screen_manager
        screen_manager = ScreenManager(transition=NoTransition())

        # ADD ALL SCREENS TO BE USED HERE
        screen_manager.add_widget(Builder.load_file('idleWindow.kv'))
        screen_manager.add_widget(Builder.load_file('greetWindow.kv'))

        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/datacollect.kv'))

        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))

        screen_manager.add_widget(Builder.load_file('Office KVs/officehours.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/admissions.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/finance.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/registrar.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/itro.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/bmo.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/logitics.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/do.kv'))

        screen_manager.add_widget(Builder.load_file('Announcements KVs/announcements.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/orgs.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/specialOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/acadsOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/pagOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/socioOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Calendar/calendars.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Calendar/calendarInfo.kv'))

        screen_manager.add_widget(Builder.load_file('faculty.kv'))

        screen_manager.add_widget(Builder.load_file('Floors KVs/floormaps.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor.kv'))

        screen_manager.add_widget(Builder.load_file('Programs KVs/programsoffered.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/programs.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gradSchool.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gsInfo.kv'))

        self.frame_rate = 10
        self.frame_count = 50
        self.texture = Texture.create(size=(640, 480), colorfmt='bgr')

        return screen_manager

    def update_label(self, screen_name, id, text):
        '''Update labels in mapscreen'''
        screen_name = self.root.get_screen(screen_name)
        try:
            label = screen_name.ids[id]
            label.text = text
        except:
            print("Label not found")
            pass

    def update_image(self, screen_name, id, source):
        '''Update image sources in mapscreen'''
        screen_name = self.root.get_screen(screen_name)
        try:
            label = screen_name.ids[id]
            label.source = source
        except:
            print("Source not found")
            pass

    def get_text(self, screen_name, id):
        '''Get text from textinput in newuser screen'''
        screen_name = self.root.get_screen(screen_name)

        try:
            text = screen_name.ids[id]
            return text.text

        except:
            print("Text not found")
            pass

    def add_apc_user_to_db(self):
        global user_ID
        MainApp.add_user_flag = 1
        try:
            user_ID = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            profession = self.get_text('adduser', 'profession')

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, profession)

        except Exception as e:
            print(f"Error in uploading to db: {e}")

    def add_visitor_user_to_db(self):
        global user_ID
        MainApp.add_user_flag = 2
        try:
            user_ID = DataCollector.generate_visitor_id()
            given_name = self.get_text('adduser2', 'given_name')
            middle_initial = self.get_text('adduser2', 'middle_initial')
            last_name = self.get_text('adduser2', 'last_name')
            nickname = self.get_text('adduser2', 'nickname')
            profession = self.get_text('adduser2', 'profession')

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, profession)
        except Exception as e:
            print(f"Error in uploading to db: {e}")

    def captures(self):
        global start

        user_dir = DataCollector.user_dir
        user_id = DataCollector.user_id

        count = 0

        self.image = Image(texture=self.texture)
        screen_manager.ids.camera = self.texture

        self.camera = cv2.VideoCapture(0)

        capture_width, capture_height = 640, 480

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)

        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Error reading frame from video source.")
                break

            frame = cv2.resize(frame, (capture_width, capture_height))

            buffer = cv2.flip(frame, 1).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

            self.image.texture = texture

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detect.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                # Increment the count for each detected face
                count += 1

                face_image = gray[y:y + h, x:x + w]
                image_path = os.path.join(user_dir, f"User.{user_id}.{count}.jpg")
                cv2.imwrite(image_path, face_image)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

                if count >= 50:
                    # Release the video capture and exit the application
                    self.camera.release()
                    cv2.destroyAllWindows()

    def face_recognition_module(self):
        print('ACTIVE FACE SCANNING')
        self.camera = cv2.VideoCapture(0)
        conf = trainedModel.face_recognition(self.camera)
        if conf is not None:
            gpio.set_gpio_pin(4, 1)
            put_in_queue(screen_queue, 'greetings')
            self.update_label('greetings', 'greet_user_label', f'Good Day, {main.user_nickname}')

    def on_start(self):
        Clock.schedule_interval(self.await_change_screen, .5)

    def await_change_screen(self, dt):
        """periodically check if an item is in queue and change screen according to the screen name corresponding to
        the item in queue"""
        try:
            item = screen_queue.get_nowait()
            print(item)
            change_screen(item)
        except Empty:
            pass

    def await_change_state(self, dt):
        """ periodically check if an item is in queue and set or clear an event"""
        try:
            item = event_queue.get_nowait()
            print(item)

            if item == 'stop face':
                stop_face.set()

            if item == "run face":
                stop_face.clear()

            if item == 'stop voice':
                stop_voice.set()

            if item == "run voice":
                stop_voice.clear()

            if item == 'stop motor':  # experimental
                stop_motor.set()

            if item == "run motor":
                stop_motor.clear()


        except Empty:
            pass

    def face_thread(self):
        face_thread.start()


def navigate_to_previous_screen():
    screen_manager.current = screen_manager.previous()


def change_screen(screen_name):
    screen_manager.current = screen_name


def put_in_queue(myqueue, item):
    myqueue.put(item)
    print("placed" + item)


def get_from_queue(myqueue):
    try:
        return myqueue.get_nowait()
    except Empty:
        return None


def voice_thread():
    print("voice thread active")
    while True:
        if not stop_voice.is_set():
            voicebot.activate_on_button_press()
        else:
            pass


def face_thread():
    print("face thread active")
    if not stop_face.is_set():
        app.face_recognition_module()


def timeout_counter(dt):
    global count
    count = count + 1
    if count == 30:
        change_screen('idlescreen')
        gpio.GPIO.cleanup()


def reset_timeout():
    global count
    count = 0


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")
    count = 0
    # Queues
    event_queue = Queue()
    screen_queue = Queue()
    # inter thread communication
    # a clocked function checks and gets the items in the queue periodically

    # Classes
    voicebot = VoiceAssistant()
    app = MainApp()

    # Thread initialization
    voice_thread = threading.Thread(target=voice_thread)
    face_thread = threading.Thread(target=face_thread)
    voice_thread.daemon = True
    face_thread.daemon = True

    # Event States
    stop_voice = threading.Event()
    stop_face = threading.Event()
    stop_motor = threading.Event()
    # set events to stop thread processes and clear event to resume

    # voice_thread.start()

    app.run()
