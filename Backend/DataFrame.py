#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import pandas as pd
import pickle
import sqlite3
import sys

from sqlite3 import Error

from Toolbox.Formatting_Tools import convert_to_float, decimal_places, remove_space
from Toolbox.SQL_Tools import obtain_sql_list


def create_DF(account, database, error_log):
    """For isolated testing purposes."""
    sqlName = remove_space(account)
    statement = f"""SELECT * FROM "{sqlName}" """

    try:
        conn = sqlite3.connect(database)
        with conn:
            df = pd.read_sql_query(statement, conn)
    except Error:
        df = None
        error_String = f"""DataFrame_Func: create_DF_dict \n statement: "{statement} \n database: {database}"""
        error_log.error(error_String, exc_info=True)
    finally:
        conn.close()

    return df


def create_DF_dict(database, error_log):
    """Using the Account_Summary page creates a dictionary of Account ledgers using a Pandas DataFrame"""
    summary_statement = "SELECT ID FROM Account_Summary"
    account_list_raw = obtain_sql_list(summary_statement, database, error_log)

    archive_statement = "SELECT ID FROM Account_Archive"
    archive_list_raw = obtain_sql_list(archive_statement, database, error_log)

    for account in archive_list_raw:
        account_list_raw.append(account)

    account_dict = {}

    for account in account_list_raw:
        df = create_DF(account[0], database, error_log)
        df.sort_values(by=['Transaction_Date'], ascending=True)
        df.reset_index(drop=True)
        account_dict[account[0]] = df

    return account_dict


def load_df_ledger(ledgerContainer, account):
    ledger_dictionary = empty_container(ledgerContainer)
    activeLedger = None
    try:
        activeLedger = ledger_dictionary[account]
    except KeyError:
        if account == "" or account is None:
            pass
        else:
            activeLedger = pd.DataFrame({'Transaction_Date': ['null'],
                                         'Transaction_Method': ['null'],
                                         'Transaction_Description': ['null'],
                                         'Category': ['null'],
                                         'Debit': ['null'],
                                         'Credit': ['null'],
                                         'Balance': ['null'],
                                         'Note': ['null'],
                                         'Status': ['null'],
                                         'Receipt': ['null'],
                                         'Post_Date': ['null'],
                                         'Update_Date': ['null']})
    finally:
        del ledger_dictionary
        return activeLedger


def empty_container(ledgerContainer):
    container = open(ledgerContainer, "rb")
    ledger_dictionary = pickle.load(container)
    container.close()
    return ledger_dictionary


def refill_container(ledgerContainer, ledgerDictionary):
    container = open(ledgerContainer, "wb+")
    pickle.dump(ledgerDictionary, container)
    container.close()
    return


def update_df_ledger(ledgerContainer, account, error_log, activeLedger, action="Update", new_account=None):
    ledger_dictionary = empty_container(ledgerContainer)

    if account is None:
        pass
    elif action == "Update" or action == "New":
        ledger_dictionary[account] = activeLedger
    elif action == "Delete":
        try:
            del ledger_dictionary[account]
        except KeyError:
            error_String = f"""DataFrame_Func: update_df_ledger \n action: {action} Failed to execute \n account {account}"""
            error_log.error(error_String, exc_info=True)
    elif action == "Rename":
        try:
            ledger_dictionary[new_account] = ledger_dictionary.pop(account)
        except KeyError:
            error_String = f"""DataFrame_Func: update_df_ledger \n action: {action} Failed to execute \n account: {account} and new_account: {new_account}"""
            error_log.error(error_String, exc_info=True)

    refill_container(ledgerContainer, ledger_dictionary)
    del ledger_dictionary


def update_df_balance(activeLedger):
    running_balance = 0
    df_row_count = activeLedger.shape[0]
    df_row_count = int(df_row_count)
    activeLedger = activeLedger.sort_values(by=['Transaction_Date', 'Update_Date'], ascending=True)
    activeLedger = activeLedger.reset_index(drop=True)

    for row in range(0, df_row_count):
        debit = convert_to_float(activeLedger.iloc[row]['Debit'])
        credit = convert_to_float(activeLedger.iloc[row]['Credit'])
        trans_balance_calc = running_balance + credit - debit
        trans_balance_calc = str(trans_balance_calc)
        trans_balance_calc = decimal_places(trans_balance_calc, 2)
        activeLedger.at[row, 'Balance'] = str(trans_balance_calc)
        running_balance = float(trans_balance_calc)

    return activeLedger


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
