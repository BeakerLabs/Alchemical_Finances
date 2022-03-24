#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Accounts(object):
    def setupUi(self, Dialog):
        # Dialog Settings
        Dialog.setObjectName("accountDialog")
        Dialog.setWindowTitle("Accounts")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        Dialog.resize(400, 550)
        Dialog.setMinimumSize(QtCore.QSize(400, 550))
        Dialog.setMaximumSize(QtCore.QSize(500, 688))

        # Central Widget and Gridlayout
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridlayout")

        # Fonts and SizePolicy
        label_font = QtGui.QFont()
        label_font.setPixelSize(16)
        label_font.setBold(True)

        general_font = QtGui.QFont()
        general_font.setPixelSize(16)

        lineEdit_font = QtGui.QFont()
        lineEdit_font.setPixelSize(16)
        lineEdit_font.setBold(False)

        error_font = QtGui.QFont()
        error_font.setPixelSize(16)
        error_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.retainSizeWhenHidden()

        button_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        label_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # Row 1 -- HVSPacer1 (C1)
        self.hVSpacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer1, 1, 1, 1, 1)

        # Row 2 -- Horizontal Layout (C2-5)
        self.hBLayout = QtWidgets.QHBoxLayout()
        self.hBLayout.setObjectName("hBLayout")
        self.gridLayout.addLayout(self.hBLayout, 2, 2, 1, 4)

        # Row 2A -- Vertical Layout
        self.vBLayout = QtWidgets.QVBoxLayout()
        self.vBLayout.setObjectName("vBLayout")
        self.hBLayout.addLayout(self.vBLayout)

        # Row 2AA -- 4x PushButton -- HVSpacer2
        self.pBNew = QtWidgets.QPushButton()
        self.pBNew.setObjectName("pBNew")
        self.pBNew.setText("New")
        self.pBNew.setFont(general_font)
        self.pBNew.setFixedWidth(135)
        self.pBNew.setSizePolicy(button_sizePolicy)
        self.vBLayout.addWidget(self.pBNew)

        self.pBEdit = QtWidgets.QPushButton()
        self.pBEdit.setObjectName("pbEdit")
        self.pBEdit.setText("Edit")
        self.pBEdit.setFont(general_font)
        self.pBEdit.setFixedWidth(135)
        self.pBEdit.setSizePolicy(button_sizePolicy)
        self.vBLayout.addWidget(self.pBEdit)

        self.pBDelete = QtWidgets.QPushButton()
        self.pBDelete.setObjectName("pBDelete")
        self.pBDelete.setText("Delete")
        self.pBDelete.setFont(general_font)
        self.pBDelete.setFixedWidth(135)
        self.pBDelete.setSizePolicy(button_sizePolicy)
        self.vBLayout.addWidget(self.pBDelete)

        self.pBArchive = QtWidgets.QPushButton()
        self.pBArchive.setObjectName("pBArchive")
        self.pBArchive.setText("Archive")
        self.pBArchive.setFont(general_font)
        self.pBArchive.setFixedWidth(135)
        self.pBArchive.setSizePolicy(button_sizePolicy)
        self.vBLayout.addWidget(self.pBArchive)

        self.hVSpacer2 = QtWidgets.QSpacerItem(130, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.vBLayout.addItem(self.hVSpacer2)

        # Row 2B -- Listview
        self.listWidgetAccount = QtWidgets.QListWidget(Dialog)
        self.listWidgetAccount.setObjectName("listWidgetAccount")
        self.listWidgetAccount.setFont(general_font)
        self.hBLayout.addWidget(self.listWidgetAccount)

        # Row 3 -- V Spacer (C2) -- V Spacer(C3) -- V Spacer(C4) -- VSpacer(C5)
        self.hspacer1 = QtWidgets.QSpacerItem(130, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hspacer1, 3, 2, 1, 1)

        self.hspacer2 = QtWidgets.QSpacerItem(90, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(self.hspacer2, 3, 3, 1, 1)

        self.hspacer3 = QtWidgets.QSpacerItem(80, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(self.hspacer3, 3, 4, 1, 1)

        self.hspacer4 = QtWidgets.QSpacerItem(80, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(self.hspacer4, 3, 5, 1, 1)

        # Row 4 -- label (C2) -- LineEdit (C3-5)
        self.lAccountName = QtWidgets.QLabel()
        self.lAccountName.setObjectName("lAccountName")
        self.lAccountName.setText("Account Name: ")
        self.lAccountName.setFont(label_font)
        self.lAccountName.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lAccountName.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lAccountName, 4, 2, 1, 1)

        self.lEditAN = QtWidgets.QLineEdit()
        self.lEditAN.setObjectName("lEditAN")
        self.lEditAN.setEnabled(False)
        self.lEditAN.setFont(lineEdit_font)
        self.lEditAN.setSizePolicy(sizePolicy)
        self.lEditAN.setMaxLength(38)
        self.gridLayout.addWidget(self.lEditAN, 4, 3, 1, 3)

        # Row 5 -- label (C2) -- ComboBox (C3-4) -- Pushbutton (C5)
        self.lAccountType = QtWidgets.QLabel()
        self.lAccountType.setObjectName("lAccountType")
        self.lAccountType.setText("Account Type: ")
        self.lAccountType.setFont(label_font)
        self.lAccountType.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lAccountType.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lAccountType, 5, 2, 1, 1)

        self.comboboxAT = QtWidgets.QComboBox()
        self.comboboxAT.setObjectName("ComboboxAT")
        self.comboboxAT.setFont(general_font)
        self.comboboxAT.setSizePolicy(sizePolicy)
        self.comboboxAT.setEnabled(False)
        self.gridLayout.addWidget(self.comboboxAT, 5, 3, 1, 2)

        self.pBModify = QtWidgets.QPushButton()
        self.pBModify.setObjectName("pBModify")
        self.pBModify.setText("Modify")
        self.pBModify.setFont(general_font)
        self.pBModify.setSizePolicy(sizePolicy)
        self.pBModify.setEnabled(False)
        self.gridLayout.addWidget(self.pBModify, 5, 5, 1, 1)

        # Row 6 - label(C2) -- Combobox(C3-5)
        self.lSector = QtWidgets.QLabel()
        self.lSector.setObjectName("lSector")
        self.lSector.setText("Sector: ")
        self.lSector.setFont(label_font)
        self.lSector.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lSector.setMinimumWidth(127)
        self.lSector.setSizePolicy(label_sizePolicy)
        self.lSector.setHidden(True)
        self.gridLayout.addWidget(self.lSector, 6, 2, 1, 1)

        # Ledger 2 - ParentType = Equity
        sectorList = ["Information Technology", "Health Care", "Financial", "Consumer Discretionary", "Communication",
                      "Industrial", "Consumer Staples", "Energy", "Real Estate", "Materials", "Broad Market", "Unspecified"]

        self.comboboxSector = QtWidgets.QComboBox()
        self.comboboxSector.setObjectName("comboboxSector")
        self.comboboxSector.setEnabled(False)
        self.comboboxSector.setHidden(True)
        self.comboboxSector.setFont(general_font)
        self.comboboxSector.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.comboboxSector, 6, 3, 1, 3)

        self.comboboxSector.addItems(sectorList)
        self.comboboxSector.model().sort(0)
        self.comboboxSector.setCurrentIndex(0)

        # Row 7 --- label (C2) -- LineEdit (C3-5)
        self.lPrimaryOwner = QtWidgets.QLabel()
        self.lPrimaryOwner.setObjectName("lPrimaryOwner")
        self.lPrimaryOwner.setText("Primary Owner: ")
        self.lPrimaryOwner.setFont(label_font)
        self.lPrimaryOwner.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lPrimaryOwner.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lPrimaryOwner, 7, 2, 1, 1)

        self.lEditPO = QtWidgets.QLineEdit()
        self.lEditPO.setObjectName("lEditPO")
        self.lEditPO.setEnabled(False)
        self.lEditPO.setFont(lineEdit_font)
        self.lEditPO.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lEditPO, 7, 3, 1, 3)

        # Row 8 -- label (C2) -- LineEdit (C3-5)
        self.lBank = QtWidgets.QLabel()
        self.lBank.setObjectName("lBank")
        self.lBank.setText("Bank: ")
        self.lBank.setFont(label_font)
        self.lBank.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lBank.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lBank, 8, 2, 1, 1)

        self.lEditB = QtWidgets.QLineEdit()
        self.lEditB.setObjectName("lEditB")
        self.lEditB.setEnabled(False)
        self.lEditB.setFont(lineEdit_font)
        self.lEditB.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lEditB, 8, 3, 1, 3)

        # Row 9 -- label (C2) -- LineEdit (C3-5)
        self.lStatement = QtWidgets.QLabel()
        self.lStatement.setObjectName("lStatement")
        self.lStatement.setText("Statement Date: ")
        self.lStatement.setFont(label_font)
        self.lStatement.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lStatement.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lStatement, 9, 2, 1, 1)

        self.spinBStatement = QtWidgets.QSpinBox()
        self.spinBStatement.setObjectName("lspinBStatement")
        self.spinBStatement.setMinimum(1)
        self.spinBStatement.setMaximum(31)
        self.spinBStatement.setSingleStep(1)
        self.spinBStatement.setEnabled(False)
        self.spinBStatement.setFont(lineEdit_font)
        self.spinBStatement.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.spinBStatement, 9, 3, 1, 3)

        # Row 10 -- label (C2) -- LineEdit (C3-5)
        self.lVariable1 = QtWidgets.QLabel()
        self.lVariable1.setObjectName("lVariable1")
        self.lVariable1.setText("Interest Rate: ")
        self.lVariable1.setFont(label_font)
        self.lVariable1.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lVariable1.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lVariable1, 10, 2, 1, 1)

        self.lEditV1 = QtWidgets.QLineEdit()
        self.lEditV1.setObjectName("lEditV1")
        self.lEditV1.setEnabled(False)
        self.lEditV1.setFont(lineEdit_font)
        self.lEditV1.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lEditV1, 10, 3, 1, 3)

        # Row 11 -- label (C2) -- LineEdit (C3-5)
        self.lVariable2 = QtWidgets.QLabel()
        self.lVariable2.setObjectName("lVariable2")
        self.lVariable2.setText("County, St Zip: ")
        self.lVariable2.setFont(label_font)
        self.lVariable2.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lVariable2.setMinimumWidth(127)
        self.lVariable2.setSizePolicy(label_sizePolicy)
        self.gridLayout.addWidget(self.lVariable2, 11, 2, 1, 1)

        self.r10HBLayout = QtWidgets.QHBoxLayout()
        self.r10HBLayout.setObjectName("r10HBLayout")
        self.gridLayout.addLayout(self.r10HBLayout, 11, 3, 1, 3, alignment=QtCore.Qt.Alignment())

        self.lEditV2 = QtWidgets.QLineEdit()
        self.lEditV2.setObjectName("lEditV2")
        self.lEditV2.setEnabled(False)
        self.lEditV2.setFont(lineEdit_font)
        self.lEditV2.setSizePolicy(sizePolicy)
        self.r10HBLayout.addWidget(self.lEditV2)

        # Ledger 1 - Parentype = Property
        self.comboboxState = QtWidgets.QComboBox()
        self.comboboxState.setObjectName("comboboxState")
        self.comboboxState.setEnabled(False)
        self.comboboxState.setHidden(True)
        self.comboboxState.setFont(general_font)
        self.comboboxState.setSizePolicy(sizePolicy)
        self.r10HBLayout.addWidget(self.comboboxState)

        stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        self.comboboxState.addItems(stateList)
        self.comboboxState.model().sort(0)
        self.comboboxState.setCurrentIndex(0)

        self.lEZipCode = QtWidgets.QLineEdit()
        self.lEZipCode.setObjectName("lEditV2")
        self.lEZipCode.setEnabled(False)
        self.lEZipCode.setHidden(True)
        self.lEZipCode.setFont(lineEdit_font)
        self.lEZipCode.setSizePolicy(sizePolicy)
        self.r10HBLayout.addWidget(self.lEZipCode)

        # Row 12 -- label (C2-3) -- PushButton (C4-5)
        self.lError = QtWidgets.QLabel()
        self.lError.setObjectName("lError")
        self.lError.setText("")
        self.lError.setFont(error_font)
        self.lError.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.lError.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lError, 12, 2, 1, 2)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBLayout2")
        self.gridLayout.addLayout(self.hBLayout2, 12, 4, 1, 2, alignment=QtCore.Qt.Alignment())

        self.pBSubmit = QtWidgets.QPushButton()
        self.pBSubmit.setObjectName("pBSubmit")
        self.pBSubmit.setText("Submit")
        self.pBSubmit.setFont(general_font)
        self.pBSubmit.setSizePolicy(sizePolicy)
        self.pBSubmit.setEnabled(False)
        self.hBLayout2.addWidget(self.pBSubmit)

        self.pBEditSubmit = QtWidgets.QPushButton()
        self.pBEditSubmit.setObjectName("pBEditSumbit")
        self.pBEditSubmit.setText("Submit Edit")
        self.pBEditSubmit.setFont(general_font)
        self.pBEditSubmit.setSizePolicy(sizePolicy)
        self.pBEditSubmit.setEnabled(False)
        self.pBEditSubmit.setHidden(True)
        self.hBLayout2.addWidget(self.pBEditSubmit)

        # Row 13 -- HVSpacer3 (C6)
        self.hVSpacer3 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer3, 13, 6, 1, 1)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")

