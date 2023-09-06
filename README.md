# Pressure Monitor and Logger with Adafruit Qt Py 2040
A simple Python application interfaces with an Adafruit Qt Py 2040 via a serial interface to display real-time pressure data in a graphical interface with the option to save data to a .csv file.

## Features:
* Real-time plotting
* Adjustable time window
* Logging to CSV file
* Auto detection of serial devices

## Prerequisites:
* Python 3.7 or later
* PySide6, pyqtgraph, and pyserial Python packages

## Setup and Installation:
* Clone the repository: `git clone https://github.com/SpencerMarquardt/PressureLogger`
* Navigate to the project directory and install the required Python packages:
  * `cd <project-directory>`
  * `pip install PySide6 pyqtgraph pyserial`
* Generate the 'ui_form.py' file if not available `pyside6-uic form.ui -o ui_form.py`
* 
