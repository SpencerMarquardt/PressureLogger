from PyQt6.QtCore import QThread, pyqtSignal
import serial
import time

class PressureSerialController(QThread):
    pressure_received = pyqtSignal(float)
    status_updated = pyqtSignal(str)

    def __init__(self, port_name, baudrate=115200, parent=None):
        super().__init__(parent)
        self.port_name = port_name
        self.baudrate = baudrate
        self.serial = None
        self.running = False

    def run(self):
        try:
            self.serial = serial.Serial(self.port_name, self.baudrate, timeout=1)
            self.status_updated.emit(f"Connected to {self.port_name}")
            self.running = True

            while self.running:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode("utf-8").strip()
                    try:
                        pressure = float(line)
                        self.pressure_received.emit(pressure)
                    except ValueError:
                        self.status_updated.emit(f"Invalid pressure {line}")
                time.sleep(0.05)
        except serial.SerialException:
            self.status_updated.emit(f"Serial port {self.port_name} not found")
        finally:
            if self.serial and self.serial.is_open:
                self.serial.close()
            self.status_updated.emit(f"Serial port {self.port_name} closed")

    def stop(self):
        self.running = False
        self.wait()

