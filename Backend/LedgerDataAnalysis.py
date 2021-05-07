"""
This script is the backend for the Category Pie Chart that will be embedded into Ledger 1.

Future Concepts
1)

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import operator
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value
from Toolbox.Formatting_Tools import add_space, cash_format, decimal_places, remove_space


def category_spending_data(database, account, error_log):
    """ Obtains the Account Specific Spending based upon Category. """

    statement = f"SELECT Transaction_Date, Category, Debit, Credit FROM {account} WHERE Status='Posted'"
    raw_data = obtain_sql_list(statement, database, error_log)

    years = []
    [years.append(tup[0][:4]) for tup in raw_data if tup[0][:4] not in years]
    years.sort(reverse=True)

    parentType_statement = f"SELECT ParentType from Account_Summary WHERE ID='{add_space(account)}'"
    parentType_raw = obtain_sql_value(parentType_statement, database, error_log)
    parentType = parentType_raw[0]

    active_categories = f"SELECT Method FROM Categories WHERE ParentType ='{parentType}' AND Tabulate ='True'"
    active_categories_raw = obtain_sql_list(active_categories, database, error_log)

    categories = []
    [categories.append(tup[0]) for tup in active_categories_raw if tup[0] not in categories]

    return years, categories, raw_data


def category_spending_by_interval(database, account, interval_length, interval, error_log):
    """ Returns a 'result list' of the category spending from highest to lowest percentage"""
    _, categories, raw_data = category_spending_data(database, account, error_log)

    spending_dict = {}
    result_list = []
    total = 0

    for category in categories:
        spending_dict[category] = 0

    if interval_length == "Statement":
        # Convert Statement Period into proper formatting and create date range.
        convert_to_datetime = datetime.strptime(interval, '%B %d, %Y')
        format_datetime = convert_to_datetime.strftime("%Y/%m/%d")
        return_to_datetime = datetime.strptime(format_datetime, "%Y/%m/%d")
        start_datetime = return_to_datetime + relativedelta(months=-1)
        end_datetime = return_to_datetime + relativedelta(days=-1)

    elif interval_length == "Year":
        # Convert Year into YYYY/01/01 and YYYY/12/31 to obtain transactions in that range
        convert_to_datetime = datetime.strptime(interval, '%Y')
        format_datetime = convert_to_datetime.strftime("%Y/%m/%d")
        start_datetime = datetime.strptime(format_datetime, "%Y/%m/%d")
        end_datetime = start_datetime + relativedelta(days=-1) + relativedelta(years=+1)

    elif interval_length == "Overall":
        # Convert First and Last Transaction into datetime format
        raw_sorted = sorted(raw_data, key=lambda x: x[0])
        start_transaction = raw_sorted[0][0]
        end_transaction = raw_sorted[-1][0]

        start_datetime = datetime.strptime(start_transaction, "%Y/%m/%d")
        end_datetime = datetime.strptime(end_transaction, "%Y/%m/%d")

    else:  # Shouldn't hit this point
        raise Exception("interval_length != 'Statement', 'Year', 'Overall'")

    for transaction in raw_data:
        # [ Transaction_Date, Category, Debit, Credit ]
        if transaction[1] in spending_dict:
            transaction_date = datetime.strptime(transaction[0], "%Y/%m/%d")
            if start_datetime <= transaction_date <= end_datetime:

                if transaction[2] == "":
                    debit = decimal_places("0.00", 2)
                else:
                    debit = decimal_places(transaction[2], 2)

                if transaction[3] == "":
                    credit = decimal_places("0.00", 2)
                else:
                    credit = decimal_places(transaction[3], 2)

                value = abs(credit - debit)
                spending_dict[transaction[1]] += value
                total += value
        else:
            pass
            # a Spending Category that isn't being calculated

    if total <= 0 or total is None:
        total = 1

    for category in spending_dict:
        percentage = (spending_dict[category] / total) * 100
        percentage = float(percentage)
        subtotal = decimal_places(str(spending_dict[category]), 2)
        result_list.append([category, percentage, subtotal])
        result_list.sort(reverse=True, key=lambda x: x[1])

    spending_string_dict = format_result_string(result_list)

    # result_list = [Category, Percentage, subtotal]
    # spending_String_dict = {Category: string}
    # spending_dict = {Category: cash Balance}
    return result_list, spending_string_dict, spending_dict


def format_result_string(data_list):
    temp_dict = {}
    # Data List = [ID, Percentage]
    for count, dataPoint in enumerate(data_list, start=1):
        if count < 10:
            count = "0" + str(count)

        if 0 <= decimal_places(dataPoint[1], 2) < 10:
            string_convert = str(decimal_places(dataPoint[1], 2))
            percentage = "    " + string_convert
        elif 10 <= decimal_places(dataPoint[1], 2) < 100:
            string_convert = str(decimal_places(dataPoint[1], 2))
            percentage = "  " + string_convert
        elif decimal_places(dataPoint[1], 2) >= 100:
            percentage = str(decimal_places(dataPoint[1], 2))
        else:
            percentage = "   0.00%"
        formatted_subtotal = cash_format(dataPoint[2], 2)
        temp_string = f"{count}: {percentage}%  -- {dataPoint[0]}\n          ({formatted_subtotal[2]})"
        temp_dict[dataPoint[0]] = temp_string
    return temp_dict


def equity_subtype_data(database, parentType, error_log):
    statement = f"SELECT ID, SubType, Balance FROM Account_Summary WHERE ParentType='{parentType}'"
    raw_data = obtain_sql_list(statement, database, error_log)

    subType_dic = {}
    subType_dic = {investment[1]: [0, 0] for investment in raw_data if investment[1] not in subType_dic}
    # subType_dic = {SubType: [percentage, SubTotal]}
    subType_list = []

    investment_list = []
    investment_list = [[investment[0], 0, investment[2]] for investment in raw_data if investment[0] not in investment_list]
    # investment_list = [Investment, percentage, SubTotal]
    total = 0

    sector_dictionary = {"Information Technology": [0, 0],
                         "Health Care": [0, 0],
                         "Financial": [0, 0],
                         "Consumer Discretionary": [0, 0],
                         "Communication": [0, 0],
                         "Industrial": [0, 0],
                         "Consumer Staples": [0, 0],
                         "Energy": [0, 0],
                         "Real Estate": [0, 0],
                         "Materials": [0, 0],
                         "Broad Market": [0, 0],
                         "Unspecified": [0, 0]}

    sector_list = []

    for investment in raw_data:
        subtype = investment[1]
        subType_dic[subtype][1] += investment[2]
        total += investment[2]

        sector_statement = f"SELECT Sector FROM {parentType}_account_details WHERE Account_Name='{remove_space(investment[0])}'"
        sector_raw = obtain_sql_value(sector_statement, database, error_log)
        sector_value = sector_raw[0]
        sector_dictionary[sector_value][1] += investment[2]

    for subType in subType_dic:
        balance = subType_dic[subType][1]

        if total <= 0:
            subType_dic[subType][0] = 0
        else:
            subType_dic[subType][0] = (balance / total) * 100

    [subType_list.append([subType, subType_dic[subType][0], subType_dic[subType][1]]) for subType in subType_dic]
    # [subType, percentage, SubTotal, string]

    for investment in investment_list:
        if total <= 0:
            investment[1] = 0
        else:
            investment[1] = (investment[2] / total) * 100

    for sector in sector_dictionary:
        balance = sector_dictionary[sector][1]

        if total <= 0:
            sector_dictionary[sector][0] = 0
        else:
            sector_dictionary[sector][0] = (balance / total) * 100

    [sector_list.append([sector, sector_dictionary[sector][0], sector_dictionary[sector][1]]) for sector in sector_dictionary]

    investment_list.sort(reverse=True, key=lambda x: x[1])
    subType_list.sort(reverse=True, key=lambda x: x[1])
    sector_list.sort(reverse=True, key=lambda x: x[1])

    subType_string_dict = format_result_string(subType_list)
    investment_string_dict = format_result_string(investment_list)
    sector_string_dict = format_result_string(sector_list)

    return subType_list, investment_list, sector_list, subType_string_dict, investment_string_dict, sector_string_dict


if __name__ == "__main__":
    print("error")
