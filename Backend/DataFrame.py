#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

# Current script is experimental and will be isolated from core program for now.

import sqlite3
import pandas as pd

from pathlib import Path
from sqlite3 import Error

from Toolbox.Formatting_Tools import remove_space
from Toolbox.SQL_Tools import obtain_sql_list


def create_DF(database, account):
    sqlName = remove_space(account)
    statement = f"""SELECT * FROM "{sqlName}" """

    try:
        conn = sqlite3.connect(database)
        with conn:
            df = pd.read_sql_query(statement, conn)
    except Error:
        df = None
        error_String = f"""DataFrame_Func: create_DF_diuct \n statement: "{statement} \n database: {database}"""
        # error_log.error(error_string, exc_info=True)
        print(error_String)
    finally:
        conn.close()

    return df


def create_DF_dict(database):
    summary_statement = "SELECT ID FROM Account_Summary"

    # This will be exchanged for a SQL_Tools_FUNC: Obtain_sql_list when implemented. As currently an error_log is not active
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(summary_statement)
    value = cur.fetchall()
    account_list_raw = value
    conn.close()

    account_dict = {}

    for account in account_list_raw:
        sqlName = remove_space(account[0])
        statement = f"""SELECT * FROM "{sqlName}" """

        try:
            conn = sqlite3.connect(database)
            with conn:
                df = pd.read_sql_query(statement, conn)
        except Error:
            df = None
            error_String = f"""DataFrame_Func: create_DF_diuct \n statement: "{statement} \n database: {database}"""
            # error_log.error(error_string, exc_info=True)
            print(error_String)
        finally:
            conn.close()

        account_dict[account] = df

    return account_dict


def update_df_balances(df):
    pass


if __name__ == "__main__":
    database = "mgj013781has1erbm4.db"
    pathway = str(Path.cwd())
    adjusted_pathway = pathway[:-8]
    database_pathway = Path(adjusted_pathway) / "data" / "account" / database
    example_dict = create_DF_dict(database_pathway)
