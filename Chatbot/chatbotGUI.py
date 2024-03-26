import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.config import Config
from Chatbot.chatbot import handle_request
from kivy.uix.vkeyboard import VKeyboard

os.environ['MESA_LOADER_DRIVER_OVERRIDE'] = 'i965 ./kiwix-desktop'

Window.size = (1920, 1080)
Config.set('graphics', 'borderless', 0)  # 0 being off 1 being on as in true/false
Config.set('kivy','keyboard_mode','dock')

class ChatBubble(MDLabel):
    pass


class ChatScreen(Screen):
    pass


class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()

    font_size = 17


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()

    font_size = 17


class ChatBot(MDApp):
    input_text = ""

    def __init__(self, **kwargs):
        super().__init__()
        self.status = None

    def change_screen(self, screen_name):
        screen_manager.current = screen_name

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))
        self.status = False
        return screen_manager

    def send_message(self):
        global size, halign, value
        # Get the text from the text input
        self.input_text = screen_manager.get_screen("chatscreen").text_input.text.strip()

        # Check if the input text is not empty
        if self.input_text:
            value = self.input_text
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

            # Add the message to the chat list
            screen_manager.get_screen("chatscreen").chat_list.add_widget(
                Command(text=value, size_hint_x=size, halign=halign))
        # Clear the text input
        screen_manager.get_screen("chatscreen").text_input.text = ""
        self.get_text_input()
        self.response()

    def get_text_input(self):
        print("Input text:", self.input_text)

    def response(self, *args):
        response = ""
        context = [""]
        response = handle_request(self.input_text.lower(), context)
        screen_manager.get_screen("chatscreen").chat_list.add_widget(
            Response(text=response, size_hint_x=.75, halign=halign))

    def move_text_box(self):
        text_box = screen_manager.get_screen("ChatGUI").ids.text_bar_layout

        if self.status:
            text_box.pos_hint = {"center_y": 0.05}
            self.status = False
        else:
            text_box.pos_hint = {"center_y": 0.7}
            self.status = True

        screen_manager.do_layout()


if __name__ == '__main__':
    LabelBase.register(name='Poppins', fn_regular="GUI/Assets/Poppins-Regular.otf")  # font for chat bubbles
    ChatBot().run()
