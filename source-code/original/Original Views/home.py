"""
Author: Jacob Pitsenberger
Program: Management UI
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the HomeView class which is displayed in the Main window on valid login.
Uses: N/A
"""

from tkinter import Frame, Label, Button

class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew")

        header = Frame(self, bg="#414141")
        header.columnconfigure([0, 7], weight=1)
        header.rowconfigure(0, weight=1)
        header.grid(row=0, column=0, sticky="nsew")

        self.head_txt = Label(header, text="Drone Controller Data Management System", font="Courier 24 bold",
                              bg="#242424", fg="green", height=4)
        self.head_txt.grid(row=0, column=0, columnspan=8, sticky="ew")

        self.controller_btn = Button(header, text="Drone Controller", width="20", font="Courier 10 bold",
                                     fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                     relief="groove")
        self.controller_btn.grid(row=1, column=1, padx=10, pady=10)

        self.mapping_btn = Button(header, text="Mapping Controller", width="20", font="Courier 10 bold",
                                     fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                     relief="groove")
        self.mapping_btn.grid(row=1, column=2, padx=10, pady=10)

        self.logs_btn = Button(header, text="Logs", width="20", font="Courier 10 bold",
                               fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                               relief="groove")
        self.logs_btn.grid(row=1, column=3, padx=10, pady=10)

        self.faces_btn = Button(header, text="Faces", width="20", font="Courier 10 bold",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                relief="groove")
        self.faces_btn.grid(row=1, column=4, padx=10, pady=10)

        self.objects_btn = Button(header, text="Objects", width="20", font="Courier 10 bold",
                                  fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                  relief="groove")
        self.objects_btn.grid(row=1, column=5, padx=10, pady=10)

        self.logout_btn = Button(header, text="Logout", width="20", font="Courier 10 bold",
                                 fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                 relief="groove")
        self.logout_btn.grid(row=1, column=6, padx=10, pady=10)

        info = Frame(self, bd=4, bg="#161616")
        info.columnconfigure([0, 2], weight=1)
        info.rowconfigure([0, 6], weight=1)
        info.grid(row=1, sticky="nsew")
        self.welcome_lbl = Label(info, width="100", height="5", text="welcome to the drone controller application.",
                                 font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.welcome_lbl.grid(row=1, column=1)
        self.pic_lbl = Label(info, width="100", height="2", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.pic_lbl.grid(row=2, column=1)
        self.drone_lbl = Label(info, width="100", height="2", font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.drone_lbl.grid(row=3, column=1)
        self.sdk_lbl = Label(info, width="100", height="2", text="SDK: 3.0",
                             font="Courier 10 bold", fg="#003300", bg="#BEBDB8")
        self.sdk_lbl.grid(row=4, column=1)
