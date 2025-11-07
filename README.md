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
* Update the repository: `git pull --rebase https://github.com/SpencerMarquardt/PressureLogger`
* Create a virtual environment (Windows) `python -m venv myenv`
* Activate the virtual environment (Windows) `myenv\Scripts\activate`
* Navigate to the project directory and install the required Python packages:
  * `cd <project-directory>`
  * `pip install PySide6 pyqtgraph pyserial`
  * or all at once: `pip install -r requirements.txt`
* Install the Qt Designer plugin for PySide6: `pip install pyside6-tools`
* Open the 'form.ui' file in Qt Designer and save the file as 'form.py'`
* Generate the 'ui_form.py' file if not available `pyside6-uic form.ui -o ui_form.py`

## Usage:
* To run the application: `python pressurewidget.py`
