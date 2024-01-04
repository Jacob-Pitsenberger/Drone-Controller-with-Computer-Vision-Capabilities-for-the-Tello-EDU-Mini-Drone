"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the HomeController class which is used to control
         the elements in the Home frame view.
Uses: main.py (models package), main.py (views package), users.py (models package)
"""
"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

import os
from models.main import Model
from views.main import View

class HomeController:
    def __init__(self, model: Model, view: View) -> None:
        # Initialize the Model and View classes, set the current frame, and bind its widgets
        self.model = model
        self.view = view
        self.frame = self.view.frames["Home"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.logout_btn.config(command=self.logout)
        self.frame.controller_btn.config(command=self.open_controller)
        self.frame.mapping_btn.config(command=self.open_mapping)
        self.frame.logs_btn.config(command=self.open_logs)
        self.frame.faces_btn.config(command=self.open_faces)
        self.frame.objects_btn.config(command=self.open_objects)

    def logout(self) -> None:
        # Call the users models logout method
        self.model.users.logout()

    def open_logs(self) -> None:
        # Switch view to the logs frame view
        self.view.switch("Logs")

    def open_faces(self) -> None:
        # Switch view to the faces frame view
        self.view.switch("Faces")

    def open_objects(self) -> None:
        # Switch view to the objects frame view
        self.view.switch("Objects")

    def open_controller(self) -> None:
        # Launch the drone controller executable and end this program
        print("launching drone controller")
        drone_controller = 'D:\Project\execution-folder\droneController.exe'
        print("before os.system")
        os.system('"%s"' % drone_controller)
        print("destroying root")
        self.view.root.destroy()
        print("end of method")

    def open_mapping(self) -> None:
        # Launch the mapping controller executable and end this program
        drone_controller = 'D:\Project\execution-folder\mappingController.exe'
        os.system('"%s"' % drone_controller)
        self.view.root.destroy()

    def update_view(self) -> None:
        # Get the current user
        current_user = self.model.users.activeUser
        # If there is a current user display their first name and last name attributes in the home frame
        if current_user:
            first_name = current_user["firstName"]
            last_name = current_user["lastName"]
            drone_name = current_user["drone"]
            self.frame.pic_lbl.config(text=f"Pilot In command: {first_name} {last_name}")
            self.frame.drone_lbl.config(text=f"Drone: {drone_name}")
        # Else set this lbl text to be empty
        else:
            self.frame.pic_lbl.config(text=f"")
