# Standard library imports
import random
import threading
import time
from queue import Queue, Empty

# Third party imports
import cv2
import requests
from kivy.core.audio import SoundLoader
from kivymd.uix.dialog import MDDialog
from requests.exceptions import Timeout
import gpio
import TTS
import sql_module
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton

# Local application imports
from Chatbot.chatbot import handle_request
from Chatbot.chatbotGUI import Command, Response
from Facerecog import face_recog_module
from Voicebot import voicebotengine
from Voicebot.voice_assistant_module import VoiceAssistant, active_state, Transcription_Queue, Timeout_Queue

import config

Window.size = config.WINDOW_SIZE
Window.fullscreen = True
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

HOST_IP = config.HOST_IP
IMAGE_PATH = config.IMAGE_PATH
REQUEST_TIMEOUT = config.REQUEST_TIMEOUT
TIMEOUT_DURATION = config.TIMEOUT_DURATION
ANNOUNCEMENT_INTERVAL = config.ANNOUNCEMENT_INTERVAL

CAMERA_INDEX = config.CAMERA_INDEX

halign = "center"


def _set_missing_image():
    """Helper method to set the missing image"""
    screen_manager.get_screen('image_info').ids.img.source = "Assets/missing.png"
    screen_manager.get_screen('image_info').ids.img.reload()


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_sound = SoundLoader.load('audio/button_click.mp3')
        self.timeout = None
        self.camera = cv2.VideoCapture(CAMERA_INDEX)

        self.Main_Menu = sql_module.get_column_data("button_list", "main_menu")
        self.Office_Schedule = sql_module.get_column_data("button_list", "office_schedule")
        self.Faculty_Schedule = sql_module.get_column_data("button_list", "faculty_schedule")
        self.SOE_Faculty = sql_module.get_column_data("button_list", "soe_faculty")
        self.SHS_Faculty = sql_module.get_column_data("button_list", "shs_faculty")
        self.SOAR_Faculty = sql_module.get_column_data("button_list", "soar_faculty")
        self.SOCIT_Faculty = sql_module.get_column_data("button_list", "socit_faculty")
        self.SOM_Faculty = sql_module.get_column_data("button_list", "som_faculty")
        self.SOMA_Faculty = sql_module.get_column_data("button_list", "soma_faculty")
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

        self.keyboard_status = False
        self.current_screen = None
        self.previous_screen = None

        self.timeout_trigger = Clock.create_trigger(self.timeout_reset, TIMEOUT_DURATION)
        self.trigger_idle_start = Clock.create_trigger(self.start_timer)
        self.trigger_idle_stop = Clock.create_trigger(self.stop_timer)
        self.trigger_idle_reset = Clock.create_trigger(self.reset_timer)

    stop_face = threading.Event()

    def build(self):
        global screen_manager
        screen_manager = ScreenManager(transition=NoTransition())

        # ADD ALL SCREENS TO BE USED HERE
        screen_manager.add_widget(Builder.load_file('KV Screens/idlescreen.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/lowbatteryscreen.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/greetscreen.kv'))

        # MAY BUTTON LIST
        screen_manager.add_widget(Builder.load_file('KV Screens/main.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/chatscreen.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/voicescreen.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/office_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/faculty_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/programs_offered.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/soe_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/shs_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/soar_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/socit_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/som_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/soma_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/gs_faculty.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/school_information.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/other_information.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/accreditations_and_certifications.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/tuition_fees.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/school_calendar.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/school_organizations.kv'))
        screen_manager.add_widget(Builder.load_file('KV Screens/floor_maps.kv'))

        screen_manager.add_widget(Builder.load_file('KV Screens/image_info.kv'))

        screen_manager.add_widget(Builder.load_file('KV Screens/suggestions.kv'))


        Window.bind(on_touch_down=self.on_touch_down)
        print("built")
        return screen_manager

    def on_touch_down(self, touch, *args):
        self.reset_timer()

    def on_start(self):
        sql_module.connect()
        Clock.schedule_interval(self.await_change_gui_elements, .3)
        Clock.schedule_interval(self.await_recharge_change, .5)

        #Clock.schedule_interval(self.await_timeout_change, .5)

        Clock.schedule_interval(self.show_active_threads, 5)

    def show_active_threads(self, dt=None):
        print("\nActive Threads:")
        for thread in threading.enumerate():
            print(f"Thread Name: {thread.name}, Thread ID: {thread.ident}, Daemon: {thread.daemon}")

    def on_stop(self):
        sql_module.disconnect()

    def request_image(self, image, timeout=REQUEST_TIMEOUT):
        """
        Request an image from the server and save it locally.

        Args:
        image (str): The image path (with or without extension)
        timeout (int): The timeout for the request in seconds (default 10)
        """
        try:
            # Check if the image path ends with .png, if not add .png
            if not image.endswith('.png'):
                image += '.png'

            # Send the request to the server with a timeout
            response = requests.get(f'{HOST_IP}/get_image/{image}', timeout=timeout)

            if response.status_code == 200:
                # Write to temp file
                with open(IMAGE_PATH, 'wb') as f:
                    f.write(response.content)
                    print("Image downloaded successfully")
                screen_manager.get_screen('image_info').ids.img.source = IMAGE_PATH
                screen_manager.get_screen('image_info').ids.img.reload()
            else:
                print(f"Failed to load image: {response.status_code}")
                _set_missing_image()
        except Timeout:
            print(f"Request timed out after {timeout} seconds")
            _set_missing_image()
        except Exception as e:
            print(f"Failed to load image: {e}")
            _set_missing_image()

    # GUI BUTTONS -------------------------------------

    def submit_suggestion(self, suggestion):
        """Submit a suggestion to the database."""
        print(suggestion)
        sql_module.add_row_to_suggestions(suggestion, time.strftime("%H:%M:%S"), time.strftime("%Y-%m-%d"))
        print("Suggestion submitted")

    def play_button_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def back_button(self):
        self.button_sound()
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
        if self.button_sound:
            self.button_sound.play()
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
        if self.button_sound:
            self.button_sound.play()
        screen_manager.current = "image_info"  # navigate to image info screen
        self.request_image(button_text)  # request image from server

    def clear_buttons(self):
        # Get a reference to the button layout
        button_layout = screen_manager.get_screen(screen_manager.current).ids.button_layout

        # Remove all children (buttons) from the button layout
        if button_layout.children:
            button_layout.clear_widgets()

    # GUI MODIFIERS -------------------------------------

    def update_label(self, screen_name, id, text):
        """Update labels in mapscreen"""
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

    # AWAIT FUNCTIONS -------------------------------------

    def await_change_gui_elements(self, dt):

        if not screen_queue.empty():
            item = screen_queue.get_nowait()
            print(item)

            current_screen = screen_manager.current
            if item != current_screen:
                self.change_screen(item)
        else:
            pass

        # check if there is an item in the queue and change image accordingly
        if not image_queue.empty():
            current_screen = screen_manager.current
            if current_screen == 'image_info':
                image_path = image_queue.get_nowait()
                self.request_image(image_path)  # request image from server
        else:
            pass


    def await_face_change(self, dt):
        """periodically check if an item is in queue and change face image accordingly"""
        if not image_queue.empty():
            current_screen = screen_manager.current
            if current_screen == 'idlescreen':
                image_path = image_queue.get_nowait()

                self.update_image(current_screen, 'face', image_path)
        else:
            pass

    def await_recharge_change(self, dt):
        """periodically check if return to charger status is low and change screen accordingly"""
        try:
            state = sql_module.show_value_as_bool("admin_control", "LCD_state", "ID", 1)

            if state:
                if screen_manager.current != 'lowbatteryscreen':
                    put_in_queue(screen_queue, 'lowbatteryscreen')
                else:
                    pass
            if not state:

                if screen_manager.current == 'lowbatteryscreen':
                    put_in_queue(screen_queue, 'idlescreen')
                else:
                    pass

        except:
            print("pin reading error")
            pass

    def await_timeout_change(self, dt):
        """periodically handles executing timeout commands from inputs in the timeout queue from other threads"""
        if not Timeout_Queue.empty():
            item = Timeout_Queue.get_nowait()
            print(item + "in timeout queue")
            if item == 'reset':
                self.reset_timer()
                print("reset")
            if item == 'start':
                self.start_timer()
                print("start")
            if item == 'stop':
                self.stop_timer()
                print("stop")


    # FACE FUNCTIONS -------------------------------------

    def face_blink(self, dt):
        if screen_manager.current == 'idlescreen':
            blink_probability = random.randint(1, 10)  # Generate a random number between 1 and 10
            if blink_probability > 8:
                print("Blinking")
                put_in_queue(image_queue, 'rami_faces/blink.png')
                put_in_queue(image_queue, 'rami_faces/smile.png')

    def set_face_blink(self):
        Clock.schedule_interval(self.await_face_change, .8)
        Clock.schedule_interval(self.face_blink, 3)
        if screen_manager.current != 'idlescreen':
            Clock.unschedule(self.face_blink)
            Clock.unschedule(self.await_face_change)
            print("unscheduled face blink")

    def change_face_and_speak(self, text, face_path):
        # Change the face
        put_in_queue(image_queue, face_path)
        # Start the thread
        TTS.speak_async(text)

    def idle_announcement(self, dt):
        column_data = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
        text = random.choice(column_data)

        self.change_face_and_speak(text, 'rami_faces/wink.png')
        # back to normal face after speaking
        put_in_queue(image_queue, 'rami_faces/smile.png')

    def schedule_idle_announcement(self):
        print("Current Screen: ", screen_manager.current)
        if screen_manager.current == 'idlescreen':
            Clock.schedule_interval(self.idle_announcement, ANNOUNCEMENT_INTERVAL)

    def unschedule_idle_announcement(self):
        Clock.unschedule(self.idle_announcement)

    def get_current_screen(self):
        print("Current Screen is ", screen_manager.current)
        return screen_manager.current

    # FACE DETECTION --------------------------------------
    def face_detection_module(self):
        print(face_recog_module.person_detected)

        if not sql_module.show_value_as_bool("admin_control", "LCD_state", "ID", 1):
            print('ACTIVE FACE SCANNING')
            self.camera = cv2.VideoCapture(CAMERA_INDEX)
            detected = face_recog_module.realtime_face_recognition(self.camera)

            if detected:
                # gpio.set_gpio_pin(4, 1)
                self.on_motor()
                TTS.speak_async(detected)  # Speak the greeting for the detected person
                #TTS.play_audio_file_async(detected)

                put_in_queue(screen_queue, 'greetscreen')

    def close_camera(self):
        self.camera.release()

    # CHATBOT --------------------------------------

    def send_message(self):
        """Send a message."""
        start_time = time.time()

        self.input_text = screen_manager.get_screen("chatscreen").text_input.text.strip()
        if self.input_text:
            self.add_message_to_chat()
        screen_manager.get_screen("chatscreen").text_input.text = ""
        self.get_text_input()
        response, confidence_score, intent_tag = self.response()

        end_time = time.time()  # End time after the function execution
        execution_time = end_time - start_time  # Calculate the execution time

        # log the chatbot results
        sql_module.add_row_to_chatbot_results(response_time=execution_time,
                                              intent_recognized=intent_tag,
                                              confidence_score=confidence_score,
                                              received_text=self.input_text,
                                              bot_response=response,
                                              query_time=time.strftime("%H:%M:%S"),
                                              query_date=time.strftime("%Y-%m-%d"),
                                              error_code="None")

    def add_message_to_chat(self):
        """Add the message to the chat list."""
        global size, halign, value
        value = self.input_text
        self.set_message_size_and_alignment()
        screen_manager.get_screen("chatscreen").chat_list.add_widget(
            Command(text=value, size_hint_x=size, halign=halign))

    def set_message_size_and_alignment(self):
        """Set the size and alignment of the message boxbased on its length."""
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
        response, confidence_score, intent_tag = handle_request(self.input_text.lower())

        screen_manager.get_screen("chatscreen").chat_list.add_widget(
            Response(text=response, size_hint_x=.75, halign=halign))
        return response, confidence_score, intent_tag

    def clear_chat(self):
        screen_manager.get_screen("chatscreen").ids.chat_list.clear_widgets()

    def move_text_box(self):
        text_box = screen_manager.get_screen("chatscreen").ids.text_bar_layout

        if self.keyboard_status:
            text_box.pos_hint = {"center_y": 0.05}
            self.keyboard_status = False
        else:
            text_box.pos_hint = {"center_y": 0.558}
            self.keyboard_status = True

        screen_manager.do_layout()

    # VOICEBOT --------------------------------------

    def tap_to_talk(self):
        print("talk with rami button pressed")

        screen_manager.get_screen("voicescreen").ids.retry_message.opacity = 0
        self.update_voice_gui_to_default()

        # Disable the mic button
        mic_button = screen_manager.get_screen("voicescreen").ids.mic_button
        mic_button.disabled = True

        # Hide the back button
        back_button = screen_manager.get_screen("voicescreen").ids.back_button
        back_button.opacity = 0  # Make the button invisible
        back_button.disabled = True  # Disable the button

        # change button_box color to indicate listening
        screen_manager.get_screen("voicescreen").ids.button_box.md_bg_color = (.1745, .55, .2685, 1)
        screen_manager.get_screen("voicescreen").ids.button_box_text.text = "Listening..."

        # change bot_icon image to indicate listening
        screen_manager.get_screen("voicescreen").ids.bot_icon.source = "Assets/listening.png"
        screen_manager.get_screen("voicescreen").ids.bot_icon.reload()

        # Schedule the wait message
        Clock.schedule_once(self.show_wait_message, 5)
        # Schedule again for extra 3 seconds
        self.wait_event = Clock.schedule_once(self.show_wait_message, 8)

        # Start a new thread for the voice assistant function
        voice_thread = threading.Thread(target=self.run_voice_assistant)
        voice_thread.start()

    def show_wait_message(self, dt):
        wait_message = ["Please wait...", "Any second now...", "Processing your audio...", "Analyzing your command...",
                        "Almost there...", "Just a moment...", "Processing...", "Analyzing...", "Just a sec..."]
        random_wait_message = random.choice(wait_message)
        screen_manager.get_screen("voicescreen").ids.button_box.md_bg_color = (.5, .5, .5, 1)  # Grey color
        screen_manager.get_screen("voicescreen").ids.button_box_text.text = random_wait_message


    def run_voice_assistant(self):
        voicebot.voice_assistant_tap_to_speak(self.update_gui_after_voice_command)

    def update_gui_after_voice_command(self, status, message, response):
        # This function is called from a different thread, so we need to schedule the GUI update on the main thread
        Clock.schedule_once(lambda dt: self._update_gui(status, message, response))

    def _update_gui(self, status, message, response=None):
        screen_manager.get_screen("voicescreen").ids.retry_message.opacity = 0

        self.stop_timer()

        self.wait_event.cancel()

        if status == 'success':
            # hide button box
            screen_manager.get_screen("voicescreen").ids.button_box.opacity = 0
            screen_manager.get_screen("voicescreen").ids.button_box_text.opacity = 0
            # hide bot image
            screen_manager.get_screen("voicescreen").ids.bot_icon.opacity = 0
            screen_manager.get_screen("voicescreen").ids.bot_icon.source = ""
            screen_manager.get_screen("voicescreen").ids.bot_icon.reload()

            # show transcription
            screen_manager.get_screen("voicescreen").ids.audio_received_box.opacity = 1
            screen_manager.get_screen("voicescreen").ids.audio_received_text.opacity = 1
            screen_manager.get_screen("voicescreen").ids.transcribed_text.opacity = 1
            screen_manager.get_screen("voicescreen").ids.transcribed_text.text = message

            # show bot response
            screen_manager.get_screen("voicescreen").ids.bot_response_box.opacity = 1
            screen_manager.get_screen("voicescreen").ids.bot_response.opacity = 1
            screen_manager.get_screen("voicescreen").ids.bot_response.text = response

            if not image_queue.empty():
                screen_manager.get_screen("voicescreen").ids.image_info_button.opacity = 1
                screen_manager.get_screen("voicescreen").ids.image_info_button.disabled = False

            # show and reactivate try again button
            screen_manager.get_screen("voicescreen").ids.try_again_button.opacity = 1
            screen_manager.get_screen("voicescreen").ids.try_again_button.disabled = False

            # move back button to the side
            screen_manager.get_screen("voicescreen").ids.back_button.pos_hint = {"center_x": .75}

        elif status == 'error':
            # Handle error, update GUI accordingly
            screen_manager.get_screen("voicescreen").ids.button_box.md_bg_color = (.003, .4, .6, 1)
            screen_manager.get_screen("voicescreen").ids.button_box_text.text = "Error: " + message
            # change bot_icon image to indicate error
            screen_manager.get_screen("voicescreen").ids.bot_icon.source = "Assets/error.png"
            screen_manager.get_screen("voicescreen").ids.bot_icon.reload()
            screen_manager.get_screen("voicescreen").ids.retry_message.opacity = 1

        elif status == 'error_wait':
            self.wait_event.cancel()

            mic_button = screen_manager.get_screen("voicescreen").ids.mic_button
            mic_button.disabled = True


            screen_manager.get_screen("voicescreen").ids.button_box.md_bg_color = (.5, .5, .5, 1)  # Grey color
            screen_manager.get_screen("voicescreen").ids.button_box_text.text = message
            # change bot_icon image to indicate error
            screen_manager.get_screen("voicescreen").ids.bot_icon.source = "Assets/error.png"
            screen_manager.get_screen("voicescreen").ids.bot_icon.reload()


            Clock.schedule_once(self.update_voice_gui_to_default, 6)


        elif status == 'deactivated':
            # Handle deactivation, update GUI accordingly
            screen_manager.get_screen("voicescreen").ids.button_box.md_bg_color = (1, 1, 0, 1)  # Yellow color
            screen_manager.get_screen("voicescreen").ids.button_box_text.text = "Voice assistant deactivated"
            # change bot_icon image to indicate error
            screen_manager.get_screen("voicescreen").ids.bot_icon.source = "Assets/error.png"
            screen_manager.get_screen("voicescreen").ids.bot_icon.reload()


        # Re-enable the mic button
        mic_button = screen_manager.get_screen("voicescreen").ids.mic_button
        mic_button.disabled = False

        back_button = screen_manager.get_screen("voicescreen").ids.back_button
        back_button.opacity = 1  # Make the button visible
        back_button.disabled = False  # Enable the button

        # Schedule the GUI to start timeout again
        Clock.schedule_once(self.start_timer, 10)


    def update_voice_gui_to_default(self, dt=None):
        # return bot image
        screen_manager.get_screen("voicescreen").ids.bot_icon.opacity = 1
        screen_manager.get_screen("voicescreen").ids.bot_icon.source = "Assets/start.png"
        screen_manager.get_screen("voicescreen").ids.bot_icon.reload()

        # return button box to default
        screen_manager.get_screen("voicescreen").ids.button_box.opacity = 1
        screen_manager.get_screen("voicescreen").ids.button_box_text.opacity = 1
        screen_manager.get_screen("voicescreen").ids.button_box.md_bg_color = (.003, .4, .6, 1)
        screen_manager.get_screen("voicescreen").ids.button_box_text.text = "Press the microphone to start"
        screen_manager.get_screen("voicescreen").ids.mic_button.disabled = False



        # hide transcription bar
        screen_manager.get_screen("voicescreen").ids.audio_received_box.opacity = 0
        screen_manager.get_screen("voicescreen").ids.audio_received_text.opacity = 0
        screen_manager.get_screen("voicescreen").ids.transcribed_text.opacity = 0

        # hide bot response
        screen_manager.get_screen("voicescreen").ids.bot_response_box.opacity = 0
        screen_manager.get_screen("voicescreen").ids.bot_response.opacity = 0

        # hide retry message elements
        screen_manager.get_screen("voicescreen").ids.retry_message.opacity = 0

        # hide and deactivate try again button
        screen_manager.get_screen("voicescreen").ids.image_info_button.opacity = 0
        screen_manager.get_screen("voicescreen").ids.image_info_button.disabled = True

        screen_manager.get_screen("voicescreen").ids.try_again_button.opacity = 0
        screen_manager.get_screen("voicescreen").ids.try_again_button.disabled = True

        # move back button to the center
        screen_manager.get_screen("voicescreen").ids.back_button.pos_hint = {"center_x": .5}


        # GPIO --------------------------------------

    def gpio_cleanup(self):
        print('cleared pin values')
        gpio.set_gpio_pin(4, 0)
        gpio.GPIO.cleanup()

    def on_gpio(self):
        gpio.set_gpio_pin(4, 1)
        self.on_motor()

    def on_motor(self):
        sql_module.change_value("admin_control", "MOTOR_state", 0, "ID", 1)

    def off_motor(self):
        sql_module.change_value("admin_control", "MOTOR_state", 1, "ID", 1)

    def read_low_battery_state(self):
        sql_module.show_value("admin_control", "LCD_state", "ID", 1)

    # TIMER FUNCTIONS --------------------------------------
    def start_timer(self, dt=None):
        print("idle timer started")
        self.timeout_trigger()

    def reset_timer(self):
        print("idle timer reset")
        self.stop_timer()
        self.start_timer()

    def stop_timer(self):
        print("idle timer stopped")
        self.timeout_trigger.cancel()

    def timeout_reset(self, dt):
        self.stop_timer()
        self.on_motor()
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


def put_in_queue(myqueue, item):
    if not myqueue.empty() and myqueue.queue[0] == item:
        print("Item already at the front of the queue")
    else:
        myqueue.put(item)
        print("Placed " + item + "at" + str(myqueue))


def get_from_queue(myqueue):
    try:
        item = myqueue.get_nowait()
        return item
    except Empty:
        return None


def face_thread():
    print("face thread active")
    if not MainApp.stop_face.is_set():
        app.face_detection_module()
    else:
        print("FACE THREAD DISABLED")

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Fonts/Poppins-SemiBold.ttf")
    # Queues
    screen_queue = voicebotengine.Speech_Queue
    image_queue = voicebotengine.Image_Queue

    # inter thread communication
    # a clocked function checks and gets the items in the queue periodically

    # Classes
    voicebot = VoiceAssistant()
    app = MainApp()

    app.run()
