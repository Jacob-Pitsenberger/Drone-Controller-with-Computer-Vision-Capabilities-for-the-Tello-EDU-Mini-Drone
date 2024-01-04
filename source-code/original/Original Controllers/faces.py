"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the FacesController class which is used to control
         the elements in the Faces frame view.
Uses: main.py (models package), main.py (views package), faces.py (models package)
"""

import os
from models.main import Model
from views.main import View
from tkinter import filedialog
from PIL import Image, ImageTk

class FacesController:
    def __init__(self, model: Model, view: View):
        # Initialize the Model and View classes, set the current frame, and bind its widgets
        self.model = model
        self.view = view
        self.frame = self.view.frames["Faces"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.close_btn.config(command=self.close)
        self.frame.open_btn.config(command=self.open)
        self.frame.new_btn.config(command=self.open_add_face)

    def close(self) -> None:
        # Remove reference to image object and filename text when closing the frame
        self.remove_lbl_txt()
        self.frame.image_lbl.image = None
        self.view.switch("Home")

    def open_add_face(self) -> None:
        # remove filename lbl text, image from image lbl, and switch view to the add faces frame view.
        self.remove_lbl_txt()
        self.frame.image_lbl.image = None
        self.view.switch("Add Face")

    def open(self) -> None:
        """Display the file search box in the faces directory and display the image selected"""
        dirPath = self.model.faces.path
        self.view.filePath = filedialog.askopenfilename(initialdir=dirPath, title="Open Face Image File")
        filename = os.path.basename(self.view.filePath)
        faceName = os.path.splitext(filename)[0]
        self.frame.filename_lbl.config(text=faceName)
        face_img = ImageTk.PhotoImage(Image.open(self.view.filePath))
        self.frame.image_lbl.config(image=face_img)
        # Keep reference to image object by attaching it to widget attribute
        self.frame.image_lbl.image = face_img

    def remove_lbl_txt(self):
        # remove the text from the filename label
        self.frame.filename_lbl.config(text="")



