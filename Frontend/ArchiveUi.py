#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

# MdiArea SubWindow -- Displays the ledgers for Archived Accounts
# Archived Accounts are accounts that have been closed.
# Archiving keeps the account history without it being apart of the summary report

import pickle

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Archive(object):
    def setupUi(self, Dialog):
        # Dialog Settings
        Dialog.setObjectName("ArchiveLedger")
        Dialog.setWindowTitle("Archive")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        # Dialog size
        screen_dimensions_file = open("Resources/dimensions.pkl", "rb")
        screen_dimensions = pickle.load(screen_dimensions_file)
        screen_dimensions_file.close()

        work_area = screen_dimensions[1]

        size_factor = 0.50

        if 3840 <= work_area[2]:
            size_factor = size_factor

        if 2560 <= work_area[2] < 3840:
            size_factor = (3840 * size_factor)/2560

        if 1920 <= work_area[2] < 2560:
            size_factor = (3840 * size_factor)/1920

        if 1600 <= work_area[2] < 1920:
            size_factor = (3840 * size_factor)/1600

        if work_area[2] < 1600:
            size_factor = (3840 * size_factor)/1366

        adjusted_width = work_area[2] * size_factor  # for non full screen sizing
        adjusted_height = work_area[3] * size_factor
        Dialog.resize(adjusted_width, adjusted_height)

        # Font and Size Policy
        general_font = QtGui.QFont()
        general_font.setPixelSize(18)
        general_font.setBold(False)

        pushButton_font = QtGui.QFont()
        pushButton_font.setPixelSize(12)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        pushButton_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        label_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # CentralWidget and hBLayout1
        # self.centralWidget = QtWidgets.QWidget(Dialog)
        # self.centralWidget.setObjectName("centralWidget")
        # Dialog.setCentralWidget(self.centralWidget)

        self.hBLayout1 = QtWidgets.QHBoxLayout(Dialog)
        self.hBLayout1.setObjectName("HBLayout1")

        # hBLayout1 --> hSpacer1 -- vBLayout1 -- hspacer2
        self.hSpacer1 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer1)

        self.vBLayout1 = QtWidgets.QVBoxLayout()
        self.vBLayout1.setObjectName("vBLayout1")
        self.hBLayout1.addLayout(self.vBLayout1)

        self.hSpacer2 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer2)

        # vBLayout1 --> vSpacer1 -- hBLayout2 -- tablewidget -- vSpacer2
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer1)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBlayout2")
        self.vBLayout1.addLayout(self.hBLayout2)

        self.vSpacer2 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer2)

        self.tWArchive = QtWidgets.QTableWidget()
        self.tWArchive.setObjectName("tWArchive")
        self.tWArchive.setLineWidth(2)
        self.tWArchive.setTextElideMode(QtCore.Qt.ElideRight)
        self.tWArchive.setShowGrid(False)
        self.tWArchive.setGridStyle(QtCore.Qt.SolidLine)
        self.tWArchive.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tWArchive.setAlternatingRowColors(True)
        self.tWArchive.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tWArchive.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tWArchive.verticalHeader().setStretchLastSection(False)
        self.tWArchive.horizontalHeader().setStretchLastSection(True)
        self.tWArchive.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tWArchive.setColumnCount(0)
        self.tWArchive.setRowCount(0)
        self.vBLayout1.addWidget(self.tWArchive)

        self.vSpacer3 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer3)

        # hBlayout2 --> Label -- Combobox -- pBRestore -- pBDelete -- pbDisplayReceipt -- hVSpacer1
        self.lArchived = QtWidgets.QLabel()
        self.lArchived.setObjectName("InputLabel")
        self.lArchived.setText("Archived Account: ")
        self.lArchived.setFont(general_font)
        self.lArchived.setAlignment(QtCore.Qt.AlignHCenter)
        self.lArchived.setSizePolicy(label_sizePolicy)
        self.hBLayout2.addWidget(self.lArchived)

        self.comboBAccounts = QtWidgets.QComboBox()
        self.comboBAccounts.setObjectName("comboBAccounts")
        self.comboBAccounts.setFont(general_font)
        self.comboBAccounts.setSizePolicy(sizePolicy)
        self.comboBAccounts.setMaximumWidth(adjusted_width/4)
        self.hBLayout2.addWidget(self.comboBAccounts)

        self.pBRestore = QtWidgets.QPushButton()
        self.pBRestore.setObjectName("pB")
        self.pBRestore.setText("Restore")
        self.pBRestore.setFont(pushButton_font)
        self.pBRestore.setSizePolicy(pushButton_sizePolicy)
        self.pBRestore.setFixedWidth(150)
        self.hBLayout2.addWidget(self.pBRestore)

        self.pBDisplayReceipt = QtWidgets.QPushButton()
        self.pBDisplayReceipt.setObjectName("pB")
        self.pBDisplayReceipt.setText("Display Receipt")
        self.pBDisplayReceipt.setFont(pushButton_font)
        self.pBDisplayReceipt.setSizePolicy(pushButton_sizePolicy)
        self.pBDisplayReceipt.setFixedWidth(150)
        self.hBLayout2.addWidget(self.pBDisplayReceipt)

        self.pBDelete = QtWidgets.QPushButton()
        self.pBDelete.setObjectName("pB")
        self.pBDelete.setText("Delete")
        self.pBDelete.setFont(pushButton_font)
        self.pBDelete.setSizePolicy(pushButton_sizePolicy)
        self.pBDelete.setFixedWidth(150)
        self.hBLayout2.addWidget(self.pBDelete)

        self.hVSpacer1 = QtWidgets.QSpacerItem(adjusted_width/6, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout2.addItem(self.hVSpacer1)

        self.lStatementPeriod = QtWidgets.QLabel()
        self.lStatementPeriod.setObjectName("lStatementPeriod")
        self.lStatementPeriod.setText("Statement Period: ")
        self.lStatementPeriod.setFont(general_font)
        self.lStatementPeriod.setAlignment(QtCore.Qt.AlignHCenter)
        self.lStatementPeriod.setSizePolicy(label_sizePolicy)
        self.hBLayout2.addWidget(self.lStatementPeriod)

        self.comboBStatements = QtWidgets.QComboBox()
        self.comboBStatements.setObjectName("comboBStatements")
        self.comboBStatements.setFont(general_font)
        self.comboBStatements.setSizePolicy(sizePolicy)
        self.comboBStatements.setMaximumWidth(adjusted_width/4)
        self.hBLayout2.addWidget(self.comboBStatements)




if __name__ == "__main__":
    print("error")