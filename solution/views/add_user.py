"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the AddUserView class which is displayed in the Main window
         when the user selects the New User button on the login frame.
Uses: N/A
"""

from tkinter import Frame, Label, Entry, Button

class AddUserView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(background="#161616")

        container = Frame(self, bd=4, bg="#003300")
        container.rowconfigure([0, 1, 2], weight=1)
        container.columnconfigure(1, weight=1)
        container.grid()

        header = Frame(container, bd=4, bg="#BEBDB8")
        header.columnconfigure(0, weight=1)
        header.rowconfigure(0, weight=1)
        header.grid(row=0, column=1, sticky="nsew")
        self.headTxt = Label(header, text="Add User Form", font="Courier 16 bold", bg="#003300", fg="#FFFFFF", pady=5)
        self.headTxt.grid(row=0, column=0, stick="nsew")
        self.instructions = Label(header, text="* All fields are required.", font="Courier 8", bg="#003300",
                                  fg="#FFFFFF", pady=2)
        self.instructions.grid(row=1, column=0, sticky="nsew")

        form = Frame(container, bd=4, bg="#BEBDB8")
        form.columnconfigure([0, 3], weight=1)
        form.rowconfigure([0, 8], weight=1)
        form.grid(row=1, column=1, sticky="nsew")

        # create text box labels
        self.username_label = Label(form, text="Username", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.username_label.grid(row=1, column=1)
        self.password_label = Label(form, text="Password", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.password_label.grid(row=2, column=1)
        self.first_name_label = Label(form, text="First Name", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.first_name_label.grid(row=3, column=1)
        self.last_name_label = Label(form, text="Last Name", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.last_name_label.grid(row=4, column=1)
        self.drone_name_label = Label(form, text="Drone Name", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.drone_name_label.grid(row=5, column=1)

        self.username = Entry(form, width=30)
        self.username.grid(row=1, column=2, padx=5, pady=10)
        self.password = Entry(form, width=30)
        self.password.grid(row=2, column=2, padx=5, pady=10)
        self.first_name = Entry(form, width=30)
        self.first_name.grid(row=3, column=2, padx=5, pady=10)
        self.last_name = Entry(form, width=30)
        self.last_name.grid(row=4, column=2, padx=5, pady=10)
        self.drone_name = Entry(form, width=30)
        self.drone_name.grid(row=5, column=2, padx=5, pady=10)

        interactions = Frame(container, bd=4, bg="#BEBDB8")
        interactions.columnconfigure([0, 3], weight=1)
        interactions.rowconfigure([0, 1], weight=1)
        interactions.grid(row=2, column=1, sticky="nsew")

        # Create submit button
        self.add_user_btn = Button(interactions, text="Submit", bg="white", width=10, font="Courier 10 bold",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.add_user_btn.grid(row=0, column=2, pady=20, padx=20)

        # Create cancel button
        self.cancel_btn = Button(interactions, text="Cancel", bg="white", width=10, font="Courier 10 bold",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.cancel_btn.grid(row=0, column=1, pady=20, padx=20)

        self.success_message_label = Label(interactions, text="", bg="#BEBDB8", fg="green", font="Courier 10 bold")
        self.success_message_label.grid(row=1, column=1, sticky="nsew")

