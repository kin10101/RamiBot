import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()

# Specify the base directory where user-specific folders are located
base_path = "datasets"


def getImageID(base_path):
    imagePaths = [os.path.join(base_path, user_id, image_file) for user_id in os.listdir(base_path) for image_file in
                  os.listdir(os.path.join(base_path, user_id))]
    faces = []
    ids = []
    print("Training Model............")
    for imagePath in imagePaths:
        faceImage = Image.open(imagePath).convert('L')
        faceNP = np.array(faceImage)

        # Extract the user ID from the folder name (user_id) within the base_path
        user_id = os.path.basename(os.path.dirname(imagePath))
        Id = int(user_id)

        faces.append(faceNP)
        ids.append(Id)
        cv2.imshow("Training", faceNP)
        cv2.waitKey(1)

    return ids, faces


IDs, facedata = getImageID(base_path)
try:
    recognizer.train(facedata, np.array(IDs))
except cv2.error as e:
    print(f"OpenCV error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
recognizer.write("Trainer.yml")
cv2.destroyAllWindows()
print("Training Completed............")
