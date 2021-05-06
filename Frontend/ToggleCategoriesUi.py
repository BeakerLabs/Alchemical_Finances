#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

# Dialog screen for use to determine what categories are used to calculate spending habits
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMainWindow, QDialog, QApplication, QLayout


class Ui_ToggleCategories(object):
    def setupUi(self, Dialog):
        # Dialog Settings
        Dialog.setObjectName("Toggle_Categories")
        Dialog.setWindowTitle("Toggle Categories")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        Dialog.resize(600, 300)
        Dialog.setMinimumSize(600, 300)
        Dialog.setMaximumSize(600, 400)

        header_font = QtGui.QFont()
        header_font.setPixelSize(16)
        header_font.setBold(True)

        general_font = QtGui.QFont()
        general_font.setPixelSize(12)
        general_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.retainSizeWhenHidden()

        # Core Layout
        self.coreHBLayout = QtWidgets.QHBoxLayout(Dialog)
        self.coreHBLayout.setObjectName("Core")

        # hSpacer1 -- vBLayout1 -- hSpacer2
        self.hSpacer1 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.coreHBLayout.addItem(self.hSpacer1)

        self.vBLayout1 = QtWidgets.QVBoxLayout()
        self.coreHBLayout.addLayout(self.vBLayout1)

        self.hSpacer2 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.coreHBLayout.addItem(self.hSpacer2)

        # vBLayout1 --> vSpacer1 -- hBLayout2 -- vSpacer2 -- hBLayout3 -- hBLayout4 -- vSpacer3
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer1)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBLayout2")
        self.vBLayout1.addLayout(self.hBLayout2)

        self.vSpacer2 = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer2)

        self.hBLayout3 = QtWidgets.QHBoxLayout()
        self.hBLayout3.setObjectName("hBLayout3")
        self.vBLayout1.addLayout(self.hBLayout3)

        self.vSpacer3 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer3)

        self.hBLayout4 = QtWidgets.QHBoxLayout()
        self.hBLayout4.setObjectName("hBLayout4")
        self.vBLayout1.addLayout(self.hBLayout4)

        self.vSpacer4 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer4)

        # vBLayout1 --> hBLayout2 --> --> QLabel1 -- hSPacer3 -- QLabel2
        self.lActive = QtWidgets.QLabel()
        self.lActive.setObjectName("lActive")
        self.lActive.setText("Active")
        self.lActive.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.lActive.setFont(header_font)
        self.lActive.setSizePolicy(sizePolicy)
        self.hBLayout2.addWidget(self.lActive)

        self.hSpacer3 = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout2.addItem(self.hSpacer3)

        self.lInActive = QtWidgets.QLabel()
        self.lInActive.setObjectName("lInActive")
        self.lInActive.setText("Deactivated")
        self.lInActive.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.lInActive.setFont(header_font)
        self.lInActive.setSizePolicy(sizePolicy)
        self.hBLayout2.addWidget(self.lInActive)

        # vBLayout1 --> hBLayout3 --> --> hSpacer4 -- QListWidget -- vBLayout2 -- QLightWidget
        self.hSpacer4 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout3.addItem(self.hSpacer4)

        self.listWidgetActive = QtWidgets.QListWidget()
        self.listWidgetActive.setObjectName("listWidgetActive")
        self.listWidgetActive.setFont(general_font)
        self.listWidgetActive.setSortingEnabled(True)
        self.hBLayout3.addWidget(self.listWidgetActive)

        self.vBLayout2 = QtWidgets.QVBoxLayout()
        self.vBLayout2.setObjectName("vBLayout2")
        self.hBLayout3.addLayout(self.vBLayout2)

        self.listWidgetDeactivated = QtWidgets.QListWidget()
        self.listWidgetDeactivated.setObjectName("listWidgetDeactivated")
        self.listWidgetDeactivated.setFont(general_font)
        self.listWidgetDeactivated.setSortingEnabled(True)
        self.hBLayout3. addWidget(self.listWidgetDeactivated)

        # vBLayout2 --> hSpacer5 -- QPushButton1 -- QPushButton2
        self.hSpacer5 = QtWidgets.QSpacerItem(100, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vBLayout2.addItem(self.hSpacer5)

        # self.hSpacer5 = QtWidgets.QSpacerItem(width, vertical, hor, vert)

        self.pBToggleOn = QtWidgets.QPushButton()
        self.pBToggleOn.setObjectName("pBToggleOn")
        self.pBToggleOn.setText("<<<")
        self.pBToggleOn.setFont(header_font)
        self.vBLayout2.addWidget(self.pBToggleOn)

        self.pBToggleOff = QtWidgets.QPushButton()
        self.pBToggleOff.setObjectName("pBToggleOff")
        self.pBToggleOff.setText(">>>")
        self.pBToggleOff.setFont(header_font)
        self.vBLayout2.addWidget(self.pBToggleOff)

        self.vSpacer5 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vBLayout2.addItem(self.vSpacer5)

        # HBLayout4 --> hSpacer6 -- pBSave -- pBCancel
        self.hSpacer5 = QtWidgets.QSpacerItem(100, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout4.addItem(self.hSpacer5)

        self.pBSave = QtWidgets.QPushButton()
        self.pBSave.setObjectName("pBSave")
        self.pBSave.setText("Save")
        self.pBSave.setFixedWidth(100)
        self.pBSave.setFont(general_font)
        self.hBLayout4.addWidget(self.pBSave)

        self.pBClose = QtWidgets.QPushButton()
        self.pBClose.setObjectName("pBClose")
        self.pBClose.setText("Close")
        self.pBClose.setFixedWidth(100)
        self.pBClose.setFont(general_font)
        self.hBLayout4.addWidget(self.pBClose)


if __name__ == "__main__":
    print("error")

