from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder

# Load the .kv file
Builder.load_file('test.kv')

class TestKivyApp(App):
    def build(self):
        return Label(text="Hello, Kivy on Raspberry Pi!")

if __name__ == '__main__':
    TestKivyApp().run()
