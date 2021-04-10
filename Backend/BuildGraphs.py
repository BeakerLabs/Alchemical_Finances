import os

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Toolbox.Formatting_Tools import add_space, decimal_places
from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value
from math import ceil


class AF_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, facecolor="#f5fbef"):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=facecolor)
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#e3e3e3')
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
    x_interval = ceil(len(x_date) / 6)

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


def nested_snapshot(database, graph_focus, error_log):
    if graph_focus == "Asset":
        parentTypes = ["Bank", "Cash", "CD", "Equity", "Treasury", "Retirement", "Property"]
    elif graph_focus == "Liability":
        parentTypes = ["Debt", "Credit"]
    else:
        # User shouldn't hit this
        parentTypes = ["Bank"]

    bank_accounts = []
    cash_accounts = []
    cd_accounts = []
    equity_accounts = []
    treasury_accounts = []
    retirement_accounts = []
    property_accounts = []
    debt_accounts = []
    credit_accounts = []
    flat_values = []
    sizes = []

    parentType_dict = {
        "Bank": bank_accounts,
        "Cash": cash_accounts,
        "CD": cd_accounts,
        "Equity": equity_accounts,
        "Treasury": treasury_accounts,
        "Retirement": retirement_accounts,
        "Property": property_accounts,
        "Debt": debt_accounts,
        "Credit": credit_accounts,
    }

    gross_statement = "SELECT SUM(Balance) FROM Account_Summary WHERE ItemType='{0}'".format(graph_focus)
    gross_worth = obtain_sql_value(gross_statement, database, error_log)[0]

    if gross_worth <= 0 or gross_worth is None:
        gross_worth = 1

    for parent in parentTypes:
        size_statement = "SELECT SUM(Balance) FROM Account_Summary WHERE ParentType='{0}'".format(parent)
        value = obtain_sql_value(size_statement, database, error_log)[0]
        if value is None or value < 0:
            value = 0
        percentage = (float(value) / float(gross_worth)) * 100
        percentage = decimal_places(percentage, 2)
        sizes.append(percentage)

        balance_statement = "SELECT Balance FROM Account_Summary WHERE ParentType='{0}'".format(parent)
        account_balances = obtain_sql_list(balance_statement, database, error_log)
        account_balances.sort(reverse=True)
        for balance in account_balances:
            correction = balance[0]
            if correction < 0:
                correction = 0
            parentType_dict[parent].append(correction)
            flat_values.append(correction)

    if graph_focus == "Asset":
        sum_balances = [sum(bank_accounts), sum(cash_accounts), sum(cd_accounts), sum(equity_accounts), sum(treasury_accounts), sum(retirement_accounts), sum(property_accounts)]
        cmap = plt.cm.BuGn
        outer_colors = [*cmap(np.linspace(1, .33, 7))]
        inner_colors = [*cmap(np.linspace(0.6, .1, len(bank_accounts))),
                        *cmap(np.linspace(0.6, .1, len(cash_accounts))),
                        *cmap(np.linspace(0.6, .1, len(cd_accounts))),
                        *cmap(np.linspace(0.6, .1, len(equity_accounts))),
                        *cmap(np.linspace(0.6, .1, len(treasury_accounts))),
                        *cmap(np.linspace(0.6, .1, len(retirement_accounts))),
                        *cmap(np.linspace(0.6, .1, len(property_accounts))),
                        ]

    elif graph_focus == "Liability":
        sum_balances = [sum(debt_accounts), sum(credit_accounts)]
        cmap = plt.cm.OrRd
        outer_colors = [*cmap(np.linspace(0.8, .33, 2))]
        inner_colors = [*cmap(np.linspace(0.6, .1, len(debt_accounts))),
                        *cmap(np.linspace(0.6, .1, len(credit_accounts))),
                        ]

    else:  # Shouldn't use this
        sum_balances = [sum(bank_accounts)]
        cmap = plt.cm.Greys
        outer_colors = [*cmap(np.linspace(0.8, .33, 6))]
        inner_colors = [*cmap(np.linspace(0.6, .1, len(debt_accounts))),
                        ]

    target_values = [sum_balances, outer_colors, flat_values, inner_colors, sizes]

    return target_values


if __name__ == "__main__":
    print("error")
