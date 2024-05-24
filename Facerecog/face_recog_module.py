import random
import numpy as np

from deepface import DeepFace
import cv2

# Initialize global variables
person_detected = False
running = False


def realtime_face_recognition(video):
    global person_detected
    global running

    running = True

    while running:
        try:
            # Read frame from video
            ret, frame = video.read()
            if not ret:
                break

            # Get frame dimensions and calculate center point
            height, width, _ = frame.shape
            center_x = width // 2
            center_y = height // 2

            # Extract faces using DeepFace
            detections = DeepFace.extract_faces(img_path=frame, detector_backend='yunet', enforce_detection=False)
            for face in detections:
                facial_area = face['facial_area']
                x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']

                # Calculate the center point of the face
                face_center_x = x + w // 2
                face_center_y = y + h // 2

                # Calculate Euclidean distance between face center and frame center
                distance = np.sqrt((face_center_x - center_x) ** 2 + (face_center_y - center_y) ** 2)

                # Consider as valid detection if within threshold distance
                if distance < 50:  # Adjust threshold as needed
                    person_detected = True
                    #print("Person detected")
                    running = False
                    break
            else:
                pass
                #print("No face detected")

        except Exception as e:
            person_detected = False
            print(f"An error occurred: {e}")

        # Uncomment the lines below to display the frame (optional)
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame', 800, 600)
        # cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    video.release()
    cv2.destroyAllWindows()


def greet_new_user():
    random_num = random.randint(1, 5)
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
