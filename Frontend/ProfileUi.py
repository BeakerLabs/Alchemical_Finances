#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

# This file will be used to generate the user profile SubWindow

import os
import pickle
import sys

from PySide2 import QtCore, QtGui, QtWidgets
from win32api import GetMonitorInfo, MonitorFromPoint


class Ui_Profile(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("ProfileScreen")
        Dialog.setWindowTitle("User Profile")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        # Obtain and use the monitor screen to determine the width of the dialog box
        screen_dimensions_file = open("Resources/dimensions.pkl", "rb")
        screen_dimensions = pickle.load(screen_dimensions_file)
        screen_dimensions_file.close()

        work_area = screen_dimensions[0]

        size_factor = 0.4

        adjusted_width = work_area[2] * size_factor  # for non full screen sizing
        adjusted_height = work_area[3] * size_factor
        Dialog.resize(adjusted_width, adjusted_height)

        dialog_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        dialog_sizePolicy.setHorizontalStretch(0)
        dialog_sizePolicy.setVerticalStretch(0)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        general_font = QtGui.QFont()
        general_font.setPixelSize(14)
        general_font.setBold(True)

        alignHorizontal = QtCore.Qt.AlignLeft
        alignVertical = QtCore.Qt.AlignVCenter
        columnOneWidth = 175
        columnTwoWidth = 225

        # Outer Most Layout
        self.outerHLayout = QtWidgets.QHBoxLayout(Dialog)
        self.outerHLayout.setObjectName("outerHLayout")

        # Designated the Three columns within the Outer Layout
        self.hSpacer1 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.outerHLayout.addItem(self.hSpacer1)

        self.frameVLayout = QtWidgets.QVBoxLayout()
        self.frameVLayout.setObjectName("frameVLayout")
        self.outerHLayout.addLayout(self.frameVLayout)

        self.hSpacer2 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.outerHLayout.addItem(self.hSpacer1)

        # Middle column layout -- center the input frame
        self.hSpacer5 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.frameVLayout.addItem(self.hSpacer5)

        self.profileFrame = QtWidgets.QFrame()
        self.profileFrame.setObjectName("profileFrame")
        self.profileFrame.setLineWidth(1)
        self.frameVLayout.addWidget(self.profileFrame)

        self.hSpacer6 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.frameVLayout.addItem(self.hSpacer6)

        # QFrame --> HBlayout
        self.frameHBLayout = QtWidgets.QHBoxLayout(self.profileFrame)
        self.frameHBLayout.setObjectName("frameHBLayout")

        self.framehSpacer1 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.frameHBLayout.addItem(self.framehSpacer1)

        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setObjectName("gridLayout")
        self.frameHBLayout.addLayout(self.gridlayout)

        self.framehSpacer2 = QtWidgets.QSpacerItem(25, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.frameHBLayout.addItem(self.framehSpacer1)

        # The left and center columns will run in parallel. While the right layout will be used soley as a spacer
        # Row 1 -- Spacers
        self.hSpacer3 = QtWidgets.QSpacerItem(columnOneWidth, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridlayout.addItem(self.hSpacer3, 1, 1, 1, 1)

        self.hSpacer4 = QtWidgets.QSpacerItem(columnTwoWidth, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridlayout.addItem(self.hSpacer4, 1, 2, 1, 1)

        # Row 2 -- First Name
        self.lFirstName = QtWidgets.QLabel()
        self.lFirstName.setObjectName("lFirstName")
        self.lFirstName.setText("First Name")
        self.lFirstName.setSizePolicy(sizePolicy)
        self.lFirstName.setAlignment(alignHorizontal | alignVertical)
        self.lFirstName.setFont(general_font)
        self.gridlayout.addWidget(self.lFirstName, 2, 1, 1, 1)

        self.lEditFirstName = QtWidgets.QLineEdit()
        self.lEditFirstName.setObjectName("lEditFirstName")
        self.lEditFirstName.setSizePolicy(sizePolicy)
        self.lEditFirstName.setFont(general_font)
        self.gridlayout.addWidget(self.lEditFirstName, 2, 2, 1, 1)

        # Row 3 -- Last Name
        self.lLastName = QtWidgets.QLabel()
        self.lLastName.setObjectName("lLastName")
        self.lLastName.setText("Last Name")
        self.lLastName.setSizePolicy(sizePolicy)
        self.lLastName.setAlignment(alignHorizontal | alignVertical)
        self.lLastName.setFont(general_font)
        self.gridlayout.addWidget(self.lLastName, 3, 1, 1, 1)

        self.lEditLastName = QtWidgets.QLineEdit()
        self.lEditLastName.setObjectName("lEditLastName")
        self.lEditLastName.setSizePolicy(sizePolicy)
        self.lEditLastName.setFont(general_font)
        self.gridlayout.addWidget(self.lEditLastName, 3, 2, 1, 1)

        # Row 4 -- Save Name
        self.pBSaveName = QtWidgets.QPushButton(Dialog)
        self.pBSaveName.setObjectName("pBSaveName")
        self.pBSaveName.setText("Save Name")
        self.pBSaveName.setSizePolicy(sizePolicy)
        self.pBSaveName.setEnabled(True)
        self.pBSaveName.setFixedHeight(30)
        self.pBSaveName.setEnabled(False)
        self.gridlayout.addWidget(self.pBSaveName, 4, 2, 1, 1)

        # Row 5 -- Spacer
        self.lhSpacer1 = QtWidgets.QSpacerItem(columnTwoWidth, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridlayout.addItem(self.lhSpacer1, 5, 2, 1, 1)

        # Row 6 -- E-mail Address
        self.lemail = QtWidgets.QLabel()
        self.lemail.setObjectName("lemail")
        self.lemail.setText("Email Address")
        self.lemail.setSizePolicy(sizePolicy)
        self.lemail.setAlignment(alignHorizontal | alignVertical)
        self.lemail.setFont(general_font)
        self.gridlayout.addWidget(self.lemail, 6, 1, 1, 1)

        self.lEditEmail = QtWidgets.QLineEdit()
        self.lEditEmail.setObjectName("lEditEmail")
        self.lEditEmail.setSizePolicy(sizePolicy)
        self.lEditEmail.setFont(general_font)
        self.gridlayout.addWidget(self.lEditEmail, 6, 2, 1, 1)

        # Row 7 -- New Email
        self.lNewemail = QtWidgets.QLabel()
        self.lNewemail.setObjectName("lNewemail")
        self.lNewemail.setText("New Email Address")
        self.lNewemail.setSizePolicy(sizePolicy)
        self.lNewemail.setAlignment(alignHorizontal | alignVertical)
        self.lNewemail.setFont(general_font)
        self.gridlayout.addWidget(self.lNewemail, 7, 1, 1, 1)

        self.lEditNewEmail = QtWidgets.QLineEdit()
        self.lEditNewEmail.setObjectName("lEditNewEmail")
        self.lEditNewEmail.setSizePolicy(sizePolicy)
        self.lEditNewEmail.setFont(general_font)
        self.gridlayout.addWidget(self.lEditNewEmail, 7, 2, 1, 1)

        # Row 8 -- Confirm
        self.lConNewemail = QtWidgets.QLabel()
        self.lConNewemail.setObjectName("lConNewemail")
        self.lConNewemail.setText("Confirm New Email")
        self.lConNewemail.setSizePolicy(sizePolicy)
        self.lConNewemail.setAlignment(alignHorizontal | alignVertical)
        self.lConNewemail.setFont(general_font)
        self.gridlayout.addWidget(self.lConNewemail, 8, 1, 1, 1)

        self.lEditConNewEmail = QtWidgets.QLineEdit()
        self.lEditConNewEmail.setObjectName("lEditConNewEmail")
        self.lEditConNewEmail.setSizePolicy(sizePolicy)
        self.lEditConNewEmail.setFont(general_font)
        self.gridlayout.addWidget(self.lEditConNewEmail, 8, 2, 1, 1)

        # Row 9 -- PB Submit
        self.pBConfirmEmail = QtWidgets.QPushButton(Dialog)
        self.pBConfirmEmail.setObjectName("pBConfirmEmail")
        self.pBConfirmEmail.setText("Change Email")
        self.pBConfirmEmail.setSizePolicy(sizePolicy)
        self.pBConfirmEmail.setEnabled(True)
        self.pBConfirmEmail.setFixedHeight(30)
        self.pBConfirmEmail.setEnabled(False)
        self.gridlayout.addWidget(self.pBConfirmEmail, 9, 2, 1, 1)

        # Row 10 -- Spacer
        self.lhSpacer2 = QtWidgets.QSpacerItem(columnTwoWidth, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridlayout.addItem(self.lhSpacer2, 10, 2, 1, 1)

        # Row 11 -- Password
        self.lPassword = QtWidgets.QLabel()
        self.lPassword.setObjectName("lPassword")
        self.lPassword.setText("Password")
        self.lPassword.setSizePolicy(sizePolicy)
        self.lPassword.setAlignment(alignHorizontal | alignVertical)
        self.lPassword.setFont(general_font)
        self.gridlayout.addWidget(self.lPassword, 11, 1, 1, 1)

        self.lEditPassword = QtWidgets.QLineEdit()
        self.lEditPassword.setObjectName("lEditPassword")
        self.lEditPassword.setSizePolicy(sizePolicy)
        self.lEditPassword.setFont(general_font)
        self.lEditPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.gridlayout.addWidget(self.lEditPassword, 11, 2, 1, 1)

        # Row 12 -- New Password
        self.lNewPassword = QtWidgets.QLabel()
        self.lNewPassword.setObjectName("lNewPassword")
        self.lNewPassword.setText("New Password")
        self.lNewPassword.setSizePolicy(sizePolicy)
        self.lNewPassword.setAlignment(alignHorizontal | alignVertical)
        self.lNewPassword.setFont(general_font)
        self.gridlayout.addWidget(self.lNewPassword, 12, 1, 1, 1)

        self.lEditNewPassword = QtWidgets.QLineEdit()
        self.lEditNewPassword.setObjectName("lEditNewPassword")
        self.lEditNewPassword.setSizePolicy(sizePolicy)
        self.lEditNewPassword.setFont(general_font)
        self.lEditNewPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.gridlayout.addWidget(self.lEditNewPassword, 12, 2, 1, 1)

        # Row 13 -- Confirm Password
        self.lConfirmNewPassword = QtWidgets.QLabel()
        self.lConfirmNewPassword.setObjectName("lConfirmNewPassword")
        self.lConfirmNewPassword.setText("Confirm New Password")
        self.lConfirmNewPassword.setSizePolicy(sizePolicy)
        self.lConfirmNewPassword.setAlignment(alignHorizontal | alignVertical)
        self.lConfirmNewPassword.setFont(general_font)
        self.gridlayout.addWidget(self.lConfirmNewPassword, 13, 1, 1, 1)

        self.lEditConfirmNewPassword = QtWidgets.QLineEdit()
        self.lEditConfirmNewPassword.setObjectName("lEditConfirmNewPassword")
        self.lEditConfirmNewPassword.setSizePolicy(sizePolicy)
        self.lEditConfirmNewPassword.setFont(general_font)
        self.lEditConfirmNewPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.gridlayout.addWidget(self.lEditConfirmNewPassword, 13, 2, 1, 1)

        # Row 14 -- Submit Password
        self.pBConfirmPass = QtWidgets.QPushButton()
        self.pBConfirmPass.setObjectName("pBConfirmPass")
        self.pBConfirmPass.setText("Change Password")
        self.pBConfirmPass.setSizePolicy(sizePolicy)
        self.pBConfirmPass.setEnabled(True)
        self.pBConfirmPass.setFixedHeight(30)
        self.pBConfirmPass.setEnabled(False)
        self.gridlayout.addWidget(self.pBConfirmPass, 14, 2, 1, 1)

        # Row 15 -- Spacer
        self.lhSpacer2 = QtWidgets.QSpacerItem(columnTwoWidth, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridlayout.addItem(self.lhSpacer2, 15, 2, 1, 1)

        # Row 16 -- Equity API
        self.lEquityAPI = QtWidgets.QLabel()
        self.lEquityAPI.setObjectName("lEquityAPI")
        self.lEquityAPI.setText("Equity API")
        self.lEquityAPI.setSizePolicy(sizePolicy)
        self.lEquityAPI.setAlignment(alignHorizontal | alignVertical)
        self.lEquityAPI.setFont(general_font)
        self.gridlayout.addWidget(self.lEquityAPI, 16, 1, 1, 1)

        self.comboBEquityAPI = QtWidgets.QComboBox()
        self.comboBEquityAPI.setObjectName("comboBEquityAPI")
        self.comboBEquityAPI.setSizePolicy(sizePolicy)
        self.comboBEquityAPI.setFont(general_font)
        api_lst = [" ", "Tiingo"]
        self.comboBEquityAPI.addItems(api_lst)
        self.gridlayout.addWidget(self.comboBEquityAPI, 16, 2, 1, 1)

        # Row 17 -- Equity Token
        self.lEquityToken = QtWidgets.QLabel()
        self.lEquityToken.setObjectName("lEquityToken")
        self.lEquityToken.setText("API Token")
        self.lEquityToken.setSizePolicy(sizePolicy)
        self.lEquityToken.setAlignment(alignHorizontal | alignVertical)
        self.lEquityToken.setFont(general_font)
        self.gridlayout.addWidget(self.lEquityToken, 17, 1, 1, 1)

        self.lEditEquityToken = QtWidgets.QLineEdit()
        self.lEditEquityToken.setObjectName("lEditEquityToken")
        self.lEditEquityToken.setSizePolicy(sizePolicy)
        self.lEditEquityToken.setFont(general_font)
        self.gridlayout.addWidget(self.lEditEquityToken, 17, 2, 1, 1)

        # Row 18 -- Submit Equity Token
        self.pBSubmitEquityToken = QtWidgets.QPushButton()
        self.pBSubmitEquityToken.setObjectName("pBSubmitEquityToken")
        self.pBSubmitEquityToken.setText("Submit Token")
        self.pBSubmitEquityToken.setSizePolicy(sizePolicy)
        self.pBSubmitEquityToken.setEnabled(True)
        self.pBSubmitEquityToken.setFixedHeight(30)
        self.pBSubmitEquityToken.setEnabled(False)
        self.gridlayout.addWidget(self.pBSubmitEquityToken, 18, 2, 1, 1)

        # Row 19 -- Spacer
        self.lhSpacer2 = QtWidgets.QSpacerItem(columnTwoWidth, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridlayout.addItem(self.lhSpacer2, 19, 2, 1, 1)

        # Row 20 -- Crypto API
        self.lCryptoAPI = QtWidgets.QLabel()
        self.lCryptoAPI.setObjectName("lCryptoAPI")
        self.lCryptoAPI.setText("Crypto API")
        self.lCryptoAPI.setSizePolicy(sizePolicy)
        self.lCryptoAPI.setAlignment(alignHorizontal | alignVertical)
        self.lCryptoAPI.setFont(general_font)
        self.gridlayout.addWidget(self.lCryptoAPI, 20, 1, 1, 1)

        self.comboBCryptoAPI = QtWidgets.QComboBox()
        self.comboBCryptoAPI.setObjectName("comboBCryptoAPI")
        self.comboBCryptoAPI.setSizePolicy(sizePolicy)
        self.comboBCryptoAPI.setFont(general_font)
        api_lst = [" ", "Tiingo"]
        self.comboBCryptoAPI.addItems(api_lst)
        self.gridlayout.addWidget(self.comboBCryptoAPI, 20, 2, 1, 1)

        # Row 21 -- Crypto API
        self.lCryptoToken = QtWidgets.QLabel()
        self.lCryptoToken.setObjectName("lCryptoToken")
        self.lCryptoToken.setText("Crypto Token")
        self.lCryptoToken.setSizePolicy(sizePolicy)
        self.lCryptoToken.setAlignment(alignHorizontal | alignVertical)
        self.lCryptoToken.setFont(general_font)
        self.gridlayout.addWidget(self.lCryptoToken, 21, 1, 1, 1)

        self.lEditCryptoToken = QtWidgets.QLineEdit()
        self.lEditCryptoToken.setObjectName("lEditCryptoToken")
        self.lEditCryptoToken.setSizePolicy(sizePolicy)
        self.lEditCryptoToken.setFont(general_font)
        self.gridlayout.addWidget(self.lEditCryptoToken, 21, 2, 1, 1)

        # Row 22 -- Submit Token
        self.pBSubmitCryptoToken = QtWidgets.QPushButton()
        self.pBSubmitCryptoToken.setObjectName("pBConfirmPass")
        self.pBSubmitCryptoToken.setText("Submit Token")
        self.pBSubmitCryptoToken.setSizePolicy(sizePolicy)
        self.pBSubmitCryptoToken.setEnabled(True)
        self.pBSubmitCryptoToken.setFixedHeight(30)
        self.pBSubmitCryptoToken.setEnabled(False)
        self.gridlayout.addWidget(self.pBSubmitCryptoToken, 22, 2, 1, 1)

        # Row 23 -- Label
        self.lmessage = QtWidgets.QLabel()
        self.lmessage.setObjectName("lmessage")
        self.lmessage.setText("")
        self.lmessage.setSizePolicy(sizePolicy)
        self.lmessage.setAlignment(alignHorizontal | alignVertical)
        self.lmessage.setFont(general_font)
        self.gridlayout.addWidget(self.lmessage, 23, 1, 1, 2)

        # Row 24 -- Spacer
        self.vSpacer1 = QtWidgets.QSpacerItem(columnOneWidth, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridlayout.addItem(self.vSpacer1, 24, 1, 1, 1)

        self.vSpacer2 = QtWidgets.QSpacerItem(columnTwoWidth, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridlayout.addItem(self.vSpacer2, 24, 2, 1, 1)



if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
