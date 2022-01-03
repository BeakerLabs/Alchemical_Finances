#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from datetime import datetime

from dateutil.relativedelta import relativedelta

from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtGui import QColor
from PySide2 import QtCore, QtGui

from Backend.DataFrame import update_df_balance

from Toolbox.Formatting_Tools import cash_format, convert_to_float, decimal_places, remove_space
from Toolbox.SQL_Tools import obtain_sql_value, obtain_sql_list


def disp_LedgerV1_Table(account_combobox, statement_combobox, parentType, tablewidget, activeLedger):
    """
    Function used to display a given [non equity] account in the tablewidget of Ledger1.
    Function resides in a toolbox to allow access for Ledger 1 and the Archive.
    """
    tablewidget.setRowCount(0)
    centered = [0, 3]
    ledgerName = account_combobox.currentText()
    statement_day = statement_combobox.currentText()
    pending = 0

    tablewidget.setColumnCount(11)
    tablewidget.clearContents()

    if ledgerName == "":
        pass
    else:
        if parentType != "Property":
            target_transactions = statement_range(activeLedger, statement_day, parentType)

            if len(target_transactions) == 0:
                statement_index = statement_combobox.currentIndex()
                statement_combobox.removeItem(statement_index)

        else:
            target_transactions = statement_range(activeLedger, "January 01, 2018", parentType)

        for data_point in target_transactions:
            data_point[0] = datetime.strptime(data_point[0], "%Y/%m/%d")
            data_point[0] = data_point[0].strftime("%m/%d/%Y")

            data_point = [data_point[0],   # TDate
                          data_point[1],   # TMeth
                          data_point[2],   # TDesc
                          data_point[3],   # Cat
                          (convert_to_float(data_point[5]) - convert_to_float(data_point[4])),  # (Credit - Debit)
                          data_point[6],   # Balance
                          data_point[8],   # Status
                          data_point[9],   # Receipt
                          data_point[7],   # Note
                          data_point[10],  # Post_Date
                          ]
            current_row = tablewidget.rowCount()
            tablewidget.insertRow(current_row)
            sublist = data_point[:11]

            for index, value in enumerate(sublist):
                if index in centered:
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                elif index == 4:
                    value = cash_format(value, 2)[1]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                elif index == 5:
                    disp_balance = cash_format(value, 2)[1]
                    item = QTableWidgetItem(disp_balance)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                elif index == 6:
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    if pending == 0 or pending == 2:
                        color = QColor(222, 239, 189)
                    elif pending == 1:
                        color = QColor(208, 232, 161)
                    pending = pending_row_color(value, pending)
                else:
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                tablewidget.setItem(current_row, index, QTableWidgetItem(item))
            if pending == 1 or pending == 2:
                setColortoRow(tablewidget, current_row, color)

    tablewidget.setHorizontalHeaderLabels(["Transaction Date",
                                           "Transaction Method",
                                           "Transaction Description",
                                           "Category",
                                           "Amount",
                                           "Balance",
                                           "Status",
                                           "Receipt",
                                           "Additional Notes",
                                           "Posted Date",
                                           "Updated Date"])
    tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
    table_widths = [140, 160, 250, 150, 150, 150, 150, 250, 150]
    for column in range(0, 9, 1):
        tablewidget.setColumnWidth(column, table_widths[column])
    tablewidget.setColumnHidden(9, True)
    tablewidget.setColumnHidden(10, True)
    tablewidget.resizeRowsToContents()
    tableFont = QtGui.QFont()
    tableFont.setPixelSize(12)
    tablewidget.setFont(tableFont)
    tablewidget.scrollToBottom()


