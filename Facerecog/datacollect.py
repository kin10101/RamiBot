from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import os
import main as m

background = KivyImage(source='facerecogbg.png', allow_stretch=True, keep_ratio=False)
Window.add_widget(background)

class MainWindow(App):
    # Initialize count as a class variable
    count = 0
    def build(self):
        Window.size = (1920, 1080)
        Window.fullscreen = True

        self.window = GridLayout()
        self.window.cols = 1
        self.background_color = '#213b9a'
        self.window.size_hint = (0.8, 0.65)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.55}

        capture_width, capture_height = 640, 480

        # Create an Image widget to display the video feed
        self.video_image = KivyImage(allow_stretch=True, keep_ratio=False)
        self.window.add_widget(self.video_image)

        # Start the OpenCV video capture with the specified size
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.window

    def update(self, user_dir):
        # Read a frame from the camera
        ret, frame = self.capture.read()

        # Customize the video capture size (width, height)
        capture_width, capture_height = 640, 480
        frame = cv2.resize(frame, (capture_width, capture_height))

        # Convert the OpenCV frame to a Kivy texture
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        # Update the texture of the video Image widget
        self.video_image.texture = texture

        # Perform face detection and data collection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Increment the count for each detected face
            MainWindow.count += 1

            face_image = gray[y:y + h, x:x + w]
            image_path = os.path.join(user_dir, f"User.{id}.{MainWindow.count}.jpg")
            cv2.imwrite(image_path, face_image)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y), (50, 50, 255), 1)

            '''if MainWindow.count >= 50:
                # Release the video capture and exit the application
                self.capture.release()
                App.get_running_app().stop()'''

if __name__ == "__main__":
    # Load a Haar Cascade Classifier for face detection
    detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    MainWindow().run()




