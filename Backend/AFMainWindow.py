"""
This script is the backend to Frontend.AFui.py

Future Concepts
1) Create a profile tab. This can be used to house settings and an e-mail address
2) Create Properties Ledger Page
"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

import os
import shutil
import sqlite3

from pathlib import Path
from PySide2.QtWidgets import QMainWindow, QMessageBox
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Slot
from sqlite3 import Error

from Frontend.AFui import Ui_MainWindow

from Backend.Ledger1 import LedgerV1
from Backend.Ledger2 import LedgerV2
from Backend.Summary import Ledger_Summary
from Backend.About import AboutProgram
from Backend.Profile import Profile
from Backend.ArchiveLedger import Archive
from Backend.RequestReport import user_report_request
# from Backend.Scrape import update_stock_price
from Backend.OverTimeGraph import OverTimeGraph

from Toolbox.OS_Tools import file_destination
from Toolbox.AF_Tools import set_networth
from Toolbox.SQL_Tools import check_for_data, create_table, execute_sql_statement_list, specific_sql_statement, obtain_sql_list, obtain_sql_value
from Toolbox.Formatting_Tools import decimal_places, remove_space

from StyleSheets.MainWindowCSS import mainWindow


class AFBackbone(QMainWindow):
    refresh_signal_summary = QtCore.Signal(str)

    def __init__(self, user, messageCount, error_log):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Global Variables
        self.dbPathway = file_destination(['data', 'account'])
        self.dbPathway = Path.cwd() / self.dbPathway / "UAInformation.db"
        self.refUser = user
        self.switchCheck = int(messageCount)

        # This will hold the saved version of the database
        self.saveState = None

        # A true saveToggle equates to being saved.
        self.saveToggle = False
        # Data Check is a Legacy Variable that isn't in use.
        self.dataCheck = None

        # Dictionary used to determine what Tabs are open currently. Prevents duplicates
        self.tabdic = {}

        # Program Error Logger
        self.error_Logger = error_log

        # obtain e-mail if it exists
        email_Statement = f"SELECT Email FROM Users WHERE Profile='{self.refUser}'"
        email_raw = obtain_sql_value(email_Statement, self.dbPathway, self.error_Logger)
        self.email = email_raw[0]

        # Menu Bar Button Functionality
        # -- -- File - Summary, Generate Report, Export [Future], Save[Future] Close
        self.ui.actionProfile.triggered.connect(lambda: self.switch_tab("Profile"))
        self.ui.actionSummary.triggered.connect(lambda: self.switch_tab("Summary"))
        self.ui.actionGenerate.triggered.connect(lambda: user_report_request(self.refUserDB, self.refUser, self.error_Logger))
        self.ui.actionNWG.triggered.connect(lambda: self.switch_tab("OTG"))
        self.ui.actionSave.triggered.connect(lambda: self.save_database(close=False))
        self.ui.actionClose.triggered.connect(self.close_app)
        # -- Assets - Bank, Equity, Retirement, CD, TB
        self.ui.actionBank.triggered.connect(lambda: self.switch_tab("Bank"))
        self.ui.actionEquity.triggered.connect(lambda: self.switch_tab("Equity"))
        self.ui.actionProperty.triggered.connect(lambda: self.switch_tab("Property"))
        self.ui.actionRetirement.triggered.connect(lambda: self.switch_tab("Retirement"))
        self.ui.actionCertificate_of_Deposit.triggered.connect(lambda: self.switch_tab("CD"))
        self.ui.actionTreasury_Bonds.triggered.connect(lambda: self.switch_tab("Treasury"))
        self.ui.actionCash.triggered.connect(lambda: self.switch_tab("Cash"))
        # -- Liabilities - Debt, CC, DC[Future], Cash[Future]
        self.ui.actionDebt.triggered.connect(lambda: self.switch_tab("Debt"))
        self.ui.actionCredit_Cards.triggered.connect(lambda: self.switch_tab("Credit"))
        self.ui.actionAbout.triggered.connect(lambda: self.switch_tab("About"))
        self.ui.actionArchive.triggered.connect(lambda: self.switch_tab("Archive"))
        self.ui.actionUserManual.triggered.connect(self.user_manual)

        # Creation of a New User
        if self.create_profile_db():

            # ParentType: [Example Account Name, Example Account Type, [Account SubType List]]
            example_accounts_dict = {
                "Bank": ["Example Banking Account", "Checking", ["Checking", "Savings", "Money Market"]],
                "Cash": ["Example Wallet", "Wallet", ["Wallet", "Envelope"]],
                "CD": ["Example CD Account", "12 Month", ["12 Month", "2 Year", "3 Year", "4 Year", "5 Year"]],
                "Treasury": ["Example Treasury Bond", "E Bond", ["E Bond", "EE Bond"]],
                "Credit": ["Example Credit Card Account", "Visa", ["Visa", "Mastercard", "Discover", "American Express"]],
                "Debt": ["Example Debt Account", "Student Loan", ["Student Loan", "Personal Loan", "Mortgage", "Car Loan"]],
                "Equity": ["Example Equity Account", "Stock", ["Stock", "ETF", "Mutual Fund"]],
                "Retirement": ["Example Retirement Account", "Traditional 401K", ["Traditional 401K", "Roth 401K", "Traditional IRA", "Roth IRA"]],
                "Property": ["Example Home", "Single Occupancy", ["Single Occupancy", "Rental", "Vacation", "Duplex"]],
            }

            self.initial_categories(["Initial", "Statement"], ["Bank", "Equity", "Retirement", "CD", "Treasury", "Debt", "Credit", "Cash", "Property"], self.saveState)

            for parentType in example_accounts_dict:
                self.account_subtypes(example_accounts_dict[parentType][2], parentType, self.saveState)

                # Account Summary Function (below) designed for use with example accounts.
                summaryStatement = "CREATE TABLE IF NOT EXISTS Account_Summary(ID TEXT, ItemType TEXT, ParentType TEXT, SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
                specific_sql_statement(summaryStatement, self.saveState, self.error_Logger)
                self.account_details(parentType, self.saveState, toggle_example=False, subtype='')  # Subtype had no effect when not creating an example account

                # Example accounts are great for debugging and testing. However, for actual users probably just annoying
                # self.account_ledger(example_accounts_dict[parentType][0], parentType)
                # self.account_summary(example_accounts_dict[parentType][0], parentType)
                # self.account_details(example_accounts_dict[parentType][0], example_accounts_dict[parentType][1], parentType, toggle_example=True)

            archiveStatement = "CREATE TABLE IF NOT EXISTS Account_Archive(ID TEXT, ItemType TEXT, ParentType TEXT," \
                               " SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
            nw_graph_statement = "CREATE TABLE IF NOT EXISTS NetWorth(Date TEXT, Gross TEXT, Liabilities TEXT, Net TEXT)"
            ov_graph_statement = "CREATE TABLE IF NOT EXISTS AccountWorth(Date TEXT)"
            contribution_graph_statement = "CREATE TABLE IF NOT EXISTS ContributionTotals(Date TEXT)"
            execute_sql_statement_list([archiveStatement,
                                        nw_graph_statement,
                                        ov_graph_statement,
                                        contribution_graph_statement], self.saveState, self.error_Logger)

        # Swap over to temporary Database
        # This will hold the temporary/active version of the database
        temp_pathway = self.saveState[:-3] + "-temp.db"
        shutil.copyfile(self.saveState, temp_pathway)
        self.refUserDB = temp_pathway

        if self.email is None:  # Intended to help prevent a case where the user can not reclaim their password
            profile = Profile(self.refUser, self.error_Logger)
            self.ui.mdiArea.addSubWindow(profile)
            profile.remove_tab_profile.connect(self.remove_tab)
            profile.showMaximized()
            self.tabdic.update({"Profile": profile})

        else:
            summary = Ledger_Summary(self, self.refUserDB, self.error_Logger)
            self.ui.mdiArea.addSubWindow(summary)
            summary.remove_tab_LS.connect(self.remove_tab)
            summary.showMaximized()
            self.tabdic.update({"Summary": summary})
            self.statusBar().showMessage("Operational")

        # Initialize appearance upon Loading
        self.setStyleSheet(mainWindow)
        self.statusBar().showMessage("Stock Prices Updated")

        netWorth = set_networth(self.refUserDB, "Account_Summary", toggleformatting=True)
        self.ui.labelNW.setText(netWorth[1])
        self.ui.labelTAssests.setText(netWorth[2])
        self.ui.labelTLiabilities.setText(netWorth[3])

        snapshot = set_networth(self.refUserDB, "Account_Summary", toggleformatting=False)
        self.log_netWorth(snapshot, "Login")

    def acquire_key(self):
        keyStatement = f"SELECT UserKey FROM Users WHERE Profile ='{self.refUser}'"
        try:
            conn = sqlite3.connect(self.dbPathway)
            with conn:
                cur = conn.cursor()
                cur.execute(keyStatement)
                row = cur.fetchone()
                if row is None:
                    self.statusBar().showMessage("ERROR: MISSING USER KEY")
                else:
                    key = str(row[0])
        except Error:
            error_string = f"""ERROR: AFBackbone: acquireKey \n statement: "{keyStatement}" \n Profile: "{self.refUser}" \n Database: "{self.refUserDB}" """
            self.error_Logger.error(error_string)
        finally:
            conn.close()
            return key

    def create_profile_db(self):
        key = self.acquire_key()
        databaseFN = "db" + key + "rf.dat"                                                  # database File Name
        userDbPathway = file_destination(['data', 'account'])
        databaseFN_Pathway = Path.cwd() / userDbPathway / databaseFN
        databaseN = self.create_db_name()                                                   # database Name
        databaseN_Pathway = Path.cwd() / userDbPathway / databaseN
        try:
            with open(databaseFN_Pathway, mode="rb") as f:
                codedDN = f.read()
                self.saveState = codedDN.decode('utf-8')
                # DataCheck is legacy Variable not currently in use.
                self.dataCheck = ("Opened File: " + self.saveState + " User Key: "
                                  + key + " User Name: " + str(self.refUser))
                f.close()
                return False
        except IOError:
            with open(databaseFN_Pathway, mode="wb") as nf:
                databaseN_Pathway_string = str(databaseN_Pathway)
                nf.write(databaseN_Pathway_string.encode('utf-8'))
                nf.close()
                self.saveState = databaseN_Pathway_string
                # DataCheck is legacy Variable not currently in use.
                self.dataCheck = ("New File Made: " + str(self.saveState))
                return True

    def create_db_name(self):
        from random import shuffle
        key = self.acquire_key()
        databaseName = ""
        nameList = []
        countUser = len(self.refUser) - 1
        countKey = len(key) - 1
        while countUser >= 0:
            nameList.append(self.refUser[countUser])
            countUser -= 1
        while countKey >= 0:
            nameList.append(key[countKey])
            countKey -= 1
        shuffle(nameList)
        for piece in nameList:
            databaseName = databaseName + piece
        databaseName = databaseName + ".db"
        return databaseName

    def save_database(self, close=False):
        if not self.saveToggle:
            save_mesg = "Do you wish to save your current information?"
            reply = QMessageBox.question(self, "Save Account", save_mesg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                shutil.copyfile(self.refUserDB, self.saveState)
                complete_mesg = "You work has been saved."
                done = QMessageBox.information(self, "Save Complete", complete_mesg, QMessageBox.Close, QMessageBox.NoButton)
                if done == QMessageBox.Close:
                    self.saveToggle = True
            else:
                if close:
                    doubleCheck = "Are you sure?"
                    usercheck = QMessageBox.question(self, "Save Before Close", doubleCheck, QMessageBox.Yes, QMessageBox.No)
                    if usercheck == QMessageBox.Yes:
                        pass
                    else:
                        self.save_database(close=True)

        else:
            unnecessary = "Your information was already saved."
            done = QMessageBox.information(self, "Save Complete", unnecessary, QMessageBox.Close, QMessageBox.NoButton)
            if done == QMessageBox.Close:
                pass

    def close_app(self):
        quit_msg = "Are you sure you want to quit the program?"
        reply = QMessageBox.question(self, 'Quit Message', quit_msg, QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            pass

    def closeEvent(self, event):
        event.ignore()
        snapshot = set_networth(self.refUserDB, "Account_Summary", toggleformatting=False)
        self.log_netWorth(snapshot, "Logout")

        if self.saveToggle:
            event.accept()
        else:
            self.save_database(close=True)
            os.remove(self.refUserDB)
            event.accept()

    def switch_tab(self, parentType):
        type1 = ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit", "Property"]
        type2 = ["Equity", "Retirement"]
        try:
            self.tabdic[parentType].setFocus()
        except KeyError:
            if parentType == "Summary":
                summary = Ledger_Summary(self, self.refUserDB, self.error_Logger)
                self.ui.mdiArea.addSubWindow(summary)
                summary.remove_tab_LS.connect(self.remove_tab)
                summary.showMaximized()
                self.tabdic.update({parentType: summary})
            elif parentType == "Profile":
                profile = Profile(self.refUser, self.error_Logger)
                self.ui.mdiArea.addSubWindow(profile)
                profile.remove_tab_profile.connect(self.remove_tab)
                profile.showMaximized()
                self.tabdic.update({parentType: profile})
            elif parentType in type1:
                ledger = LedgerV1(self.refUserDB, parentType, self.refUser, self.error_Logger)
                self.ui.mdiArea.addSubWindow(ledger)
                ledger.refresh_signal.connect(self.refresh_netWorth)
                ledger.remove_tab.connect(self.remove_tab)
                ledger.showMaximized()
                self.tabdic.update({parentType: ledger})
            elif parentType in type2:
                ledger2 = LedgerV2(self.refUserDB, parentType, self.refUser, self.error_Logger)
                self.ui.mdiArea.addSubWindow(ledger2)
                ledger2.refresh_signal_L2.connect(self.refresh_netWorth)
                ledger2.remove_tab_L2.connect(self.remove_tab)
                ledger2.showMaximized()
                self.tabdic.update({parentType: ledger2})
            elif parentType == "About":
                about = AboutProgram()
                self.ui.mdiArea.addSubWindow(about)
                about.remove_tab_about.connect(self.remove_tab)
                about.showMaximized()
                self.tabdic.update({parentType: about})
            elif parentType == "Archive":
                archive = Archive(self.refUserDB, self.refUser, self.error_Logger)
                self.ui.mdiArea.addSubWindow(archive)
                archive.remove_tab_archive.connect(self.remove_tab)
                archive.showMaximized()
                self.tabdic.update({parentType: archive})
            elif parentType == "OTG":
                graph = OverTimeGraph(self, self.refUserDB, self.error_Logger)
                self.ui.mdiArea.addSubWindow(graph)
                graph.remove_tab_OTG.connect(self.remove_tab)
                graph.showMaximized()
                self.tabdic.update({parentType: graph})
            else:
                print(f"""ERROR: AFMainWindow: switch_tab \n Input Error -- Variable = {parentType}""")

    def account_ledger(self, accountName, parentType):
        finalName = remove_space(accountName)
        variant1 = ["Bank", "CD", "Treasury", "Debt", "Credit", "Cash"]
        variant2 = ["Equity", "Retirement"]
        # Property will not have a 'ledger' as the mortgage counts as the Debt.
        if parentType in variant1:
            ledgerStatement = "CREATE TABLE IF NOT EXISTS " + finalName + \
                            "(Transaction_Date NUMERIC, Transaction_Method TEXT," \
                            " Transaction_Description TEXT, Category TEXT, Debit REAL, Credit REAL, Balance REAL, Note TEXT," \
                            " Status TEXT, Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            specific_sql_statement(ledgerStatement, self.refUserDB, self.error_Logger)
        elif parentType in variant2:
            ledgerStatement = "CREATE TABLE IF NOT EXISTS " + finalName + \
                              "(Transaction_Date NUMERIC, Transaction_Description TEXT, Category TEXT," \
                              " Debit REAL, Credit REAL, Sold REAL, Purchased REAL, Price REAL, Note TEXT, Status TEXT," \
                              " Receipt TEXT, Post_Date NUMERIC, Update_Date NUMERIC)"
            specific_sql_statement(ledgerStatement, self.refUserDB, self.error_Logger)

    def account_summary(self, accountName: str, accountType: str):
        """Single use Function: Creates Account Summary Table, then adds example accounts to the table. Used for Asset, Liability, and Net Worth Calculations"""

        summaryStatement = "CREATE TABLE IF NOT EXISTS Account_Summary(ID TEXT, ItemType TEXT, ParentType TEXT, SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
        specific_sql_statement(summaryStatement, self.refUserDB, self.error_Logger)
        if check_for_data("Account_Summary", "ParentType", accountType, self.refUserDB, self.error_Logger) is True:
            exampleStatement = f"INSERT INTO Account_Summary VALUES('{accountName}', NULL, '{accountType}', NULL, NULL, '0.00')"
            specific_sql_statement(exampleStatement, self.refUserDB, self.error_Logger)

    def account_details(self, parentType, database, toggle_example, subtype, accountName="Example_Account"):
        """ Single use Function: Used to Create Parent Type Account Details Table, and Example Account Details
            These details are intended to be Parent Type specific while the Account Summary Table it more general

            Admittance - These tables could be wrapped into the summary table. However, they were created to minimize the number
            of empty columns and null values.
        """
        from datetime import datetime
        currentDate = datetime.now().strftime("%m/%d/%Y")

        itemTypeDict = {
            "Bank": ["Asset", "Bank_Account_Details"],
            "Cash": ["Asset", "Cash_Account_Details"],
            "CD": ["Asset", "CD_Account_Details"],
            "Treasury": ["Asset", "Treasury_Account_Details"],
            "Credit": ["Liability", "Credit_Account_Details"],
            "Debt": ["Liability", "Debt_Account_Details"],
            "Equity": ["Asset", "Equity_Account_Details"],
            "Retirement": ["Asset", "Retirement_Account_Details"],
            "Property": ["Asset", "Property_Account_Details"],
        }

        # Sector will not correspond with the AccountDetails Window order. This was done due to post add, and to keep consistency for the first 4-5 Columns.
        detailsTableDict = {
            "Bank": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL)",
            "Cash": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER)",
            "CD": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL, Maturity_Date NUMERIC)",
            "Treasury": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL, Maturity_Date NUMERIC)",
            "Credit": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Credit_Limit INTEGER)",
            "Debt": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Interest_Rate REAL, Starting_Balance REAL)",
            "Equity": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Ticker_Symbol TEXT, Stock_Price REAL, Sector TEXT)",
            "Retirement": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Owner TEXT, Bank TEXT, Statement_Date INTEGER, Ticker_Symbol TEXT, Stock_Price REAL, Sector TEXT)",
            "Property": f"CREATE TABLE IF NOT EXISTS {itemTypeDict[parentType][1]} (Account_Name TEXT, Account_Type TEXT, Primary_Ownder TEXT, Bank TEXT, Address_1 TEXT, County TEXT, State_Initials TEXT, Zip_Code INTEGER, Image TEXT)",
        }

        if toggle_example is True:
            if parentType == "Equity" or parentType == "Retirement":
                summaryStatement = f"UPDATE Account_Summary SET SubType='{subtype}', ItemType='{itemTypeDict[parentType][0]}', Ticker_Symbol='AFB' WHERE ID='{accountName}'"
            else:
                summaryStatement = f"UPDATE Account_Summary SET SubType='{subtype}', ItemType='{itemTypeDict[parentType][0]}' WHERE ID='{accountName}'"

            detailsValueDict= {
                "Bank": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', 'Alchemical Finances Bank', '1','1.00')",
                "Cash": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', 'Alchemical Finances Bank', '1')",
                "CD": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', 'Alchemical Finances Bank', ',1', '1.00', '{currentDate}')",
                "Treasury": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', 'Alchemical Finances Bank', '1', '1.00',, '{currentDate}')",
                "Credit": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', 'Alchemical Finances Bank', '1', '10000')",
                "Debt": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', 'Alchemical Finances Bank', '1', '1.00', '10000')",
                "Equity": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', 'Unspecified', '{self.refUser}', 'Alchemical Finances Bank', '1', 'AFB',  '1.0000')",
                "Retirement": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', 'Unspecified', '{self.refUser}', 'Alchemical Finances Bank', '1', 'AFB',  '1.0000')",
                "Property": f"INSERT INTO {itemTypeDict[parentType][1]} VALUES('{accountName}', '{subtype}', '{self.refUser}', '123 Finance Street', 'County', 'State 91002', NULL)",
            }
            specific_sql_statement(detailsTableDict[parentType], database, self.error_Logger)
            if check_for_data(itemTypeDict[parentType][1], "Account_Name", accountName, database, self.error_Logger) is True:
                specific_sql_statement(detailsValueDict[parentType], database, self.error_Logger)
                specific_sql_statement(summaryStatement, database, self.error_Logger)
        else:
            specific_sql_statement(detailsTableDict[parentType], database, self.error_Logger)

    def initial_categories(self, methodList, typeList, database):
        """ Single Use Function: Used to create the starting spending Categories for each Parent Type"""
        create_table("Categories", ["Method", "ParentType", "Tabulate"], ["TEXT", "TEXT", "BOOL"], database, self.error_Logger)
        if check_for_data("Categories", "ParentType", typeList[0], database, self.error_Logger) is True:
            statementList = []
            for method in methodList:
                for catType in typeList:
                    statement = f"INSERT INTO Categories VALUES('{method}', '{catType}', 'True')"
                    statementList.append(statement)
            execute_sql_statement_list(statementList, database, self.error_Logger)
        else:
            pass

    def account_subtypes(self, subTypes, parentType, database):
        """ Single Use Function: Used to create the starting list of Account Sub Types for each Parent Type"""
        create_table("AccountSubType", ["SubType", "ParentType"], ["TEXT", "TEXT"], database, self.error_Logger)
        if check_for_data("AccountSubType", "ParentType", parentType, database, self.error_Logger) is True:
            statementList = []
            for account in subTypes:
                dbStatement = f"INSERT INTO AccountSubType VALUES('{account}', '{parentType}')"
                statementList.append(dbStatement)
            execute_sql_statement_list(statementList, database, self.error_Logger)
        else:
            pass

    def log_contributions(self, action, date):
        """ Obtain Equity and Retirement Contribution sums for the Contributions Table"""
        select_target_accounts = "SELECT ID FROM Account_Summary WHERE ParentType='Equity' or ParentType='Retirement'"
        target_accounts_raw = obtain_sql_list(select_target_accounts, self.refUserDB, self.error_Logger)

        if action == "Insert":
            insert_date = f"INSERT INTO ContributionTotals(Date) VALUES('{date}')"
            specific_sql_statement(insert_date, self.refUserDB, self.error_Logger)
        else:
            pass

        for account in target_accounts_raw:
            account = account[0]
            sql_account = remove_space(account)
            contribution_statement = f"SELECT SUM(Credit - Debit) FROM '{sql_account}'"
            contribution_sum_raw = obtain_sql_value(contribution_statement, self.refUserDB, self.error_Logger)

            if contribution_sum_raw[0] is None:
                contribution_sum_checked = 0
            else:
                contribution_sum_checked = contribution_sum_raw[0]

            contribution_sum = str(decimal_places(contribution_sum_checked, 2))

            insert_contribution = f"UPDATE ContributionTotals SET '{sql_account}'={contribution_sum} WHERE Date='{date}'"
            specific_sql_statement(insert_contribution, self.refUserDB, self.error_Logger)

    def log_netWorth(self, data, entryPoint):
        """ Adds Finance Data points [Gross, Liabilities, Net] to NetWorth Table
            Expanded to input data into AccountWorth and ContributionsTotals

            all intended for Graphing over time
        """
        from datetime import datetime, timedelta

        updated = False

        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.strftime("%Y/%m/%d")
        today = today.strftime("%Y/%m/%d")

        # Data = [Assets, Liabilities, Net] -- NetWorth = [Gross, Liabilities, Net]
        # NetWorth Table Structure (Date TEXT, Gross TEXT, Liabilities TEXT, Net TEXT)
        insert_today_statement = f"INSERT INTO NetWorth Values('{today}', '{data[0]}', '{data[1]}', '{data[2]}')"
        insert_yesterday_statement = f"INSERT INTO NetWorth Values('{yesterday}', '{data[0]}', '{data[1]}', '{data[2]}')"
        update_statement = f"UPDATE NetWorth SET Gross='{data[0]}', Liabilities='{data[1]}', Net='{data[2]}' WHERE Date='{today}'"

        last_data_point_Statement = f"SELECT Date FROM Networth ORDER BY Date DESC LIMIT 1"
        last_data_point = obtain_sql_value(last_data_point_Statement, self.refUserDB, self.error_Logger)

        account_balances_statement = "SELECT ID, Balance FROM Account_Summary"
        account_balances_raw = obtain_sql_list(account_balances_statement, self.refUserDB, self.error_Logger)

        if last_data_point is None:
            last_data_point = "1978/01/01"  # Just an unlikely date

        if updated is False:
            if entryPoint == "Login" and today == last_data_point[0]:
                for account in account_balances_raw:
                    update_account_statement = f"UPDATE AccountWorth SET '{remove_space(account[0])}'='{account[1]}' WHERE Date='{today}'"
                    specific_sql_statement(update_account_statement, self.refUserDB, self.error_Logger)

                specific_sql_statement(update_statement, self.refUserDB, self.error_Logger)
                updated = True

                self.log_contributions("Update", today)

                print(f"Finances inserted for {today}")

        if updated is False:
            if entryPoint == "Login" and today != last_data_point[0] and yesterday != last_data_point[0]:
                # Insert current values for yesterday
                insertDate_accountWorth_table = f"INSERT INTO AccountWorth(Date) VALUES('{yesterday}')"
                specific_sql_statement(insertDate_accountWorth_table, self.refUserDB, self.error_Logger)
                for account in account_balances_raw:
                    update_account_statement = f"UPDATE AccountWorth SET '{remove_space(account[0])}'='{account[1]}' WHERE Date='{yesterday}'"
                    specific_sql_statement(update_account_statement, self.refUserDB, self.error_Logger)

                specific_sql_statement(insert_yesterday_statement, self.refUserDB, self.error_Logger)
                self.log_contributions("Insert", yesterday)

                print(f"Finances inserted for {yesterday}")

                # Follow by insert today
                insertDate_accountWorth_table = f"INSERT INTO AccountWorth(Date) VALUES('{today}')"
                specific_sql_statement(insertDate_accountWorth_table, self.refUserDB, self.error_Logger)
                for account in account_balances_raw:
                    update_account_statement = f"UPDATE AccountWorth SET '{remove_space(account[0])}'='{account[1]}' WHERE Date='{today}'"
                    specific_sql_statement(update_account_statement, self.refUserDB, self.error_Logger)

                specific_sql_statement(insert_today_statement, self.refUserDB, self.error_Logger)
                self.log_contributions("Insert", today)
                updated = True

                print(f"Finances inserted for {today}")

        if updated is False:
            if entryPoint == "Login" and today != last_data_point[0] and yesterday == last_data_point[0]:
                insertDate_accountWorth_table = f"INSERT INTO AccountWorth(Date) VALUES('{today}')"
                specific_sql_statement(insertDate_accountWorth_table, self.refUserDB, self.error_Logger)
                for account in account_balances_raw:
                    update_account_statement = f"UPDATE AccountWorth SET '{remove_space(account[0])}'='{account[1]}' WHERE Date='{today}'"
                    specific_sql_statement(update_account_statement, self.refUserDB, self.error_Logger)

                specific_sql_statement(insert_today_statement, self.refUserDB, self.error_Logger)
                self.log_contributions("Insert", today)
                updated = True

                print(f"Finances inserted for {today}")

        if updated is False:
            if entryPoint == "Logout":
                for account in account_balances_raw:
                    update_account_statement = f"UPDATE AccountWorth SET '{remove_space(account[0])}'='{account[1]}' WHERE Date='{today}'"
                    specific_sql_statement(update_account_statement, self.refUserDB, self.error_Logger)

                specific_sql_statement(update_statement, self.refUserDB, self.error_Logger)
                self.log_contributions("Update", today)
                updated = True
                print(f"Finances updated for {today}")

    def user_manual(self):
        user_manual_path = Path.cwd() / "Resources" / "USER_MANUAL.pdf"
        user_manual_str = str(user_manual_path)
        os.startfile(user_manual_str)

    @Slot(str)
    def refresh_netWorth(self, message):
        """ formats and updates Net Worth values"""
        if message == "1":
            netWorth = set_networth(self.refUserDB, "Account_Summary", toggleformatting=True)
            self.ui.labelNW.setText(netWorth[1])
            self.ui.labelTAssests.setText(netWorth[2])
            self.ui.labelTLiabilities.setText(netWorth[3])
            self.saveToggle = False
            self.trigger_refresh_summer()
        else:
            pass

    @Slot(str)
    def remove_tab(self, message):
        """ Function to remove tab from MDIarea"""
        try:
            self.ui.mdiArea.removeSubWindow(self.tabdic[message])
            self.tabdic.pop(message)
        except KeyError:
            self.statusBar().showMessage(f"""ERROR: AFMainWindow: remove_tab \n message: {message} \n tabledic contents: {self.tabdic}""")

    def trigger_refresh_summer(self):
        """ Signal to trigger the Summary QDialog to refresh Account Balances """
        self.refresh_signal_summary.emit("2")


if __name__ == "__main_":
    print("error")
