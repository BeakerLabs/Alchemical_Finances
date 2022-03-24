#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from PySide6.QtWidgets import QDialog, QInputDialog

from Frontend.SubTypeQuestionUi import Ui_YNCInput

from StyleSheets.StandardCSS import standardAppearance

from Toolbox.SQL_Tools import obtain_sql_list, specific_sql_statement


class YNTypeQuestion(QDialog):
    def __init__(self, database, parentType, error_log):
        super().__init__()
        self.ui = Ui_YNCInput()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.parentType = parentType

        self.setModal(True)
        self.setStyleSheet(standardAppearance)
        self.show()

        # Program Error Logger
        self.error_Logger = error_log

        self.ui.InputLabel.setText(f"How would you like to modify the available types of {self.parentType} accounts?\n\n [Do not feel restricted to standard conventions]")
        self.ui.pBAdd.clicked.connect(lambda: self.addType("AccountSubType"))
        self.ui.pBRemove.clicked.connect(lambda: self.removeType("SubType", "AccountSubType", "ParentType"))
        self.ui.pBCancel.clicked.connect(self.close)

    def addType(self, tableName):
        questionType, ok = QInputDialog.getText(self, "Add", "Enter Account Type:")
        if ok and questionType != "":
            addStatement = f"INSERT INTO {tableName} VALUES('{questionType}', '{self.parentType}')"
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

        questionType, ok = QInputDialog.getItem(self, "Remove", "Choose Account Type: ", typeList, 0, False)
        if ok and questionType:
            deleteStatement = f"DELETE FROM {tablename} WHERE {colone}='{questionType}' and {coltwo}='{self.parentType}'"
            specific_sql_statement(deleteStatement, self.refUserDB, self.error_Logger)
        else:
            pass


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
