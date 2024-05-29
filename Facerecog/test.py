import cv2
import face_recog_module

video = cv2.VideoCapture(0)
face_recog_module.realtime_face_recognition(video)