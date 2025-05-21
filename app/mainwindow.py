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
        # self.ui.pressureDisplay.setText('0.00 mbar')
        self.ui.csvButton.setEnabled(False)  # Disable at startup
        self.ui.csvButton.setText("Start Logging")
        self.pressure_plot = self.ui.pressurePlotWidget
        self.pressure_curves = None
        self.initialize_plot()
        self.legend = None

        # Initialize variables
        self.selected_port = None
        self.pressure_controller = None
        self.pressure_model = PressureModel()
        self.logging_active = False
        self.unit = "mbar"
        self.unit_conversion = {
            "mbar": lambda x: x,
            "torr": lambda x: x * 0.750061683
        }
    # Initialize a listener for serial device changes
        self.device_listener = SerialDeviceListener(self.update_serial_devices_combobox)
        self.device_listener.start()
        self.update_serial_devices_combobox()

    # Handle signals
        self.ui.pressureUnitComboBox.currentTextChanged.connect(self.change_unit)

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

    def update_pressure_display(self, pressure_dict):
        for n, ch in enumerate(sorted(pressure_dict.keys())):
            val = pressure_dict[ch]
            label_name = f"pressureDisplay_{n}"
            label = getattr(self.ui, label_name, None)
            if label:
                val_converted = self.unit_conversion[self.unit](val)
                label.setText(f"{ch}: {val_converted:.2f} {self.unit}")

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
        # Set background and grid
        self.pressure_plot.setBackground('w')
        self.pressure_plot.showGrid(x=True, y=True)

        # Customize axis tick and label colors
        label_style = {'color': 'k', 'font-size': '14pt'}
        for axis in ['left', 'bottom']:
            ax = self.pressure_plot.getAxis(axis)
            ax.setTextPen('k')  # Tick label color
            ax.setPen('k')  # Axis line color
            ax.setLabel(**label_style)

        # Axis labels
        self.pressure_plot.setLabel('left', 'Pressure (mbar)', units='')
        self.pressure_plot.setLabel('bottom', 'Time', units='s')

        self.pressure_curves = {
            "CH0": self.pressure_plot.plot(pen=pg.mkPen('b', width=2)),
            "CH1": self.pressure_plot.plot(pen=pg.mkPen('r', width=2)),
        }
        # Legend
        self.legend = self.pressure_plot.addLegend()
        self.legend.setBrush(pg.mkBrush(255, 255, 255, 200))
        self.legend.setPen(pg.mkPen('k'))
        self.legend.anchor((0, 0), (0, 0))

        for ch, curve in self.pressure_curves.items():
            self.legend.addItem(curve, ch)

        # Make legend text black and larger
        for _, label in self.legend.items:
            if hasattr(label, 'item') and hasattr(label.item, 'setStyleSheet'):
                label.item.setStyleSheet("color: black; font-size: 12pt;")

    def update_plot(self):
        minutes = self.ui.minutesSpinBox.value()
        for channel, curve in self.pressure_curves.items():
            data = self.pressure_model.get_recent_data(minutes, channel=channel)
            if not data:
                curve.setData([], [])
                continue

            timestamps, pressures = zip(*data)
            t0 = datetime.fromisoformat(timestamps[0])
            times_sec = [(datetime.fromisoformat(ts) - t0).total_seconds() for ts in timestamps]
            pressures_converted = [self.unit_conversion[self.unit](p) for p in pressures]
            curve.setData(times_sec, pressures_converted)

        # Update y-axis label
        self.pressure_plot.setLabel('left', f'Pressure ({self.unit})', units='')

    def change_unit(self, unit_text):
        self.unit = unit_text
        self.update_plot()  # Refresh plot with new unit