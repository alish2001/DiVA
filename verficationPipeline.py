import time
import cv2
import os
from PIL import Image
from blinkDetector import blinkDetector
from documentLocalizer import documentLocalizer
from faceRecoginition import faceRecognition


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

        frame_counter += 1  # frame counter
        ret, frame = camera.read()  # getting frame from camera
        if not ret:
            break  # no more frames break

        frame, CEF_COUNTER, TOTAL_BLINKS = bl.detectBlinks(
            frame, CEF_COUNTER, TOTAL_BLINKS)

        # calculating frame per seconds FPS
        end_time = time.time()
        fps = frame_counter/(end_time - start_time)
        cv2.putText(frame, f'FPS: {round(fps,1)}',
                    (30, 50), FONTS, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, 'Total Time left: {0:.2f}'.format(
            timeout - (end_time - start_time)), (400, 50), FONTS, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, 'Period Time left: {0:.2f}'.format(
            period_interval - (end_time-period_time)), (400, 100), FONTS, 0.6, (0, 0, 255), 2)

        frame = camera.get_frame(frame)

        # writing image for thumbnail drawing shape
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    if status == 400:
        ret, frame = camera.read()  # getting frame from camera
        cv2.rectangle(frame, (120, 120), (550, 300), (0, 153, 0), -1)
        cv2.putText(frame, 'LIVELINESS VERIFIED!',
                    (170, 200), FONTS, 1.0, (0, 0, 255), 2)
        cv2.putText(frame, 'PRESS NEXT', (200, 260),
                    FONTS, 1.0, (0, 0, 255), 2)
        frame = camera.get_frame(frame)
    else:
        ret, frame = camera.read()  # getting frame from camera
        cv2.rectangle(frame, (120, 120), (550, 300), (0, 0, 0), -1)
        cv2.putText(frame, 'LIVELINESS FAILED!',
                    (170, 200), FONTS, 1.0, (0, 0, 255), 2)
        frame = camera.get_frame(frame)

    # writing image for thumbnail drawing shape
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def id_check(camera, base_folder='Photos', selfie_file_name='selfie_file.png', id_file_name='id_file.jpg', selfie_time=5, id_time=10, break_timer=5):
    # Initial Break
    start_time = time.time()
    curr_time = start_time
    while True:
        _, frame = camera.read()  # getting frame from camera
        if curr_time - start_time > break_timer:
            break

        curr_time = time.time()
        cv2.rectangle(frame, (120, 120), (550, 300), (0, 255, 0), -1)
        cv2.putText(frame, "Get Ready For Selfie", (170, 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
        frame = cv2.putText(frame, "break will end after {0:.1f}s".format(
            break_timer - (curr_time-start_time)), (180, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        frame = camera.get_frame(frame)
        # writing image for thumbnail drawing shape
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Take Selfie
    start_time = time.time()
    curr_time = start_time

    while True:
        _, frame = camera.read()  # getting frame from camera
        if curr_time - start_time > selfie_time:
            selfie_image = frame
            break
        curr_time = time.time()
        frame = cv2.putText(frame, "picture will be taken after {0:.1f}s".format(
            selfie_time - (curr_time-start_time)), (180, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        frame = camera.get_frame(frame)
        # writing image for thumbnail drawing shape
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Second Break
    start_time = time.time()
    curr_time = start_time
    while True:
        _, frame = camera.read()  # getting frame from camera
        if curr_time - start_time > break_timer:
            break

        curr_time = time.time()
        cv2.rectangle(frame, (120, 120), (550, 300), (0, 255, 0), -1)
        cv2.putText(frame, 'Get Ready For ID', (170, 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
        frame = cv2.putText(frame, "break will end after {0:.1f}s".format(
            break_timer - (curr_time-start_time)), (180, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        frame = camera.get_frame(frame)
        # writing image for thumbnail drawing shape
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Take ID Picture
    start_time = time.time()
    curr_time = start_time
    dl = documentLocalizer()
    while True:
        _, frame = camera.read()  # getting frame from camera
        frame = dl.getPlaceHolder(frame)
        if curr_time - start_time > id_time:
            id_image = dl.getLocalizedDocument(frame)
            break

        curr_time = time.time()
        frame = cv2.putText(frame, "picture will be taken after {0:.1f}s".format(
            id_time - (curr_time-start_time)), (180, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        frame = camera.get_frame(frame)
        # writing image for thumbnail drawing shape
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Save files temporarily
    selfie_image_path = os.path.join(base_folder, selfie_file_name)
    cv2.imwrite(selfie_image_path, selfie_image)
    id_image_path = os.path.join(base_folder, id_file_name)
    cv2.imwrite(id_image_path, id_image)

    # Verify Pictures Match
    fc = faceRecognition()
    result = fc.detect_and_verify_faces(
        base_folder, selfie_file_name, id_file_name, draw=False)

    if result.is_identical:
        ret, frame = camera.read()  # getting frame from camera
        cv2.rectangle(frame, (120, 120), (550, 300), (0, 153, 0), -1)
        cv2.putText(frame, 'You Are VERIFIED!', (170, 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
        cv2.putText(frame, 'PRESS Finish', (200, 260),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
        frame = camera.get_frame(frame)
    else:
        ret, frame = camera.read()  # getting frame from camera
        cv2.rectangle(frame, (120, 120), (550, 300), (0, 0, 0), -1)
        cv2.putText(frame, 'Verification Failed', (170, 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
        frame = camera.get_frame(frame)

    # writing image for thumbnail drawing shape
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
