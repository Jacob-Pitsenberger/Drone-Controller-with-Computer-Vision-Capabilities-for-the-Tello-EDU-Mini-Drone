"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the AddUserController class which is used to control
         the elements in the addUser frame view.
Uses: main.py (models package), main.py (views package), users.py (models package)
"""
import database

"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

from models.main import Model
from views.main import View

class AddUserController:
    def __init__(self, model: Model, view: View):
        # Initialize the Model and View classes, set the current frame, and bind its widgets
        self.model = model
        self.view = view
        self.frame = self.view.frames["New User"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.add_user_btn.config(command=self.add_user)
        self.frame.cancel_btn.config(command=self.cancel)

    def cancel(self) -> None:
        """Display the Login frame"""
        self.view.switch("Login")

    def add_user(self) -> None:
        """Get the text from the entry boxes, call the add user method from the Users model, clear the form,
        and display the success message"""
        username = self.frame.username.get()
        password = self.frame.password.get()
        first_name = self.frame.first_name.get()
        last_name = self.frame.last_name.get()
        drone_name = self.frame.drone_name.get()
        # If all fields entered and a record with these values doesn't exist add new record with
        # entries as values to database
        if username or password or first_name or last_name or drone_name != "" and database.getName(username, password) is None:
            self.model.users.add_user(username, password, first_name, last_name, drone_name)
            self.clear_form()
            self.frame.success_message_label.config(text="User added to the System.")
        else:
            pass

    def clear_form(self) -> None:
        # Clear all entered text from the frame
        username = self.frame.username.get()
        password = self.frame.password.get()
        first_name = self.frame.first_name.get()
        last_name = self.frame.last_name.get()
        drone_name = self.frame.drone_name.get()
        self.frame.username.delete(0, last=len(username))
        self.frame.password.delete(0, last=len(password))
        self.frame.first_name.delete(0, last=len(first_name))
        self.frame.last_name.delete(0, last=len(last_name))
        self.frame.drone_name.delete(0, last=len(drone_name))


