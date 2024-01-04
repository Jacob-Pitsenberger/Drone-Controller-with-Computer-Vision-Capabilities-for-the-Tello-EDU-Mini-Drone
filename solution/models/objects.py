"""
Author: Jacob Pitsenberger
Program: Used in both Drone Controller and ManagementUI programs
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the Object model class which interacts with the Objects directory.
         This handles the data logic of a user request regarding getting data from and writing data
         to the Objects directory. This module also contains a function for getting the descriptors
         for the object images in the objects directory which is not used in the management system
         but is used to create the object descriptors when the drone controller is launched.
Uses: base.py
"""

import os
import cv2
from .base import ObservableModel
from pathlib import Path

# Create orb
orb = cv2.ORB_create(nfeatures=1000)

# Create fxn to take list of images and create descriptors one by one then store in new list
def findDes(images):
    """
    Title: Feature Detection and Matching + Image Classifier Project | OPENCV PYTHON
    Author: Murtaza's Workshop - Robotics and AI
    Date: 6-16-20
    Code Version: N/A
    Availability: https://www.youtube.com/watch?v=nnH55-zD38I
    """
    """
    Define a list to hold descriptors then loop through the images passed in, get the descriptors for each
    image, and append these to the descriptors list and return it.
    """
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

class Objects(ObservableModel):
    def __init__(self):
        super().__init__()
        # Create a path to the Objects directory and create the directory if it doesn't exist.
        self.path = Path('D:\Project\data-files\output-files\Objects')
        self.make_dir()

        # Store grayscale images and object names in two lists
        self.images = []
        self.classNames = []

        # Load these lists
        self.load_lists()

        # Get the descriptors for the images in the images list
        self.descriptors = findDes(self.images)

    def load_lists(self):
        """
            -Adapted From-
        Title: Feature Detection and Matching + Image Classifier Project | OPENCV PYTHON
        Author: Murtaza's Workshop - Robotics and AI
        Date: 6-16-20
        Code Version: N/A
        Availability: https://www.youtube.com/watch?v=nnH55-zD38I
        """
        """For each image in the faces directory add the image to the images list and get each images
        file name and add it to the list of face names.
        """
        objectList = os.listdir(self.path)
        # Loop to import each in grayscale (0) using imRead fxn
        for cl in objectList:
            curImg = cv2.imread(f'{self.path}/{cl}', 0)
            self.images.append(curImg)
            # Remove file extension when appending name
            self.classNames.append(os.path.splitext(cl)[0])

    def make_dir(self) -> None:
        """
        This checks if the directory exists and if not make it
        """
        if not os.path.exists(self.path):
            self.path.mkdir()



