"""
This script is the backend to Frontend.SubTypeQuestionUi.py

Future Concepts

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QInputDialog

from Frontend.SubTypeQuestionUi import Ui_YNCInput

from Toolbox.SQL_Tools import obtain_sql_list, specific_sql_statement


class YNTypeQuestion(QDialog):
    def __init__(self, database, parentType, error_log):
        super().__init__()
        self.ui = Ui_YNCInput()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.parentType = parentType

        self.setModal(True)
        self.show()

        # Program Error Logger
        self.error_Logger = error_log

        self.ui.InputLabel.setText(f"How would you like to modify the available types of {self.parentType} accounts?\n\n [Do not feel restricted to standard conventions]")
        self.ui.pBAdd.clicked.connect(lambda: self.addType("AccountSubType"))
        self.ui.pBRemove.clicked.connect(lambda: self.removeType("SubType", "AccountSubType", "ParentType"))
        self.ui.pBCancel.clicked.connect(self.close)

    def addType(self, tableName):
        type, ok = QInputDialog.getText(self, "Add", "Enter Account Type:")
        if ok and type != "":
            addStatement = f"INSERT INTO {tableName} VALUES('{type}', '{self.parentType}')"
            specific_sql_statement(addStatement, self.refUserDB, self.error_Logger)
        else:
            # canceled and not submitted
            pass

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def removeType(self, colone, tablename, coltwo):
        typeStatement = f"SELECT {colone} FROM {tablename} WHERE {coltwo}='{self.parentType}'"
        typeTuple = obtain_sql_list(typeStatement, self.refUserDB, self.error_Logger)
        typeList = []
        for account in typeTuple:
            typeList.append(account[0])
        typeList.sort()

        type, ok = QInputDialog.getItem(self, "Remove", "Choose Account Type: ", typeList, 0, False)
        if ok and type:
            deleteStatement = f"DELETE FROM {tablename} WHERE {colone}='{type}' and {coltwo}='{self.parentType}'"
            specific_sql_statement(deleteStatement, self.refUserDB, self.error_Logger)
        else:
            pass


if __name__ == "__main__":
    print("error")
