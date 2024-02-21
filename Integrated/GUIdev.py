import time

import Facerecog.main
from Facerecog import trainedModel
from Facerecog import main

# Chatbot imports
from Chatbot.chatbot import handle_request
from Chatbot.chatbotGUI import ChatScreen, Command, Response


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

from Voicebot import voicebotengine
from Voicebot.voice_assistant_module import VoiceAssistant

Window.size = (1920, 1080)
Window.fullscreen = True
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
global count


class MainApp(MDApp):
    face_count = 0
    add_user_flag = 0
    global user_ID
    global start

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timeout = None
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
        screen_manager.add_widget(Builder.load_file('idlescreen.kv'))
        screen_manager.add_widget(Builder.load_file('greetscreen.kv'))

        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/datacollect.kv'))

        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))
        screen_manager.add_widget(Builder.load_file('chatscreen.kv'))
    #ALISIN TONGCOMMENT

        screen_manager.add_widget(Builder.load_file('Office KVs/officehours.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/officeInfo.kv'))

        screen_manager.add_widget(Builder.load_file('Announcements KVs/announcements.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/orgs.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/orgsInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/specialOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/acadsOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/pagOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/socioOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Calendar/calendars.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Calendar/calendarInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/Scholarships/scholarships.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/Scholarships/scholarInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/About APC/aboutAPC.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/About APC/Accreditations.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/About APC/APCinfo.kv'))

        screen_manager.add_widget(Builder.load_file('faculty.kv'))

        screen_manager.add_widget(Builder.load_file('Floors KVs/floormaps.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor.kv'))

        screen_manager.add_widget(Builder.load_file('Programs KVs/programsoffered.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/programs.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gradSchool.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gsInfo.kv'))


        Window.bind(on_touch_down=self.on_touch_down)
        print("built")
        return screen_manager

    def on_touch_down(self, touch, *args):
        self.reset_timer()

    def on_start(self):

        self.frame_rate = 10
        self.frame_count = 50
        self.texture = Texture.create(size=(640, 480), colorfmt='bgr')

        Clock.schedule_interval(self.await_change_screen, .5)

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

    def navigate_to_previous_screen(self):
        screen_manager.current = screen_manager.previous()

    def add_apc_user_to_db(self):
        global user_ID
        MainApp.add_user_flag = 1
        try:
            user_ID = self.get_text('adduserscreen', 'school_id')
            given_name = self.get_text('adduserscreen', 'given_name')
            middle_initial = self.get_text('adduserscreen', 'middle_initial')
            last_name = self.get_text('adduserscreen', 'last_name')
            nickname = self.get_text('adduserscreen', 'nickname')
            role = self.get_text('adduserscreen', 'role')

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)

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
            role = self.get_text('adduser2', 'role')

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)
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
            gray_eq = cv2.equalizeHist(gray)
            faces = detect.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors= 50, minSize=(100, 100))

            for (x, y, w, h) in faces:
                # Increment the count for each detected face
                count += 1


                face_image = gray_eq[y:y + h, x:x + w]
                image_path = os.path.join(user_dir, f"User.{user_id}.{count}.jpg")
                cv2.imwrite(image_path, face_image)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

                if count >= 1000:
                    # Release the video capture and exit the application
                    self.camera.release()
                    cv2.destroyAllWindows()

    def face_recognition_module(self):
        print('ACTIVE FACE SCANNING')
        self.camera = cv2.VideoCapture(0)
        conf = trainedModel.face_recognition(self.camera)

        if conf is not None:
            gpio.set_gpio_pin(4, 1)
            put_in_queue(screen_queue, 'greetscreen')
            self.update_label('greetscreen', 'greet_user_label', f'{main.result_text}')
            pygtts.speak(f'{main.result_text}')

    def is_face_recognized(self):
        lower_conf = main.lower_conf
        if lower_conf is True:
            self.change_screen('newuser')

        if lower_conf is False:
            self.change_screen('mainmenu')


    def send_message(self):
        """Send a message."""
        self.input_text = screen_manager.get_screen("chatscreen").text_input.text.strip()
        if self.input_text:
            self.add_message_to_chat()
        screen_manager.get_screen("chatscreen").text_input.text = ""
        self.get_text_input()
        self.response()

    def add_message_to_chat(self):
        """Add the message to the chat list."""
        global size, halign, value
        value = self.input_text
        self.set_message_size_and_alignment()
        screen_manager.get_screen("chatscreen").chat_list.add_widget(
            Command(text=value, size_hint_x=size, halign=halign))

    def set_message_size_and_alignment(self):
        """Set the size and alignment of the message based on its length."""
        global size, halign
        if len(value) < 6:
            size = .22
            halign = "center"
        elif len(value) < 11:
            size = .32
            halign = "center"
        elif len(value) < 16:
            size = .45
            halign = "center"
        elif len(value) < 21:
            size = .58
            halign = "center"
        elif len(value) < 26:
            size = .71
            halign = "center"
        else:
            size = .85
            halign = "left"

    def get_text_input(self):
        """Print the input text."""
        print("Input text:", self.input_text)

    def response(self, *args):
        """Generate and display a response."""
        response = ""
        context = [""]
        response = handle_request(self.input_text.lower(), context)
        screen_manager.get_screen("chatscreen").chat_list.add_widget(
            Response(text=response, size_hint_x=.75, halign=halign))

    def gpio_cleanup(self):
        print('cleared pin values')
        gpio.set_gpio_pin(4, 0)
        gpio.GPIO.cleanup()

    def start_timer(self):
        self.timeout = Clock.schedule_once(self.timeout_reset, 30)

    def reset_timer(self):
        self.timeout.cancel()
        self.start_timer()

    def timeout_reset(self, dt):
        gpio.set_gpio_pin(4, 0)
        self.change_screen('idlescreen')

    def start_thread(self, thread_obj):
        thread = thread_obj()
        thread.start()
        return thread

    def change_screen(self, screen_name):
        screen_manager.current = screen_name


    def await_change_screen(self, dt):
        """periodically check if an item is in queue and change screen according to the screen name corresponding to
        the item in queue"""
        try:
            item = screen_queue.get_nowait()
            print(item)
            self.change_screen(item)
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


    def start_face_thread(self):
        face = threading.Thread(target=face_thread)
        face.daemon = True
        face.start()


def navigate_to_previous_screen(self):
    screen_manager.current = screen_manager.previous()





def put_in_queue(myqueue, item):
    myqueue.put(item)
    print("placed" + item)


def get_from_queue(myqueue):
    try:
        return myqueue.get_nowait()
    except Empty:
        return None

def face_thread():
    print("face thread active")
    if not stop_face.is_set():
        app.face_recognition_module()
def voice_thread():
    print("voice thread active")
    while True:
        if not stop_voice.is_set():
            voicebot.voice_assistant_loop()
        else:
            pass


def start_voice_thread():
    voice = threading.Thread(target=voice_thread)
    voice.daemon = True
    voice.start()









if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")

    # Queues
    event_queue = Queue()
    screen_queue = voicebotengine.Speech_Queue
    # inter thread communication
    # a clocked function checks and gets the items in the queue periodically

    # Classes
    voicebot = VoiceAssistant()
    app = MainApp()

    # Thread initialization

    start_voice_thread()

    # Event States
    stop_voice = threading.Event()
    stop_face = threading.Event()
    stop_motor = threading.Event()
    # set events to stop thread processes and clear event to resume

    app.run()
