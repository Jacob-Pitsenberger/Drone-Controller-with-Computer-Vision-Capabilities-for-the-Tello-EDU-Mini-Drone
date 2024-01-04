"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the LoginController class which is used to control
         the elements in the Login frame view.
Uses: main.py (models package), main.py (views package), users.py (models package), database.py
"""
"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

from models.main import Model
from models.users import User
from views.main import View
import database as db

class LoginController:
    def __init__(self, model: Model, view: View) -> None:
        # Initialize the Model and View classes, set the current frame, and bind its widgets
        self.model = model
        self.view = view
        self.frame = self.view.frames["Login"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.login_btn.config(command=self.login)
        self.frame.new_user_btn.config(command=self.add_user)

    def add_user(self) -> None:
        # Switch view to the add users frame view
        self.view.switch("New User")

    def login(self) -> None:
        """Get the username and password from the entry boxes and the associated records first and last names
        if a record exists for this in the database then check that this exists and if so create a dictionary
        record to hold that user's information, calls the users models login method, and configure the invalid
        label to no contain text."""
        username = self.frame.username.get()
        password = self.frame.password.get()
        # Make sure entry boxes are not empty
        if len(username) and len(password) != 0:
            fullName = db.getName(username, password)
            # if fullName is none then a record doesn't exist for the username/password entered
            if fullName is None:
                self.frame.invalid_lbl.config(text="Wrong Username or Password")
                print("check if fullname is none")
                print(username)
                print(password)
                print(fullName)
            else:
                data = {"username": username, "password": password, "firstName": fullName[0],
                        "lastName": fullName[1], "droneName": fullName[2]}
                user: User = {"username": data["username"], "password": data["password"],
                              "firstName": data["firstName"], "lastName": data["lastName"], "drone": data["droneName"]}
                self.model.users.login(user)
                self.clear_form()

    def clear_form(self) -> None:
        # Clear all entered text from the frame
        username = self.frame.username.get()
        password = self.frame.password.get()
        self.frame.username.delete(0, last=len(username))
        self.frame.password.delete(0, last=len(password))
        self.frame.invalid_lbl.config(text="")




