"""
Author: Jacob Pitsenberger
Program: ManagementUI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module defines the Users class model which is used to interact with the User database table.
         This handles the data logic of a user request regarding writing data to, getting data from, and
         validating data from the Users table. A dictionary is also contained in this module to define
         the columns for a record in the Users table.
Uses: base.py, database.py
"""
"""
    -Adapted From-
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

import sqlite3
import database as db
from typing import TypedDict, Union
from .base import ObservableModel


class User(TypedDict):
    username: str
    password: str
    firstName: str
    lastName: str
    drone: str


class Users(ObservableModel):
    def __init__(self):
        super().__init__()
        # Connect to the database and make the database tables if they don't exist.
        self.connection = sqlite3.connect('D:\Project\data-files\database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(db.make_users)
        self.cursor.execute(db.make_drones)
        self.cursor.execute(db.make_flight_logs)

        # User is initially not active
        self.isActive = False

        # Initially no current users
        self.activeUser: Union[User, None] = None

    def add_user(self, username, password, first_name, last_name, drone_name) -> None:
        # Insert into table
        # drone = "TelloEDU"
        sdk = "3.0"
        flights = None
        self.cursor.execute("INSERT OR IGNORE INTO Users VALUES (:u_name, :password, :f_name, :l_name, :d_name)",
                            {
                                'u_name': username,
                                'password': password,
                                'f_name': first_name,
                                'l_name': last_name,
                                'd_name': drone_name
                            })
        self.cursor.execute("INSERT OR IGNORE INTO Drones (name, flights, sdk) Values (:name, :flights, :sdk)",
                            {
                                'name': drone_name,
                                'flights': flights,
                                'sdk': sdk
                            })
        self.connection.commit()

    def login(self, user: User):
        # Set user as active if this is successful
        self.isActive = db.login(user['username'], user['password'])

        # If set as active then the user logged in with valid credentials and is set as the current user
        if self.isActive:
            self.activeUser = user
            # trigger the event to display the home frame
            self.trigger_event("auth_changed")
        # Else no valid credentials were entered
        else:
            self.activeUser = None
            print("wrong username or password")

    def logout(self) -> None:
        """
        Title: tkinter-multiframe-mvc
        Author: Nazmul Ahsan
        Date: 1-6-23
        Code Version: N/A
        Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
        """
        """
        Upon pressing the logout button set that the user in not active, that there are not current users,
        and trigger the event to display the login frame.
        """
        self.isActive = False
        self.activeUser = None
        self.trigger_event("auth_changed")
