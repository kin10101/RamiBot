from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window


class MainWindow(Screen):
    pass

class AdmissionsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

Window.size = (1920,1080)
kv2 = Builder.load_file("my.ohkv")

class Main(MDApp):
    def build (self):
        Window.fullscreen = True

        return kv2

Main().run()