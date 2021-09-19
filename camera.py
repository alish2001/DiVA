# camera.py
# import the necessary packages
import cv2
from blinkDetector import blinkDetector
import time

# defining face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6


class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def read(self):
        return self.video.read()

    def release(self):
        self.video.release()

    def get_frame(self, frame):
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
