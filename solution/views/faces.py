"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the FacesView class which is displayed in the Main window
         when the user selects the Faces menu item.
Uses: N/A
"""

from tkinter import Frame, Label, Button

class FacesView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure([0, 2], weight=1)
        self.grid_rowconfigure([0, 2], weight=1)
        self.configure(background="#161616")

        container = Frame(self, bd=4, bg="#003300")
        container.rowconfigure([0, 1], weight=1)
        container.columnconfigure(1, weight=1)
        container.grid(column=1, row=1, sticky="nsew")

        header = Frame(container, bd=4, bg="#BEBDB8")
        header.columnconfigure(0, weight=1)
        header.rowconfigure(0, weight=1)
        header.grid(row=0, column=1, sticky="nsew")
        self.headTxt = Label(header, text="Faces", font="Courier 16 bold", bg="#003300", fg="#FFFFFF")
        self.headTxt.grid(row=0, column=0, sticky="nsew")

        image_frame = Frame(container, bd=4, pady=10, bg="#BEBDB8")
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(0, weight=1)
        image_frame.grid(row=1, column=1, sticky="ew")

        self.image_lbl = Label(image_frame, bg="#BEBDB8")
        self.image_lbl.grid(row=0, column=1, pady=10, padx=20)

        self.filename_lbl = Label(image_frame, width=40, height=1, bg="#BEBDB8")
        self.filename_lbl.grid(row=1, column=1)

        inputs = Frame(container, bg="#414141")
        inputs.columnconfigure([0, 3], weight=1)
        inputs.rowconfigure(0, weight=1)
        inputs.grid(row=2, column=1, sticky="nsew")

        self.open_btn = Button(inputs, text="Open", width=7, bg="white", font="Courier 10 bold",
                               fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.open_btn.grid(row=5, column=1, padx=20, pady=5)

        self.new_btn = Button(inputs, text="New", width=7, bg="white", font="Courier 10 bold",
                              fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.new_btn.grid(row=5, column=2, padx=20, pady=5)

        self.close_btn = Button(inputs, text="Close", width=7, bg="white", font="Courier 10 bold",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove")
        self.close_btn.grid(row=6, column=1, columnspan=2, pady=5)
