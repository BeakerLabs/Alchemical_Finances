"""
As the current file name states. This file is to execute the entire program. I will refer to it as my nexus Point
  Porcelainoffering = QDialog for User Login
  PorcelainSupplement = QDialog for Messages
  Porcelaingod = QMainWindow for the programs main hub.
"""

import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMainWindow, QDialog, QApplication, QLayout

from Backend.UserLogin import LoginForm
from Backend.WelcomeMessage import Message
from Backend.AFMainWindow import AFBackbone

# class Screen(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_Summary()
#         # self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     display = Screen()
#     display.show()
#     sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    porcelainoffering = LoginForm()
    if porcelainoffering.exec_() == QDialog.Accepted:
        user = porcelainoffering.refUser
        messageCount = porcelainoffering.count
        PorcelainSupplement = Message(messageCount, user)
        if PorcelainSupplement.exec_() == QDialog.Accepted:
            porcelaingod = AFBackbone(user, messageCount)
            porcelaingod.show()
            sys.exit(app.exec_())


