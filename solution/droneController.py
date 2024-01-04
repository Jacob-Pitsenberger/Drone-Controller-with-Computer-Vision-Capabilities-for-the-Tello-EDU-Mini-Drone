"""
Author: Jacob Pitsenberger
Program: Drone Controller
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the GUI class and executes the main loop for the droneController program.
         This class returns and instance of the GUI to be run as the tkinter main loop which is called in
         the python main loop found in this module by calling the GUI classes run application method after
         initializing an instance of it.
Uses: flight_commands.py module, faces.py, objects.py, and logs.py model modules
"""

import os
import cv2
from datetime import date, datetime
import time
import threading
import face_recognition
import numpy as np
from djitellopy import tello
from tkinter import *
from PIL import Image, ImageTk
from models.logs import Logs
from models.faces import Faces
from models.objects import Objects
from flight_commands import start_flying, stop_flying

current_time = datetime.now()

# noinspection PyRedundantParentheses
class GUI():
    def __init__(self):
        """       -Adapted From-
            Title: flydo - app.py
            Author: Charles Yuan
            Date: 1-7-22
            Code Version: N/A
            Availability: https://github.com/Chubbyman2/flydo/blob/main/commands.py
        """
        # Initialize the root window and set its state to fill the screen (JP)
        self.root = Tk()
        self.root.configure(background="#161616")
        self.root.title("Drone Controller with Computer Vision Capabilities for the Tello EDU Mini Drone")
        self.root.state('zoomed')

        # Connect to the drone and start receiving video (JP)
        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamon()

        # set the default speed for the drone
        self.drone.speed = 50

        # Initialize the logs model
        self.log = Logs()

        # Initialize the faces model
        self.faces = Faces()

        # Initialize the Objects model
        self.objects = Objects()

        # Get the battery level on connection
        self.start_battery = self.drone.get_battery()

        # Set the start time to the current time
        self.start_time = current_time.strftime("%H:%M:%S")

        # Drones fly state for takeoff/land button functionality
        self.flying = False

        # Initialize the cameras state for taking videos
        self.recording = False
        self.recorder = threading.Thread(target=self.take_video)

        # Initialize the state of the image for the video stream
        self.image = None

        # Initialize a variable to get the video frames from the drone
        self.frame = self.drone.get_frame_read()

    def takeoff_land(self):
        """
            Title: flydo - app.py
            Author: Charles Yuan
            Date: 1-7-22
            Code Version: N/A
            Availability: https://github.com/Chubbyman2/flydo/blob/main/commands.py
        """

        # Set the command for the takeoff/land button depending on the drones flying state
        if self.flying:
            threading.Thread(target=lambda: self.drone.land()).start()
            self.flying = False
        else:
            threading.Thread(target=lambda: self.drone.takeoff()).start()
            self.flying = True

    def take_picture(self):
        """Get the current frame then check if the pictures directory exists and if not create it.
        After this use imwrite to save the current frame to the images directory with the file name being
        the time the picture was taken"""
        frame = self.frame.frame
        if not os.path.exists("D:\\Project\\data-files\\output-files\\pictures"):
            os.mkdir("D:\\Project\\data-files\\pictures")
        # must save image with different name each time or will overwrite previous.
        # Simplest way is to use the time since this will always be different.
        cv2.imwrite(f"D:\\Project\\data-files\\output-files\\pictures/{time.time()}.png", frame)
        print("image saved")
        # Delay to limit the number of images saved per press to only one img
        time.sleep(0.3)

    def take_video(self):
        """Takes video for the duration of the flight by constantly getting the current frame read and writing
        it to a video file when the record button has been pressed"""
        self.vid_btn.config(relief="sunken", bg="red", fg="#FFFFFF")
        self.recording = True
        h, w = self.frame.frame.shape[:-1]
        video = cv2.VideoWriter(f"D:\\Project\\data-files\\output-files\\videos/{time.time()}.avi",
                                cv2.VideoWriter_fourcc(*'XVID'), 30, (w, h))
        while self.recording:
            video.write(self.frame.frame)
            time.sleep(1 / 30)
        video.release()

    def end_flight(self):
        """ Run the add_log method, delete the drone object and close the root window ending all processes"""
        self.add_log()
        del self.drone
        self.root.quit()

    def add_log(self) -> None:
        """Update the flight logs table whenever the users ends a flight"""
        flightDate = date.today()
        startBattery = self.start_battery
        endBattery = self.drone.get_battery()
        startTime = self.start_time
        time_now = datetime.now()
        endTime = time_now.strftime("%H:%M:%S")
        motorTime = self.drone.get_flight_time()
        self.log.add_log(flightDate, startTime, endTime, startBattery, endBattery, motorTime)

    def updateSpeed(self):
        """Set the drones default speed to the value in the speed scale bar"""
        self.drone.speed = self.speed_bar.get()
        print(f'reset distance to {self.speed:.1f}')

    def run_app(self):
        """       -Adapted From-
            Title: flydo - app.py
            Author: Charles Yuan
            Date: 1-7-22
            Code Version: N/A
            Availability: https://github.com/Chubbyman2/flydo/blob/main/commands.py
        """
        """
        Add all widgets to the GUI and bind all button and key presses to commands methods of this class
        """

        # Create a button to send takeoff and land commands to the drone
        takeoff_land_button = Button(self.root, text="Takeoff/Land", font=("Courier", 14, "bold"), bg="white",
                                     fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                     relief="groove", width=15, command=lambda: self.takeoff_land())
        takeoff_land_button.place(relx=0.95, rely=0.7, anchor="e")

        # Create a button to end close the program and log all events
        end_flight_btn = Button(self.root, text="End Flight", font=("Courier", 14, "bold"), bg="white",
                                fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                relief="groove", width=15, command=lambda: self.end_flight())
        end_flight_btn.place(relx=0.95, rely=0.8, anchor="e")

        # Create a button to recognize a face in the frame
        recognize_face_btn = Button(self.root, text="Recognize Face", font=("Courier", 10, "bold"), bg="white",
                                    fg="#003300", activebackground="green", activeforeground="#FFFFFF", relief="groove",
                                    width=20, command=lambda: self.recognizeFace())
        recognize_face_btn.place(relx=0.95, rely=0.3, anchor="e")

        # Create a button to recognize a face in the frame
        recognize_object_btn = Button(self.root, text="Recognize Object", font=("Courier", 10, "bold"), bg="white",
                                      fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                      relief="groove", width=20, command=lambda: self.recognizeObject())
        recognize_object_btn.place(relx=0.95, rely=0.45, anchor="e")

        # binding arrow keys to flight commands
        self.tmp_f = Frame(self.root, bg="#161616")
        self.tmp_f.bind('<KeyPress-w>', lambda event: start_flying(event, "upward", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-w>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-s>', lambda event: start_flying(event, "downward", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-s>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-a>', lambda event: start_flying(event, "yaw_left", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-a>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-d>', lambda event: start_flying(event, "yaw_right", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-d>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-Up>', lambda event: start_flying(event, "forward", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-Up>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-Down>', lambda event: start_flying(event, "backward", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-Down>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-Left>', lambda event: start_flying(event, "left", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-Left>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.bind('<KeyPress-Right>', lambda event: start_flying(event, "right", self.drone, self.drone.speed))
        self.tmp_f.bind('<KeyRelease-Right>', lambda event: stop_flying(event, self.drone))
        self.tmp_f.pack()
        # Make frame for key press events active until execution of the program
        self.tmp_f.focus_set()

        # Create a button to take pictures
        pic_btn = Button(self.root, text="pic.", font=("Courier", 10, "bold"), bg="white", fg="blue",
                         activebackground="blue", activeforeground="#FFFFFF", relief="groove",
                         width=7, height=2, command=lambda: self.take_picture())
        pic_btn.place(relx=0.55, rely=0.9, anchor="center")

        # Create a button to take videos for the duration of the flight
        self.vid_btn = Button(self.root, text="rec.", font=("Courier", 10, "bold"), bg="white", fg="red",
                              activebackground="red", activeforeground="#FFFFFF", relief="groove",
                              width=7, height=2, command=lambda: self.recorder.start())
        self.vid_btn.place(relx=0.45, rely=0.9, anchor="center")

        # Create a label to show the video stream
        self.cap_lbl = Label(self.root)
        self.cap_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Create a label to show the count of faces in frame
        self.face_count_lbl = Label(self.root, width=30, bg="gray")
        self.face_count_lbl.place(relx=0.95, rely=0.18, anchor="e")

        # Create a label to show the name of faces recognized
        self.face_recognized_lbl = Label(self.root, width=30, bg="red")
        self.face_recognized_lbl.place(relx=0.95, rely=0.25, anchor="e")

        # Create a label to show the name of object recognized
        self.object_recognized_lbl = Label(self.root, width=30, bg="green")
        self.object_recognized_lbl.place(relx=0.95, rely=0.4, anchor="e")

        # Add the video stream to the window
        self.video_stream()

        # Add and configure the frame for the control help image
        control_info = Frame(self.root, bd=4, bg="#161616")
        control_info.place(relx=0.04, rely=0.15, anchor="nw", width=200)

        control_info_header = Label(control_info, text="Keyboard Controls", font=("Courier", 14, "bold"), bg="#006400")
        control_info_header.pack()

        # Create an object of tkinter ImageTk to open the control help image
        control_info_img = ImageTk.PhotoImage(Image.open("D:\Project\data-files\input-files\controls.png"))

        # Create a Label Widget to display the control help Image and add the image for this
        control_info_lbl = Label(control_info, padx=10, bg="#161616")
        control_info_lbl.pack()
        control_info_lbl.img = control_info_img
        control_info_lbl.configure(image=control_info_img)

        # Add the scale bar to set the speed the drone fly's at
        self.speed_bar = Scale(self.root, from_=25, to=100, length=150, tickinterval=25,
                               digits=3, label='Drone Flight Speed:',
                               resolution=25, showvalue=False, orient="horizontal", font=("Courier", 10, "bold"),
                               bg="white", fg="#003300", activebackground="green", relief="groove")
        self.speed_bar.set(50)
        self.speed_bar.place(relx=0.055, rely=0.7, anchor="nw")

        # Add a button to reset the speed according to the scale bars value
        self.set_speed_btn = Button(self.root, text='Reset Speed', font=("Courier", 10, "bold"), bg="white",
                                    fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                    relief="groove", command=self.updateSpeed, )
        self.set_speed_btn.place(relx=0.075, rely=0.8, anchor="nw")

        # Start the tkinter main loop
        self.root.mainloop()

    def countFaces(self, img):
        """       -Adapted From-
            Title: Drone Programming With Python Course | 3 Hours | Including x4 Projects | Computer Vision
            Author: Murtaza's Workshop - Robotics and AI
            Date: 1-1-21
            Code Version: N/A
            Availability: https://www.youtube.com/watch?v=LmEcyQnfpDA&t=6736s
        """
        """This program counts the number of faces detected in the drones camera stream and writes this count
            on the face count label in the GUI."""

        # Create a cascade
        faceCascade = cv2.CascadeClassifier("D:\Project\data-files\input-files\haarcascade_frontalface_default.xml")
        # covert to grayscale
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # pass in grayscale image, scale factor, and minimum neighbors
        faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

        # create list to hold the number of faces detected in the current frame
        faceList = []

        # If any faces are detected append them to the list
        for face in faces:
            faceList.append(face)

        # Update the face count label with the number of faces detected
        face_count = "Faces: " + str(len(faceList))
        self.face_count_lbl.config(text=face_count)

    def recognizeFace(self):
        """
            -Adapted From-
        Title: FACE RECOGNITION + ATTENDANCE PROJECT | OpenCV Python | Computer Vision
        Author: Murtaza's Workshop - Robotics and AI
        Date: 6-11-20
        Code Version: N/A
        Availability: https://www.youtube.com/watch?v=sz25xxF_AVE&t=957s
        """
        """This program is used to recognize faces in the drones camera feed if a image file exists for that 
        face in the faces directory. If a face is recognized the face recognized label on the GUI is updated
        to display the faces filename. """

        # Get the most recent frame
        frame = self.frame.frame

        # reduce size of image to speed up process since doing in real time
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)

        # convert to grayscale
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Find the location of faces then send to encoding fxn
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        # Before checking if the face matches set the label to "unknown" so that if no match this shows
        self.face_recognized_lbl.config(text="unknown")

        # Find the matches by iterating through faces in current frame and comparing them the face models
        # list of face encodings
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.faces.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(self.faces.encodeListKnown, encodeFace)

            # set the matched index according to the lowest Distance between comparisons as this is the best match
            matchIndex = np.argmin(faceDis)

            # if a match is found set the text for the label to be equal to that faces name
            if matches[matchIndex]:
                name = self.faces.classNames[matchIndex].upper()
                self.face_recognized_lbl.config(text=name)

    def recognizeObject(self):
        """
            -Adapted From-
        Title: Feature Detection and Matching + Image Classifier Project | OPENCV PYTHON
        Author: Murtaza's Workshop - Robotics and AI
        Date: 6-16-20
        Code Version: N/A
        Availability: https://www.youtube.com/watch?v=nnH55-zD38I
        """
        """This program is used to recognize objects in the drones camera feed if a image file exists for that 
        object in the objects directory. If an object is recognized the object recognized label on the GUI 
        is updated to display the objects filename. """

        # Create orb
        orb = cv2.ORB_create(nfeatures=1000)

        # get the most recent frame
        frame = self.frame.frame

        # get known descriptors
        desList = self.objects.descriptors

        # Define the minimum threshold value for a good match
        thres = 15

        # Before checking if the object matches set the label to "unknown" so that if no match this shows
        self.object_recognized_lbl.config(text="unknown")

        # get the descriptors for the current frame
        kp2, des2 = orb.detectAndCompute(frame, None)

        # Must check that descriptors were found in the current frame
        # If not errors are returned...
        if des2 is None:
            return False

        # Create a brute force matcher
        bf = cv2.BFMatcher()

        # Create a list to hold good matches
        matchList = []

        # If a match isn't found later, then this will be set as the objects id
        # If an objects id is one this indicates that no objects were recognized
        finalVal = -1

        # Loop through known descriptors and match to ID's one by one to get k best matches
        # Need try/except in case of error
        try:
            for des in desList:

                # Use brute force knnMatch to get the matches
                matches = bf.knnMatch(des, des2, k=2)

                # List for good matches
                good = []

                # loop through matches and distances between features
                for m, n in matches:

                    # apply ratio test to get good matches and append them to the good list
                    if m.distance < 0.75 * n.distance:
                        good.append([m])

                # Append good matches to list so that they can be accessed by their index
                matchList.append(len(good))
        except:
            pass

        # Check whether list is empty or not
        if len(matchList) != 0:
            # if the best match is greater than the threshold defined for a good match then this is the
            # index for a good match
            if max(matchList) > thres:
                # Set this index as the good match
                finalVal = matchList.index(max(matchList))

        # Set the object id to the good match index
        objectID = finalVal

        # if this isn't -1 then it is a good matches index in the list
        if objectID != -1:
            # Set the object name to this objects class name getting with it id value
            objectName = self.objects.classNames[objectID]

            # Write the object name to the object recognized label
            self.object_recognized_lbl.config(text=objectName)

    def video_stream(self):
        """       -Adapted From-
            Title: flydo - app.py
            Author: Charles Yuan
            Date: 1-7-22
            Code Version: N/A
            Availability: https://github.com/Chubbyman2/flydo/blob/main/commands.py
        """
        # Define the height and width to resize the current frame to
        h = 480
        w = 720

        # Get the current frame
        frame = self.frame.frame

        # Must have an input frame and a return frame. To do this with Tkinter must define both as single
        # variable is determined as input or returned by checking if the initial class variable has changed state
        # So, if the initial state for the video stream has changed then set the frame to this resized
        if self.image is not None:
            frame = cv2.resize(self.image, (w, h))
        # Else set the frame to itself resized
        else:
            frame = cv2.resize(frame, (w, h))

        # Convert the current frame to grayscale
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Convert this to a Pillow image
        img = Image.fromarray(cv2image)

        # Convert this then to a Tkinter compatible photo image
        imgtk = ImageTk.PhotoImage(image=img)

        # place the image label
        self.cap_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Set it to the photo image
        self.cap_lbl.imgtk = imgtk

        # configure the photo image as the displayed image
        self.cap_lbl.configure(image=imgtk)

        # Update the face count each time video stream label is updated with current frame
        self.countFaces(frame)

        # Update the video stream label with the current frame by calling the method itself with a delay
        self.cap_lbl.after(5, self.video_stream)


if __name__ == "__main__":

    # Initialize the GUI
    gui = GUI()

    # Call the run_app method to run tkinter mainloop
    gui.run_app()