"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the FlightLogsView class which is displayed in the Main window
         when the user selects the logs menu item
Uses: N/A
"""

from tkinter import Frame, Label, ttk, Button, Scrollbar

class FlightLogsView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rowconfigure([0, 2], weight=1)
        self.columnconfigure([0, 2], weight=1)
        self.configure(background="#161616")

        container = Label(self, bg="black")
        container.grid(row=1, column=1)

        logs_header = Label(container, text="Flight Logs", font=("Courier", 16, "bold"), bg="black", fg="green",
                            width="50", pady=5)
        logs_header.grid(row=1, column=1)

        # Add style
        style = ttk.Style()

        # pick a theme - not all support field background
        style.theme_use("default")

        # configure the style options for the cells
        style.configure("Treeview",
                        background="gray",
                        rowheight=30,
                        fieldbackground="gray",
                        font=("Courier", 10, "bold")
                        )

        # change the color when row is selected and map the style
        style.map('Treeview',
                  background=[('selected', 'green')])

        # create treeview frame to add scrollbar
        scroll_frame = Frame(container)
        scroll_frame.grid(row=2, column=1)

        # create scrollbar
        scroll = Scrollbar(scroll_frame)
        scroll.pack(side="right", fill="y")

        # Create tree view
        self.log_tree = ttk.Treeview(scroll_frame, yscrollcommand=scroll.set)

        # Define main columns
        self.log_tree['columns'] = ("id", "flightDate", "startTime", "endTime", "startBattery", "endBattery", "motorTime")

        # format the columns
        self.log_tree.column("#0", width=0, stretch="no")

        # Create the columns
        self.log_tree.column("id", anchor="center", width=25)
        self.log_tree.column("flightDate", anchor="center", width=100)
        self.log_tree.column("startTime", anchor="center", width=100)
        self.log_tree.column("endTime", anchor="center", width=100)
        self.log_tree.column("startBattery", anchor="center", width=100)
        self.log_tree.column("endBattery", anchor="center", width=100)
        self.log_tree.column("motorTime", anchor="center", width=120)

        # Create the column headings
        self.log_tree.heading("#0", text="", anchor="center")
        self.log_tree.heading("id", text="ID", anchor="center")
        self.log_tree.heading("flightDate", text="Date", anchor="center")
        self.log_tree.heading("startTime", text="Start Time", anchor="center")
        self.log_tree.heading("endTime", text="End Time", anchor="center")
        self.log_tree.heading("startBattery", text="Start Battery", anchor="center")
        self.log_tree.heading("endBattery", text="End Battery", anchor="center")
        self.log_tree.heading("motorTime", text="Motor Run Time", anchor="center")

        # pack to the screen
        self.log_tree.pack()
        scroll.config(command=self.log_tree.yview)

        # button to switch to home frame
        self.close_btn = Button(container, text="Close", font=("Courier", 10, "bold"), width=10, bd=2)
        self.close_btn.grid(row=3, column=1)
