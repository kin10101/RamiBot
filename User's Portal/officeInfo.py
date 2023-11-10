from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window


class MainWindow(Screen):
    pass
class SchedulesWindow(Screen):
    pass
class AdmissionsWindow(Screen):
    pass
class FloorMapsWindow(Screen):
    pass
class FirstFloor(Screen):
    pass
class SecondFloor(Screen):
    pass
class ThirdFloor(Screen):
    pass
class FourthFloor(Screen):
    pass
class FifthFloor(Screen):
    pass
class SixthFloor(Screen):
    pass
class SeventhFloor(Screen):
    pass
class EighthFloor(Screen):
    pass
class NinthFloor(Screen):
    pass
class TenthFloor(Screen):
    pass
class EleventhFloor(Screen):
    pass
class TwelveFloor(Screen):
    pass
class WindowManager(ScreenManager):
    pass

Window.size = (1920,1080)
kv2 = Builder.load_file("myoh.kv")

class Main(MDApp):
    def build (self):
        Window.fullscreen = True

        return kv2

Main().run()