#  Copyright (c) 2022 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from pathlib import Path
from PySide6.QtWidgets import QDialog

from Frontend.ManualUi import Ui_UserManual

from StyleSheets.StandardCSS import standardAppearance


class UserManual(QDialog):
    def __init__(self, error_Log):
        super().__init__()
        self.ui = Ui_UserManual()
        self.ui.setupUi(self)

        # Global Variable for this Dialog
        self.topics_dict = {"  0. Quick Start": "0_Quick_Start.txt",
                            "  1. Welcome": "1_Welcome.txt",
                            "  2. Account Types": "2_Account_Types.txt",
                            "  3. Spending Categories": "3_Spending_Categories.txt",
                            "  4. Equities": "4_Equities.txt",
                            "  5. Ledger Functionality": "5_ledger_functionality.txt",
                            "  6. Receipt Viewer": "6_Receipt_Viewer.txt",
                            "  7. Archive": "7_Archive.txt",
                            "  8. Over Time Graphs": "8_Over_Time_Graphs.txt",
                            "  9. Equity APIs": "9_Equity_APIs.txt",
                            "  10. License": "10_License.txt",
                            "  11. User Data Ownership": "11_User_Data_Ownership.txt",}

        self.topics_lst = []

        for key in self.topics_dict:
            self.topics_lst.append(key)

        self.ui.listWidgetTopics.addItems(self.topics_lst)
        self.ui.listWidgetTopics.setCurrentRow(0)

        self.change_page()
        self.ui.listWidgetTopics.itemClicked.connect(self.change_page)

        # Button
        self.ui.pBClose.clicked.connect(self.close)

        # Program Error Log
        self.error_log = error_Log

        self.setStyleSheet(standardAppearance)
        self.show()

    def change_page(self):
        current_page = self.ui.listWidgetTopics.currentItem().text()
        target_file = self.topics_dict[current_page]

        self.ui.textEditDisplay.clear()

        page_pathway = Path.cwd() / "Resources" / "Manual" / target_file
        f = open(page_pathway, "r")
        pageText = f.read()
        f.close()

        self.ui.textEditDisplay.setText(pageText)
        self.ui.textEditDisplay.toHtml()
        self.ui.textEditDisplay.setReadOnly(True)
        self.ui.textEditDisplay.setContentsMargins(10, 0, 10, 0)

    def close_manual(self):
        self.close()



if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")