def disp_LedgerV2_Table(account_combobox, statement_combobox, tablewidget, activeLedger):
    """
    Function used to display a given [equity] account in the tablewidget of Ledger1.
    Function resides in a toolbox to allow access for Ledger 2 and the Archive.
    """
    tablewidget.setRowCount(0)
    centered = [0, 2]
    ledgerName = account_combobox.currentText()
    statement_day = statement_combobox.currentText()

    pending = 0
    tablewidget.setColumnCount(11)
    tablewidget.clearContents()

    if ledgerName == "":
        pass
    else:
        target_transactions = statement_range(activeLedger, statement_day, parentType="Equity")  # Actual parentType doesn't matter

        if len(target_transactions) == 0:
            statement_index = statement_combobox.currentIndex()
            statement_combobox.removeItem(statement_index)

        for data_point in target_transactions:
            data_point[0] = datetime.strptime(data_point[0], "%Y/%m/%d")
            data_point[0] = data_point[0].strftime("%m/%d/%Y")

            data_point = [data_point[0],   # Transaction Date
                          data_point[1],   # Transaction Desc
                          data_point[2],   # Category
                          (convert_to_float(data_point[4]) - convert_to_float(data_point[3])),  # (Credit - Debit)
                          (convert_to_float(data_point[6]) - convert_to_float(data_point[5])),  # (Purchased - Sold)
                          data_point[7],   # Price
                          data_point[9],   # Status
                          data_point[10],  # Receipt
                          data_point[8],   # Note
                          data_point[11],  # Post_Date
                          ]

            current_row = tablewidget.rowCount()
            tablewidget.insertRow(current_row)
            sublist = data_point[:12]

            for index, value in enumerate(sublist):
                if index in centered:
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                elif index == 3:
                    value = cash_format(value, 2)[1]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                elif index == 4:
                    value = decimal_places(value, 4)
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                elif index == 5:
                    value = cash_format(value, 4)[1]
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                elif index == 6:
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    if pending == 0 or pending == 2:
                        color = QColor(222, 239, 189)
                    elif pending == 1:
                        color = QColor(208, 232, 161)
                    pending = pending_row_color(value, pending)
                else:
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                tablewidget.setItem(current_row, index, QTableWidgetItem(item))
            if pending == 1 or pending == 2:
                setColortoRow(tablewidget, current_row, color)
        tablewidget.setHorizontalHeaderLabels(["Transaction Date",
                                               "Transaction Description",
                                               "Category",
                                               "Amount",
                                               "Shares (+/-)",
                                               "Price/Share",
                                               "Status",
                                               "Receipt",
                                               "Additional Transaction Notes",
                                               "Posted Date",
                                               "Updated Date"])
        tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        table_widths = [140, 250, 150, 150, 150, 150, 150, 250, 150]
        for column in range(0, 9, 1):
            tablewidget.setColumnWidth(column, table_widths[column])
        tablewidget.setColumnHidden(9, True)
        tablewidget.setColumnHidden(10, True)
        tablewidget.resizeRowsToContents()
        tableFont = QtGui.QFont()
        tableFont.setPixelSize(12)
        tablewidget.setFont(tableFont)
        tablewidget.scrollToBottom()


def fill_statement_period(account, statementComboBox, ledgerStatus, database, activeLedger, error_log):
    """ Fills a target combobox with Statement periods based upon the Account Details"""
    statementComboBox.clear()
    statement_period_list = generate_statement_months(account, ledgerStatus, database, activeLedger, error_log)
    statementComboBox.addItems(statement_period_list)
    statementComboBox.setCurrentIndex(0)


def fill_widget(widget, statement: str, sorted: bool, database: str, error_log):
    """primarily used to fill QComboBox and QListWidget. Doesn't return a variable"""
    raw_comboBox_list = obtain_sql_list(statement, database, error_log)
    unsorted_comboBox_list = []

    if raw_comboBox_list is None:
        return unsorted_comboBox_list
    else:
        for combobox_item in raw_comboBox_list:
            unsorted_comboBox_list.append(combobox_item[0])

        if sorted is True:
            unsorted_comboBox_list.sort()
            sorted_comboBox_list = unsorted_comboBox_list
            widget.addItems(sorted_comboBox_list)
        else:
            widget.addItems(unsorted_comboBox_list)


def find_mult_row(tableWidget, col_num: int, string: str):
    """obtains all rows associated with a string input"""
    allrows = tableWidget.rowCount()
    rowList = []
    for row in range(allrows):
        cell = tableWidget.item(row, col_num).text()
        if cell == string:
            rowList.append(cell)
    return rowList


def find_row(tableWidget, col_num: int, string: str):
    """obtains the rwo number on the table Widget based upon a column and string."""
    allrows = tableWidget.rowCount() + 1
    for row in range(allrows):
        cell = tableWidget.item(row, col_num).text()
        if cell == string:
            return row


