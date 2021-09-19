import cv2 as cv
import mediapipe as mp
import time
import math
import numpy as np

class blinkDetector():
    def __init__(self) -> None:

        # constants
        self.CLOSED_EYES_FRAME = 2
        self.FONTS =cv.FONT_HERSHEY_COMPLEX

        # Left eyes indices 
        self.LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        # right eyes indices
        self.RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  

        self.map_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5)


    # landmark detection function 
    def landmarksDetection(self, frame, results, draw=False):
        img_height, img_width= frame.shape[:2]
        # list[(x,y), (x,y)....]
        mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
        if draw :
            [cv.circle(frame, p, 2, (0,255,0), -1) for p in mesh_coord]
        
        return mesh_coord

    # Euclaidean distance 
    def euclaideanDistance(self, point, point1):
        x, y = point
        x1, y1 = point1
        distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
        return distance

    # Blinking Ratio
    def blinkRatio(self, landmarks):
        # Right eyes 
        # horizontal line 
        rh_right = landmarks[self.RIGHT_EYE[0]]
        rh_left = landmarks[self.RIGHT_EYE[8]]
        # vertical line 
        rv_top = landmarks[self.RIGHT_EYE[12]]
        rv_bottom = landmarks[self.RIGHT_EYE[4]]

        # LEFT_EYE 
        # horizontal line 
        lh_right = landmarks[self.LEFT_EYE[0]]
        lh_left = landmarks[self.LEFT_EYE[8]]

        # vertical line 
        lv_top = landmarks[self.LEFT_EYE[12]]
        lv_bottom = landmarks[self.LEFT_EYE[4]]

        rhDistance = self.euclaideanDistance(rh_right, rh_left)
        rvDistance = self.euclaideanDistance(rv_top, rv_bottom)

        lvDistance = self.euclaideanDistance(lv_top, lv_bottom)
        lhDistance = self.euclaideanDistance(lh_right, lh_left)

        reRatio = rhDistance/rvDistance
        leRatio = lhDistance/lvDistance

        ratio = (reRatio+leRatio)/2
        return ratio

    def detectBlinks(self, frame, CEF_COUNTER, TOTAL_BLINKS):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        results  = self.face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_coords = self.landmarksDetection(frame, results, False)
            ratio = self.blinkRatio(mesh_coords)
            cv.putText(frame, 'Ratio {0:.2f}'.format(ratio), (100, 100), self.FONTS, 0.8, (0,255,0), 2)

            if ratio > 5.0:
                CEF_COUNTER +=1
                cv.putText(frame, 'Blink', (200, 50), self.FONTS, 0.8, (147,20,255), 2)
        
            else:
                if CEF_COUNTER>self.CLOSED_EYES_FRAME:
                    TOTAL_BLINKS +=1
                    CEF_COUNTER =0

            cv.putText(frame, f'Total Blinks: {TOTAL_BLINKS}', (100, 150), self.FONTS, 0.8, (0,255,0), 2)
            
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.LEFT_EYE ], dtype=np.int32)], True, (0,255,0), 1, cv.LINE_AA)
            cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.RIGHT_EYE ], dtype=np.int32)], True,(0,255,0), 1, cv.LINE_AA)
        
        return frame, CEF_COUNTER, TOTAL_BLINKS


def main():
    bd = BlinkDetector()
    bd.detectBlinks()

if __name__=='__main__':
    main()