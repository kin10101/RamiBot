import cv2
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
import Facerecog.datacollect as DataCollector
import os
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

Window.size = (1920, 1080)
Window.fullscreen = True
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")



class MainApp(MDApp):
    face_count = 0
    add_user_flag = 0
    global user_ID
    global start

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texture = None
        self.camera = None
        self.frame_count = None
        self.frame_rate = None
        self.num_images_to_capture = 50
        self.current_image_count = 0
        self.detect = None
        self.image = None

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

        self.frame_rate = 10
        self.frame_count = 50
        self.texture = Texture.create(size=(640, 480), colorfmt='bgr')

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
        global user_ID
        MainApp.add_user_flag = 1
        try:
            user_ID = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            profession = self.get_text('adduser', 'profession')

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, profession)

        except Exception as e:
            print(f"Error in uploading to db: {e}")

    def add_visitor_user_to_db(self):
        global user_ID
        MainApp.add_user_flag = 2
        try:
            user_ID = DataCollector.generate_visitor_id()
            given_name = self.get_text('adduser2', 'given_name')
            middle_initial = self.get_text('adduser2', 'middle_initial')
            last_name = self.get_text('adduser2', 'last_name')
            nickname = self.get_text('adduser2', 'nickname')
            profession = self.get_text('adduser2', 'profession')

            DataCollector.add_to_db(user_ID, nickname, last_name, given_name, middle_initial, profession)
        except Exception as e:
            print(f"Error in uploading to db: {e}")

    def captures(self):
        global start

        user_dir = DataCollector.user_dir
        user_id = DataCollector.user_id

        count = 0

        self.image = Image(texture=self.texture)
        screen_manager.ids.camera = self.texture

        self.camera = cv2.VideoCapture(1)

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
            faces = detect.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                # Increment the count for each detected face
                count += 1

                face_image = gray[y:y + h, x:x + w]
                image_path = os.path.join(user_dir, f"User.{user_id}.{count}.jpg")
                cv2.imwrite(image_path, face_image)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

                if count >= 50:
                    # Release the video capture and exit the application
                    self.camera.release()
                    cv2.destroyAllWindows()


if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf")
    MainApp().run()

