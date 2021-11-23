#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import sqlite3

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QObject, QThread, Signal, Slot
from PySide2.QtWidgets import QDialog
from sqlite3 import Error

from Frontend.SaveDFlUi import Ui_SaveDF

from Backend.DataFrame import empty_container, refill_container

from Toolbox.Formatting_Tools import remove_space


class SaveProgress(QDialog):
    def __init__(self, ledgerContainer, database, error_log):
        super().__init__()
        self.ui = Ui_SaveDF()
        self.ui.setupUi(self)
        # self.setModal(True)
        self.show()

        self.ledgerContainer = ledgerContainer
        self.refuserDB = database
        self.errorLog = error_log

        self.EstablishThread()

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def EstablishThread(self):
        self.processor = ProgressThread(self.ledgerContainer, self.refuserDB, self.errorLog)
        self.threadHolder = QThread()
        self.processor.moveToThread(self.threadHolder)
        self.threadHolder.started.connect(self.processor.ProcessRunner)
        self.threadHolder.start()

        self.processor.saveFinishedSignal.connect(self.FilesSaved)
        self.processor.labelSignal.connect(self.updateLabel)
        self.processor.valueSignal.connect(self.updateProgress)

    @Slot(str)
    def FilesSaved(self, status):
        if status == "Saved":
            print("Saved")
            self.close()
        else:
            print("Failed")
            pass

    @Slot(int)
    def updateProgress(self, value):
        self.ui.saveProgressBar.setValue(value)

    @Slot(str)
    def updateLabel(self, account):
        self.ui.labelActionInProgress.setText(f"In Progress of Saving:  {account}")


class ProgressThread(QObject):
    saveFinishedSignal = Signal(str)
    labelSignal = Signal(str)
    valueSignal = Signal(int)

    def __init__(self, ledgerContainer, database, error_log):
        super().__init__()
        self.connected = True

        self.ledgerContainer = ledgerContainer
        self.refuserDB = database
        self.errorLog = error_log
        self.ledger_dictionary = empty_container(self.ledgerContainer)
        self.ledger_count = len(self.ledger_dictionary)
        self.savePercentage = 0
        self.count = 0

    def ProcessRunner(self):
        while self.connected:
            try:
                conn = sqlite3.connect(self.refuserDB)
                with conn:
                    for account in self.ledger_dictionary:
                        self.labelSignal.emit(account)
                        self.count += 1
                        print(f"Saved: {self.count}/{self.ledger_count} -- [{account}]")
                        sql_tableName = remove_space(account)
                        target_DF = self.ledger_dictionary[account]

                        target_DF.to_sql(sql_tableName,
                                         conn,
                                         if_exists="replace",
                                         index=False,
                                         index_label=None)
                        self.savePercentage += (1 / self.ledger_count) * 100
                        self.valueSignal.emit(self.savePercentage)

            except Error:
                conn.close()
                error_string = f"""DataFrame_Func: df_saveto_sql \n account: "{account} \n database: {self.refuserDB}"""
                self.error_log.error(error_string, exc_info=True)
            finally:
                conn.close()

            if round(self.savePercentage) == 100 and self.count == self.ledger_count:
                self.connected = False
            else:
                self.savePercentage = 100
                self.valueSignal.emit(self.savePercentage)
                self.connected = False

        del self.ledger_dictionary
        self.saveFinishedSignal.emit("Saved")


if __name__ == "__main__":
    print("Check Executable")


