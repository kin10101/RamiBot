from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
class MainWindow(MDApp):
    def build(self):
        Window.size = (1920, 1080)
        return Builder.load_file('my.kv')

if __name__ == "__main__":
    MainWindow().run()


