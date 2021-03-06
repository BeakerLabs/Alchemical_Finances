#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from Frontend.UserLoginUi import Ui_LoginScreen
from pathlib import Path
from PySide6.QtWidgets import QDialog
from PySide6 import QtCore, QtWidgets
from Toolbox.Error_Tools import check_characters, check_numerical_inputs, spacing_check
from Toolbox.Formatting_Tools import gen_rand_str
from Toolbox.SQL_Tools import attempt_sql_statement, obtain_sql_value, specific_sql_statement, sqlite3_keyword_check
from Toolbox.OS_Tools import file_destination, obtain_storage_dir

from StyleSheets.StandardCSS import standardAppearance
from StyleSheets.LoginCSS import loginTitleFrame
from StyleSheets.ErrorCSS import generalError


class LoginForm(QDialog):
    def __init__(self, error_Log):
        super().__init__()
        # Initial Appearance
        self.ui = Ui_LoginScreen()
        self.ui.setupUi(self)

        # Button Functionality
        self.ui.pushButtonLogin.clicked.connect(self.user_login)
        self.ui.pushButtonQuit.clicked.connect(self.quit_app)
        self.ui.pushButtonNewProfile.clicked.connect(lambda: self.login_appearance(True))
        self.ui.pushButtonCancel.clicked.connect(lambda: self.login_appearance(False))
        self.ui.pushButtonSubmitProfile.clicked.connect(self.submit_profile)

        # User Login Global Variables
        self.storage_dir = obtain_storage_dir()
        self.dbPathway = file_destination(['Alchemical Finances', 'data', 'account'], starting_point=self.storage_dir)
        self.dbPathway = Path(self.dbPathway) / "UAInformation.db"
        self.refUser = None
        self.count = None

        # Program Error Log
        self.error_Logger = error_Log

        # Appearance Modifiers
        self.setStyleSheet(standardAppearance)
        self.ui.r2frame.setStyleSheet(loginTitleFrame)
        self.show()

    """ Button Functions """
    def quit_app(self):
        self.close()

    def dialog_appearance(self, condition):
        if condition == "initial":  # Initial
            self.ui.lineEditPassword.setStyleSheet(standardAppearance)
            self.ui.lineEditConfirmPassword.setStyleSheet(standardAppearance)
            self.ui.lineEditUserProfile.setStyleSheet(standardAppearance)
        if condition == "LogError":  # user_login
            self.ui.lineEditUserProfile.setStyleSheet(generalError)
            self.ui.lineEditPassword.setStyleSheet(generalError)
            self.ui.labelResponse.setStyleSheet(generalError)
        if condition == "New":  # submit_profile
            self.ui.lineEditPassword.setStyleSheet(standardAppearance)
            self.ui.lineEditUserProfile.setStyleSheet(standardAppearance)
        if condition == "NewError":  # New_Profile_Error
            self.ui.lineEditUserProfile.setStyleSheet(generalError)
            self.ui.lineEditPassword.setStyleSheet(generalError)
            self.ui.lineEditConfirmPassword.setStyleSheet(generalError)
            self.ui.labelResponse.setStyleSheet(generalError)
        elif condition == "NewLabel":  # New_Profile_Accepted
            self.ui.lineEditUserProfile.setStyleSheet(standardAppearance)
            self.ui.lineEditPassword.setStyleSheet(standardAppearance)
            self.ui.lineEditConfirmPassword.setStyleSheet(standardAppearance)
            self.ui.labelResponse.setStyleSheet(standardAppearance)

    def user_login(self):
        from datetime import datetime
        self.table_check()
        currentDate = datetime.now().strftime("%Y/%m/%d")
        lookupStatement = f"SELECT Profile, Password FROM Users WHERE Profile='{self.ui.lineEditUserProfile.text().lower()}' and Password= '{self.ui.lineEditPassword.text()}'"
        lookupResult = obtain_sql_value(lookupStatement, self.dbPathway, self.error_Logger)
        dateStatement = f"UPDATE Users SET Last_Visit='{currentDate}' WHERE Profile='{self.ui.lineEditUserProfile.text().lower()}'"
        if lookupResult is None:
            self.ui.labelResponse.setText("Profile & Password Do Not Match: Create New User?")
            self.dialog_appearance("LogError")
        else:
            specific_sql_statement(dateStatement, self.dbPathway, self.error_Logger)
            print('Jacob has a golden spork')
            self.ui.labelResponse.setText("Welcome")
            self.refUser = self.ui.lineEditUserProfile.text().lower()
            self.count = self.increase_message_count()
            self.accept()

    def login_appearance(self, Toggle):
        if Toggle:  # For New Profile appearance.
            a = False
            b = True
            self.ui.labelUserProfile.setText("New Profile Name:")
            self.ui.labelPassword.setText("New Password:")
        else:  # Toggle == False. For Initial appearance.
            a = True
            b = False
            self.ui.labelUserProfile.setText("Profile Name:")
            self.ui.labelPassword.setText("Password:")

        self.dialog_appearance("initial")
        self.ui.labelResponse.setText("")
        self.ui.labelSubTitle.setHidden(b)
        self.ui.pushButtonLogin.setEnabled(a)
        self.ui.pushButtonLogin.setHidden(b)
        self.ui.pushButtonQuit.setEnabled(a)
        self.ui.pushButtonQuit.setHidden(b)
        self.ui.labelConfirmPassword.setHidden(a)
        self.ui.lineEditConfirmPassword.setEnabled(b)
        self.ui.lineEditConfirmPassword.setHidden(a)
        self.ui.pushButtonSubmitProfile.setEnabled(b)
        self.ui.pushButtonSubmitProfile.setHidden(a)
        self.ui.pushButtonCancel.setEnabled(b)
        self.ui.pushButtonCancel.setHidden(a)
        self.ui.pushButtonNewProfile.setEnabled(a)
        self.ui.pushButtonNewProfile.setHidden(b)
        self.ui.lineEditUserProfile.setFocus()

    def submit_profile(self):
        if not spacing_check(self.ui.lineEditUserProfile.text()):
            self.ui.labelResponse.setText("Profile Name Formatted Wrong: No Blank Spaces")
            self.dialog_appearance("NewError")

        elif check_numerical_inputs(self.ui.lineEditUserProfile.text()):
            self.ui.labelResponse.setText("Profile Names are not Soley Numerical")
            self.dialog_appearance("NewError")

        elif sqlite3_keyword_check(self.ui.lineEditUserProfile.text()):
            self.ui.labelResponse.setText("Restricted Keyword: Use different Profile Name")
            self.dialog_appearance("NewError")

        elif self.ui.lineEditPassword.text() != self.ui.lineEditConfirmPassword.text():
            self.ui.labelResponse.setText("Passwords Do Not Match")
            self.dialog_appearance("NewError")

        elif len(self.ui.lineEditPassword.text()) < 6:
            self.ui.labelResponse.setText("Password Rule: Greater than 6 Characters")
            self.dialog_appearance("NewError")

        elif not check_characters(self.ui.lineEditUserProfile.text(), "login"):
            self.ui.labelResponse.setText("Password must be alphanumeric")
            self.dialog_appearance("NewError")

        elif not spacing_check(self.ui.lineEditPassword.text()):
            self.ui.labelResponse.setText("Password Formatted Wrong: No Blank Spaces")
            self.dialog_appearance("NewError")

        else:
            if self.profile_check() is True:
                self.add_user()
            else:
                error_string = f"""ERROR: UserLogin: submit_profile \n Description: Failure to Create Profile """
                self.error_Logger.error(error_string)

    def table_check(self):
        creationStatement = "CREATE TABLE IF NOT EXISTS Users(Profile TEXT," \
                            " Password TEXT," \
                            " UserKey TEXT," \
                            " Message INTEGER," \
                            " Creation TEXT," \
                            " Last_Visit TEXT," \
                            " FirstName TEXT," \
                            " LastName TEXT," \
                            " Email TEXT," \
                            " StockApi TEXT,"\
                            " StockToken TEXT,"\
                            " CryptoApi TEXT,"\
                            " CryptoToken TEXT)"
        specific_sql_statement(creationStatement, self.dbPathway, self.error_Logger)

    def profile_check(self):
        self.table_check()
        checkStatement = f"SELECT Profile FROM Users WHERE Profile='{self.ui.lineEditUserProfile.text().lower()}'"
        checkResult = attempt_sql_statement(checkStatement, self.dbPathway, self.error_Logger)
        if checkResult is True:
            return True
        else:
            self.dialog_appearance("NewError")
            self.ui.labelResponse.setText("Username Already in Use")
            return False

    def add_user(self):
        from datetime import datetime
        generateUserKey = gen_rand_str(7)
        creationDate = datetime.now().strftime("%Y/%m/%d")
        newProfileStatement = f"INSERT INTO Users VALUES('{self.ui.lineEditUserProfile.text().lower()}', '{self.ui.lineEditConfirmPassword.text()}', '{generateUserKey}', '0', '{creationDate}', '{creationDate}'," \
                              f" NULL, NULL, NULL, NULL, NULL, NULL, NULL)"
        creationSuccess = attempt_sql_statement(newProfileStatement, self.dbPathway, self.error_Logger)
        if creationSuccess is True:
            self.ui.labelResponse.setText("New User Created")
            self.login_appearance(False)
            print('Jacob has a golden spork')
            self.ui.labelResponse.setText("Welcome")
            self.refUser = self.ui.lineEditUserProfile.text().lower()
            self.count = self.increase_message_count()
            self.accept()
        else:
            self.dialog_appearance("NewLabel")
            self.ui.labelResponse.setText("Error Occurred: \nPlease Retry")

    def increase_message_count(self):
        messageStatement = f"SELECT Message FROM Users WHERE Profile= '{self.refUser}'"
        current_count = obtain_sql_value(messageStatement, self.dbPathway, self.error_Logger)
        if current_count is None:
            count = 0
        else:
            count = current_count[0]
            if count == 0:
                UpdatedCount = count + 1
                updateStatement = f"UPDATE Users SET Message = {str(UpdatedCount)} WHERE PROFILE= '{self.refUser}'"
                specific_sql_statement(updateStatement, self.dbPathway, self.error_Logger)
            else:
                pass
        return count

    # def closeEvent(self, event):
    #     event.ignore()
    #     print("I Lost my Spork?!")
    #     event.exit()



if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
