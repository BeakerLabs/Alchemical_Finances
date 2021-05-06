""" Was used to crease AccountWorth and ContributionTotals Tables"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

from Toolbox.SQL_Tools import *
from Toolbox.OS_Tools import *
from Toolbox.Formatting_Tools import *

if __name__ == "__main__":
    database = "b8aem6j45m5r36ghs.db"

    ov_graph_statement = "CREATE TABLE IF NOT EXISTS AccountWorth(Date TEXT)"
    contribution_graph_statement = "CREATE TABLE IF NOT EXISTS ContributionTotals(Date TEXT)"
    specific_sql_statement(ov_graph_statement, database)
    specific_sql_statement(contribution_graph_statement, database)

    from datetime import datetime, timedelta

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime("%Y/%m/%d")
    today = today.strftime("%Y/%m/%d")

    insertDate_accountWorth_table = f"INSERT INTO AccountWorth(Date) VALUES('{today}')"
    insert_date = f"INSERT INTO ContributionTotals(Date) VALUES('{today}')"

    execute_sql_statement_list([insertDate_accountWorth_table, insert_date], database)

    accounts_worth = "SELECT ID, ParentType FROM Account_Summary"
    accounts = obtain_sql_list(accounts_worth, database)

    for account in accounts:
        parentType = account[1]
        account = remove_space(account[0])

        accountWorth_statement = f"ALTER TABLE AccountWorth ADD COLUMN '{account}' TEXT"
        specific_sql_statement(accountWorth_statement, database)

        if parentType in ["Equity", "Retirement"]:
            contributions_statement = f"ALTER TABLE ContributionTotals ADD COLUMN '{account}' TEXT"
            specific_sql_statement(contributions_statement, database)
        else:
            pass