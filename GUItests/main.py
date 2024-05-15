from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
import sql_module


'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED'''

Window.size = (1920, 1080)

on_press_list = [f"fn{i}" for i in range(1, 30)]
class MainWindow(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        # ADD ALL SCREENS HERE
        screen_manager.add_widget(Builder.load_file('my.kv'))

        return screen_manager

    def change_screen(self, screen_name):
        screen_manager.current = screen_name

    def create_button_list(self):
        for button_text in button_list:
            button = MDFillRoundFlatButton(
                text=button_text,
                font_name='Poppins',
                font_size=24,
                halign='center',
                text_color=(1, 1, 1, 1),
                md_bg_color=(0.003, 0.4, 0.6, 1),
                size_hint=(0.7, None),
                pos_hint={'center_x': 0.5},
                padding=(30, 30)
            )
            # Get the corresponding item from the second list based on the index
            index = button_list.index(button_text)
            corresponding_item = other_list[index]

            # Bind the button_callback method with both button_text and corresponding_item arguments
            button.bind(
                on_release=lambda btn, text=button_text, item=corresponding_item: self.button_callback(text, item))
            screen_manager.get_screen('mainmenu').ids.button_layout.add_widget(button)

    def button_callback(self, button_text, corresponding_item):
        print("Button pressed:", button_text)
        print("Corresponding item:", corresponding_item)
        func = getattr(self, corresponding_item)
        func()


    def fn1(self):
        self.clear_buttons()
        print("fn1")
        self.new_list(on_press_list) # change to column name



    def new_list(self, on_press_list):
        for button_text in on_press_list:
            button = MDFillRoundFlatButton(
                text=button_text,
                font_name='Poppins',
                font_size=24,
                halign='center',
                text_color=(1, 1, 1, 1),
                md_bg_color=(0.003, 0.4, 0.6, 1),
                size_hint=(0.7, None),
                pos_hint={'center_x': 0.5},
                padding=(30, 30)
            )
            screen_manager.get_screen('mainmenu').ids.button_layout.add_widget(button)

    def clear_buttons(self):
        # Get a reference to the button layout
        button_layout = screen_manager.get_screen('mainmenu').ids.button_layout

        # Remove all children (buttons) from the button layout
        button_layout.clear_widgets()


if __name__ == "__main__":
    other_list = [f"fn{i}" for i in range(1, 30)]

    sql_module.connect()
    column_data = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
    count_data = len(column_data)
    print(column_data)
    print(count_data)

    button_list = column_data
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")
    MainWindow().run()