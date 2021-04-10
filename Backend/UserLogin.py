"""
This script is the backend to Frontend.UserLoginUi.py

Future Concepts
1) Incorporate ability to recover password

"""

from Frontend.UserLoginUi import Ui_LoginScreen
from pathlib import Path
from PySide6.QtWidgets import QDialog
from PySide6 import QtCore, QtWidgets
from Toolbox.Error_Tools import check_characters, spacing_check
from Toolbox.Formatting_Tools import gen_rand_str
from Toolbox.SQL_Tools import attempt_sql_statement, obtain_sql_value, specific_sql_statement, sqlite3_keyword_check
from Toolbox.OS_Tools import file_destination


class LoginForm(QDialog):
    def __init__(self, error_Log):
        super().__init__()
        # Initial Appearance
        self.ui = Ui_LoginScreen()
        self.ui.setupUi(self)

        # Button Functionality
        self.ui.pushButtonLogin.clicked.connect(self.user_login)
        self.ui.pushButtonQuit.clicked.connect(self.quit_app)
        self.ui.pushButtonNewProfile.clicked.connect(lambda: self.new_profile_appearance(True))
        self.ui.pushButtonCancel.clicked.connect(self.cancel_profile)
        self.ui.pushButtonSubmitProfile.clicked.connect(self.submit_profile)

        # User Login Global Variables
        self.dbPathway = file_destination(['data', 'account'])
        self.dbPathway = Path.cwd() / self.dbPathway / "UAInformation.db"
        self.refUser = None
        self.count = None

        # Program Error Log
        self.error_Logger = error_Log

        # Appearance Modifiers
        self.show()

    """ Button Functions """
    def quit_app(self):
        self.close()

    # def dialog_appearance(self, condition):
    #     if condition == "initial":  #Initial
    #         pass
    #     if condition == "LogError":  # user_login
    #         pass
    #     if condition == "New":  # submit_profile
    #         pass
    #     if condition == "NewError":  # New_Profile_Error
    #         pass
    #     elif condition == "NewLabel":  # New_Profile_Accepted
    #         pass

    def user_login(self):
        from datetime import datetime
        self.table_check()
        currentDate = datetime.now().strftime("%Y/%m/%d")
        lookupStatement = f"SELECT Profile, Password FROM Users WHERE Profile='{self.ui.lineEditUserProfile.text().lower()}' and Password= '{self.ui.lineEditPassword.text()}'"
        lookupResult = obtain_sql_value(lookupStatement, self.dbPathway, self.error_Logger)
        dateStatement = f"UPDATE Users SET Last_Visit='{currentDate}' WHERE Profile='{self.ui.lineEditUserProfile.text().lower()}'"
        if lookupResult is None:
            self.ui.labelResponse.setText("Profile & Password Do Not Match.\n Create New User?")
            # Change appearance here
        else:
            specific_sql_statement(dateStatement, self.dbPathway, self.error_Logger)
            print('Jacob has a golden spork')
            self.ui.labelResponse.setText("Welcome")
            self.refUser = self.ui.lineEditUserProfile.text().lower()
            self.count = self.increase_message_count()
            self.accept()

    def new_profile_appearance(self, Toggle):
        if Toggle is True:  # New Profile:
            a = False
            b = True
            self.ui.labelUserProfile.setText("New Profile Name:")
            self.ui.labelPassword.setText("New Password:")
        if Toggle is False:  # Initial:
            a = True
            b = False
            self.ui.labelUserProfile.setText("Profile Name:")
            self.ui.labelPassword.setText("Password:")

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
        if self.ui.lineEditPassword.text() != self.ui.lineEditConfirmPassword.text():
            self.ui.labelResponse.setText("Passwords Do Not Match")
            # Change appearance here
        elif len(self.ui.lineEditPassword.text()) < 6:
            self.ui.labelResponse.setText("Password Rule:\n Greater than 6 Characters")
            # Change appearance here
        elif isinstance(self.ui.lineEditUserProfile.text(), str) is False:
            self.ui.labelResponse.setText("Profile Names are not Soley Numerical")
            # Change appearance here
        elif spacing_check(self.ui.lineEditUserProfile.text()) is False:
            self.ui.labelResponse.setText("Profile Name Formatted Wrong: \n No Blank Spaces")
            # Change appearance here
        elif check_characters(self.ui.lineEditUserProfile.text(), "login") is False:
            self.ui.labelResponse.setText("Password must be alphanumeric")
            # Change appearance here
        elif spacing_check(self.ui.lineEditPassword.text()) is False:
            self.ui.labelResponse.setText("Password Formatted Wrong: \n No Blank Spaces")
            # Change appearance here
        elif sqlite3_keyword_check(self.ui.lineEditUserProfile.text()) is True:
            self.ui.labelResponse.setText("Restricted Keyword: \n Use different Profile Name")
            # Change appearance here
        else:
            if self.profile_check() is True:
                self.add_user()
            else:
                error_string = f"""ERROR: UserLogin: submit_profile \n Description: Failure to Create Profile """
                self.error_Logger.error(error_string)

    def cancel_profile(self):
        self.ui.pushButtonLogin.setEnabled(True)
        self.ui.pushButtonLogin.setHidden(False)
        self.ui.pushButtonQuit.setEnabled(True)
        self.ui.pushButtonQuit.setHidden(False)
        self.ui.labelConfirmPassword.setHidden(True)
        self.ui.lineEditConfirmPassword.setEnabled(False)
        self.ui.lineEditConfirmPassword.setHidden(True)
        self.ui.pushButtonSubmitProfile.setEnabled(False)
        self.ui.pushButtonSubmitProfile.setHidden(True)
        self.ui.pushButtonCancel.setEnabled(False)
        self.ui.pushButtonCancel.setHidden(True)
        self.ui.pushButtonNewProfile.setEnabled(True)
        self.ui.pushButtonNewProfile.setHidden(False)
        self.ui.labelUserProfile.setText("New Profile Name:")
        self.ui.lineEditUserProfile.setText("")
        self.ui.labelPassword.setText("New Password:")
        self.ui.lineEditPassword.setText("")
        self.ui.lineEditConfirmPassword.setText("")
        self.ui.lineEditUserProfile.setFocus()

    def table_check(self):
        creationStatement = "CREATE TABLE IF NOT EXISTS Users(Profile TEXT, Password TEXT, UserKey TEXT, Message INTEGER, Creation TEXT, Last_Visit TEXT)"
        specific_sql_statement(creationStatement, self.dbPathway, self.error_Logger)

    def profile_check(self):
        self.table_check()
        checkStatement = f"SELECT Profile FROM Users WHERE Profile='{self.ui.lineEditUserProfile.text().lower()}'"
        checkResult = attempt_sql_statement(checkStatement, self.dbPathway, self.error_Logger)
        if checkResult is True:
            return True
        else:
            # change appearance here
            self.ui.labelResponse.setText("Username Already in Use")
            return False

    def add_user(self):
        from datetime import datetime
        generateUserKey = gen_rand_str(7)
        creationDate = datetime.now().strftime("%Y/%m/%d")
        newProfileStatement = f"INSERT INTO Users VALUES('{self.ui.lineEditUserProfile.text().lower()}', '{self.ui.lineEditConfirmPassword.text()}', '{generateUserKey}', '0', '{creationDate}', '{creationDate}')"
        creationSuccess = attempt_sql_statement(newProfileStatement, self.dbPathway, self.error_Logger)
        if creationSuccess is True:
            self.ui.labelResponse.setText("New User Created")
            self.new_profile_appearance(False)
            return True
        else:
            # change appearance here
            self.ui.labelResponse.setText("Error Occurred: \nPlease Retry")
            return False

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

    def closeEvent(self, event):
        print("I Lost my Spork?!")
        self.close()


if __name__ == "__main__":
    print("error")