def generate_statement_months(account, ledgerStatus, database, activeLedger, error_log):
    """Function used to obtain and format the Statement Months from the transactions submitted into the ledger"""
    parentType_dict = {
        "Bank": "Bank_Account_Details",
        "Cash": "Cash_Account_Details",
        "CD": "CD_Account_Details",
        "Treasury": "Treasury_Account_Details",
        "Credit": "Credit_Account_Details",
        "Debt": "Debt_Account_Details",
        "Equity": "Equity_Account_Details",
        "Retirement": "Retirement_Account_Details",
        "Property": "Property_Account_Details"
    }

    active_account = account

    # obtain the account ParentType from the Database
    if ledgerStatus == "Archive":
        parentType_statement = f"SELECT ParentType FROM Account_Archive WHERE ID='{active_account}'"

    elif ledgerStatus == "Active":
        parentType_statement = f"SELECT ParentType FROM Account_Summary WHERE ID='{active_account}'"

    parentType = obtain_sql_value(parentType_statement, database, error_log)
    parentType = parentType[0]

    # obtain the Statement Date from the Database
    date_statement = f"SELECT Statement_Date FROM {parentType_dict[parentType]} WHERE Account_Name='{active_account}'"
    date_value = obtain_sql_value(date_statement, database, error_log)
    date_value = date_value[0]

    if date_value < 10:
        date_value = f"0{str(date_value)}"

    activeLedger = activeLedger.sort_values(by=['Transaction_Date', 'Update_Date'], ascending=True)
    list_of_Dates = activeLedger['Transaction_Date'].to_list()

    raw_month_list = []
    display_month_list = []

    for date in list_of_Dates:
        month_w_day = f"{date[:7]}/{date_value}"
        if month_w_day in raw_month_list:
            pass
        else:
            raw_month_list.append(month_w_day)

    raw_month_list.sort(reverse=True)

    for month in raw_month_list:
        convert_datetime = datetime.strptime(month, '%Y/%m/%d')
        increase_month = convert_datetime + relativedelta(months=+1)
        change_datetime = increase_month.strftime('%B %d, %Y')
        string_datetime = str(change_datetime)
        display_month_list.append(string_datetime)

    return display_month_list


def pending_row_color(value, pending):
    """
    Function used to help bounce between color values for a pending transaction.
    used for readability of the ledger display function.

    :param value: string
    :param pending: QColor RGB value
    :return: int
    """
    if value == "Pending" and pending == 0:
        pending = 1
    elif value == "Pending" and pending == 1:
        pending = 2
    elif value == "Pending" and pending == 2:
        pending = 1
    else:
        pending = 0
    return pending


def rename_image(accountComboBox, categoryComboBox):
    """
    generates a new file name for the uploaded receipts. Its mostly important for appearance, no real functionality
    :param accountComboBox:
    :param categoryComboBox:
    :return:
    """
    from datetime import datetime
    ledgerName = accountComboBox.currentText()
    modifiedLN = remove_space(ledgerName)
    category = categoryComboBox.currentText()
    currentDate = datetime.now().strftime("%y%j%H%M%S")
    newImageName = modifiedLN[:5] + " - " + category + " - " + currentDate
    return newImageName


def statement_range(activeLedger: object, statement_day: str, parentType: str):
    """
    Function used to filter out the transactions associated with the active statement period. This avoid a 500 transaction table.
    :param activeLedger: object
    :param statement_day: str-- (datetime.strftime('%B %d %Y'))
    :param parentType: str -- Ledger Type
    :return: list
    """
    from datetime import datetime
    convert_to_datetime = datetime.strptime(statement_day, '%B %d, %Y')
    format_datetime = convert_to_datetime.strftime("%Y/%m/%d")
    return_to_datetime = datetime.strptime(format_datetime, "%Y/%m/%d")

    if parentType == "Property":
        start_datetime = datetime.strptime("2010/01/01", "%Y/%m/%d")
        today = datetime.today() + relativedelta(days=1)
        today_str = today.strftime("%Y/%m/%d")
        end_datetime = datetime.strptime(today_str, "%Y/%m/%d")
    else:
        start_datetime = return_to_datetime + relativedelta(months=-1)
        end_datetime = return_to_datetime + relativedelta(days=-1)

    target_transactions = []

    activeLedger = update_df_balance(activeLedger)
    ledger_row_count = activeLedger.shape[0]
    ledger_row_count = int(ledger_row_count)

    for transaction_row in range(0, ledger_row_count):
        transaction = activeLedger.loc[transaction_row, :].values.tolist()
        transaction_Date = datetime.strptime(transaction[0], "%Y/%m/%d")
        if start_datetime <= transaction_Date <= end_datetime:
            target_transactions.append(transaction)
        else:
            pass

    target_transactions = sorted(target_transactions, key=lambda x: (x[0], x[11]))

    return target_transactions


