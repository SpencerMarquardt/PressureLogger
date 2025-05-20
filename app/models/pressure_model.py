from PyQt6.QtCore import QObject, pyqtSignal
import csv
import os
from datetime import datetime

class PressureModel(QObject):
    data_updated = pyqtSignal()

    def __init__(self, log_path="pressure_log.csv"):
        super().__init__()
        self.log_path = log_path
        self.pressure_data = []

        if os.path.exists(self.log_path):
            with open(self.log_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                self.pressure_data = [(row[0], float(row[1])) for row in reader]

    def add_reading(self, pressure_value):
        timestamp = datetime.now().isoformat()
        self.pressure_data.append((timestamp, pressure_value))

        # append to CSV
        with open(self.log_path, newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, pressure_value])

        self.data_updateda.emit()

    def get_recent_data(self, minutes=2):
        """ Returns data within the last X minutes"""
        cutoff = datetime.now().timestamp() - (minutes * 60)
        return [(ts, val) for ts, val in self.pressure_data if datetime.fromisoformat(ts).timestamp() > cutoff]
