"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the FlightLogsController class which is used to control
         the elements in the Logs frame view.
Uses: main.py (models package), main.py (views package), logs.py (models package)
"""

from models.main import Model
from views.main import View


class FlightLogsController:
    def __init__(self, model: Model, view: View) -> None:
        """Initialize the Model and View classes, set the current frame, bind its widgets, and call this classes
        show_logs method"""
        self.model = model
        self.view = view
        self.frame = self.view.frames["Logs"]
        self._bind()
        self.show_logs()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.close_btn.config(command=self.open_home)

    def open_home(self) -> None:
        # switch view to the Home frame view.
        self.view.switch("Home")

    def show_logs(self):
        """loop through records and add them to the logs tree view"""
        data = self.model.logs.get_logs()
        count = 0
        for record in data:
            self.frame.log_tree.insert(parent='', index='end', iid=count, text="",
                                       values=(
                                           record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
            count += 1
