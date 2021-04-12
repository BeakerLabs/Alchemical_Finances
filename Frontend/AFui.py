# This Front End Code is used to Generate the GUI for the MainWindow of the Alchemical Finances Program
# Many of the UI will be placed into the MdiArea as sub windows. Some will be dialog boxes


from PySide6 import QtCore, QtGui, QtWidgets
from win32api import GetMonitorInfo, MonitorFromPoint


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        adjusted_width = work_area[2] * 0.5
        adjusted_height = work_area[3] * 0.5
        MainWindow.resize(adjusted_width, adjusted_height)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(int(adjusted_width * 0.8), int(adjusted_height * 0.80)))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))

        MainWindow.setWindowIcon(QtGui.QIcon('AF Logo.png'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("Centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.divider = QtWidgets.QFrame(self.centralwidget)
        self.divider.setObjectName("divider")
        self.dividerB = QtWidgets.QFrame(self.centralwidget)
        self.dividerB.setObjectName("dividerB")
        self.dividerC = QtWidgets.QFrame(self.centralwidget)
        self.dividerC.setObjectName("dividerC")
        self.dividerD = QtWidgets.QFrame(self.centralwidget)
        self.dividerD.setObjectName("dividerD")

        dividers = [self.divider,
                    self.dividerB,
                    self.dividerC,
                    self.dividerD]

        for line in dividers:
            line.setGeometry(QtCore.QRect(0, 0, 6, 200))
            line.setFrameShadow(QtWidgets.QFrame.Plain)
            line.setLineWidth(4)
            line.setFrameShape(QtWidgets.QFrame.VLine)

        self.labelStaticTA = QtWidgets.QLabel(self.centralwidget)
        self.labelStaticTA.setObjectName("labelStaticTA")
        self.labelStaticTA.setText("     Total Assets: ")
        self.labelTAssests = QtWidgets.QLabel(self.centralwidget)
        self.labelTAssests.setObjectName("labelTAssests")

        self.labelStaticTL = QtWidgets.QLabel(self.centralwidget)
        self.labelStaticTL.setObjectName("labelStaticTL")
        self.labelStaticTL.setText("Total Liabilities: ")
        self.labelTLiabilities = QtWidgets.QLabel(self.centralwidget)
        self.labelTLiabilities.setObjectName("labelTLiabilities")

        self.labelStaticTN = QtWidgets.QLabel(self.centralwidget)
        self.labelStaticTN.setObjectName("labelStaticTN")
        self.labelStaticTN.setText("        Net Worth: ")
        self.labelNW = QtWidgets.QLabel(self.centralwidget)
        self.labelNW.setObjectName("labelNW")

        label_construction = [(self.labelStaticTA, "standard", "R"),
                              (self.labelTAssests, "standard", "L"),
                              (self.labelStaticTL, "standard", "R"),
                              (self.labelTLiabilities, "standard", "L"),
                              (self.labelStaticTN, "highlight", "R"),
                              (self.labelNW, "highlight", "L")]

        # Debugging placeholders. Used for spacing checks
        self.labelNW.setText("$10,000,000.00")
        self.labelTLiabilities.setText("$10,000,000.00")
        self.labelTAssests.setText("$10,000,000.00")

        for label in label_construction:
            font = QtGui.QFont()
            if label[1] == "standard":
                font.setPointSize(18)
                font.setBold(False)
            else:
                font.setPointSize(20)
                font.setBold(True)

            initial_x = 0
            constant_y = 0
            label_length = 186
            label_height = 200

            label[0].setGeometry(QtCore.QRect(initial_x, constant_y, label_length, label_height))
            label[0].setFont(font)
            if label[2] == "R":
                label[0].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
            else:
                label[0].setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.horizontalLayout.addWidget(self.divider)
        self.horizontalLayout.addWidget(self.labelStaticTA)
        self.horizontalLayout.addWidget(self.labelTAssests)
        self.horizontalLayout.addWidget(self.dividerB)
        self.horizontalLayout.addWidget(self.labelStaticTL)
        self.horizontalLayout.addWidget(self.labelTLiabilities)
        self.horizontalLayout.addWidget(self.dividerC)
        self.horizontalLayout.addWidget(self.labelStaticTN)
        self.horizontalLayout.addWidget(self.labelNW)
        self.horizontalLayout.addWidget(self.dividerD)

        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy)
        self.mdiArea.setEnabled(True)

        self.mdiArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mdiArea.setActivationOrder(QtWidgets.QMdiArea.StackingOrder)
        self.mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.verticalLayout.addWidget(self.mdiArea)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 18))
        self.menubar.setObjectName("menubar")
        font = self.menubar.font()
        font.setPointSize(14)
        self.menubar.setFont(font)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAssets = QtWidgets.QMenu(self.menubar)
        self.menuAssets.setObjectName("menuAssets")
        self.menuLiabilities = QtWidgets.QMenu(self.menubar)
        self.menuLiabilities.setObjectName("menuLiabilities")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)

        self.actionSummary = QtWidgets.QWidgetAction(MainWindow)
        self.actionSummary.setObjectName("actionSummary")
        self.actionGenerate = QtWidgets.QWidgetAction(MainWindow)
        self.actionGenerate.setObjectName("actionGenerate")
        self.actionNWG = QtWidgets.QWidgetAction(MainWindow)
        self.actionNWG.setObjectName("actionNWG")
        self.actionExport = QtWidgets.QWidgetAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionSave = QtWidgets.QWidgetAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClose = QtWidgets.QWidgetAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        self.actionBank = QtWidgets.QWidgetAction(MainWindow)
        self.actionBank.setObjectName("actionBank")
        self.actionCash = QtWidgets.QWidgetAction(MainWindow)
        self.actionCash.setObjectName("actionCash")
        self.actionCertificate_of_Deposit = QtWidgets.QWidgetAction(MainWindow)
        self.actionCertificate_of_Deposit.setObjectName("actionCertificate_of_Deposit")
        self.actionEquity = QtWidgets.QWidgetAction(MainWindow)
        self.actionEquity.setObjectName("actionEquity")
        self.actionProperty = QtWidgets.QWidgetAction(MainWindow)
        self.actionProperty.setObjectName("actionProperty")
        self.actionTreasury_Bonds = QtWidgets.QWidgetAction(MainWindow)
        self.actionTreasury_Bonds.setObjectName("actionTreasury_Bonds")
        self.actionRetirement = QtWidgets.QWidgetAction(MainWindow)
        self.actionRetirement.setObjectName("actionRetirement")


        self.actionDebt = QtWidgets.QWidgetAction(MainWindow)
        self.actionDebt.setObjectName("actionDebt")
        self.actionCredit_Cards = QtWidgets.QWidgetAction(MainWindow)
        self.actionCredit_Cards.setObjectName("actionCredit_Cards")

        self.actionUserManual = QtWidgets.QWidgetAction(MainWindow)
        self.actionUserManual.setObjectName("actionUserManual")
        self.actionAbout = QtWidgets.QWidgetAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.actionArchive = QtWidgets.QWidgetAction(MainWindow)
        self.actionArchive.setObjectName("actionArchive")
        self.actionReports_Future = QtWidgets.QWidgetAction(MainWindow)
        self.actionReports_Future.setObjectName("actionReports_Future")
        self.actionBudgeting_Future = QtWidgets.QWidgetAction(MainWindow)
        self.actionBudgeting_Future.setObjectName("actionBudgeting_Future")

        submenu_lst = [self.actionSummary, self.actionGenerate, self.actionNWG, self.actionExport, self.actionSave,
                       self.actionClose, self.actionBank, self.actionCash, self.actionCertificate_of_Deposit,
                       self.actionEquity, self.actionProperty, self.actionRetirement, self.actionTreasury_Bonds,
                       self.actionDebt, self.actionCredit_Cards, self.actionCredit_Cards, self.actionUserManual,
                       self.actionAbout, self.actionArchive, self.actionReports_Future, self.actionBudgeting_Future]

        for submenu in submenu_lst:
            font = submenu.font()
            font.setPointSize(12)
            submenu.setFont(font)

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuFile.addAction(self.actionSummary)
        self.menuFile.addAction(self.actionGenerate)
        self.menuFile.addAction(self.actionNWG)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClose)

        self.menuAssets.addAction(self.actionBank)
        self.menuAssets.addAction(self.actionCash)
        self.menuAssets.addAction(self.actionCertificate_of_Deposit)
        self.menuAssets.addAction(self.actionEquity)
        self.menuAssets.addAction(self.actionProperty)
        self.menuAssets.addAction(self.actionTreasury_Bonds)
        self.menuAssets.addAction(self.actionRetirement)

        self.menuLiabilities.addAction(self.actionDebt)
        self.menuLiabilities.addAction(self.actionCredit_Cards)

        self.menuTools.addAction(self.actionArchive)
        self.menuTools.addAction(self.actionBudgeting_Future)
        self.menuAbout.addAction(self.actionUserManual)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAssets.menuAction())
        self.menubar.addAction(self.menuLiabilities.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', "Alchemical Finances - Reformulated", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuAssets.setTitle(_translate("MainWindow", "Assets", None))
        self.menuLiabilities.setTitle(_translate("MainWindow", "Liabilities", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.menuAbout.setTitle(_translate("MainWindow", "Other", None))
        self.actionSummary.setText(_translate("MainWindow", "Summary", None))
        self.actionExport.setText(_translate("MainWindow", "Export [Future]", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionBank.setText(_translate("MainWindow", "Bank", None))
        self.actionEquity.setText(_translate("MainWindow", "Equity", None))
        self.actionEquity.setToolTip(_translate("MainWindow", "Equity", None))
        self.actionProperty.setText(_translate("MainWindow", "Property", None))
        self.actionProperty.setToolTip(_translate("MainWindow", "Property", None))
        self.actionCertificate_of_Deposit.setText(_translate("MainWindow", "Certificate of Deposit", None))
        self.actionRetirement.setText(_translate("MainWindow", "Retirement", None))
        self.actionRetirement.setToolTip(_translate("MainWindow", "Retirement", None))
        self.actionTreasury_Bonds.setText(_translate("MainWindow", "Treasury Bonds", None))
        self.actionDebt.setText(_translate("MainWindow", "Debt", None))
        self.actionCredit_Cards.setText(_translate("MainWindow", "Credit Cards", None))
        self.actionCash.setText(_translate("MainWindow", "Cash", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionUserManual.setText(_translate("MainWindow", "User Manual", None))
        self.actionUserManual.setToolTip(_translate("MainWindow", "User Manual", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionAbout.setToolTip(_translate("MainWindow", "Other", None))
        self.actionArchive.setText(_translate("MainWindow", "Archive", None))
        self.actionBudgeting_Future.setText(_translate("MainWindow", "Budgeting [Future]", None))
        self.actionGenerate.setText(_translate("MainWindow", "Generate Report", None))
        self.actionNWG.setText(_translate("MainWindow", "Net Worth Graph", None))
