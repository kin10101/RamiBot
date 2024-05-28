import cv2
import face_recog_module

video = cv2.VideoCapture(1)
face_recog_module.realtime_face_recognition(video)