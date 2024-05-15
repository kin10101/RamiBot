import queue
from multiprocessing import connection

import mysql
import mysql.connector
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

#FACE RECOGNITION------
import cv2
import os
import Facerecog.datacollect as DataCollector
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from Facerecog import trainedModel
from Facerecog import main

from kivy.graphics.texture import Texture

#from sql import sql_query

detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

global start
#FACE RECOGNITION------



'''DEVELOPMENT CODE FOR GUI'''
'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED PACKAGE'''

Window.size = (1920, 1080)
Window.fullscreen = True

def close_connection():
    pass


class MainWindow(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texture = None

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()

   #     self.bind(on_stop=lambda x: close_connection())

        # ADD ALL SCREENS TO BE USED HERE
        #screen_manager.add_widget(Builder.load_file('chatscreen.kv'))
        screen_manager.add_widget(Builder.load_file('idleWindow.kv'))
        screen_manager.add_widget(Builder.load_file('greetWindow.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/face_capture_done.kv'))

        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))

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
        screen = self.root.get_screen(screen_name)
        try:
            label = screen.ids[id]
            label.source = source
        except Exception as e:
            print("Error updating image source:", e)

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
                host="localhost", #"airhub-soe.apc.edu.ph"
                user="root", #"marj",
                password= "", #RAMIcpe211",
                database="mj_test" #"ramibot"
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

    def fetch_image_url(self, img_id):
        tables = ['calendars_img', 'floor_map', 'tuition_img', 'programs_img', 'offices', 'apcinfo_img', 'org_img']
        for table in tables:
            # Execute the query
            user_query = f"SELECT img_url FROM {table} WHERE img_identifier = %s"
            MainWindow.pics_cursor.execute(user_query, (img_id,))
            image_found = MainWindow.pics_cursor.fetchone()
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
        tables = ['faculty_scheds']
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

'''
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
        #MainApp.add_user_flag = 1
        try:
            user_ID = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            role = self.get_text('adduser', 'role')

            if not all([user_ID, given_name, last_name, nickname, role]): # Check if any of the variables are empty
                raise ValueError("Empty fields detected")

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, role)
            print("Uploaded to database successfully!")
            self.open_popup()

        except ValueError as ve:
            print(f"Error: {ve}")
            self.warning()
            self.change_screen('adduser')
        except Exception as e:
            print(f"Error in uploading to db: {e}")
            self.warning()
            self.change_screen('adduser')

    def add_visitor_user_to_db(self):
        global user_ID
        MainWindow.add_user_flag = 2
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
'''

window_instance = MainWindow()
# Connect to the database
window_instance.connect_to_db()
#window_instance.fetch_image_url(img_id='')

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
    # Close the database connection when the app exits
    window_instance.close_connection()
