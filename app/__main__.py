import sys
import traceback

from PyQt6.QtWidgets import QApplication

from app.mainwindow import MainWindow
from PyQt6.QtGui import QIcon
from qt_material import apply_stylesheet
from app.utils import whoi_icon_path
import os

def new_excepthook(type, value, tb):
    # By default, Qt does not output any errors and crashes silently, this prevents that
    traceback.print_exception(type, value, tb)

sys.excepthook = new_excepthook

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(whoi_icon_path()))

    window = MainWindow()
    # Apply the stylesheet here eventually

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
