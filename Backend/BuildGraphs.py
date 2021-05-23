"""
This script is the backend to all graphical displays

Future Concepts
1)

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os

import matplotlib.pyplot as plt
import numpy as np

from math import ceil
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Toolbox.Formatting_Tools import add_space, cash_format, decimal_places
from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value


class AF_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, facecolor="#FAFAFA"):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=facecolor)
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#e3e3e3')
        self.axes.spines[["top", "bottom", "left", "right"]].set_linewidth(0.5)
        super(AF_Canvas, self).__init__(fig)


def overTimeLineGraph(database, account, error_log):
    parentType_statement = f"SELECT ParentType FROM Account_Summary WHERE ID='{add_space(account)}'"
    parentType_raw = obtain_sql_value(parentType_statement, database, error_log)
    if parentType_raw is None:
        parentType = None
    else:
        parentType = parentType_raw[0]

    # SQL raw data acquisition
    if account == "Net_Worth_Graph":
        combined_data_statement = "SELECT Date, Gross, Liabilities, Net FROM NetWorth ORDER BY Date ASC LIMIT 0, 49999"
        combined_data_tuple = obtain_sql_list(combined_data_statement, database, error_log)

        largest_grossValue_raw = []
        largest_liabilityValue_raw = []

        for value in combined_data_tuple:
            largest_grossValue_raw.append(int(float(value[1])))
            largest_liabilityValue_raw.append(int(float(value[2])))

        largest_grossValue = max(largest_grossValue_raw)
        largest_liabilityValue = max(largest_liabilityValue_raw)

        if largest_grossValue >= largest_liabilityValue:
            largest_y_value = largest_grossValue
        else:
            largest_y_value = largest_liabilityValue

    elif account != "Net_Worth_Graph" and parentType in ["Equity", "Retirement"]:
        value_data_statement = f"SELECT Date, {account} FROM AccountWorth ORDER BY Date ASC Limit 0, 49999"
        value_data_tuple = obtain_sql_list(value_data_statement, database, error_log)
        contribution_data_statement = f"SELECT Date, {account} FROM ContributionTotals ORDER BY Date ASC Limit 0, 49999"
        contribution_tuple = obtain_sql_list(contribution_data_statement, database, error_log)

        combined_data_tuple = []
        x = 0
        for value in value_data_tuple:
            contribution = contribution_tuple[x][1]
            tuple = (value[0], value[1], contribution)
            combined_data_tuple.append(tuple)
            x += 1

        largest_grossValue_raw = []
        largest_ContributionValue_raw = []

        for value in combined_data_tuple:
            largest_grossValue_raw.append(int(float(value[1])))
            largest_ContributionValue_raw.append(int(float(value[2])))

        largest_grossValue = max(largest_grossValue_raw)
        largest_ContributionValue = max(largest_ContributionValue_raw)

        if largest_grossValue >= largest_ContributionValue:
            largest_y_value = largest_grossValue
        else:
            largest_y_value = largest_ContributionValue

    else:
        combined_data_statement = f"SELECT Date, {account} FROM AccountWorth ORDER BY Date ASC Limit 0, 49999"
        combined_data_tuple = obtain_sql_list(combined_data_statement, database, error_log)
        largest_value_statement = f"SELECT {account} FROM AccountWorth"
        largest_y_tuple = obtain_sql_list(largest_value_statement, database, error_log)
        largest_y_raw = []

        for value in largest_y_tuple:
            largest_y_raw.append(int(float(value[0])))

        largest_y_value = max(largest_y_raw)

    # placeholder lists
    x_date = []

    # For standard account y1_gross will be the only value
    y1_gross = []
    y1_gross_fill = []
    y2_liability = []
    y2_liability_fill = []
    y3_net = []
    y3_net_fill = []
    divisor = 0
    designation = ""

    # determines the divisor for the y-axis.
    if largest_y_value >= 1000000:
        divisor = 10000
        designation = "ten thousands"
    elif largest_y_value >= 100000:
        divisor = 1000
        designation = "thousands"
    elif largest_y_value >= 10000:
        divisor = 100
        designation = "hundreds"
    elif largest_y_value >= 1000:
        divisor = 10
        designation = "tens"
    elif largest_y_value < 1000:
        divisor = 1
        designation = "dollars"

    # separates the SQL data into their appropriate axis designations
    for date in combined_data_tuple:
        from datetime import datetime
        date_formatted = datetime.strptime(date[0], "%Y/%m/%d")
        date_formatted = str(date_formatted.strftime("%m/%d/%y"))

        if account == "Net_Worth_Graph":
            x_date.append(date_formatted)
            y1_gross.append(int(float(date[1])/divisor))
            y2_liability.append(int(float(date[2])/divisor))
            y3_net.append(int(float(date[3])/divisor))

            if divisor == 1:
                y1_gross_fill.append(int(float(date[1])/divisor))
                y2_liability_fill.append(int(float(date[2]) / divisor))
                y3_net_fill.append(int(float(date[3]) / divisor))
            else:
                y1_gross_fill.append(int(float(date[1]) / divisor) - 1)
                y2_liability_fill.append(int(float(date[2]) / divisor) - 1)
                y3_net_fill.append(int(float(date[3]) / divisor) - 1)

        elif account != "Net_Worth_Graph" and parentType in ["Equity", "Retirement"]:
            x_date.append(date_formatted)
            y1_gross.append(int(float(date[1])/divisor))
            y2_liability.append(int(float(date[2])/divisor))  # Contribution not Liability
            if divisor == 1:
                y1_gross_fill.append(int(float(date[1])/divisor))
                y2_liability_fill.append(int(float(date[2]) / divisor))
            else:
                y1_gross_fill.append(int(float(date[1]) / divisor) - 1)
                y2_liability_fill.append(int(float(date[2]) / divisor) - 1)

        else:
            x_date.append(date_formatted)
            y1_gross.append(int(float(date[1])/divisor))
            if divisor == 1:
                y1_gross_fill.append(int(float(date[1])/divisor))
            else:
                y1_gross_fill.append(int(float(date[1]) / divisor) - 1)

    # determines axis internals and max values. This is to help keep the graph legible with fluctuating input quantities
    x_interval = ceil(len(x_date) / 10)

    mod_lar_y = largest_y_value / divisor

    y_max = round(mod_lar_y + 50, -2)
    if y_max < 100:
        y_max = 100

    y_interval_raw = ceil(mod_lar_y/10)

    y_interval = round(y_interval_raw, -1)
    if 90 <= y_interval < 1000:
        y_interval = 100
    elif 50 <= y_interval < 90:
        y_interval = 50
    elif 40 <= y_interval < 50:
        y_interval = 40
    elif 10 <= y_interval < 40:
        y_interval = 20
    elif y_interval < 10:
        y_interval = 10

    lg_data = [x_date, y1_gross, y2_liability, y3_net, x_interval, y_interval, y_max, designation, y1_gross_fill, y2_liability_fill, y3_net_fill]
    return lg_data


def snapshot_chart(database, graph_focus, error_log):
    if graph_focus == "Asset":
        parentTypes = ["Bank", "Cash", "CD", "Equity", "Treasury", "Retirement", "Property"]
    elif graph_focus == "Liability":
        parentTypes = ["Debt", "Credit"]
    else:
        error_message = "BuildGraphs: nested_snapshot \n incorrect graph_focus ['Asset', 'Liability']"
        error_log.error(error_message, exc_info=True)
        raise AttributeError(error_message)

    segment_data_raw = []
    segment_data = []
    segment_balances = []

    gross_statement = "SELECT SUM(Balance) FROM Account_Summary WHERE ItemType='{0}'".format(graph_focus)
    gross_worth = obtain_sql_value(gross_statement, database, error_log)[0]

    if gross_worth is None:
        gross_worth = 1
    if gross_worth <= 0:
        gross_worth = 1

    for parent in parentTypes:
        size_statement = "SELECT SUM(Balance) FROM Account_Summary WHERE ParentType='{0}'".format(parent)
        value = obtain_sql_value(size_statement, database, error_log)[0]
        if value is None or value < 0:
            value = 0
        percentage = (float(value) / float(gross_worth)) * 100
        formatted_value = cash_format(value, 2)
        percentage = decimal_places(str(percentage), 2)
        segment_data_raw.append([parent, percentage, formatted_value[2], value])

    segment_data_raw.sort(key=lambda x: x[1], reverse=True)

    for parentType in segment_data_raw:
        if parentType[1] > 0:
            segment_data.append(parentType[:3])
            segment_balances.append(parentType[3])

    if graph_focus == "Asset":
        if gross_worth < 1:
            cmap = plt.cm.Greys
            segment_data.append(["", 100, 0])
            segment_colors = [*cmap(np.linspace(0.8, .33, 1))]
        else:
            cmap = plt.cm.terrain
            segment_colors = [*cmap(np.linspace(0, 0.8, len(segment_data)))]

    else:  # graph_focus == 'Liability'
        if gross_worth < 1:
            cmap = plt.cm.Greys
            segment_data.append(["", 100, 0])
            segment_colors = [*cmap(np.linspace(0.8, .33, 1))]
        else:
            cmap = plt.cm.OrRd
            segment_colors = [*cmap(np.linspace(0.8, .33, 2))]

    return segment_balances, segment_data, segment_colors


if __name__ == "__main__":
    print("error")
