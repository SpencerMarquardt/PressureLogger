from PyQt6.QtWidgets import QMainWindow, QFileDialog
from datetime import datetime
import pyqtgraph as pg

import os
# custom imports
from app.ui.ui_mainwindow import Ui_PressureWidget
from app.controllers.serial_device_listener import SerialDeviceListener, get_serial_ports
from app.controllers.pressure_serial_controller import PressureSerialController
from app.models.pressure_model import PressureModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PressureWidget()
        self.ui.setupUi(self)

    # Initialize views and design
        self.setWindowTitle("MPRLS Pressure Logger")
        self.ui.pressureDisplay.setText('0.00 mbar')
        self.ui.csvButton.setEnabled(False)  # Disable at startup
        self.ui.csvButton.setText("Start Logging")
        self.pressure_plot = self.ui.pressurePlotWidget
        self.initialize_plot()
        
    # Initialize variables
        self.selected_port = None
        self.pressure_controller = None
        self.pressure_model = PressureModel()
        self.logging_active = False

    # Initialize a listener for serial device changes
        self.device_listener = SerialDeviceListener(self.update_serial_devices_combobox)
        self.device_listener.start()
        self.update_serial_devices_combobox()

    # Handle signals

        self.ui.connectButton.clicked.connect(self.connect_to_selected_port)
        self.ui.csvButton.clicked.connect(self.handle_csv_button)

        self.pressure_model.data_updated.connect(self.update_plot)

    def update_serial_devices_combobox(self):
        available_ports = get_serial_ports()
        self.ui.serialPortComboBox.clear()
        for port in available_ports:
            port_text = f"{port.device} - {port.description}"
            self.ui.serialPortComboBox.addItem(port_text)

    def connect_to_selected_port(self):
        if self.pressure_controller and self.pressure_controller.running:
            # Disconnect logic
            self.pressure_controller.stop()
            self.pressure_controller = None

            self.ui.connectButton.setText("Connect")
            self.ui.connectionStatus.setText("Disconnected")

            # Stop logging if it was active
            if self.logging_active:
                self.logging_active = False
                self.pressure_model.set_log_path(None)
                self.ui.csvButton.setText("Start Logging")
                self.update_refresh_notification("Logging stopped due to disconnection.")

            self.ui.csvButton.setEnabled(False)
            return

        # Connect logic
        self.selected_port = self.ui.serialPortComboBox.currentText().split(' - ')[0]

        if self.pressure_controller:
            self.pressure_controller.stop()

        self.pressure_controller = PressureSerialController(self.selected_port)
        self.pressure_controller.pressure_received.connect(self.update_pressure_display)
        self.pressure_controller.status_updated.connect(self.update_refresh_notification)
        self.pressure_controller.connection_state_changed.connect(self.update_connection_status)
        self.pressure_controller.pressure_received.connect(self.pressure_model.add_reading)
        self.pressure_controller.start()


    def update_pressure_display(self, pressure):
        self.ui.pressureDisplay.setText(f"{pressure:.4f} mbar")

    def update_connection_status(self, connected):
        self.ui.connectionStatus.setText("Connected" if connected else "Disconnected")
        self.ui.connectButton.setText("Disconnect" if connected else "Connect")
        self.ui.csvButton.setEnabled(connected)

        if not connected and self.logging_active:
            self.logging_active = False
            self.pressure_model.set_log_path(None)
            self.ui.csvButton.setText("Start Logging")
            self.update_refresh_notification("Logging stopped due to disconnection.")

    def update_refresh_notification(self, message):
        self.ui.refreshNotificationLabel.setText(message)

    def handle_csv_button(self):
        if not self.logging_active:
            # Start logging
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            default_filename = f"{timestamp}_pressure.csv"

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Select CSV Log File",
                default_filename,
                "CSV Files (*.csv);;All Files (*)"
            )

            if file_path:
                self.pressure_model.set_log_path(file_path)
                self.update_refresh_notification(f"Logging to: {file_path}")
                self.ui.csvButton.setText("Stop Logging")
                self.logging_active = True
        else:
            # Stop logging
            self.pressure_model.set_log_path(None)
            self.update_refresh_notification("Logging stopped.")
            self.ui.csvButton.setText("Start Logging")
            self.logging_active = False

    def initialize_plot(self):
        # Initialize the plot

        self.pressure_plot.setBackground('w')
        self.pressure_plot.showGrid(x=True, y=True)
        self.pressure_plot.setLabel('left', 'Pressure', units='mbar')
        self.pressure_plot.setLabel('bottom', 'Time', units='s')

        self.pressure_curve = self.pressure_plot.plot(pen=pg.mkPen(color='b', width=2))

    def update_plot(self):
        minutes = self.ui.minutesSpinBox.value()
        data = self.pressure_model.get_recent_data(minutes)

        if not data:
            self.pressure_curve.setData([], [])
            return

        timestamps, pressures = zip(*data)
        times_sec = [(datetime.fromisoformat(ts) - datetime.fromisoformat(timestamps[0])).total_seconds() for ts in
                     timestamps]
        self.pressure_curve.setData(times_sec, pressures)