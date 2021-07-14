"""
This script is the backend to Frontend.Ledger1Ui.py

Future Concepts


Warning: While many bad practices have been fixed between the Alpha program and the Release build. Some Artifacts may survive; such as
the center and right display frames were previously referred to as variable1 [interestRate] and variable2 [variable1]. Refer to the Ui file
to clarify function/purpose of any given object.
"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import pandas as pd
import time

from PySide2.QtWidgets import QMessageBox, QDialog, QFileDialog, QInputDialog
from PySide2.QtCore import QDate
from PySide2.QtGui import QPixmap
from PySide2 import QtCore, QtWidgets, QtGui

from pathlib import Path, PurePath
from shutil import copy

from Backend.AccountDetails import AccountsDetails
from Backend.DataFrame import load_df_ledger, update_df_ledger, update_df_balance
from Backend.LedgerDataAnalysis import category_spending_data, category_spending_by_interval
from Backend.SpendingCategories import SpendingCategories
from Backend.ToggleCategories import Toggle_Categories
from Backend.ReceiptViewer import Receipt

from Frontend.Ledger1Ui import Ui_Ledger1

from Toolbox.AF_Tools import disp_LedgerV1_Table, fill_widget, find_mult_row, fill_statement_period, rename_image, set_font
from Toolbox.Error_Tools import check_characters, check_numerical_inputs
from Toolbox.Formatting_Tools import add_comma, decimal_places, remove_comma, remove_space
from Toolbox.SQL_Tools import obtain_sql_value, specific_sql_statement, sqlite3_keyword_check
from Toolbox.OS_Tools import file_destination

from StyleSheets.StandardCSS import standardAppearance
from StyleSheets.LedgerCSS import transFrame, spendingLabel


class LedgerV1(QDialog):
    refresh_signal = QtCore.Signal(str)
    remove_tab = QtCore.Signal(str)

    def __init__(self, database, parentType, user, ledger_container, error_log):
        super().__init__()
        self.ui = Ui_Ledger1(parentType)
        self.ui.setupUi(self)
        self.setWindowTitle(parentType)
        self.show()

        # Class Global Variables
        self.refUserDB = database
        self.parentType = parentType
        self.refUser = user
        self.ledgerContainer = ledger_container
        self.error_Logger = error_log

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

        self.statement_label_dict = {}
        self.year_label_dict = {}
        self.overall_label_dict = {}

        # Prepare Widgets for initial Use
        self.comboBoxAccountStatement = f"SELECT ID FROM Account_Summary WHERE ParentType= '{self.parentType}'"
        fill_widget(self.ui.comboBLedger1, self.comboBoxAccountStatement, True, self.refUserDB, self.error_Logger)

        self.active_account = self.ui.comboBLedger1.currentText()
        self.activeLedger = load_df_ledger(self.ledgerContainer, self.active_account)
        self.activeLedger = self.activeLedger.sort_values(by=['Transaction_Date', 'Update_Date'], ascending=True)

        self.comboBoxCategoriesStatement = f"SELECT Method FROM Categories WHERE ParentType= '{self.parentType}'"
        fill_widget(self.ui.comboBCategory, self.comboBoxCategoriesStatement, True, self.refUserDB, self.error_Logger)

        if self.ui.comboBLedger1.currentText() == "":
            self.toggle_entire_ledger(False)
        else:
            self.toggle_entire_ledger(True)

        # Prepare Spending By Category Data Representation.
        if self.parentType != "Property" and self.ui.comboBLedger1.currentText() != "":
            fill_statement_period(self.active_account, self.ui.comboBPeriod, "Active", self.refUserDB, self.activeLedger, self.error_Logger)
            sql_account = remove_space(self.ui.comboBLedger1.currentText())
            years, *_ = category_spending_data(self.refUserDB, sql_account, self.activeLedger, self.error_Logger)
            self.ui.comboBTab2Year.addItems(years)
            self.ui.comboBTab2Year.currentIndexChanged.connect(lambda: self.update_spending_tab("Year"))

            self.update_spending_tab("Statement")
            self.update_spending_tab("Year")
            self.update_spending_tab("Overall")

        if self.parentType != "Property":
            self.ui.pBToggle.clicked.connect(self.toggle_dialog)
            self.ui.comboBLedger1.currentIndexChanged.connect(self.change_ledger1_account)
            self.ui.comboBPeriod.currentIndexChanged.connect(self.display_ledger_1)
        else:
            self.ui.comboBLedger1.currentIndexChanged.connect(self.change_ledger1_account)

        self.ui.DateEditTransDate.setDate(QDate.currentDate())
        self.ui.rBPending.setChecked(True)

        self.ui.pBModAccount.clicked.connect(self.accounts_dialog)
        self.ui.pBCatModify.clicked.connect(self.categories_dialog)

        self.ui.pBAddTransaction.clicked.connect(self.add_transaction)
        self.ui.pBSelect.clicked.connect(self.select_transaction)
        self.ui.pBUpdate.clicked.connect(self.update_transaction)
        self.ui.pBDelete.clicked.connect(self.delete_transaction)
        self.ui.pBClearInputs.clicked.connect(self.clear_inputs)

        self.ui.pBUpload.clicked.connect(self.upload_receipt_button)
        self.ui.pBDisplay.clicked.connect(self.display_receipt)
        self.ui.pBClear.clicked.connect(self.clear_receipt_action)
        self.ui.pBDeleteReceipt.clicked.connect(self.delete_receipt_action)

        if self.parentType == "Property":
            self.ui.comboBPeriod.setHidden(True)
            image_result = self.display_house_image()
            if image_result is True:
                self.ui.pBUploadHouse.setEnabled(False)
                self.ui.pBDeleteHouse.setEnabled(True)
            self.ui.pBUploadHouse.clicked.connect(self.upload_house_button)
            self.ui.pBDeleteHouse.clicked.connect(self.delete_house_action)

        self.display_ledger_1()

        self.initialMoneyList = self.net_ledger_value()
        self.ui.lAccountBalance.setText(self.initialMoneyList[1])
        if self.ui.comboBLedger1.currentText() != "":
            self.set_variable1B()  # self.ui.lInterestRate
            self.set_variable2B()  # self.ui.lVariable1

        self.setStyleSheet(standardAppearance)
        self.ui.lInputFrame.setStyleSheet(transFrame)
        self.ui.rInputFrame.setStyleSheet(transFrame)
        self.ui.leftDisplayFrame.setStyleSheet(transFrame)
        self.ui.centerDisplayFrame.setStyleSheet(transFrame)
        self.ui.rightDisplayFrame.setStyleSheet(transFrame)
        self.ui.ledgerFrame.setStyleSheet(transFrame)
        self.set_ledger1_appearance()

    # Opens Modal Dialogs for ledger Modification
    def accounts_dialog(self):
        alf = AccountsDetails(self.refUserDB, self.parentType, self.refUser, self.error_Logger)
        if alf.exec_() == QDialog.Accepted:
            self.ui.comboBLedger1.clear()
            self.ui.comboBPeriod.clear()
            if self.parentType != "Property":
                self.ui.comboBTab2Year.clear()

            self.comboBoxAccountStatement = f"SELECT ID FROM Account_Summary WHERE ParentType= '{self.parentType}'"
            fill_widget(self.ui.comboBLedger1, self.comboBoxAccountStatement, True, self.refUserDB, self.error_Logger)

            if self.ui.comboBLedger1.currentText() != "" and self.parentType != "Property":
                self.active_account = self.ui.comboBLedger1.currentText()
                self.activeLedger = load_df_ledger(self.ledgerContainer, self.active_account)

                fill_statement_period(self.active_account, self.ui.comboBPeriod, "Active", self.refUserDB, self.activeLedger, self.error_Logger)
                self.toggle_entire_ledger(True)

            elif self.ui.comboBLedger1.currentText() == "":
                  self.toggle_entire_ledger(False)

            self.ui.comboBLedger1.setCurrentIndex(0)
            self.set_variable1B()
            self.set_variable2B()
            self.trigger_refresh()

    # Opens Modal Dialog for Spending Category Modifications
    def categories_dialog(self):
        molly = SpendingCategories(self.refUserDB, self.parentType, self.error_Logger)
        if molly.exec_() == QDialog.Accepted:
            self.ui.comboBCategory.clear()
            self.comboBoxCategoriesStatement = f"SELECT Method FROM Categories WHERE ParentType= '{self.parentType}'"
            fill_widget(self.ui.comboBCategory, self.comboBoxCategoriesStatement, True, self.refUserDB, self.error_Logger)

    # Opens Modal Dialog for Modifying which Spending Categories are used in the Graphical Calculations
    def toggle_dialog(self):
        boston = Toggle_Categories(self.refUserDB, self.parentType, self.error_Logger)
        if boston.exec_() == QDialog.Accepted:
            self.update_spending_tab("Statement")
            self.update_spending_tab("Year")
            self.update_spending_tab("Overall")

    # General Functions
    def check_transactions(self):
        detail_inputs = [[self.ui.lEditTransMethod.text(), "general"],
                         [self.ui.lEditTransDesc.text(), "general"],
                         [self.ui.lEditDebit.text(), "general"],
                         [self.ui.lEditCredit.text(), "general"],
                         [self.ui.textEditAddNotes.toPlainText(), "general"]]

        for value in detail_inputs:
            if not check_characters(value[0], value[1]):
                return False

            if sqlite3_keyword_check(value[0]):
                return False

        if self.ui.lEditTransDesc.text() == "" or self.ui.lEditTransDesc.text() == " ":
            return False  # Transaction description is only user input that is required (Cat and Date are technically unavoidable)

        if len(self.ui.textEditAddNotes.toPlainText()) > 150:
            return False  # Restricts the length of the Note input

        # The following three conditions are valid variants on the Debit and Credit Inputs
        # Debit appears before Credit on the screen so it is checked first for a value
        elif self.ui.lEditDebit.text() == "" and self.ui.lEditCredit.text() == "":
            return True    # Debit and Credit are blank
        elif check_numerical_inputs(self.ui.lEditDebit.text()) is True and self.ui.lEditCredit.text() == "":
            return True     # Debit is Numerical and Credit is Blank
        elif self.ui.lEditDebit.text() == "" and check_numerical_inputs(self.ui.lEditCredit.text()):
            return True    # Debit is Blank and Credit is Numerical
        else:
            # Catches Debit or Credit = " " or having a non numerical input
            return False

    def clear_inputs(self):
        self.ui.DateEditTransDate.setDate(QDate.currentDate())
        self.ui.lEditTransDesc.setText("")
        self.ui.lEditTransMethod.setText("")
        self.ui.comboBCategory.setCurrentIndex(0)
        self.ui.lEditDebit.setText("")
        self.ui.lEditCredit.setText("")
        self.ui.textEditAddNotes.setPlainText("")
        self.ui.rBPending.setChecked(True)
        self.clear_receipt_action()
        self.ui.DateEditTransDate.setFocus()

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

    def set_ledger1_appearance(self):
        if self.parentType == "Bank":
            self.ui.rightDisplayFrame.setHidden(True)
            self.ui.lStaticVariable1.setHidden(True)
            self.ui.lVariable1.hide()
        elif self.parentType == "CD" or self.parentType == "Treasury":
            pass
        elif self.parentType == "Credit":
            self.ui.rightDisplayFrame.setHidden(True)
            self.ui.lStaticVariable1.setHidden(True)
            self.ui.lVariable1.setHidden(True)
            self.ui.lStaticInterestRate.setText("Credit Limit:")
        elif self.parentType == "Debt":
            self.ui.lStaticVariable1.setText(" Starting Balance:")
        else:  # Cash and Property
            self.ui.centerDisplayFrame.setHidden(True)
            self.ui.rightDisplayFrame.setHidden(True)

    def user_selection_input(self, tableWidget, text1, text2):
        row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
        if ok and row:
            return row
        else:
            row = 0
            return row

    # Functions that depend on SQLite3
    def add_transaction(self):
        tic = time.perf_counter()
        if self.ui.comboBLedger1.currentText() == "":
            noLedger_msg = "Create a new Ledger"
            self.input_error_msg(noLedger_msg)
        else:
            if self.check_transactions():
                from datetime import datetime
                modDebit = decimal_places(self.ui.lEditDebit.text(), 2)
                modCredit = decimal_places(self.ui.lEditCredit.text(), 2)

                status = self.transaction_status(self.ui.rBPending, self.ui.rBPosted)
                currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                transaction_df = pd.DataFrame({'Transaction_Date': [self.ui.DateEditTransDate.date().toString("yyyy/MM/dd")],
                                               'Transaction_Method': [self.ui.lEditTransMethod.text()],
                                               'Transaction_Description': [self.ui.lEditTransDesc.text()],
                                               'Category': [self.ui.comboBCategory.currentText()],
                                               'Debit': [str(modDebit)],
                                               'Credit': [str(modCredit)],
                                               'Balance': ['0.00'],
                                               'Note': [self.ui.textEditAddNotes.toPlainText()],
                                               'Status': [status],
                                               'Receipt': [self.ui.lEditReceipt.text()],
                                               'Post_Date': [currentDate],
                                               'Update_Date': [currentDate]})
                self.activeLedger = self.activeLedger.append(transaction_df, ignore_index=True)
                self.activeLedger = self.activeLedger.sort_values(by=['Transaction_Date', 'Update_Date'], ascending=True)
                self.activeLedger = update_df_balance(self.activeLedger)

                self.transaction_refresh()
                toc = time.perf_counter()
                print(f'Full Transaction took {toc - tic:0.4f} seconds')
            else:
                input_error = """
                    Transaction Input Instructions:

                1  :  Ensure these fields are completed
                [T Date, T Description, Category, and Status]
                2  :  Alphanumeric inputs only
                3  :  Check the character length of your
                      additional notes input

                """
                self.input_error_msg(input_error)

    def delete_transaction(self):
        inputText1 = "Delete Transaction"
        inputText2 = "Enter Row #: "
        row = self.user_selection_input(self.ui.tableWLedger1, inputText1, inputText2) - 1
        deleteMessage = "Selecting 'OK' will permanently remove " + \
                        "\nrow #: " + str(row + 1) + " from the ledger"
        confirm = QMessageBox.warning(self, 'Confirm', deleteMessage, QMessageBox.Ok, QMessageBox.Cancel)
        if confirm == QMessageBox.Ok:
            target_transaction = self.activeLedger[(self.activeLedger['Post_Date'] == self.ui.tableWLedger1.item(row, 9).text()) &
                                                   (self.activeLedger['Transaction_Description'] == self.ui.tableWLedger1.item(row, 2).text())].index
            self.activeLedger = self.activeLedger.drop(target_transaction, inplace=False)
            self.activeLedger = self.activeLedger.reset_index(drop=True)

            update_df_balance(self.activeLedger)
            self.transaction_refresh()
        else:
            pass

    def change_ledger1_account(self):
        update_df_ledger(self.ledgerContainer, self.active_account, self.error_Logger, self.activeLedger, action="Update")

        if self.ui.comboBLedger1.currentText() is None:
            self.toggle_entire_ledger(False)
            self.active_account = None
            self.activeLedger = None
        elif self.ui.comboBLedger1.currentText() == "":
            self.toggle_entire_ledger(False)
            self.active_account = None
            self.activeLedger = None
        else:
            self.toggle_entire_ledger(True)
            self.active_account = self.ui.comboBLedger1.currentText()
            self.activeLedger = load_df_ledger(self.ledgerContainer, self.active_account)
            self.activeLedger = self.activeLedger.sort_values(by=['Transaction_Date', 'Update_Date'], ascending=True)

            if self.parentType != "Property":
                self.ui.comboBTab2Year.clear()
                fill_statement_period(self.active_account, self.ui.comboBPeriod, "Active", self.refUserDB, self.activeLedger, self.error_Logger)
                sql_account = remove_space(self.active_account)
                years, *_ = category_spending_data(self.refUserDB, sql_account, self.activeLedger, self.error_Logger)
                self.ui.comboBTab2Year.addItems(years)
                self.set_variable1B()
                self.set_variable2B()
                # Spending_tabs should auto update due to change in the combobox due to new account
                self.update_spending_tab("Statement")
                self.update_spending_tab("Year")
                self.update_spending_tab("Overall")
                self.display_ledger_1()
            else:
                self.set_variable1B()
                self.set_variable2B()
                self.display_ledger_1()

    def display_ledger_1(self):
        ledger = self.active_account
        statement = self.ui.comboBPeriod.currentText()
        if ledger is None or statement == "":

            self.ui.tableWLedger1.clearContents()
            self.ui.lAccountBalance.setText("$ 0.00")
            if self.parentType != "Property":
                self.ui.lStatementGraph.setText("Spending During TBD")

            for dictionary in [self.statement_label_dict, self.year_label_dict, self.overall_label_dict]:
                for key in dictionary:
                    label = dictionary[key]
                    label.setText("")

        else:
            if self.parentType in ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit", "Property"]:
                disp_LedgerV1_Table(self.ui.comboBLedger1, self.ui.comboBPeriod, self.parentType, self.ui.tableWLedger1, self.activeLedger)
                self.initialMoneyList = self.net_ledger_value()
                self.ui.lAccountBalance.setText(self.initialMoneyList[1])
            else:
                error = "Parent Type doesn't belong with this ledger"
                self.input_error_msg(error)

        if self.parentType != "Property":
            self.ui.lStatementGraph.setText(f"Spending During {self.ui.comboBPeriod.currentText()}")
            self.update_spending_tab("Statement")

    def transaction_refresh(self):
        # Refreshes the tableWidget to display the most recent statement period. May be considered annoying if working on an old statement.
        self.change_ledger1_account()

        # Changes the Account Balance to reflect the "posted" balance
        ledgerValue = self.net_ledger_value()
        self.ui.lAccountBalance.setText(ledgerValue[1])

        # Updates the database Account_Summary to reflect the "posted" balance
        balanceStatement = f"UPDATE Account_Summary SET Balance='{ledgerValue[0]}' WHERE ID='{self.ui.comboBLedger1.currentText()}'"
        specific_sql_statement(balanceStatement, self.refUserDB, self.error_Logger)

        # Clears Inputs to allow for a new transaction
        self.clear_inputs()

        # Triggers to refresh the other variables on the QMainWindow and subsequently the Summary window (if open)
        self.trigger_refresh()

    def select_transaction(self):
        self.clear_inputs()
        inputText1 = "Select Row"
        inputText2 = "Enter Row #: "
        row = self.user_selection_input(self.ui.tableWLedger1, inputText1, inputText2) - 1
        if row == -1:
            self.clear_inputs()
        else:
            for col in range(0, 10):
                widget = col + 2
                dataPoint = self.ui.tableWLedger1.item(row, col).text()
                if widget == 2:
                    # col 0 = TDate
                    self.ui.DateEditTransDate.setDate(QtCore.QDate.fromString(dataPoint, "MM/dd/yyyy"))
                elif widget == 3:
                    # col 1 = TM
                    self.ui.lEditTransMethod.setText(dataPoint)
                elif widget == 4:
                    # col 2 = TD
                    self.ui.lEditTransDesc.setText(dataPoint)
                elif widget == 5:
                    # col 3 = Category
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
                elif widget == 6:
                    # col 4 = Amount
                    dataPoint = dataPoint[4:]
                    if dataPoint == "":
                        self.ui.lEditDebit.setText(dataPoint)
                    elif dataPoint == " -  ":
                        self.ui.lEditDebit.setText("0")
                    elif dataPoint[len(dataPoint) - 1:] == ")":
                        dataPoint = dataPoint[1:]
                        dataPoint = dataPoint[:len(dataPoint) - 1]
                        displayValue = remove_comma(dataPoint)
                        self.ui.lEditDebit.setText(displayValue)
                    elif dataPoint[len(dataPoint) - 1:] == " ":
                        dataPoint = dataPoint[:len(dataPoint) - 1]
                        displayValue = remove_comma(dataPoint)
                        self.ui.lEditCredit.setText(displayValue)
                elif widget == 7:
                    pass
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

    def update_dataFrame(self, row):
        from datetime import datetime
        tic = time.perf_counter()
        status = self.transaction_status(self.ui.rBPending, self.ui.rBPosted)
        modDebit = str(decimal_places(self.ui.lEditDebit.text(), 2))
        modCredit = str(decimal_places(self.ui.lEditCredit.text(), 2))
        currentDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        column_headers = ["Transaction_Date",
                          'Transaction_Method',
                          'Transaction_Description',
                          'Category',
                          'Debit',
                          'Credit',
                          'Note',
                          'Status',
                          'Receipt',
                          'Update_Date']

        new_transaction = [self.ui.DateEditTransDate.date().toString("yyyy/MM/dd"),
                           self.ui.lEditTransMethod.text(),
                           self.ui.lEditTransDesc.text(),
                           self.ui.comboBCategory.currentText(),
                           modDebit,
                           modCredit,
                           self.ui.textEditAddNotes.toPlainText(),
                           status,
                           self.ui.lEditReceipt.text(),
                           currentDate]

        target_transaction = self.activeLedger[self.activeLedger['Post_Date'] == self.ui.tableWLedger1.item(row, 9).text()].index
        self.activeLedger.at[target_transaction, column_headers] = new_transaction

        subtoc = time.perf_counter()
        # update_ledger_balance(self.ui.comboBLedger1, self.refUserDB, self.error_Logger)
        update_df_balance(self.activeLedger)
        toc = time.perf_counter()
        print(f'Update ledger took {subtoc - tic:0.4f} seconds')
        print(f'Full Transaction took {subtoc - toc:0.4f} seconds')

    def update_transaction(self):
        inputText1 = "Update Transaction"
        inputText2 = "Enter Row #: "
        if self.check_transactions():
            row = self.user_selection_input(self.ui.tableWLedger1, inputText1, inputText2) - 1
            if row == -1:
                self.clear_inputs()
            else:
                updateMessage = "Selecting 'OK' will update target row #: " + str(row + 1) + \
                                "\nto the current input values designated"
                reply = QMessageBox.warning(self, 'Verify', updateMessage, QMessageBox.Ok, QMessageBox.Cancel)
                if reply == QMessageBox.Ok:
                    self.update_dataFrame(row)
                    self.transaction_refresh()

                else:
                    pass
        else:
            input_error = """
                Transaction Input Instructions:

            1  :  Ensure these fields are completed
            [T Date, T Description, Category, and Status]
            2  :  Alphanumeric inputs only
            3  :  Check the character length of your
                  additional notes input

            """
            self.input_error_msg(input_error)

    # Functions Associated with the Ledger Display Frames and the variable values/displays
    def net_ledger_value(self):
        ledgerName = self.ui.comboBLedger1.currentText()

        if ledgerName == "":
            netValue = ["0.00", "0.00"]
            return netValue
        else:
            posted_df = self.activeLedger[['Credit', 'Debit']][self.activeLedger['Status'] == 'Posted'].copy()
            total_credit = pd.to_numeric(posted_df['Credit'], errors='coerce').sum()
            total_debit = pd.to_numeric(posted_df['Debit'], errors='coerce').sum()
            qtyMoney = total_credit - total_debit

            if qtyMoney is None:
                moneyWOComma = "0.00"
                formatString = "$ 0.00"
                moneylist = [moneyWOComma, formatString]
                return moneylist
            elif qtyMoney < 0:
                rounded_qtyMoney = round(qtyMoney, 2)
                moneyWComma = add_comma(rounded_qtyMoney, 2)
                moneyWOComma = "-" + remove_comma(moneyWComma)
                formatString = "($ " + moneyWComma + ")"
                moneylist = [moneyWOComma, formatString]
                return moneylist
            else:
                rounded_qtyMoney = round(qtyMoney, 2)
                moneyWComnma = add_comma(rounded_qtyMoney, 2)
                moneyWOComma = remove_comma(moneyWComnma)
                formatString = "$ " + moneyWComnma
                moneylist = [moneyWOComma, formatString]
                return moneylist

    # In Alpha the LStaticInterestRate was set are variable 1. I changed the variable but not the function name.
    def set_variable1B(self):
        detailsTable = self.parentType_dict[self.parentType]
        setInterest = ["Bank", "CD", "Treasury", "Debt"]
        setCreditLimit = ["Credit"]
        if self.parentType in setInterest:
            interestStatement = f"SELECT Interest_Rate FROM {detailsTable} WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
            interest = obtain_sql_value(interestStatement, self.refUserDB, self.error_Logger)
            if interest is None:
                interest = "Unknown"
            else:
                interest = str(decimal_places(interest[0], 2))
                interest = interest + "%"
            self.ui.lInterestRate.setText(interest)
        elif self.parentType in setCreditLimit:
            limitStatement = f"SELECT Credit_Limit FROM {detailsTable} WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
            limit = obtain_sql_value(limitStatement, self.refUserDB, self.error_Logger)
            if limit is None:
                limit = [0.00]
            limit = add_comma(limit[0], 2)
            limit = "$ " + limit
            self.ui.lInterestRate.setText(limit)
        else:
            pass

    def set_variable2B(self):
        detailsTable = self.parentType_dict[self.parentType]
        setMaturity = ["CD", "Treasury"]
        setStart = ["Debt"]
        if self.parentType in setMaturity:
            maturityStatement = f"SELECT Maturity_Date FROM {detailsTable} WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
            maturity = obtain_sql_value(maturityStatement, self.refUserDB, self.error_Logger)
            if maturity is None:
                maturity = ["Unknown"]
            else:
                maturity = str(maturity[0])
            self.ui.lVariable1.setText(maturity)
        elif self.parentType in setStart:
            startStatement = f"SELECT Starting_Balance FROM {detailsTable} WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
            startingBalance = obtain_sql_value(startStatement, self.refUserDB, self.error_Logger)
            if startingBalance is None:
                startingBalance = [0]
            sBalance = add_comma(startingBalance[0], 2)
            sBalance = "$ " + sBalance
            self.ui.lVariable1.setText(sBalance)
        else:
            pass

    # Functions focused on Spending Catagory Calculations
    def build_tabWidget_display(self, target_tab):
        label_font = QtGui.QFont()
        set_font(label_font, 12, True, False)

        tab_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        if target_tab == 'Year' and self.ui.comboBTab2Year.currentText() == "":
            pass
        else:
            account = remove_space(self.ui.comboBLedger1.currentText())
            spending_statement_data, spending_statement_string, _ = category_spending_by_interval(self.refUserDB, account, self.activeLedger, target_tab, self.ui.comboBPeriod.currentText(), self.error_Logger)

            if target_tab == "Statement":
                label_dict = self.statement_label_dict
                tabLayout = self.ui.statementScrollLayout
            elif target_tab == "Year":
                label_dict = self.year_label_dict
                tabLayout = self.ui.yearScrollLayout
            elif target_tab == "Overall":
                label_dict = self.overall_label_dict
                tabLayout = self.ui.overallScrollLayout
            else:
                return

            for count, value in enumerate(spending_statement_data, start=1):
                self.spendingLabel = QtWidgets.QLabel()
                self.spendingLabel.setObjectName(f"lspending{target_tab}Type{count}")
                self.spendingLabel.setText(spending_statement_string[value[0]])
                self.spendingLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                # self.spendingLabel.setFixedHeight(40)
                self.spendingLabel.setFont(label_font)
                self.spendingLabel.setStyleSheet(spendingLabel)
                self.spendingLabel.setSizePolicy(tab_sizePolicy)
                label_dict[count] = self.spendingLabel

                tabLayout.addWidget(self.spendingLabel)

    def update_spending_tab(self, target_tab):
        label_font = QtGui.QFont()
        set_font(label_font, 12, True, False)

        tab_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        if target_tab == "Statement":
            label_dict = self.statement_label_dict
            tabLayout = self.ui.statementScrollLayout
        elif target_tab == "Year":
            label_dict = self.year_label_dict
            tabLayout = self.ui.yearScrollLayout
        elif target_tab == "Overall":
            label_dict = self.overall_label_dict
            tabLayout = self.ui.overallScrollLayout
        else:
            return

        account = remove_space(self.ui.comboBLedger1.currentText())

        # spending_Statement_data will be used for the graph

        if target_tab == 'Year' and self.ui.comboBTab2Year.currentText() == "":
            pass
        elif target_tab == "Statement" and self.ui.comboBPeriod.currentText() == "":
            pass
        elif target_tab == "Overall" and self.ui.comboBTab2Year.currentText() == "":
            pass
        else:
            if target_tab == 'Year' and self.ui.comboBTab2Year.currentText() != "":
                spending_statement_data, spending_statement_string, _ = category_spending_by_interval(self.refUserDB, account, self.activeLedger, target_tab, self.ui.comboBTab2Year.currentText(), self.error_Logger)
            elif target_tab == "Statement" and self.ui.comboBPeriod.currentText() != "":
                spending_statement_data, spending_statement_string, _ = category_spending_by_interval(self.refUserDB, account, self.activeLedger, target_tab, self.ui.comboBPeriod.currentText(), self.error_Logger)
            else:  # Overall
                spending_statement_data, spending_statement_string, _ = category_spending_by_interval(self.refUserDB, account, self.activeLedger, target_tab, self.ui.comboBTab2Year.currentText(), self.error_Logger)

            for count, value in enumerate(spending_statement_data, start=1):
                try:
                    target_label = label_dict[count]
                    target_label.setText(spending_statement_string[value[0]])
                except KeyError:
                    self.spendingLabel = QtWidgets.QLabel()
                    self.spendingLabel.setObjectName(f"lspending{target_tab}Type{count}")
                    self.spendingLabel.setText(spending_statement_string[value[0]])
                    self.spendingLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                    self.spendingLabel.setFont(label_font)
                    self.spendingLabel.setStyleSheet(spendingLabel)
                    self.spendingLabel.setSizePolicy(tab_sizePolicy)
                    label_dict[count] = self.spendingLabel

                    tabLayout.addWidget(self.spendingLabel)

            if len(label_dict) > len(spending_statement_data):
                unused_label_count = len(label_dict) - (len(label_dict) - len(spending_statement_string))
                for defunctLabel in range(unused_label_count + 1, len(label_dict) + 1, 1):
                    target_label = label_dict[defunctLabel]
                    target_label.setText("")

    # Functions focused around the Receipt/Invoice inputs
    def clear_receipt_action(self):
        if self.ui.lEditReceipt.text() == "":
            pass
        else:
            oRName = self.ui.lEditReceipt.text()
            self.ui.lEditReceipt.setText("")
            rowList = self.activeLedger.loc[self.activeLedger['Receipt'] == oRName]
            # if no rows are found with the file. The image is just deleted
            if rowList.shape[0] == 0:
                self.ui.lEditReceipt.setText("")
                modifiedLN = remove_space(self.ui.comboBLedger1.currentText())
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
            row = find_mult_row(self.ui.tableWLedger1, 7, self.ui.lEditReceipt.text())
            if len(row) == 0:
                self.clear_receipt_action()
            elif len(row) >= 1:
                target_row = self.select_transaction()
                self.clear_receipt_action()
                self.update_dataFrame(target_row)
            else:
                self.clear_receipt_action()

    def display_receipt(self):
        ledger = self.ui.comboBLedger1.currentText()
        modifiedLN = remove_space(ledger)
        fileName = self.ui.lEditReceipt.text()
        suffix = PurePath(fileName).suffix

        receipt_path = file_destination(['Receipts', self.refUser, self.parentType, modifiedLN])
        receipt_path = Path.cwd() / receipt_path / fileName

        if fileName == "":
            noReceipt = "Sorry, No Receipt Uploaded"
            self.input_error_msg(noReceipt)
        elif suffix == ".pdf":
            try:
                os.startfile(receipt_path)
            except FileNotFoundError:
                noFileMessage = f"{fileName} was not located.\n\nDelete Receipt and Re-Upload if necessary."
                self.input_error_msg(noFileMessage)
        else:
            if os.path.isfile(receipt_path):
                ion = Receipt(str(receipt_path), fileName)
                if ion.exec_() == QDialog.Accepted:
                    pass
            else:
                noFileMessage = f"{fileName} was not located.\n\nDelete Receipt and Re-Upload if necessary."
                self.input_error_msg(noFileMessage)

    def receipt_check_on_close(self):
        if self.ui.lEditReceipt.text() != "":
            self.clear_receipt_action()

    def upload_receipt_action(self):
        suffixlist = ['.jpg', '.jpeg', 'JPEG', '.gif', '.pdf', '.png']
        # rname = Receipt [File] Name
        rname, _ = QFileDialog.getOpenFileName(self, 'Target Receipt', '/home',
                                               'Images (*.png *.jpg  *.jpeg *.gif);; PDF (*.pdf *.PDF)')
        if rname:
            rname_path = Path(rname)
            suffix = PurePath(rname_path).suffix
            if suffix not in suffixlist:
                wrongType = "Sorry, those files types are not support yet."
                self.input_error_msg(wrongType)
            else:
                nRName = rename_image(self.ui.comboBLedger1, self.ui.comboBCategory) + str(suffix)
                modifiedLN = remove_space(self.ui.comboBLedger1.currentText())
                nRName_path = file_destination(['Receipts', self.refUser, self.parentType, modifiedLN])
                nRName_path = Path.cwd() / nRName_path / nRName
                copy(rname_path, nRName_path)
                self.ui.lEditReceipt.setText(nRName)
        else:
            self.ui.lEditReceipt.setText("")

    def upload_receipt_button(self):
        if self.ui.comboBLedger1.currentText() == "":
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

    # Functions focused on Property House Images
    def delete_house_action(self):
        house_Image_statement = f"SELECT Image FROM Property_Account_Details WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
        house_Image_location_raw = obtain_sql_value(house_Image_statement, self.refUserDB, self.error_Logger)
        house_Image_location = house_Image_location_raw[0]

        modifiedLN = remove_space(self.ui.comboBLedger1.currentText())
        currentPIname_path = file_destination(['Images', self.refUser, self.parentType, modifiedLN])
        currentPIname_path = Path.cwd() / currentPIname_path / house_Image_location
        os.remove(currentPIname_path)

        self.ui.lHouseImage.setText(f"Upload a House Image\n\n Max Dimensions:\n{self.ui.houseFrame.geometry().width()} pixel x {self.ui.houseFrame.geometry().height()} pixel")

        delete_statement = f"UPDATE Property_Account_Details SET Image=NULL WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
        specific_sql_statement(delete_statement, self.refUserDB, self.error_Logger)

        self.ui.pBDeleteHouse.setEnabled(False)
        self.ui.pBUploadHouse.setEnabled(True)

    def display_house_image(self):
        if self.ui.comboBLedger1.currentText() != "":
            house_Image_statement = f"SELECT Image FROM Property_Account_Details WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
            house_Image_location_raw = obtain_sql_value(house_Image_statement, self.refUserDB, self.error_Logger)
            house_Image_location = house_Image_location_raw[0]

            if house_Image_location is None:
                return False
            else:
                modifiedLN = remove_space(self.ui.comboBLedger1.currentText())
                currentPIname_path = file_destination(['Images', self.refUser, self.parentType, modifiedLN])
                currentPIname_path = Path.cwd() / currentPIname_path / house_Image_location
                house_Image = QPixmap(f'{currentPIname_path}')

                self.ui.lHouseImage.setPixmap(house_Image)
                return True
        else:
            return False

    def upload_house_action(self):
        suffixlist = ['.jpg', '.jpeg', 'JPEG', '.gif', '.png']
        # pIname = Property Image Name
        pIname, _ = QFileDialog.getOpenFileName(self, 'Property Image', '/home', 'Images (*.png *.jpg  *.jpeg *.gif)')

        if pIname:
            pIname_path = Path(pIname)
            suffix = PurePath(pIname_path).suffix
            if suffix not in suffixlist:
                wrongType = "Sorry, those file types are not support yet."
                self.input_error_msg(wrongType)
            else:
                nPIname = rename_image(self.ui.comboBLedger1, self.ui.comboBCategory) + str(suffix)
                modifiedLN = remove_space(self.ui.comboBLedger1.currentText())
                nPIName_path = file_destination(['Images', self.refUser, self.parentType, modifiedLN])
                nPIName_path = Path.cwd() / nPIName_path / nPIname
                copy(pIname_path, nPIName_path)

                house_image_statement = f"UPDATE Property_Account_Details SET Image='{nPIname}' WHERE Account_Name='{self.ui.comboBLedger1.currentText()}'"
                specific_sql_statement(house_image_statement, self.refUserDB, self.error_Logger)

                self.display_house_image()

                self.ui.pBUploadHouse.setEnabled(False)
                self.ui.pBDeleteHouse.setEnabled(True)

        else:
            pass

    def upload_house_button(self):
        if self.ui.comboBLedger1.currentText() == "":
            noLedger_msg = "Create a New Ledger"
            self.input_error_msg(noLedger_msg)
        else:
            self.upload_house_action()

    def toggle_entire_ledger(self, toggle: bool):
        self.ui.comboBLedger1.setEnabled(toggle)
        self.ui.DateEditTransDate.setEnabled(toggle)
        self.ui.lEditTransMethod.setEnabled(toggle)
        self.ui.lEditTransDesc.setEnabled(toggle)
        self.ui.comboBCategory.setEnabled(toggle)
        self.ui.pBCatModify.setEnabled(toggle)
        self.ui.lEditDebit.setEnabled(toggle)
        self.ui.lEditCredit.setEnabled(toggle)
        self.ui.textEditAddNotes.setEnabled(toggle)
        self.ui.rBPending.setEnabled(toggle)
        self.ui.rBPosted.setEnabled(toggle)
        self.ui.pBUpload.setEnabled(toggle)
        self.ui.pBDisplay.setEnabled(toggle)
        self.ui.pBClear.setEnabled(toggle)
        self.ui.pBDeleteReceipt.setEnabled(toggle)
        self.ui.comboBPeriod.setEnabled(toggle)
        self.ui.pBAddTransaction.setEnabled(toggle)
        self.ui.pBSelect.setEnabled(toggle)
        self.ui.pBUpdate.setEnabled(toggle)
        self.ui.pBDelete.setEnabled(toggle)
        self.ui.pBClearInputs.setEnabled(toggle)

        if self.parentType == "Property":
            self.ui.pBUploadHouse.setEnabled(toggle)
        else:
            self.ui.tabWidget.setEnabled(toggle)
            self.ui.pBToggle.setEnabled(toggle)
            self.ui.comboBTab2Year.setEnabled(toggle)

    # Pyside6 signals to refresh the QMainWindow Labels for NetWorth
    def trigger_refresh(self):
        self.refresh_signal.emit("1")

    def trigger_del_tab(self):
        self.remove_tab.emit(self.parentType)

    def closeEvent(self, event):
        event.ignore()
        self.receipt_check_on_close()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")