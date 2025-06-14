#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

# Function of this script is to clean your Receipt Repository and Database. Removing files that are not referenced
# in the database and vice versa. This script may in the future be upgraded to allow users to delete/archive older receipts
# to free up space on their system. For now it just cleans up gaps.


import os
import sqlite3

import sys
import time

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QDialog
from sqlite3 import Error

from Frontend.SaveDFlUi import Ui_SaveDF

from Backend.DataFrame import empty_container

from Toolbox.Formatting_Tools import remove_space
from Toolbox.OS_Tools import file_destination, obtain_storage_dir
from Toolbox.SQL_Tools import obtain_sql_value

class receipt_cleaner(QDialog):

    def __init__(self, refUser, ledgerContainer, database, error_log):
        super().__init__()
        self.ui = Ui_SaveDF()
        self.ui.setupUi(self)
        # self.setModal(True)
        self.show()

        self.refUser = refUser
        self.ledgerContainer = ledgerContainer
        self.refUserDB = database
        self.errorLog = error_log

        self.storage_dir = obtain_storage_dir()

        self.EstablishThread()

    def closeEvent(self,event):
        event.ignore()
        self.accept()

    def EstablishThread(self):
        self.processor = ProgressThread(self.refUser, self.ledgerContainer, self.refUserDB, self.errorLog)
        self.threadHolder = QThread()
        self.processor.moveToThread(self.threadHolder)
        self.threadHolder.started.connect(self.processor.ProcessRunner)
        self.threadHolder.start()

        self.processor.cleanFinishedSignal.connect(self.FilesCleaned)
        self.processor.labelSignal.connect(self.updateLabel)
        self.processor.valueSignal.connect(self.updateProgress)

        self.threadHolder.quit()

    @Slot(str)
    def FilesCleaned(self, status):
        if status == "Cleaned":
            print("Cleaned")
            self.close()
        else:
            print("Failed")
            pass

    @Slot(int)
    def updateProgress(self, value):
        self.ui.saveProgressBar.setValue(value)

    @Slot(str)
    def updateLabel(self, name_input):
        self.ui.labelActionInProgress.setText(f"Reviewing Receipt: {name_input}")

class ProgressThread(QObject):
    cleanFinishedSignal = Signal(str)
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
        self.percentage = 0
        self.count = 0

    def ProcessRunner(self):
        while self.connected:
            tic = time.perf_counter()
            try:
                conn = sqlite3.connect(self.refuserDB)
                with conn:
                    for account in self.ledger_dictionary:
                        self.count += 1
                        print(f"Receipt Cleaning: {self.count}/{self.ledger_count} -- [{account}]")
                        target_DF = self.ledger_dictionary[account]
                        sql_tableName = remove_space(account)

                        # Break Point from SaveDataFrame.py code.
                        parentType = self.obtain_parentType(account)
                        if parentType is not None:
                            # obtain list of file names from OS directory. Does not contain the file extension
                            receipt_directory = file_destination(['Alchemical Finances', 'Receipts', self.refUser, parentType, sql_tableName], starting_point=self.storage_dir)
                            directory_file_list = [x for x in os.listdir(receipt_directory) if os.path.isfile(os.path.join(receipt_directory, x))]
                            directory_len = len(directory_file_list)
                            directory_count = 0

                            # obtain list of file names from target Dataframe. Modified to include and exclude file extension
                            df_Receipts_list = list(target_DF['Receipt'])
                            dataframe_file_list  = [x for x in df_Receipts_list]
                            dataframe_len = len(dataframe_file_list)
                            dataframe_count = 0

                            print(f"Reviewing Directory: {directory_len} Receipts")
                            for receipt in directory_file_list:
                                self.labelSignal.emit(receipt)
                                if receipt in dataframe_file_list:
                                    print(f"Receipt File: {receipt} -- Maintained")
                                    directory_count += 1
                                else:
                                    full_receipt_path = os.path.join(receipt_directory, receipt)
                                    os.remove(full_receipt_path)
                                    print(f"Receipt File: {receipt} -- Deleted")

                                    # Potentially unnecessary catch. Incase the count doesn't match with the receipt value.
                                    if directory_file_list[directory_count] == receipt:
                                        directory_file_list.pop(directory_count)
                                    else:
                                        directory_file_list.remove(receipt)

                            time.sleep(0.1)

                            print(f"Reviewing Dataframe: {dataframe_len} Inputs")
                            for receipt in df_Receipts_list:
                                self.labelSignal.emit(2)
                                self.labelSignal[str].emit(receipt)
                                if receipt in directory_file_list:
                                    print(f"Receipt Record: {receipt} -- Maintained")
                                    dataframe_count += 1
                                else:
                                    receipt_loc = target_DF.loc[target_DF['Receipt']==receipt]
                                    receipt_row = receipt_loc.index.tolist()
                                    for row in receipt_row:
                                        target_DF.loc[row, 'Receipt'] = None
                                    print(f"Receipt Record: {receipt} -- Deleted")

                                    if dataframe_file_list[dataframe_count] == receipt:
                                        dataframe_file_list.pop(dataframe_count)
                                    else:
                                        dataframe_file_list.remove(receipt)

                            time.sleep(0.1)

                    # End Break Point from SaveDataFrame.py code.
                    time.sleep(0.1)
                    self.percentage += (1 / self.ledger_count) * 100
                    self.valueSignal.emit(self.percentage)

            except Error:
                conn.close()
                error_string = f"""Receipt Cleaner Error: \n account: "{account} \n database: {self.refuserDB}"""
                self.error_log.error(error_string, exc_info=True)
            finally:
                conn.close()

                if round(self.percentage) == 100 and self.count == self.ledger_count:
                    self.connected = False
                else:
                    self.percentage = 100
                    self.valueSignal.emit(self.percentage)
                    self.connected = False

            del self.ledger_dictionary
            toc = time.perf_counter()
            print(f'Full Receipt Cleaning took {tic - toc:0.4f} seconds')
            self.cleanFinishedSignal.emit("Cleaned")


    def obtain_parentType(self, account):
        parentType_archive = f"SELECT ParentType FROM Account_Archive WHERE ID='{account}'"
        archive_parentType = obtain_sql_value(parentType_archive, self.refuserDB, self.errorLog)
        parentType_summary  = f"SELECT ParentType FROM Account_Summary WHERE ID='{account}'"
        summary_parentType = obtain_sql_value(parentType_summary, self.refuserDB, self.errorLog)
        if archive_parentType is not None:
            parentType = archive_parentType[0]
        elif summary_parentType is not None:
            parentType = summary_parentType[0]
        else:
            parentType = None
        return parentType


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")


