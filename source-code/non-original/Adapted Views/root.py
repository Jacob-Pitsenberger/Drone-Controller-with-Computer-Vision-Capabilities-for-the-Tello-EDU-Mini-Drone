"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the Root class which is used as the sole root window in this program.
Uses: N/A
"""
"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

from tkinter import Tk

class Root(Tk):
    def __init__(self):
        super().__init__()
        # set the size of the root window to full screen
        self.state('zoomed')
        # Set the title
        self.title("Drone Controller with Computer Vision Capabilities for the Tello EDU Mini Drone")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)