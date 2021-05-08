"""
This script is the backend to Frontend.GenReportUi.py

Future Concepts

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import os

from PySide2.QtWidgets import QDialog, QFileDialog
from PySide2 import QtCore, QtWidgets


from Frontend.GenReportUi import Ui_GenReport

from Backend.BuildReports import Generate_user_report

from StyleSheets.StandardCSS import standardAppearance

class user_report_request(QDialog):
    def __init__(self, database, user, error_log):
        super().__init__()
        self.ui = Ui_GenReport()
        self.ui.setupUi(self)
        self.setWindowTitle("Request Summary Report")
        # self.setStyleSheet(UniversalStyleSheet)
        self.setModal(True)
        self.setStyleSheet(standardAppearance)
        self.show()

        # --- Class Global Variables ------------------------------------------------------------------------------------------------------------------------------------------
        self.refUserDB = database
        self.refUser = user
        self.error_Logger = error_log

        self.widgetList = [
            self.ui.cBBank,
            self.ui.cBCash,
            self.ui.cBCD,
            self.ui.cBCC,
            self.ui.cBEquity,
            self.ui.cBRetirement,
            self.ui.cBTreasury,
            self.ui.cBDebt,
        ]

        self.parentType = {
            self.ui.cBBank: "Bank",
            self.ui.cBCash: "Cash",
            self.ui.cBCD: "CD",
            self.ui.cBEquity: "Equity",
            self.ui.cBRetirement: "Retirement",
            self.ui.cBTreasury: "Treasury",
            self.ui.cBDebt: "Debt",
            self.ui.cBCC: "Credit",

        }

        # --- Main Program ----------------------------------------------------------------------------------------------------------------------------------------------------
        self.ui.pBDeselect.clicked.connect(lambda: self.select_checkboxes(False))
        self.ui.pBSelect.clicked.connect(lambda: self.select_checkboxes(True))
        self.ui.pBGenerate.clicked.connect(lambda: self.generate_list(self.ui.lEditPath.text()))
        self.ui.pBPath.clicked.connect(self.obtain_user_dir)

        initial_dir = os.path.join(os.path.expanduser("~"), "Documents/")
        self.ui.lEditPath.setText(initial_dir)

    # --- Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # --- -- Used to Select all and Deselect all checkbox options -------------------------------------------------------------------------------------------------------------
    def select_checkboxes(self, state):
        for widget in self.widgetlist:
            widget.setChecked(state)

    # --- -- Obtain user input directory --------------------------------------------------------------------------------------------------------------------------------------
    def obtain_user_dir(self):
        dirname = QFileDialog.getExistingDirectory(self, "Chose Destination", os.getcwd(), QFileDialog.ShowDirsOnly)
        if dirname:
            self.ui.lEditPath.setText(dirname)
        else:
            dirname = os.path.join(os.path.expanduser("~"), "Documents/")
            self.ui.lEditPath.setText(dirname)

    # --- -- Used to Generate the report and open the .pdf file ---------------------------------------------------------------------------------------------------------------
    def generate_list(self, directory):
        request = []
        for widget in self.widgetList:
            if widget.checkState() == 2:
                parenType_request = [self.parentType[widget], "", ""]
                request.append(parenType_request)

        input_Data = [self.refUserDB, self.refUser, request, directory]
        Generate_user_report(input_Data, self.error_Logger)
        self.close()

    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    print("error")
