"""
This script is the backend to Frontend.ToggleCategoriesUi.py

Future Concepts
1)

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

from Frontend.ToggleCategoriesUi import Ui_ToggleCategories

from PySide2.QtWidgets import QDialog, QApplication

from Toolbox.AF_Tools import fill_widget
from Toolbox.SQL_Tools import specific_sql_statement


class Toggle_Categories(QDialog):
    def __init__(self, dbName, parentType, error_log):
        super().__init__()
        self.ui = Ui_ToggleCategories()
        self.ui.setupUi(self)
        self.setModal(True)

        self.refuserDB = dbName
        self.parentType = parentType

        # Program Error Logger
        self.error_Logger = error_log

        active_statement = f"SELECT Method FROM Categories WHERE ParentType='{self.parentType}' AND Tabulate='True'"
        fill_widget(self.ui.listWidgetActive, active_statement, True, self.refuserDB, self.error_Logger)
        self.ui.listWidgetActive.setCurrentRow(0)

        deactivated_statement = f"SELECT Method FROM Categories WHERE ParentType='{self.parentType}' AND Tabulate='False'"
        fill_widget(self.ui.listWidgetDeactivated, deactivated_statement, True, self.refuserDB, self.error_Logger)
        self.ui.listWidgetDeactivated.setCurrentRow(0)

        self.ui.pBToggleOn.clicked.connect(lambda: self.Toggle(True))
        self.ui.pBToggleOff.clicked.connect(lambda: self.Toggle(False))
        self.ui.pBSave.setEnabled(False)
        self.ui.pBSave.clicked.connect(self.SaveToggle)
        self.ui.pBClose.clicked.connect(self.closeDialog)

    def closeDialog(self):
        self.close()

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def SaveToggle(self):
        active_list = []
        [active_list.append(self.ui.listWidgetActive.item(x).text()) for x in range(self.ui.listWidgetActive.count())]
        deactivated_list = []
        [deactivated_list.append(self.ui.listWidgetDeactivated.item(x).text()) for x in range(self.ui.listWidgetDeactivated.count())]

        for category in active_list:
            if len(active_list) == 0:
                pass
            else:
                toggle_on_statement = f"UPDATE Categories SET Tabulate='True' WHERE METHOD='{category}' and ParentType='{self.parentType}'"
                specific_sql_statement(toggle_on_statement, self.refuserDB, self.error_Logger)

        for category in deactivated_list:
            if len(deactivated_list) == 0:
                pass
            else:
                toggle_off_statement = f"UPDATE Categories SET Tabulate='False' WHERE METHOD='{category}' and ParentType='{self.parentType}'"
                specific_sql_statement(toggle_off_statement, self.refuserDB, self.error_Logger)

        self.ui.pBSave.setEnabled(False)

    def Toggle(self, toggle):
        if toggle is True:
            row = self.ui.listWidgetDeactivated.currentRow()
            text = self.ui.listWidgetDeactivated.item(row).text()
            self.ui.listWidgetActive.addItem(text)
            self.ui.listWidgetDeactivated.takeItem(row)
            self.ui.pBSave.setEnabled(True)
        elif toggle is False:
            row = self.ui.listWidgetActive.currentRow()
            text = self.ui.listWidgetActive.item(row).text()
            self.ui.listWidgetDeactivated.addItem(text)
            self.ui.listWidgetActive.takeItem(row)
            self.ui.pBSave.setEnabled(True)


if __name__ == "__main__":
    print("error")