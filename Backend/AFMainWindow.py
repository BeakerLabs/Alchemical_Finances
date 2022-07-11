#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import pandas as pd
import pickle
import shutil
import sqlite3
import time

from datetime import date, datetime, timedelta
from pathlib import Path
from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QDialog, QMessageBox
from sqlite3 import Error

from Frontend.AFui import Ui_MainWindow

from StyleSheets.MainWindowCSS import mainWindow

from Backend.About import AboutProgram
from Backend.ArchiveLedger import Archive
from Backend.DataFrame import contribution_balance, create_DF_dict, load_df_ledger
from Backend.EquityUpdate import obtain_equity_prices
from Backend.Ledger1 import LedgerV1
from Backend.Ledger2 import LedgerV2
from Backend.Manual import UserManual
from Backend.OverTimeGraph import OverTimeGraph
from Backend.Profile import Profile
from Backend.RequestReport import user_report_request
from Backend.SaveDataFrame import SaveProgress
from Backend.Summary import Ledger_Summary

from Toolbox.AF_Tools import set_networth
from Toolbox.Formatting_Tools import decimal_places, remove_comma, remove_space
from Toolbox.OS_Tools import file_destination, obtain_storage_dir
from Toolbox.SQL_Tools import check_for_data, create_table, execute_sql_statement_list, specific_sql_statement, obtain_sql_list, obtain_sql_value

