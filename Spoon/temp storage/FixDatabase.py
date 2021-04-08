""" Purpose of this Fix Database will be to add the generic statement period and associated account details.
    Technically a larger fix than the others and the last to be implimented as it doesn't cross between the two verisons.
"""

from Toolbox.SQL_Tools import *
from Toolbox.OS_Tools import *
from Toolbox.Formatting_Tools import *

import time


def update_ledger_balance(targetLedger, database):
    # active_ledger = targetLedger.currentText()
    active_ledger = targetLedger
    sql_active_ledger = remove_space(active_ledger)

    running_balance = 0

    rowID_Statement = f"SELECT ROWID FROM {sql_active_ledger} Order by Transaction_Date ASC Limit 0, 49999"
    rowID_list = obtain_sql_list(rowID_Statement, database)

    for rowID in rowID_list:
        row = rowID[0]
        transaction = f"SELECT SUM(Credit - Debit) FROM {sql_active_ledger} WHERE ROWID='{row}'"
        CreditDebit = obtain_sql_value(transaction, database)
        transaction_balance = running_balance + CreditDebit[0]
        transaction_balance = decimal_places(transaction_balance, 2)
        update_balance = f"UPDATE {sql_active_ledger} SET Balance='{transaction_balance}' WHERE ROWID='{row}'"
        specific_sql_statement(update_balance, database)
        running_balance = float(transaction_balance)


def correct_details_tables(database):
    details_pages_list = [["Bank_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Bank_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Interest_Rate",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Interest_Rate"],
                          ["Cash_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Cash_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1"],
                          ["CD_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS CD_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL, Maturity_Date NUMERIC)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Interest_Rate, Maturity_Date",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Interest_Rate, Maturity_Date"],
                          ["Treasury_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Treasury_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL, Maturity_Date NUMERIC)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Interest_Rate, Maturity_Date",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Interest_Rate, Maturity_Date"],
                          ["Credit_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Credit_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Credit_Limit INTEGER)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Credit_Limit",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Credit_Limit"],
                          ["Debt_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Debt_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL, Starting_Balance REAL)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Interest_Rate, Starting_Balance",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Interest_Rate, Starting_Balance"],
                          ["Equity_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Equity_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Ticker_Symbol TEXT, Stock_Price REAL)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Ticker_Symbol, Stock_Price",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Ticker_Symbol, Stock_Price"],
                          ["Retirement_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Retirement_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Ticker_Symbol TEXT, Stock_Price REAL)",
                           "Account_Name, Account_Type, Primary_Owner, Bank, Statement_Date, Ticker_Symbol, Stock_Price",
                           "Account_Name, Account_Type, Primary_Owner, Bank, 1, Ticker_Symbol, Stock_Price"],
                          ["Property_Account_Details",
                           f"CREATE TABLE IF NOT EXISTS Property_Account_Details (Account_Name TEXT, Account_Type TEXT, Primary_Ownder TEXT, Bank TEXT, Statement_Date INTEGER, Address_1 TEXT, County TEXT, State_Initials TEXT,"
                           f" Zip_Code INTEGER, Image TEXT)"]]

    for table in details_pages_list:
        if table[0] == "Property_Account_Details":
            specific_sql_statement(table[1], database)
        else:
            temp = "temporary"
            change_table_name = f"ALTER TABLE {table[0]} RENAME TO {temp}"
            new_table_statement = table[1]
            execute_sql_statement_list([change_table_name, new_table_statement], database)
            rowID_Statement = f"SELECT ROWID FROM {temp} Order by Account_Name ASC Limit 0, 49999"
            rowID_list = obtain_sql_list(rowID_Statement, database)

            for rowID in rowID_list:
                insert = f"INSERT INTO {table[0]}({table[2]}) SELECT {table[3]} FROM {temp} WHERE ROWID='{rowID[0]}'"
                specific_sql_statement(insert, database)

            drop = f"DROP TABLE {temp}"
            specific_sql_statement(drop, database)


def correct_ledger1_tables(database):
    parentType_dict = {
        "Bank": "Bank_Account_Details",
        "Cash": "Cash_Account_Details",
        "CD": "CD_Account_Details",
        "Treasury": "Treasury_Account_Details",
        "Credit": "Credit_Account_Details",
        "Debt": "Debt_Account_Details",
    }
    temp = "temporaryName"
    for parentType in parentType_dict:
        ledger_list_statement = f"SELECT Account_Name FROM {parentType_dict[parentType]}"
        ledger_list = obtain_sql_list(ledger_list_statement, database)

        for ledger in ledger_list:
            modifiedLN = remove_space(ledger[0])

            ledgerStatement = "CREATE TABLE IF NOT EXISTS " + modifiedLN + \
                              "(Transaction_Date NUMERIC, Transaction_Method TEXT," \
                              " Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Balance REAL, Note TEXT," \
                              " Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"

            change_table_name = f"ALTER TABLE {modifiedLN} RENAME TO {temp}"
            execute_sql_statement_list([change_table_name, ledgerStatement], database)
            rowID_Statement = f"SELECT ROWID FROM {temp} ORDER BY Transaction_Date ASC Limit 0, 49999"
            rowID_list = obtain_sql_list(rowID_Statement, database)

            for rowID in rowID_list:
                referenceA = "Transaction_Date, Transaction_Method, Transaction_Description, Category, Debit, Credit, Balance, Note, Status, Receipt, Post_Date, Update_Date"
                referenceB = "Transaction_Date, Transaction_Method, Transaction_Description, Category, Debit, Credit, 0, Note, Status, Receipt, Post_Date, Update_Date"
                insert = f"INSERT INTO {modifiedLN}({referenceA}) SELECT {referenceB} FROM {temp} WHERE ROWID='{rowID[0]}'"
                specific_sql_statement(insert, database)

            drop = f"DROP TABLE {temp}"
            specific_sql_statement(drop, database)


def correct_ledger_balance(database):
    parentType_dict = {
        "Bank": "Bank_Account_Details",
        "Cash": "Cash_Account_Details",
        "CD": "CD_Account_Details",
        "Treasury": "Treasury_Account_Details",
        "Credit": "Credit_Account_Details",
        "Debt": "Debt_Account_Details",
    }

    for parentType in parentType_dict:
        ledger_list_statement = f"SELECT Account_Name FROM {parentType_dict[parentType]}"
        ledger_list = obtain_sql_list(ledger_list_statement, database)

        for ledger in ledger_list:
            modifiedLN = remove_space(ledger[0])
            update_ledger_balance(modifiedLN, database)


if __name__ == "__main__":
    database = "b8aem6j45m5r36ghs.db"
    correct_details_tables(database)
    correct_ledger1_tables(database)
    # Create Property Value subtypes
    property_subtypes = ["Single Occupancy", "Rental", "Vacation", "Duplex"]
    for subtype in property_subtypes:
        statement = f"INSERT INTO AccountSubType VALUES('{subtype}', 'Property')"
        specific_sql_statement(statement, database)
    # Fix Balances on Ledgers
    correct_ledger_balance(database)

    # Create Property Value Summary
    #
    # Create Property Value Account details



