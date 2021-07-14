#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import time

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QObject, QThread, Signal, Slot
from PySide2.QtWidgets import QDialog, QApplication

from Frontend.SaveDFlUi import Ui_SaveDF

from Backend.DataFrame import empty_container, df_saveto_sql


class SaveProgress(QDialog):
    def __init__(self, ledgerContainer, database, error_log):
        super().__init__()
        self.ui = Ui_SaveDF()
        self.ui.setupUi(self)
        self.setModal(True)
        self.show()

        self.ledgerContainer = ledgerContainer
        self.refuserDB = database
        self.errorLog = error_log

        self.EstablishThread()

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def EstablishThread(self):
        self.Processor = ProgressThread(self.ui.labelActionInProgress, self.ui.saveProgressBar, self.ledgerContainer, self.refuserDB, self.errorLog)
        self.ThreadHolder = QThread()
        self.Processor.moveToThread(self.ThreadHolder)
        self.ThreadHolder.started.connect(self.Processor.ProcessRunner)
        self.ThreadHolder.start()

        self.Processor.saveFinishedSignal.connect(self.FilesSaved)

    @Slot(str)
    def FilesSaved(self, status):
        if status == "Saved":
            self.close()
        else:
            pass


class ProgressThread(QObject):
    saveFinishedSignal = Signal(str)

    def __init__(self, accountlabel, progressBar, ledgerContainer, database, error_log):
        super().__init__()
        self.connected = True

        self.actionLabel = accountlabel
        self.progressBar = progressBar
        self.ledgerContainer = ledgerContainer
        self.refuserDB = database
        self.errorLog = error_log
        self.ledger_dictionary = empty_container(self.ledgerContainer)
        self.ledger_count = len(self.ledger_dictionary)
        print(f"Total Ledger Count: {self.ledger_count}")
        self.savePercentage = 0
        self.count = 0

    def ProcessRunner(self):
        while self.connected:
            for account in self.ledger_dictionary:
                self.actionLabel.setText(f"In Progress of Saving:  {account}")
                saveSuccess = df_saveto_sql(account, self.ledger_dictionary[account], self.refuserDB, self.errorLog)
                if saveSuccess:
                    self.savePercentage += (1 / self.ledger_count) * 100
                    self.count += 1
                    self.progressBar.setValue(self.savePercentage)
                    print(f"Saved: {self.count}/{self.ledger_count}")
                    time.sleep(0.3)
                else:
                    print(f"Failed: {self.count}/{self.ledger_count} -- {account}")
                    time.sleep(0.3)
                    self.connected = False

            if round(self.savePercentage) == 100 and self.count == self.ledger_count:
                self.connected = False
            else:
                self.savePercentage = 100
                self.progressBar.setValue(self.savePercentage)
                time.sleep(0.3)
                self.connected = False

        self.saveFinishedSignal.emit("Saved")


if __name__ == "__main__":
    print("Check Executable")


