import cv2
import os
import main as m

# Create a directory for storing the face images
dataset_dir = "datasets"
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

# Open a video capture object
video = cv2.VideoCapture(1)

# Load a Haar Cascade Classifier for face detection
detect = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

id = input("Enter user ID (e.g. 2021140544): ")
m.insertToDB(id)
user_dir = os.path.join(dataset_dir, id)

# Check if the user directory already exists
if os.path.exists(user_dir):
    # Find the maximum existing image number in the directory
    existing_images = [f for f in os.listdir(user_dir) if f.endswith(".jpg")]
    if existing_images:
        existing_numbers = [int(image.split(".")[2]) for image in existing_images]
        count = max(existing_numbers) + 1
    else:
        count = 101
else:
    os.makedirs(user_dir)
    count = 1

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Increment the count for each detected face
        count += 1

        face_image = gray[y:y + h, x:x + w]
        image_path = os.path.join(user_dir, f"User.{id}.{count}.jpg")
        cv2.imwrite(image_path, face_image)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)

    if count > 200:  # You can adjust this number as needed
        break

video.release()
cv2.destroyAllWindows()
print("Dataset Collection Done..................")
