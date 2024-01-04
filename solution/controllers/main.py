"""
Author: Jacob Pitsenberger
Program: ManagementUI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the Controller class which initializes controller classes for use by this program,
         contains a method to control user login/logout state changes regarding switching between login and home
         frames, and a method to start the view class as the Tkinter main loop.
Uses: users.py (models package), main.py (models package), main.py (views package), and all modules
      in the controllers package
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
from views.main import View
from .add_face import AddFaceController
from .faces import FacesController
from .home import HomeController
from .login import LoginController
from .add_user import AddUserController
from .flight_logs import FlightLogsController
from .objects import ObjectsController
from .add_object import AddObjectController
from models.users import Users

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        # Initialize the Model and View classes, and all controller classes
        self.view = view
        self.model = model
        self.login_controller = LoginController(model, view)
        self.add_user_controller = AddUserController(model, view)
        self.home_controller = HomeController(model, view)
        self.faces_controller = FacesController(model, view)
        self.add_face_controller = AddFaceController(model, view)
        self.flight_logs_controller = FlightLogsController(model, view)
        self.objects_controller = ObjectsController(model, view)
        self.add_object_controller = AddObjectController(model, view)

        # Add an event listener for authorization state changes
        self.model.users.add_event_listener("auth_changed", self.auth_state_listener)

    def auth_state_listener(self, data: Users) -> None:
        """This method is used to update the home frame view and switch between the login and home
        frames depending on whether a user is authorized through valid login to the system"""
        if data.isActive:
            self.home_controller.update_view()
            self.view.switch("Home")
        else:
            self.view.switch("Login")

    def start(self) -> None:
        """This method determines whether there is an active user and starts the mainloop with the root window
        first displaying either the login view or the home view depending on whether the user is active or not"""
        if self.model.users.isActive:
            self.view.switch("home")
        else:
            self.view.switch("Login")
        self.view.start_mainloop()
