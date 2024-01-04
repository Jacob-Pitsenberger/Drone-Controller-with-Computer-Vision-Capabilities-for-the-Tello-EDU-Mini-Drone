"""
Author: Jacob Pitsenberger
Program: ManagementUI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the Model class which initializes the Faces, Objects, Users, and Logs
         model classes for use in this program.
Uses: users.py, faces.py, logs.py, objects.py (from the models package)
"""
"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

from .users import Users
from .faces import Faces
from .logs import Logs
from .objects import Objects

class Model:
    def __init__(self):
        self.users = Users()
        self.faces = Faces()
        self.logs = Logs()
        self.objects = Objects()