class AFBackbone(QMainWindow):
    refresh_signal_summary = QtCore.Signal(str)
    refresh_signal_OTG = QtCore.Signal(str)

    def __init__(self, user, messageCount, error_log):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Global Variables
        self.storage_dir = obtain_storage_dir()
        self.dbPathway = file_destination(['Alchemical Finances', 'Data', 'account'], starting_point=self.storage_dir)
        self.dbPathway = Path(self.dbPathway) / "UAInformation.db"
        self.refUser = user
        self.switchCheck = int(messageCount)
        self.error_Logger = error_log

        self.today = date.today()
        self.today = self.today.strftime("%Y/%m/%d")

        # This will hold the saved version of the database
        self.saveState = None

        # A true saveToggle equates to being saved.
        self.saveToggle = False
        # Data Check is a Legacy Variable that isn't in use.
        self.dataCheck = None

        # Dictionary used to determine what Tabs are open currently to prevent duplicate instances
        self.tabdic = {}

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
        # -- Liabilities - Debt, CC
        self.ui.actionDebt.triggered.connect(lambda: self.switch_tab("Debt"))
        self.ui.actionCredit_Cards.triggered.connect(lambda: self.switch_tab("Credit"))
        # -- Tools -- Archive, Budget [Future]
        self.ui.actionArchive.triggered.connect(lambda: self.switch_tab("Archive"))
        self.ui.actionBudgeting.triggered.connect(lambda: self.switch_tab("Budget"))
        # -- Other -- About
        self.ui.actionUserManual.triggered.connect(self.user_manual)
        self.ui.actionAbout.triggered.connect(lambda: self.switch_tab("About"))

        creation_container = self.create_profile_db()

        # Creation of a New User
        if creation_container:

            # ParentType: [Example Account Name, Example Account Type, [Account SubType List]]
            initial_subtypes_dict = {
                "Bank": ["Checking", "Savings", "Money Market"],
                "Cash": ["Wallet", "Envelope"],
                "CD": ["12 Month", "2 Year", "3 Year", "4 Year", "5 Year"],
                "Treasury": ["E Bond", "EE Bond"],
                "Credit": ["Visa", "Mastercard", "Discover", "American Express"],
                "Debt": ["Student Loan", "Personal Loan", "Mortgage", "Car Loan"],
                "Equity": ["Stock", "ETF", "Mutual Fund"],
                "Retirement": ["Traditional 401K", "Roth 401K", "Traditional IRA", "Roth IRA"],
                "Property": ["Single Occupancy", "Rental", "Vacation", "Duplex"],
            }

            self.initial_categories(["Initial", "Statement"], ["Bank", "Equity", "Retirement", "CD", "Treasury", "Debt", "Credit", "Cash", "Property"], self.saveState)

            for parentType in initial_subtypes_dict:
                self.account_subtypes(initial_subtypes_dict[parentType], parentType, self.saveState)

                summaryStatement = "CREATE TABLE IF NOT EXISTS Account_Summary(ID TEXT, ItemType TEXT, ParentType TEXT, SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
                specific_sql_statement(summaryStatement, self.saveState, self.error_Logger)
                self.account_details(parentType, self.saveState)

            archiveStatement = "CREATE TABLE IF NOT EXISTS Account_Archive(ID TEXT, ItemType TEXT, ParentType TEXT," \
                               " SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
            nw_graph_statement = "CREATE TABLE IF NOT EXISTS NetWorth(Date TEXT, Gross TEXT, Liabilities TEXT, Net TEXT)"
            ov_time_graph_statement = "CREATE TABLE IF NOT EXISTS AccountWorth(Date TEXT)"
            contribution_graph_statement = "CREATE TABLE IF NOT EXISTS ContributionTotals(Date TEXT)"
            delete_acc_statement = "CREATE TABLE IF NOT EXISTS DeletePending(ID TEXT, ParentType TEXT)"
            execute_sql_statement_list([archiveStatement,
                                        nw_graph_statement,
                                        ov_time_graph_statement,
                                        delete_acc_statement,
                                        contribution_graph_statement], self.saveState, self.error_Logger)

        # No else statement for the creation of a new profile. Not necessary if database already exists

        # Swap over to temporary Database
        # This will hold the temporary/active version of the database
        temp_pathway = self.saveState[:-3] + "-temp.db"
        shutil.copyfile(self.saveState, temp_pathway)
        self.refUserDB = temp_pathway

        # Create dataframe dictionary
        account_dictionary = create_DF_dict(self.refUserDB, self.error_Logger)
        self.ledger_container = self.create_dataframe_container(account_dictionary)  # Used with ledgers but created upon sign-in
        del account_dictionary  # unnecessary usage of memory after creation of the container.

        # Update Equity values [Today/Yesterday] and Record for start of session.
        self.log_netWorth("Login")

        if self.email is None:  # Intended to help prevent a case where the user can not reclaim their password
            profile = Profile(self.refUser, self.error_Logger)
            self.ui.mdiArea.addSubWindow(profile)
            profile.remove_tab_profile.connect(self.remove_tab)
            profile.showMaximized()
            self.tabdic.update({"Profile": profile})

        else:
            summary = Ledger_Summary(self, self.refUserDB, self.ledger_container, self.error_Logger)
            self.ui.mdiArea.addSubWindow(summary)
            summary.remove_tab_LS.connect(self.remove_tab)
            summary.showMaximized()
            self.tabdic.update({"Summary": summary})
            self.statusBar().showMessage("Operational")

        # Initialize appearance upon Loading
        self.setStyleSheet(mainWindow)
        self.statusBar().showMessage("Stock Prices Updated")

        # Display Net Worth now with updated Equity Values
        netWorth = set_networth(self.refUserDB, "Account_Summary", toggleformatting=True)
        self.ui.labelNW.setText(netWorth[1])
        self.ui.labelTAssests.setText(netWorth[2])
        self.ui.labelTLiabilities.setText(netWorth[3])

        if self.switchCheck == 0:
            self.user_manual()

    def account_details(self, parentType, database):
        """ Single use Function: Used to Create Parent Type Account Details Table
            These details are intended to be Parent Type specific while the Account Summary Table it more general

            Admittance - These tables could be wrapped into the summary table. However, they were created to minimize the number
            of empty columns and null values.
        """

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

        specific_sql_statement(detailsTableDict[parentType], database, self.error_Logger)

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

    def account_summary(self, accountName: str, accountType: str):
        """Single use Function: Creates Account Summary Table, then adds example accounts to the table. Used for Asset, Liability, and Net Worth Calculations"""

        summaryStatement = "CREATE TABLE IF NOT EXISTS Account_Summary(ID TEXT, ItemType TEXT, ParentType TEXT, SubType TEXT, Ticker_Symbol TEXT, Balance REAL)"
        specific_sql_statement(summaryStatement, self.refUserDB, self.error_Logger)
        if check_for_data("Account_Summary", "ParentType", accountType, self.refUserDB, self.error_Logger) is True:
            exampleStatement = f"INSERT INTO Account_Summary VALUES('{accountName}', NULL, '{accountType}', NULL, NULL, '0.00')"
            specific_sql_statement(exampleStatement, self.refUserDB, self.error_Logger)

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

    def close_app(self):
        quit_msg = "Are you sure you want to quit the program?"
        reply = QMessageBox.question(self, 'Quit Message', quit_msg, QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            pass

    def closeEvent(self, event):
        event.ignore()
        self.log_netWorth("Logout")

        if not self.saveToggle:
            self.save_database(close=True)

        os.remove(self.refUserDB)
        os.remove(self.ledger_container)
        event.accept()

    def create_dataframe_container(self, dictionary):
        key = self.acquire_key()
        containerFN = "df" + key + "rf.pkl"
        dfPathway = Path(self.storage_dir) / 'Alchemical Finances' / 'data' / 'account' / containerFN

        if os.path.exists(dfPathway):
            os.remove(dfPathway)
            # dataframe container should not exist unless program didn't close properly.
            # dataframe container is only used during active session. Long term storage is in database

        with open(dfPathway, mode="wb") as nf:
            pickle.dump(dictionary, nf)
            nf.close()

        return dfPathway

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

    def create_profile_db(self):
        key = self.acquire_key()
        databaseFileName = "db" + key + "rf.dat"
        userDbPathway = file_destination(['Alchemical Finances', 'data', 'account'], starting_point=self.storage_dir)
        databaseFN_Pathway = Path(userDbPathway) / databaseFileName
        databaseName = self.create_db_name()
        databaseName_Pathway = Path(userDbPathway) / databaseName

        try:
            with open(databaseFN_Pathway, mode="rb") as f:
                codedDN = f.read()
                self.saveState = codedDN.decode('utf-8')
                # DataCheck is legacy Variable not currently in use.
                # self.dataCheck = ("Opened File: " + self.saveState + " User Key: "
                #                   + key + " User Name: " + str(self.refUser))
                # print(self.dataCheck)
                f.close()
                return False
        except IOError:
            with open(databaseFN_Pathway, mode="wb") as nf:
                databaseN_Pathway_string = str(databaseName_Pathway)
                nf.write(databaseN_Pathway_string.encode('utf-8'))
                nf.close()
                self.saveState = databaseN_Pathway_string
                # DataCheck is legacy Variable not currently in use.
                self.dataCheck = ("New File Made: " + str(self.saveState))
                return True

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

    def log_contributions(self, action, instanceDate):
        """ Obtain Equity and Retirement Contribution sums for the Contributions Table"""
        select_target_accounts = "SELECT ID FROM Account_Summary WHERE ParentType='Equity' or ParentType='Retirement'"
        target_accounts_raw = obtain_sql_list(select_target_accounts, self.refUserDB, self.error_Logger)

        if action == "Insert":
            insert_date = f"INSERT INTO ContributionTotals(Date) VALUES('{instanceDate}')"
            specific_sql_statement(insert_date, self.refUserDB, self.error_Logger)
        else:
            pass

        for account in target_accounts_raw:
            account = account[0]
            sql_account = remove_space(account)

            account_df = load_df_ledger(self.ledger_container, account)
            contribution_sum_raw = contribution_balance(account_df)

            if contribution_sum_raw is None:
                contribution_sum_checked = 0
            else:
                contribution_sum_checked = contribution_sum_raw

            contribution_sum = str(decimal_places(contribution_sum_checked, 2))
            insert_contribution = f"UPDATE ContributionTotals SET '{sql_account}'={contribution_sum} WHERE Date='{instanceDate}'"
            specific_sql_statement(insert_contribution, self.refUserDB, self.error_Logger)

    def log_netWorth(self, entryPoint):
        """ Adds Finance Data points [Gross, Liabilities, Net] to NetWorth Table
            Expanded to input data into AccountWorth and ContributionsTotals

            all intended for Graphing over time
        """
        updated = False

        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.strftime("%Y/%m/%d")
        today = today.strftime("%Y/%m/%d")

        # Data = [Assets, Liabilities, Net] -- NetWorth = [Gross, Liabilities, Net]
        # NetWorth Table Structure (Date TEXT, Gross TEXT, Liabilities TEXT, Net TEXT)
        last_data_point_Statement = f"SELECT Date FROM Networth ORDER BY Date DESC LIMIT 1"
        last_data_point = obtain_sql_value(last_data_point_Statement, self.refUserDB, self.error_Logger)

        if last_data_point is None:
            last_data_point = "1978/01/01"  # Just an unlikely date

        if updated is False:
            if entryPoint == "Login" and today != last_data_point[0] and yesterday != last_data_point[0]:
                target = ["Yesterday", "Today", "Insert"]
            elif entryPoint == "Login" and today == last_data_point[0] and yesterday != last_data_point[0]:
                target = [None, "Today", "Update"]
            elif entryPoint == "Login" and today != last_data_point[0] and yesterday == last_data_point[0]:
                target = [None, "Today", "Insert"]
            elif entryPoint == "Logout":
                target = [None, "Today", "Update"]
            else:
                target = [None, None, None]

            if target[0] is None:
                pass
            else:  # "Yesterday"
                self.update_equity(yesterday)
                self.update_networth(yesterday)
                self.update_accountWorth(yesterday)
                self.log_contributions("Insert", yesterday)
                print(f"Finances inserted for yesterday: {yesterday}")

            if target[1] is None:
                pass
            else:  # "Today"
                self.update_equity(today)

                if entryPoint != "Logout":
                    self.log_contributions("Update", today)

                if target[2] == "Update":
                    self.update_networth(today, update=True)
                    self.update_accountWorth(today, update=True)
                    self.log_contributions("Update", today)

                else:  # "Insert"
                    self.update_networth(today)
                    self.update_accountWorth(today)
                    self.log_contributions("Insert", today)

                print(f"Finances {target[2]} for today: {today}")

    def save_database(self, close=False):
        if not self.saveToggle:
            save_mesg = "Do you wish to save your current information?"
            reply = QMessageBox.question(self, "Save Account", save_mesg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                progressDialog = SaveProgress(self.refUser, self.ledger_container, self.refUserDB, self.error_Logger)
                if progressDialog.exec() == QDialog.Accepted:
                    shutil.copyfile(self.refUserDB, self.saveState)
                    time.sleep(1)
                    complete_mesg = "Your work has been saved."
                    done = QMessageBox.information(self, "Save Complete", complete_mesg, QMessageBox.Close, QMessageBox.NoButton)
                    if done == QMessageBox.Close:
                        self.saveToggle = True

            else:
                if close:
                    doubleCheck = "Are you sure?          "
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

    def switch_tab(self, switch: str):
        type1 = ["Bank", "Cash", "CD", "Treasury", "Debt", "Credit", "Property"]
        type2 = ["Equity", "Retirement"]
        try:
            self.tabdic[switch].setFocus()
        except KeyError:
            if switch == "Summary":
                summary = Ledger_Summary(self, self.refUserDB, self.ledger_container, self.error_Logger)
                self.ui.mdiArea.addSubWindow(summary)
                summary.remove_tab_LS.connect(self.remove_tab)
                summary.showMaximized()
                self.tabdic.update({switch: summary})
            elif switch == "Profile":
                profile = Profile(self.refUser, self.error_Logger)
                self.ui.mdiArea.addSubWindow(profile)
                profile.remove_tab_profile.connect(self.remove_tab)
                profile.showMaximized()
                self.tabdic.update({switch: profile})
            elif switch in type1:
                ledger = LedgerV1(self.refUserDB, switch, self.refUser, self.ledger_container, self.error_Logger)
                self.ui.mdiArea.addSubWindow(ledger)
                ledger.refresh_signal.connect(self.refresh_netWorth)
                ledger.remove_tab.connect(self.remove_tab)
                ledger.showMaximized()
                self.tabdic.update({switch: ledger})
            elif switch in type2:
                ledger2 = LedgerV2(self.refUserDB, switch, self.refUser, self.ledger_container, self.error_Logger)
                self.ui.mdiArea.addSubWindow(ledger2)
                ledger2.refresh_signal_L2.connect(self.refresh_netWorth)
                ledger2.remove_tab_L2.connect(self.remove_tab)
                ledger2.showMaximized()
                self.tabdic.update({switch: ledger2})
            elif switch == "About":
                about = AboutProgram()
                self.ui.mdiArea.addSubWindow(about)
                about.remove_tab_about.connect(self.remove_tab)
                about.showMaximized()
                self.tabdic.update({switch: about})
            elif switch == "Archive":
                archive = Archive(self.refUserDB, self.refUser, self.ledger_container, self.error_Logger)
                self.ui.mdiArea.addSubWindow(archive)
                archive.remove_tab_archive.connect(self.remove_tab)
                archive.showMaximized()
                self.tabdic.update({switch: archive})
            elif switch == "OTG":
                graph = OverTimeGraph(self, self.refUserDB, self.error_Logger)
                self.ui.mdiArea.addSubWindow(graph)
                graph.remove_tab_OTG.connect(self.remove_tab)
                graph.showMaximized()
                self.tabdic.update({switch: graph})
            elif switch == "Budget":
                budget_msg = "The Budget application is currently under development."
                read_msg = QMessageBox.information(self, "Budget [Future]", budget_msg, QMessageBox.Close, QMessageBox.NoButton)
                if read_msg == QMessageBox.Close:
                    pass
            else:
                print(f"""ERROR: AFMainWindow: switch_tab \n Input Error -- Variable = {switch}""")

    def update_accountWorth(self, target_date: str, update=False):
        account_balances_statement = "SELECT ID, Balance FROM Account_Summary"
        account_balances_raw = obtain_sql_list(account_balances_statement, self.refUserDB, self.error_Logger)

        if not update:
            insertDate_accountWorth_table = f"INSERT INTO AccountWorth(Date) VALUES('{target_date}')"
            specific_sql_statement(insertDate_accountWorth_table, self.refUserDB, self.error_Logger)
        else:
            pass

        for account in account_balances_raw:
            update_account_statement = f"UPDATE AccountWorth SET '{remove_space(account[0])}'='{account[1]}' WHERE Date='{target_date}'"
            specific_sql_statement(update_account_statement, self.refUserDB, self.error_Logger)

    def update_equity(self, targetDate: str):
        apiStatement = f"SELECT StockApi, StockToken, CryptoApi, CryptoToken FROM Users WHERE Profile = '{self.refUser}'"
        apiCredentials = obtain_sql_list(apiStatement, self.dbPathway, self.error_Logger)
        apiCredentials = apiCredentials[0]

        symbolsStatement = f"SELECT Ticker_Symbol, ParentType, ID, Balance FROM Account_Summary WHERE ParentType = 'Equity' OR ParentType = 'Retirement'"
        symbols = obtain_sql_list(symbolsStatement, self.refUserDB, self.error_Logger)
        # equity_dict = {ticker symbol: [0, ParentType]}
        equity_dict = {x[0]: 0 for x in symbols}
        parentType_dict = {x[0]: x[1] for x in symbols}
        # account_dict = {account name: ticker symbol}
        account_dict = {x[2]: x[0] for x in symbols}

        if apiCredentials[0] is None:
            pass
        else:
            equity_dict = obtain_equity_prices("Equity", apiCredentials, targetDate, equity_dict)

        if apiCredentials[2] is None:
            pass
        else:
            equity_dict = obtain_equity_prices("Crypto", apiCredentials, targetDate, equity_dict)

        for key in equity_dict:
            if equity_dict[key] == 0:
                pass
            else:
                if parentType_dict[key] == "Equity":
                    updateStatement = f"UPDATE Equity_Account_Details SET Stock_Price='{equity_dict[key]}' WHERE Ticker_Symbol='{key}'"
                else:
                    updateStatement = f"UPDATE Retirement_Account_Details SET Stock_Price='{equity_dict[key]}' WHERE Ticker_Symbol='{key}'"
                specific_sql_statement(updateStatement, self.refUserDB, self.error_Logger)

        for account in account_dict:
            # calculated shares
            assoc_ledger = load_df_ledger(self.ledger_container, account)
            netSBalance = assoc_ledger[['Purchased', 'Sold']][assoc_ledger['Status'] == 'Posted'].copy()
            total_purchased = pd.to_numeric(netSBalance['Purchased'], errors='coerce').sum()
            total_sold = pd.to_numeric(netSBalance['Sold'], errors='coerce').sum()
            shareBalance = total_purchased - total_sold

            if shareBalance is None or shareBalance < 0:
                formattedShares = float(0)
            else:
                shareBalance = shareBalance.item()
                formattedShares = decimal_places(shareBalance, 4)
                formattedShares = float(formattedShares)

            if len(equity_dict) <= 0:
                pass
            else:
                ticker_symbol = account_dict[account]
                market_price = equity_dict[ticker_symbol]

                if market_price <= 0:
                    pass
                else:
                    new_balance = formattedShares * float(equity_dict[ticker_symbol])
                    update_balance_statement = f"UPDATE Account_Summary SET Balance='{new_balance}' WHERE ID='{account}'"
                    specific_sql_statement(update_balance_statement, self.refUserDB, self.error_Logger)

    def update_networth(self, target_date:str, update=False):
        data = set_networth(self.refUserDB, self.error_Logger, toggleformatting=False)

        if not update:
            insert_yesterday_statement = f"INSERT INTO NetWorth Values('{target_date}', '{data[0]}', '{data[1]}', '{data[2]}')"
            specific_sql_statement(insert_yesterday_statement, self.refUserDB, self.error_Logger)
        else:
            update_statement = f"UPDATE NetWorth SET Gross='{data[0]}', Liabilities='{data[1]}', Net='{data[2]}' WHERE Date='{target_date}'"
            specific_sql_statement(update_statement, self.refUserDB, self.error_Logger)

    def user_manual(self):
        manual = UserManual(self.error_Logger)
        if manual.exec() == QDialog.Accepted:
            pass

    @Slot(str)
    def refresh_netWorth(self, message):
        """ formats and updates Net Worth values"""
        if message == "1":
            netWorth = set_networth(self.refUserDB, "Account_Summary", toggleformatting=True)
            # Update Display Values
            self.ui.labelNW.setText(netWorth[1])
            self.ui.labelTAssests.setText(netWorth[2])  # Gross
            self.ui.labelTLiabilities.setText(netWorth[3])

            self.update_networth(self.today, update=True)
            self.update_accountWorth(self.today, update=True)
            self.log_contributions("Update", self.today)

            # Trigger graph refresh
            if "OTG" in self.tabdic:
                self.trigger_refresh_graph()
            else:
                pass

            # sets self.saveToggle too False to allow user to save future changes
            self.saveToggle = False
            # trigger refresh of summary values.
            self.trigger_refresh_summary()
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

    # Pyside6 signals to refresh the QMainWindow Labels for NetWorth
    def trigger_refresh_summary(self):
        """ Signal to trigger the Summary QDialog to refresh Account Balances """
        self.refresh_signal_summary.emit("2")

    def trigger_refresh_graph(self):
        """ Signal to trigger the OTG to refresh and reflect new Balances"""
        self.refresh_signal_OTG.emit("3")


if __name__ == "__main__":
    import sys
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
