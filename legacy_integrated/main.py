# Kivy and KivyMD imports
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.config import Config

# Chatbot imports
from Chatbot.chatbot import handle_request
from Chatbot.chatbotGUI import ChatScreen, Command, Response


# Voicebot imports
from Voicebot.voice_assistant_module import VoiceAssistant as va
va = va()


# Global variables
Window.size = (1920, 1080)
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Config.set('graphics', 'borderless', 0)  # 0 being off 1 being on as in true/false
Config.set('kivy','keyboard_mode','dock')

class MainWindow(MDApp):
    """Main application window."""

    def build(self):
        """Build the application."""
        global screen_manager
        screen_manager = ScreenManager()
        self.add_screens()
        return screen_manager

    def add_screens(self):
        """Add all screens to the screen manager."""
        screen_manager.add_widget(Builder.load_file('my.kv'))  # main screen
        screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))  # chatbot screen
        screen_manager.add_widget(Builder.load_file('voice.kv'))  # voice screen
        screen_manager.add_widget(ChatScreen())

    def change_screen(self, screen_name):
        """Change the current screen."""
        screen_manager.current = screen_name

    def send_message(self):
        """Send a message."""
        self.input_text = screen_manager.get_screen("ChatGUI").text_input.text.strip()
        if self.input_text:
            self.add_message_to_chat()
        screen_manager.get_screen("ChatGUI").text_input.text = ""
        self.get_text_input()
        self.response()

    def add_message_to_chat(self):
        """Add the message to the chat list."""
        global size, halign, value
        value = self.input_text
        self.set_message_size_and_alignment()
        screen_manager.get_screen("ChatGUI").chat_list.add_widget(
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
        screen_manager.get_screen("ChatGUI").chat_list.add_widget(
            Response(text=response, size_hint_x=.75, halign=halign))

    def voice(self):
        """Start listening for voice commands."""
        va.activate_on_button_press()

def main():
    """Main function to run the application."""
    LabelBase.register(name='Poppins', fn_regular="GUI/Assets/Poppins-Regular.otf")
    MainWindow().run()


# Run the application
if __name__ == "__main__":
    main()