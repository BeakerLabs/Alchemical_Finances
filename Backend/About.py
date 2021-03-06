#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import sys
import os

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QDialog

from Frontend.AboutUI import Ui_AboutScreen

from StyleSheets.StandardCSS import standardAppearance


class AboutProgram(QDialog):
    remove_tab_about = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_AboutScreen()
        self.ui.setupUi(self)
        self.setWindowTitle("About Page")
        self.setStyleSheet(standardAppearance)
        self.show()

    def trigger_del_tab(self):
        self.remove_tab_about.emit("About")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")

