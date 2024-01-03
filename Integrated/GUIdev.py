from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
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

        screen_manager.add_widget(Builder.load_file('announcements.kv'))
        screen_manager.add_widget(Builder.load_file('faculty.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floormaps.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor1.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor2.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor3.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor4.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor5.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor6.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor7.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor8.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor9.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor10.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor11.kv'))
        screen_manager.add_widget(Builder.load_file('Floors KVs/floor12.kv'))

        screen_manager.add_widget(Builder.load_file('Programs KVs/programsoffered.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/soe.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/som.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/soma.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/socit.kv'))
        screen_manager.add_widget(Builder.load_file('Programs KVs/gradschool.kv'))

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
        '''adds APCuser to db and is called when information is submitted'''
        try:
            school_id = self.get_text('adduser', 'school_id')
            given_name = self.get_text('adduser', 'given_name')
            middle_initial = self.get_text('adduser', 'middle_initial')
            last_name = self.get_text('adduser', 'last_name')
            nickname = self.get_text('adduser', 'nickname')
            profession = self.get_text('adduser', 'profession')

            m.insertToDB(school_id, nickname, last_name, given_name, middle_initial, profession)
            user_dir = os.path.join("datasets", school_id)

            # Check if the user directory already exists
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
        except:
            print("error in uploading to db")
            pass

    def add_VisitorUser_to_db(self):
        '''adds Visitor to db and is called when information is submitted'''
        try:
            visitor_id = '00000000000'
            print(visitor_id)
            given_name = self.get_text('adduser2', 'given_name')
            middle_initial = self.get_text('adduser2', 'middle_initial')
            last_name = self.get_text('adduser2', 'last_name')
            nickname = self.get_text('adduser2', 'nickname')
            profession = self.get_text('adduser2', 'profession')

            m.insertToDB(visitor_id, nickname, last_name, given_name, middle_initial, profession)
            user_dir = os.path.join("datasets", visitor_id)

            # Check if the user directory already exists
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
        except:
            print("error in uploading to db")
            pass

    def videocam(self):
        layout = BoxLayout(orientation = 'vertical')
        camera = Camera(play = True, index = 0)
        layout.add_widget(camera)
        return layout

    def navigateToPreviousScreen(self):
        screen_manager.current = screen_manager.previous()

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
