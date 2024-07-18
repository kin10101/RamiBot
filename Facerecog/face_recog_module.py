import os
import random
import numpy as np
import time
from deepface import DeepFace
import cv2

person_detected = False
running = False


def realtime_face_recognition(video):
    print("face recog thread running")
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

            # Get the dimensions of the frame
            height, width, _ = frame.shape

            # Calculate the center point of the frame
            center_x = width // 2
            center_y = height // 2

            detections = DeepFace.extract_faces(img_path=frame, detector_backend='yunet')
            for face in detections:
                facial_area = face['facial_area']
                x = facial_area['x']
                y = facial_area['y']
                w = facial_area['w']
                h = facial_area['h']

                # Calculate the center point of the face
                face_center_x = x + w // 2
                face_center_y = y + h // 2

                # Calculate the Euclidean distance between the center of the face and the center of the frame
                distance = np.sqrt((face_center_x - center_x) ** 2 + (face_center_y - center_y) ** 2)

                # If the distance is less than a certain threshold, consider it as a valid detection
                if distance < 50:  # You can adjust this value as needed
                    person_detected = True
                    print("person detected")
                    greeting = greet_new_user()
                    return greeting

                # else:
                # print("face not in center")
        except Exception as e:
            person_detected = False
            # print(f"An error occurred: {e}")

        # display
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 800, 600)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


def greet_new_user():
    greetings = [
        "hi, I'm Rami bot, nice to meet you",
        "hello! i am rami with the bot, Rami bot",
        "excuse me, could you please move, you're blocking my view",
        "almost didn't see you there, hi! i'm Rami bot",
        "hello there, i'm Rami bot, how can i help you today?",
        "Hey! I'm Rami bot, nice to meet you",
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
    get_camera_list()