def set_font(target, size: int, bold: bool, underline: bool):
    """
    function to reduce repitition and clean up the backend code.

    :param target: Pysde6 Widget
    :param size: int
    :param bold: bool
    :param underline: bool
    :return: None
    """
    target.setPixelSize(size)
    target.setBold(bold)
    target.setUnderline(underline)


def setColortoRow(tableWidget, rowIndex, color):
    """
    overly simple function to change the color of the TableWidget Row.
    Used to help with readability

    :param tableWidget: object
    :param rowIndex: int
    :param color: int
    :return:
    """
    for j in range(0, 9):
        tableWidget.item(rowIndex, j).setBackground(color)


def set_networth(database: str, error_log, tablename="Account_Summary",  toggleformatting=True):
    """
    Specialized function. Takes Balance Values from the Account Summary Table based upon the account's tablename,
    and asset/Liability.
    """
    qtyAssetStatement = f"SELECT SUM(Balance) FROM {tablename} WHERE ItemType='Asset'"
    qtyLiabilityStatement = f"SELECT SUM(Balance) FROM {tablename} WHERE ItemType='Liability'"  # AND ParentType='Debt'"
    qtyMoney = obtain_sql_value(qtyAssetStatement, database, error_log)
    if qtyMoney[0] is None:
        qtyMoney = "0.00"
    else:
        qtyMoney = qtyMoney[0]

    qtyDebt = obtain_sql_value(qtyLiabilityStatement, database, error_log)
    if qtyDebt[0] is None:
        qtyDebt = "0.00"
    else:
        qtyDebt = qtyDebt[0]

    decimal_assets = decimal_places(qtyMoney, 2)
    decimal_debt = decimal_places(qtyDebt, 2)
    netMoney = decimal_assets - decimal_debt

    string_assets = cash_format(decimal_assets, 2)
    string_debt = cash_format(decimal_debt, 2)
    string_net = cash_format(netMoney, 2)

    if toggleformatting is True:
        moneyList = [string_net[0], string_net[1], string_assets[1], string_debt[1]]
    elif toggleformatting is False:
        moneyList = [string_assets[0], string_debt[0], string_net[0]]
    else:
        moneyList = ["0.00", "0.00", "0.00", "0.00"]

    return moneyList


# def update_ledger_balance(comboBox, database, error_log):
#     """
#     Function used to adjust the ledger balance amounts whenever a transaction is added, deleted, or updated. This will maintain correct
#     balance values based upon the "order of transaction"
#     """
#     active_ledger = comboBox.currentText()
#     sql_active_ledger = remove_space(active_ledger)
#
#     running_balance = 0
#
#     rowID_Statement = f"SELECT ROWID, Credit - Debit, Balance FROM '{sql_active_ledger}' Order by Transaction_Date Limit 0, 49999"
#     rowID_list = obtain_sql_list(rowID_Statement, database, error_log)
#
#     for rowID in rowID_list:
#         row = rowID[0]
#         CreditDebit = rowID[1]
#         trans_balance_ledger = rowID[2]
#         trans_balance_calc = running_balance + CreditDebit
#         trans_balance_calc = decimal_places(trans_balance_calc, 2)
#
#         if trans_balance_calc == trans_balance_ledger:
#             pass
#         else:
#             update_balance = f"UPDATE '{sql_active_ledger}' SET Balance='{trans_balance_calc}' WHERE ROWID='{row}'"
#             specific_sql_statement(update_balance, database, error_log)
#
#         running_balance = float(trans_balance_calc)


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
