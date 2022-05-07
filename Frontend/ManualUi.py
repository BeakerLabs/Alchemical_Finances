#  Copyright (c) 2022 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from pathlib import Path
from PySide6 import QtCore, QtGui, QtWidgets

from Toolbox.OS_Tools import obtain_screen_dimensions, file_destination

class Ui_UserManual(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("UserManual")
        Dialog.setWindowTitle("Alchemical Finances")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        # Obtain and use the monitor screen to determine the size of the dialog box
        screen_dimensions, _ = obtain_screen_dimensions()
        # reference full screen not MDI area.
        work_area = screen_dimensions[0]

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
        adjusted_width = (work_area[2] * size_factor) + modifier

        # Making the Message screen larger than log in but not full screen.
        # Rational - Make it catch the users eye
        Dialog.resize(adjusted_width, adjusted_height)

        title_font = QtGui.QFont()
        title_font.setPixelSize(36)
        title_font.setBold(True)

        general_font = QtGui.QFont()
        general_font.setPixelSize(14)
        general_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(int(adjusted_height), int(adjusted_height)))
        Dialog.setMaximumSize(QtCore.QSize(int(adjusted_height), int(adjusted_height)))

        self.outsideFrame = QtWidgets.QFrame(Dialog)
        self.outsideFrame.setObjectName("ousideFrame")
        # self.outsideFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.outsideFrame.setLineWidth(1)
        self.outsideFrame.setGeometry(40, 40, adjusted_height - 90, adjusted_height - 90)

        self.gridLayout = QtWidgets.QGridLayout(self.outsideFrame)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.gridLayout.setObjectName("gridLayout")

        self.RowCounter = 1
        # Row 1 -- Manual Label
        self.vlr1 = QtWidgets.QVBoxLayout()
        self.vlr1.setObjectName("vlr1")
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addLayout(self.vlr1, self.RowCounter, 1, 1, 3, alignment=QtCore.Qt.Alignment())

        self.hlr1 = QtWidgets.QHBoxLayout()
        self.hlr1.setObjectName("hlr1")
        self.vlr1.addLayout(self.hlr1)

        self.labelTitle = QtWidgets.QLabel()
        self.labelTitle.setObjectName("labelTitle")
        self.labelTitle.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.labelTitle.setFont(title_font)
        label_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        label_sizePolicy.setHorizontalStretch(0)
        label_sizePolicy.setVerticalStretch(0)
        self.labelTitle.setSizePolicy(label_sizePolicy)
        # Development purposes only
        self.labelTitle.setText("User Manual")
        self.hlr1.addWidget(self.labelTitle)

        self.RowCounter += 1
        # Row 2 -- Spacer
        self.hVSpacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer1, self.RowCounter, 1, 1, 3)

        self.RowCounter += 1
        # Row 3 -- QVBoxLayout -- QSpacer -- QTextEdit
        self.vlr3c1 = QtWidgets.QVBoxLayout()
        self.vlr3c1.setObjectName("vlr3c1")
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addLayout(self.vlr3c1, self.RowCounter, 1, 1, 1, alignment=QtCore.Qt.Alignment())

        self.widgetSpacer = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(self.widgetSpacer, self.RowCounter, 2, 1, 1)

        self.textEditDisplay = QtWidgets.QTextEdit()
        self.textEditDisplay.setObjectName("textEditDisplay")
        self.textEditDisplay.setFont(general_font)
        self.gridLayout.addWidget(self.textEditDisplay, self.RowCounter, 3, 1, 1)

        # vlr3c1 --> List Widget -- Spacer
        self.listWidgetTopics = QtWidgets.QListWidget()
        self.listWidgetTopics.setObjectName("listWidgetTopics")
        self.listWidgetTopics.setMaximumWidth(200)
        self.listWidgetTopics.setMaximumHeight(300)
        self.vlr3c1.addWidget(self.listWidgetTopics)

        self.listWidgetSpacer = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vlr3c1.addItem(self.listWidgetSpacer)

        self.pBClose = QtWidgets.QPushButton()
        self.pBClose.setObjectName("pBClose")
        self.pBClose.setText("Close Manual")
        self.pBClose.setFont(general_font)
        button_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pBClose.setSizePolicy(button_sizePolicy)
        self.pBClose.setFixedHeight(45)
        self.pBClose.setFixedWidth(200)
        self.vlr3c1.addWidget(self.pBClose)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")