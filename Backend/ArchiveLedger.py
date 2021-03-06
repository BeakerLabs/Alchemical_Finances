#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import shutil
import sys

from pathlib import Path, PurePath
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox, QDialog, QInputDialog

from Frontend.ArchiveUi import Ui_Archive

from StyleSheets.StandardCSS import standardAppearance

from Backend.DataFrame import load_df_ledger
from Backend.ReceiptViewer import Receipt

from Toolbox.AF_Tools import disp_LedgerV1_Table, disp_LedgerV2_Table, generate_statement_months
from Toolbox.Formatting_Tools import remove_space
from Toolbox.OS_Tools import file_destination, obtain_storage_dir
from Toolbox.SQL_Tools import execute_sql_statement_list, move_row_sql_tables, obtain_sql_value, obtain_sql_list


class Archive(QDialog):
    remove_tab_archive = QtCore.Signal(str)

    def __init__(self, database, user, ledger_container, error_log):
        super().__init__()
        self.ui = Ui_Archive()
        self.ui.setupUi(self)
        self.setWindowTitle("Archive")
        # set Stylesheet here
        self.show()

        self.storage_dir = obtain_storage_dir()
        self.refUserDB = database
        self.refUser = user
        self.ledger_container = ledger_container
        self.error_Logger = error_log

        self.parentType_dict = {"Bank": "Bank_Account_Details",
                                "Equity": "Equity_Account_Details",
                                "Retirement": "Retirement_Account_Details",
                                "CD": "CD_Account_Details",
                                "Treasury": "Treasury_Account_Details",
                                "Debt": "Debt_Account_Details",
                                "Credit": "Credit_Account_Details",
                                "Cash": "Cash_Account_Details",
                                "Property": "Property_Account_Details"}

        self.fill_combobox(self.ui.comboBAccounts, "Account")

        if self.ui.comboBAccounts.currentText() != "":
            self.active_account = self.ui.comboBAccounts.currentText()
            self.activeLedger = load_df_ledger(self.ledger_container, self.active_account)

            self.fill_combobox(self.ui.comboBStatements, "Statement")
            self.toggle_entire_ledger(True)
            self.display_ledger()
        else:
            self.toggle_entire_ledger(False)

        self.ui.comboBAccounts.currentIndexChanged.connect(self.change_account)
        self.ui.comboBStatements.currentIndexChanged.connect(self.display_ledger)
        self.ui.pBRestore.clicked.connect(self.restore_account)
        self.ui.pBDelete.clicked.connect(self.delete_account)
        self.ui.pBDisplayReceipt.clicked.connect(self.display_receipt)

        self.setStyleSheet(standardAppearance)

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()

    def change_account(self):
        self.active_account = self.ui.comboBAccounts.currentText()
        self.activeLedger = load_df_ledger(self.ledger_container, self.active_account)

        self.ui.comboBStatements.clear()
        self.fill_combobox(self.ui.comboBStatements, "Statement")

    def delete_account(self):
        ledger_name = self.ui.comboBAccounts.currentText()
        modified_ledger_name = remove_space(ledger_name)

        parentType_statement = f"SELECT ParentType FROM Account_Archive WHERE ID='{ledger_name}'"
        parentType_value = obtain_sql_value(parentType_statement, self.refUserDB, self.error_Logger)
        parentType_value = parentType_value[0]
        details_table = self.parentType_dict[parentType_value]

        delete_message = "Selecting 'YES' will permanently delete this account and all associated information"
        confirm = QMessageBox.warning(self, 'Confirm', delete_message, QMessageBox.Yes, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            delete_archive = f"DELETE FROM Account_Archive WHERE ID = '{ledger_name}'"
            delete_details = f"DELETE FROM {details_table} WHERE Account_Name ='{ledger_name}'"
            delete_ledger = f"DROP TABLE IF EXISTS {modified_ledger_name}"
            dropAccountWorth = f"ALTER TABLE AccountWorth DROP COLUMN {modified_ledger_name}"
            delete_statement = f"INSERT INTO DeletePending VALUES({modified_ledger_name}, {parentType_value})"

            statement_lst = [delete_archive,
                             delete_details,
                             delete_ledger,
                             dropAccountWorth,
                             delete_statement]
            execute_sql_statement_list(statement_lst, self.refUserDB, self.error_Logger)

            self.ui.comboBAccounts.clear()
            self.ui.comboBStatements.clear()
            self.fill_combobox(self.ui.comboBAccounts, "Account")
            self.fill_combobox(self.ui.comboBStatements, "Statement")
            self.ui.tWArchive.clear()
            self.display_ledger()
        else:
            pass

    def display_ledger(self):
        ledger = self.ui.comboBAccounts.currentText()
        statement = self.ui.comboBStatements.currentText()
        if ledger == "":
            pass
        elif statement == "":
            pass
        else:
            parentType_statement = f"SELECT ParentType FROM Account_Archive WHERE ID='{ledger}'"
            parentType_value = obtain_sql_value(parentType_statement, self.refUserDB, self.error_Logger)
            parentType_value = parentType_value[0]

            type1 = ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit"]
            type2 = ["Equity", "Retirement"]
            if parentType_value in type1:
                disp_LedgerV1_Table(self.ui.comboBAccounts, self.ui.comboBStatements, parentType_value, self.ui.tWArchive, self.activeLedger)
            elif parentType_value in type2:
                disp_LedgerV2_Table(self.ui.comboBAccounts, self.ui.comboBStatements, self.ui.tWArchive, self.activeLedger)
            else:
                error = "Ledger Type Doesn't Exist"
                self.input_error_msg(error)

    def display_receipt(self):
        ledger = self.ui.comboBAccounts.currentText()
        ledger_sql = remove_space(ledger)

        parentType_statement = f"SELECT ParentType FROM Account_Archive WHERE ID='{ledger}'"
        parentType_value = obtain_sql_value(parentType_statement, self.refUserDB, self.error_Logger)
        parentType_value = parentType_value[0]

        inputText1 = "Select Row"
        inputText2 = "Enter Row#: "
        row = self.user_selection_input(self.ui.tWArchive, inputText1, inputText2)
        if row == -1:
            pass
        elif row == 0:
            pass
        else:
            row -= 1
            file_Name = self.ui.tWArchive.item(row, 7).text()
            suffix = PurePath(file_Name).suffix

            file_pathway = file_destination(['Alchemical Finances', 'Receipts', self.refUser, parentType_value, ledger_sql], starting_point=self.storage_dir)
            pathway = Path(file_pathway) / file_Name

            if file_Name == "":
                noReceipt = "Sorry, No Receipt Uploaded"
                self.input_error_msg(noReceipt)
            elif suffix == ".pdf":
                os.startfile(pathway)
            else:
                ion = Receipt(str(pathway), file_Name)
                if ion.exec() == QDialog.Accepted:
                    pass

    def fill_combobox(self, combobox, target):
        if target == "Account":
            account_sql_statement = "SELECT ID FROM Account_Archive"
            comboBox_rawData = obtain_sql_list(account_sql_statement, self.refUserDB, self.error_Logger)
            comboBox_list = []
            for ID in comboBox_rawData:
                comboBox_list.append(ID[0])
            combobox.addItems(comboBox_list)
            combobox.model().sort(0)
            combobox.setCurrentIndex(0)

        else:  # Statement
            account = self.ui.comboBAccounts.currentText()
            if account is None or account == "" or account == " ":
                pass
            else:
                statement_period_list = generate_statement_months(self.active_account, "Archive", self.refUserDB, self.activeLedger, self.error_Logger)
                combobox.addItems(statement_period_list)
                combobox.setCurrentIndex(0)

    def input_error_msg(self, message):
        reply = QMessageBox.warning(self, 'Input Error', message, QMessageBox.Ok, QMessageBox.NoButton)
        if reply == QMessageBox.Ok:
            pass
        else:
            pass

    def restore_account(self):
        move_row_sql_tables("Account_Summary", "Account_Archive", "ID", self.ui.comboBAccounts.currentText(), self.refUserDB, self.error_Logger)
        self.ui.comboBAccounts.clear()
        self.ui.comboBStatements.clear()
        self.fill_combobox(self.ui.comboBAccounts, "Account")

        if self.ui.comboBAccounts.currentText() != "":
            self.fill_combobox(self.ui.comboBStatements, "Statement")
            self.display_ledger()
        else:
            self.toggle_entire_ledger(False)

    def toggle_entire_ledger(self, toggle: bool):
        self.ui.comboBAccounts.setEnabled(toggle)
        self.ui.pBDisplayReceipt.setEnabled(toggle)
        self.ui.pBDelete.setEnabled(toggle)
        self.ui.pBRestore.setEnabled(toggle)
        self.ui.comboBStatements.setEnabled(toggle)

    def trigger_del_tab(self):
        self.remove_tab_archive.emit("Archive")

    def user_selection_input(self, tableWidget, text1, text2):
        row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
        if ok and row:
            return row
        else:
            row = 0
            return row


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
