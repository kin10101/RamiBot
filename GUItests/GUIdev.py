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



'''DEVELOPMENT CODE FOR GUI'''
'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED PACKAGE'''

Window.size = (1920, 1080)
Window.fullscreen = True

def close_connection():
    pass


class MainWindow(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()

#        self.bind(on_stop=lambda x: close_connection())

        # ADD ALL SCREENS TO BE USED HERE
        #screen_manager.add_widget(Builder.load_file('chatscreen.kv'))
        screen_manager.add_widget(Builder.load_file('idleWindow.kv'))
        screen_manager.add_widget(Builder.load_file('greetWindow.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))

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
           # label = MainWindow.getFromDB()
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

    connection = None  # Placeholder for the database connection
    pics_cursor = None  # Placeholder for the cursor

    @staticmethod
    def connect_to_db():
        try:
            MainWindow.connection = mysql.connector.connect(
                host="airhub-soe.apc.edu.ph",
                user="marj",
                password="RAMIcpe211",
                database="ramibot"
            )
            if MainWindow.connection.is_connected():
                print("Connected to MySQL database")
                MainWindow.pics_cursor = MainWindow.connection.cursor()
        except mysql.connector.Error as err:
            print("Failed to connect to MySQL database: {}".format(err))

    @staticmethod
    def close_connection():
        if MainWindow.connection and MainWindow.connection.is_connected():
            MainWindow.connection.close()
            print("Connection to MySQL database closed")

    @staticmethod
    def getFromDB(imgID, imgURL):
        try:
            # Check if the image with the given imgID already exists in the database
           # user_query = f"SELECT img_id FROM programs_img WHERE img_id = {12}"
            programs_offered = f"SELECT img_url FROM programs_img WHERE img_id = {imgID}"
            MainWindow.pics_cursor.execute(programs_offered)
            image_found = MainWindow.pics_cursor.fetchone()

            if image_found:
                print("Image already exists in the database")
                print(image_found[0])

            else:
                # Image does not exist, you can handle this case as needed
                print("Image does not exist in the database")
        except Exception as e:
            print("Error:", e)

# Connect to the database
MainWindow.connect_to_db()

# Usage example: Call the getFromDB method with your desired imgID and imgURL
MainWindow.getFromDB(imgID='', imgURL=" ")

# Close the database connection when the app exits
MainWindow.close_connection()

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
