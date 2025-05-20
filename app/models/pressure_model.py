from PyQt6.QtCore import QObject, pyqtSignal
import csv
import os
from datetime import datetime


class PressureModel(QObject):
    data_updated = pyqtSignal()

    def __init__(self, log_path=None):
        super().__init__()
        self.log_path = log_path
        self.pressure_data = []

    def set_log_path(self, path):
        self.log_path = path
        if path is None:
            return  # Don't try to create or check the file
        if not os.path.exists(self.log_path):
            # Create file and write header
            with open(self.log_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["timestamp", "pressure"])

    def add_reading(self, pressure_value):
        timestamp = datetime.now().isoformat()
        self.pressure_data.append((timestamp, pressure_value))

        # Only log if a valid file path is set
        if self.log_path:
            with open(self.log_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, pressure_value])

        self.data_updated.emit()

    def get_recent_data(self, minutes=2):
        cutoff = datetime.now().timestamp() - (minutes * 60)
        return [
            (ts, val) for ts, val in self.pressure_data
            if datetime.fromisoformat(ts).timestamp() > cutoff
        ]
