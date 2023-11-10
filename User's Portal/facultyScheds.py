from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

class MainWindow(Screen):
    pass

class SHSWindow(Screen):
    pass

class CollegeWindow(Screen):
    pass

class GradWindow(Screen):
    pass

class OfficesWindow(Screen):
    pass

class SoEFacultyWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kvfs = Builder.load_file("myfs.kv")
Window.size = (1920, 1080)
Window.fullscreen = True
class Main(MDApp):
    def build (self):
        Window.fullscreen = True
        return kvfs

Main().run()