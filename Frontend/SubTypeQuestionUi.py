#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_YNCInput(object):  # YNC == Yes No Cancel
    def setupUi(self, Dialog):
        Dialog.setObjectName("YNCInput")
        Dialog.setWindowTitle("Modify -- Account Types")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        # This dialog size will be constant. Unlike other screens it should always fit.
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(600, 200)  # width x height
        Dialog.setMinimumSize(QtCore.QSize(300, 150))
        Dialog.setMaximumSize(QtCore.QSize(600, 200))

        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        # Row 1 -- Spacer (C1-C5)
        self.vhspacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.vhspacer1, 1, 1, 1, 1)

        # Row 2 -- Label (C2-C4) Spacer (C5)
        input_font = QtGui.QFont()
        input_font.setPixelSize(16)

        self.InputLabel = QtWidgets.QLabel()
        self.InputLabel.setObjectName("InputLabel")
        self.InputLabel.setFont(input_font)
        self.InputLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.InputLabel.setWordWrap(True)
        self.gridLayout.addWidget(self.InputLabel, 2, 2, 1, 3)

        # Spacer was not required. The other spacers cover the other 3 rows.
        # The label will fill the extra space accordingly

        # Row 3 -- Spacer (C1) Pushbutton (C2) Pushbutton (C3) Pushbutton (C4)
        self.vspacer1 = QtWidgets.QSpacerItem(0, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.vspacer1, 3, 1, 1, 1)

        button_font = QtGui.QFont()
        button_font.setPixelSize(14)

        self.pBAdd = QtWidgets.QPushButton()
        self.pBAdd.setObjectName("addPushButton")
        self.pBAdd.setText("Add")
        self.pBAdd.setFont(button_font)
        self.gridLayout.addWidget(self.pBAdd, 3, 2, 1, 1)

        self.pBRemove = QtWidgets.QPushButton()
        self.pBRemove.setObjectName("removePushButton")
        self.pBRemove.setText("Remove")
        self.pBRemove.setFont(button_font)
        self.gridLayout.addWidget(self.pBRemove, 3, 3, 1, 1)

        self.pBCancel = QtWidgets.QPushButton()
        self.pBCancel.setObjectName("cancelPushButton")
        self.pBCancel.setText("Cancel")
        self.pBCancel.setFont(button_font)
        self.gridLayout.addWidget(self.pBCancel, 3, 4, 1, 1)

        # Row 4 -- Spacer (C5)
        self.vhspacer2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.vhspacer2, 4, 5, 1, 1)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
