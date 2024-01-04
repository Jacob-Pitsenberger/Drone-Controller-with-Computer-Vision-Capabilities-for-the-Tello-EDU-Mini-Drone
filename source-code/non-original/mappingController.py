"""
Author: Jacob Pitsenberger
Program: Mapping Controller
Version: 1.0
Project: Drone Controller with Computer Vision Capabilities
Course: CPSC-4900-01_23SP: Senior Project and Seminar_2023SP
Date: 4/28/2023
Purpose: This module contains the MappingUI class and executes the main loop for the mappingController program.
         This class takes the drone object as its parameter and returns and instance of the GUI to be run
         as the tkinter main loop which is called in the main function in this module.
Uses: tello.py module
"""

import turtle
from tkinter import Tk, Scale, Canvas, Button, Frame, Label
import threading
import time
import tello

from PIL import ImageGrab


class MappingUI(object):
    """       -Adapted From-
    Title: Python, Manual Control
    Author: One-Off Coder
    Date: 3-5-23
    Code Version: N/A
    Availability: https://tello.oneoffcoder.com/python-manual-control.html
    """

    def __init__(self, tello):

        # initialize the drone
        self.tello = tello

        # initialize the thread of the Tkinter mainloop and set it to None
        self.thread = None

        # initialize the stop event and set it to None
        self.stopEvent = None

        # Initialize the flag to stop the program from waiting for responses from the drone
        # Set to false makes the program wait for responses from the drone until True
        self.quit_waiting_flag = False

        # Initialize the default distance for 'move' cmd
        self.distance = 0.2
        # Initialize the default degree for 'cw' or 'ccw' cmd
        self.degree = 90

        # Initialize the Starting coordinates
        self.x = 0
        self.y = 0

        # Initialize the root window
        self.root = Tk()
        self.root.configure(background="#161616")
        self.root.state('zoomed')

        # Initialize the turtle and turtle canvas
        self.map_screen = Canvas(self.root, width=700, height=600)
        self.turtle_screen = turtle.TurtleScreen(self.map_screen)
        self.mapper = turtle.RawTurtle(self.turtle_screen)
        self.mapper.color("green")

        # Set the drone default heading to north
        self.mapper.setheading(90)

        # Initialize the stop event
        self.stopEvent = threading.Event()

        # set a callback for when the root window is closed
        self.root.wm_title('Drone Mapping Controller')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        # Initialize the thread for sending commands to the drone
        # set its target to the _sendingCommand method of this class
        self.sending_command_thread = threading.Thread(target=self._sendingCommand)

        # Call this classes run application method
        self.runApp()

    def _sendingCommand(self):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """

        """
        Starts a while loop that sends 'command' to tello every 5 second.

        :return: None
        """

        while True:
            self.tello.send_command('command')
            time.sleep(5)

    def _setQuitWaitingFlag(self):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        """
        Set the variable as TRUE; it will stop computer waiting for response from tello.

        :return: None
        """
        self.quit_waiting_flag = True

    def runApp(self):
        """
        Add all widgets to the GUI and bind all button and key presses to commands methods of this class
        """

        # Add the turtle canvas and write the starting coordinates
        self.map_screen.place(relx=0.5, rely=0.45, anchor="center")
        self.mapper.write("(" + str(self.x) + ", " + str(self.y) + ")")

        # Add the button for writing coordinates on canvas
        self.writeCoords = Button(self.root, text='Write Point', font=("Courier", 14, "bold"), bg="#BEBDB8",
                                  fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                  relief="groove", width=15, command=self.writeCoordinates)
        self.writeCoords.place(relx=0.4, rely=0.92, anchor="center")

        # Add the button to save the map to the maps directory
        self.completeMap = Button(self.root, text='Save Map', font=("Courier", 14, "bold"), bg="#BEBDB8",
                                  fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                  relief="groove", width=15, command=self.saveMap)
        self.completeMap.place(relx=0.6, rely=0.92, anchor="center")

        # Add the instructions image
        instructions = Label(self.root, text='Arrow Up - Move Tello Forward\n\n'
                                             'W - Move Tello Up\n\n'
                                             'S - Move Tello Down\n\n'
                                             'A - Rotate Tello CCW 90 degrees\n\n'
                                             'D - Rotate Tello CW 90 degrees\n\n\n'
                                             'Write Point Button - \n'
                                             '     Put point with current\n '
                                             '     position on the map.\n\n'
                                             'Save Map Button - \n'
                                             '     Save the current map\n'
                                             '     to the Maps directory\n\n'
                                             'Reset the distance - \n'
                                             '     Adjust the scale bar and\n'
                                             '     press the reset button\n'
                                             '     to change the distance\n'
                                             '     moved for each key press.', justify="left",
                             font=("Courier", 10, "bold"), bg="#787775", fg="#003300")

        instructions.place(relx=0.12, rely=0.5, anchor="center")

        # Add the landing button
        self.btn_landing = Button(self.root, text='Land', font=("Courier", 14, "bold"), bg="#BEBDB8",
                                  fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                  relief="groove", width=15, command=self.telloLanding)
        self.btn_landing.place(relx=0.88, rely=0.75, anchor="center")

        # Add the takeoff button
        self.btn_takeoff = Button(self.root, text='Takeoff', font=("Courier", 14, "bold"), bg="#BEBDB8",
                                  fg="#003300",
                                  activebackground="green", activeforeground="#FFFFFF", relief="groove", width=15,
                                  command=self.telloTakeOff)
        self.btn_takeoff.place(relx=0.88, rely=0.85, anchor="center")

        # bind arrow keys to drone control
        self.tmp_f = Frame(self.root, width=100, height=2, bg="#161616")
        self.tmp_f.bind('<KeyPress-w>', self.on_keypress_w)
        self.tmp_f.bind('<KeyPress-s>', self.on_keypress_s)
        self.tmp_f.bind('<KeyPress-a>', self.on_keypress_a)
        self.tmp_f.bind('<KeyPress-d>', self.on_keypress_d)
        self.tmp_f.bind('<KeyPress-Up>', self.on_keypress_up)
        self.tmp_f.pack(side='bottom')
        self.tmp_f.focus_set()

        # Add the default movement distance scale bar
        self.distance_bar = Scale(self.root, from_=0.2, to=1, tickinterval=0.2,
                                  digits=3, label='Distance(m)',
                                  resolution=0.2, length=200, orient="horizontal", showvalue=False,
                                  font=("Courier", 10, "bold"), bg="#BEBDB8", fg="#003300", activebackground="green",
                                  relief="groove")
        self.distance_bar.set(0.2)
        self.distance_bar.place(relx=0.88, rely=0.3, anchor="center")

        # Add the button to reset the default movement distance to the value in the scale bar
        self.btn_distance = Button(self.root, text='Reset Distance', font=("Courier", 10, "bold"), bg="#BEBDB8",
                                   fg="#003300", activebackground="green", activeforeground="#FFFFFF",
                                   relief="groove", command=self.updateDistancebar)
        self.btn_distance.place(relx=0.88, rely=0.4, anchor="center")

    def telloTakeOff(self):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the takeoff command to the drone
        return self.tello.takeoff()

    def telloLanding(self):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the land command to the drone
        return self.tello.land()

    def telloCW(self, degree):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the rotate_cw command to the drone
        return self.tello.rotate_cw(degree)

    def telloCCW(self, degree):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the rotate_ccw command to the drone
        return self.tello.rotate_ccw(degree)

    def telloMoveForward(self, distance):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the move_forward command to the drone
        return self.tello.move_forward(distance)

    def telloUp(self, dist):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the move_up command to the drone
        return self.tello.move_up(dist)

    def telloDown(self, dist):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the move_down command to the drone
        return self.tello.move_down(dist)

    def updateDistancebar(self):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Update the default movement distance to the value in the distance bar.
        self.distance = self.distance_bar.get()

    def updateCoordinates(self, distance):
        """
        Take the distance moved by the drone, determine the direction moved by checking the current
        heading, and then update the x or y coordinate by adding the distance moved to the current
        x or y value.
        """
        if self.mapper.heading() == 90:
            self.y += distance
        elif self.mapper.heading() == 0:
            self.x += distance
        elif self.mapper.heading() == 180:
            self.x -= distance
        elif self.mapper.heading() == 270:
            self.y -= distance

    def writeCoordinates(self):
        """
        Write the current x, y coordinates on the map canvas
        """
        self.mapper.write("(" + str(self.x) + ", " + str(self.y) + ")")

    def saveMap(self):
        """     -Adapted From-
        Title: How can I convert canvas content to an image? (stack overflow thread)
        Author: B.Jenkins
        Date: 7-28-16
        Code Version: N/A
        Availability: https://stackoverflow.com/questions/9886274/how-can-i-convert-canvas-content-to-an-image
        """
        x = self.root.winfo_rootx() + self.map_screen.winfo_x()
        y = self.root.winfo_rooty() + self.map_screen.winfo_y()
        x1 = x + self.map_screen.winfo_width()
        y1 = y + self.map_screen.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(f"D:\\Project\\data-files\\output-files\\Maps/{time.time()}.png")

    def on_keypress_w(self, event):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the telloUp command to the drone
        self.telloUp(self.distance)

    def on_keypress_s(self, event):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the telloDown command to the drone
        self.telloDown(self.distance)

    def on_keypress_a(self, event):
        """     -Adapted From-
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the rotate_ccw command to the drone
        self.tello.rotate_ccw(self.degree)

        # Get the mappers current heading direction
        current_heading = self.mapper.heading()

        # If the current heading is South then can't add 90 degrees because this will produce invalid heading value
        # So, reset it to 0 indicating direction is East
        if current_heading == 270:
            self.mapper.setheading(0)
        # Else add 90 degrees to the current heading value
        else:
            self.mapper.setheading(current_heading + 90)

    def on_keypress_d(self, event):
        """     -Adapted From-
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the rotate_cw command to the drone
        self.tello.rotate_cw(self.degree)

        # Get the mappers current heading direction
        current_heading = self.mapper.heading()

        # If the current heading is East then can't subtract 90 degrees because this will produce invalid heading value
        # So, reset it to 270 indicating direction is South
        if current_heading == 0:
            self.mapper.setheading(270)
        # Else subtract 90 degrees from the current heading value
        else:
            self.mapper.setheading(current_heading - 90)

    def on_keypress_up(self, event):
        """     -Adapted From-
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        # Send the moveForward command to the drone passing the default movement distance value
        self.telloMoveForward(self.distance)

        # Move the mapper forward the same distance multiplied by a scale value
        # which is used to make lines long enough to be visible on the map canvas
        self.mapper.forward(self.distance * 60)

        # Update the current position of the drone/mapper
        self.updateCoordinates(self.distance)

    def on_close(self):
        """
        Title: Python, Manual Control
        Author: One-Off Coder
        Date: 3-5-23
        Code Version: N/A
        Availability: https://tello.oneoffcoder.com/python-manual-control.html
        """
        """
        Sets the stop event, cleanup the camera, and allow the rest of
        the quit process to continue.
        :return: None
        """
        self.stopEvent.set()
        del self.tello
        self.root.quit()


if __name__ == "__main__":
    """     -Adapted From-
    Title: Python, Manual Control
    Author: One-Off Coder
    Date: 3-5-23
    Code Version: N/A
    Availability: https://tello.oneoffcoder.com/python-manual-control.html
    """

    # Initialize the Tello class passing in the UDP port used to connect to it
    drone = tello.Tello('', 8889)

    # Initialize the GUI and start it as the tkinter main loop
    GUI = MappingUI(drone)
    GUI.root.mainloop()
