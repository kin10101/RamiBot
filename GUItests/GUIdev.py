from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

'''DEVELOPMENT CODE FOR GUI'''
'''TEST HERE GUI CODE TO BE IMPLEMENTED IN INTEGRATED PACKAGE'''

Window.size = (1920, 1080)
Window.fullscreen = True

class MainWindow(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()

        # ADD ALL SCREENS TO BE USED HERE
        #screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
        screen_manager.add_widget(Builder.load_file('mainscreen.kv'))
        screen_manager.add_widget(Builder.load_file('officehours.kv'))
        screen_manager.add_widget(Builder.load_file('floormaps.kv'))
        screen_manager.add_widget(Builder.load_file('programsoffered.kv'))
        screen_manager.add_widget(Builder.load_file('announcements.kv'))
        screen_manager.add_widget(Builder.load_file('faculty.kv'))
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

    def navigateToPreviousScreen(self):
        screen_manager.current = screen_manager.previous()



if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
