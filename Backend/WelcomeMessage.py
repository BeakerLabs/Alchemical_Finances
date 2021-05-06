"""
This script is the backend to Frontend.WelcomeMessageUi.py

Future Concepts
1) Ability to disable the Welcome Message after reading the "last message"
"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import pickle

from pathlib import Path
from Frontend.WelcomeMessageUi import Ui_WelcomeMessage

from PySide6.QtWidgets import QDialog

from Toolbox.OS_Tools import file_destination
from Toolbox.SQL_Tools import obtain_sql_value, specific_sql_statement

from StyleSheets.StandardCSS import standardAppearance
from StyleSheets.WelcomeCSS import welcomeMesgFrame


class Message(QDialog):
    def __init__(self, messageCount, user, error_Log):
        super().__init__()
        self.ui = Ui_WelcomeMessage()
        self.ui.setupUi(self)

        # Global Variable for this Dialog
        self.userCount = messageCount
        self.refuser = user
        self.userName = None
        self.dbPathway = file_destination(['data', 'account'])
        self.dbPathway = Path.cwd() / self.dbPathway / "UAInformation.db"

        self.dictionaryFile = open("Resources/welcomedictionary.pkl", "rb")
        self.messageDict = pickle.load(self.dictionaryFile)
        self.dictionaryFile.close()

        # Program Error Log
        self.error_log = error_Log

        # Button Functionality
        self.ui.pushButtonNext.clicked.connect(self.disp_next_message)
        self.ui.pushButtonClose.clicked.connect(self.close_message)

        # Obtain User Name if exists
        name_statement = f"SELECT FirstName || ' ' || LastName FROM Users"
        name_raw = obtain_sql_value(name_statement, self.dbPathway, self.error_log)
        self.userName = name_raw[0]

        if self.userName is None:
            username = self.refuser
        else:
            username = self.userName

        # Set Appearance
        self.ui.labelWelcome.setText(f"{self.messageDict[self.userCount][0]} {username},")
        self.ui.messageLabel.setText(self.messageDict[self.userCount][1])

        if self.userCount == len(self.messageDict) - 1:
            self.ui.pushButtonNext.setHidden(True)
            self.ui.pushButtonNext.setEnabled(False)

        self.setStyleSheet(standardAppearance)
        self.ui.scrollFrame.setStyleSheet(welcomeMesgFrame)
        self.ui.messageScroll.setStyleSheet(welcomeMesgFrame)
        self.show()

    def disp_next_message(self):
        self.refresh_count(self.refuser)
        self.ui.labelWelcome.setText(f"{self.messageDict[self.userCount][0]} {self.refuser.capitalize()},")
        self.ui.messageLabel.setText(self.messageDict[self.userCount][1] * 100)

        if self.userCount == len(self.messageDict) - 1:
            self.ui.pushButtonNext.setHidden(True)
            self.ui.pushButtonNext.setEnabled(False)

    def close_message(self):
        self.accept()

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def refresh_count(self, user):
        """ This function refreshes and increases the message count. Future Proofing for new messages"""
        refreshStatement = f"SELECT Message FROM Users WHERE Profile='{self.refuser}'"
        newCount = obtain_sql_value(refreshStatement, self.dbPathway, self.error_Logger)
        self.userCount = newCount[0]
        nextCount = int(self.userCount) + 1

        if nextCount in self.messageDict:
            updateStatement = f"UPDATE Users Set Message = {str(nextCount)} WHERE Profile= '{self.refuser}'"
            specific_sql_statement(updateStatement, self.dbPathway, self.error_Logger)


if __name__ == "__main__":
    print("error")
