from PyQt6.QtCore import QThread, pyqtSignal
import serial
import time
import json
class PressureSerialController(QThread):
    pressure_received = pyqtSignal(dict)
    status_updated = pyqtSignal(str)
    connection_state_changed = pyqtSignal(bool)

    def __init__(self, port_name, baudrate=115200, parent=None):
        super().__init__(parent)
        self.port_name = port_name
        self.baudrate = baudrate
        self.serial = None
        self.running = False

    def run(self):
        try:
            self.serial = serial.Serial(self.port_name, self.baudrate, timeout=1)
            self.running = True
            self.connection_state_changed.emit(True)  # Connected
            self.status_updated.emit(f"Connected to {self.port_name}")

            while self.running:
                if self.serial.in_waiting:
                    try:
                        line = self.serial.readline().decode("utf-8").strip()
                        print(f"Pressure Controller Received: {line}")

                        data = json.loads(line)

                        # Emit only if it's a dict of numeric pressures
                        if isinstance(data, dict) and all(isinstance(v, (int, float)) for v in data.values()):
                            self.pressure_received.emit(data)
                        elif 'error' in data:
                            self.status_updated.emit(f"Device error: {data['error']}")
                        else:
                            self.status_updated.emit("Unrecognized data format")

                    except ValueError:
                        self.status_updated.emit("Invalid JSON received")
                    except Exception as e:
                        self.status_updated.emit(f"Parse error: {str(e)}")

                time.sleep(0.05)

        except serial.SerialException:
            self.status_updated.emit(f"Serial port {self.port_name} not found")
        finally:
            if self.serial and self.serial.is_open:
                self.serial.close()
            self.connection_state_changed.emit(False)  # Disconnected
            self.status_updated.emit(f"Serial port {self.port_name} closed")

    def stop(self):
        self.running = False
        self.wait()

