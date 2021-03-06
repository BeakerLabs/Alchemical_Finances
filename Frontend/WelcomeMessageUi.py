#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPixmap
from win32api import GetMonitorInfo, MonitorFromPoint

from Toolbox.OS_Tools import obtain_screen_dimensions


class Ui_WelcomeMessage(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("WelcomeScreen")
        Dialog.setWindowTitle("Message Screen")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        # Obtain and use the monitor screen to determine the size of the dialog box
        screen_dimensions, _ = obtain_screen_dimensions()
        work_area = screen_dimensions

        size_factor = 0.25
        modifier = 0

        if 2160 <= work_area[3]:
            size_factor = size_factor
            modifier = 0

        if 1600 <= work_area[3] < 2160:
            size_factor = (2160 * size_factor)/1600
            modifier = 0

        if 1080 <= work_area[3] < 1600:
            size_factor = (2160 * size_factor)/1080
            modifier = 150

        if 900 <= work_area[3] < 1080:
            size_factor = (2160 * size_factor)/900
            modifier = 150

        if work_area[3] < 900:
            size_factor = (2160 * size_factor)/900
            modifier = 200

        adjusted_height = (work_area[3] * size_factor) + modifier
        adjusted_width = work_area[2] * size_factor

        # Making the Message screen larger than log in but not full screen.
        # Rational - Make it catch the users eye
        Dialog.resize(adjusted_width, adjusted_height)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(int(adjusted_height), int(adjusted_height)))
        Dialog.setMaximumSize(QtCore.QSize(int(adjusted_height), int(adjusted_height)))

        self.outsideFrame = QtWidgets.QFrame(Dialog)
        self.outsideFrame.setObjectName("outsideFrame")
        # self.outsideFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.outsideFrame.setLineWidth(1)
        self.outsideFrame.setGeometry(40, 40, adjusted_height - 90, adjusted_height - 90)

        self.gridLayout = QtWidgets.QGridLayout(self.outsideFrame)
        self.gridLayout.setObjectName("gridLayout")

        # Row 1 -- Label for Welcome message
        self.vlr1 = QtWidgets.QVBoxLayout()
        self.vlr1.setObjectName("vlr1")
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addLayout(self.vlr1, 1, 1, 1, 4, alignment=QtCore.Qt.Alignment())

        self.hlr1 = QtWidgets.QHBoxLayout()
        self.hlr1.setObjectName("hlr1")
        self.vlr1.addLayout(self.hlr1)

        self.titleLSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr1.addItem(self.titleLSpacer)

        self.labelWelcome = QtWidgets.QLabel()
        self.labelWelcome.setObjectName("labelWelcome")
        title_font = QtGui.QFont()
        title_font.setPixelSize(37)
        self.labelWelcome.setAlignment(QtCore.Qt.AlignLeft)
        self.labelWelcome.setFont(title_font)
        label_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        label_sizePolicy.setHorizontalStretch(0)
        label_sizePolicy.setVerticalStretch(0)
        self.labelWelcome.setSizePolicy(label_sizePolicy)
        # Development purposes only
        self.labelWelcome.setText("Welcome User...")
        self.hlr1.addWidget(self.labelWelcome)

        # Row 2 -- Frame -- Message

        # QHBoxLayout --> QFrame --> QHBoxLayout --> QSpacer & QFrame --> QScrollArea (Set as Widget) --> QVBoxLayout --> QLabel
        # The messageFrame sets the "invisible" outermost width
        # The messageSpacer keeps the scroll area height constant. This allows for the buttons to have an expanding height
        # From an alignment standpoint The scroll area doesn't align with the outermost widgets in Rows 1, 3 & 4

        self.hlr2 = QtWidgets.QHBoxLayout()
        self.hlr2.setObjectName("hlr2")
        self.gridLayout.addLayout(self.hlr2, 2, 1, 1, 4, alignment=QtCore.Qt.Alignment())

        self.messageSpacer = QtWidgets.QSpacerItem(0, adjusted_height - 348, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.hlr2.addItem(self.messageSpacer)

        self.scrollFrame = QtWidgets.QFrame()
        self.scrollFrame.setObjectName("scrollFrame")
        self.scrollFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.scrollFrame.setLineWidth(3)
        self.scrollFrame.setFixedHeight(adjusted_height - 348)
        scrollFrame_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.scrollFrame.setSizePolicy(scrollFrame_sizePolicy)
        self.hlr2.addWidget(self.scrollFrame)

        self.messageScroll = QtWidgets.QScrollArea(self.scrollFrame)
        self.messageScroll.setGeometry(3, 3, 0, 0)
        self.messageScroll.setFixedWidth(adjusted_height - 115)
        self.messageScroll.setFixedHeight(adjusted_height - 354)
        self.messageScroll.setFrameStyle(0)
        self.messageScroll.horizontalScrollBar().setEnabled(False)
        self.messageScroll.setWidgetResizable(True)

        widget = QtWidgets.QWidget()
        self.messageScroll.setWidget(widget)
        self.scrolllayout = QtWidgets.QVBoxLayout(widget)

        self.messageLabel = QtWidgets.QLabel()
        self.messageLabel.setObjectName("messageLabel")
        message_font = QtGui.QFont()
        message_font.setPixelSize(20)
        self.messageLabel.setFont(message_font)
        self.messageLabel.setWordWrap(True)
        # Text for the purpose of ensuring the scroll is both functioning and aligned
        test = "This is the Scroll test message the goes on and on. " * 100
        self.messageLabel.setText(test)
        self.scrolllayout.addWidget(self.messageLabel)

        # Row 3 -- Logo -- Signiture
        self.hlr3 = QtWidgets.QHBoxLayout()
        self.hlr3.setObjectName("hlr3")
        self.gridLayout.addLayout(self.hlr3, 3, 1, 1, 4, alignment=QtCore.Qt.Alignment())

        self.signatureLSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hlr3.addItem(self.signatureLSpacer)

        self.logoImage = QtWidgets.QLabel()
        self.logoImage.setObjectName("logoImage")
        Image = QPixmap('Resources/AF Logo.png')
        logoAdjustment = Image.scaled(125, 125)
        self.logoImage.setPixmap(logoAdjustment)
        self.logoImage.setSizePolicy(sizePolicy)
        self.hlr3.addWidget(self.logoImage)

        self.signaturelabel = QtWidgets.QLabel()
        self.signaturelabel.setObjectName("signaturelabel")
        signature_font = QtGui.QFont()
        signature_font.setPixelSize(24)
        signature_font.setBold(True)
        self.signaturelabel.setFont(signature_font)
        self.signaturelabel.setSizePolicy(sizePolicy)
        self.signaturelabel.setAlignment(QtCore.Qt.AlignLeft)
        self.signaturelabel.setText("""Your Grateful Software Developer,\nBeaker Labs LLC\nContact@beakerlabstech.com""")
        self.hlr3.addWidget(self.signaturelabel)

        self.signatureRspacer = QtWidgets.QSpacerItem(int((adjusted_height - 90)/2) - 10, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hlr3.addItem(self.signatureRspacer)

        # Row 4 -- Spacer -- Spacer -- Button -- Button
        self.hlr4 = QtWidgets.QHBoxLayout()
        self.hlr4.setObjectName("hlr4")
        self.gridLayout.addLayout(self.hlr4, 4, 1, 1, 4, alignment=QtCore.Qt.Alignment())

        buttonSpacer_width = int((adjusted_height - 90)/2) - 10

        self.buttonLSpacer = QtWidgets.QSpacerItem(buttonSpacer_width, 50, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hlr4.addItem(self.buttonLSpacer)
        
        pushbuttonSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        pushbuttonSizePolicy.retainSizeWhenHidden()

        pusbutton_width = (adjusted_height - buttonSpacer_width) / 2

        self.pushButtonNext = QtWidgets.QPushButton()
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.pushButtonNext.setText("Next")
        pushbutton_font = QtGui.QFont()
        pushbutton_font.setPixelSize(16)
        self.pushButtonNext.setFont(pushbutton_font)
        self.pushButtonNext.setSizePolicy(pushbuttonSizePolicy)
        self.pushButtonNext.setFixedWidth(pusbutton_width)
        self.hlr4.addWidget(self.pushButtonNext)

        self.pushButtonClose = QtWidgets.QPushButton()
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.pushButtonClose.setText("Close")
        self.pushButtonClose.setFont(pushbutton_font)
        self.pushButtonClose.setSizePolicy(pushbuttonSizePolicy)
        self.pushButtonClose.setFixedWidth(pusbutton_width)
        self.hlr4.addWidget(self.pushButtonClose)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
