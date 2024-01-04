"""
Author: Jacob Pitsenberger
Program: Used in both Drone Controller and ManagementUI programs
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains variables that store the create table statements for the three database tables
         used by the system. In addition to this, a login function that is used to validate user login
         credentials and a function to get the name of the current user logged in are contained in this module
         but are only used in the management program. For the drone controller program this module is imported
         for use in the models packages logs module.
Uses: N/A
"""

import sqlite3

# Variable for Users create table statement
make_users = (''' CREATE TABLE IF NOT EXISTS Users
                ( username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  firstName TEXT NOT NULL,
                  lastName TEXT NOT NULL,
                  drone TEXT,
                  PRIMARY KEY(username, password)
                );''')

# Variable for Drones create table statement
make_drones = (''' CREATE TABLE IF NOT EXISTS Drones
                ( name TEXT PRIMARY KEY NOT NULL,
                  flights INT,
                  sdk TEXT NOT NULL,
                  FOREIGN KEY(name) REFERENCES Users(drone)
                );''')

# Variable for FlightLogs create table statement
make_flight_logs = (''' CREATE TABLE IF NOT EXISTS FlightLogs
                    (   id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flightDate TEXT NOT NULL,
                        startTime TEXT NOT NULL,
                        endTime TEXT NOT NULL,
                        startBattery TEXT NOT NULL,
                        endBattery TEXT NOT NULL,
                        motorTime TEXT NOT NULL,
                        FOREIGN KEY(id) REFERENCES Drones(flights)
                    ); ''')


# Used for login in users model
def login(username, password):
    # Have to connect to db and create cursor inside function when use function
    conn = sqlite3.connect('D:\Project\data-files\database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
    if c.fetchall():
        return True
    else:
        return False

    conn.close()

# Used in login controller for user login
def getName(username, password):
    # Have to connect to db and create cursor inside function when use function
    conn = sqlite3.connect('D:\Project\data-files\database.db')
    c = conn.cursor()
    c.execute("SELECT firstName, lastName, drone FROM Users WHERE username=? AND "
              "password=?", (username, password))
    user = c.fetchone()
    return user
    conn.close()

