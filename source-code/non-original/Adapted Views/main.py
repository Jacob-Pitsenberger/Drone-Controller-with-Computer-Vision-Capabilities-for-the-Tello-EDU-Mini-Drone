"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the View class which is used to add and switch between frames in root window and
         start the tkinter mainloop. A dictionary is also contained in this module to hold the different frame
         classes so that they can be added in the View class add frame method.
Uses: All modules from the views package
"""
"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""


from typing import TypedDict

from .add_face import AddFaceView
from .faces import FacesView
from .home import HomeView
from .root import Root
from .login import LoginView
from .add_user import AddUserView
from .flight_logs import FlightLogsView
from .objects import ObjectsView
from.add_object import AddObjectView


class Frames(TypedDict):
    login: LoginView
    add_user: AddUserView
    home: HomeView
    faces: FacesView
    add_face: AddFaceView
    logs: FlightLogsView
    objects: ObjectsView
    add_object: AddObjectView

class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        self._add_frame(LoginView, "Login")
        self._add_frame(AddUserView, "New User")
        self._add_frame(HomeView, "Home")
        self._add_frame(FacesView, "Faces")
        self._add_frame(AddFaceView, "Add Face")
        self._add_frame(FlightLogsView, "Logs")
        self._add_frame(ObjectsView, "Objects")
        self._add_frame(AddObjectView, "Add Object")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self) -> None:
        self.root.mainloop()
