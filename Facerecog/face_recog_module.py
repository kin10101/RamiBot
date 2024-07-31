import os
import random
import numpy as np
import time
from deepface import DeepFace
import cv2

person_detected = False
running = False

def realtime_face_recognition(video):
    print("face recognition thread running")
    global person_detected
    global running
    running = True

    if not video.isOpened():
        print("Error: Camera is not initialized properly. Exiting...")
        return

    while running:
        try:
            ret, frame = video.read()
            if not ret:
                print("Can't receive frame. Exiting...")
                break

            height, width, _ = frame.shape

            # Define the center rectangle's boundaries
            rect_width = width // 2
            rect_height = height // 1
            left = (width - rect_width) // 2
            top = (height - rect_height) // 2
            right = left + rect_width
            bottom = top + rect_height

            # Draw the rectangle on the frame
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            detections = DeepFace.extract_faces(img_path=frame, detector_backend='yunet')
            for face in detections:
                facial_area = face['facial_area']
                x = facial_area['x']
                y = facial_area['y']
                w = facial_area['w']
                h = facial_area['h']

                # Check if the face is within the center rectangle
                if left <= x + w // 2 <= right and top <= y + h // 2 <= bottom:
                    person_detected = True
                    print("Face detected")
                    greeting = greet_new_user()
                    return greeting

        except Exception as e:
            person_detected = False
            #print("No face detected")



        # display
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 800, 600)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #
    # video.release()
    # cv2.destroyAllWindows()





def greet_new_user():
    greetings = [
        "hi, I'm Rami bot, nice to meet you",
        "hello! i am rami with the bot, Rami bot",
        "almost didn't see you there, hi! i'm Rami bot",
        "hello there, i'm Rami bot, how can i help you today?",
        "Hey! I'm Rami bot, nice to meet you",
        "psst, hey! look at me!",
        "Rami bot here, how can i help you today?",
        "i saw you with my eyes, hello! i'm Rami bot"
    ]

    # folder_path = "../Integrated/audio/jp_greeting"
    # greetings = []
    # for filename in os.listdir(folder_path):
    #     if filename.endswith(".mp3"):
    #         greetings.append(os.path.join(folder_path, filename))

    return random.choice(greetings)


def get_camera_list(max_cameras=10):
    """Get a list of available camera devices and their index."""
    cameras = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cameras.append(index)
        cap.release()
    return cameras


if __name__ == '__main__':
    available_cameras = get_camera_list()
    print(f"Available cameras: {available_cameras}")

    if available_cameras:
        video_capture = cv2.VideoCapture(available_cameras[0])
    else:
        print("No cameras found")