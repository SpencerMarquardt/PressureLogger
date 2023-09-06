# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFrame,
    QHBoxLayout, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_PressureWidget(object):
    def setupUi(self, PressureWidget):
        if not PressureWidget.objectName():
            PressureWidget.setObjectName(u"PressureWidget")
        PressureWidget.resize(800, 600)
        self.centralwidget = QWidget(PressureWidget)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pressureDisplay = QLabel(self.frame_3)
        self.pressureDisplay.setObjectName(u"pressureDisplay")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.pressureDisplay.setFont(font)
        self.pressureDisplay.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.pressureDisplay)


        self.horizontalLayout_3.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.minutesSpinBox = QSpinBox(self.frame_2)
        self.minutesSpinBox.setObjectName(u"minutesSpinBox")
        self.minutesSpinBox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.minutesSpinBox.setMaximum(60)
        self.minutesSpinBox.setValue(2)

        self.horizontalLayout_2.addWidget(self.minutesSpinBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.csvButton = QPushButton(self.frame_2)
        self.csvButton.setObjectName(u"csvButton")

        self.verticalLayout_4.addWidget(self.csvButton)


        self.horizontalLayout_3.addWidget(self.frame_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(1)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.portList = QComboBox(self.frame)
        self.portList.setObjectName(u"portList")

        self.horizontalLayout.addWidget(self.portList)

        self.connectButton = QPushButton(self.frame)
        self.connectButton.setObjectName(u"connectButton")

        self.horizontalLayout.addWidget(self.connectButton)

        self.refreshPortsButton = QPushButton(self.frame)
        self.refreshPortsButton.setObjectName(u"refreshPortsButton")

        self.horizontalLayout.addWidget(self.refreshPortsButton)

        self.verticalLayout2 = QVBoxLayout()
        self.verticalLayout2.setObjectName(u"verticalLayout2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout2.addWidget(self.label)

        self.connectionStatus = QLabel(self.frame)
        self.connectionStatus.setObjectName(u"connectionStatus")
        self.connectionStatus.setAlignment(Qt.AlignCenter)

        self.verticalLayout2.addWidget(self.connectionStatus)

        self.refreshNotificationLabel = QLabel(self.frame)
        self.refreshNotificationLabel.setObjectName(u"refreshNotificationLabel")
        self.refreshNotificationLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout2.addWidget(self.refreshNotificationLabel)


        self.horizontalLayout.addLayout(self.verticalLayout2)


        self.verticalLayout_2.addWidget(self.frame)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        PressureWidget.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(PressureWidget)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        PressureWidget.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(PressureWidget)
        self.statusbar.setObjectName(u"statusbar")
        PressureWidget.setStatusBar(self.statusbar)

        self.retranslateUi(PressureWidget)

        QMetaObject.connectSlotsByName(PressureWidget)
    # setupUi

    def retranslateUi(self, PressureWidget):
        PressureWidget.setWindowTitle(QCoreApplication.translate("PressureWidget", u"PressureWidget", None))
        self.pressureDisplay.setText(QCoreApplication.translate("PressureWidget", u"0.0000 atm", None))
        self.label_2.setText(QCoreApplication.translate("PressureWidget", u"Show last:", None))
        self.minutesSpinBox.setSuffix(QCoreApplication.translate("PressureWidget", u" minutes", None))
        self.csvButton.setText(QCoreApplication.translate("PressureWidget", u"Log to .csv", None))
        self.connectButton.setText(QCoreApplication.translate("PressureWidget", u"Connect", None))
        self.refreshPortsButton.setText(QCoreApplication.translate("PressureWidget", u"Refresh Ports", None))
        self.label.setText(QCoreApplication.translate("PressureWidget", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">Connection Status:</span></p></body></html>", None))
        self.connectionStatus.setText(QCoreApplication.translate("PressureWidget", u"<html><head/><body><p><span style=\" font-size:10pt;\">Connection Status </span></p></body></html>", None))
        self.refreshNotificationLabel.setText(QCoreApplication.translate("PressureWidget", u"<html><head/><body><p><span style=\" font-size:10pt;\">Connection message</span></p></body></html>", None))
    # retranslateUi

