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
        self.fieldnames = None

    def set_log_path(self, path):
        self.log_path = path
        if path is None:
            return
        if not os.path.exists(self.log_path):
            # Wait for first reading to get full header
            self.fieldnames = None

    def add_reading(self, pressure_dict):
        timestamp = datetime.now().isoformat()
        row = {"timestamp": timestamp}
        row.update(pressure_dict)
        self.pressure_data.append(row)

        # Only log if a valid file path is set
        if self.log_path:
            file_exists = os.path.exists(self.log_path)
            with open(self.log_path, 'a', newline='') as csvfile:
                if self.fieldnames is None:
                    self.fieldnames = ["timestamp"] + sorted(pressure_dict.keys())
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                if not file_exists or os.stat(self.log_path).st_size == 0:
                    writer.writeheader()
                writer.writerow(row)

        self.data_updated.emit()

    def get_recent_data(self, minutes=2, channel="CH0"):
        cutoff = datetime.now().timestamp() - (minutes * 60)
        return [
            (entry["timestamp"], entry[channel])
            for entry in self.pressure_data
            if channel in entry and datetime.fromisoformat(entry["timestamp"]).timestamp() > cutoff
        ]
