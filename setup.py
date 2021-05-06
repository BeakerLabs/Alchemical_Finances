"""
As the current file name states. This file is to execute the entire program. I will refer to it as my nexus Point
  Porcelainoffering = QDialog for User Login
  PorcelainSupplement = QDialog for Messages
  Porcelaingod = QMainWindow for the programs main hub.
"""
#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import os
import pickle
import sys

from pathlib import Path
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QDialog, QApplication

from Backend.UserLogin import LoginForm
from Backend.WelcomeMessage import Message
from Backend.AFMainWindow import AFBackbone

from Toolbox.Logging_System import create_log_fileName, get_logger
from Toolbox.OS_Tools import file_destination


def main():

    log_created = False
    sessionCount = 0

    while log_created is False:
        errorLog_File = create_log_fileName(sessionCount)
        errorLog_Pathway = file_destination(['Data', 'Error_Log'])
        errorLog_Pathway = Path.cwd() / errorLog_Pathway / errorLog_File

        if not errorLog_Pathway.exists():
            log_created = True

        else:
            f = open(errorLog_Pathway, "r")
            if len(f.readlines()) < 1:
                f.close()
                os.remove(errorLog_Pathway)
                log_created = True
            else:
                f.close()
                sessionCount += 1

    errorLog_Pathway = str(errorLog_Pathway)
    error_Log = get_logger("AF_ERROR_LOG", errorLog_Pathway)

    app = QApplication(sys.argv)

    screen_dimensions_path = file_destination(['Resources'])
    screen_dimensions_path = Path.cwd() / screen_dimensions_path / "dimensions.pkl"

    f = open(screen_dimensions_path, "wb")
    screen = app.primaryScreen()
    size = screen.size()
    dimensions = [0, 0, size.width(), size.height()]
    pickle.dump(dimensions, f)
    f.close()

    porcelainoffering = LoginForm(error_Log)
    if porcelainoffering.exec_() == QDialog.Accepted:
        user = porcelainoffering.refUser
        messageCount = porcelainoffering.count
        error_Log = porcelainoffering.error_Logger
        PorcelainSupplement = Message(messageCount, user, error_Log)
        if PorcelainSupplement.exec_() == QDialog.Accepted:
            porcelaingod = AFBackbone(user, messageCount, error_Log)
            porcelaingod.show()
            sys.exit(app.exec_())


if __name__ == "__main__":
    main()


