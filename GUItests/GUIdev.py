import queue
from multiprocessing import connection

import mysql
import mysql.connector
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

from Facerecog import facerecog_popup
from kivy.uix.popup import Popup
import Facerecog.datacollect as DataCollector
from kivy.uix.image import Image

'''DEVELOPMENT CODE FOR GUI'''
'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED PACKAGE'''

Window.size = (1920, 1080)
Window.fullscreen = True


def close_connection():
    pass


class YourPopupContent(Image):  # Change the base class if needed
    pass


class MainWindow(MDApp):

    def open_popup(self):
        global popup
        content = YourPopupContent()
        popup = Popup(title="", content=Builder.load_file("New User KVs/facerecog_popup.kv"), size_hint=(None, None), size=(500, 400), background_color=(1,1,1,.0))
        popup.open()

    def warning_popup(self):
        global popup_warning

        content = YourPopupContent()
        popup_warning = Popup(title="", content=Builder.load_file("warning.kv"), size_hint=(None, None), size=(500, 400), background_color=(1,1,1,.0))
        popup_warning.open()

    def ok_button(self):
        print("ok button pressed")

    def warning_ok_button(self):
        print("ok button pressed")
        popup_warning.dismiss()

    def cancel_button(self):
        print("cancel button pressed")
        self.change_screen('userstatus')
        popup.dismiss()

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()

        try:
            self.connection = mysql.connector.connect(
                host="airhub-soe.apc.edu.ph",
                user="marj",
                password="RAMIcpe211",
                database="ramibot"
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print("Failed to connect to MySQL database: {}".format(err))
            return  # Exit the function if connection fails

        # Close the database connection when the app exits
        def close_connection():
            if self.connection.is_connected():
                self.connection.close()
                print("Connection to MySQL database closed")

        self.bind(on_stop=lambda x: close_connection())

        # ADD ALL SCREENS TO BE USED HERE

        # screen_manager.add_widget(Builder.load_file('idleWindow.kv'))
        # screen_manager.add_widget(Builder.load_file('greetWindow.kv'))
        # screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))
        #screen_manager.add_widget(Builder.load_file('New User KVs/facerecog_popup.kv'))


        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))

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

        screen_manager.add_widget(Builder.load_file('Faculty Scheds KVs/faculty.kv'))
        screen_manager.add_widget(Builder.load_file('Faculty Scheds KVs/facultyInfo.kv'))

        screen_manager.add_widget(Builder.load_file('Floors KVs/floormaps.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor.kv'))

        screen_manager.add_widget(Builder.load_file('Programs KVs/programsoffered.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/programs.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gradSchool.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gsInfo.kv'))

        return screen_manager


    def change_screen(self, screen_name):
        screen_manager.current = screen_name

    def update_label(self, screen_name, id, text):
        '''Update labels in mapscreen'''
        screen_name = self.root.get_screen(screen_name)
        try:
            label = screen_name.ids[id]
            label.text = text
        except:
            print("Label not found")
            pass

  #app.update_label("main",)
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

    def navigateToPreviousScreen(self):
        screen_manager.current = screen_manager.previous()

    def add_apc_user_to_db(self):
        global user_ID
        MainWindow.add_user_flag = 1
        try:
            user_ID = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            role = self.get_text('adduser', 'role')

            if not all([given_name, last_name, nickname, role]):  # Check if any of the variables are empty
                raise ValueError("Empty fields detected")

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)

        except ValueError as ve:
            print(f"Error: {ve}")

        except Exception as e:
            print(f"Error in uploading to db: {e}")

    def add_visitor_user_to_db(self):
        global user_ID
        MainWindow.add_user_flag = 2
        try:
            user_ID = DataCollector.generate_visitor_id()
            given_name = self.get_text('adduser2', 'given_name')
            middle_initial = self.get_text('adduser2', 'middle_initial')
            last_name = self.get_text('adduser2', 'last_name')
            nickname = self.get_text('adduser2', 'nickname')
            role = self.get_text('adduser2', 'role')

            if not all([given_name, last_name, nickname, role]):  # Check if any of the variables are empty
                raise ValueError("Empty fields detected")

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)

        except ValueError as ve:
            print(f"Error: {ve}")

        except Exception as e:
            print(f"Error in uploading to db: {e}")


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
