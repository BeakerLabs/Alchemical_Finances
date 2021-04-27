""" This fix will be used to create the "Tabulate" toggle for the categories table"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

from Toolbox.SQL_Tools import *
from Toolbox.OS_Tools import *
from Toolbox.Formatting_Tools import *
from Toolbox.Logging_System import create_log_fileName, get_logger

if __name__ == "__main__":
    errorLog_Pathway = "errorlog.txt"
    error_Log = get_logger("AF_ERROR_LOG", errorLog_Pathway)

    database = "b8aem6j45m5r36ghs.db"
    add_column("Categories", "Tabulate", "Bool", database, error_Log)

    cat_rowID_statement = "UPDATE Categories SET Tabulate='True'"
    rowID_list_raw = specific_sql_statement(cat_rowID_statement, database, error_Log)
