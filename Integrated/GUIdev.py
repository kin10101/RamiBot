import queue
import time

from Facerecog import trainedModel
from Facerecog import main

from Voicebot.voice_assistant_module import VoiceAssistant
import Voicebot.pygtts as pygtts
# gg
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

import threading
from queue import Queue, Empty

Window.size = (1920, 1080)
Window.fullscreen = True
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")


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
        screen_manager = ScreenManager()

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
        self.camera = cv2.VideoCapture(0)
        trainedModel.face_recognition(self.camera)
        # change the name in GUI
        conf = trainedModel.confidence_result
        if conf < 80:
            put_in_queue(event_queue, 'stop face')  # stop face scanning thread
            put_in_queue(screen_queue, 'greetings')  # navigate to greetings
            screen_manager.ids.greet_user.text = f'Good Day, {main.user_nickname}'
        else:
            put_in_queue(event_queue, 'stop face')  # stop face scanning thread
            put_in_queue(screen_queue, 'newuser')  # navigate to greetings
            change_screen('newuser')

    def on_start(self):
        #initial states
        stop_voice.set()

        Clock.schedule_interval(self.await_change_screen, 1)
        Clock.schedule_interval(self.await_change_state, .5)




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

            if item == 'stop motor': #experimental
                stop_motor.set()

            if item == "run motor":
                stop_motor.clear()


        except Empty:
            pass


def navigate_to_previous_screen():
    screen_manager.current = screen_manager.previous()


def change_screen(screen_name):
    screen_manager.current = screen_name


def put_in_queue(myqueue, item):
    myqueue.put(item)
    print("placed")


def get_from_queue(myqueue):
    try:
        return myqueue.get_nowait()
    except Empty:
        return None


def on_gpio(seconds):
    gpio.set_gpio_pin(17, 1)
    time.sleep(seconds)


def voice_thread():
    print("voice thread active")
    while True:
        if not stop_voice.is_set():
            voicebot.activate_on_button_press()
        else:
            pass


def face_thread():
    print("face thread active")
    while True:
        if not stop_face.is_set():
            app.face_recognition_module()
        else:
            pass

def static_motor_thread():
    while True:
        if stop_motor.is_set():
            on_gpio(30)
        else:
            pass

def dynamic_motor_thread():
    while True:
        if stop_motor.is_set():
            on_gpio(30)
        else:
            pass

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")
    # Queues
    event_queue = Queue()
    data_queue = Queue()
    screen_queue = Queue()
    # inter thread communication
    # a clocked function checks and gets the items in the queue periodically

    # Classes
    voicebot = VoiceAssistant()
    app = MainApp()

    # Threads
    voice_thread = threading.Thread(target=voice_thread)
    face_thread = threading.Thread(target=face_thread)
    voice_thread.daemon = True
    face_thread.daemon = True
    # processes running in the background indefinitely

    # face_thread identifies what the user wants and sends an item
    # in the change screen queue to change the current screen

    # Event States
    stop_voice = threading.Event()
    stop_face = threading.Event()
    stop_motor = threading.Event()
    # set events to stop thread processes and clear event to resume

    voice_thread.start()
    face_thread.start()

    app.run()
