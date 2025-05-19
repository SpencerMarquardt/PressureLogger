import os
from PyQt6.QtWidgets import QMessageBox


def whoi_icon_path():
    return os.path.join(os.path.join(os.path.dirname(__file__), "resources/icons/WHOI_PrimaryLogo_DarkBlueType_RGB.png"))

def show_error_dialog(error_message):
    msg_box = QMessageBox()
    # msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText('An error occurred:')
    msg_box.setInformativeText(error_message)
    msg_box.exec()

