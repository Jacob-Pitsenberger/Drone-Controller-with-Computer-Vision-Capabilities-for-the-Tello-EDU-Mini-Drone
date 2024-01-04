"""
Title: tkinter-multiframe-mvc
Author: Nazmul Ahsan
Date: 1-6-23
Code Version: N/A
Availability: https://github.com/AhsanShihab/tkinter-multiframe-mvc
"""

from models.main import Model
from views.main import View
from controllers.main import Controller


def main():
    # Initialize the Model, View, and Controller classes
    model = Model()
    view = View()
    controller = Controller(model, view)
    # Call the Controller classes start method
    controller.start()


if __name__ == "__main__":
    # Run the main function above as the python main loop
    main()
