#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

# This Dialog is a Subwindow for the Mainwindow MdiArea
# Ledger 1 is used for Non Equity Accounts. As there are no shares to track.

import pickle

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Ledger1(object):
    def __init__(self, ParentType):
        super().__init__()
        self.refLedgerParentType = ParentType

    def setupUi(self, Dialog):
        # Dialog settings
        Dialog.setObjectName("Ledger1")
        Dialog.setWindowTitle("Ledger1")  # Will be dynamically changed in the backend
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))  # Consider hiring an artist to make different icons for different account types

        # Dialog size
        screen_dimensions_file = open("Resources/dimensions.pkl", "rb")
        screen_dimensions = pickle.load(screen_dimensions_file)
        screen_dimensions_file.close()

        work_area = screen_dimensions[1]

        size_factor_a = 0.45
        size_factor_b = 0.50

        if 3840 <= work_area[2]:
            size_factor_NA = size_factor_a

        if 2560 <= work_area[2] < 3840:
            size_factor_NA = (3840 * size_factor_a) / 2560

        if 1920 <= work_area[2] < 2560:
            size_factor_NA = (3840 * size_factor_a) / 1920

        if 1600 <= work_area[2] < 1920:
            size_factor_NA = (3840 * size_factor_a) / 1600

        if work_area[2] < 1600:
            size_factor_NA = (3840 * size_factor_a) / 1366

        size_factor_NB = (size_factor_b * size_factor_NA) / size_factor_a

        adjusted_width = work_area[2] * size_factor_NA  # for non full screen sizing
        adjusted_height = work_area[3] * size_factor_NB
        Dialog.resize(adjusted_width, adjusted_height)

        # Font and Size Policy
        header_font = QtGui.QFont()
        header_font.setPixelSize(18)
        header_font.setBold(True)

        graph_header_font = QtGui.QFont()
        graph_header_font.setPixelSize(14)
        graph_header_font.setBold(True)

        general_font = QtGui.QFont()
        general_font.setPixelSize(12)
        general_font.setBold(False)

        pushButton_font = QtGui.QFont()
        pushButton_font.setPixelSize(12)
        pushButton_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        altSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Core gridLayout
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        # Row 1 --  hVSpacer (C1) -- hSpacer (C2) -- hSpacer3 (C3)
        self.hVSpacer1 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hVSpacer1, 1, 1, 1, 1)

        width_wo_border = adjusted_width - 50
        ledger_width = width_wo_border * 0.80
        category_width = width_wo_border * 0.20

        self.hSpacer1 = QtWidgets.QSpacerItem(ledger_width, 0, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hSpacer1, 1, 2, 1, 1)

        self.hSpacer2 = QtWidgets.QSpacerItem(category_width, 0, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hSpacer2, 1, 3, 1, 1)

        # Row 2 -- QFrame1 (C2) -- QFrame 2 (C3)
        self.ledgerFrame = QtWidgets.QFrame()
        self.ledgerFrame.setObjectName("ledgerFrame")
        scrollFrame_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.ledgerFrame.setSizePolicy(scrollFrame_sizePolicy)
        self.gridLayout.addWidget(self.ledgerFrame, 2, 2, 1, 1)

        self.outerScrollLayout = QtWidgets.QVBoxLayout(self.ledgerFrame)
        self.outerScrollLayout.setObjectName("outerScrollLayout")

        self.ledgerScroll = QtWidgets.QScrollArea()
        self.ledgerScroll.horizontalScrollBar().setEnabled(True)
        self.ledgerScroll.verticalScrollBar().setEnabled(True)
        self.ledgerScroll.setGeometry(0, 0, self.ledgerFrame.width(), self.ledgerFrame.height())
        self.ledgerScroll.setWidgetResizable(True)
        self.ledgerScroll.setFrameStyle(0)
        self.outerScrollLayout.addWidget(self.ledgerScroll)

        widget = QtWidgets.QWidget()
        widget.setObjectName("scrollWidget")
        self.ledgerScroll.setWidget(widget)

        self.vBLayout1 = QtWidgets.QVBoxLayout(widget)
        self.vBLayout1.setObjectName("vBLayout1")

        self.categoryFrame = QtWidgets.QFrame()
        self.categoryFrame.setObjectName("categoryFrame")
        # self.categoryFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.categoryFrame.setLineWidth(1)
        self.categoryFrame.setFixedWidth(category_width)
        self.gridLayout.addWidget(self.categoryFrame, 2, 3, 1, 1)

        self.vBLayout2 = QtWidgets.QVBoxLayout(self.categoryFrame)
        self.vBLayout2.setObjectName("vBLayout2")

        # LedgerFrame -- vBLayout1 -- hbLayout1
        self.hBLayout1 = QtWidgets.QHBoxLayout()
        self.hBLayout1.setObjectName("hBlayout1")
        self.vBLayout1.addLayout(self.hBLayout1)

        self.staticAccount = QtWidgets.QLabel()
        self.staticAccount.setObjectName("staticAccount")
        self.staticAccount.setText("Active Account: ")
        self.staticAccount.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.staticAccount.setFont(header_font)
        self.staticAccount.setFixedWidth(200)
        self.staticAccount.setFixedHeight(40)
        self.staticAccount.setSizePolicy(sizePolicy)
        self.hBLayout1.addWidget(self.staticAccount)

        self.comboBLedger1 = QtWidgets.QComboBox()
        self.comboBLedger1.setObjectName("comboBLedger1")
        self.comboBLedger1.setFont(header_font)
        self.comboBLedger1.setFixedWidth(ledger_width / 3)
        self.comboBLedger1.setFixedHeight(40)
        self.comboBLedger1.setSizePolicy(sizePolicy)
        self.hBLayout1.addWidget(self.comboBLedger1)

        self.pBModAccount = QtWidgets.QPushButton()
        self.pBModAccount.setObjectName("pBModAccount")
        self.pBModAccount.setText("Modify")
        self.pBModAccount.setFont(pushButton_font)
        self.pBModAccount.setFixedWidth(150)
        self.pBModAccount.setFixedHeight(40)
        self.pBModAccount.setSizePolicy(sizePolicy)
        self.hBLayout1.addWidget(self.pBModAccount)

        self.hSpacer3 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout1.addSpacerItem(self.hSpacer3)

        # LedgerFrame --  vBLayout1 -- hbLayout2
        self.vSpacer2 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addSpacerItem(self.vSpacer2)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBlayout2")
        self.vBLayout1.addLayout(self.hBLayout2)

        self.vSpacer3 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addSpacerItem(self.vSpacer3)

        # LedgerFrame --> vBLayout1 --> hBLayout2 --> hSpacer -- LFrame -- CFrame -- RFrame -- hSpacer
        self.hSpacer4 = QtWidgets.QSpacerItem(25, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout2.addSpacerItem(self.hSpacer4)

        self.leftDisplayFrame = QtWidgets.QFrame()
        self.leftDisplayFrame.setObjectName("leftFrame")
        self.leftDisplayFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.leftDisplayFrame.setLineWidth(1)
        self.leftDisplayFrame.setFixedWidth((ledger_width - 40) / 3)
        self.leftDisplayFrame.setFixedHeight(60)
        self.hBLayout2.addWidget(self.leftDisplayFrame)

        self.centerDisplayFrame = QtWidgets.QFrame()
        self.centerDisplayFrame.setObjectName("centerFrame")
        self.centerDisplayFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.centerDisplayFrame.setLineWidth(1)
        self.centerDisplayFrame.setFixedWidth((ledger_width - 350) / 3)
        self.centerDisplayFrame.setFixedHeight(60)
        self.hBLayout2.addWidget(self.centerDisplayFrame)

        self.rightDisplayFrame = QtWidgets.QFrame()
        self.rightDisplayFrame.setObjectName("leftFrame")
        self.rightDisplayFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.rightDisplayFrame.setLineWidth(1)
        self.rightDisplayFrame.setFixedWidth((ledger_width - 40) / 3)
        self.rightDisplayFrame.setFixedHeight(60)
        self.hBLayout2.addWidget(self.rightDisplayFrame)

        self.hSpacer5 = QtWidgets.QSpacerItem(25, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout2.addSpacerItem(self.hSpacer5)

        # LedgerFrame --  vBLayout1 -- hbLayout2 -- leftDisplayFrame --> hblayout2A --> --> StaticLabel -- Label
        self.hBLayout2A = QtWidgets.QHBoxLayout(self.leftDisplayFrame)
        self.hBLayout2A.setObjectName("hBLayout2A")

        self.lStaticAccountBalance = QtWidgets.QLabel()
        self.lStaticAccountBalance.setObjectName("lStaticAccountBalance")
        self.lStaticAccountBalance.setText("Account Balance: ")
        self.lStaticAccountBalance.setFont(header_font)
        self.lStaticAccountBalance.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hBLayout2A.addWidget(self.lStaticAccountBalance)

        self.lAccountBalance = QtWidgets.QLabel()
        self.lAccountBalance.setObjectName("lAccountBalance")
        self.lAccountBalance.setText("$ 0.00")
        self.lAccountBalance.setFont(header_font)
        self.lAccountBalance.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hBLayout2A.addWidget(self.lAccountBalance)

        # LedgerFrame --  vBLayout1 -- hbLayout2 -- CenterDisplayFrame  --> hbLayout2B --> --> StaticLabel -- Label
        self.hBLayout2B = QtWidgets.QHBoxLayout(self.centerDisplayFrame)
        self.hBLayout2B.setObjectName("hBLayout2B")

        self.lStaticInterestRate = QtWidgets.QLabel()
        self.lStaticInterestRate.setObjectName("lStaticInterestRate")
        self.lStaticInterestRate.setText("Interest Rate: ")
        self.lStaticInterestRate.setFont(header_font)
        self.lStaticInterestRate.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hBLayout2B.addWidget(self.lStaticInterestRate)

        self.lInterestRate = QtWidgets.QLabel()
        self.lInterestRate.setObjectName("lInterestRate")
        self.lInterestRate.setText("1.00%")
        self.lInterestRate.setFont(header_font)
        self.lInterestRate.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hBLayout2B.addWidget(self.lInterestRate)

        # LedgerFrame --  vBLayout1 -- hbLayout2 -- RightDisplayFrame  --> hbLayout2C --> --> StaticLabel -- Label
        self.hBLayout2C = QtWidgets.QHBoxLayout(self.rightDisplayFrame)
        self.hBLayout2C.setObjectName("hBLayout2C")

        self.lStaticVariable1 = QtWidgets.QLabel()
        self.lStaticVariable1.setObjectName("lstaticVariable1")
        self.lStaticVariable1.setText("Starting Balance: ")
        self.lStaticVariable1.setFont(header_font)
        self.lStaticVariable1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hBLayout2C.addWidget(self.lStaticVariable1)

        self.lVariable1 = QtWidgets.QLabel()
        self.lVariable1.setObjectName("lVariable1")
        self.lVariable1.setText("  0.00")
        self.lVariable1.setFont(header_font)
        self.lVariable1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.hBLayout2C.addWidget(self.lVariable1)

        # LedgerFrame --  vBLayout1 -- hbLayout3 --> hSpacer -- lInputFrame -- rInputFrame -- hSpacer
        self.hBLayout3 = QtWidgets.QHBoxLayout()
        self.hBLayout3.setObjectName("hBlayout3")
        self.hBLayout3.setSpacing(0)
        self.vBLayout1.addLayout(self.hBLayout3)

        self.hSpacer6 = QtWidgets.QSpacerItem(25, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout3.addSpacerItem(self.hSpacer6)

        inputFrameWidth = (ledger_width - 250) / 2

        self.lInputFrame = QtWidgets.QFrame()
        self.lInputFrame.setObjectName("lInputFrame")
        self.lInputFrame.setFixedWidth(inputFrameWidth)
        # self.lInputFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.lInputFrame.setLineWidth(1)
        self.hBLayout3.addWidget(self.lInputFrame)

        self.rInputFrame = QtWidgets.QFrame()
        self.rInputFrame.setObjectName("rInputFrame")
        self.rInputFrame.setFixedWidth(inputFrameWidth)
        # self.rInputFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.rInputFrame.setLineWidth(1)
        self.hBLayout3.addWidget(self.rInputFrame)

        self.hSpacer7 = QtWidgets.QSpacerItem(25, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout3.addSpacerItem(self.hSpacer7)

        # LedgerFrame -- VBlayout1 -- hbLayout3 -- lInputFrame --> gridlayout2 --> --> Inputs A
        self.gridLayout2 = QtWidgets.QGridLayout(self.lInputFrame)
        self.gridLayout2.setObjectName("gridLayout2")

        # Inputs A - Row # 1 -- hspacer (C1) hSpacer9  (c2) -- hSpacer 10 (c4) -- hSpacer(C5)
        self.hSpacer13 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout2.addItem(self.hSpacer13, 1, 1, 1, 1)

        self.hSpacer9 = QtWidgets.QSpacerItem(inputFrameWidth - 600, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout2.addItem(self.hSpacer9, 1, 2, 1, 1)

        self.hSpacer10 = QtWidgets.QSpacerItem(100, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout2.addItem(self.hSpacer10, 1, 4, 1, 1)

        # Inputs A - Row # 2 -- Label (c2) -- ComboBox (C3-4)
        self.lTransDate = QtWidgets.QLabel()
        self.lTransDate.setObjectName("lTransDate")
        self.lTransDate.setText("Trans. Date: ")
        self.lTransDate.setFont(general_font)
        self.lTransDate.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lTransDate.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lTransDate, 2, 2, 1, 1)

        self.DateEditTransDate = QtWidgets.QDateEdit()
        self.DateEditTransDate.setObjectName("DateEditTransDate")
        self.DateEditTransDate.setFont(general_font)
        self.DateEditTransDate.setSizePolicy(altSizePolicy)
        self.DateEditTransDate.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.DateEditTransDate.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 1, 1), QtCore.QTime(0, 0, 0)))
        self.DateEditTransDate.setDisplayFormat("MM/dd/yyyy")
        self.DateEditTransDate.setFixedHeight(33)
        self.DateEditTransDate.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.DateEditTransDate.setCalendarPopup(True)
        self.gridLayout2.addWidget(self.DateEditTransDate, 2, 3, 1, 1)

        # Inputs A - Row # 3 -- Label (c1) -- LineEdit (C2-3)
        self.lTransMethod = QtWidgets.QLabel()
        self.lTransMethod.setObjectName("lTransMethod")
        self.lTransMethod.setText("Trans. Method: ")
        self.lTransMethod.setFont(general_font)
        self.lTransMethod.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lTransMethod.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lTransMethod, 3, 2, 1, 1)

        self.lEditTransMethod = QtWidgets.QLineEdit()
        self.lEditTransMethod.setObjectName("lEditTransMethod")
        self.lEditTransMethod.setPlaceholderText(" (Max 20 Characters)")
        self.lEditTransMethod.setMaxLength(20)
        self.lEditTransMethod.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lEditTransMethod.setFont(general_font)
        self.lEditTransMethod.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lEditTransMethod, 3, 3, 1, 2)

        # Inputs A - Row # 4 -- Label (c1) -- LineEdit (C2-3)
        self.lTransDesc = QtWidgets.QLabel()
        self.lTransDesc.setObjectName("lTransDesc")
        self.lTransDesc.setText("Trans. Description: ")
        self.lTransDesc.setFont(general_font)
        self.lTransDesc.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lTransDesc.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lTransDesc, 4, 2, 1, 1)

        self.lEditTransDesc = QtWidgets.QLineEdit()
        self.lEditTransDesc.setObjectName("lEditTransDesc")
        self.lEditTransDesc.setPlaceholderText(" (Max 40 Characters)")
        self.lEditTransDesc.setMaxLength(40)
        self.lEditTransDesc.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lEditTransDesc.setFont(general_font)
        self.lEditTransDesc.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lEditTransDesc, 4, 3, 1, 2)

        # Inputs A - Row # 5 -- Label (c1) -- Combobox  (C2) -- pB (C3)
        self.lCategory = QtWidgets.QLabel()
        self.lCategory.setObjectName("lCategory")
        self.lCategory.setText("Category: ")
        self.lCategory.setFont(general_font)
        self.lCategory.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lCategory.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lCategory, 5, 2, 1, 1)

        self.comboBCategory = QtWidgets.QComboBox()
        self.comboBCategory.setObjectName("comboBTCategory")
        self.comboBCategory.setFont(general_font)
        self.comboBCategory.setFixedHeight(33)
        self.comboBCategory.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.comboBCategory, 5, 3, 1, 1)

        self.pBCatModify = QtWidgets.QPushButton()
        self.pBCatModify.setObjectName("pBCatModify")
        self.pBCatModify.setText("Modify")
        self.pBCatModify.setFont(pushButton_font)
        self.pBCatModify.setFixedWidth(150)
        self.pBCatModify.setFixedHeight(33)
        self.pBCatModify.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.pBCatModify, 5, 4, 1, 1)

        # Inputs A - Row # 6 -- Label (c1) -- LineEdit (C2-3)
        self.lDebit = QtWidgets.QLabel()
        self.lDebit.setObjectName("lDebit")
        self.lDebit.setText("Debit (-): ")
        self.lDebit.setFont(general_font)
        self.lDebit.setAlignment(QtCore.Qt.AlignLeft)
        self.lDebit.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lDebit, 6, 2, 1, 1)

        self.lEditDebit = QtWidgets.QLineEdit()
        self.lEditDebit.setObjectName("lEditDebit")
        self.lEditDebit.setPlaceholderText("0.00 ")
        self.lEditDebit.setAlignment(QtCore.Qt.AlignRight)
        self.lEditDebit.setFont(general_font)
        self.lEditDebit.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lEditDebit, 6, 3, 1, 1)

        # Inputs A - Row # 7 -- Label (c1) -- LineEdit (C2-3)
        self.lCredit = QtWidgets.QLabel()
        self.lCredit.setObjectName("lCredit")
        self.lCredit.setText("Credit (+): ")
        self.lCredit.setFont(general_font)
        self.lCredit.setAlignment(QtCore.Qt.AlignLeft)
        self.lCredit.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lCredit, 7, 2, 1, 1)

        self.lEditCredit = QtWidgets.QLineEdit()
        self.lEditCredit.setObjectName("lEditCredit")
        self.lEditCredit.setPlaceholderText("0.00 ")
        self.lEditCredit.setAlignment(QtCore.Qt.AlignRight)
        self.lEditCredit.setFont(general_font)
        self.lEditCredit.setSizePolicy(altSizePolicy)
        self.gridLayout2.addWidget(self.lEditCredit, 7, 3, 1, 1)

        # Inputs A - Row # 8 -- hSpacer12
        self.hSpacer12 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout2.addItem(self.hSpacer10, 8, 5, 1, 1)

        # LedgerFrame -- VBlayout1 -- hbLayout3 -- rInputFrame --> gridlayout3 --> --> Inputs B
        self.gridLayout3 = QtWidgets.QGridLayout(self.rInputFrame)
        self.gridLayout3.setObjectName("gridLayout3")

        # Inputs B -- Row# 1 - hSpacer3(C1) -- hSpacer15 (C2)
        self.hVSpacer3 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout3.addItem(self.hVSpacer3, 1, 1, 1, 1)

        self.hSpacer14 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout3.addItem(self.hSpacer14, 1, 3, 1, 1)

        # Inputs B -- Row# 2 - label (C2) -- TextEdit (C4-7)
        self.lAddNotes = QtWidgets.QLabel()
        self.lAddNotes.setObjectName("lAddNotes")
        self.lAddNotes.setText("Additional Notes: ")
        self.lAddNotes.setFont(general_font)
        self.lAddNotes.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lAddNotes.setSizePolicy(altSizePolicy)
        self.lAddNotes.setFixedHeight(80)
        self.gridLayout3.addWidget(self.lAddNotes, 2, 2, 1, 1)

        self.textEditAddNotes = QtWidgets.QTextEdit()
        self.textEditAddNotes.setObjectName("textEditAddNotes")
        self.textEditAddNotes.setPlaceholderText(" (Max 150 Characters)")
        self.textEditAddNotes.setFont(general_font)
        self.textEditAddNotes.setMaximumHeight(80)
        self.textEditAddNotes.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.textEditAddNotes, 2, 4, 1, 4)

        # Inputs B -- Row# 3 - label (C2) -- QRadiobutton (C4) -- QRadioButton - (C5)
        self.lTransStatus = QtWidgets.QLabel()
        self.lTransStatus.setObjectName("lTransStatus")
        self.lTransStatus.setText("Transaction Status: ")
        self.lTransStatus.setFont(general_font)
        self.lTransStatus.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lTransStatus.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.lTransStatus, 3, 2, 1, 1)

        self.rBPending = QtWidgets.QRadioButton()
        self.rBPending.setObjectName("rBPending")
        self.rBPending.setText("Pending")
        self.rBPending.setFont(general_font)
        self.rBPending.setChecked(True)
        self.gridLayout3.addWidget(self.rBPending, 3, 4, 1, 1)

        self.rBPosted = QtWidgets.QRadioButton()
        self.rBPosted.setObjectName("rBPosted")
        self.rBPosted.setText("Posted")
        self.rBPosted.setFont(general_font)
        self.rBPosted.setChecked(False)
        self.gridLayout3.addWidget(self.rBPosted, 3, 5, 1, 1)

        # Inputs B -- Row# 4 - label (C2) -- LineEdit (C4-7)
        self.lReceipt = QtWidgets.QLabel()
        self.lReceipt.setObjectName("lReceipt")
        self.lReceipt.setText("Receipt: ")
        self.lReceipt.setFont(general_font)
        self.lReceipt.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lReceipt.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.lReceipt, 4, 2, 1, 1)

        self.lEditReceipt = QtWidgets.QLineEdit()
        self.lEditReceipt.setObjectName("lEditReceipt")
        self.lEditReceipt.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lEditReceipt.setFont(general_font)
        self.lEditReceipt.setSizePolicy(altSizePolicy)
        self.lEditReceipt.setEnabled(False)
        self.gridLayout3.addWidget(self.lEditReceipt, 4, 4, 1, 4)

        # Inputs B -- Row# 5 - blank (C2-3) pushButtons x4 (C3-7)
        self.pBUpload = QtWidgets.QPushButton()
        self.pBUpload.setObjectName("pBUpload")
        self.pBUpload.setText("Upload")
        self.pBUpload.setFont(pushButton_font)
        self.pBUpload.setFixedHeight(30)
        self.pBUpload.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.pBUpload, 5, 4, 1, 1)

        self.pBDisplay = QtWidgets.QPushButton()
        self.pBDisplay.setObjectName("pBDisplay")
        self.pBDisplay.setText("Display")
        self.pBDisplay.setFont(pushButton_font)
        self.pBDisplay.setFixedHeight(30)
        self.pBDisplay.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.pBDisplay, 5, 5, 1, 1)

        self.pBClear = QtWidgets.QPushButton()
        self.pBClear.setObjectName("pBClear")
        self.pBClear.setText("Clear")
        self.pBClear.setFont(pushButton_font)
        self.pBClear.setFixedHeight(30)
        self.pBClear.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.pBClear, 5, 6, 1, 1)

        self.pBDeleteReceipt = QtWidgets.QPushButton()
        self.pBDeleteReceipt.setObjectName("pBDeleteReceipt")
        self.pBDeleteReceipt.setText("Delete")
        self.pBDeleteReceipt.setFont(pushButton_font)
        self.pBDeleteReceipt.setFixedHeight(30)
        self.pBDeleteReceipt.setSizePolicy(altSizePolicy)
        self.gridLayout3.addWidget(self.pBDeleteReceipt, 5, 7, 1, 1)

        # Inputs B -- Row#6 - hSpacer(C1-C8)
        self.vSpacer6 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout3.addItem(self.vSpacer6, 6, 1, 1, 8)

        # Inputs B -- Row# 7 - hVSpacer (C8)
        self.hvSpacer4 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout3.addItem(self.hvSpacer4, 7, 8, 1, 1)

        # LedgerFrame --  vBLayout1 --> hbLayout4 --> --> hspacer -- 5x buttons
        self.vSpacer5 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addSpacerItem(self.vSpacer5)

        self.hBLayout4 = QtWidgets.QHBoxLayout()
        self.hBLayout4.setObjectName("hBlayout4")
        self.vBLayout1.addLayout(self.hBLayout4)

        self.comboBPeriod = QtWidgets.QComboBox()
        self.comboBPeriod.setObjectName("comboBLedger1")
        self.comboBPeriod.setFont(general_font)
        self.comboBPeriod.setFixedWidth(300)
        self.comboBPeriod.setFixedHeight(33)
        self.comboBPeriod.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.comboBPeriod)

        self.hSpacer8 = QtWidgets.QSpacerItem(25, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout4.addSpacerItem(self.hSpacer8)

        self.pBAddTransaction = QtWidgets.QPushButton()
        self.pBAddTransaction.setObjectName("pBAddTransaction")
        self.pBAddTransaction.setText("Add Transaction")
        self.pBAddTransaction.setFont(pushButton_font)
        self.pBAddTransaction.setFixedWidth(250)
        self.pBAddTransaction.setFixedHeight(40)
        self.pBAddTransaction.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.pBAddTransaction)

        self.pBSelect = QtWidgets.QPushButton()
        self.pBSelect.setObjectName("pBSelect")
        self.pBSelect.setText("Select")
        self.pBSelect.setFont(pushButton_font)
        self.pBSelect.setFixedWidth(125)
        self.pBSelect.setFixedHeight(40)
        self.pBSelect.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.pBSelect)

        self.pBUpdate = QtWidgets.QPushButton()
        self.pBUpdate.setObjectName("pBUpdate")
        self.pBUpdate.setText("Update")
        self.pBUpdate.setFont(pushButton_font)
        self.pBUpdate.setFixedWidth(125)
        self.pBUpdate.setFixedHeight(40)
        self.pBUpdate.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.pBUpdate)

        self.pBDelete = QtWidgets.QPushButton()
        self.pBDelete.setObjectName("pBDelete")
        self.pBDelete.setText("Delete")
        self.pBDelete.setFont(pushButton_font)
        self.pBDelete.setFixedWidth(125)
        self.pBDelete.setFixedHeight(40)
        self.pBDelete.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.pBDelete)

        self.pBClearInputs = QtWidgets.QPushButton()
        self.pBClearInputs.setObjectName("pBClearInputs")
        self.pBClearInputs.setText("Clear Inputs")
        self.pBClearInputs.setFont(pushButton_font)
        self.pBClearInputs.setFixedWidth(125)
        self.pBClearInputs.setFixedHeight(40)
        self.pBClearInputs.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.pBClearInputs)

        # LedgerFrame -->  vBLayout1 --> hbLayout5 --> --> vSpacer -- QTableWidget
        self.hBLayout5 = QtWidgets.QHBoxLayout()
        self.hBLayout5.setObjectName("hBlayout5")
        self.vBLayout1.addLayout(self.hBLayout5)

        self.vSpacer1 = QtWidgets.QSpacerItem(0, adjusted_height / 2, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout5.addSpacerItem(self.vSpacer1)

        self.tableWLedger1 = QtWidgets.QTableWidget()
        self.tableWLedger1.setObjectName("tableWLedger1")
        self.tableWLedger1.setLineWidth(2)
        self.tableWLedger1.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWLedger1.setShowGrid(False)
        self.tableWLedger1.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWLedger1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWLedger1.setAlternatingRowColors(True)
        self.tableWLedger1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWLedger1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWLedger1.verticalHeader().setStretchLastSection(False)
        self.tableWLedger1.horizontalHeader().setStretchLastSection(True)
        self.tableWLedger1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWLedger1.setColumnCount(0)
        self.tableWLedger1.setRowCount(0)
        self.hBLayout5.addWidget(self.tableWLedger1)

        # This Frame 'Functions' separately to the LedgerFrame. Intended to calculate Spending by Category
        # Calculate Spending by Category will function for all Ledger1 ParentTypes EXCEPT Property.
        # Property will provide the option to upload an image of the house. (Code below)
        # CategoryFrame --> vBLayout2 --> --> QTabWidget w/ 3 Tabs
        if self.refLedgerParentType != "Property":
            self.tabWidget = QtWidgets.QTabWidget()
            self.tabWidget.setObjectName("tabWidget")
            self.vBLayout2.addWidget(self.tabWidget)
            self.tab1 = QtWidgets.QWidget()
            self.tab1.setObjectName("StatementTab")
            self.tab2 = QtWidgets.QWidget()
            self.tab2.setObjectName("YearTab")
            self.tab3 = QtWidgets.QWidget()
            self.tab3.setObjectName("OverallTab")

            self.tabWidget.addTab(self.tab1, "Statement")
            self.tabWidget.addTab(self.tab2, "Year")
            self.tabWidget.addTab(self.tab3, "Overall")

            self.tab1.hBlayout1 = QtWidgets.QHBoxLayout()
            self.tab1.setLayout(self.tab1.hBlayout1)
            self.tab2.hBlayout2 = QtWidgets.QHBoxLayout()
            self.tab2.setLayout(self.tab2.hBlayout2)
            self.tab3.hBlayout3 = QtWidgets.QHBoxLayout()
            self.tab3.setLayout(self.tab3.hBlayout3)

            # self.tab1.hBlayout1 -- STATEMENT PERIOD
            self.hvSpacer5 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.tab1.hBlayout1.addItem(self.hvSpacer5)

            self.lTab1vBLayout = QtWidgets.QVBoxLayout()
            self.lTab1vBLayout.setObjectName("lTab1vBLayout")
            self.tab1.hBlayout1.addLayout(self.lTab1vBLayout)

            self.hvSpacer6 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.tab1.hBlayout1.addItem(self.hvSpacer6)

            # self.tab1.hBlayout1 --> self.lTab1vBlayout --> --> Label -- hSpacer -- frame -- hblayout - hblayout
            self.vSpacer7 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.lTab1vBLayout.addItem(self.vSpacer7)

            self.lStatementGraph = QtWidgets.QLabel()
            self.lStatementGraph.setObjectName("lStatementGraph")
            self.lStatementGraph.setText(f"Spending During TBD")
            self.lStatementGraph.setFont(graph_header_font)
            self.lStatementGraph.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.lStatementGraph.setSizePolicy(altSizePolicy)
            self.lTab1vBLayout.addWidget(self.lStatementGraph)

            self.statementFrame = QtWidgets.QFrame()
            self.statementFrame.setObjectName("statementFrame")
            self.statementFrame.setSizePolicy(altSizePolicy)
            self.statementFrame.setFixedHeight(300)
            # self.statementFrame.setFrameShape(QtWidgets.QFrame.Panel)
            # self.statementFrame.setLineWidth(1)
            self.lTab1vBLayout.addWidget(self.statementFrame)

            self.tab1HBLayout1 = QtWidgets.QHBoxLayout()
            self.tab1HBLayout1.setObjectName("tab1HBLayout1")
            self.lTab1vBLayout.addLayout(self.tab1HBLayout1)

            self.tab1HBLayout2 = QtWidgets.QHBoxLayout()
            self.tab1HBLayout2.setObjectName("tab1HBLayout2")
            self.lTab1vBLayout.addLayout(self.tab1HBLayout2)

            # self.tab1.hBlayout1 --> self.lTab1vBlayout --> tab1HBLayout1 -- hSpacer -- pbButton toggle
            self.hSpacer11 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.tab1HBLayout1.addItem(self.hSpacer11)

            self.pBToggle = QtWidgets.QPushButton()
            self.pBToggle.setObjectName("pBToggle")
            self.pBToggle.setText("Toggle Categories")
            self.pBToggle.setFixedWidth(200)
            self.pBToggle.setFont(pushButton_font)
            self.pBToggle.setSizePolicy(sizePolicy)
            self.tab1HBLayout1.addWidget(self.pBToggle)

            # self.tab1.hBlayout1 --> self.lTab1vBlayout --> tab1HBLayout2 -- vSpacer -- DataScrollArea
            self.vSpacer8 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            self.tab1HBLayout2.addItem(self.vSpacer8)

            self.statementDataScroll = QtWidgets.QScrollArea()
            self.statementDataScroll.setObjectName("statementDataScroll")
            self.statementDataScroll.horizontalScrollBar().setEnabled(False)
            self.statementDataScroll.setFrameStyle(0)
            self.tab1HBLayout2.addWidget(self.statementDataScroll)

            widget = QtWidgets.QWidget()
            self.statementDataScroll.setWidget(widget)
            self.statementDataScroll.setWidgetResizable(True)
            self.statementScrollLayout = QtWidgets.QVBoxLayout(widget)

            # self.tab2.hBlayout2 YEAR
            self.hvSpacer7 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.tab2.hBlayout2.addItem(self.hvSpacer7)

            self.lTab2vBLayout = QtWidgets.QVBoxLayout()
            self.lTab2vBLayout.setObjectName("lTab2vBLayout")
            self.tab2.hBlayout2.addLayout(self.lTab2vBLayout)

            self.hvSpacer8 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.tab2.hBlayout2.addItem(self.hvSpacer8)

            # self.tab2.hBlayout2 --> self.lTab2vBlayout --> --> Label -- hSpacer -- frame -- hblayout - hblayout
            self.vSpacer9 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.lTab2vBLayout.addItem(self.vSpacer9)

            self.tab2TitleHBLayout = QtWidgets.QHBoxLayout()
            self.tab2TitleHBLayout.setObjectName("tab2TitleHBLayout")
            self.lTab2vBLayout.addLayout(self.tab2TitleHBLayout)

            self.yearFrame = QtWidgets.QFrame()
            self.yearFrame.setObjectName("YearFrame")
            self.yearFrame.setSizePolicy(altSizePolicy)
            self.yearFrame.setFixedHeight(300)
            # self.yearFrame.setFrameShape(QtWidgets.QFrame.Panel)
            # self.yearFrame.setLineWidth(1)
            self.lTab2vBLayout.addWidget(self.yearFrame)

            self.tab2HBLayout1 = QtWidgets.QHBoxLayout()
            self.tab2HBLayout1.setObjectName("tab2HBLayout1")
            self.lTab2vBLayout.addLayout(self.tab2HBLayout1)

            self.tab2HBLayout2 = QtWidgets.QHBoxLayout()
            self.tab2HBLayout2.setObjectName("tab2HBLayout2")
            self.lTab2vBLayout.addLayout(self.tab2HBLayout2)

            # self.tab2.vBLayout2 --> self.tab2TitleHBLayout --> --> Label -- combobox
            self.lYearGraph = QtWidgets.QLabel()
            self.lYearGraph.setObjectName("lYearGraph")
            self.lYearGraph.setText(f"Spending During: ")
            self.lYearGraph.setFont(graph_header_font)
            self.lYearGraph.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.lYearGraph.setSizePolicy(altSizePolicy)
            self.tab2TitleHBLayout.addWidget(self.lYearGraph)

            self.comboBTab2Year = QtWidgets.QComboBox()
            self.comboBTab2Year.setObjectName("comboBTab2Year")
            self.comboBTab2Year.setFixedWidth(100)
            self.comboBTab2Year.setFont(graph_header_font)
            self.comboBTab2Year.setSizePolicy(sizePolicy)
            self.tab2TitleHBLayout.addWidget(self.comboBTab2Year)

            # self.tab2.vBlayout2 --> self.lTab2vBlayout --> tab2HBLayout1 -- hSpacer -- pbButton toggle
            self.hSpacer15 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.tab2HBLayout1.addItem(self.hSpacer15)

            # self.tab2.hBlayout2 --> self.lTab2vBlayout --> tab2HBLayout2 -- vSpacer -- DataScrollArea
            self.vSpacer10 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            self.tab2HBLayout2.addItem(self.vSpacer10)

            self.yearDataScroll = QtWidgets.QScrollArea()
            self.yearDataScroll.setObjectName("yearDataScroll")
            self.yearDataScroll.horizontalScrollBar().setEnabled(False)
            self.yearDataScroll.setFrameStyle(0)
            self.tab2HBLayout2.addWidget(self.yearDataScroll)

            widget = QtWidgets.QWidget()
            self.yearDataScroll.setWidget(widget)
            self.yearDataScroll.setWidgetResizable(True)
            self.yearScrollLayout = QtWidgets.QVBoxLayout(widget)

            # self.tab3.hBlayout3 OVERALL
            self.hvSpacer9 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.tab3.hBlayout3.addItem(self.hvSpacer9)

            self.lTab3vBLayout = QtWidgets.QVBoxLayout()
            self.lTab3vBLayout.setObjectName("lTab3vBLayout")
            self.tab3.hBlayout3.addLayout(self.lTab3vBLayout)

            self.hvSpacer10 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.tab3.hBlayout3.addItem(self.hvSpacer10)

            # self.tab3.hBlayout3 --> self.lTab3vBlayout --> --> Label -- hSpacer -- frame -- hblayout - hblayout
            self.vSpacer11 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.lTab3vBLayout.addItem(self.vSpacer11)

            self.lOverAllGraph = QtWidgets.QLabel()
            self.lOverAllGraph.setObjectName("lOverAllGraph")
            self.lOverAllGraph.setText(f"Spending Over Account Lifetime")
            self.lOverAllGraph.setFont(graph_header_font)
            self.lOverAllGraph.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.lOverAllGraph.setSizePolicy(altSizePolicy)
            self.lTab3vBLayout.addWidget(self.lOverAllGraph)

            self.overAllFrame = QtWidgets.QFrame()
            self.overAllFrame.setObjectName("overAllFrame")
            self.overAllFrame.setSizePolicy(altSizePolicy)
            self.overAllFrame.setFixedHeight(300)
            # self.overAllFrame.setFrameShape(QtWidgets.QFrame.Panel)
            # self.overAllFrame.setLineWidth(1)
            self.lTab3vBLayout.addWidget(self.overAllFrame)

            self.tab3HBLayout1 = QtWidgets.QHBoxLayout()
            self.tab3HBLayout1.setObjectName("tab3HBLayout1")
            self.lTab3vBLayout.addLayout(self.tab3HBLayout1)

            self.tab3HBLayout2 = QtWidgets.QHBoxLayout()
            self.tab3HBLayout2.setObjectName("tab3HBLayout2")
            self.lTab3vBLayout.addLayout(self.tab3HBLayout2)

            # self.tab3.hBlayout3 --> self.lTab3vBlayout --> tab3HBLayout1 -- hSpacer -- pbButton toggle
            self.hSpacer16 = QtWidgets.QSpacerItem(10, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.tab3HBLayout1.addItem(self.hSpacer16)

            # self.tab3.hBlayout3 --> self.lTab3vBlayout --> tab3HBLayout2 -- vSpacer -- DataScrollArea
            self.vSpacer12 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            self.tab3HBLayout2.addItem(self.vSpacer12)

            self.overallDataScroll = QtWidgets.QScrollArea()
            self.overallDataScroll.setObjectName("OverallDataScroll")
            self.overallDataScroll.horizontalScrollBar().setEnabled(False)
            self.overallDataScroll.setFrameStyle(0)
            self.tab3HBLayout2.addWidget(self.overallDataScroll)

            widget = QtWidgets.QWidget()
            self.overallDataScroll.setWidget(widget)
            self.overallDataScroll.setWidgetResizable(True)
            self.overallScrollLayout = QtWidgets.QVBoxLayout(widget)

        else:  # Property
            # CategoryFrame --> vBLayout2 --> --> QFrame -- HBLayout
            self.houseFrame = QtWidgets.QFrame()
            self.houseFrame.setObjectName("houseFrame")
            self.houseFrame.setSizePolicy(altSizePolicy)
            self.houseFrame.setFixedHeight(600)
            # self.houseFrame.setFrameShape(QtWidgets.QFrame.Panel)
            # self.houseFrame.setLineWidth(1)
            self.vBLayout2.addWidget(self.houseFrame)

            self.hBLayout6 = QtWidgets.QHBoxLayout()
            self.hBLayout6.setObjectName("hBLayout6")
            self.vBLayout2.addLayout(self.hBLayout6)

            # CategoryFrame --> vBLayout2 --> QFrame  --> --> vBLayout
            self.vBLayout3 = QtWidgets.QVBoxLayout(self.houseFrame)
            self.vBLayout3.setObjectName("vBLayout3")

            # CategoryFrame --> vBLayout2 --> QFrame  --> vBLayout --> --> Spacer -- QLabel
            self.houseSpacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.vBLayout3.addItem(self.houseSpacer)

            self.lHouseImage = QtWidgets.QLabel()
            self.lHouseImage.setObjectName("lHouseImage")
            self.lHouseImage.setFixedHeight(600)
            self.lHouseImage.setSizePolicy(altSizePolicy)
            self.lHouseImage.setText(f"Upload a House Image\n\n Max Dimensions:\n{self.houseFrame.geometry().width()} pixel x {self.houseFrame.geometry().height()} pixel")
            self.lHouseImage.setFont(general_font)
            self.lHouseImage.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.vBLayout3.addWidget(self.lHouseImage)

            # CategoryFrame --> vBLayout2 --> --> HBLayout
            self.hBLayout7 = QtWidgets.QHBoxLayout()
            self.hBLayout7.setObjectName("hBLayout7")
            self.vBLayout2.addLayout(self.hBLayout7)

            # CategoryFrame --> vBLayout2 --> HBLayout --> pBUpload -- pBDelete
            self.pBUploadHouse = QtWidgets.QPushButton()
            self.pBUploadHouse.setObjectName("pBUploadHouse")
            self.pBUploadHouse.setText("Upload")
            self.pBUploadHouse.setFixedWidth(150)
            self.pBUploadHouse.setFixedHeight(40)
            self.hBLayout7.addWidget(self.pBUploadHouse)

            self.pBDeleteHouse = QtWidgets.QPushButton()
            self.pBDeleteHouse.setObjectName("pBDeleteHouse")
            self.pBDeleteHouse.setText("Delete")
            self.pBDeleteHouse.setFixedWidth(150)
            self.pBDeleteHouse.setFixedHeight(40)
            self.pBDeleteHouse.setEnabled(False)
            self.hBLayout7.addWidget(self.pBDeleteHouse)

        # Row Last -- hVSpacer (C4)
        self.hVSpacer2 = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.hVSpacer2, 3, 4, 1, 1)


if __name__ == "__main__":
    print("error")