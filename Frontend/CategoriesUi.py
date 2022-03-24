#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Categories(object):
    def setupUi(self, Dialog):
        # Dialog Settings
        Dialog.setObjectName("categoriesDialog")
        Dialog.setWindowTitle("Spending Categories")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        Dialog.resize(285, 430)
        Dialog.setMinimumSize(285, 430)
        Dialog.setMaximumSize(285, 580)

        # Core GridLayout
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridlayout")

        # Fonts and Size Policy
        header_font = QtGui.QFont()
        header_font.setPixelSize(18)
        header_font.setBold(True)

        subheader_font = QtGui.QFont()
        subheader_font.setPixelSize(14)
        subheader_font.setBold(False)

        general_font = QtGui.QFont()
        general_font.setPixelSize(14)
        general_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.retainSizeWhenHidden()

        # Row 1 -- HVSpacer 1 (C1)
        self.hVSpacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer1, 1, 1, 1, 1)

        # Row 2 -- Label (C2-3)
        self.lparentType = QtWidgets.QLabel()
        self.lparentType.setObjectName("lparentType")
        self.lparentType.setText("Spending Categories")
        self.lparentType.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.lparentType.setFont(header_font)
        self.lparentType.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lparentType, 2, 2, 1, 2)

        # Row 3 -- Label (C2-3)
        self.lsubheader = QtWidgets.QLabel()
        self.lsubheader.setObjectName("lsubheader")
        self.lsubheader.setText("for {ParentType} Accounts")
        self.lsubheader.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
        self.lsubheader.setFont(subheader_font)
        self.lsubheader.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lsubheader, 3, 2, 1, 2)

        # Row 4 -- VSpacer1 (C1) -- ListWidget (C2-3)
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 400, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(self.vSpacer1, 4, 1, 1, 2)

        self.listWidgetCat = QtWidgets.QListWidget()
        self.listWidgetCat.setObjectName("listWidgetCat")
        self.listWidgetCat.setFont(general_font)
        self.gridLayout.addWidget(self.listWidgetCat, 4, 2, 1, 2)

        # Row 5 -- VSpacer2 (C1)
        self.vSpacer2 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.vSpacer2, 5, 1, 1, 1)

        # Row 6 -- Label (C2-3)
        self.lInstruction = QtWidgets.QLabel()
        self.lInstruction.setObjectName("lInstruction")
        self.lInstruction.setText("Selected spending category: ")
        self.lInstruction.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lInstruction.setFont(subheader_font)
        self.lInstruction.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lInstruction, 6, 2, 1, 2)

        # Row 7 -- LineEdit (C2-3)
        self.lEditSelection = QtWidgets.QLineEdit()
        self.lEditSelection.setObjectName("lEditSelection")
        self.lEditSelection.setEnabled(False)
        self.lEditSelection.setFont(general_font)
        self.lEditSelection.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lEditSelection, 7, 2, 1, 2)

        # Row 8 -- pBNew (C2) -- pBEdit (C3)
        self.pBNew = QtWidgets.QPushButton()
        self.pBNew.setObjectName("pBNew")
        self.pBNew.setText("New")
        self.pBNew.setFont(general_font)
        self.pBNew.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBNew, 8, 2, 1, 1)

        self.pBEdit = QtWidgets.QPushButton()
        self.pBEdit.setObjectName("pBEdit")
        self.pBEdit.setText("Edit")
        self.pBEdit.setFont(general_font)
        self.pBEdit.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBEdit, 8, 3, 1, 1)

        # Row 9 -- pBreplace (C2) -- pBDelete (C3)
        self.pBReplace = QtWidgets.QPushButton()
        self.pBReplace.setObjectName("pB")
        self.pBReplace.setText("Replace")
        self.pBReplace.setFont(general_font)
        self.pBReplace.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBReplace, 9, 2, 1, 1)

        self.pBDelete = QtWidgets.QPushButton()
        self.pBDelete.setObjectName("pB")
        self.pBDelete.setText("Delete")
        self.pBDelete.setFont(general_font)
        self.pBDelete.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBDelete, 9, 3, 1, 1)

        # Row 10 -- hBLayout(C2-3)
        self.hBLayout = QtWidgets.QHBoxLayout()
        self.hBLayout.setObjectName("hBLayout")
        self.gridLayout.addLayout(self.hBLayout, 10, 2, 1, 2, alignment=QtCore.Qt.Alignment())

        self.pBSubmit = QtWidgets.QPushButton()
        self.pBSubmit.setObjectName("pBSubmitNew")
        self.pBSubmit.setText("Submit")
        self.pBSubmit.setEnabled(False)
        self.pBSubmit.setHidden(True)
        self.pBSubmit.setFont(general_font)
        self.pBSubmit.setSizePolicy(sizePolicy)
        self.hBLayout.addWidget(self.pBSubmit)

        self.pBCancel = QtWidgets.QPushButton()
        self.pBCancel.setObjectName("pBCancel")
        self.pBCancel.setText("Cancel")
        self.pBCancel.setEnabled(False)
        self.pBCancel.setHidden(True)
        self.pBCancel.setFont(general_font)
        self.pBCancel.setSizePolicy(sizePolicy)
        self.hBLayout.addWidget(self.pBCancel)

        # Row 11 -- HVSpacer 2 (C4)
        self.hVSpacer2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer2, 11, 4, 1, 1)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
