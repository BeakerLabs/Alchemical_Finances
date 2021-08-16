"""
This script is the backend to Frontend.SummaryUi.py

Future Concepts
1)

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QDialog, QFrame, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QProgressBar
from PySide2.QtCore import Slot

from Frontend.SummaryUi import Ui_Summary

from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value
from Toolbox.Formatting_Tools import add_comma, cash_format, decimal_places, remove_space
from Toolbox.AF_Tools import set_font

from Backend.BuildGraphs import snapshot_chart, AF_Canvas
from StyleSheets.SummaryCSS import summarySTD, parentFormat, columnHeader, accountDetails, messageFormat, subtotalBalanceFormat


class Ledger_Summary(QDialog):
    remove_tab_LS = QtCore.Signal(str)

    def __init__(self, parent, database, ledgerContainer, error_Log):
        super().__init__(parent)
        self.ui = Ui_Summary()
        self.ui.setupUi(self)

        self.refUserDB = database
        self.ledgerContainer = ledgerContainer

        self.summaryTuple = None
        self.summaryFrame_width = self.ui.frameSummary.geometry().width()
        self.progress_width = self.summaryFrame_width * (2/3)
        self.labelHeight = 45
        self.row = 0
        # label dictionary[AccountName] = label for Account Balances
        self.balancelabeldic = {}
        # label dictionary[ParentType] = label for SubType Balances
        self.subtotaldic = {}
        # label dictionary[AccountName] = label for ProgressBar
        self.progBardic = {}
        # vBoxLayout dicionary[ParentType] = layout for Accounts
        self.accountLayoutdic = {}
        self.updateMessages = []

        # Program Error Log
        self.error_Logger = error_Log

        # Asset Nested Pie Graph
        self.assetCanvas = AF_Canvas(self, width=5, height=4, dpi=200)
        self.aCanvasLayout = QVBoxLayout(self.ui.frameAGraph)
        self.aCanvasLayout.addWidget(self.assetCanvas)
        self.update_plot(focus="Asset", canvas=self.assetCanvas)

        # Liability Nested Pie Graph
        self.liabilityCanvas = AF_Canvas(self, width=5, height=4, dpi=200)
        self.lCanvasLayout = QVBoxLayout(self.ui.frameLGraph)
        self.lCanvasLayout.addWidget(self.liabilityCanvas)
        self.update_plot(focus="Liability", canvas=self.liabilityCanvas)

        # Build Summary Display
        summaryStatement = """SELECT ItemType, ParentType, SubType, ID, Balance FROM Account_Summary """ \
                           + """ORDER BY "ItemType", "ParentType", "SubType", "Balance" DESC LIMIT 0, 49999"""
        self.summaryTuple = obtain_sql_list(summaryStatement, self.refUserDB, self.error_Logger)
        self.generate_summary()
        self.setStyleSheet(summarySTD)
        self.ui.lAsset.setStyleSheet(parentFormat)
        self.ui.lLiability.setStyleSheet(parentFormat)
        self.ui.frameAGraph.setStyleSheet(summarySTD)
        self.ui.frameLGraph.setStyleSheet(summarySTD)
        parent.refresh_signal_summary.connect(self.refresh_summary)

    def set_formatting(self, target, font, Alignment, stylesheet):
        target.setFont(font)
        target.setFrameShape(QFrame.Panel)
        target.setFrameShadow(QFrame.Sunken)
        target.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | Alignment)
        target.setStyleSheet(stylesheet)

    def generate_summary(self):
        subTotal = 0

        listofBank = [account for account in self.summaryTuple if "Bank" in account]
        listofCD = [account for account in self.summaryTuple if "CD" in account]
        listofCash = [account for account in self.summaryTuple if "Cash" in account]
        listofEquity = [account for account in self.summaryTuple if "Equity" in account]
        listofRetirement = [account for account in self.summaryTuple if "Retirement" in account]
        listofCredit = [account for account in self.summaryTuple if "Credit" in account]
        listofDebt = [account for account in self.summaryTuple if "Debt" in account]
        listofTreasury = [account for account in self.summaryTuple if "Treasury" in account]
        listofProperty = [account for account in self.summaryTuple if "Property" in account]

        parentType_dict = {
            "Bank": listofBank,
            "Cash": listofCash,
            "Certificate of Deposit": listofCD,
            "Equity": listofEquity,
            "Treasury": listofTreasury,
            "Property": listofProperty,
            "Retirement": listofRetirement,
            "Credit": listofCredit,
            "Debt": listofDebt,
        }

        # This pre-exists to allow the program to update warnings as needed
        lMessage = QLabel(self)
        lMessage.setObjectName("labelMessages")
        lMessage.setMaximumHeight(40)
        lMessage.setText("")

        messagefont = QtGui.QFont()
        messagefont.setPixelSize(12)
        messagefont.setBold(True)
        messagefont.setUnderline(False)

        lMessage.setFont(messagefont)
        lMessage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        lMessage.setStyleSheet(messageFormat)
        self.ui.vBLayout5.addWidget(lMessage)
        lMessage.hide()
        self.updateMessages.append(lMessage)

        self.row += 1
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Part 1 of Cycle adds Parent Type Header Label
        for parentType in parentType_dict:
            listofAccounts = parentType_dict[parentType]
            if len(listofAccounts) > 0:
                lParent = QLabel(self)
                lParent.setObjectName(f"label{parentType}")
                lParent.setText(f"  {parentType.title()}")
                lParent.setSizePolicy(sizePolicy)
                # lParent.setFixedHeight(65)
                parentfont = QtGui.QFont()
                set_font(parentfont, 24, True, False)

                self.set_formatting(lParent, parentfont, QtCore.Qt.AlignLeft, parentFormat)
                self.ui.vBLayout5.addWidget(lParent)

                self.row += 1

                # Part 2 of Cycle adds Column Labels for the Parent Type
                self.headerhBoxLayout = QtWidgets.QHBoxLayout()
                self.headerhBoxLayout.setObjectName(f"headerBoxLayoutrow{self.row}")
                self.ui.vBLayout5.addLayout(self.headerhBoxLayout)

                lColheader1 = QLabel(self)
                lColheader1.setObjectName("labelAN" + parentType + "header")
                lColheader1.setText("Account Name")
                lColheader1.setFixedHeight(self.labelHeight)
                headerfont = QtGui.QFont()
                set_font(headerfont, 16, True, False)

                lColheader1.setFont(headerfont)
                self.set_formatting(lColheader1, headerfont, QtCore.Qt.AlignHCenter, columnHeader)
                self.headerhBoxLayout.addWidget(lColheader1)

                lColheader2 = QLabel(self)
                lColheader2.setObjectName("labelAT" + parentType + "header")
                lColheader2.setText("Account Type")
                lColheader2.setFont(headerfont)
                lColheader2.setFixedHeight(self.labelHeight)
                self.set_formatting(lColheader2, headerfont, QtCore.Qt.AlignHCenter, columnHeader)
                self.headerhBoxLayout.addWidget(lColheader2)

                if parentType in ["Equity", "Retirement"]:
                    lColheaderShares = QLabel(self)
                    lColheaderShares.setObjectName(f"labelSB{parentType}header")
                    lColheaderShares.setText("Share Balance")
                    lColheaderShares.setFont(headerfont)
                    lColheaderShares.setFixedHeight(self.labelHeight)
                    self.set_formatting(lColheaderShares, headerfont, QtCore.Qt.AlignHCenter, columnHeader)
                    self.headerhBoxLayout.addWidget(lColheaderShares)

                lColheader3 = QLabel(self)
                lColheader3.setObjectName("labelB" + parentType + "header")
                lColheader3.setText("Balance")
                lColheader3.setFont(headerfont)
                lColheader3.setFixedHeight(self.labelHeight)
                self.set_formatting(lColheader3, headerfont, QtCore.Qt.AlignHCenter, columnHeader)
                self.headerhBoxLayout.addWidget(lColheader3)

                self.row += 1

                # Part 3 adds a VBoxLayout to add all of the account labels to
                self.accountVBoxLayout = QtWidgets.QVBoxLayout()
                self.accountVBoxLayout.setObjectName(f"{self.row}VBoxLayout{parentType}")
                self.accountLayoutdic[parentType] = self.accountVBoxLayout
                self.ui.vBLayout5.addLayout(self.accountVBoxLayout)

                for account in listofAccounts:
                    accountID = remove_space(account[3])

                    # Part 3b adds a HBoxLayout per account in the Parent Type
                    self.accountHBoxLayout = QtWidgets.QHBoxLayout()
                    self.accountHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{self.row}")
                    self.accountVBoxLayout.addLayout(self.accountHBoxLayout)

                    # [Asset/Liability, ParentType, Subtype, ID, Balance]

                    verticalSpacer = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    self.accountHBoxLayout.addItem(verticalSpacer)

                    accountFont = QtGui.QFont()
                    set_font(accountFont, 16, False, False)

                    lID = QLabel(self)
                    lID.setObjectName(f"labelAN{accountID}")
                    lID.setText(account[3].title())
                    lID.setFont(accountFont)
                    lID.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
                    lID.setStyleSheet(accountDetails)
                    lID.setWordWrap(True)
                    lID.setFixedHeight(self.labelHeight)
                    self.accountHBoxLayout.addWidget(lID)

                    lSubType = QLabel(self)
                    lSubType.setObjectName(f"labelAT{accountID}")
                    lSubType.setText(account[2].title())
                    lSubType.setFont(accountFont)
                    lSubType.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignHCenter)
                    lSubType.setStyleSheet(accountDetails)
                    lSubType.setFixedHeight(self.labelHeight)
                    self.accountHBoxLayout.addWidget(lSubType)

                    if parentType in ["Equity", "Retirement"]:
                        shareBalance_Statement = f"SELECT SUM(Purchased - Sold) FROM '{accountID}'"
                        shareBalance_raw = obtain_sql_value(shareBalance_Statement, self.refUserDB, self.error_Logger)
                        if shareBalance_raw[0] is None:
                            shareBalance_checked = 0
                        else:
                            shareBalance_checked = shareBalance_raw[0]
                        shareBalance = decimal_places(shareBalance_checked, 4)
                        lShareBalance = QLabel(self)
                        lShareBalance.setObjectName(f"lShareBalance{accountID}")
                        lShareBalance.setText(str(shareBalance))
                        lShareBalance.setFont(accountFont)
                        lShareBalance.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignHCenter)
                        lShareBalance.setStyleSheet(accountDetails)
                        lShareBalance.setFixedHeight(self.labelHeight)
                        self.accountHBoxLayout.addWidget(lShareBalance)

                    lBalance = QLabel(self)
                    lBalance.setObjectName("labelBal" + accountID)
                    self.balancelabeldic[account[3]] = lBalance

                    if account[0] == "Liability":
                        raw_Balance = - account[4]
                    else:
                        raw_Balance = account[4]

                    modBalance = decimal_places(raw_Balance, 2)
                    subTotal += modBalance

                    raw_Balance = float(raw_Balance)
                    balance_formatted = cash_format(raw_Balance, 2)
                    lBalance.setText(balance_formatted[2])

                    lBalance.setFont(accountFont)
                    lBalance.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                    lBalance.setStyleSheet(accountDetails)
                    lBalance.setFixedHeight(self.labelHeight)
                    self.accountHBoxLayout.addWidget(lBalance)

                    self.row += 1

                    # Part 3C adds a progress bar for the Debt and Credit accounts
                    if parentType == "Debt" or parentType == "Credit":
                        self.progressHBoxLayout = QtWidgets.QHBoxLayout()
                        self.progressHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{self.row}")
                        self.accountVBoxLayout.addLayout(self.progressHBoxLayout)

                        self.hSpacer = QtWidgets.QSpacerItem(self.progress_width, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                        self.progressHBoxLayout.addItem(self.hSpacer)

                        labelprogress = QLabel(self)
                        labelprogress.setObjectName("labelProg" + accountID)
                        if parentType == "Debt":
                            labelprogress.setText("Percent Remaining:")
                        else:
                            labelprogress.setText("Credit Available:")
                        progressfont = QtGui.QFont()
                        set_font(progressfont, 12, True, False)
                        labelprogress.setFont(progressfont)
                        labelprogress.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                        self.progressHBoxLayout.addWidget(labelprogress)

                        debtprogressBar = QProgressBar(self)
                        debtprogressBar.setMinimum(0)
                        debtprogressBar.setMaximum(100)

                        if parentType == "Debt":
                            start_statement = f"SELECT Starting_Balance FROM Debt_Account_Details WHERE Account_Name='{account[3]}'"
                            start = obtain_sql_value(start_statement, self.refUserDB, self.error_Logger)
                            start = start[0]
                            progress = (decimal_places(account[4], 2) / decimal_places(start, 2)) * 100
                            progress = int(progress)
                        else:
                            start_statement = f"SELECT Credit_Limit FROM Credit_Account_Details WHERE Account_Name='{account[3]}'"
                            start = obtain_sql_value(start_statement, self.refUserDB, self.error_Logger)
                            start = start[0]
                            progress = 100 - ((decimal_places(account[4], 2) / decimal_places(start, 2)) * 100)
                            progress = int(progress)

                        debtprogressBar.setProperty("value", progress)
                        debtprogressBar.setObjectName("progressBar" + accountID)
                        # label dictionary[AccountName] = label for ProgressBar
                        self.progBardic[account[3]] = debtprogressBar
                        self.progressHBoxLayout.addWidget(debtprogressBar)

                    self.row += 1

                self.subTotalHBoxLayout = QtWidgets.QHBoxLayout()
                self.subTotalHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{self.row}")
                self.ui.vBLayout5.addLayout(self.subTotalHBoxLayout)

                subtotalSpacer_width = self.summaryFrame_width * 0.55
                self.hSpacer = QtWidgets.QSpacerItem(subtotalSpacer_width, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                self.subTotalHBoxLayout.addItem(self.hSpacer)

                labelTotal = QLabel(self)
                labelTotal.setObjectName("label" + parentType + "total")
                labelTotal.setText("Subtotal")
                totalfont = QtGui.QFont()
                set_font(totalfont, 16, True, False)
                labelTotal.setFont(totalfont)
                labelTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                labelTotal.setFixedHeight(self.labelHeight)
                self.subTotalHBoxLayout.addWidget(labelTotal)

                labelSubTotal = QLabel(self)
                labelSubTotal.setObjectName("label" + parentType + "Subtotal")
                # label dictionary[ParentType] = label for SubType Balances
                self.subtotaldic[parentType] = labelSubTotal

                if parentType == "Debt" or parentType == "Credit":
                    subTotal = - subTotal

                subTotal = cash_format(subTotal, 2)
                labelSubTotal.setText(subTotal[2])

                labelSubTotal.setFont(totalfont)
                labelSubTotal.setFrameShape(QFrame.Panel)
                labelSubTotal.setFrameShadow(QFrame.Sunken)
                labelSubTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                labelSubTotal.setStyleSheet(subtotalBalanceFormat)
                labelSubTotal.setFixedHeight(self.labelHeight)
                subTotal_Balance_width = self.summaryFrame_width * 0.45
                labelSubTotal.setFixedWidth(subTotal_Balance_width)
                self.subTotalHBoxLayout.addWidget(labelSubTotal)

                self.row += 1
                subTotal = 0
            else:
                pass

    def refresh_balance_labels(self):
        current_accounts_statement = f"SELECT ItemType, ParentType, SubType, ID, Balance FROM Account_Summary"
        current_accounts_raw = obtain_sql_list(current_accounts_statement, self.refUserDB, self.error_Logger)
        current_accounts = []

        for account in current_accounts_raw:
            if account[3] not in self.balancelabeldic:
                current_accounts.append(account)

        if len(current_accounts) > 0:
            for account in current_accounts:
                try:
                    target_layout = self.accountLayoutdic[account[1]]
                except KeyError:
                    target_layout = QtWidgets.QVBoxLayout()
                    target_layout.setObjectName(f"{self.row}VBoxLayout{account[1]}")
                    self.accountLayoutdic[account[1]] = target_layout
                finally:
                    self.row += 1
                    parentType = account[1]
                    accountID = remove_space(account[3])

                    self.accountHBoxLayout = QtWidgets.QHBoxLayout()
                    self.accountHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{self.row}")
                    target_layout.addLayout(self.accountHBoxLayout)

                    # [Asset/Liability, ParentType, Subtype, ID, Balance]
                    verticalSpacer = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    self.accountHBoxLayout.addItem(verticalSpacer)

                    accountFont = QtGui.QFont()
                    set_font(accountFont, 16, False, False)

                    lID = QLabel(self)
                    lID.setObjectName(f"labelAN{accountID}")
                    lID.setText(account[3].title())
                    lID.setFont(accountFont)
                    lID.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
                    lID.setStyleSheet(accountDetails)
                    lID.setFixedHeight(self.labelHeight)
                    self.accountHBoxLayout.addWidget(lID)

                    lSubType = QLabel(self)
                    lSubType.setObjectName(f"labelAT{accountID}")
                    lSubType.setText(account[2].title())
                    lSubType.setFont(accountFont)
                    lSubType.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
                    lSubType.setStyleSheet(accountDetails)
                    lSubType.setFixedHeight(self.labelHeight)
                    self.accountHBoxLayout.addWidget(lSubType)

                    if parentType in ["Equity", "Retirement"]:
                        shareBalance_Statement = f"SELECT SUM(Purchased - Sold) FROM '{accountID}'"
                        shareBalance_raw = obtain_sql_value(shareBalance_Statement, self.refUserDB, self.error_Logger)
                        if shareBalance_raw[0] is None:
                            shareBalance_checked = 0
                        else:
                            shareBalance_checked = shareBalance_raw[0]
                        shareBalance = decimal_places(shareBalance_checked, 4)
                        lShareBalance = QLabel(self)
                        lShareBalance.setObjectName(f"lShareBalance{accountID}")
                        lShareBalance.setText(str(shareBalance))
                        lShareBalance.setFont(accountFont)
                        lShareBalance.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
                        lShareBalance.setStyleSheet(accountDetails)
                        lShareBalance.setFixedHeight(self.labelHeight)
                        self.accountHBoxLayout.addWidget(lShareBalance)

                    lBalance = QLabel(self)
                    lBalance.setObjectName("labelBal" + accountID)
                    self.balancelabeldic[account[3]] = lBalance

                    if account[0] == "Liability":
                        raw_Balance = - account[4]
                    else:
                        raw_Balance = account[4]

                    raw_Balance = float(raw_Balance)
                    balance_formatted = cash_format(raw_Balance, 2)
                    lBalance.setText(balance_formatted[2])

                    lBalance.setFont(accountFont)
                    lBalance.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                    lBalance.setStyleSheet(accountDetails)
                    lBalance.setFixedHeight(self.labelHeight)
                    self.accountHBoxLayout.addWidget(lBalance)

                    self.row += 1

                    if parentType == "Debt" or parentType == "Credit":
                        self.progressHBoxLayout = QtWidgets.QHBoxLayout()
                        self.progressHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{self.row}")
                        target_layout.addLayout(self.progressHBoxLayout)

                        self.hSpacer = QtWidgets.QSpacerItem(self.progress_width, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                        self.progressHBoxLayout.addItem(self.hSpacer)

                        labelprogress = QLabel(self)
                        labelprogress.setObjectName("labelProg" + accountID)
                        if parentType == "Debt":
                            labelprogress.setText("Percent Remaining:")
                        else:
                            labelprogress.setText("Credit Available:")

                        progressfont = QtGui.QFont()
                        set_font(progressfont, 12, True, False)
                        labelprogress.setFont(progressfont)
                        labelprogress.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                        self.progressHBoxLayout.addWidget(labelprogress)

                        debtprogressBar = QProgressBar(self)
                        debtprogressBar.setMinimum(0)
                        debtprogressBar.setMaximum(100)

                        if parentType == "Debt":
                            start_statement = f"SELECT Starting_Balance FROM Debt_Account_Details WHERE Account_Name='{account[3]}'"
                            start = obtain_sql_value(start_statement, self.refUserDB, self.error_Logger)
                            start = start[0]
                            progress = (decimal_places(account[4], 2) / decimal_places(start, 2)) * 100
                            progress = int(progress)
                        else:
                            start_statement = f"SELECT Credit_Limit FROM Credit_Account_Details WHERE Account_Name='{account[3]}'"
                            start = obtain_sql_value(start_statement, self.refUserDB, self.error_Logger)
                            start = start[0]
                            progress = 100 - ((decimal_places(account[4], 2) / decimal_places(start, 2)) * 100)
                            progress = int(progress)

                        debtprogressBar.setProperty("value", progress)
                        debtprogressBar.setObjectName("progressBar" + accountID)
                        # label dictionary[AccountName] = label for ProgressBar
                        self.progBardic[account[3]] = debtprogressBar
                        self.progressHBoxLayout.addWidget(debtprogressBar)

        for account in self.balancelabeldic:
            balanceStatement = f"SELECT Balance, ItemType, ParentType FROM Account_Summary WHERE ID='{account}'"
            accountInfo = obtain_sql_value(balanceStatement, self.refUserDB, self.error_Logger)

            if accountInfo is None:
                accountInfo = (0.00, "Deleted", "Deleted")

            modBalance = add_comma(accountInfo[0],  2)
            targetlabel = self.balancelabeldic[account]

            if accountInfo[1] == "Liability":
                if accountInfo[0] >= 0:
                    targetlabel.setText(f"(${modBalance})")
                else:
                    targetlabel.setText(f"${modBalance}")
            elif accountInfo[1] == "Deleted":
                targetlabel.setText("$ 0.00")
            else:
                if accountInfo[0] >= 0:
                    targetlabel.setText(f"${modBalance}")
                else:
                    targetlabel.setText(f"(${modBalance})")

            if account in self.progBardic:
                if accountInfo[2] == "Debt":
                    start = self.obtain_liability_start("Starting_Balance", "Debt_Account_Details", account)
                    progress = (decimal_places(accountInfo[0], 2) / decimal_places(start, 2)) * 100
                    progress = int(progress)
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)
                elif accountInfo[2] == "Deleted":
                    progress = 100
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)
                else:
                    start = self.obtain_liability_start("Credit_Limit", "Credit_Account_Details", account)
                    progress = 100 - ((decimal_places(accountInfo[0], 2) / decimal_places(start, 2)) * 100)
                    progress = int(progress)
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)

        for parentType in self.subtotaldic:
            if parentType == "Certificate of Deposit":
                sqlparentType = "CD"
            elif parentType == "Treasury Bonds":
                sqlparentType = "Treasury"
            else:
                sqlparentType = parentType
            subTotalStatement = f"SELECT SUM(Balance), ItemType FROM Account_Summary WHERE ParentType='{sqlparentType}'"
            subTotalInfo = obtain_sql_value(subTotalStatement, self.refUserDB, self.error_Logger)
            preModSubTotal = subTotalInfo[0]

            if preModSubTotal is None:
                preModSubTotal = 0.0

            if subTotalInfo[1] == "Liability":
                raw_Balance = - preModSubTotal
            else:
                raw_Balance = preModSubTotal

            modBalance = decimal_places(raw_Balance, 2)
            modSubTotal = add_comma(modBalance, 2)
            targetlabel = self.subtotaldic[parentType]

            if modBalance > 0:
                targetlabel.setText("  $  " + modSubTotal + "    ")
            elif modBalance == 0:
                targetlabel.setText("$  0.00     ")
            else:
                targetlabel.setText("  ($  " + modSubTotal + ")    ")

    def obtain_liability_start(self, col, tableName, accountName):
        startStatement = f"SELECT {col} FROM {tableName} WHERE Account_Name='{accountName}'"
        start_value_raw = obtain_sql_value(startStatement, self.refUserDB, self.error_Logger)
        start_value = start_value_raw[0]

        if start_value is None:
            start_value = 0.00

        return start_value

    def user_messages(self):
        accountStatement = "SELECT ID FROM Account_Summary"
        accountList = obtain_sql_list(accountStatement, self.refUserDB, self.error_Logger)
        currentQTYaccounts = len(accountList)
        oldQTYaccounts = len(self.summaryTuple)
        messagelabel = self.updateMessages[0]

        changes = "Reload Summary Page to Display New Accounts or Remove Old Accounts"

        if currentQTYaccounts != oldQTYaccounts:
            messagelabel.setText(changes)
            messagelabel.show()

    def update_plot(self, focus, canvas):
        """ Generates a Ring Style Pie Chart, for Asset and Liability distributions on the Summary Page."""
        # focus = "Asset" or "Liability"
        segment_balances, segment_data, segment_colors = snapshot_chart(self.refUserDB, graph_focus=focus, error_log=self.error_Logger)
        # pie_data = [segment_data = [parent, percentage, value], segment_colors]

        canvas.axes.clear()
        canvas.axes.pie(segment_balances,
                        radius=1.5,
                        colors=segment_colors,
                        counterclock=True,
                        startangle=90,
                        wedgeprops={'linewidth': 0.2, 'edgecolor': 'grey', 'width': 0.4},
                        normalize=True)

        LegendLabels = []
        for segment in segment_data:
            parent = segment[0]
            percentage = segment[1]
            balance = segment[2]
            if percentage > 0:
                LegendLabels.append(f"{parent} - {percentage}%\n[{balance}]")

        canvas.axes.legend(
            loc="center",
            labels=LegendLabels,
            ncol=1,
            fontsize=3.5,
            bbox_to_anchor=(0.52, 0.5),
            frameon=False,
        )
        canvas.draw()

    # --- Receive a message from the MainWindow to refresh -----------------------
    @Slot(str)
    def refresh_summary(self, message):
        if message == "2":
            self.update_plot("Asset", self.assetCanvas)
            self.update_plot("Liability", self.liabilityCanvas)
            self.refresh_balance_labels()
            self.user_messages()
        else:
            print("Error: Summary_Func: refresh_summary")

    # --- Pyside6 signal to remove ParentType Ledger from tabdic ---------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_LS.emit("Summary")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")
