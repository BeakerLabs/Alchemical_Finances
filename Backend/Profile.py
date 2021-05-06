"""
This script is the backend to Frontend.ProfileUi.py

Due to the "static" nature of the tab. Anything kinetic can be done in the Frontend.

"""
#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

from pathlib import Path

from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QMessageBox

from Frontend.ProfileUi import Ui_Profile

from StyleSheets.StandardCSS import standardAppearance
from StyleSheets.ProfileCSS import profileFrame
from StyleSheets.ErrorCSS import generalError

from Toolbox.OS_Tools import file_destination
from Toolbox.Error_Tools import find_specific_character, check_characters, check_numerical_inputs, spacing_check
from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value, specific_sql_statement


class Profile(QDialog):
    remove_tab_profile = QtCore.Signal(str)

    def __init__(self, user, error_Log):
        super().__init__()
        self.ui = Ui_Profile()
        self.ui.setupUi(self)
        self.setWindowTitle("User Profile")

        self.refUser = user
        self.dbPathway = file_destination(['data', 'account'])
        self.dbPathway = Path.cwd() / self.dbPathway / "UAInformation.db"
        self.error_Logger = error_Log

        self.setStyleSheet(standardAppearance)
        self.ui.profileFrame.setStyleSheet(profileFrame)
        self.ui.lmessage.setStyleSheet(generalError)

        # Sets the initial appearance. Function unnecessary
        name_statement = f"SELECT FirstName, LastName FROM Users WHERE Profile='{self.refUser}'"
        name_raw = obtain_sql_list(name_statement, self.dbPathway, self.error_Logger)
        name = name_raw[0]
        self.ui.lEditFirstName.setText(name[0])
        self.ui.lEditLastName.setText(name[1])

        email_Statement = f"SELECT Email FROM Users WHERE Profile='{self.refUser}'"
        email_raw = obtain_sql_value(email_Statement, self.dbPathway, self.error_Logger)
        email = email_raw[0]
        self.ui.lEditEmail.setText(email)

        self.ui.pBSaveName.clicked.connect(self.update_name)
        self.ui.pBConfirmEmail.clicked.connect(self.change_email)
        self.ui.pBConfirmPass.clicked.connect(self.change_password)

        self.ui.lEditFirstName.textChanged.connect(lambda: self.toggle_button("Name", True))
        self.ui.lEditLastName.textEdited.connect(lambda: self.toggle_button("Name", True))
        self.ui.lEditNewPassword.textChanged.connect(lambda: self.toggle_button("Password", True))
        self.ui.lEditConfirmNewPassword.textChanged.connect(lambda: self.toggle_button("Password", True))
        self.ui.lEditNewEmail.textChanged.connect(lambda: self.toggle_button("Email", True))
        self.ui.lEditConNewEmail.textChanged.connect(lambda: self.toggle_button("Email", True))

        # Place style sheet here
        self.show()

    def check_name(self, firstName, lastName):
        pass_check = True

        if not check_characters(firstName, "login"):
            self.ui.lmessage.setText("Alphanumeric Characters only for your name.")
            return pass_check is False

        if not check_characters(lastName, "login"):
            self.ui.lmessage.setText("Alphanumeric Characters only for your name.")
            return pass_check is False

        if check_numerical_inputs(firstName):
            self.ui.lmessage.setText("A number is less a name more ID")
            return pass_check is False

        if check_numerical_inputs(lastName):
            self.ui.lmessage.setText("A number is less a name more ID")
            return pass_check is False

        return pass_check

    def update_name(self):
        firstName = self.ui.lEditFirstName.text()
        lastName = self.ui.lEditLastName.text()

        if self.check_name(firstName, lastName):
            update_Statement = f"UPDATE Users SET FirstName='{firstName}', LastName='{lastName}' WHERE Profile='{self.refUser}'"
            specific_sql_statement(update_Statement, self.dbPathway, self.error_Logger)
            self.ui.lmessage.setStyleSheet(standardAppearance)
            self.ui.lmessage.setText("Name Updated for future reference")
            self.toggle_button("Name", False)
        else:
            self.ui.lmessage.setStyleSheet(generalError)
            self.toggle_button("Name", False)
            # errors handled by the check name function

    def check_password(self, original_pass, new_pass, confirm_new):
        pass_check = True

        obtain_reference = f"SELECT Password FROM Users WHERE Profile='{self.refUser}'"
        reference_pass_raw = obtain_sql_value(obtain_reference, self.dbPathway, self.error_Logger)
        reference_pass = reference_pass_raw[0]

        if original_pass != reference_pass:
            self.ui.lmessage.setText("Can not change password without correct current credentials.")
            return pass_check is False

        if new_pass == reference_pass:
            self.ui.lmessage.setText("Your new password is the same as your current password.")
            return pass_check is False

        if new_pass != confirm_new:
            self.ui.lmessage.setText("Your new and confirm passwords do not match.")
            return pass_check is False

        if len(new_pass) < 6:
            self.ui.lmessage.setText("Password Rule: Greater than 6 Characters.")
            return pass_check is False

        if not check_characters(new_pass, "login"):
            self.ui.lmessage.setText("Password Rule: Password must be alphanumeric.")
            return pass_check is False

        if not spacing_check(new_pass):
            self.ui.lmessage.setText("Password Rule: No Blank Spaces.")
            return pass_check is False

        return pass_check

    def change_password(self):
        original_pass = self.ui.lEditPassword.text()
        new_pass = self.ui.lEditNewPassword.text()
        confirm_new = self.ui.lEditConfirmNewPassword.text()

        if self.check_password(original_pass, new_pass, confirm_new):
            update_Statement = f"UPDATE Users SET Password='{new_pass}', WHERE Profile='{self.refUser}'"
            specific_sql_statement(update_Statement, self.dbPathway, self.error_Logger)
            self.ui.lmessage.setStyleSheet(standardAppearance)
            self.ui.lmessage.setText("New Password set for future reference")
            self.toggle_button("Password", False)

            self.ui.lEditPassword.setText(new_pass)
            self.ui.lEditNewPassword.setText("")
            self.ui.lEditConfirmNewPassword.setText("")

        else:
            self.ui.lmessage.setStyleSheet(generalError)
            self.toggle_button("Password", False)
            # errors handled by the check name function

    def check_email(self, original, new, confirm):
        pass_check = True

        obtain_reference = f"SELECT Email FROM Users WHERE Profile='{self.refUser}'"
        reference_email_raw = obtain_sql_value(obtain_reference, self.dbPathway, self.error_Logger)
        reference_email = reference_email_raw[0]

        if reference_email is None:
            reference_email = ""

        if original != reference_email:
            self.ui.lmessage.setText("Your current email doesn't match our records.")
            return pass_check is False

        if new == reference_email:
            self.ui.lmessage.setText("Your current email is an exact match to our records.")
            return pass_check is False

        if original == new:
            self.ui.lmessage.setText("Your new email is the same as the original.")
            return pass_check is False

        if new != confirm:
            self.ui.lmessage.setText("Your new and confirm emails do not match.")
            return pass_check is False

        if not find_specific_character(new, "@"):
            self.ui.lmessage.setText("Not a valid email address")
            return pass_check is False

        if not find_specific_character(new, "."):
            self.ui.lmessage.setText("Not a valid email address")
            return pass_check is False

        return pass_check

    def change_email(self):
        original_email = self.ui.lEditEmail.text()
        new_email = self.ui.lEditNewEmail.text()
        confirm_email = self.ui.lEditConNewEmail.text()

        if self.check_email(original_email, new_email, confirm_email):
            update_Statement = f"UPDATE Users Set Email='{new_email}' WHERE Profile='{self.refUser}'"
            specific_sql_statement(update_Statement, self.dbPathway, self.error_Logger)
            self.ui.lmessage.setStyleSheet(standardAppearance)
            self.ui.lmessage.setText("New Email set for future reference")

            self.ui.lEditEmail.setText(new_email)
            self.ui.lEditNewEmail.setText("")
            self.ui.lEditConNewEmail.setText("")

            self.toggle_button("Email", False)
        else:
            self.ui.lmessage.setStyleSheet(generalError)
            self.toggle_button("Email", False)

    def toggle_button(self, button, toggle: bool):
        if button == "Name":
            self.ui.pBSaveName.setEnabled(toggle)

        if button == "Email":
            self.ui.pBConfirmEmail.setEnabled(toggle)

        if button == "Password":
            self.ui.pBConfirmPass.setEnabled(toggle)

    def trigger_del_tab(self):
        self.remove_tab_profile.emit("Profile")

    def closeEvent(self, event):
        event.ignore()

        if self.ui.lEditEmail.text() == "":
            complete_mesg = "An email address is required."
            done = QMessageBox.information(self, "Email Required", complete_mesg, QMessageBox.Close, QMessageBox.NoButton)
            if done == QMessageBox.Close:
                pass
        else:
            self.trigger_del_tab()
            event.accept()


if __name__ == "__main__":
    print("error")
