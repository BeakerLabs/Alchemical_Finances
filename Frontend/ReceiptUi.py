#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

# Dialog for user to load images within the program.

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Receipt(object):
    def setupUi(self, Dialog):
        # Dialog Setting
        Dialog.setObjectName("ReceiptDialog")
        Dialog.setWindowTitle("Receipt")
        Dialog.setWindowIcon(QtGui.QIcon("AF Logo.png"))

        Dialog.resize(600, 700)
        Dialog.setMinimumSize(600, 700)
        Dialog.setMaximumSize(800, 950)

        # Core gridlayout
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        # Font and Size Policy
        general_font = QtGui.QFont()
        general_font.setPointSize(12)
        general_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.retainSizeWhenHidden()

        # Row 1 -- HVSpacer1 (C1) -- HSpacer1 (C2) -- HSpacer2 (C3)
        self.hVSpacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer1, 1, 1, 1, 1)

        self.hSpacer1 = QtWidgets.QSpacerItem(290, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hSpacer1, 1, 2, 1, 1)

        self.hSpacer2 = QtWidgets.QSpacerItem(290, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hSpacer2, 1, 3, 1, 1)

        # Row 2 -- Label (C2-3)
        self.lRName = QtWidgets.QLabel()
        self.lRName.setObjectName("lRName")
        self.lRName.setText("Placeholder Text")
        self.lRName.setAlignment(QtCore.Qt.AlignLeft)
        self.lRName.setFont(general_font)
        self.lRName.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lRName, 2, 2, 1, 2)

        # Row 3 -- Label (C2-3)
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 600, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(self.vSpacer1, 3, 1, 1, 1)

        self.imageScroll = QtWidgets.QScrollArea()
        self.imageScroll.setObjectName("imageScroll")
        self.imageScroll.horizontalScrollBar().setEnabled(True)
        self.imageScroll.verticalScrollBar().setEnabled(True)
        self.imageScroll.setFrameStyle(1)
        self.gridLayout.addWidget(self.imageScroll, 3, 2, 1, 2)

        widget = QtWidgets.QWidget()
        self.imageScroll.setWidget(widget)
        self.imageScroll.setWidgetResizable(True)
        self.imageLayout = QtWidgets.QHBoxLayout(widget)

        self.lRImage = QtWidgets.QLabel()
        self.lRImage.setObjectName("LRImage")
        text = "The image goes here, and here, and here \n" * 100
        self.lRImage.setText(text)
        self.lRImage.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.imageLayout.addWidget(self.lRImage)


        # Row 4 -- pBRotate CounterClockwise(C2) -- pBRotate Clockwise (C3)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.gridLayout.addLayout(self.buttonLayout, 4, 2, 1, 2, alignment=QtCore.Qt.Alignment())

        self.pBRotateCC = QtWidgets.QPushButton()
        self.pBRotateCC.setObjectName("pBRotate")
        self.pBRotateCC.setText("Rotate CC")
        self.pBRotateCC.setFont(general_font)
        self.pBRotateCC.setSizePolicy(sizePolicy)
        self.buttonLayout.addWidget(self.pBRotateCC)
        # self.gridLayout.addWidget(self.pBRotateCC, 4, 2, 1, 1)

        self.pBZoomIn = QtWidgets.QPushButton()
        self.pBZoomIn.setObjectName("pBZoomIn")
        self.pBZoomIn.setText("Enlarge Image")
        self.pBZoomIn.setFont(general_font)
        self.pBZoomIn.setSizePolicy(sizePolicy)
        self.buttonLayout.addWidget(self.pBZoomIn)

        self.pBZoomOut = QtWidgets.QPushButton()
        self.pBZoomOut.setObjectName("pBZoomOut")
        self.pBZoomOut.setText("Shrink Image")
        self.pBZoomOut.setFont(general_font)
        self.pBZoomOut.setSizePolicy(sizePolicy)
        self.buttonLayout.addWidget(self.pBZoomOut)

        self.pBRotateC = QtWidgets.QPushButton()
        self.pBRotateC.setObjectName("pBRotate")
        self.pBRotateC.setText("Rotate C")
        self.pBRotateC.setFont(general_font)
        self.pBRotateC.setSizePolicy(sizePolicy)
        self.buttonLayout.addWidget(self.pBRotateC)
        # self.gridLayout.addWidget(self.pBRotateC, 4, 3, 1, 1)

        # Row 5 -- HVSpacer2 (C4)
        self.hVSpacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hVSpacer1, 5, 4, 1, 1)


if __name__ == "__main__":
    print("error")
