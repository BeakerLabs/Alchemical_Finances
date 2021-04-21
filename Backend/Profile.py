"""
This script is the backend to Frontend.ProfileUi.py

Due to the "static" nature of the tab. Anything kinetic can be done in the Frontend.

"""

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QDialog

from Frontend.ProfileUi import Ui_Profile

from StyleSheets.Standard import standardAppearance
from StyleSheets.ProfileCSS import profileFrame


class Profile(QDialog):
    remove_tab_profile = QtCore.Signal(str)

    def __init__(self, database, error_Log):
        super().__init__()
        self.ui = Ui_Profile()
        self.ui.setupUi(self)
        self.setWindowTitle("User Profile")

        self.refUserDB = database
        self.error_Logger = error_Log

        self.setStyleSheet(standardAppearance)
        self.ui.profileFrame.setStyleSheet(profileFrame)
        # Place style sheet here
        self.show()

    def trigger_del_tab(self):
        self.remove_tab_profile.emit("Profile")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")
