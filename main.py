"""
As the current file name states. This file is to execute the entire program. I will refer to it as my nexus Point
  Porcelainoffering = QDialog for User Login
  PorcelainSupplement = QDialog for Messages
  Porcelaingod = QMainWindow for the programs main hub.
"""
#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import pickle
import sys

from pathlib import Path
from PySide6.QtWidgets import QDialog, QApplication

from Backend.UserLogin import LoginForm
from Backend.WelcomeMessage import Message
from Backend.AFMainWindow import AFBackbone

from Toolbox.Logging_System import create_log_fileName, get_logger
from Toolbox.OS_Tools import file_destination, obtain_storage_dir


def main():

    log_created = False
    errorLog_Pathway = None
    sessionCount = 0

    user_pathway = obtain_storage_dir()

    while log_created is False:
        errorLog_File = create_log_fileName(sessionCount)
        errorLog_Pathway = file_destination(dir_name_lst=['Alchemical Finances', 'data', 'Error_Log'], starting_point=user_pathway)
        errorLog_Pathway = Path(errorLog_Pathway) / errorLog_File

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
    screen_dimensions_path = screen_dimensions_path + "dimensions.pkl"
    screen_dimensions_path = Path(screen_dimensions_path)

    f = open(screen_dimensions_path, "wb")
    os.chmod(screen_dimensions_path, 0o777)
    screen = app.primaryScreen()
    size = screen.size()
    dimensions = [0, 0, size.width(), size.height()]
    pickle.dump(dimensions, f)
    f.close()

    porcelainOffering = LoginForm(error_Log)
    if porcelainOffering.exec() == QDialog.Accepted:
        user = porcelainOffering.refUser
        messageCount = porcelainOffering.count
        error_Log = porcelainOffering.error_Logger
        porcelainSupplement = Message(messageCount, user, error_Log)
        if porcelainSupplement.exec() == QDialog.Accepted:
            porcelainGod = AFBackbone(user, messageCount, error_Log)
            porcelainGod.show()
            sys.exit(app.exec())


if __name__ == "__main__":
    main()
