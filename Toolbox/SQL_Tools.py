#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import pickle
import sqlite3

from sqlite3 import Error

from Toolbox.Formatting_Tools import cash_format, decimal_places


# --- SQL Functions --- #
def add_column(tableName: str, col: str, sqlType: str, database: str, error_log):
    """ Specific SQL Statement to highlight addition of column to a table """
    alterStatement = f"ALTER TABLE {tableName} ADD COLUMN {col} {sqlType}"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(alterStatement)
    except Error:
        error_string = f"""SQL_FUNC: add_column \n statement: "{alterStatement}" \n database: "{database}" """
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def attempt_sql_statement(statement: str, database: str, error_log):
    """ For SQL Statements that pass/fail """
    result = True
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
    except Error:
        error_string = f"""SQL_FUNC: attempt_sql_statement \n statement: "{statement}" \n database: "{database}" """
        error_log.error(error_string, exc_info=True)
        result = False
    finally:
        conn.close()
    return result


def check_column(tablename: str, col: str, database: str, error_log):
    """ Used to confirm a column header exists  """
    checkColumn = f"SELECT COUNT(*) AS CENTRA FROM PRAGMA_table_info('{tablename}') WHERE name='{col}'"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(checkColumn)
            row = cur.fetchone()
            if row is None:
                return True
            else:
                return False
    except Error:
        error_string = f"""SQL_FUNC: check_column \n statement: "{checkColumn}" \n database: "{database}" """
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def check_for_data(tablename: str, colTwo: str, value: str, database: str, error_log):
    """ Checks for the existence of a Value in given Table Name and Column """
    checkStatement = f"SELECT * FROM {tablename} WHERE {colTwo}= '{value}'"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(checkStatement)
            row = cur.fetchone()
            if row is None:
                return True
            else:
                return False
    except Error:
        error_string = f"""SQLTools_Func: check_for_data \n text: {checkStatement} \n database: {database}"""
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def create_table(tableName: str, columns: list, inputType: list, database: str, error_log):
    """ Safety Catch - Checks for table and create it if it doesn't exist """
    baseStatement = f"CREATE TABLE IF NOT EXISTS {tableName}("
    input_string = ""

    for x in range(0, len(columns)):
        if x > 0:
            input_string += f", {columns[x]} {inputType[x]}"
        else:
            input_string += f"{columns[x]} {inputType[x]}"

    fullStatement = f"{baseStatement}{input_string})"

    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(fullStatement)
    except Error:
        error_string = f"""SQLTools_Func: create_table \n text: {fullStatement} \n database: {database}"""
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def delete_column(table: str, column: str, database: str, error_log):
    """ Sqlite3 doesn't inherently have the ability to delete a column. This is a work around.  """
    temp = "temporary"

    # obtain all existing columns
    obtain_columns = f"PRAGMA table_info({table})"
    column_data_raw = obtain_sql_list(obtain_columns, database, error_log, exc_info=True)

    retained_columns = []
    new_table_column_str = ""
    select_table_column_str = ""

    # removes the unwanted column
    for header in column_data_raw:
        if header[1] != column:
            retained_columns.append([header[1], header[2]])
            new_table_column_str += f"'{header[1]}' {header[2]}, "
            select_table_column_str += f"{header[1]}, "
        else:
            pass

    new_table_column_str = new_table_column_str[:-2]
    select_table_column_str = select_table_column_str[:-2]

    change_table_name = f"ALTER TABLE {table} RENAME TO {temp}"
    new_table_statement = f"CREATE TABLE IF NOT EXISTS {table}({new_table_column_str})"
    execute_sql_statement_list([change_table_name, new_table_statement], database, error_log)

    rowID_Statement = f"SELECT ROWID FROM {temp}"
    rowID_list = obtain_sql_list(rowID_Statement, database, error_log)

    for rowID in rowID_list:
        insert = f"INSERT INTO {table} SELECT {select_table_column_str} FROM {temp} WHERE ROWID='{rowID[0]}'"
        specific_sql_statement(insert, database, error_log)

    drop = f"DROP TABLE {temp}"
    specific_sql_statement(drop, database, error_log)


def execute_sql_statement_list(statement_lst: list, database: str, error_log):
    """ Opens connection to designated database and executes a list of statements that do not return values """
    x = 0
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            for statement in statement_lst:
                cur.execute(statement)
                x += 1
    except Error:
        error_string = f"""SQLTools_Func: execute_sql_statement_list \n statement number: {x} \n text: "{statement_lst[x]}" \n database: {database}"""
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def obtain_sql_value(statement: str, database: str, error_log):
    """ Obtains a single value as string """

    rValue = ""
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
            value = cur.fetchone()
            rValue = value
    except Error:
        rValue = None
        error_string = f"""SQLTools_Func: obtain_sql_value \n statement: "{statement} \n database: {database}"""
        error_log.error(error_string, exc_info=True)
        return rValue
    finally:
        conn.close()
        return rValue


def obtain_sql_list(statement: str, database: str, error_log):
    """ Obtains a single list of string values  """

    rValue = ""
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
            value = cur.fetchall()
            rValue = value
    except Error:
        error_string = f"""SQLTools_Func: obtain_sql_lst \n statement: "{statement}" \n database: {database}"""
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()
        return rValue


def move_sql_tables(destination: str, origin: str, identifier: str, target: str, database: str, error_log):
    """ Move value(s) between sqlite3 tables. Deletes original input """

    insert_statement = f"INSERT INTO {destination} SELECT * FROM {origin} WHERE {identifier} ='{target}'"
    delete_statement = f"DELETE FROM {origin} WHERE {identifier}='{target}'"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(insert_statement)
            cur.execute(delete_statement)
    except Error:
        error_string = f"""TB_Func: move_sql_tables \n Insert Statement: "{insert_statement}" \n Delete Statement: "{delete_statement}" \n database: {database}"""
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def specific_sql_statement(statement: str, database: str, error_log):
    """ Opens connection to designated database and executes a single statement that does not return a value """
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
    except Error:
        error_string = f"""SQL_FUNC: specific_sql_statement \n statement: "{statement}" \n database: "{database}" """
        error_log.error(error_string, exc_info=True)
    finally:
        conn.close()


def sqlite3_keyword_check(statement: str):
    keyword_list = open("Resources/sql_Keyword_list.pkl", "rb")
    sqlite3_keyword_masterlist = pickle.load(keyword_list)

    if statement.upper() in sqlite3_keyword_masterlist:
        return True
    else:
        return False


# --- Catchall --- #
if __name__ == '__main__':
    print("Error - Check your executable")
