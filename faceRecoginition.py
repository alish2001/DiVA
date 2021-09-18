import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import numpy as np
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


# This key will serve all examples in this document.
KEY = "1ab54bc5614647758a15fa64980c4af1"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://face-recognition-diva.cognitiveservices.azure.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


IMAGE_BASE_PATH = 'Faces'

# Create target image file name and path
target_image_file_name = 'Faraz-face.jpeg'
target_image_file_path =  os.path.join(IMAGE_BASE_PATH, target_image_file_name)
# Create source image file name and path
source_image_file_name = 'Faraz-id-2.jpeg'
source_image_file_path =  os.path.join(IMAGE_BASE_PATH, source_image_file_name)


target_image = open(target_image_file_path, 'r+b')
source_image = open(source_image_file_path, 'r+b')

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

def drawFaceRectangles(face_image_path, detected_faces) :
    image = Image.open(face_image_path)

    # For each face returned use the face rectangle and draw a red box.
    #print('Drawing rectangle around face... see popup for results.')
    draw = ImageDraw.Draw(image)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red', width=5)

    # Display the image in the default image browser.
    #image.show()
    return image

def detectFaces(image_path):
    # Get Image from path
    image = open(image_path, 'r+b')

    # Detect face(s) from source image 1, returns a list[DetectedFaces]
    detected_faces = face_client.face.detect_with_stream(image, detection_model='detection_03')
    
    # Add the returned face's face ID
    detected_image_id = detected_faces[0].face_id
    print('{} face(s) detected from image {}.'.format(len(detected_faces), image_path))
    
    return detected_faces, detected_image_id

def verifyFaces(detected_source_image_id, detected_target_image_id):
    # Verification example for faces of the same person. The higher the confidence, the more identical the faces in the images are.
    # Since target faces are the same person, in this example, we can use the 1st ID in the detected_faces_ids list to compare.
    verify_result = face_client.face.verify_face_to_face(detected_source_image_id, detected_target_image_id)
    print('Faces from {} & {} are of the same person, with confidence: {}'
        .format(source_image_file_name, target_image_file_name, verify_result.confidence)
        if verify_result.is_identical
        else 'Faces from {} & {} are of a different person, with confidence: {}'
            .format(source_image_file_name, target_image_file_name, verify_result.confidence))

    return verify_result



source_detected_faces, detected_source_image_id = detectFaces(source_image_file_path)
# Draw faces around image
source_image_with_face = drawFaceRectangles(
    source_image_file_path,
    source_detected_faces
)

target_detected_faces, detected_target_image_id = detectFaces(target_image_file_path)
# Draw faces around image
target_image_with_face = drawFaceRectangles(
   target_image_file_path,
   target_detected_faces
)

source_image_with_face = source_image_with_face.resize((400, 400))
target_image_with_face = target_image_with_face.resize((400, 400))
Image.fromarray(np.column_stack((np.array(target_image_with_face),np.array(source_image_with_face)))).show()

verify_result = verifyFaces(detected_source_image_id, detected_target_image_id)



