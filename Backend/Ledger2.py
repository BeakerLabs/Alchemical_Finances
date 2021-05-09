"""
This script is the backend to Frontend.Ledger2Ui.py

Future Concepts


Warning: While many bad practices have been fixed between the Alpha program and the Release build. Some Artifacts may survive; such as
the center and right display frames were previously referred to as variable1 [ShareBalance] and variable2 [variable1]. Refer to the Ui file
to clarify function/purpose of any given object.
"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import os

from PySide2.QtWidgets import QMessageBox, QDialog, QFileDialog, QInputDialog
from PySide2.QtCore import QDate
from PySide2 import QtGui, QtCore, QtWidgets

from pathlib import Path, PurePath
from shutil import copy

from Backend.AccountDetails import AccountsDetails
from Backend.LedgerDataAnalysis import equity_subtype_data
from Backend.SpendingCategories import SpendingCategories
from Backend.ReceiptViewer import Receipt

from Frontend.Ledger2Ui import Ui_Ledger2

from Toolbox.AF_Tools import disp_LedgerV2_Table, fill_widget, find_mult_row, fill_statement_period, rename_image, set_font
from Toolbox.Error_Tools import check_characters, check_numerical_inputs
from Toolbox.Formatting_Tools import add_comma, decimal_places, remove_comma, remove_space
from Toolbox.SQL_Tools import execute_sql_statement_list, obtain_sql_value, specific_sql_statement, sqlite3_keyword_check
from Toolbox.OS_Tools import file_destination

from StyleSheets.StandardCSS import standardAppearance
from StyleSheets.LedgerCSS import transFrame, spendingLabel


class LedgerV2(QDialog):
    refresh_signal_L2 = QtCore.Signal(str)
    remove_tab_L2 = QtCore.Signal(str)

    def __init__(self, database, parentType, user, error_log):
        super().__init__()
        self.ui = Ui_Ledger2()
        self.ui.setupUi(self)
        self.setWindowTitle(parentType)
        self.show()

        # Class Global Variables
        self.refUserDB = database
        self.parentType = parentType
        self.refUser = user

        self.parentType_dict = {
            "Bank": "Bank_Account_Details",
            "Cash": "Cash_Account_Details",
            "CD": "CD_Account_Details",
            "Treasury": "Treasury_Account_Details",
            "Credit": "Credit_Account_Details",
            "Debt": "Debt_Account_Details",
            "Equity": "Equity_Account_Details",
            "Retirement": "Retirement_Account_Details",
            "Property": "Property_Account_Details",
        }

        self.subType_label_dict = {}
        self.investment_label_dict = {}
        self.sector_label_dict = {}

        # Program Error Logger
        self.error_Logger = error_log

        # Prepare Widgets for initial Use
        self.comboBoxAccountStatement = f"SELECT ID FROM Account_Summary WHERE ParentType= '{self.parentType}'"
        fill_widget(self.ui.comboBLedger2, self.comboBoxAccountStatement, True, self.refUserDB, self.error_Logger)
        self.comboBoxCategoriesStatement = f"SELECT Method FROM Categories WHERE ParentType= '{self.parentType}'"
        fill_widget(self.ui.comboBCategory, self.comboBoxCategoriesStatement, True, self.refUserDB, self.error_Logger)

        if self.ui.comboBLedger2.currentText() == "":
            self.toggle_entire_ledger(False)
        else:
            fill_statement_period(self.ui.comboBLedger2, self.ui.comboBPeriod, "Ledger", self.refUserDB, self.error_Logger)

        self.build_tabWidget_display("SubType")
        self.build_tabWidget_display("Investment")
        self.build_tabWidget_display("Sector")

        # Ledger Widget Functionality
        self.ui.comboBLedger2.currentIndexChanged.connect(self.change_ledger2_account)
        self.ui.comboBPeriod.currentIndexChanged.connect(self.display_ledger_2)
        self.ui.DateEditTransDate.setDate(QDate.currentDate())
        self.ui.rBPending.setChecked(True)

        self.ui.pBModAccount.clicked.connect(self.accounts_dialog)
        self.ui.pBCatModify.clicked.connect(self.categories_dialog)

        self.ui.pBAddTransaction.clicked.connect(self.add_transaction)
        self.ui.pBSelect.clicked.connect(self.select_transaction)
        self.ui.pBUpdate.clicked.connect(self.update_transaction)
        self.ui.pBDelete.clicked.connect(self.delete_transaction)
        self.ui.pBClearInputs.clicked.connect(self.clear_inputs)
        self.ui.pBUStockPrice.clicked.connect(self.update_ticker_price)

        self.ui.pBUpload.clicked.connect(self.upload_receipt_button)
        self.ui.pBDisplay.clicked.connect(self.display_receipt)
        self.ui.pBClear.clicked.connect(self.clear_receipt_action)
        self.ui.pBDelete.clicked.connect(self.delete_receipt_action)

        self.change_ledger2_account()

        self.tickerPrice = self.obtain_ticker_price()
        self.ui.lVariable1.setText("$ " + self.tickerPrice)
        self.display_ledger_2()

        self.setStyleSheet(standardAppearance)
        self.ui.lInputFrame.setStyleSheet(transFrame)
        self.ui.rInputFrame.setStyleSheet(transFrame)
        self.ui.leftDisplayFrame.setStyleSheet(transFrame)
        self.ui.centerDisplayFrame.setStyleSheet(transFrame)
        self.ui.rightDisplayFrame.setStyleSheet(transFrame)
        self.ui.ledgerScroll.setStyleSheet(transFrame)
        self.ui.ledgerFrame.setStyleSheet(transFrame)

    # Opens Modal Dialogs for ledger Modification
    def accounts_dialog(self):
        alf = AccountsDetails(self.refUserDB, self.parentType, self.refUser, self.error_Logger)
        if alf.exec_() == QDialog.Accepted:
            self.ui.comboBLedger2.clear()
            self.ui.comboBPeriod.clear()

            self.comboBoxAccountStatement = f"SELECT ID FROM Account_Summary WHERE ParentType= '{self.parentType}'"
            fill_widget(self.ui.comboBLedger2, self.comboBoxAccountStatement, True, self.refUserDB, self.error_Logger)
            if self.ui.comboBLedger2.currentText() != "":
                fill_statement_period(self.ui.comboBLedger2, self.ui.comboBPeriod, "Ledger", self.refUserDB, self.error_Logger)
                self.toggle_entire_ledger(True)
                self.display_ledger_2()
            elif self.ui.comboBLedger2.currentText() == "":
                self.toggle_entire_ledger(False)

            self.ui.comboBLedger2.setCurrentIndex(0)
            self.trigger_refresh()

    def categories_dialog(self):
        molly = SpendingCategories(self.refUserDB, self.parentType, self.error_Logger)
        if molly.exec_() == QDialog.Accepted:
            self.ui.comboBCategory.clear()
            self.comboBoxCategoriesStatement = f"SELECT Method FROM Categories WHERE ParentType= '{self.parentType}'"
            fill_widget(self.ui.comboBCategory, self.comboBoxCategoriesStatement, True, self.refUserDB, self.error_Logger)

    # General Functions
    def check_transactions(self):
        listA = [self.ui.lEditTransDesc, self.ui.lEditSharePrice]
        listB = [self.ui.lEditCredit.text(), self.ui.lEditDebit.text(), self.ui.lEditSharePurch.text(),
                 self.ui.lEditShareSold.text(), self.ui.lEditSharePrice.text(), self.ui.textEditAddNotes.toPlainText()]

        for widget in listA:
            if not check_characters(widget.text(), "general"):
                return False  # Input Has Non Alphanumeric characters

            if widget.text() == "" or widget.text() == " ":
                return False  # Input is Blank

            if sqlite3_keyword_check(widget.text()):
                return False  # No restricted keywords
                # Doesn't account for restricted statements. However, should be unlikely.

            else:
                continue

        for widget in listB:
            if not check_characters(widget, "general"):
                return False  # These are all numerical inputs

        if len(self.ui.textEditAddNotes.toPlainText()) > 150:
            return False  # Limit the Additional Notes field

        if check_numerical_inputs(self.ui.lEditDebit.text()) and check_numerical_inputs(self.ui.lEditCredit.text()):
            return False  # Simultaneous Credit and Debit inputs

        if check_numerical_inputs(self.ui.lEditSharePurch.text()) and check_numerical_inputs(self.ui.lEditShareSold.text()):
            return False  # Simultaneous Share Purchase and Debit Share Sold

        if not check_numerical_inputs(self.ui.lEditSharePrice.text()):
            return False  # Must be numerical

        else:
            # Date, Transaction Description and Share Price are required non-blank inputs.
            # (Debit & Credit) or (Shared Purchased & Sold) can not be simultaneous
            # The Transaction note can not exceed 150 characters
            return True

    def clear_inputs(self):
        self.ui.DateEditTransDate.setDate(QDate.currentDate())
        self.ui.lEditTransDesc.setText("")
        self.ui.comboBCategory.setCurrentIndex(0)
        self.ui.lEditDebit.setText("")
        self.ui.lEditCredit.setText("")
        self.ui.lEditSharePrice.setText("")
        self.ui.lEditSharePurch.setText("")
        self.ui.lEditShareSold.setText("")
        self.ui.textEditAddNotes.setPlainText("")
        self.ui.rBPending.setChecked(True)
        self.clear_receipt_action()
        self.ui.lEditSharePrice.setText("")
        self.ui.lEditTransDesc.setFocus()

    def input_error_msg(self, message):
        reply = QMessageBox.warning(self, 'Input Error', message, QMessageBox.Ok, QMessageBox.NoButton)
        if reply == QMessageBox.Ok:
            pass
        else:
            pass

    def transaction_status(self, status1, status2):
        if status1.isChecked():
            currentStatus1 = "Pending"
            return currentStatus1
        elif status2.isChecked():
            currentStatus2 = "Posted"
            return currentStatus2
        else:
            currentStatus3 = "Unknown"
            return currentStatus3

    def user_selection_input(self, tableWidget, text1, text2):
        row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
        if ok and row:
            return row
        else:
            row = 0
            return row

    # Functions that depend on SQLite3
    def add_transaction(self):
        if self.ui.comboBLedger2.currentText() == "":
            noLedger_msg = "Create a new Ledger"
            self.input_error_msg(noLedger_msg)
        else:
            if self.check_transactions():
                from datetime import datetime
                ledgerName = self.ui.comboBLedger2.currentText()
                modifiedLN = remove_space(ledgerName)
                modDebit = decimal_places(self.ui.lEditDebit.text(), 2)
                modCredit = decimal_places(self.ui.lEditCredit.text(), 2)
                modPurchased = decimal_places(self.ui.lEditSharePurch.text(), 4)
                modSold = decimal_places(self.ui.lEditShareSold.text(), 4)
                modPrice = decimal_places(self.ui.lEditSharePrice.text(), 4)
                status = self.transaction_status(self.ui.rBPending, self.ui.rBPosted)
                currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                # 2- date -- 3- T Description -- 4- Category -- 5- Debit
                # 6- credit -- 8- sold -- 7- Purchased -- 10/11- Status -- ## - UserDate -- 12- Receipt
                addStatement = "INSERT INTO " + modifiedLN + " VALUES('"\
                               + self.ui.DateEditTransDate.date().toString("yyyy/MM/dd") + "', '"\
                               + self.ui.lEditTransDesc.text() + "', '"\
                               + self.ui.comboBCategory.currentText() + "', '"\
                               + str(modDebit) + "', '"\
                               + str(modCredit) + "', '"\
                               + str(modSold) + "', '"\
                               + str(modPurchased) + "', '" \
                               + str(modPrice) + "', '" \
                               + self.ui.textEditAddNotes.toPlainText() + "', '"\
                               + status + "', '"\
                               + self.ui.lEditReceipt.text() + "', '"\
                               + currentDate + "', '"\
                               + currentDate + "')"
                specific_sql_statement(addStatement, self.refUserDB, self.error_Logger)
                self.transaction_refresh()
            else:
                input_error = """
                    Transaction Input Instructions:

                1  :  Ensure these fields are completed
                [T Date, T Desc, Category and Price per share]
                2  :  Alphanumeric inputs only
                3  :  Check the character length of your
                      additional notes input

                """
                self.input_error_msg(input_error)

    def change_ledger2_account(self):
        if self.ui.comboBLedger2.currentText() is None:
            pass
        elif self.ui.comboBLedger2.currentText() == "":
            pass
        else:
            self.ui.comboBPeriod.clear()
            fill_statement_period(self.ui.comboBLedger2, self.ui.comboBPeriod, "Ledger", self.refUserDB, self.error_Logger)
            ledgerValue = self.net_ledger_value()
            self.ui.lAccountBalance.setText(ledgerValue[1])
            self.ui.lShareBalance.setText(self.net_share_balance())
            self.tickerPrice = self.obtain_ticker_price()
            self.ui.lVariable1.setText("$ " + self.tickerPrice)

    def delete_transaction(self):
        ledgerName = self.ui.comboBLedger2.currentText()
        modifiedLN = remove_space(ledgerName)
        inputText1 = "Delete Transaction"
        inputText2 = "Enter Row #: "
        row = self.user_selection_input(self.ui.tableWLedger2, inputText1, inputText2) - 1
        deleteMessage = "Selecting 'OK' will permanently remove " + \
                        "\nrow #: " + str(row + 1) + " from the ledger"
        confirm = QMessageBox.warning(self, 'Confirm', deleteMessage, QMessageBox.Ok, QMessageBox.Cancel)
        if confirm == QMessageBox.Ok:
            deleteStatement = "DELETE FROM " + modifiedLN + " WHERE " \
                              + "Post_Date='" + self.ui.tableWLedger2.item(row, 9).text() + "'"

            specific_sql_statement(deleteStatement, self.refUserDB, self.error_Logger)
            self.transaction_refresh()
        else:
            pass

    def display_ledger_2(self):
        ledger = self.ui.comboBLedger2.currentText()
        statement = self.ui.comboBPeriod.currentText()
        if ledger == "":
            pass
        elif statement == "":
            pass
        else:
            parentType_statement = f"SELECT ParentType FROM Account_Summary WHERE ID='{ledger}'"
            parentType_value = obtain_sql_value(parentType_statement, self.refUserDB, self.error_Logger)
            parentType_value = parentType_value[0]

            if parentType_value in ["Equity", "Retirement"]:
                disp_LedgerV2_Table(self.ui.comboBLedger2, self.ui.comboBPeriod, self.ui.tableWLedger2, self.refUserDB, self.error_Logger)
                ledgerValue = self.net_ledger_value()
                self.ui.lAccountBalance.setText(ledgerValue[1])
                self.ui.lShareBalance.setText(self.net_share_balance())
                self.tickerPrice = self.obtain_ticker_price()
                self.ui.lSharePrice.setText("$ " + self.tickerPrice)
            else:
                error = "Parent Type doesn't belong with this ledger"
                self.input_error_msg(error)

    def get_ticker_price(self):
        price, ok = QInputDialog.getDouble(self, "Ticker Price", "Market Price:", 1.0000, 0, 1000000, 4)
        if ok and price != "":
            return price
        else:
            price = "1.0000"
            return price

    def net_ledger_value(self):
        ledgerName = self.ui.comboBLedger2.currentText()
        modifiedLN = remove_space(ledgerName)
        if ledgerName == "":
            netValue = ["0.00", "0.00"]
            return netValue
        else:
            netValueStatement = "SELECT SUM(Purchased - Sold) FROM " + modifiedLN + " WHERE Status='Posted'"
            qtyShares = obtain_sql_value(netValueStatement, self.refUserDB, self.error_Logger)
            if qtyShares[0] is None:
                netValue = "0.00"
                return netValue
            elif decimal_places(qtyShares[0], 4) <= decimal_places('0.0001', 4):
                moneyWComma = add_comma(qtyShares[0], 2)
                moneyWOComma = "-" + remove_comma(moneyWComma)
                formatString = "($ " + moneyWComma + ")"
                moneylist = [moneyWOComma, formatString]
                return moneylist
            else:
                self.tickerPrice = self.obtain_ticker_price()
                accountValue = decimal_places(self.tickerPrice, 4) * decimal_places(qtyShares[0], 4)
                moneyWComnma = add_comma(accountValue, 2)
                moneyWOComma = remove_comma(moneyWComnma)
                formatString = "$ " + moneyWComnma
                moneylist = [moneyWOComma, formatString]
                return moneylist

    def net_share_balance(self):
        ledgerName = self.ui.comboBLedger2.currentText()
        modifiedLN = remove_space(ledgerName)
        if ledgerName == "":
            shareBalance = "0.0000"
            return shareBalance
        else:
            netSBalance = "SELECT SUM(Purchased - Sold) FROM " + modifiedLN + " WHERE Status='Posted'"
            shareBalance = obtain_sql_value(netSBalance, self.refUserDB, self.error_Logger)
            if shareBalance[0] is None:
                shareBalance = "0.0000"
                return shareBalance
            elif shareBalance[0] < 0:
                shareBalance = "ERROR <0"
                return shareBalance
            else:
                formatedShares = decimal_places(shareBalance[0], 4)
                formatedStrShares = str(formatedShares)
                return formatedStrShares

    def obtain_ticker_price(self):
        tickerPriceStatement = "SELECT Stock_Price FROM " + self.parentType_dict[self.parentType] +\
                                    " WHERE Account_Name ='" + self.ui.comboBLedger2.currentText() + "'"
        tickerPrice = obtain_sql_value(tickerPriceStatement, self.refUserDB, self.error_Logger)
        if tickerPrice is None:
            tickerPrice = "Unknown"
        else:
            tickerPrice = str(decimal_places(tickerPrice[0], 4))
        return tickerPrice

    def refresh_ticker_price(self):
        tickerUpdate = "SELECT Stock_Price FROM " + self.parentType_dict[self.parentType] + " WHERE Account_Name='" + self.ui.comboBLedger2.currentText() + "'"
        tickerPrice = obtain_sql_value(tickerUpdate, self.refUserDB, self.error_Logger)
        updateLedgerValue = decimal_places(tickerPrice[0], 4) * decimal_places(self.ui.lShareBalance.text(), 4)
        updateLedgerValue = decimal_places(updateLedgerValue, 2)
        balanceUpdate = "UPDATE Account_Summary SET Balance='" + str(updateLedgerValue) + "' WHERE ID='" + \
                        self.ui.comboBLedger2.currentText() + "'"
        specific_sql_statement(balanceUpdate, self.refUserDB, self.error_Logger)
        newledgerValue = self.net_ledger_value()
        self.ui.lAccountBalance.setText(newledgerValue[1])
        self.ui.lVariable1.setText("$ " + str(decimal_places(tickerPrice[0], 4)))
        self.trigger_refresh()

    def select_transaction(self):
        self.clear_inputs()
        inputText1 = "Select Row"
        inputText2 = "Enter Row #: "
        row = self.user_selection_input(self.ui.tableWLedger2, inputText1, inputText2) - 1
        if row == -1:
            self.clear_inputs()
        else:
              for col in range(0, 9):
                widget = col + 2
                dataPoint = self.ui.tableWLedger2.item(row, col).text()
                if widget == 2:
                    # col 0 = T Date
                    self.ui.DateEditTransDate.setDate(QDate.fromString(dataPoint, "yyyy/MM/dd"))
                elif widget == 3:
                    # col 1 = T Description
                    self.ui.lEditTransDesc.setText(dataPoint)
                elif widget == 4:
                    # col 2 = Category
                    categoryIndex = self.ui.comboBCategory.findText(dataPoint)
                    if categoryIndex >= 0:
                        self.ui.comboBCategory.setCurrentIndex(categoryIndex)
                    else:
                        lostCategory = "You appear to have deleted that Category. \n\n" + \
                                       "Re-add that Category to select the desired entry.  \n\n" + \
                                       "In the future remove all instances of a given  \n" + \
                                       "Category prior to deleting it from your \n" + \
                                       "options list"
                        self.input_error_msg(lostCategory)
                        self.clear_inputs()
                        break
                elif widget == 5:
                    # col 3 = Amount
                    dataPoint = dataPoint[4:]
                    if dataPoint == "":
                        self.ui.lEditDebit.setText(dataPoint)
                    elif dataPoint[len(dataPoint) - 1:] == ")":
                        dataPoint = dataPoint[1:]
                        dataPoint = dataPoint[:len(dataPoint) - 1]
                        displayValue = remove_comma(dataPoint)
                        self.ui.lEditDebit.setText(displayValue)
                    elif dataPoint[len(dataPoint) - 1:] == " ":
                        dataPoint = dataPoint[:len(dataPoint) - 1]
                        displayValue = remove_comma(dataPoint)
                        adjustment = widget + 1
                        self.ui.lEditCredit.setText(displayValue)
                elif widget == 6:
                    # col 4 = Shares (+/-)
                    if dataPoint == "":
                        self.ui.lEditSharePurch.setText(dataPoint)
                    elif dataPoint[:1] == "-":
                        dataPoint = dataPoint[1:]
                        noCommaValue = remove_comma(dataPoint)
                        self.ui.lEditShareSold.setText(noCommaValue)
                    elif dataPoint[:1] != "-":
                        noCommaValue = remove_comma(dataPoint)
                        self.ui.lEditSharePurch.setText(noCommaValue)
                elif widget == 7:
                    # col 5 = Price/Share
                    if dataPoint == "":
                        self.ui.lEditSharePrice.setText(dataPoint)
                    elif dataPoint[:3] == "  $":
                        dataPoint = dataPoint[3:len(dataPoint)-1]
                        noCommaValue = str(remove_comma(dataPoint))
                        self.ui.lEditSharePrice.setText(noCommaValue)
                elif widget == 8:
                    # col 6 = Status
                    if dataPoint == "Pending":
                        self.ui.rBPending.setChecked(True)
                    elif dataPoint == "Posted":
                        self.ui.rBPosted.setChecked(True)
                    else:
                        self.ui.rBPending.setChecked(True)
                elif widget == 9:
                    # col 7 = Receipt
                    self.ui.lEditReceipt.setText(dataPoint)
                elif widget == 10:
                    # col 8 = Note
                    self.ui.textEditAddNotes.setPlainText(dataPoint)
        return row

    def transaction_refresh(self):
        # Clears Inputs to allow for a new transaction
        self.clear_inputs()

        self.ui.comboBPeriod.clear()
        fill_statement_period(self.ui.comboBLedger2, self.ui.comboBPeriod, "Ledger", self.refUserDB, self.error_Logger)
        disp_LedgerV2_Table(self.ui.comboBLedger2, self.ui.comboBPeriod, self.ui.tableWLedger2, self.refUserDB, self.error_Logger)

        # Changes the Account Balance to reflect the "posted" balance
        ledgerValue = self.net_ledger_value()
        self.ui.lAccountBalance.setText(ledgerValue[1])

        self.ui.lShareBalance.setText(self.net_share_balance())

        # Updates the database Account_Summary to reflect the "posted" balance
        balanceStatement = "UPDATE Account_Summary SET Balance='" + ledgerValue[0] + "' WHERE ID='" + self.ui.comboBLedger2.currentText() + "'"
        specific_sql_statement(balanceStatement, self.refUserDB, self.error_Logger)

        self.update_tab_display("SubType")
        self.update_tab_display("Investment")
        self.update_tab_display("Sector")

        # Triggers to refresh the other variables on the QMainWindow and subsequently the Summary window (if open)
        self.trigger_refresh()

    def update_sql(self, row):
        from datetime import datetime
        ledgerName = self.ui.comboBLedger2.currentText()
        modifiedLN = remove_space(ledgerName)
        modDebit = str(decimal_places(self.ui.lEditDebit.text(), 2))
        modCredit = str(decimal_places(self.ui.lEditCredit.text(), 2))
        modPurchased = str(decimal_places(self.ui.lEditSharePurch.text(), 4))
        modSold = str(decimal_places(self.ui.lEditShareSold.text(), 4))
        modPrice = str(decimal_places(self.ui.lEditSharePrice.text(), 4))
        status = self.transaction_status(self.ui.rBPending, self.ui.rBPosted)
        currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        updateStatement = "Update " + modifiedLN \
                          + " SET Transaction_Date='" + self.ui.DateEditTransDate.date().toString("yyyy/MM/dd") \
                          + "', Transaction_Description='" + self.ui.lEditTransDesc.text() \
                          + "', Category='" + self.ui.comboBCategory.currentText() \
                          + "', Debit='" + modDebit \
                          + "', Credit='" + modCredit \
                          + "', Sold='" + modSold \
                          + "', Purchased='" + modPurchased \
                          + "', Price='" + modPrice \
                          + "', Note='" + self.ui.textEditAddNotes.toPlainText() \
                          + "', Status='" + status \
                          + "', Receipt='" + self.ui.lEditReceipt.text() \
                          + "', Update_Date='" + currentDate \
                          + "' WHERE Post_Date='" + self.ui.tableWLedger2.item(row, 9).text() + "'"
        specific_sql_statement(updateStatement, self.refUserDB, self.error_Logger)

    def update_transaction(self):
        inputText1 = "Update Transaction"
        inputText2 = "Enter Row #: "
        if self.check_transactions() is True:
            row = self.user_selection_input(self.ui.tableWLedger2, inputText1, inputText2) - 1
            if row == -1:
                self.clear_inputs()
            else:
                updateMessage = "Selecting 'OK' will update target row #: " + str(row + 1) + \
                                "\nto the current input values designated"
                reply = QMessageBox.warning(self, 'Verify', updateMessage, QMessageBox.Ok, QMessageBox.Cancel)
                if reply == QMessageBox.Ok:
                    self.update_sql(row)
                    self.transaction_refresh()
                else:
                    pass
        else:
            input_error = """
                Transaction Input Instructions:

            1  :  Ensure these fields are completed
            [T Date, T Desc, Category and Price per share]
            2  :  Alphanumeric inputs only
            3  :  Check the character length of your
                  additional notes input

            """
            self.input_error_msg(input_error)

    def update_ticker_price(self):
        tickerPrice = self.get_ticker_price()
        tickerPrice = decimal_places(tickerPrice, 4)
        tickerUpdate = "UPDATE " + self.parentType_dict[self.parentType] + " SET Stock_Price='" + str(tickerPrice) \
                       + "' WHERE Account_Name='" + self.ui.comboBLedger2.currentText() + "'"
        updateLedgerValue = tickerPrice * decimal_places(self.ui.lShareBalance.text(), 4)
        balanceUpdate = "UPDATE Account_Summary SET Balance='" + str(updateLedgerValue) + "' WHERE ID='" + self.ui.comboBLedger2.currentText() + "'"
        execute_sql_statement_list([tickerUpdate, balanceUpdate], self.refUserDB, self.error_Logger)
        newledgerValue = self.net_ledger_value()
        self.ui.lAccountBalance.setText(newledgerValue[1])
        self.ui.lVariable1.setText("$ " + str(tickerPrice))
        self.trigger_refresh()

    # Functions Associated with Receipts/Invoices
    def clear_receipt_action(self):
        if self.ui.lEditReceipt.text() == "":
            pass
        else:
            oRName = self.ui.lEditReceipt.text()
            self.ui.lEditReceipt.setText("")
            rowList = find_mult_row(self.ui.tableWLedger2, 6, oRName)
            # if no rows are found with the file. The image is just deleted
            if len(rowList) == 0:
                self.ui.lEditReceipt.setText("")
                modifiedLN = remove_space(self.ui.comboBLedger2.currentText())
                oRName_path = file_destination(['Receipts', self.refUser, self.parentType, modifiedLN])
                oRName_path = Path.cwd() / oRName_path / oRName
                os.remove(oRName_path)
            # If >= 1 row is found with the file name. Then the lineEdit is just cleared
            else:
                self.ui.lEditReceipt.setText("")

    def delete_receipt_action(self):
        if self.ui.lEditReceipt.text() == "":
            pass
        else:
            row = find_mult_row(self.ui.tableWLedger2, 6, self.ui.lEditReceipt.text())
            if len(row) == 0:
                self.clear_receipt_action()
            elif len(row) >= 1:
                target_row = self.select_transaction()
                self.clear_receipt_action()
                self.update_sql(target_row)
            else:
                self.clear_receipt_action()

    def display_receipt(self):
        ledger = self.ui.comboBLedger2.currentText()
        modifiedLN = remove_space(ledger)
        fileName = self.ui.lEditReceipt.text()
        suffix = PurePath(fileName).suffix

        receipt_path = file_destination(['Receipts', self.refUser, self.parentType, modifiedLN])
        receipt_path = Path.cwd() / receipt_path / fileName

        if fileName == "":
            noReceipt = "Sorry, No Receipt Uploaded"
            self.input_error_msg(noReceipt)
        elif suffix == ".pdf":
            os.startfile(receipt_path)
        else:
            ion = Receipt(str(receipt_path), fileName)
            if ion.exec_() == QDialog.Accepted:
                pass

    def receipt_check_on_close(self):
        if self.ui.lEditReceipt.text() != "":
            self.clear_receipt_action()

    def upload_receipt_action(self):
        suffixlist = ['.jpg', '.jpeg', 'JPEG', '.gif', '.pdf', '.png']
        rname, _ = QFileDialog.getOpenFileName(self, 'Target Receipt', '/home',
                                               'Images (*.png *.jpg  *.jpeg *.gif);; PDF (*.pdf *.PDF)')
        if rname:
            rname_path = Path(rname)
            suffix = PurePath(rname_path).suffix
            if suffix not in suffixlist:
                wrongType = "Sorry, those files types are not support yet."
                self.input_error_msg(wrongType)
            else:
                nRName = rename_image(self.ui.comboBLedger2, self.ui.comboBCategory) + str(suffix)
                modifiedLN = remove_space(self.ui.comboBLedger2.currentText())
                nRName_path = file_destination(['Receipts', self.refUser, self.parentType, modifiedLN])
                nRName_path = Path.cwd() / nRName_path / nRName
                copy(rname_path, nRName_path)
                self.ui.lEditReceipt.setText(nRName)
        else:
            self.ui.lEditReceipt.setText("")

    def upload_receipt_button(self):
        if self.ui.comboBLedger2.currentText() == "":
            noLedger_msg = "Create a New Ledger"
            self.input_error_msg(noLedger_msg)
        elif self.ui.lEditReceipt.text() != "":
            replace_message = """
            DELETE or CLEAR the receipt before uploading a new one.    
            """
            present = QMessageBox.information(self, 'A Receipt Already Exists', replace_message, QMessageBox.Ok)
            if present == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            self.upload_receipt_action()

    # Asset Graph Frame Functions
    def build_tabWidget_display(self, target_tab):
        subType_data, investment_data, sector_data, subType_string_dict, investment_string_dict, sector_string_dict = equity_subtype_data(self.refUserDB, self.parentType, self.error_Logger)

        label_font = QtGui.QFont()
        set_font(label_font, 12, True, False)

        tab_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        if target_tab == "SubType":
            string_dictionary = subType_string_dict
            label_dictionary = self.subType_label_dict
            layout = self.ui.typeScrollLayout
        elif target_tab == "Investment":
            string_dictionary = investment_string_dict
            label_dictionary = self.investment_label_dict
            layout = self.ui.investmentScrollLayout
        elif target_tab == "Sector":
            string_dictionary = sector_string_dict
            label_dictionary = self.sector_label_dict
            layout = self.ui.sectorScrollLayout
        else:
            raise Exception("Ledger Type 2 Doesn't Contain that Tab Widget")

        for count, Type in enumerate(string_dictionary, start=1):
            self.TypeLabel = QtWidgets.QLabel()
            self.TypeLabel.setObjectName(f"lAssetType{count}")
            self.TypeLabel.setText(string_dictionary[Type])
            self.TypeLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            self.TypeLabel.setFont(label_font)
            self.TypeLabel.setStyleSheet(spendingLabel)
            self.TypeLabel.setSizePolicy(tab_sizePolicy)
            label_dictionary[count] = self.TypeLabel
            layout.addWidget(self.TypeLabel)

    def update_tab_display(self, target_tab):
        subType_data, investment_data, sector_data, subType_string_dict, investment_string_dict, sector_string_dict = equity_subtype_data(self.refUserDB, self.parentType, self.error_Logger)

        label_font = QtGui.QFont()
        set_font(label_font, 12, True, False)

        tab_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        if target_tab == "SubType":
            label_dict = self.subType_label_dict
            string_data = subType_string_dict
            scroll_layout = self.ui.typeScrollLayout
        elif target_tab == "Investment":
            label_dict = self.investment_label_dict
            string_data = investment_string_dict
            scroll_layout = self.ui.investmentScrollLayout
        else:  # target_tab == "Sector":
            label_dict = self.sector_label_dict
            string_data = sector_string_dict
            scroll_layout = self.ui.sectorScrollLayout

        for count, assetType in enumerate(string_data, start=1):
            try:
                target_label = label_dict[count]
                target_label.setText(string_data[assetType])
            except KeyError:
                self.TypeLabel = QtWidgets.QLabel()
                self.TypeLabel.setObjectName(f"lAssetType{count}")
                self.TypeLabel.setText(string_data[assetType])
                self.TypeLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                self.TypeLabel.setFont(label_font)
                self.TypeLabel.setStyleSheet(spendingLabel)
                self.TypeLabel.setSizePolicy(tab_sizePolicy)
                label_dict[assetType] = self.TypeLabel

                scroll_layout.addWidget(self.TypeLabel)

        if len(label_dict) > len(string_data):
            unused_label_count = len(label_dict) - (len(label_dict) - len(string_data))
            for defunctLabel in range(unused_label_count + 1, len(label_dict) + 1, 1):
                target_label = label_dict[defunctLabel]
                target_label.setText("")

    def toggle_entire_ledger(self, toggle: bool):
        self.ui.DateEditTransDate.setEnabled(toggle)
        self.ui.lEditTransDesc.setEnabled(toggle)
        self.ui.comboBCategory.setEnabled(toggle)
        self.ui.pBCatModify.setEnabled(toggle)
        self.ui.lEditDebit.setEnabled(toggle)
        self.ui.lEditCredit.setEnabled(toggle)
        self.ui.lEditSharePrice.setEnabled(toggle)
        self.ui.lEditSharePurch.setEnabled(toggle)
        self.ui.lEditShareSold.setEnabled(toggle)
        self.ui.textEditAddNotes.setEnabled(toggle)
        self.ui.rBPosted.setEnabled(toggle)
        self.ui.rBPending.setEnabled(toggle)
        self.ui.pBUpload.setEnabled(toggle)
        self.ui.pBDisplay.setEnabled(toggle)
        self.ui.pBClear.setEnabled(toggle)
        self.ui.pBDeleteReceipt.setEnabled(toggle)
        self.ui.comboBLedger2.setEnabled(toggle)
        self.ui.comboBPeriod.setEnabled(toggle)
        self.ui.pBAddTransaction.setEnabled(toggle)
        self.ui.pBSelect.setEnabled(toggle)
        self.ui.pBUpdate.setEnabled(toggle)
        self.ui.pBDelete.setEnabled(toggle)
        self.ui.pBClearInputs.setEnabled(toggle)
        self.ui.pBUStockPrice.setEnabled(toggle)
        self.ui.tabWidgetLedger2.setEnabled(toggle)

    # Pyside6 signals to refresh the QMainWindow Labels for NetWorth
    def trigger_refresh(self):
        self.refresh_signal_L2.emit("1")

    def trigger_del_tab(self):
        self.remove_tab_L2.emit(self.parentType)

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")