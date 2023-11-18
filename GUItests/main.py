from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from chatbotGUI import ChatBot

class MainWindow(MDApp):
    Window.size = (1920, 1080)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ChatBot = ChatBot()


    def change_screen(self, screen_name):
        screen_manager.current = screen_name
    def build(self):

        global screen_manager
        screen_manager = ScreenManager()

        screen_manager.add_widget(Builder.load_file('my.kv'))
        screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))
        #screen_manager.add_widget(Builder.load_file('mypo.kv'))

        return screen_manager




if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")  # font for chat bubbles

    MainWindow().run()



