"""
This script is the backend to Frontend.OverTimeGraphUi.py

Future Concepts


"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import numpy as np

from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QDialog, QVBoxLayout
from PySide2.QtGui import QPainter, QColor


from Backend.BuildGraphs import AF_Canvas, overTimeLineGraph
from Toolbox.AF_Tools import fill_widget
from Toolbox.Formatting_Tools import add_space, cash_format, remove_space
from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value
from Frontend.OverTimeGraphUi import Ui_OverTimeGraph


class OverTimeGraph(QDialog):
    remove_tab_OTG = QtCore.Signal(str)

    def __init__(self, parent, database, error_log):
        super().__init__(parent)
        self.ui = Ui_OverTimeGraph()
        self.ui.setupUi(self)
        self.refUserDB = database

        # Program Error Logger
        self.error_Logger = error_log

        self.lgraphCanvas = AF_Canvas(self, width=5, height=4, dpi=400)
        self.lgLayout = QVBoxLayout(self.ui.nWFrame)
        self.lgLayout.addWidget(self.lgraphCanvas)

        self.ui.graphAccountComboBox.addItem("Net Worth Graph")
        account_statement = "SELECT ID FROM Account_Summary"
        fill_widget(self.ui.graphAccountComboBox, account_statement, True, self.refUserDB)

        self.generate_graph()
        self.ui.graphAccountComboBox.currentIndexChanged.connect(self.generate_graph)
        self.show()

    def generate_graph(self):
        account = self.ui.graphAccountComboBox.currentText()
        self.ui.lGraphTitle.setText(f"{account} over Time")
        account = remove_space(account)
        self.update_lg_plot(self.lgraphCanvas, account)

        parentType_statement = f"SELECT ParentType FROM Account_Summary WHERE ID='{add_space(account)}'"
        parentType_raw = obtain_sql_value(parentType_statement, self.refUserDB, self.error_Logger)
        if parentType_raw is None:
            parentType = None
        else:
            parentType = parentType_raw[0]

        self.drawRectangle(parentType)

        if account == "Net_Worth_Graph":
            self.peakvalues = self.obtainPeakValues(account)
            # obtaining dates & value for peak Gross and Net Worth

            self.ui.lPGWorth.setText(f"Peak Gross Worth of {self.peakvalues[0][1]} on {self.peakvalues[0][0]}")
            self.ui.lLGWorth.setText(f"Low Gross Worth of {self.peakvalues[0][3]} on {self.peakvalues[0][2]}")
            self.ui.lPNWorth.setText(f"Peak Net Worth of {self.peakvalues[1][1]} on {self.peakvalues[1][0]}")
            self.ui.lLNWorth.setText(f"Low Net Worth of {self.peakvalues[1][3]} on {self.peakvalues[1][2]}")
            self.ui.lPLWorth.setText(f"Peak Liabilities Worth of {self.peakvalues[2][1]} on {self.peakvalues[2][0]}")
            self.ui.lLLWorth.setText(f"Low Liabilities Worth of {self.peakvalues[2][3]} on {self.peakvalues[2][2]}")

        elif account != "":
            self.peakvalues = self.obtainPeakValues(account)
            # obtaining dates & value for peak Gross and Net Worth

            self.ui.lPGWorth.setText(f"Peak Account Worth of{self.peakvalues[0][1]}on {self.peakvalues[0][0]}")
            self.ui.lLGWorth.setText(f"Low Account Worth of{self.peakvalues[0][3]}on {self.peakvalues[0][2]}")
            self.ui.lPNWorth.setHidden(True)
            self.ui.lLNWorth.setHidden(True)
            self.ui.lPLWorth.setHidden(True)
            self.ui.lLLWorth.setHidden(True)

        else:
            print("test")
            pass

    def update_lg_plot(self, canvas, account):
        parentType_statement = f"SELECT ParentType FROM Account_Summary WHERE ID='{add_space(account)}'"
        parentType_raw = obtain_sql_value(parentType_statement, self.refUserDB, self.error_Logger)
        if parentType_raw is None:
            parentType = None
        else:
            parentType = parentType_raw[0]

        lg_data = overTimeLineGraph(database=self.refUserDB, account=account, error_log=self.error_Logger)

        # [X-axis, Y1-axis = gross, Y2-axis = liability, Y3-axis = net, x-interval, y_interval, y-max, y-axis units, y1-Fill, y2-Fill, y3-Fill]
        canvas.axes.clear()
        if account == "Net_Worth_Graph":
            canvas.axes.plot(lg_data[0], lg_data[1], color='#000000', linewidth=0)  # Gross
            canvas.axes.plot(lg_data[0], lg_data[3], color='#000000', linewidth=0)  # Net
            canvas.axes.plot(lg_data[0], lg_data[2], color='#d73838', linewidth=0.35, linestyle='--')  # Liability

            canvas.axes.fill_between(lg_data[0], lg_data[8], lg_data[3], color='#275929')  # Gross-Net
            canvas.axes.fill_between(lg_data[0], lg_data[10], 0, color='#38803B')  # Net-0
            canvas.axes.fill_between(lg_data[0], lg_data[9], y2=0, color=(128/255, 56/255, 56/255, 150/255))  # Liability-O

        elif account != "Net_Worth_Graph" and parentType not in ["Equity", "Retirement"]:
            canvas.axes.plot(lg_data[0], lg_data[1], color='#000000', linewidth=0)  # Account Worth
            canvas.axes.fill_between(lg_data[0], lg_data[8], y2=0, color='#275929')  # Account Worth - 0

        elif account != "Net_Worth_Graph" and parentType in ["Equity", "Retirement"]:
            canvas.axes.plot(lg_data[0], lg_data[2], color='#10ad32', linewidth=0.35, linestyle='--')  # Contribution
            canvas.axes.fill_between(lg_data[0], lg_data[9], y2=0, color=(16/255, 173/255, 50/255, 175/255))
            canvas.axes.plot(lg_data[0], lg_data[1], color='#000000', linewidth=0)  # Account Worth
            canvas.axes.fill_between(lg_data[0], lg_data[8], y2=0, color='#275929')  # Account Worth - 0

        else:
            pass

        x_points = np.arange(0, len(lg_data[0]), lg_data[4])
        x_labels = [lg_data[0][x] for x in x_points]
        canvas.axes.set_xticks(x_points)
        canvas.axes.set_xticklabels(x_labels, ha='left')
        canvas.axes.set_yticks(np.arange(0, lg_data[6] + 10, lg_data[5]))

        canvas.axes.minorticks_on()
        canvas.axes.tick_params(axis='y', which='major', labelsize='3', grid_alpha=1, width=0.35)
        canvas.axes.tick_params(axis='y', which='minor', width=0.2)
        canvas.axes.tick_params(axis='x', which='major', labelsize='3', pad=2.0, width=0.35)
        canvas.axes.tick_params(axis='x', which='minor', bottom=False, width=0.2)

        canvas.axes.set_ylim(bottom=0)
        canvas.axes.set_xlim(left=0, right=len(lg_data[0]))
        canvas.axes.set_xlabel('Date (MM/DD/YY) ', labelpad=3, size='3')
        canvas.axes.set_ylabel(f'$ ({lg_data[7]})', labelpad=3, size='3')

        canvas.axes.grid(b=True,
                         which='major',
                         axis='y',
                         color='0.10',
                         linestyle='-',
                         linewidth='0.4')

        canvas.axes.grid(b=True,
                         which='minor',
                         axis='y',
                         color='0.35',
                         linestyle='-',
                         linewidth='0.2')

        pos = [0.11, 0.15, 0.85, 0.80]
        canvas.axes.set_position(pos, which='both')
        canvas.draw()

    def drawRectangle(self, parentType):
        if self.ui.graphAccountComboBox.currentText() == "Net Worth Graph":
            self.ui.lGrossLegend.setHidden(False)
            self.ui.lGrossValue.setHidden(False)
            self.ui.lGrossValue.setText("Gross Worth")
            self.ui.lNetLegend.setHidden(False)
            self.ui.lNetValue.setHidden(False)
            self.ui.lLiabilitiesLegend.setHidden(False)
            self.ui.lLiabilitiesValue.setHidden(False)
            self.ui.lLiabilitiesLegend.setStyleSheet("background: rgb(128, 56, 56)")
        elif self.ui.graphAccountComboBox.currentText() != "Net Worth Graph" and parentType not in ["Equity", "Retirement"]:
            self.ui.lGrossLegend.setHidden(False)
            self.ui.lGrossValue.setHidden(False)
            self.ui.lGrossValue.setText("Account Value")
            self.ui.lNetLegend.setHidden(True)
            self.ui.lNetValue.setHidden(True)
            self.ui.lLiabilitiesLegend.setHidden(True)
            self.ui.lLiabilitiesValue.setHidden(True)
        elif self.ui.graphAccountComboBox.currentText() != "Net Worth Graph" and parentType in ["Equity", "Retirement"]:
            self.ui.lGrossLegend.setHidden(False)
            self.ui.lGrossValue.setHidden(False)
            self.ui.lGrossValue.setText("Account Value")
            self.ui.lNetLegend.setHidden(True)
            self.ui.lNetValue.setHidden(True)
            self.ui.lLiabilitiesLegend.setHidden(False)
            self.ui.lLiabilitiesValue.setHidden(False)
            self.ui.lLiabilitiesValue.setText("Contribution Level")
            self.ui.lLiabilitiesLegend.setStyleSheet("background: rgb(16, 173, 50)")

    def obtainPeakValues(self, account):
        from datetime import datetime
        if account == "Net_Worth_Graph":
            statement = "SELECT * FROM NetWorth"
            # Date, Gross, Liabilities, Net
            row = obtain_sql_list(statement, self.refUserDB, self.error_Logger)
        else:
            statement = f"SELECT Date, {account} FROM AccountWorth ORDER BY DATE ASC Limit 0, 49999"
            row = obtain_sql_list(statement, self.refUserDB, self.error_Logger)

        # Gross peak format will be used as the Account Value from Account Worth
        row.sort(key=lambda tup: (tup[1], tup[0]), reverse=True)
        grosspeakdate = datetime.strptime(row[0][0], "%Y/%m/%d")
        grosspeakdate = str(grosspeakdate.strftime("%m/%d/%Y"))

        grosspeakformat = cash_format(float(row[0][1]), 2)

        grossmindate = datetime.strptime((row[-1][0]), "%Y/%m/%d")
        grossmindate = str(grossmindate.strftime("%m/%d/%Y"))

        grossminformat = cash_format(float(row[-1][1]), 2)
        gross = [grosspeakdate, str(grosspeakformat[2]), grossmindate, str(grossminformat[2])]

        if account == "Net_Worth_Graph":
            row.sort(key=lambda tup: (tup[3], tup[0]), reverse=True)
            netpeakdate = datetime.strptime(row[0][0], "%Y/%m/%d")
            netpeakdate = str(netpeakdate.strftime("%m/%d/%Y"))

            netpeakformat = cash_format(float(row[0][3]), 2)

            netmindate = datetime.strptime((row[-1][0]), "%Y/%m/%d")
            netmindate = str(netmindate.strftime("%m/%d/%Y"))

            netminformat = cash_format(float(row[-1][3]), 2)
            net = [netpeakdate, str(netpeakformat[2]), netmindate, str(netminformat[2])]

            row.sort(key=lambda tup: (tup[2], tup[0]), reverse=True)
            liabilitypeakdate = datetime.strptime(row[0][0], "%Y/%m/%d")
            liabilitypeakdate = str(liabilitypeakdate.strftime("%m/%d/%Y"))

            liabilitypeakformat = cash_format(float(row[0][2]), 2)

            row.sort(key=lambda tup: (tup[2], tup[0]), reverse=False)
            liabilitymindate = datetime.strptime(row[0][0], "%Y/%m/%d")
            liabilitymindate = str(liabilitymindate.strftime("%m/%d/%Y"))

            liabilityminformat = cash_format(float(row[0][2]), 2)
            liability = [liabilitypeakdate, str(liabilitypeakformat[2]), liabilitymindate, str(liabilityminformat[2])]
        else:
            net = 0
            liability = 0

        peakdata = (gross, net, liability)
        return peakdata

    def trigger_del_tab(self):
        self.remove_tab_OTG.emit("OTG")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    print("error")
