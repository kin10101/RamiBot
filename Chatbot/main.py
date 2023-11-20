from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from Chatbot.chatbot import handle_request
from kivy.config import Config
from kivy.uix.textinput import TextInput
# Import and reference ChatBotGUI classes
from chatbotGUI import ChatScreen, Command, Response

Window.size = (1920, 1080)
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"
Config.set('kivy','keyboard_mode','multi_touch')


class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super(CustomTextInput, self).__init__(**kwargs)
        #self.bind(focus=self.on_focus)

    def on_focus(self, *args):
        self.setup_keyboard()
        print("focus")

    def setup_keyboard(self):
        kb = Window.request_keyboard(self._keyboard_close, self)
        if kb.widget:
            kb.widget.layout = 'qwerty.json'
            kb.widget.height = 200
            kb.widget.width = 800
            kb.font_size = 20
            kb.widget.background_color = (1, 1, 1, 1)

    def _keyboard_close(self):
        print("keyboard close")
        #self.focus = False
        pass
class MainWindow(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        # ADD ALL SCREENS HERE
        screen_manager.add_widget(Builder.load_file('my.kv'))
        screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))
        #screen_manager.add_widget(Builder.load_file('mypo.kv'))
        screen_manager.add_widget(Builder.load_file('voice.kv'))
        screen_manager.add_widget(ChatScreen())

        return screen_manager

    def change_screen(self, screen_name):
        screen_manager.current = screen_name

    def send_message(self):
        global size, halign, value
        # Get the text from the text input
        self.input_text = screen_manager.get_screen("ChatGUI").text_input.text.strip()

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
            screen_manager.get_screen("ChatGUI").chat_list.add_widget(
                Command(text=value, size_hint_x=size, halign=halign))
        # Clear the text input
        screen_manager.get_screen("ChatGUI").text_input.text = ""
        self.get_text_input()
        self.response()

    def get_text_input(self):
        print("Input text:", self.input_text)

    def response(self, *args):
        response = ""
        context = [""]
        response = handle_request(self.input_text.lower(), context)
        screen_manager.get_screen("ChatGUI").chat_list.add_widget(
            Response(text=response, size_hint_x=.75, halign=halign))


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="GUI/Assets/Poppins-Regular.otf")
    MainWindow().run()