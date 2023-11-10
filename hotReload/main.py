from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp

class UI(Factory.ScreenManager):

    Builder.load_file('layout.kv')

class Main(MDApp):
    def build(self):
        return UI()


if __name__ == '__main__':
    Main().run()

