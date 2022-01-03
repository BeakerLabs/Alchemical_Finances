#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

# Dialog screen for user to set parameters to generate a .pdf snapshot report

import os
import sys

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_GenReport(object):
    def setupUi(self, Dialog):
        pass
        # Dialog Settings
        Dialog.setObjectName("GenReport")
        Dialog.setWindowTitle("Generate Report")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        Dialog.resize(285, 500)
        Dialog.setMinimumSize(285, 500)
        Dialog.setMaximumSize(285, 500)

        # Core GridLayout (eight Columns)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        # Fonts and Size Policy
        groupBox_font = QtGui.QFont()
        groupBox_font.setPixelSize(16)
        groupBox_font.setBold(True)

        parentType_font = QtGui.QFont()
        parentType_font.setPixelSize(12)
        parentType_font.setBold(False)

        general_font = QtGui.QFont()
        general_font.setPixelSize(12)
        general_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.retainSizeWhenHidden()

        pB_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        # Row 1 -- hvSpacer1 (C1)
        self.hVSpacer1 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer1, 1, 1, 1, 1)

        # Row 2 -- Group Box (C2-7)
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFont(groupBox_font)
        self.groupBox.setTitle("Account Types")
        self.gridLayout.addWidget(self.groupBox, 2, 2, 1, 6)

        # Row 2A -- VBoxLayout1
        self.vBLayout1 = QtWidgets.QVBoxLayout(self.groupBox)
        self.vBLayout1.setObjectName("vBLayout1")

        # Row 2AA -- 1AI ParentType Check Boxes
        # Bank
        self.cBBank = QtWidgets.QCheckBox()
        self.cBBank.setObjectName("cBBank")
        self.cBBank.setChecked(True)
        self.cBBank.setFont(parentType_font)
        self.cBBank.setText("Bank")
        self.vBLayout1.addWidget(self.cBBank)

        # Cash
        self.cBCash = QtWidgets.QCheckBox()
        self.cBCash.setObjectName("cBCash")
        self.cBCash.setChecked(True)
        self.cBCash.setFont(parentType_font)
        self.cBCash.setText("Cash")
        self.vBLayout1.addWidget(self.cBCash)

        # Certificates of Deposit
        self.cBCD = QtWidgets.QCheckBox()
        self.cBCD.setObjectName("cBCD")
        self.cBCD.setChecked(True)
        self.cBCD.setFont(parentType_font)
        self.cBCD.setText("Certificate of Deposit")
        self.vBLayout1.addWidget(self.cBCD)

        # Credit Cards
        self.cBCC = QtWidgets.QCheckBox()
        self.cBCC.setObjectName("cBCC")
        self.cBCC.setChecked(True)
        self.cBCC.setFont(parentType_font)
        self.cBCC.setText("Credit Cards")
        self.vBLayout1.addWidget(self.cBCC)

        # Debt
        self.cBDebt = QtWidgets.QCheckBox()
        self.cBDebt.setObjectName("cBDebt")
        self.cBDebt.setChecked(True)
        self.cBDebt.setFont(parentType_font)
        self.cBDebt.setText("Debt")
        self.vBLayout1.addWidget(self.cBDebt)

        # Equity
        self.cBEquity = QtWidgets.QCheckBox()
        self.cBEquity.setObjectName("cBEquity")
        self.cBEquity.setChecked(True)
        self.cBEquity.setFont(parentType_font)
        self.cBEquity.setText("Equity")
        self.vBLayout1.addWidget(self.cBEquity)

        # Property
        self.cBProperty = QtWidgets.QCheckBox()
        self.cBProperty.setObjectName("cBProperty")
        self.cBProperty.setChecked(True)
        self.cBProperty.setFont(parentType_font)
        self.cBProperty.setText("Property")
        self.vBLayout1.addWidget(self.cBProperty)

        # Treasury Bonds
        self.cBTreasury = QtWidgets.QCheckBox()
        self.cBTreasury.setObjectName("cBTreasury")
        self.cBTreasury.setChecked(True)
        self.cBTreasury.setFont(parentType_font)
        self.cBTreasury.setText("Treasury")
        self.vBLayout1.addWidget(self.cBTreasury)

        # Retirement Accounts
        self.cBRetirement = QtWidgets.QCheckBox()
        self.cBRetirement.setObjectName("cBRetirement")
        self.cBRetirement.setChecked(True)
        self.cBRetirement.setFont(parentType_font)
        self.cBRetirement.setText("Retirement")
        self.vBLayout1.addWidget(self.cBRetirement)

        # Row 3 -- pBSelect (C2-4) -- pBDeselect (C5-7)
        self.pBSelect = QtWidgets.QPushButton()
        self.pBSelect.setObjectName("pBSelect")
        self.pBSelect.setText("Select All")
        self.pBSelect.setFont(general_font)
        self.pBSelect.setMaximumWidth(135)
        self.pBSelect.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBSelect, 3, 2, 1, 3)

        self.pBDeselect = QtWidgets.QPushButton()
        self.pBDeselect.setObjectName("pBDseelect")
        self.pBDeselect.setText("Deselect All")
        self.pBDeselect.setFont(general_font)
        self.pBDeselect.setMaximumWidth(130)
        self.pBDeselect.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBDeselect, 3, 5, 1, 3)

        # Row 4 -- Label (C2-6) -- HSpacer (C7)
        self.lDestination = QtWidgets.QLabel()
        self.lDestination.setObjectName("lDestination")
        self.lDestination.setText("Report Destination")
        self.lDestination.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.lDestination.setFont(general_font)
        self.lDestination.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lDestination, 4, 2, 1, 6)

        self.hSpacer3 = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hSpacer3, 4, 7, 1, 1)

        # Row 5 -- LineEdit (C2-6) -- pBPathway (C7)
        self.lEditPath = QtWidgets.QLineEdit()
        self.lEditPath.setObjectName("lEditPath")
        self.lEditPath.setEnabled(True)
        self.lEditPath.setFont(general_font)
        self.lEditPath.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lEditPath, 5, 2, 1, 5)

        self.pBPath = QtWidgets.QPushButton()
        self.pBPath.setObjectName("pBPath")
        self.pBPath.setText("...")
        self.pBPath.setFont(general_font)
        self.pBPath.setMaximumWidth(60)
        self.pBPath.setSizePolicy(pB_sizePolicy)
        self.gridLayout.addWidget(self.pBPath, 5, 7, 1, 1)

        # Row 6 -- pBGenerate Report
        self.pBGenerate = QtWidgets.QPushButton()
        self.pBGenerate.setObjectName("pBGenerate")
        self.pBGenerate.setText("Generate Report")
        self.pBGenerate.setFont(general_font)
        self.pBGenerate.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.pBGenerate, 6, 2, 1, 6)

        # Row 7 -- hvSpacer2 (c8)
        self.hVSpacer2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # Row, Column, RowSpan, ColSpan
        self.gridLayout.addItem(self.hVSpacer2, 7, 8, 1, 1)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
