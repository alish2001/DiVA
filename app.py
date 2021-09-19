# main.py
# import the necessary packages
from verficationPipeline import anti_spoof_check
from flask import Flask, render_template, Response, redirect
from camera import VideoCamera
import time
import cv2

app = Flask(__name__)
STATUS_MSG = ''

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

@app.route('/anti_spoof_verification')
def anti_spoof_verification():
    return Response(anti_spoof_check(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/id_verification')
def id_verification():
    return Response(id_check(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)