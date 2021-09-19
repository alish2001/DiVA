# main.py
# import the necessary packages
from verficationPipeline import anti_spoof_check, id_check
from flask import Flask, render_template, Response, redirect
from camera import VideoCamera

app = Flask(__name__)

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
    return render_template('id_check.html')

@app.route('/id_verification/video_feed')
def id_verification_video_feed():
    return Response(id_check(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
