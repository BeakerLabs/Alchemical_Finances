""" This fix will be used to create the "Tabulate" toggle for the categories table"""

from Toolbox.SQL_Tools import *
from Toolbox.OS_Tools import *
from Toolbox.Formatting_Tools import *


if __name__ == "__main__":
    database = "b8aem6j45m5r36ghs.db"
    add_column("Categories", "Tabulate", "Bool", database)

    cat_rowID_statement = "UPDATE Categories SET Tabulate='True'"
    rowID_list_raw = specific_sql_statement(cat_rowID_statement, database)
