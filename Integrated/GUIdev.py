from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.camera import Camera
from kivy.clock import Clock
import Facerecog.main as m #importing main.py from facerecog
import os
import cv2

'''DEVELOPMENT CODE FOR GUI'''
'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED PACKAGE'''

Window.size = (1920, 1080)
Window.fullscreen = True
user_dir = ''
class MainWindow(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()

        # ADD ALL SCREENS TO BE USED HERE
        #screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))
        screen_manager.add_widget(Builder.load_file('idleWindow.kv'))
        screen_manager.add_widget(Builder.load_file('greetWindow.kv'))

        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))

        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))

        screen_manager.add_widget(Builder.load_file('Office KVs/officehours.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/admissions.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/finance.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/registrar.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/itro.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/bmo.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/logitics.kv'))
        screen_manager.add_widget(Builder.load_file('Office KVs/do.kv'))

        screen_manager.add_widget(Builder.load_file('Announcements KVs/announcements.kv'))
        screen_manager.add_widget(Builder.load_file('faculty.kv'))

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

    def add_APCuser_to_db(self):
        '''Add user to database. read text from newuser screen edittexts components, and call
        add_user_to_db() from facerecog.main'''
        try:
            school_id = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            profession = self.get_text('adduser', 'profession')

            m.insertToDB(school_id, nickname, last_name, given_name, middle_initial, profession)
        except:
            print("error in uploading to db")
            pass

    def videocam(self):
        layout = GridLayout(orientation = 'vertical')
        camera = Camera(play = True, index = 0)
        layout.add_widget(camera)

        detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

        capture_width, capture_height = 640, 480
        # Start the OpenCV video capture with the specified size
        self.capture = camera
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)

        Clock.schedule_interval(self.videocam(), 1.0 / 30.0)

        # Customize the video capture size (width, height)
        capture_width, capture_height = 640, 480
        frame = cv2.resize(camera, (capture_width, capture_height))

        # Perform face detection and data collection
        gray = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
        faces = detect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Increment the count for each detected face
            MainWindow.count += 1

            face_image = gray[y:y + h, x:x + w]
            image_path = os.path.join(user_dir, f"User.{id}.{MainWindow.count}.jpg")
            cv2.imwrite(image_path, face_image)

            cv2.rectangle(camera, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(camera, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)
            #
            if MainWindow.count >= 50:
                # Release the video capture and exit the application
                self.capture.release()
        return layout
    def navigateToPreviousScreen(self):
        screen_manager.current = screen_manager.previous()

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
