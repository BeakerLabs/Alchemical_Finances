"""
This script is the backend to Frontend.CategoriesUi.py

Future Concepts

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6.QtWidgets import QDialog, QMessageBox

from Backend.DataFrame import load_df_ledger, update_df_ledger

from Frontend.CategoriesUi import Ui_Categories

from Toolbox.AF_Tools import fill_widget
from Toolbox.Error_Tools import check_characters, first_character_check
from Toolbox.SQL_Tools import attempt_sql_statement, obtain_sql_list, specific_sql_statement

from StyleSheets.StandardCSS import standardAppearance


class SpendingCategories(QDialog):
    def __init__(self, database, parentType, ledger_container, error_log):
        super().__init__()
        self.ui = Ui_Categories()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.parentType = parentType
        self.ledgerContainer = ledger_container
        self.dialogState = None
        self.initialCategory = None

        # Program Error Logger
        self.error_Logger = error_log

        self.ui.lsubheader.setText(f"for {self.parentType} Accounts")
        self.listWidget_Statement = f"SELECT Method FROM Categories WHERE ParentType= '{self.parentType}'"
        fill_widget(self.ui.listWidgetCat, self.listWidget_Statement, True, self.refUserDB, self.error_Logger)
        self.ui.pBNew.clicked.connect(lambda: self.alter_appearance("new"))
        self.ui.pBEdit.clicked.connect(lambda: self.alter_appearance("edit"))
        self.ui.pBReplace.clicked.connect(lambda: self.alter_appearance("replace"))
        self.ui.pBDelete.clicked.connect(self.delete_category)
        self.ui.pBSubmit.clicked.connect(self.submit_Input)
        self.ui.pBCancel.clicked.connect(lambda: self.alter_appearance("reset"))
        self.ui.listWidgetCat.setCurrentRow(0)
        self.disp_current_category()
        self.ui.listWidgetCat.itemClicked.connect(self.disp_current_category)
        self.setModal(True)
        self.setStyleSheet(standardAppearance)
        self.show()

    def alter_appearance(self, state):
        self.ui.listWidgetCat.clear()
        fill_widget(self.ui.listWidgetCat, self.listWidget_Statement, True, self.refUserDB, self.error_Logger)

        self.ui.lEditSelection.setEnabled(True)
        self.ui.pBNew.setEnabled(False)
        self.ui.pBEdit.setEnabled(False)
        self.ui.pBDelete.setEnabled(False)
        self.ui.pBReplace.setEnabled(False)

        if state == "reset":
            self.ui.lInstruction.setText("Selected spending category: ")
            self.ui.lEditSelection.setText("")
            self.ui.listWidgetCat.setCurrentRow(0)
            self.disp_current_category()
            self.dialogState = None
            self.initialCategory = None

            self.ui.lEditSelection.setEnabled(False)
            self.ui.pBNew.setEnabled(True)
            self.ui.pBEdit.setEnabled(True)
            self.ui.pBDelete.setEnabled(True)
            self.ui.pBReplace.setEnabled(True)

            self.ui.pBSubmit.setEnabled(False)
            self.ui.pBSubmit.setHidden(True)
            self.ui.pBCancel.setEnabled(False)
            self.ui.pBCancel.setHidden(True)

        elif state == "new":
            self.ui.lInstruction.setText("Input new spending category: ")
            self.ui.lEditSelection.setText("")
            self.dialogState = "new"

            self.ui.pBSubmit.setEnabled(True)
            self.ui.pBSubmit.setHidden(False)
            self.ui.pBCancel.setEnabled(True)
            self.ui.pBCancel.setHidden(False)

        elif state == "edit":
            self.ui.lInstruction.setText("Input modification: ")
            self.dialogState = "edit"
            self.initialCategory = self.ui.lEditSelection.text()

            self.ui.pBSubmit.setEnabled(True)
            self.ui.pBSubmit.setHidden(False)
            self.ui.pBCancel.setEnabled(True)
            self.ui.pBCancel.setHidden(False)

        elif state == "replace":
            self.ui.lInstruction.setText("Input replacement: ")
            self.dialogState = "replace"
            self.initialCategory = self.ui.lEditSelection.text()

            self.ui.pBSubmit.setEnabled(True)
            self.ui.pBSubmit.setHidden(False)
            self.ui.pBCancel.setEnabled(True)
            self.ui.pBCancel.setHidden(False)

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def delete_category(self):
        question = "Are you sure you want to delete this Transaction Method?"
        reply = QMessageBox.question(self, "Confirmation", question, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            deleteStatement = f"DELETE FROM Categories WHERE Method ='{self.ui.lEditSelection.text()}' AND ParentType ='{self.parentType}'"
            specific_sql_statement(deleteStatement, self.refUserDB, self.error_Logger)
            self.ui.listWidgetCat.clear()
            fill_widget(self.ui.listWidgetCat, self.listWidget_Statement, True, self.refUserDB, self.error_Logger)
            self.ui.lEditSelection.setText("")
            self.ui.listWidgetCat.setCurrentRow(0)
            self.disp_current_category()
        else:
            pass

    def disp_current_category(self):
        if self.ui.listWidgetCat.currentItem() is None:
            selection = ""
        else:
            selection = self.ui.listWidgetCat.currentItem().text()
        self.ui.lEditSelection.setText(selection)

    def submit_Input(self):
        input_type = self.dialogState
        if self.syntax_check(self.ui.lEditSelection.text()) is False:
            if input_type == "new":
                Statement = f"INSERT INTO Categories VALUES('{self.ui.lEditSelection.text()}', '{self.parentType}', 'True')"
                specific_sql_statement(Statement, self.refUserDB, self.error_Logger)
            elif input_type == "edit":
                Statement = f"UPDATE Categories SET Method='{self.ui.lEditSelection.text()}' WHERE Method='{self.ui.listWidgetCat.currentItem().text()}'"
                specific_sql_statement(Statement, self.refUserDB, self.error_Logger)
            elif input_type == "replace":
                question = f"  Are you sure you want to replace:\n  " \
                           f"   {self.initialCategory} with {self.ui.lEditSelection.text()}?  "
                reply = QMessageBox.question(self, "Confirmation", question, QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.replace_category(self.initialCategory)
                    reminder_statement = "Remember to save to keep changes"
                    reminder = QMessageBox.information(self, "Reminder", reminder_statement, QMessageBox.Close, QMessageBox.NoButton)
                    if reminder == QMessageBox.Close:
                        pass
                else:
                    pass

            self.alter_appearance("reset")

        else:
            print(f"""ERROR: SpendingCategories: submit_Input \n Invalid Input: {self.ui.lEditSelection.text()}""")

    def syntax_check(self, question):
        error_status = False

        if error_status is False:
            if check_characters(question, "general") is False:
                error_status = True
                return error_status

        if error_status is False:
            if question == "" or question == " ":
                error_status = True
                return error_status

        if error_status is False:
            if first_character_check(question) is False:
                error_status = True
                return error_status

        if error_status is False:
            duplicate_statement = f"SELECT Method, ParentType FROM Categories WHERE Method ='{self.ui.lEditSelection.text()}' AND ParentType ='{self.parentType}'"
            if attempt_sql_statement(duplicate_statement, self.refUserDB, self.error_Logger) is False:
                error_status = True
                return error_status

        if error_status is False:
            if isinstance(question, str) is False:
                error_status = True
                return error_status

        if error_status is False:
            return error_status

    def replace_category(self, initial):
        parentType_dict = {
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
        replacement_value = self.ui.lEditSelection.text()

        # Replace the value (or remove) from the Categories Table within the database
        category_list_statement = f"SELECT Method FROM Categories WHERE ParentType='{self.parentType}'"
        raw_category_list = obtain_sql_list(category_list_statement, self.refUserDB, self.error_Logger)
        category_list = []

        for category in raw_category_list:
            category_list.append(category[0])

        # To avoid creating a duplicate value
        if category_list.count(replacement_value) > 1:
            delete_statement = f"DELETE FROM Categories WHERE Method ='{initial}' AND ParentType ='{self.parentType}'"
            specific_sql_statement(delete_statement, self.refUserDB, self.error_Logger)

        # Replaces the initial value with the replacement value
        update_statement = f"UPDATE Categories SET Method='{replacement_value}' WHERE Method='{initial}'"
        specific_sql_statement(update_statement, self.refUserDB, self.error_Logger)

        # Replace the value in all accounts associated with that parentType
        accounts_list_statement = f"SELECT Account_Name FROM {parentType_dict[self.parentType]}"
        raw_accounts_list = obtain_sql_list(accounts_list_statement, self.refUserDB, self.error_Logger)

        for account in raw_accounts_list:
            target_ledger = load_df_ledger(self.ledgerContainer, account[0])
            target_ledger.loc[(target_ledger.Category == initial), 'Category'] = replacement_value
            update_df_ledger(self.ledgerContainer,
                             account[0],
                             self.error_Logger,
                             target_ledger)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
