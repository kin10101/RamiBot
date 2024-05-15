
from kivymd.uix.button import MDFillRoundFlatButton

from Facerecog import trainedModel
from Facerecog import main
from Facerecog import test
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

        # self.main_menu_button_list = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
        # self.office_sched_button_list = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
        # self.programs_offered_button_list = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
        # self.school_info_button_list = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
        # self.floor_maps_button_list = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")

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

        screen_manager.add_widget(Builder.load_file('office_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('faculty_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('programs_offered.kv'))
        screen_manager.add_widget(Builder.load_file('school_information.kv'))
        screen_manager.add_widget(Builder.load_file('floor_maps.kv'))

        screen_manager.add_widget(Builder.load_file('image_info.kv'))

        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))
        screen_manager.add_widget(Builder.load_file('chatscreen.kv'))

        screen_manager.add_widget(Builder.load_file('Office KVs/officehours.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/officeInfo.kv'))

        screen_manager.add_widget(Builder.load_file('Announcements KVs/announcements.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/Tuitions/tuitionInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/Tuitions/tuitions.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/orgs.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/orgsInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/specialOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Orgs/acadsOrg.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Calendar/calendars.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/School Calendar/calendarInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/Scholarships/scholarships.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/Scholarships/scholarInfo.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/About APC/Accreditations.kv'))
        screen_manager.add_widget(Builder.load_file('Announcements KVs/About APC/APCinfo.kv'))

        screen_manager.add_widget(Builder.load_file('Faculty Scheds KVs/faculty.kv'))
        screen_manager.add_widget(Builder.load_file('Faculty Scheds KVs/facultyInfo.kv'))

        screen_manager.add_widget(Builder.load_file('Floors KVs/floormaps.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor.kv'))

        screen_manager.add_widget(Builder.load_file('Programs KVs/programsoffered.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/programs.kv'))

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

        Clock.schedule_interval(self.await_change_screen, .5)
        Clock.schedule_interval(self.await_pin_change, 1)

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
        path = ""  # get path source location
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

    # FACE RECOGNITION ---------------------------------
    def warning(self):
        global warning_popup
        warning_popup = Popup(title="", content=Builder.load_file("warning.kv"), size_hint=(None, None),
                              size=(500, 400), background_color=(1, 1, 1, .0))
        warning_popup.open()

    def warning_ok_button(self):

        print("warning ok button pressed")
        warning_popup.dismiss()

    def open_popup(self):
        global popup
        popup = Popup(title="", content=Builder.load_file("New User KVs/facerecog_popup.kv"), size_hint=(None, None),
                      size=(500, 400), background_color=(1, 1, 1, .0))
        popup.open()

    def ok_button(self):
        global start

        print("ok button pressed")
        start = True
        popup.dismiss()

    def cancel_button(self):
        global start

        print("cancel button pressed")
        start = False
        self.change_screen('userstatus')
        popup.dismiss()

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

            if not all([user_ID, given_name, last_name, nickname, role]):  # Check if any of the variables are empty
                raise ValueError("Empty fields detected")

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)
            print("Uploaded to database successfully!")
            self.open_popup()

        except ValueError as ve:
            print(f"Error: {ve}")
            self.warning()
            self.change_screen('adduserscreen')
        except Exception as e:
            print(f"Error in uploading to db: {e}")
            self.warning()
            self.change_screen('adduserscreen')

    def add_visitor_user_to_db(self):
        global user_ID
        MainApp.add_user_flag = 2
        try:
            user_ID = DataCollector.generate_visitor_id()
            given_name = self.get_text('adduser2', 'given_name')
            middle_initial = self.get_text('adduser2', 'middle_initial')
            last_name = self.get_text('adduser2', 'last_name')
            nickname = self.get_text('adduser2', 'nickname')
            role = self.get_text('adduser2', 'profession')

            if not all([user_ID, given_name, last_name, nickname, role]):  # Check if any of the variables are empty
                raise ValueError("Empty fields detected")
            else:
                # Only upload to the database if there are no errors
                DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)
                print("Uploaded to database successfully!")
                self.open_popup()

        except ValueError as ve:
            print(f"Error: {ve}")
            self.warning()
            self.change_screen('adduser2')
        except Exception as e:
            print(f"Error in uploading to db: {e}")
            self.warning()
            self.change_screen('adduser2')

    def captures(self):

        if start is not False:
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
                faces = detect.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=8, minSize=(60, 60))

                for (x, y, w, h) in faces:
                    # Increment the count for each detected face
                    count += 1

                    face_image = gray_eq[y:y + h, x:x + w]
                    image_path = os.path.join(user_dir, f"User.{user_id}.{count}.jpg")
                    cv2.imwrite(image_path, face_image)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

                    if count >= 50:
                        # Release the video capture and exit the application
                        self.camera.release()
                        cv2.destroyAllWindows()
        else:
            self.change_screen('newuser')

    def face_recognition_module(self):
        if self.charge_pin == 0:
            print('ACTIVE FACE SCANNING')
            self.camera = cv2.VideoCapture(0)
            #conf = trainedModel.face_recognition(self.camera)
            conf = test.realtime_face_recognition(self.camera)

            # if conf is not None:
            #     gpio.set_gpio_pin(4, 1)
            #     put_in_queue(screen_queue, 'greetscreen')
            #     self.update_label('greetscreen', 'greet_user_label', f'{main.result_text}')
            #
            #     print(f"{main.result_text}")
            #     pygtts.speak(f'{main.result_text}')

            if conf:
                gpio.set_gpio_pin(4, 1)
                put_in_queue(screen_queue, 'greetscreen')
                self.update_label('greetscreen', 'greet_user_label', f'{main.result_text}')

                print(f"{main.result_text}")

                if main.great_user:
                    pygtts.speak(f'{main.result_text}')

    def is_face_recognized(self):
        lower_conf = main.lower_conf
        print(f"lower_conf: {lower_conf}")

        if lower_conf is True:
            self.change_screen('newuser')

        elif lower_conf is False:
            self.change_screen('mainmenu')

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
        print("set")

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
    voice = threading.Thread(target=voice_thread)
    voice.daemon = True
    voice.start()


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-SemiBold.ttf")

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

    start_voice_thread()

    # Event States

    stop_motor = threading.Event()
    # set events to stop thread processes and clear event to resume

    app.run()

