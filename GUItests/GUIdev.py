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
        #screen_manager.add_widget(Builder.load_file('ChatbotGUI.kv'))1
        screen_manager.add_widget(Builder.load_file('New User KVs/newuser.kv'))
        screen_manager.add_widget(Builder.load_file('New User KVs/adduser.kv'))
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

    def update_labels(self):
        '''Update labels in mapscreen'''
        mapscreen = self.root.get_screen('mapscreen')
        main_layout = mapscreen.ids.main_layout
        info_layout = mapscreen.ids.info_layout  # Correct way to access info_layout

        title_label = mapscreen.ids.title
        descr_label = mapscreen.ids.descr
        floor_label = mapscreen.ids.floor
        sched_label = mapscreen.ids.sched
        image = mapscreen.ids.bg_img

        image.source = "Assets/bg.png"
        descr_label.text = "dummy text"
        floor_label.text = "dummy text"
        sched_label.text = "dummy text"
        title_label.text = "dummy text"

if __name__ == "__main__":
    LabelBase.register(name='Poppins', fn_regular="Assets/Poppins-Regular.otf") # register fonts for use in app
    MainWindow().run()
