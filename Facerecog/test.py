import cv2
import main

video = cv2.VideoCapture(0)
main.realtime_face_recognition(video)