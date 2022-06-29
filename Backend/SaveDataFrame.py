#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sqlite3
import shutil
import sys
import time

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QDialog
from sqlite3 import Error

from Frontend.SaveDFlUi import Ui_SaveDF

from Backend.DataFrame import empty_container

from Toolbox.Formatting_Tools import remove_space
from Toolbox.OS_Tools import file_destination, obtain_storage_dir
from Toolbox.SQL_Tools import obtain_sql_list


class SaveProgress(QDialog):
    def __init__(self, refUser, ledgerContainer, database, error_log):
        super().__init__()
        self.ui = Ui_SaveDF()
        self.ui.setupUi(self)
        # self.setModal(True)
        self.show()

        self.refUser = refUser
        self.ledgerContainer = ledgerContainer
        self.refuserDB = database
        self.errorLog = error_log

        self.EstablishThread()

    def closeEvent(self, event):
        event.ignore()
        self.accept()

    def EstablishThread(self):
        self.processor = ProgressThread(self.refUser, self.ledgerContainer, self.refuserDB, self.errorLog)
        self.threadHolder = QThread()
        self.processor.moveToThread(self.threadHolder)
        self.threadHolder.started.connect(self.processor.ProcessRunner)
        self.threadHolder.start()

        self.processor.saveFinishedSignal.connect(self.FilesSaved)
        self.processor.labelSignal.connect(self.updateLabel)
        self.processor.valueSignal.connect(self.updateProgress)

        self.threadHolder.quit()

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

    def __init__(self, refUser, ledgerContainer, database, error_log):
        super().__init__()
        self.connected = True

        self.refUser = refUser
        self.ledgerContainer = ledgerContainer
        self.refuserDB = database
        self.errorLog = error_log
        self.storage_dir = obtain_storage_dir()
        self.ledger_dictionary = empty_container(self.ledgerContainer)
        self.ledger_count = len(self.ledger_dictionary)
        self.savePercentage = 0
        self.count = 0

    def ProcessRunner(self):
        while self.connected:
            self.delete_account_receipts()
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
                        time.sleep(0.1)
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

    def delete_account_receipts(self):
        info_statement = f"SELECT ID, ParentType FROM DeletePending"
        account_info_tpl = obtain_sql_list(info_statement, self.refuserDB, self.errorLog)
        del_count = 0
        del_total = len(account_info_tpl)

        if del_total > 0:
            for account in account_info_tpl:
                del_count += 1
                sql_accountName = remove_space(account[0])
                parentType = account[1]
                obsolete_dir_path = file_destination(['Alchemical Finances', 'Receipts', self.refUser, {parentType}, sql_accountName], starting_point=self.storage_dir)
                obsolete_dir_str = str(obsolete_dir_path)
                try:
                    shutil.rmtree(obsolete_dir_str)
                    print(f"Deleted: {del_count}/{del_total} -- [{account[0]}]")
                except OSError:
                    error_string = f"Window's Denied Deletion Action. Manual action required once program is closed.\n"
                    self.errorLog.error(error_string, exc_info=True)
        else:
            print("Deleted: 0/0 -- [No Accounts Found]")

if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
