# Description: This file contains the configuration settings for the application.


# MainApp.py
WINDOW_SIZE = (1920, 1080)
HOST_IP = 'http://192.168.80.4:5000'
# HOST_IP = "http://192.168.254.169:5000" # laptop IP
IMAGE_PATH = 'downloaded_image.jpg'  # Define a constant path for the image to prevent storage bloat
REQUEST_TIMEOUT = 2
TIMEOUT_DURATION = 20
ANNOUNCEMENT_INTERVAL = 120

# face recognition
CAMERA_INDEX = 0

# speech recognition
DEVICE_INDEX = None

# speech recog parameters
PAUSE_THRESHOLD = .8
ENERGY_THRESHOLD = 3500
OPERATION_TIMEOUT = 5000
DYNAMIC_ENERGY_THRESHOLD = False
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 5

MODEL_PATH = "../en_US-lessac-medium.onnx"  # Update this with the path to your local model file

# SQL profile for Local laptop
HOST = "localhost"
USER = "kin"
PASSWORD = "asdf"
DATABASE ="ramibot_local"
AUTOCOMMIT = True

# SQL profile for APC Network
# HOST = "airhub-soe.apc.edu.ph"
# USER = "marj"
# PASSWORD = "RAMIcpe211"
# DATABASE ="ramibot"
# AUTOCOMMIT = True

