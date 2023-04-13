import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class Main(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.background_color = '#213b9a'
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.6}

        #add widgets to window
        #label widget
        self.greeting = Label(
                    text="Faculty Schedules",
                    font_size = 70,
                    color = '#FFFFFF')
        self.window.add_widget(self.greeting) #to call

        #text widget
        '''self.user = TextInput(
                    multiline=False, #multiline false - one input only
        padding_y = (20,20),
        size_hint = (1, 0.5) #percentage
        )
        self.window.add_widget(self.user)'''

        #button widget
        self.button1 = Button(
                text="Senior High School",
                size_hint = (1.2, 0.5),
                bold = True,
                background_color = '#213b9a'
                #background_normal = "" - to copy exact color
                )
        self.button2 = Button(
                text="College Department",
                size_hint = (1.2, 0.5),
                bold = True,
                background_color = '#213b9a'
                )
        self.button3 = Button(
            text="Graduate School",
            size_hint = (1.2, 0.5),
            bold = True,
            background_color = '#213b9a'
            )
        self.button4 = Button(
            text="Offices",
            size_hint = (1.2, 0.5),
            bold = True,
            background_color = '#213b9a'
            )

        # call button function
        self.button1.bind(on_press=self.callback1)
        self.button2.bind(on_press=self.callback2)
        self.button3.bind(on_press=self.callback3)
        self.button4.bind(on_press=self.callback4)

        self.window.add_widget(self.button1)
        self.window.add_widget(self.button2)
        self.window.add_widget(self.button3)
        self.window.add_widget(self.button4)

        return self.window

    def callback1(self, instance): #function for button
        self.greeting.text = "SHS Department"
    def callback2(self, instance): #function for button
        self.greeting.text = "College Department"
    def callback3(self, instance):  # function for button
        self.greeting.text = "Graduate School"
    def callback4(self, instance):  # function for button
        self.greeting.text = "Offices"
        #self.greeting.text = "Hello " + self.user.text + "!"

if __name__ == "__main__":
    Main().run() #run class

