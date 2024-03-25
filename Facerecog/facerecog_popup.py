from kivy.uix.boxlayout import BoxLayout
from Integrated import GUIdev


class PopupContent(BoxLayout):
    def ok_button(self):
        print("ok button pressed")
        GUIdev.start = True

    def cancel_button(self):
        print("cancel button pressed")
        GUIdev.start = False


# class face_capture_popup(BoxLayout):
#     def open_popup(self):
#         content = PopupContent()
#         popup = Popup(title='face capture', content=content, size_hint=(None, None), size=(500, 400))
#         popup.open()
#
# class TestApp(App):
#     def build(self):
#         return face_capture_popup()
#
#
# if __name__ == '__main__':
#     TestApp().run()