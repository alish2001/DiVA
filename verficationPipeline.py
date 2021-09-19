import time
import cv2
from blinkDetector import blinkDetector


def anti_spoof_check(camera, min_count=3, timeout=30, period_interval=7):
    bl = blinkDetector()
    FONTS = cv2.FONT_HERSHEY_COMPLEX
    TOTAL_BLINKS = 0
    CEF_COUNTER = 0
    frame_counter = 0
    status = 400
    
    # starting time here 
    start_time = time.time()
    end_time = start_time
    period_time = start_time

    # starting Video loop here.
    while True:
        if TOTAL_BLINKS >= min_count and end_time - period_time >= 0:
            status = 400
            break
        elif end_time - start_time > timeout:
            status = 401
            break
            
        if end_time - period_time > period_interval:
            period_time = end_time

        frame_counter +=1 # frame counter
        ret, frame = camera.read() # getting frame from camera 
        if not ret: 
            break # no more frames break

        frame, CEF_COUNTER, TOTAL_BLINKS = bl.detectBlinks(frame, CEF_COUNTER, TOTAL_BLINKS)

        # calculating frame per seconds FPS
        end_time = time.time()
        fps = frame_counter/(end_time - start_time)
        cv2.putText(frame,f'FPS: {round(fps,1)}',(30, 50), FONTS, 1.2, (0,255,0), 2)

        cv2.putText(frame,'Total Time left: {0:.2f}'.format(timeout - (end_time- start_time)),(600, 50), FONTS, 0.8, (0,0,255), 2)
        cv2.putText(frame,'Period Time left: {0:.2f}'.format(period_interval - (end_time-period_time)),(600, 100), FONTS, 0.8, (0,0,255), 2)

        frame = camera.get_frame(frame)

        # writing image for thumbnail drawing shape
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    if status == 400:
        ret, frame = camera.read() # getting frame from camera
        cv2.rectangle(frame, (120, 120), (550, 300), (0,153,0), -1)
        cv2.putText(frame,'LIVELINESS VERIFIED!', (170, 200), FONTS, 1.0, (0,0,255), 2)
        cv2.putText(frame,'PRESS NEXT', (200, 260), FONTS, 1.0, (0,0,255), 2)
        frame = camera.get_frame(frame)
    else:
        ret, frame = camera.read() # getting frame from camera
        cv2.rectangle(frame, (120, 120), (550, 300), (0,0,0), -1)
        cv2.putText(frame,'LIVELINESS FAILED!', (170, 200), FONTS, 1.0, (0,0,255), 2)
        frame = camera.get_frame(frame)

    # writing image for thumbnail drawing shape
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def selfie_taker():
    pass

def selfie_taker():
    pass