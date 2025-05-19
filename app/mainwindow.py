from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from app.ui.ui_mainwindow import Ui_PressureWidget
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PressureWidget()
        self.ui.setupUi(self)

        self.setWindowTitle("MPRLS Pressure Logger")
