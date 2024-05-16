from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen

import sql_module

'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED'''

Window.size = (1920, 1080)
Window.fullscreen = True
global screen_manager


class MainWindow(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.Main_Menu = ["Office_Schedule", "Faculty_Schedule", "Programs_Offered", "School_Information", "Floor_Maps"]
        # self.Office_Schedule = ["Admissions_Office", "Accounting", "Registrar"]
        # self.Office_Schedule_URL = ["logo.png", "main_bg.png", "face_scan_complete.png"]
        # self.Faculty_Schedule = ["two1", "two2", "two3"]
        # self.Programs_Offered = ["three1", "three2", "three3"]
        # self.School_Information = ["four1", "four2", "four3"]
        # self.Floor_Maps = ["five1", "five2", "five3"]

        self.Main_Menu = sql_module.get_column_data("button_list", "main_menu")
        self.Office_Schedule = sql_module.get_column_data("button_list", "office_schedule")
        self.Faculty_Schedule = sql_module.get_column_data("button_list", "faculty_schedule")
        self.Programs_Offered = sql_module.get_column_data("button_list", "programs_offered")
        self.Other_Information = sql_module.get_column_data("button_list", "other_information")
        self.Tuition_Fees = sql_module.get_column_data("button_list", "tuition_fees")
        self.School_Calendar = sql_module.get_column_data("button_list", "school_calendar")
        self.School_Organizations = sql_module.get_column_data("button_list", "school_organizations")
        self.School_Information = sql_module.get_column_data("button_list", "school_information")
        self.Floor_Map_and_Directory = sql_module.get_column_data("button_list", "floor_map_and_directory")

        self.previous_screen = None

    def build(self):
        global screen_manager
        screen_manager = ScreenManager(transition=NoTransition())
        # ADD ALL SCREENS HERE

        # Load the KV file after adding the screens
        screen_manager.add_widget(Builder.load_file('main.kv'))

        screen_manager.add_widget(Builder.load_file('office_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('faculty_schedule.kv'))
        screen_manager.add_widget(Builder.load_file('programs_offered.kv'))
        screen_manager.add_widget(Builder.load_file('other_information.kv'))
        screen_manager.add_widget(Builder.load_file('tuition_fees.kv'))
        screen_manager.add_widget(Builder.load_file('school_calendar.kv'))
        screen_manager.add_widget(Builder.load_file('school_organizations.kv'))
        screen_manager.add_widget(Builder.load_file('school_information.kv'))
        screen_manager.add_widget(Builder.load_file('floor_maps.kv'))

        screen_manager.add_widget(Builder.load_file('image_info.kv'))

        return screen_manager

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
        path = ""  # get path from database
        screen_manager.get_screen(screen_manager.current).ids.img.source = path + button_text + ".png"

    def clear_buttons(self):
        # Get a reference to the button layout
        button_layout = screen_manager.get_screen(screen_manager.current).ids.button_layout

        # Remove all children (buttons) from the button layout
        if button_layout.children:
            button_layout.clear_widgets()


if __name__ == "__main__":
    # create the list of buttons in the main menu, then map the functions in the on_press_list to the buttons that takes in the argument of the list to be created as new button list

    LabelBase.register(name='Poppins', fn_regular="Poppins-Regular.otf")
    MainWindow().run()

    sql_module.connect()
    column_data = sql_module.get_column_data("text_to_voice_announcements", "announcement_name")
    count_data = len(column_data)
    print(column_data)
    print(count_data)
