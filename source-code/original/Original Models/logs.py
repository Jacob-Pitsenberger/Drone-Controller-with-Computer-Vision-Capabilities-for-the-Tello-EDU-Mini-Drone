"""
Author: Jacob Pitsenberger
Program: Used in both Drone Controller and ManagementUI programs
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the Logs model class which interacts with the FlightLogs database table.
         This handles the data logic of a user request regarding getting data from and adding data to
         the flightLogs table but for this program, data is only taken from the table. Data is added
         through use of the drone controller program.
Uses: base.py, database.py
"""

import sqlite3
import database as db
from .base import ObservableModel


class Logs(ObservableModel):
    def __init__(self):
        super().__init__()
        # Connect to the database and make the FlightLogs table if it doesn't exist.
        self.connection = sqlite3.connect('D:\Project\data-files\database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(db.make_flight_logs)
        self.current_user = None

    def get_logs(self):
        """
        Create an empty list then loop through records in flight logs table
        inserting each into to the list in the order read before returning the list
        """
        data = []
        self.cursor.execute("SELECT * FROM flightLogs")
        records = self.cursor.fetchall()
        count = 0
        for record in records:
            data.insert(count, record)
            count += 1
        return data

    def add_log(self, flightDate, startTime, endTime, startBattery, endBattery, motorTime) -> None:
        # Insert into table and commit the changes
        self.cursor.execute("INSERT INTO FlightLogs(flightDate, startTime, endTime, startBattery, "
                            "endBattery, motorTime) VALUES (:f_date, :s_time, :e_time, :s_batt, :e_batt, :m_time)",
                            {
                                # 'id': log_id,
                                'f_date': flightDate,
                                's_time': startTime,
                                'e_time': endTime,
                                's_batt': startBattery,
                                'e_batt': endBattery,
                                'm_time': motorTime
                            })
        self.connection.commit()

        # Update the flights value and commit the changes (JP)
        self.cursor.execute("UPDATE Drones SET flights = (SELECT MAX(id) FROM FlightLogs)")
        self.connection.commit()
