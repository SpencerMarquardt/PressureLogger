from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from app.ui.ui_mainwindow import Ui_PressureWidget
import os
from app.controllers.serial_device_listener import SerialDeviceListener, get_serial_ports
from app.controllers.pressure_serial_controller import PressureSerialController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PressureWidget()
        self.ui.setupUi(self)

        self.setWindowTitle("MPRLS Pressure Logger")

    # Initialize variables
        self.selected_port = None
        self.controller = None
        self.ui.pressureDisplay.setText('0.00 mbar')

    # Initialize a listener for serial device changes
        self.device_listener = SerialDeviceListener(self.update_serial_devices_combobox)
        self.device_listener.start()
        self.update_serial_devices_combobox()

    # Handle user inputs
        self.ui.connectButton.clicked.connect(self.connect_to_selected_port)

    def update_serial_devices_combobox(self):
        available_ports = get_serial_ports()
        self.ui.serialPortComboBox.clear()
        for port in available_ports:
            port_text = f"{port.device} - {port.description}"
            self.ui.serialPortComboBox.addItem(port_text)

    def connect_to_selected_port(self):
        self.selected_port = self.ui.serialPortComboBox.currentText().split("-")[0]
        if self.controller:
            self.controller.stop()

        self.controller = PressureSerialController(self.selected_port)
        self.controller.pressure_received.connect(self.update_pressure_display)
        self.controller.status_updated.connect(self.update_connection_status)
        self.controller.start()

    def update_pressure_display(self, pressure):
        self.ui.pressureDisplay.setText(f"{pressure:.2f} mbar")

    def update_connection_status(self, message):
        self.ui.refreshNotificationLabel.setText(message)
