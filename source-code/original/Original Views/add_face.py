"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the AddFaceView class which is displayed in the Main window
         when the user selects the new button on the faces frame.
Uses: N/A
"""

from tkinter import Frame, Label, Button, Entry


class AddFaceView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure([0, 2], weight=1)
        self.grid_rowconfigure([0, 2], weight=1)
        self.configure(background="#161616")

        container = Frame(self, bd=4, bg="#003300")
        container.columnconfigure(1, weight=1)
        container.grid(column=1, row=1, sticky="nsew")

        header = Frame(container, bd=4, bg="#BEBDB8")
        header.columnconfigure(0, weight=1)
        header.rowconfigure(0, weight=1)
        header.grid(row=0, column=1, sticky="nsew")
        self.headTxt = Label(header, text="Add Face", font="Courier 16 bold", bg="#003300", fg="#FFFFFF")
        self.headTxt.grid(row=0, column=0, sticky="nsew")

        form = Frame(container, bd=4, bg="#BEBDB8")
        form.columnconfigure([0, 4], weight=1)
        form.rowconfigure([0, 4], weight=1)
        form.grid(row=1, column=1, sticky="nsew")

        # create text box labels
        self.first_name_label = Label(form, text="First Name:", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.first_name_label.grid(row=1, column=1, pady=15)
        self.last_name_label = Label(form, text="Last Name:", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.last_name_label.grid(row=2, column=1, pady=15)

        self.first_name = Entry(form, width=30)
        self.first_name.grid(row=1, column=2, padx=5, sticky="ew")
        self.last_name = Entry(form, width=30)
        self.last_name.grid(row=2, column=2, padx=5, sticky="ew")

        self.img_lbl = Label(form, text="Image:", bg="#BEBDB8")
        self.img_lbl.grid(row=3, column=1, pady=15)
        self.img_path_lbl = Label(form, bg="#BEBDB8")
        self.img_path_lbl.grid(row=3, column=2, pady=15)
        self.search_btn = Button(form, text="Search", width=5, bg="white", font="Courier 10 bold",
                                 fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.search_btn.grid(row=3, column=3, pady=5, padx=10)

        self.success_lbl = Label(form, bg="#BEBDB8")
        self.success_lbl.grid(row=4, column=2)

        inputs = Frame(container, bg="#414141")
        inputs.columnconfigure([0, 3], weight=1)
        inputs.grid(row=2, column=1, sticky="nsew")

        self.add_btn = Button(inputs, text="Add", width=7, bg="white", font="Courier 10 bold",
                              fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.add_btn.grid(row=0, column=1, padx=10, pady=15)

        self.close_btn = Button(inputs, text="Close", width=7, bg="white", font="Courier 10 bold",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.close_btn.grid(row=0, column=2, padx=10, pady=15)
