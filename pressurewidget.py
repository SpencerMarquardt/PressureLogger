# This Python file uses the following encoding: utf-8
import sys
import serial
import csv
import os
import datetime
from serial.tools import list_ports
from collections import deque
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QTimer
import time
import pyqtgraph as pg

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_PressureWidget


class PressureWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PressureWidget()
        self.ui.setupUi(self)

        # Define variables and flags
        self.ports_have_changed = False
        self.last_selected_port = None
        self.was_connected = False
        self.start_time = None
        self.current_time = None
        self.is_logging = False

        # Plotting initialization
        self.time_data = deque()
        self.pressure_data = deque()

        # Handles user inputs
        self.connect_serial_port()
        self.setup_plot()
        self.ui.csvButton.setEnabled(False)
        self.ui.connectButton.clicked.connect(self.connect_to_selected_port)
        self.ui.refreshPortsButton.clicked.connect(self.update_ports)
        self.ui.minutesSpinBox.valueChanged.connect(self.update_plot)
        self.ui.csvButton.clicked.connect(self.toggle_logging)

        # Create a QTimer to read serial data
        self.serial_timer = QTimer(self)
        self.serial_timer.timeout.connect(self.read_serial)
        self.serial_timer.start(500)  # Read every 1000 ms (1 second)

        # Timer to update available ports
        # connect the timer to a notification function
        self.port_update_timer = QTimer(self)
        self.port_update_timer.timeout.connect(self.notify_ports_changed)
        self.port_update_timer.start(500)

        # Timer to check connection status
        self.connection_check_timer = QTimer(self)
        self.connection_check_timer.timeout.connect(self.check_connection_status)
        self.connection_check_timer.start(500)  # Check every .5 seconds

    # Add items to portList combobox when called
    def connect_serial_port(self):
        # Set up serial interface
        self.serial_port = serial.Serial()
        self.serial_port.BAUDRATES = 115200

        ports = list_ports.comports()
        for port in ports:
            self.ui.portList.addItem(f'{port.device} - {port.description}')

    # If a serial device appears or disappears notify the user
    def notify_ports_changed(self):
        current_ports = set([f'{port.device} - {port.description}' for port in list_ports.comports()])
        previous_ports = set([self.ui.portList.itemText(i) for i in range(self.ui.portList.count())])

        if current_ports != previous_ports:
            self.ports_have_changed = True
            self.ui.refreshNotificationLabel.setText("Ports have changed. Click refresh!")
            self.ui.refreshNotificationLabel.setStyleSheet("color: orange")
        else:
            self.ui.refreshNotificationLabel.setText("")

    # Update the portsList when the refresh button is pushed
    def update_ports(self):
        if self.ports_have_changed or not self.ui.portList.count():
            # Only update ports if they have changed or the list is empty
            self.ui.portList.clear()  # Clear existing items
            ports = list_ports.comports()

            index_to_select = -1

            for i, port in enumerate(ports):
                self.ui.portList.addItem(f'{port.device} - {port.description}')
                if port.device == self.last_selected_port:
                    index_to_select = i

            if index_to_select != -1:
                self.ui.portList.setCurrentIndex(index_to_select)

            self.ports_have_changed = False
            self.ui.refreshNotificationLabel.setText("")

    # Connect to the selected port when connect button is clicked
    def connect_to_selected_port(self):
        self.start_time = time.time()
        selected_port = self.ui.portList.currentText().split(' - ')[0]
        self.last_selected_port = selected_port
        self.serial_port.port = selected_port

        if not self.serial_port.is_open:
            try:
                self.serial_port.open()
                print(f"Connected to {selected_port}")
                self.ui.connectionStatus.setText(f"Connected to {selected_port}")
                self.ui.connectionStatus.setStyleSheet("color: green")
                self.was_connected = True
                self.ui.csvButton.setEnabled(True)
            except Exception as e:
                print(f"Failed to connect: {e}")
                self.ui.connectionStatus.setText(f"Failed to connect: {e}")
                self.ui.connectionStatus.setStyleSheet("color: red")

    # Set the connection status message
    def check_connection_status(self):
        if not self.serial_port.is_open:
            self.ui.connectionStatus.setText("Disconnected")
            self.ui.connectionStatus.setStyleSheet("color: red")
        else:
            self.ui.connectionStatus.setText(f"Connected to {self.serial_port.port}")
            self.ui.connectionStatus.setStyleSheet("color: green")

    # Read from the serial port
    def read_serial(self):
        try:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode('utf-8').strip()
                pressure_atm = round(float(data) * 0.000986923, 4)  # Convert mbar string to atm float w/4 sig figs
                data = str(pressure_atm)  # convert back to string for the display
                self.ui.pressureDisplay.setText(f'{data} atm')
                self.current_time = time.time()
                elapsed_time = self.current_time - self.start_time
                self.time_data.append(elapsed_time)  # or any other timestamp

                self.pressure_data.append(pressure_atm)
                self.update_plot()
                # Save to csv
                self.save_to_csv(self.current_time, pressure_atm)

        except serial.SerialException:
            self.stop_logging()
            self.ui.csvButton.setEnabled(False)
            if self.was_connected:
                # This block will execute if there's a serial connection error and we were previously connected
                self.ui.connectionStatus.setText("Connection lost")
                self.ui.connectionStatus.setStyleSheet("color: red")
                if self.serial_port.is_open:
                    self.serial_port.close()
                self.was_connected = False  # Reset the flag since the connection is now lost

    def setup_plot(self):
        # Initialize plot
        self.plotWidget = pg.PlotWidget()
        self.ui.verticalLayout.addWidget(self.plotWidget)
        self.curve = self.plotWidget.plot(pen=pg.mkPen('b', width=2))
        styles = {'color': 'k', 'font-size': '20px'}
        self.plotWidget.setLabel('left', 'Pressure (atm)', **styles)
        self.plotWidget.setLabel('bottom', 'Elapsed Time (s)', **styles)
        self.plotWidget.setBackground('w')

    def update_plot(self):
        self.curve.setData(self.time_data, self.pressure_data)

        # Get the time window from the spinbox
        minutes_to_show = self.ui.minutesSpinBox.value()
        seconds_to_show = minutes_to_show * 60  # Convert to seconds
        current_time = self.time_data[-1] if self.time_data else 0
        start_time = current_time - seconds_to_show

        # Filter the pressure data based on the time window
        pressure_data_to_consider = [pressure for t, pressure in zip(self.time_data, self.pressure_data) if
                                     t >= start_time]

        # Adjust the X-axis range based on the spinbox value
        self.plotWidget.setXRange(start_time, current_time)

        # Adjust the Y-axis based on the filtered data
        if pressure_data_to_consider:
            y_min = min(pressure_data_to_consider)
            y_max = max(pressure_data_to_consider)
        else:
            y_min, y_max = .9, 1.1  # Default values
        # Set the range about the max and min pressure values to display
        y_min = y_min - .01
        y_max = y_max + .01
        self.plotWidget.setYRange(y_min, y_max)

    def choose_file_location(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory to Save CSV File', '', options=options)
        return directory

    def save_to_csv(self, timestamp, pressure):
        if not self.is_logging:
            return
        # Check if file exists to determine if header is needed
        file_exists = os.path.isfile(self.csv_file_path)

        with open(self.csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Time', 'Pressure'])

            writer.writerow([timestamp, pressure])

    def toggle_logging(self):
        if self.is_logging:
            self.stop_logging()
        else:
            # Get the save path from a dialog
            save_path = QFileDialog.getExistingDirectory(self, "Choose Save Location")
            if not save_path:
                return
            # Construct the csv file path with the desired filename
            formatted_time = datetime.datetime.fromtimestamp(self.current_time).strftime('%Y-%m-%d_%H-%M-%S')
            self.csv_file_path = os.path.join(save_path, f"pressureLog_{formatted_time}.csv")
            self.is_logging = True
            self.ui.csvButton.setText('Stop Logging')

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.ui.csvButton.setText('Log to .csv')
            # You can add any other logic related to saving or finalizing the csv here if needed

    def closeEvent(self, event):
        self.stop_logging()
        if self.serial_port.is_open:
            self.serial_port.close()
        self.port_update_timer.stop()
        self.connection_check_timer.stop()
        self.serial_timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PressureWidget()
    widget.show()
    sys.exit(app.exec())
