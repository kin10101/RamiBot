import os

from kaki.app import App
from kivy.factory import Factory


class Live(App):
    CLASSES = {
        "UI": "main"
    }

    AUTORELOADER_PATHS = [(os.getcwd(), {"recursive": True})]

    def build_app(self, first = False):
        return Factory.UI()

Live().run()