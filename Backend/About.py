"""
This script is the backend to Frontend.AboutUi.py

Due to the "static" nature of the tab. Anything kinetic can be done in the Frontend. 

"""

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QDialog

from Frontend.AboutUI import Ui_AboutScreen


class AboutProgram(QDialog):
    remove_tab_about = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_AboutScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("About Page")

        # Place style sheet here
        self.show()

    def trigger_del_tab(self):
        self.remove_tab_about.emit("About")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")


