import subprocess
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainWindow(App):
    def build(self):
        Window.size = (1920, 1080)
        Window.fullscreen = True
        self.window = GridLayout()
        self.window.cols = 1
        self.background_color = '#213b9a'
        self.window.size_hint = (0.8, 0.65)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.55}

        # add widgets to window
        background = Image(source='bg.png', allow_stretch=True, keep_ratio=False)
        Window.add_widget(background)

        # label widget
        self.label = Label(
            text="Hello, I'm RamiBot!",
            font_size=75,
            bold=True,
            color='#FFFFFF'
        )
        self.window.add_widget(self.label)  #to call

        self.po = Button(
            text="Programs Offered",
            size_hint=(1.2, 0.5),
            font_size=30,
            background_color=(6/255.0, 38/255.0, 201/255.0, 0.5),
            background_normal = ""  #to copy exact color
        )
        self.window.add_widget(self.po)

        self.fs = Button(
            text="Faculty Scheduless",
            size_hint=(1.2, 0.5),
            font_size=30,
            background_color=(6/255.0, 38/255.0, 201/255.0, 0.5),
            background_normal = ""
        )
        self.window.add_widget(self.fs)

        self.offices = Button(
            text="Offices and Floor Maps",
            size_hint=(1.2, 0.5),
            font_size=30,
            background_color=(6/255.0, 38/255.0, 201/255.0, 0.5),
            background_normal = ""
        )
        self.window.add_widget(self.offices)

        self.announce = Button(
            text="Announcements",
            size_hint=(1.2, 0.5),
            font_size=30,
            background_color=(6/255.0, 38/255.0, 201/255.0, 0.5),
            background_normal = ""
        )
        self.window.add_widget(self.announce)

        self.po.bind(on_press=self.programs) #to call button
        self.offices.bind(on_press=self.office)
        self.fs.bind(on_press=self.faculty)
        return self.window

    def programs(self, instance):
        subprocess.call(['python','programMain.py'])

    def office(self, instance):
        subprocess.call(['python','officeInfo.py'])

    def faculty(self, instance):
        subprocess.call(['python', 'facultyScheds.py'])

if __name__ == "__main__":
    MainWindow().run()  # run program

