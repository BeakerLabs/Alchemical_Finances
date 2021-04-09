"""
This script is the backend to Frontend.ArchiveUi.py

Future Concepts

"""

import shutil
import time

from PySide6.QtWidgets import QMessageBox, QDialog, QInputDialog
from PySide6 import QtCore
from pathlib import Path
from Frontend.ArchiveUi import Ui_Archive
# from Backend.Receipt import Receipt

from Toolbox.OS_Tools import file_destination
from Toolbox.AF_Tools import disp_LedgerV1_Table, disp_LedgerV2_Table, generate_statement_months
from Toolbox.SQL_Tools import  execute_sql_statement_list, move_sql_tables, obtain_sql_value, obtain_sql_list
from Toolbox.Formatting_Tools import remove_space

# from Frontend.StyleSheets import UniversalStyleSheet


class Archive(QDialog):
    remove_tab_archive = QtCore.Signal(str)

    def __init__(self, database, user):
        super().__init__()
        self.ui = Ui_Archive()
        self.ui.setupUi(self)
        self.setWindowTitle("Archive")
        # set Stylesheet here
        self.show()

        self.refUserDB = database
        self.refUser = user

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
            self.fill_combobox(self.ui.comboBStatements, "Statement")
            self.display_ledger()

        self.ui.comboBAccounts.currentIndexChanged.connect(self.change_account)
        self.ui.comboBStatements.currentIndexChanged.connect(self.display_ledger)
        self.ui.pBRestore.clicked.connect(self.restore_account)
        self.ui.pBDelete.clicked.connect(self.delete_account)
        self.ui.pBDisplayReceipt.clicked.connect(self.display_receipt)

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()

    def change_account(self):
        self.ui.comboBStatements.clear()
        self.fill_combobox(self.ui.comboBStatements, "Statement")

    def delete_account(self):
        ledger_name = self.widgetlist[0].currentText()
        modified_ledger_name = remove_space(ledger_name)

        parentType_statement = f"SELECT ParentType FROM Account_Archive WHERE ID='{ledger_name}'"
        parentType_value = obtain_sql_value(parentType_statement, self.refUserDB)
        parentType_value = parentType_value[0]
        details_table = self.parentType_dict[parentType_value]

        delete_message = "Selecting 'YES' will permanently delete this account and all associated information"
        confirm = QMessageBox.warning(self, 'Confirm', delete_message, QMessageBox.Yes, QMessageBox.No)

        receipt_directory_path = Path.cwd() / 'Receipts' / parentType_value / modified_ledger_name

        if confirm == QMessageBox.Yes:
            delete_archive = f"DELETE FROM Account_Archive WHERE ID = '{ledger_name}'"
            delete_details = f"DELETE FROM {details_table} WHERE Account_Name ='{ledger_name}'"
            delete_ledger = f"DROP TABLE IF EXISTS {modified_ledger_name}"
            execute_sql_statement_list([delete_archive, delete_details, delete_ledger], self.refUserDB)
            shutil.rmtree(receipt_directory_path)
            self.ui.comboBAccounts.clear()
            self.ui.comboBStatements.clear()
            self.fill_combobox(self.ui.comboBAccounts, "Accounts")
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
            parentType_value = obtain_sql_value(parentType_statement, self.refUserDB)
            parentType_value = parentType_value[0]

            type1 = ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit"]
            type2 = ["Equity", "Retirement"]
            if parentType_value in type1:
                disp_LedgerV1_Table(self.ui.comboBAccounts, self.ui.comboBStatements, self.ui.tWArchive, self.refUserDB)
            elif parentType_value in type2:
                disp_LedgerV2_Table(self.ui.comboBAccounts, self.ui.comboBStatements, self.ui.tWArchive, self.refUserDB)
            else:
                error = "Ledger Type Doesn't Exist"
                self.input_error_msg(error)

    def display_receipt(self):
        ledger = self.widgetlist[0].currentText()
        ledger_sql = remove_space(ledger)

        parentType_statement = "SELECT ParentType FROM Account_Archive WHERE ID='" + ledger + "'"
        parentType_value = obtain_sql_value(parentType_statement, self.refUserDB)
        parentType_value = parentType_value[0]

        inputText1 = "Select Row"
        inputText2 = "Enter Row#: "
        row = self.user_selection_input(self.ui.tWArchive, inputText1, inputText2)
        if row == -1:
            pass
        elif row == 0:
            pass
        else:
            file_Name_Statement = f"SELECT Receipt FROM {ledger_sql} WHERE RowID = {str(row)}"
            file_Name = obtain_sql_value(file_Name_Statement, self.refUserDB)
            file_Name = file_Name[0]

            if file_Name == "":
                noReceipt = "Sorry, No Receipt Uploaded"
                self.input_error_msg(noReceipt)
            else:
                file_pathway = file_destination(['Receipts', self.refUser, parentType_value, ledger_sql])
                pathway = Path.cwd() / file_pathway / file_Name
                ion = Receipt(str(pathway), file_Name)
                if ion.exec_() == QDialog.Accepted:
                    pass

    def fill_combobox(self, combobox, target):
        if target == "Account":
            account_sql_statement = "SELECT ID FROM Account_Archive"
            comboBox_rawData = obtain_sql_list(account_sql_statement, self.refUserDB)
            comboBox_list = []
            for ID in comboBox_rawData:
                comboBox_list.append(ID[0])
            combobox.addItems(comboBox_list)
            combobox.model().sort(0)
            combobox.setCurrentIndex(0)

        else:
            account = self.ui.comboBAccounts.currentText()
            statement_period_list = generate_statement_months(account, "Archive", self.refUserDB)
            combobox.addItems(statement_period_list)
            combobox.setCurrentIndex(0)

    def input_error_msg(self, message):
        reply = QMessageBox.warning(self, 'Input Error', message, QMessageBox.Ok, QMessageBox.NoButton)
        if reply == QMessageBox.Ok:
            pass
        else:
            pass

    def restore_account(self):
        move_sql_tables("Account_Summary", "Account_Archive", "ID", self.ui.comboBAccounts.currentText(), self.refUserDB)
        self.ui.comboBAccounts.clear()
        self.ui.comboBStatements.clear()
        self.fill_combobox(self.ui.comboBAccounts, "Accounts")
        self.fill_combobox(self.ui.comboBStatements, "Statement")
        self.display_ledger()

    def trigger_del_tab(self):
        self.remove_tab_archive.emit("Archive")

    def user_selection_input(self, tableWidget, text1, text2):
        row, ok = QInputDialog.getInt(self, text1, text2, 1, 1, tableWidget.rowCount(), 1)
        if ok and row:
            return row
        else:
            row = 0
            return row


# --- Catchall --- #
if __name__ == '__main__':
    print("Error - Check your executable")
