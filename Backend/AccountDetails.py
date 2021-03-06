#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PySide6 import QtCore

from datetime import datetime, timedelta
from Frontend.AccountsUi import Ui_Accounts

from StyleSheets.ErrorCSS import generalError
from StyleSheets.StandardCSS import standardAppearance

from Backend.DataFrame import create_DF, load_df_ledger, update_df_ledger
from Backend.Question import YNTypeQuestion

from Toolbox.AF_Tools import fill_widget
from Toolbox.Error_Tools import check_characters, check_numerical_inputs, find_character, first_character_check
from Toolbox.Formatting_Tools import decimal_places, remove_space
from Toolbox.OS_Tools import file_destination, obtain_storage_dir
from Toolbox.SQL_Tools import move_row_sql_tables, check_for_data, delete_column, obtain_sql_value, execute_sql_statement_list, specific_sql_statement, sqlite3_keyword_check


class AccountsDetails(QDialog):
    save_signal = QtCore.Signal(str)

    def __init__(self, dbName, parentType, user, ledgerContainer, error_Log):
        super().__init__()
        self.ui = Ui_Accounts()
        self.ui.setupUi(self)

        self.storage_dir = obtain_storage_dir()
        self.refUserDB = dbName
        self.parentType = parentType
        self.refUser = user
        self.ledgerContainer = ledgerContainer

        self.parentType_dict = {"Bank": "Bank_Account_Details",
                                "Equity": "Equity_Account_Details",
                                "Retirement": "Retirement_Account_Details",
                                "CD": "CD_Account_Details",
                                "Treasury": "Treasury_Account_Details",
                                "Debt": "Debt_Account_Details",
                                "Credit": "Credit_Account_Details",
                                "Cash": "Cash_Account_Details",
                                "Property": "Property_Account_Details"}

        self.error_Logger = error_Log

        self.accountDetailsTable = self.parentType_dict[parentType]
        self.initial_appearance(self.parentType)
        self.ui.pBNew.clicked.connect(self.new_account)
        self.ui.pBDelete.clicked.connect(self.delete_account)
        self.ui.pBEdit.clicked.connect(self.edit_account)
        self.ui.pBSubmit.clicked.connect(self.submit_account)
        self.ui.pBModify.clicked.connect(self.type_modifier)
        self.ui.pBArchive.clicked.connect(self.archive_account)
        self.ui.pBEditSubmit.clicked.connect(self.submit_edit)

        self.comboboxT_Statement = f"SELECT Subtype FROM AccountSubType WHERE ParentType= '{parentType}'"
        fill_widget(self.ui.comboboxAT, self.comboboxT_Statement, True, self.refUserDB, self.error_Logger)
        self.listWidget_Statement = f"SELECT ID FROM Account_Summary WHERE ParentType= '{parentType}'"
        fill_widget(self.ui.listWidgetAccount, self.listWidget_Statement, True, self.refUserDB, self.error_Logger)
        self.ui.listWidgetAccount.setCurrentRow(0)
        self.disp_current_selection()
        self.ui.listWidgetAccount.itemClicked.connect(self.disp_current_selection)
        self.ui.listWidgetAccount.itemClicked.connect(lambda: self.toggle_widgets(False))
        self.setModal(True)
        self.setStyleSheet(standardAppearance)
        self.show()
        self.initial_appearance(self.parentType)

    def add_account_information(self):
        variant1 = ["Bank", "Credit"]
        variant2 = ["CD", "Treasury", "Debt"]
        variant3 = ["Equity", "Retirement"]
        variant4 = ["Property"]
        accountName = self.ui.lEditAN.text()
        modifiedAN = remove_space(accountName)

        if self.parentType in ["Debt", "Credit"]:
            itemType = "Liability"
        else:
            itemType = "Asset"

        accountSummary = f"INSERT INTO Account_Summary VALUES('{self.ui.lEditAN.text()}', '{itemType}', '{self.parentType}', '{self.ui.comboboxAT.currentText()}', NULL, '0.00')"
        accountLedger = f"CREATE TABLE IF NOT EXISTS {modifiedAN}(Transaction_Date NUMERIC, Transaction_Method TEXT, Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Balance REAL, Note TEXT," \
                        f" Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
        accountWorth = f"ALTER TABLE AccountWorth ADD COLUMN '{modifiedAN}' TEXT"

        today = datetime.now()
        today = datetime.strftime(today, "%Y/%m/%d")
        yesterday = datetime.strptime(today, "%Y/%m/%d") - timedelta(1)
        yesterday = datetime.strftime(yesterday, "%Y/%m/%d")

        accountWorthToday = f"UPDATE AccountWorth SET '{modifiedAN}'=('0.00') WHERE Date='{yesterday}'"
        accountWorthYest = f"UPDATE AccountWorth SET '{modifiedAN}'=('0.00') WHERE Date='{today}'"



        if self.parentType in variant1:
            accountDetails = "INSERT INTO " + self.accountDetailsTable + \
                             " VALUES('" + self.ui.lEditAN.text() + \
                             "', '" + self.ui.comboboxAT.currentText() + \
                             "', '" + self.ui.lEditPO.text() + \
                             "', '" + self.ui.lEditB.text() + \
                             "', '" + str(self.ui.spinBStatement.value()) + \
                             "', '" + self.ui.lEditV1.text() + "')"

        elif self.parentType in variant2:
            accountDetails = "INSERT INTO " + self.accountDetailsTable + \
                             " VALUES('" + self.ui.lEditAN.text() + \
                             "', '" + self.ui.comboboxAT.currentText() + \
                             "', '" + self.ui.lEditPO.text() + \
                             "', '" + self.ui.lEditB.text() + \
                             "', '" + str(self.ui.spinBStatement.value()) + \
                             "', '" + self.ui.lEditV1.text() + \
                             "', '" + self.ui.lEditV2.text() + "')"

        elif self.parentType in variant3:
            tickerPrice = self.ui.lEditV2.text()
            tickerPrice = str(decimal_places(tickerPrice, 4))
            accountDetails = "INSERT INTO " + self.accountDetailsTable + \
                             " VALUES('" + self.ui.lEditAN.text() + \
                             "', '" + self.ui.comboboxAT.currentText() + \
                             "', '" + self.ui.lEditPO.text() + \
                             "', '" + self.ui.lEditB.text() + \
                             "', '" + str(self.ui.spinBStatement.value()) + \
                             "', '" + self.ui.lEditV1.text().upper() + \
                             "', '" + str(tickerPrice) +\
                             "', '" + self.ui.comboboxSector.currentText() + "')"
            accountLedger = f"CREATE TABLE IF NOT EXISTS {modifiedAN}(Transaction_Date NUMERIC, Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Sold REAL, Purchased REAL, Price REAL, Note TEXT, Status TEXT," \
                            f" Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            accountSummary = f"INSERT INTO Account_Summary VALUES('{self.ui.lEditAN.text()}', 'Asset', '{self.parentType}', '{self.ui.comboboxAT.currentText()}', '{self.ui.lEditV1.text().upper()}', '0.00')"

            # The Contribution Totals table only applies to the Equities and Retirement. Where you compare amount invested to value.
            contribution_statement = f"ALTER TABLE ContributionTotals ADD COLUMN '{modifiedAN}' TEXT"
            specific_sql_statement(contribution_statement, self.refUserDB, self.error_Logger)

        elif self.parentType in variant4:
            accountDetails = "INSERT INTO " + self.accountDetailsTable + \
                             " VALUES('" + self.ui.lEditAN.text() + \
                             "', '" + self.ui.comboboxAT.currentText() + \
                             "', '" + self.ui.lEditPO.text() + \
                             "', '" + self.ui.lEditB.text() + \
                             "', '" + self.ui.lEditV1.text() + \
                             "', '" + self.ui.lEditV2.text() + \
                             "', '" + self.ui.comboboxState.currentText() + \
                             "', '" + self.ui.lEZipCode.text() + \
                             "', NULL)"

        else:  # Cash
            accountDetails = "INSERT INTO " + self.accountDetailsTable + \
                             " VALUES('" + self.ui.lEditAN.text() + \
                             "', '" + self.ui.comboboxAT.currentText() + \
                             "', '" + self.ui.lEditPO.text() + \
                             "', '" + self.ui.lEditB.text() + \
                             "', '" + str(self.ui.spinBStatement.value()) + "')"

        statement_list = [accountDetails, accountLedger, accountSummary, accountWorth, accountWorthToday, accountWorthYest]
        execute_sql_statement_list(statement_list, self.refUserDB, self.error_Logger)

        new_account_df = create_DF(accountName, self.refUserDB, self.error_Logger)
        update_df_ledger(self.ledgerContainer, accountName, self.error_Logger, activeLedger=new_account_df, action="New")

    def archive_account(self):
        if self.ui.listWidgetAccount.currentItem() is None:
            pass
        else:
            accountName = self.ui.self.ui.listWidgetAccount.currentItem().text()
            sql_accountName = remove_space(accountName)
            move_row_sql_tables("Account_Archive", "Account_Summary", "ID", accountName, self.refUserDB, self.error_Logger)
            self.ui.listWidgetAccount.clear()
            fill_widget(self.ui.listWidgetAccount, self.listWidget_Statement, True, self.refUserDB, self.error_Logger)
            self.clear_widgets()

    def clear_widgets(self):
        self.ui.lEditAN.setText("")
        self.ui.lEditPO.setText("")
        self.ui.lEditB.setText("")
        self.ui.lError.setText("")
        self.ui.lEditV1.setText("")
        self.ui.lEditV2.setText("")
        self.ui.lEZipCode.setText("")
        self.ui.comboboxState.setCurrentIndex(0)
        self.ui.spinBStatement.setValue(1)
        self.ui.comboboxAT.setCurrentIndex(0)
        self.ui.comboboxSector.setCurrentIndex(0)

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def disp_current_selection(self):
        variant1 = ["Bank", "Credit"]
        variant2 = ["CD", "Treasury", "Debt", "Retirement"]
        variant3 = "Equity"
        variant4 = "Property"
        variant5 = "Cash"

        if self.ui.listWidgetAccount.currentItem() is None:
            account = None
        else:
            account = self.ui.listWidgetAccount.currentItem().text()
            selectStatement = f"SELECT * FROM {self.accountDetailsTable} WHERE Account_Name ='{account}'"
            account = obtain_sql_value(selectStatement, self.refUserDB, self.error_Logger)

        if account is None:
            self.ui.lEditAN.setText("")
            self.ui.comboboxAT.setCurrentIndex(0)
            self.ui.lEditPO.setText("")
            self.ui.lEditB.setText("")
            self.ui.spinBStatement.setValue(1)
            self.ui.lEditV1.setText("")
            self.ui.lEditV2.setText("")
            self.ui.lEZipCode.setText("")
            self.ui.comboboxState.setCurrentIndex(0)

        else:  # common across all variants
            self.ui.lEditAN.setText(account[0])
            comboItem = account[1]
            self.find_combobox_text(self.ui.comboboxAT, comboItem)
            self.ui.lEditPO.setText(account[2])
            self.ui.lEditB.setText(account[3])

            if self.parentType in variant1:
                spinBox = int(account[4])
                self.ui.spinBStatement.setValue(spinBox)
                self.ui.lEditV1.setText(str(account[5]))

            elif self.parentType in variant2:
                spinBox = int(account[4])
                self.ui.spinBStatement.setValue(spinBox)
                self.ui.lEditV1.setText(str(account[5]))
                self.ui.lEditV2.setText(str(account[6]))

            elif self.parentType in variant3:
                spinBox = int(account[4])
                self.ui.spinBStatement.setValue(spinBox)
                self.ui.lEditV1.setText(str(account[5]))
                self.ui.lEditV2.setText(str(account[6]))
                sectorItem = account[7]
                self.find_combobox_text(self.ui.comboboxSector, sectorItem)

            elif self.parentType in variant4:
                self.ui.lEditV1.setText(str(account[4]))
                self.ui.lEditV2.setText(str(account[5]))
                comboState = account[6]
                self.find_combobox_text(self.ui.comboboxState, comboState)
                self.ui.lEZipCode.setText(str(account[7]))

            else:  # just a catch all
                pass

    def delete_account(self):
        question = f"Are you sure you want to delete {self.ui.listWidgetAccount.currentItem().text()}?\nAll associated data and receipts will be permanently deleted."
        reply = QMessageBox.question(self, "Confirmation", question, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            target_account = self.ui.lEditAN.text()
            self.delete_account_sql(target_account)

            update_df_ledger(self.ledgerContainer, target_account, self.error_Logger, activeLedger=None, action="Delete")

            self.ui.listWidgetAccount.clear()
            fill_widget(self.ui.listWidgetAccount, self.listWidget_Statement, True, self.refUserDB, self.error_Logger)
            self.clear_widgets()
            self.ui.listWidgetAccount.setCurrentRow(0)
            self.disp_current_selection()
        else:
            pass

    def delete_account_sql(self, accountName):
        """To Avoid permanent deletion of receipts until user commits an account save. The account will be removed superficially until a save is performed. The SQL database is a temp file.
        so if the user doesn't save all of that information will be restored from the last save state. The idea of an auto save function running in the background has been floated. However,
         this is currently not planned. As developed moved away from original auto save functionality of an SQL Database."""
        sql_accountName = remove_space(accountName)

        deleteDetails = f"DELETE FROM {self.accountDetailsTable} WHERE Account_Name ='{accountName}'"
        deleteSummary = f"DELETE FROM Account_Summary WHERE ID ='{accountName}'"
        dropLedger = f"DROP TABLE IF EXISTS {sql_accountName}"
        dropAccountWorth = f"ALTER TABLE AccountWorth DROP COLUMN {sql_accountName}"
        delete_statement = f"INSERT INTO DeletePending VALUES('{accountName}', '{self.parentType}')"

        statement_list = [deleteDetails,
                          deleteSummary,
                          dropLedger,
                          dropAccountWorth,
                          delete_statement]

        execute_sql_statement_list(statement_list, self.refUserDB, self.error_Logger)

        if self.parentType in ["Equity", "Retirement"]:
            delete_column("ContributionTotals", sql_accountName, self.refUserDB, self.error_Logger)

    def edit_account(self):
        self.toggle_widgets(True)
        self.ui.pBSubmit.setEnabled(False)
        self.ui.pBSubmit.setHidden(True)
        self.ui.pBEditSubmit.setEnabled(True)
        self.ui.pBEditSubmit.setHidden(False)
        self.ui.pBModify.setEnabled(True)
        self.ui.lEditAN.setFocus()

    def error_checking(self, purpose):
        accountName = self.ui.lEditAN.text()
        accountSubType = self.ui.comboboxAT.currentText()
        accountOwner = self.ui.lEditPO.text()
        accountBank = self.ui.lEditB.text()
        accountVariable1 = self.ui.lEditV1.text()
        accountVariable2 = self.ui.lEditV2.text()
        accountZip = self.ui.lEZipCode.text()

        detail_inputs = [[accountName, "general"], [accountSubType, "general"], [accountOwner, "general"], [accountBank, "general"], ]

        error_status = False

        for value in detail_inputs:
            if find_character(value[0]) is False:
                self.ui.lError.setText("No Blank Inputs")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status
            elif check_characters(value[0]) is False:
                self.ui.lError.setText("Alphanumeric Characters only")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status
            elif sqlite3_keyword_check(value[0]) is True:
                self.ui.lError.setText("Restricted Keyword")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status

        if error_status is False:
            if first_character_check(detail_inputs[0][0]) is False:
                self.ui.lError.setText("Start Account Name\nwith letter")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status

        if error_status is False and purpose != "Edit":
            if check_for_data(self.accountDetailsTable, "Account_Name", accountName, self.refUserDB, self.error_Logger) is False:
                self.ui.lError.setText("Duplicate Account:\nTry Unique Name")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status

        if error_status is False and purpose != "Edit":
            if check_for_data("Account_Summary", "ID", accountName, self.refUserDB, self.error_Logger) is False:
                self.ui.lError.setText("Duplicate Account:\nTry Unique Name")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status

        if error_status is False:
            if self.parentType in ["Bank", "CD", "Treasury", "Debt", "Credit"]:
                if check_characters(accountVariable1, "monetary") is False:
                    self.ui.lError.setText("Monetary Format: 0.00")
                    self.ui.lError.setStyleSheet(generalError)
                    error_status = True
                    return error_status

                elif check_numerical_inputs(accountVariable1) is False:
                    self.ui.lError.setText("Monetary Format: 0.00")
                    self.ui.lError.setStyleSheet(generalError)
                    error_status = True
                    return error_status

            elif self.parentType in ["Equity", "Retirement", "Property"]:
                if find_character(accountVariable1) is False:
                    self.ui.lError.setText("Alphanumeric Inputs")
                    self.ui.lError.setStyleSheet(generalError)
                    error_status = True
                    return error_status
            else:
                pass

        if "," in accountVariable2:
            accountVariable2 = accountVariable2.replace(",", "")

        if error_status is False:
            if check_characters(accountVariable2) is False:
                if self.parentType in ["CD", "Treasury"]:
                    self.ui.lError.setText("Date Format")
                    self.ui.lError.setStyleSheet(generalError)
                    error_status = True
                    return error_status
                elif self.parentType in ["Equity", "Retirement", "Debt"]:
                    self.ui.lError.setText("Monetary Format: 0.00")
                    self.ui.lError.setStyleSheet(generalError)
                    error_status = True
                    return error_status
                else:
                    pass

        if error_status is False and self.parentType == "Property":
            try:
                int(accountZip)
            except ValueError:
                self.ui.lError.setText("Numerical Input Only")
                self.ui.lError.setStyleSheet(generalError)
                error_status = True
                return error_status
            else:
                pass

        if error_status is False:
            return error_status

    def find_combobox_text(self, comboBox, comboItem):
        index = comboBox.findText(comboItem)
        if index >= 0:
            comboBox.setCurrentIndex(index)
        else:
            self.ui.lError.setText("Error: Unidentified Bank Type")

    def initial_appearance(self, parentType):
        if parentType in ["Bank"]:
            # Account Name, Account Type, Primary Owner, Bank, Statement Date, Interest Rate
            self.ui.lVariable2.setEnabled(False)
            self.ui.lVariable2.setHidden(True)
            self.ui.lEditV2.setHidden(True)

        elif parentType == "Cash":
            # Account Name, Account Type, Primary Owner, Bank, Statement Date
            self.ui.lVariable1.setEnabled(False)
            self.ui.lVariable1.setHidden(True)
            self.ui.lEditV1.setHidden(True)
            self.ui.lVariable2.setEnabled(False)
            self.ui.lVariable2.setHidden(True)
            self.ui.lEditV2.setHidden(True)

        elif parentType in ["CD", "Treasury"]:
            # Account Name, Account Type, Primary Owner, Bank, Statement Date, Interest Rate, Maturity Date
            self.ui.lVariable2.setText("Maturity Date")

        elif parentType in ["Equity", "Retirement"]:
            # Account Name, Account Type, Primary Owner, Bank, Statement Date, Ticker Symbol, Ticker Price
            self.resize(400, 550)
            self.ui.lVariable1.setText("Ticker Symbol")
            self.ui.lVariable2.setText("Ticker Price")
            self.ui.lSector.setHidden(False)
            self.ui.comboboxSector.setHidden(False)

        elif parentType == "Debt":
            # Account Name, Account Type, Primary Owner, Bank, Statement Date, Interest Rate, Starting Balance
            self.ui.lVariable2.setText("Starting Balance")

        elif parentType == "Credit":
            # Account Name, Account Type, Primary Owner, Bank, Statement Date, Credit Limit
            self.ui.lVariable1.setText("Credit Limit")
            self.ui.lVariable2.setEnabled(False)
            self.ui.lVariable2.setHidden(True)
            self.ui.lEditV2.setHidden(True)

        else:  # Property
            # Account Name, Account Type, Primary Owner, Bank, Street, County, St, Zip
            self.resize(500, 550)
            self.ui.lVariable1.setText("Street")
            self.ui.lVariable2.setText("County, St Zip")
            self.ui.spinBStatement.setHidden(True)
            self.ui.lStatement.setHidden(True)
            self.ui.comboboxState.setHidden(False)
            self.ui.lEZipCode.setHidden(False)

    def new_account(self):
        self.toggle_widgets(False)
        self.toggle_widgets(True)
        self.ui.pBSubmit.setEnabled(True)
        self.ui.pBSubmit.setHidden(False)
        self.ui.pBEditSubmit.setEnabled(False)
        self.ui.pBEditSubmit.setHidden(True)
        self.ui.pBModify.setEnabled(True)
        self.ui.lEditAN.setFocus()
        self.clear_widgets()

    def submit_account(self):
        accountName = self.ui.lEditAN.text()
        sqlAccountName = remove_space(self.ui.lEditAN.text())
        if self.error_checking("New") is False:
            self.add_account_information()
            self.ui.listWidgetAccount.addItem(accountName)
            file_destination(['Alchemical Finances', 'Receipts', self.refUser, self.parentType, sqlAccountName], starting_point=self.storage_dir)
            # change stylesheet here
            self.toggle_widgets(False)
            self.ui.listWidgetAccount.setCurrentRow(0)
            self.disp_current_selection()

    def submit_edit(self):
        variant1 = ["Bank", "Credit"]
        variant2 = ["CD", "Treasury", "Debt"]
        variant3 = ["Equity", "Retirement"]
        variant4 = ["Property"]

        accountName = self.ui.lEditAN.text()
        accountSubType = self.ui.comboboxAT.currentText()
        accountOwner = self.ui.lEditPO.text()
        accountBank = self.ui.lEditB.text()
        accountStatement = str(self.ui.spinBStatement.value())
        accountVariable1 = self.ui.lEditV1.text()
        accountVariable2 = self.ui.lEditV2.text()
        accountState = self.ui.comboboxState.currentText()
        accountZip = self.ui.lEZipCode.text()
        accountSector = self.ui.comboboxSector.currentText()

        if self.error_checking("Edit") is False:
            currentLedgerName = self.ui.listWidgetAccount.currentItem().text()
            sqlCurrentLedgerName = remove_space(self.ui.listWidgetAccount.currentItem().text())
            sqlNewLedgerName = remove_space(accountName)

            if self.parentType not in ["Equity", "Retirement"]:
                summaryUpdate = f"UPDATE Account_Summary SET ID='{accountName}', SubType='{accountSubType}' WHERE ID='{currentLedgerName}'"
            else:
                summaryUpdate = f"UPDATE Account_Summary SET ID='{accountName}', SubType='{accountSubType}', Ticker_Symbol='{accountVariable1}' WHERE ID='{currentLedgerName}'"

            deleteOldDetails = f"DELETE FROM {self.accountDetailsTable} WHERE Account_Name ='{currentLedgerName}'"
            if self.parentType in variant1:
                detailsUpdate = "INSERT INTO " + self.accountDetailsTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + \
                                "', '" + accountStatement + \
                                "', '" + accountVariable1 + "')"
            elif self.parentType in variant2:
                detailsUpdate = "INSERT INTO " + self.accountDetailsTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + \
                                "', '" + accountStatement + \
                                "', '" + accountVariable1 + \
                                "', '" + accountVariable2 + "')"
            elif self.parentType in variant3:
                detailsUpdate = "INSERT INTO " + self.accountDetailsTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + \
                                "', '" + accountStatement + \
                                "', '" + accountVariable1 + \
                                "', '" + accountVariable2 + \
                                "', '" + accountSector + "')"
            elif self.parentType in variant4:
                detailsUpdate = "INSERT INTO " + self.accountDetailsTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + \
                                "', '" + accountVariable1 + \
                                "', '" + accountVariable2 + \
                                "', '" + accountState + \
                                "', '" + accountZip + "')"
            else:  # Cash
                detailsUpdate = "INSERT INTO " + self.accountDetailsTable + \
                                " VALUES('" + accountName + \
                                "', '" + accountSubType + \
                                "', '" + accountOwner + \
                                "', '" + accountBank + "')"

            if sqlCurrentLedgerName != sqlNewLedgerName:
                ledgerUpdate = f"ALTER TABLE {sqlCurrentLedgerName} RENAME TO '{sqlNewLedgerName}'"
                accountWorth = f"ALTER TABLE AccountWorth RENAME COLUMN '{sqlCurrentLedgerName}' TO '{sqlNewLedgerName}'"

                old_dir_path = file_destination(['Alchemical Finances', 'Receipts', self.refUser, self.parentType, sqlCurrentLedgerName], starting_point=self.storage_dir)
                new_dir_path = file_destination(['Alchemical Finances', 'Receipts', self.refUser, self.parentType, sqlNewLedgerName], starting_point=self.storage_dir)

                old_receipt_dir = str(old_dir_path)
                new_receipt_dir = str(new_dir_path)

                os.rmdir(new_receipt_dir)
                os.rename(old_receipt_dir, new_receipt_dir)

                current_ledger = load_df_ledger(self.ledgerContainer, currentLedgerName)

                update_df_ledger(self.ledgerContainer, currentLedgerName, self.error_Logger, activeLedger=current_ledger, action="Rename", new_account=accountName)

            else:
                ledgerUpdate = f"SELECT Subtype FROM AccountSubType WHERE ParentType='{self.parentType}'"
                accountWorth = f"ALTER TABLE AccountWorth RENAME COLUMN '{sqlCurrentLedgerName}' TO '{sqlNewLedgerName}'"
            # Above functions exists just to avoid a crash -------------------------------------------------------------
            statement_list = [summaryUpdate, deleteOldDetails, detailsUpdate, ledgerUpdate, accountWorth]
            execute_sql_statement_list(statement_list, self.refUserDB, self.error_Logger)

            if self.parentType in ["Equity", "Retirement"]:
                contribution = f"ALTER TABLE ContributionTotals RENAME COLUMN '{sqlCurrentLedgerName}' TO '{sqlNewLedgerName}'"
                specific_sql_statement(contribution, self.refUserDB, self.error_Logger)

            row = self.ui.listWidgetAccount.currentRow()
            self.ui.listWidgetAccount.takeItem(row)
            self.ui.listWidgetAccount.insertItem(row, QListWidgetItem(accountName))

            self.ui.listWidgetAccount.setCurrentRow(0)
            self.disp_current_selection()
            self.toggle_widgets(False)
            self.ui.lError.setText("")

    def toggle_widgets(self, switch):
        self.ui.lEditAN.setEnabled(switch)
        self.ui.comboboxAT.setEnabled(switch)
        self.ui.lEditPO.setEnabled(switch)
        self.ui.lEditB.setEnabled(switch)
        self.ui.pBModify.setEnabled(switch)

        if self.parentType in ["Bank", "Credit"]:
            self.ui.spinBStatement.setEnabled(switch)
            self.ui.lEditV1.setEnabled(switch)
        elif self.parentType == "Cash":
            self.ui.spinBStatement.setEnabled(switch)
        elif self.parentType in ["CD", "Treasury", "Debt"]:
            self.ui.spinBStatement.setEnabled(switch)
            self.ui.lEditV1.setEnabled(switch)
            self.ui.lEditV2.setEnabled(switch)
        elif self.parentType in ["Equity", "Retirement"]:
            self.ui.spinBStatement.setEnabled(switch)
            self.ui.lEditV1.setEnabled(switch)
            self.ui.lEditV2.setEnabled(switch)
            self.ui.comboboxSector.setEnabled(switch)
        elif self.parentType == "Property":
            self.ui.lEditV1.setEnabled(switch)
            self.ui.lEditV2.setEnabled(switch)
            self.ui.comboboxState.setEnabled(switch)
            self.ui.lEZipCode.setEnabled(switch)
            self.ui.lEZipCode.setEnabled(switch)

    def type_modifier(self):
        molly = YNTypeQuestion(self.refUserDB, self.parentType, self.error_Logger)
        if molly.exec() == QDialog.Accepted:
            self.ui.comboboxAT.clear()
            fill_widget(self.ui.comboboxAT, self.comboboxT_Statement, True, self.refUserDB, self.error_Logger)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")




