"""
This script is the backend to Frontend.SummaryUi.py

Future Concepts
1)

"""
import sys

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QFrame, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QProgressBar
from PySide6.QtCore import Slot

# from Frontend.StyleSheets import messagesheet, innerframesheet, progressSheet, parentypeSheet, colheadersheet, subtotalsheet,\
#     accountsheet
from Frontend.SummaryUi import Ui_Summary

from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value
from Toolbox.Formatting_Tools import add_comma, cash_format, decimal_places, remove_comma, remove_space
from Toolbox.AF_Tools import set_font

# from Backend.BuildGraphs import nested_snapshot, AF_Canvas


class Ledger_Summary(QDialog):
    remove_tab_LS = QtCore.Signal(str)

    def __init__(self, parent, database, error_Log):
        super().__init__(parent)
        self.ui = Ui_Summary()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.summaryTuple = None
        # label dictionary[AccountName] = label for Account Balances
        self.balancelabeldic = {}
        # label dictionary[ParentType] = label for SubType Balances
        self.subtotaldic = {}
        # label dictionary[AccountName] = label for ProgressBar
        self.progBardic = {}
        self.updateMessages = []

        # Program Error Log
        self.error_Logger = error_Log

        # Asset Nested Pie Graph
        # self.assetCanvas = AF_Canvas(self, width=5, height=4, dpi=200)
        # self.aCanvasLayout = QVBoxLayout(self.frameAGraph)
        # self.aCanvasLayout.addWidget(self.assetCanvas)
        # self.update_plot(focus="Asset", canvas=self.assetCanvas)

        # Liability Nested Pie Graph
        # self.liabilityCanvas = AF_Canvas(self, width=5, height=4, dpi=200)
        # self.lCanvasLayout = QVBoxLayout(self.frameAGraph)
        # self.lCanvasLayout.addWidget(self.liabilityCanvas)
        # self.update_plot(focus="Asset", canvas=self.liabilityCanvas)

        # Build Summary Display
        summaryStatement = """SELECT ItemType, ParentType, SubType, ID, Balance FROM Account_Summary """ \
                           + """ORDER BY "ItemType", "ParentType", "SubType", "Balance" DESC LIMIT 0, 49999"""
        self.summaryTuple = obtain_sql_list(summaryStatement, self.refUserDB, self.error_Logger)
        self.generate_summary()

        parent.refresh_signal_summary.connect(self.refresh_summary)

    def set_formatting(self, target, font, Alignment, stylesheet):
        target.setFont(font)
        target.setFrameShape(QFrame.Panel)
        target.setFrameShadow(QFrame.Sunken)
        target.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | Alignment)
        target.setStyleSheet(stylesheet)

    def generate_summary(self):
        summaryFrame_width = self.ui.frameSummary.geometry().width()
        row = 0
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
            "Treasury Bonds": listofTreasury,
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
        messagefont.setPointSize(12)
        messagefont.setBold(True)
        messagefont.setUnderline(False)

        lMessage.setFont(messagefont)
        lMessage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        lMessage.setFrameShape(QFrame.Panel)
        lMessage.setFrameShadow(QFrame.Plain)
        self.ui.vBLayout5.addWidget(lMessage)
        lMessage.hide()
        self.updateMessages.append(lMessage)

        row += 1

        for parentType in parentType_dict:
            listofAccounts = parentType_dict[parentType]
            if len(listofAccounts) > 0:
                lParent = QLabel(self)
                lParent.setObjectName(f"label{parentType}")
                lParent.setText(f"  {parentType.title()}")

                parentfont = QtGui.QFont()
                set_font(parentfont, 24, True, False)

                lParent.setFont(parentfont)
                self.ui.vBLayout5.addWidget(lParent)

                row += 1

                self.headerhBoxLayout = QtWidgets.QHBoxLayout()
                self.headerhBoxLayout.setObjectName(f"headerBoxLayoutrow{row}")
                self.ui.vBLayout5.addLayout(self.headerhBoxLayout)

                lColheader1 = QLabel(self)
                lColheader1.setObjectName("labelAN" + parentType + "header")
                lColheader1.setText("Account Name")

                headerfont = QtGui.QFont()
                set_font(headerfont, 16, True, True)

                lColheader1.setFont(headerfont)
                # self.set_formatting(lColheader1, headerfont, QtCore.Qt.AlignHCenter, colheadersheet)
                self.headerhBoxLayout.addWidget(lColheader1)

                lColheader2 = QLabel(self)
                lColheader2.setObjectName("labelAT" + parentType + "header")
                lColheader2.setText("Account Type")
                lColheader2.setFont(headerfont)
                # self.set_formatting(labelColheader2, headerfont, QtCore.Qt.AlignHCenter, colheadersheet)
                self.headerhBoxLayout.addWidget(lColheader2)

                if parentType in ["Equity", "Retirement"]:
                    lColheaderShares = QLabel(self)
                    lColheaderShares.setObjectName(f"labelSB{parentType}header")
                    lColheaderShares.setText("Share Balance")
                    lColheaderShares.setFont(headerfont)
                    self.headerhBoxLayout.addWidget(lColheaderShares)

                lColheader3 = QLabel(self)
                lColheader3.setObjectName("labelB" + parentType + "header")
                lColheader3.setText("Balance")
                lColheader3.setFont(headerfont)
                # self.set_formatting(labelColheader3, headerfont, QtCore.Qt.AlignHCenter, colheadersheet)
                self.headerhBoxLayout.addWidget(lColheader3)

                row += 1

                for account in listofAccounts:
                    accountID = remove_space(account[3])

                    self.accountHBoxLayout = QtWidgets.QHBoxLayout()
                    self.accountHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{row}")
                    self.ui.vBLayout5.addLayout(self.accountHBoxLayout)

                    # [A/L, ParentType, Subtype, ID, Balance]

                    verticalSpacer = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    self.accountHBoxLayout.addItem(verticalSpacer)

                    accountFont = QtGui.QFont()
                    set_font(accountFont, 16, False, False)

                    lID = QLabel(self)
                    lID.setObjectName(f"labelAN{accountID}")
                    lID.setText(account[3].title())
                    lID.setFont(accountFont)
                    lID.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
                    # labelID.setStyleSheet(accountsheet)
                    self.accountHBoxLayout.addWidget(lID)

                    lSubType = QLabel(self)
                    lSubType.setObjectName(f"labelAT{accountID}")
                    lSubType.setText(account[2].title())
                    lSubType.setFont(accountFont)
                    lSubType.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
                    # lSubType.setStyleSheet(accountsheet)
                    self.accountHBoxLayout.addWidget(lSubType)

                    if parentType in ["Equity", "Retirement"]:
                        shareBalance_Statement = f"SELECT SUM(Purchased - Sold) FROM {accountID}"
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
                    self.accountHBoxLayout.addWidget(lBalance)

                    row += 1

                    self.accountHBoxLayout = QtWidgets.QHBoxLayout()
                    self.accountHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{row}")
                    self.ui.vBLayout5.addLayout(self.accountHBoxLayout)

                    if parentType == "Debt" or parentType == "Credit":
                        progress_width = summaryFrame_width * (2 / 3)
                        self.hSpacer = QtWidgets.QSpacerItem(progress_width, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                        self.accountHBoxLayout.addItem(self.hSpacer)

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
                        self.accountHBoxLayout.addWidget(labelprogress)

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
                        self.accountHBoxLayout.addWidget(debtprogressBar)

                    row += 1

                self.accountHBoxLayout = QtWidgets.QHBoxLayout()
                self.accountHBoxLayout.setObjectName(f"{accountID}BoxLayoutrow{row}")
                self.ui.vBLayout5.addLayout(self.accountHBoxLayout)

                subtotalSpacer_width = summaryFrame_width * (2/3)
                self.hSpacer = QtWidgets.QSpacerItem(subtotalSpacer_width, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                self.accountHBoxLayout.addItem(self.hSpacer)

                labelTotal = QLabel(self)
                labelTotal.setObjectName("label" + parentType + "total")
                labelTotal.setText("Subtotal")
                totalfont = QtGui.QFont()
                set_font(totalfont, 16, True, False)
                labelTotal.setFont(totalfont)
                labelTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                self.accountHBoxLayout.addWidget(labelTotal)

                labelSubTotal = QLabel(self)
                labelSubTotal.setObjectName("label" + parentType + "Subtotal")
                # label dictionary[ParentType] = label for SubType Balances
                self.subtotaldic[parentType] = labelSubTotal

                if parentType == "Debt" or parentType == "Credit":
                    subTotal = - subTotal

                subTotal = cash_format(subTotal, 2)
                labelSubTotal.setText(subTotal[2])

                labelSubTotal.setFont(accountFont)
                labelSubTotal.setFrameShape(QFrame.Panel)
                labelSubTotal.setFrameShadow(QFrame.Sunken)
                labelSubTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                # labelSubTotal.setStyleSheet(subtotalsheet)
                self.accountHBoxLayout.addWidget(labelSubTotal)

                row += 1
                subTotal = 0
            else:
                pass

    def refresh_balance_labels(self):
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
            subTotalStatement = "SELECT SUM(Balance), ItemType FROM Account_Summary WHERE ParentType='" + sqlparentType + "'"
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
        startStatement = "SELECT " + col + " FROM " + tableName + " WHERE Account_Name='" + accountName + "'"
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
        # messagelabel.setStyleSheet(messagesheet)

        changes = "Reload Summary Page to Display New Accounts or Remove Old Accounts"

        if currentQTYaccounts != oldQTYaccounts:
            messagelabel.setText(changes)
            messagelabel.show()

    # def update_plot(self, focus, canvas):
    #     pie_data = nested_snapshot(self.refUserDB, graph_focus=focus)
    #     canvas.axes.clear()
    #     canvas.axes.pie(pie_data[0], radius=1.5, colors=pie_data[1], wedgeprops={'linewidth': 0.5, 'edgecolor': 'grey', 'width': 0.3})
    #     canvas.axes.pie(pie_data[2], radius=1.2, colors=pie_data[3], wedgeprops={'linewidth': 0.3, 'edgecolor': 'grey', 'width': 0.25})
    #     if focus == "Asset":
    #         assetSizes = pie_data[4]
    #         LegendLabels = ["Bank - ({0}%)".format(assetSizes[0]),
    #                         "Cash - ({0}%)".format(assetSizes[1]),
    #                         "CD - ({0}%)".format(assetSizes[2]),
    #                         "Equity - ({0}%)".format(assetSizes[3]),
    #                         "Treasury - ({0}%)".format(assetSizes[4]),
    #                         "Retirement - ({0}%)".format(assetSizes[5]),
    #                         "Property - ({0}%)".format(assetSizes[6])]
    #
    #     elif focus == "Liability":
    #         liabilitySizes = pie_data[4]
    #         LegendLabels = ["Debt - ({0}%)".format(liabilitySizes[0]),
    #                         "Credit - ({0}%)".format(liabilitySizes[1])]
    #     else:
    #         LegendLabels = ["Input Error: Asset/Liability only"]
    #
    #     canvas.axes.legend(
    #         loc="center",
    #         labels=LegendLabels,
    #         ncol=1,
    #         fontsize=3.5,
    #         bbox_to_anchor=(0.52, 0.5),
    #         frameon=False,
    #     )
    #     canvas.draw()

    # --- Receive a message from the MainWindow to refresh -----------------------
    @Slot(str)
    def refresh_summary(self, message):
        if message == "2":
            # self.update_plot("Asset", self.assetCanvas)
            # self.update_plot("Liability", self.liabilityCanvas)
            self.refresh_balance_labels()
            self.user_messages()
        else:
            print("Error: Summary_Func: refresh_summary")

    # --- PyQt5 signal to remove ParentType Ledger from tabdic ---------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_LS.emit("Summary")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")
