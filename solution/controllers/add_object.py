"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the AddObjectController class which is used to control
         the elements in the addObject frame view.
Uses: main.py (models package), main.py (views package), objects.py (models package)
"""

import os
import shutil

from models.main import Model
from views.main import View
from tkinter import filedialog

class AddObjectController:
    def __init__(self, model: Model, view: View):
        # Initialize the Model and View classes, set the current frame, and bind its widgets
        self.model = model
        self.view = view
        self.frame = self.view.frames["Add Object"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.close_btn.config(command=self.close)
        self.frame.add_btn.config(command=self.add)
        self.frame.search_btn.config(command=self.search)

    def close(self) -> None:
        """Display the Objects frame"""
        self.remove_success_txt()
        self.view.switch("Objects")

    def search(self) -> None:
        """Display the file search box in the Objects directory"""
        self.view.filePath = filedialog.askopenfilename(initialdir="/", title="Search Files to add Object")
        self.frame.img_path_lbl.config(text=self.view.filePath)
        self.remove_success_txt()

    def add(self) -> None:
        # Get the path to the objects dir
        objects_dir = self.model.objects.path
        # Get the file name from the img path label
        src_file = self.frame.img_path_lbl.cget("text")
        # Get only  the base name from the file name
        old_filename = os.path.basename(src_file)

        # copy the searched image to the objects directory
        shutil.copy(str(src_file), str(objects_dir))
        # Get the objects name and rename the image for the object in the objects directory to this
        object_name = self.frame.object_name.get()
        if object_name != "":
            new_filename = object_name + ".jpg"
            src = os.path.join(objects_dir, old_filename)
            des = os.path.join(objects_dir, new_filename)
            os.rename(src, des)
            # clear the frame and configure the success message to be displayed
            self.clear_form()
            self.remove_img_txt()
            self.frame.success_lbl.config(text="Object successfully added!")
        else:
            pass

    def clear_form(self) -> None:
        # Clear all entered text from the frame
        object_name = self.frame.object_name.get()
        self.frame.object_name.delete(0, last=len(object_name))

    def remove_img_txt(self):
        # Remove the text from the path label
        self.frame.img_path_lbl.config(text="")

    def remove_success_txt(self):
        # Remove the success message text
        self.frame.success_lbl.config(text="")
