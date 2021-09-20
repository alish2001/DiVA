import cv2
import numpy as np

class documentLocalizer():

    def __init__(self, documentWidth= 350, documentHeight=200,  startPoint = (150, 140),  endPoint = (500, 340), thickness=2, color= (147, 147, 147)) -> None:
        self.documentWidth = documentWidth
        self.documentHeight = documentHeight
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.thickness = thickness
        self.color = color

    ## Function for placing a designated rectangle on video feed for ID detection
    def getPlaceHolder(self, image):
        placeHolder = cv2.rectangle(image, self.startPoint, self.endPoint, self.color, self.thickness)
        return placeHolder

    ## Function for ID card localization using change of prespective
    def getLocalizedDocument(self, image):
        pts1 = np.float32([[self.startPoint[0], self.startPoint[1]],[self.endPoint[0], self.startPoint[1]], [self.startPoint[0], self.endPoint[1]],[self.endPoint[0], self.endPoint[1]]]) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[self.documentWidth, 0], [0, self.documentHeight],[self.documentWidth, self.documentHeight]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(image, matrix, (self.documentWidth, self.documentHeight))

        return imgWarpColored

def main():
    dl = documentLocalizer()
    camera = cv2.VideoCapture(1)
    while True:
        ret, frame = camera.read() # getting frame from camera 
        if not ret: 
            break # no more frames break

        # Window name in which image is displayed
        window_name = 'Image'
        
        image = dl.getPlaceHolder(frame)
        imgWarpColored = dl.getLocalizedDocument(frame)
        
        # Displaying the image 
        cv2.imshow(window_name, image)
        cv2.imshow("Warpped", imgWarpColored)
        key =cv2.waitKey(2)
        if key==ord('q') or key ==ord('Q'):
            break

    cv2.destroyAllWindows()
    camera.release()

if __name__ == "__main__":
    main()