"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the LoginView class which is displayed in the main window on program start.
Uses: N/A
"""

from tkinter import Frame, Label, Entry, Button

class LoginView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure([0,2], weight=1)
        self.grid_rowconfigure([0, 2], weight=1)
        self.configure(background="#161616")

        container = Frame(self, bd=4, bg="#003300", width=500, height=500)
        container.rowconfigure([0, 1], weight=1)
        container.columnconfigure(1, weight=1)
        container.grid(column=1, row=1, sticky="nsew")

        header = Frame(container, bd=4, bg="#BEBDB8")
        header.columnconfigure(0, weight=1)
        header.rowconfigure(0, weight=1)
        header.grid(row=0, column=1, sticky="nsew")
        self.headTxt = Label(header, text="Login", font="Courier 16 bold", bg="#003300", fg="#FFFFFF")
        self.headTxt.grid(row=0, column=0, sticky="nsew")

        form = Frame(container, bd=4, bg="#BEBDB8")
        form.columnconfigure([0, 3], weight=1)
        form.rowconfigure([0, 7], weight=1)
        form.grid(row=1, column=1,sticky="nsew")

        # create text box labels
        self.username_label = Label(form, text="Username", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.username_label.grid(row=1, column=1)
        self.password_label = Label(form, text="Password", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.password_label.grid(row=2, column=1)

        self.username = Entry(form, width=30)
        self.username.grid(row=1, column=2, padx=10, pady=15)
        self.password = Entry(form, width=30, show="*")
        self.password.grid(row=2, column=2, padx=10, pady=15)

        interactions = Frame(container, bd=4, bg="#BEBDB8")
        interactions.columnconfigure([0, 3], weight=1)
        interactions.rowconfigure(0, weight=1)
        interactions.grid(row=2, column=1, sticky="nsew")

        # Create login button
        self.login_btn = Button(interactions, text="Login", bg="white", width=10, font="Courier 10 bold",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.login_btn.grid(row=5, column=2, padx=20, pady=15, sticky="w")

        # Create cancel button
        self.new_user_btn = Button(interactions, text="New User", width=10, bg="white", font="Courier 10 bold",
                                   fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.new_user_btn.grid(row=5, column=1, padx=20, pady=15, sticky="w")

        # Create invalid login label
        self.invalid_lbl = Label(interactions, bg="#BEBDB8", fg="red", font="Courier 10 bold")
        self.invalid_lbl.grid(row=6, column=1, columnspan=2)
