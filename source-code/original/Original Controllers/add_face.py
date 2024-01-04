"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the AddFaceController class which is used to control
         the elements in the addFace frame view.
Uses: main.py (models package), main.py (views package), faces.py (models package)
"""

import os
import shutil
from models.main import Model
from views.main import View
from tkinter import filedialog

class AddFaceController:
    def __init__(self, model: Model, view: View):
        # Initialize the Model and View classes, set the current frame, and bind its widgets
        self.model = model
        self.view = view
        self.frame = self.view.frames["Add Face"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.close_btn.config(command=self.close)
        self.frame.add_btn.config(command=self.add)
        self.frame.search_btn.config(command=self.search)

    def close(self) -> None:
        """Display the Faces frame"""
        self.remove_success_txt()
        self.view.switch("Faces")

    def search(self) -> None:
        """Display the file search box in the faces directory"""
        self.view.filePath = filedialog.askopenfilename(initialdir="/", title="Search Files to add Face")
        self.frame.img_path_lbl.config(text=self.view.filePath)
        self.remove_success_txt()

    def add(self) -> None:
        # Get the path to the faces dir
        faces_dir = self.model.faces.path
        # Get the file name from the img path label
        src_file = self.frame.img_path_lbl.cget("text")
        # Get only  the base name from the file name
        old_filename = os.path.basename(src_file)

        # copy the searched image to the faces directory
        shutil.copy(str(src_file), str(faces_dir))
        # Get the faces name and rename the image for the face in the faces directory to this
        first_name = self.frame.first_name.get()
        last_name = self.frame.last_name.get()
        if first_name and last_name != "":
            new_filename = first_name + " " + last_name + ".jpg"
            src = os.path.join(faces_dir, old_filename)
            des = os.path.join(faces_dir, new_filename)
            os.rename(src, des)
            # clear the frame and configure the success message to be displayed
            self.clear_form()
            self.remove_img_txt()
            self.frame.success_lbl.config(text="Face successfully added!")
        else:
            pass

    def clear_form(self) -> None:
        # Clear all entered text from the frame
        first_name = self.frame.first_name.get()
        last_name = self.frame.last_name.get()
        self.frame.first_name.delete(0, last=len(first_name))
        self.frame.last_name.delete(0, last=len(last_name))

    def remove_img_txt(self):
        # Remove the text from the path label
        self.frame.img_path_lbl.config(text="")

    def remove_success_txt(self):
        # Remove the success message text
        self.frame.success_lbl.config(text="")

