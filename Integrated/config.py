import os
from dotenv import load_dotenv

# Description: This file contains the configuration settings for the application.

# Load the .env file
load_dotenv()


# MainApp.py
WINDOW_SIZE = tuple(map(int, os.getenv('WINDOW_SIZE').strip('()').split(',')))
HOST_IP = os.getenv('HOST_IP')
IMAGE_PATH = os.getenv('IMAGE_PATH')
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT'))
TIMEOUT_DURATION = int(os.getenv('TIMEOUT_DURATION'))
ANNOUNCEMENT_INTERVAL = int(os.getenv('ANNOUNCEMENT_INTERVAL'))

# face recognition
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX'))

# speech recognition
DEVICE_INDEX = os.getenv('DEVICE_INDEX')

# speech recog parameters
PAUSE_THRESHOLD = float(os.getenv('PAUSE_THRESHOLD'))
ENERGY_THRESHOLD = int(os.getenv('ENERGY_THRESHOLD'))
OPERATION_TIMEOUT = int(os.getenv('OPERATION_TIMEOUT'))
DYNAMIC_ENERGY_THRESHOLD = os.getenv('DYNAMIC_ENERGY_THRESHOLD') == 'True'
LISTEN_TIMEOUT = int(os.getenv('LISTEN_TIMEOUT'))
PHRASE_TIME_LIMIT = int(os.getenv('PHRASE_TIME_LIMIT'))

MODEL_PATH = os.getenv('MODEL_PATH')

# SQL profile for Local laptop
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
AUTOCOMMIT = os.getenv('AUTOCOMMIT') == 'True'

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

