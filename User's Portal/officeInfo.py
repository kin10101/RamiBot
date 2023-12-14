from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window


class OfficesMain(Screen):
    pass
class SchedulesWindow(Screen):
    pass
class Admissions(Screen):
    pass
class Registrar(Screen):
    pass
class Finance(Screen):
    pass
class ITRO(Screen):
    pass
class BMO(Screen):
    pass
class Logistics(Screen):
    pass
class DO(Screen):
    passx
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