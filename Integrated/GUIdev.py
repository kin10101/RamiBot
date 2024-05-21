
from kivymd.uix.button import MDFillRoundFlatButton

from Facerecog import main
from kivy.uix.popup import Popup

from kivy.metrics import dp

# Chatbot imports
from Chatbot.chatbot import handle_request
from Chatbot.chatbotGUI import Command, Response

import pygtts as pygtts
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
from Voicebot.voice_assistant_module import VoiceAssistant, active_state
import random
import time

import sql_module

Window.size = (1920, 1080)
Window.fullscreen = True
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
global count
global start
global screen_manager



class MainApp(MDApp):
    face_count = 0
    add_user_flag = 0
    global user_ID

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection = None
        self.timeout = None
        self.texture = None
        self.camera = cv2.VideoCapture(0)
        self.frame_count = None
        self.frame_rate = None
        self.num_images_to_capture = 50
        self.current_image_count = 0
        self.detect = None
        self.image = None
        self.charge_pin = gpio.read_gpio_pin(17)

        self.Main_Menu = sql_module.get_column_data("button_list", "main_menu")
        self.Office_Schedule = sql_module.get_column_data("button_list", "office_schedule")
        self.Faculty_Schedule = sql_module.get_column_data("button_list", "faculty_schedule")
        self.SOE_Faculty = sql_module.get_column_data("button_list", "soe_faculty")
        self.SHS_Faculty = sql_module.get_column_data("button_list", "shs_faculty")
        self.SOAR_Faculty = sql_module.get_column_data("button_list", "soar_faculty")
        self.SOCIT_Faculty = sql_module.get_column_data("button_list", "socit_faculty")
        self.SOM_Faculty = sql_module.get_column_data("button_list", "som_faculty")
        self.SOMAFaculty = sql_module.get_column_data("button_list", "soma_faculty")
        self.GS_Faculty = sql_module.get_column_data("button_list", "gs_faculty")
        self.Programs_Offered = sql_module.get_column_data("button_list", "programs_offered")
        self.School_Information = sql_module.get_column_data("button_list", "school_information")
        self.Other_Information = sql_module.get_column_data("button_list", "other_information")
        self.Accreditations_and_Certifications = sql_module.get_column_data("button_list",
                                                                            "accreditations_and_certifications")
        self.Tuition_Fees = sql_module.get_column_data("button_list", "tuition_fees")
        self.School_Calendar = sql_module.get_column_data("button_list", "school_calendar")
        self.School_Organizations = sql_module.get_column_data("button_list", "school_organizations")
        self.Floor_Maps = sql_module.get_column_data("button_list", "floor_maps")

        self.status = False
        self.current_screen = None
        self.previous_screen = None

    stop_voice = threading.Event()
    stop_face = threading.Event()

    def build(self):
        global screen_manager
        screen_manager = ScreenManager(transition=NoTransition())

        # ADD ALL SCREENS TO BE USED HERE
        screen_manager.add_widget(Builder.load_file('idlescreen.kv'))
        screen_manager.add_widget(Builder.load_file('lowbatteryscreen.kv'))
        screen_manager.add_widget(Builder.load_file('greetscreen.kv'))

        screen_manager.add_widget(Builder.load_file('New User KVs/face_capture_done.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/datacollect.kv'))

        # MAY BUTTON LIST
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('chatscreen.kv'))
        screen_manager.add_widget(Builder.load_file('office_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('faculty_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('programs_offered.kv'))
        screen_manager.add_widget(Builder.load_file('soe_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('shs_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('soar_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('socit_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('som_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('soma_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('gs_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('school_information.kv'))
        screen_manager.add_widget(Builder.load_file('other_information.kv'))
        screen_manager.add_widget(Builder.load_file('accreditations_and_certifications.kv'))
        screen_manager.add_widget(Builder.load_file('tuition_fees.kv'))
        screen_manager.add_widget(Builder.load_file('school_calendar.kv'))
        screen_manager.add_widget(Builder.load_file('school_organizations.kv'))
        screen_manager.add_widget(Builder.load_file('floor_maps.kv'))

        screen_manager.add_widget(Builder.load_file('image_info.kv'))


        Window.bind(on_touch_down=self.on_touch_down)
        print("built")
        return screen_manager

    def on_touch_down(self, touch, *args):
        self.reset_timer()

    def on_start(self):
        self.frame_rate = 10
        self.frame_count = 50
        self.texture = Texture.create(size=(640, 480), colorfmt='bgr')
        sql_module.connect()

        Clock.schedule_interval(self.await_change_screen, .3)
        Clock.schedule_interval(self.await_pin_change, 1)
        start_voice_thread()

    def on_stop(self):
        sql_module.disconnect()

    # GUI MODIFIERS -------------------------------------
    def back_button(self):
        screen_manager.current = self.previous_screen

    def create_button_list_to_button_list(self, button_list):
        self.clear_buttons()
        for button_text in button_list:
            button_title = button_text.replace("_", " ")
            button = MDFillRoundFlatButton(
                text=button_title,
                font_name='Poppins',
                font_size=24,
                halign='center',
                text_color=(1, 1, 1, 1),
                md_bg_color=(0.003, 0.4, 0.6, 1),
                size_hint=(0.7, None),
                pos_hint={'center_x': 0.5},
                padding=(30, 30),
                on_press=lambda instance, text=button_text: self.on_list_to_list(text)
            )
            screen_manager.get_screen(screen_manager.current).ids.button_layout.add_widget(button)

    def on_list_to_list(self, button_text):
        # Handle button press here
        print(f"Button {button_text} pressed")
        screen_manager.current = button_text

    def create_button_list_to_image_info(self, button_list):
        self.clear_buttons()

        for button_text in button_list:
            button_title = button_text.replace("_", " ")
            button = MDFillRoundFlatButton(
                text=button_title,
                font_name='Poppins',
                font_size=24,
                halign='center',
                text_color=(1, 1, 1, 1),
                md_bg_color=(0.003, 0.4, 0.6, 1),
                size_hint=(0.7, None),
                pos_hint={'center_x': 0.5},
                padding=(30, 30),
                on_press=lambda instance, text=button_text: self.on_list_to_image(text)
            )
            screen_manager.get_screen(screen_manager.current).ids.button_layout.add_widget(button)

    def on_list_to_image(self, button_text):

        print(f"Button {button_text} pressed")
        screen_manager.current = "image_info"  # navigate to image info screen
        path = "/home/rami/PycharmProjects/RamiBot/Integrated/Assets/Image Infos/"  # get path source location
        screen_manager.get_screen(screen_manager.current).ids.img.source = path + button_text + ".png"

    def clear_buttons(self):
        # Get a reference to the button layout
        button_layout = screen_manager.get_screen(screen_manager.current).ids.button_layout

        # Remove all children (buttons) from the button layout
        if button_layout.children:
            button_layout.clear_widgets()

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
        """Update image sources"""
        screen_name = self.root.get_screen(screen_name)
        try:
            label = screen_name.ids[id]
            label.source = source
        except:
            print("Source not found")
            pass

    connection = None  # Placeholder for the database connection
    pics_cursor = None  # Placeholder for the cursor

    def fetch_image_url(self, img_id):
        tables = ['calendars_img', 'floor_map', 'tuition_img', 'programs_img', 'offices', 'apcinfo_img', 'org_img']
        for table in tables:
            # Execute the query
            user_query = f"SELECT img_url FROM {table} WHERE img_identifier = %s"
            MainApp.pics_cursor.execute(user_query, (img_id,))
            image_found = MainApp.pics_cursor.fetchone()
            print(f"image found: {image_found}")

            if image_found:
                return image_found[0]

        return None

    def update_images(self, screenName, imageLabel, img_id):
        screens = self.root.get_screen(screenName)
        image_url = self.fetch_image_url(img_id)

        print(f"image url: {image_url}")
        if image_url:
            pic = screens.ids[imageLabel]
            pic.source = image_url
        else:
            print("Image not found")

    def fetch_all_images(self, table):
        tables = [table]
        all_images = []
        for table in tables:
            user_query = f"SELECT img_url FROM {table}"
            self.pics_cursor.execute(user_query)
            images = self.pics_cursor.fetchall()
            all_images.extend([img[0] for img in images])
        return all_images
    def update_all_images(self, screenName, table):
        screen = self.root.get_screen(screenName)
        images = self.fetch_all_images(table)
        image_widget = screen.ids.image_grid

        if images:
            print("Updating multiple images:")
            image_widget.clear_widgets()

            for image_url in images:
                new_image = Image(source=image_url, size_hint=(None, None), size=(dp(600), dp(800)))
                image_widget.add_widget(new_image)
                print(f"Added image: {image_url}")

        else:
            print("No images found")

    def get_text(self, screen_name, id):
        """Get text from textinput in newuser screen"""
        screen_name = self.root.get_screen(screen_name)

        try:
            text = screen_name.ids[id]
            return text.text

        except:
            print("Text not found")
            pass

    def change_screen(self, screen_name):
        screen_manager.current = screen_name

    def navigate_to_previous_screen(self):
        screen_manager.current = screen_manager.previous()

    def await_change_screen(self, dt):
        """periodically check if an item is in queue and change screen according to the screen name corresponding to
        the item in queue"""
        if not screen_queue.empty():
            item = screen_queue.get_nowait()
            print(item)

            current_screen = screen_manager.current
            if item != current_screen:
                self.change_screen(item)
            if not image_queue.empty():
                current_screen = screen_manager.current
                image_path = image_queue.get_nowait()

                self.update_image(current_screen, 'img', image_path)
            # TODO get the current screen and update the image


        else:
            pass

    def await_face_change(self, dt):
        if not image_queue.empty():
            current_screen = screen_manager.current
            if current_screen == 'idlescreen':
                image_path = image_queue.get_nowait()

                self.update_image(current_screen, 'face', image_path)
        else:
            pass

    def await_pin_change(self, dt):
        # print("current screen = ", screen_manager.current)

        try:
            pin = gpio.read_gpio_pin(17)
            self.charge_pin = pin

            if self.charge_pin == 1:
                # print("read one")
                if screen_manager.current != 'lowbatteryscreen':
                    put_in_queue(screen_queue, 'lowbatteryscreen')
                else:
                    pass
            if self.charge_pin == 0:
                # print("read zero")
                if screen_manager.current == 'lowbatteryscreen':
                    put_in_queue(screen_queue, 'idlescreen')
                else:
                    pass
        except:
            print("pin reading error")
            pass

    def face_blink(self, dt):
        if screen_manager.current == 'idlescreen':
            blink_probability = random.randint(1, 10)  # Generate a random number between 1 and 10
            if blink_probability > 8:
                put_in_queue(image_queue, 'rami_faces/blink.png')
                put_in_queue(image_queue, 'rami_faces/smile.png')

    def set_face_blink(self):
        Clock.schedule_interval(self.await_face_change, .8)
        Clock.schedule_interval(self.face_blink, 3)
        if screen_manager.current != 'idlescreen':
            Clock.unschedule(self.face_blink)
            Clock.unschedule(self.await_face_change)

    def change_face_and_speak(self, text, face_path):
        # Change the face
        put_in_queue(image_queue, face_path)
        # Start the thread
        speak_thread = threading.Thread(target=pygtts.speak, args=(text,))
        speak_thread.start()
        speak_thread.join()

    def idle_announcement(self, dt):

        column_data = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
        text = random.choice(column_data)

        self.change_face_and_speak(text, 'rami_faces/wink.png')


    def schedule_idle_announcement(self):
        print("Current Screen: ", screen_manager.current)
        if screen_manager.current == 'idlescreen':
            Clock.schedule_interval(self.idle_announcement, 40)

    def unschedule_idle_announcement(self):
        Clock.unschedule(self.idle_announcement)

    def get_current_screen(self):
        print("Current Screen is ", screen_manager.current)
        return screen_manager.current

    # FACE detection ---------------------------------
    def face_recognition_module(self):
        if self.charge_pin == 0:
            print('ACTIVE FACE SCANNING')
            self.camera = cv2.VideoCapture(0)
            main.realtime_face_recognition(self.camera)

            if main.person_detected is True:
                gpio.set_gpio_pin(4, 1)
                put_in_queue(screen_queue, 'greetscreen')
                self.update_label('greetscreen', 'greet_user_label', f'{main.greet_new_user()}')
                pygtts.speak(f'{main.greet_new_user()}')
                print(f"{main.greet_new_user()}")

    def close_camera(self):
        self.camera.release()

    # CHATBOT -----------------------------------------

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

    def clear_chat(self):
        screen_manager.get_screen("chatscreen").ids.chat_list.clear_widgets()

    def move_text_box(self):
        text_box = screen_manager.get_screen("chatscreen").ids.text_bar_layout

        if self.status:
            text_box.pos_hint = {"center_y": 0.05}
            self.status = False
        else:
            text_box.pos_hint = {"center_y": 0.58}
            self.status = True

        screen_manager.do_layout()

    # GPIO -------------------------------------------

    def gpio_cleanup(self):
        print('cleared pin values')
        gpio.set_gpio_pin(4, 0)
        gpio.GPIO.cleanup()

    def on_gpio(self, pin=4, state=1):
        gpio.set_gpio_pin(pin, state)

    # TIMER FUNCTIONS --------------------------------
    def start_timer(self):
        self.timeout = Clock.schedule_once(self.timeout_reset, 25)

    def reset_timer(self):
        self.timeout.cancel()
        self.start_timer()

    def stop_timer(self):
        self.timeout.cancel()

    def timeout_reset(self, dt):
        gpio.set_gpio_pin(4, 0)
        self.change_screen('idlescreen')

    # THREADS & EVENTS --------------------------------------

    def start_thread(self, thread_obj):
        thread = thread_obj()
        thread.start()
        return thread

    def start_face_thread(self):
        face = threading.Thread(target=face_thread)
        face.daemon = True
        face.start()

    def set_event(self, event=active_state):
        event.set()
        print("active_set")

    def clear_event(self, event=active_state):
        event.clear()
        print("cleared")

    def greet(self):
        wake_word_response = voicebotengine.get_from_json("GEN hello")
        pygtts.speak(wake_word_response)


def put_in_queue(myqueue, item):
    if not myqueue.empty() and myqueue.queue[0] == item:
        print("Item already at the front of the queue")
    else:
        myqueue.put(item)
        print("Placed " + item)


def get_from_queue(myqueue):
    try:
        item = myqueue.get_nowait()
        return item
    except Empty:
        return None


def face_thread():
    print("face thread active")
    if not MainApp.stop_face.is_set():
        app.face_recognition_module()
    else:
        print("FACE THREAD DISABLED")


def voice_thread():
    print("voice thread active")
    while True:
        if not MainApp.stop_voice.is_set():
            voicebot.voice_assistant_loop()
        else:
            print("VOICE THREAD DISABLED")
            pass


def start_voice_thread():
    print("starting voice thread")
    voice = threading.Thread(target=voice_thread)
    voice.daemon = True
    voice.start()
    print("voice thread now activeid")


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Fonts/Poppins-SemiBold.ttf")

    # Queues
    event_queue = Queue()
    screen_queue = voicebotengine.Speech_Queue
    image_queue = voicebotengine.Image_Queue
    # inter thread communication
    # a clocked function checks and gets the items in the queue periodically

    # Classes
    voicebot = VoiceAssistant()
    app = MainApp()

    # Thread initialization
    # Event States

    stop_motor = threading.Event()
    # set events to stop thread processes and clear event to resume

    app.run()

