import random
import numpy as np
import time
from deepface import DeepFace
import cv2

# Initialize global variables
person_detected = False
running = False

#start of face recognition module--------------------------------------------------------------------------------------
def realtime_face_recognition(video):
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
                print("Can't receive frame (stream end?). Exiting...")


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
                    return person_detected
                    break

                else:
                    print("face not in center")
        except Exception as e:
            person_detected = False
            print(f"An error occurred: {e}")

        # display
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 800, 600)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

#end of face recognition module----------------------------------------------------------------------------------------

#other modules---------------------------------------------------------------------------------------------------------

def greet_new_user():
    random_num = random.randint(1,5)
    if random_num == 1:
        return "Hello there, I'm Rami bot!"
    elif random_num == 2:
        return "Hello friend! my name is Rami bot!"
    elif random_num == 3:
        return "Good day, I'm Rami bot!"
    elif random_num == 4:
        return "Hi there, I'm Rami bot!"
    elif random_num == 5:
        return "Greetings, I'm Rami bot!"

def get_camera_list(max_cameras=10):
    """Get a list of available camera devices and their index."""
    cameras = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cameras.append(index)
        cap.release()
    return cameras

get_camera_list(5)