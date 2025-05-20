"""
serial_ports.py

This module provides functionality for detecting and handling serial port connections
on a Windows system. It includes:
1. A function to list available serial ports.
2. A class to listen for USB device connection and disconnection events, updating the
   available ports dynamically.

Dependencies:
- pyserial (for serial port enumeration)
- pywin32 (for Windows API interaction)

Author: Your Name
"""

import win32gui
import win32con
import win32api
import serial
from serial.tools import list_ports
import threading

# Constants for Windows device change events
DBT_DEVICEARRIVAL = 0x8000  # Event triggered when a new device is inserted
DBT_DEVICEREMOVECOMPLETE = 0x8004  # Event triggered when a device is removed

class SerialDeviceListener:
    """
    Listens for USB device change events and triggers a callback function when a serial device is inserted or removed.

    Attributes:
        callback (function): Function to be called when a device change event is detected.
        hwnd (int): Handle to the hidden window that listens for events.
        thread (threading.Thread): Background thread running the event listener.
    """

    def __init__(self, callback):
        """
        Initializes the device change listener.

        Args:
            callback (function): The function to be called when a device is added or removed.
        """
        self.callback = callback
        self.hwnd = None  # Handle for the event listener window
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _window_proc(self, hwnd, msg, wparam, lparam):
        """
        Window procedure for handling device change events.

        Args:
            hwnd (int): Window handle.
            msg (int): Message ID.
            wparam (int): Additional message-specific information.
            lparam (int): Additional message-specific information.

        Returns:
            int: Result of the default window procedure.
        """
        if msg == win32con.WM_DEVICECHANGE:
            if wparam in [DBT_DEVICEARRIVAL, DBT_DEVICEREMOVECOMPLETE]:
                print("USB device change detected, updating serial ports...")
                self.callback()  # Invoke the callback to refresh serial ports
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def _run(self):
        """
        Creates a hidden window to listen for Windows device change events.
        """
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._window_proc  # Assign the window procedure
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = 'SerialDeviceListener'

        # Register the window class
        class_atom = win32gui.RegisterClass(wc)

        # Create a hidden window to listen for device events
        self.hwnd = win32gui.CreateWindow(
            class_atom, "Device Change Listener", 0,
            0, 0, 0, 0, 0, 0, wc.hInstance, None
        )

        print("SerialDeviceListener started. Listening for USB events...")
        win32gui.PumpMessages()  # Start the event loop

    def start(self):
        """
        Starts the background thread to listen for device events.
        """
        self.thread.start()

    def stop(self):
        """
        Stops the listener by destroying the hidden window.
        """
        if self.hwnd:
            win32gui.DestroyWindow(self.hwnd)
            self.hwnd = None
            print("SerialDeviceListener stopped.")


def get_serial_ports():
    """
    Retrieves a list of available serial ports.

    Returns:
        list: A list of serial port objects, each containing device name and description.
    """
    ports = list_ports.comports()
    return ports


def validate_port(port_name):
    available_ports = [port.device for port in list_ports.comports()]
    if port_name not in available_ports:
        raise ValueError(f"Port {port_name} is not available.")
    try:
        test_port = serial.Serial(port_name)
        test_port.close()
        return True
    except serial.SerialException as e:
        raise RuntimeError(f"Port {port_name} is in use or inaccessible: {e}")

