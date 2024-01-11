from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.texture import Texture
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
import Facerecog.main as m  # importing main.py from facerecog
import os
import cv2

Window.size = (1920, 1080)
Window.fullscreen = True

class MainApp(MDApp):
    face_count = 0
    user_directory = ''
    user_id = ''
    school_id = ''
    add_user_flag = 0

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()

        # ADD ALL SCREENS TO BE USED HERE
        screen_manager.add_widget(Builder.load_file('idleWindow.kv'))
        screen_manager.add_widget(Builder.load_file('greetWindow.kv'))

        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/userstatus.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser2.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/datacollect.kv'))

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
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gradSchool.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/GS/gsInfo.kv'))

        return screen_manager

    def navigate_to_previous_screen(self):
        screen_manager.current = screen_manager.previous()

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

    def add_apc_user_to_db(self):
        MainApp.add_user_flag = 1
        try:
            MainApp.school_id = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            profession = self.get_text('adduser', 'profession')

            m.insertToDB(MainApp.school_id, nickname, last_name, given_name, middle_initial, profession)
            MainApp.user_directory = os.path.join("datasets", MainApp.school_id)

            if not os.path.exists(MainApp.user_directory):
                os.makedirs(MainApp.user_directory)
        except:
            print("Error in uploading to db")

    def add_visitor_user_to_db(self):
        MainApp.add_user_flag = 2
        try:
            MainApp.user_id = '00000000000'
            given_name = self.get_text('adduser2', 'given_name')
            middle_initial = self.get_text('adduser2', 'middle_initial')
            last_name = self.get_text('adduser2', 'last_name')
            nickname = self.get_text('adduser2', 'nickname')
            profession = self.get_text('adduser2', 'profession')

            m.insertToDB(MainApp.user_id, nickname, last_name, given_name, middle_initial, profession)
            MainApp.user_directory = os.path.join("datasets", MainApp.user_id)

            if not os.path.exists(MainApp.user_directory):
                os.makedirs(MainApp.user_directory)
        except:
            print("Error in uploading to db")

    def videocam(self):
        layout = GridLayout(orientation='vertical')
        self.video_image = KivyImage(allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.video_image)

        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

        capture_width, capture_height = 640, 480
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)

        Clock.schedule_interval(self.videocam, 1.0 / 30.0)

        ret, frame = self.capture.read()
        capture_width, capture_height = 640, 480
        frame = cv2.resize(frame, (capture_width, capture_height))

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        self.video_image.texture = texture

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            MainApp.face_count += 1
            face_image = gray[y:y + h, x:x + w]

            if MainApp.add_user_flag == 1:
                image_path1 = os.path.join(MainApp.user_directory, f"User.{MainApp.school_id}.{MainApp.face_count}.jpg")
                cv2.imwrite(image_path1, face_image)
                MainApp.add_user_flag = 0
            if MainApp.add_user_flag == 2:
                image_path2 = os.path.join(MainApp.user_directory, f"User.{MainApp.user_id}.{MainApp.face_count}.jpg")
                cv2.imwrite(image_path2, face_image)
                MainApp.add_user_flag = 0

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

            if MainApp.face_count >= 50:
                self.capture.release()


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")
    MainApp().run()