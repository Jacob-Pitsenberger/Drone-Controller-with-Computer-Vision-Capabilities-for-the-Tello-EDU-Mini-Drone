"""
Author: Jacob Pitsenberger
Program: Used in both Drone Controller and ManagementUI programs
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This model contains the Faces model class which interacts with the Faces directory.
         This handles the data logic of a user request regarding getting data from and writing
         data to the Faces directory. This module also contains a function for encoding the face
         images in the faces directory which is not used in the management system but is used to
         create the face encodings when the drone controller is launched.
Uses: base.py
"""

import os
import cv2
import face_recognition

from .base import ObservableModel
from pathlib import Path

def findEncodings(images):
    """
    Title: FACE RECOGNITION + ATTENDANCE PROJECT | OpenCV Python | Computer Vision
    Author: Murtaza's Workshop - Robotics and AI
    Date: 6-11-20
    Code Version: N/A
    Availability: https://www.youtube.com/watch?v=sz25xxF_AVE&t=957s
    """
    """
    Define a list to hold encoding then loop through the images passed in, convert them to
    grayscale, get their encodings, add the encodings to the list, and then return this list of encodings
    """
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


class Faces(ObservableModel):
    def __init__(self):
        super().__init__()
        # Create a path to the Faces directory and create the directory if it doesn't exist.
        self.path = Path('D:\Project\data-files\output-files\Faces')
        self.make_dir()

        # Create an empty list to hold the images
        self.images = []

        # Take names from images and put them in a list
        self.classNames = []

        # Load these two lists
        self.load_lists()

        # Make list of encodings
        self.encodeListKnown = findEncodings(self.images)

    def load_lists(self):
        """
            -Adapted From-
        Title: FACE RECOGNITION + ATTENDANCE PROJECT | OpenCV Python | Computer Vision
        Author: Murtaza's Workshop - Robotics and AI
        Date: 6-11-20
        Code Version: N/A
        Availability: https://www.youtube.com/watch?v=sz25xxF_AVE&t=957s
        """
        """For each image in the faces directory add the image to the images list and get each images
        file name and add it to the list of face names
        """
        imgList = os.listdir(self.path)
        for cl in imgList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])

    def make_dir(self) -> None:
        """
        This checks if the directory exists and if not make it
        """
        if not os.path.exists(self.path):
            self.path.mkdir()


