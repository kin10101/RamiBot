from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window


class MainWindow(Screen):
    pass

class SHSWindow(Screen):
    pass

class SoEWindow(Screen):
    pass
class CpEWindow(Screen):
    pass
class ECEWindow(Screen):
    pass
class CEWindow(Screen):
    pass

class SoCITWindow(Screen):
    pass
class ComsciWindow(Screen):
    pass
class ITWindow(Screen):
    pass
class CTWindow(Screen):
    pass

class SoMAWindow(Screen):
    pass
class MMAWindow(Screen):
    pass
class PsychWindow(Screen):
    pass

class SoMWindow(Screen):
    pass
class AccWindow(Screen):
    pass
class BSMAWindow(Screen):
    pass
class TMWindow(Screen):
    pass
class BSBAWindow(Screen):
    pass
class BMWindow(Screen):
    pass
class MAWindow(Screen):
    pass
class DBWindow(Screen):
    pass

class SoAWindow(Screen):
    pass

class GSWindow(Screen):
    pass
class MengCpeWindow(Screen):
    pass
class MSCSWindow(Screen):
    pass
class MGDWindow(Screen):
    pass
class MISWindow(Screen):
    pass
class MITWindow(Screen):
    pass
class MMWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

Window.size = (1920,1080)
kv = Builder.load_file("my.pokv")

class Main(MDApp):
    def build (self):
        Window.fullscreen = True

        return kv

Main().run()