import pickle
import sqlite3

from sqlite3 import Error

from Toolbox.Formatting_Tools import cash_format, decimal_places


# --- SQL Functions --- #
def add_column(tableName: str, col: str, sqlType: str, database: str):
    """
    {Debugging Tool} Specific SQL Statement to highlight addition of column to a table

    :param tableName: str
    :param col: strA
    :param sqlType: str
    :param database: str
    :return: None
    """
    alterStatement = f"ALTER TABLE {tableName} ADD COLUMN {col} {sqlType}"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(alterStatement)
    except Error:
        print(f"""ERROR: SQL_FUNC: add_column \n statement: "{alterStatement}" \n database: "{database}" """)
    finally:
        conn.close()


def attempt_sql_statement(statement: str, database: str):
    """
    For SQL Statements that pass/fail

    :param statement: str
    :param database: str
    :return: bool
    """
    result = True
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
    except Error:
        print(f"""ERROR: SQL_FUNC: attempt_sql_statement \n statement: "{statement}" \n database: "{database}" """)
        result = False
    finally:
        conn.close()
    return result


def check_column(tablename: str, col: str, database: str):
    """
    {Debugger Tool} Used to confirm a column header exists

    :param tablename: str
    :param col: str
    :param database: str
    :return:
    """
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
        print(f"""ERROR: SQL_FUNC: check_column \n statement: "{checkColumn}" \n database: "{database}" """)
    finally:
        conn.close()


def check_for_data(tablename: str, colTwo: str, value: str, database: str):
    """
    Checks for the existence of a Value in given Table Name and Column

    :param tablename: str
    :param colTwo: str
    :param value:str
    :param database: str
    :return: bool
    """
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
    except Error as e:
        print(f"""ERROR: SQLTools_Func: check_for_data \n text: {checkStatement} \n database: {database}""")
    finally:
        conn.close()


def create_table(tableName: str, columns: list, inputType: list, database: str):
    """
    Safety Catch - Checks for table and create it if it doesn't exist

    :param tableName: str
    :param columns: list
    :param inputType: list
    :param database: str
    :return: None
    """
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
    except Error as e:
        print(f"""ERROR: SQLTools_Func: create_table \n text: {fullStatement} \n database: {database}""")
    finally:
        conn.close()


def delete_column(table: str, column: str, database: str):
    """
    Sqlite3 doesn't inherently have the ability to delete a column. This is a work around.
    :param table: str
    :param column: str
    :param database: str
    :return: None
    """
    temp = "temporary"

    # obtain all existing columns
    obtain_columns = f"PRAGMA table_info({table})"
    column_data_raw = obtain_sql_list(obtain_columns, database)

    retained_columns = []
    new_table_column_str = ""

    # removes the unwanted column
    for header in column_data_raw:
        if header[1] != column:
            retained_columns.append([header[1], header[2]])
            new_table_column_str += f"{header[1]} {header[2]}, "
        else:
            pass

    new_table_column_str = new_table_column_str[:-2]

    change_table_name = f"ALTER TABLE {table} RENAME TO {temp}"
    new_table_statement = f"CREATE TABLE IF NOT EXISTS {table}({new_table_column_str})"
    execute_sql_statement_list([change_table_name, new_table_statement], database)

    rowID_Statement = f"SELECT ROWID FROM {temp}"
    rowID_list = obtain_sql_list(rowID_Statement, database)

    for rowID in rowID_list:
        insert = f"INSERT INTO {table} VALUES({new_table_column_str}) SELECT {new_table_column_str} FROM {temp} WHERE ROWID='{rowID[0]}'"
        specific_sql_statement(insert, database)

    drop = f"DROP TABLE {temp}"
    specific_sql_statement(drop, database)


def execute_sql_statement_list(statement_lst: list, database: str):
    """
    Opens connection to designated database and executes a list of statements that do not return values

    :param statement_lst: list of sqlite3 formatted statements
    :param database: pathway to connect to sqlite3 database
    :return: None
    """

    x = 0
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            for statement in statement_lst:
                cur.execute(statement)
                x += 1
    except Error:
        print(f"""ERROR: SQLTools_Func: execute_sql_statement_list \n statement number: {x} \n text: "{statement_lst[x]}" \n database: {database}""")
    finally:
        conn.close()


def obtain_sql_value(statement: str, database: str):
    """
    Obtains a single value as string

    :param statement: sqlite3 formatted statement
    :param database: pathway to connect to sqlite3 database
    :return: value as string
    """

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
        print(f"""ERROR: SQLTools_Func: obtain_sql_value \n statement: "{statement} \n database: {database}""")
        return rValue
    finally:
        conn.close()
        return rValue


def obtain_sql_list(statement: str, database: str):
    """
    Obtains a single list of string values,

    :param statement: sqlite3 formatted statement
    :param database: pathway to connect to sqlite3 database
    :return: list of string values -- typically nested lists
    """

    rValue = ""
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
            value = cur.fetchall()
            rValue = value
    except Error:
        print(f"""ERROR: SQLTools_Func: obtain_sql_lst \n statement: "{statement}" \n database: {database}""")
    finally:
        conn.close()
        return rValue


def move_sql_tables(destination: str, origin: str, identifier: str, target: str, database: str):
    """
    Move value(s) between sqlite3 tables. Deletes original input

    :param destination: Target table
    :param origin: Initial table
    :param identifier: Column name or row number used to identify target value(s)
    :param target: Specific value associated with identifier
    :param database: pathway to connect to sqlite3 database
    :return: No value is returned to console for use
    """

    insert_statement = "INSERT INTO " + destination + " SELECT * FROM " + origin + " WHERE " + identifier + "= '" + target + "'"
    delete_statement = "DELETE FROM " + origin + " WHERE " + identifier + "= '" + target + "'"
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(insert_statement)
            cur.execute(delete_statement)
    except Error:
        print(f"""ERROR: TB_Func: move_sql_tables \n Insert Statement: "{insert_statement}" \n Delete Statement: "{delete_statement}" \n database: {database}""")
    finally:
        conn.close()


def specific_sql_statement(statement: str, database: str):
    """
    Opens connection to designated database and executes a single statement that does not return a value

    :param statement: sqlite3 formatted string statement
    :param database: pathway to connect to sqlite3 database
    :return: None
    """
    try:
        conn = sqlite3.connect(database)
        with conn:
            cur = conn.cursor()
            cur.execute(statement)
    except Error:
        print(f"""ERROR: SQL_FUNC: specific_sql_statement \n statement: "{statement}" \n database: "{database}" """)
    finally:
        conn.close()


def sqlite3_keyword_check(statement: str):
    keyword_list = open("Spoon/sql_Keyword_list.pkl", "rb")
    sqlite3_keyword_masterlist = pickle.load(keyword_list)

    if statement.upper() in sqlite3_keyword_masterlist:
        return True
    else:
        return False


# --- Catchall --- #
if __name__ == '__main__':
    print("Error - Check your executable")
