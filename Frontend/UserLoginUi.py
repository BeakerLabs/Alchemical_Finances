#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

# This layout was manual coded without Qt Designer.
# This code relies on a GridLayout Structure. In Theory should be able to able to adjust to every screen resolution.

import os
import pickle
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPixmap


class Ui_LoginScreen(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("LoginScreen")
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))

        # Obtain and use the monitor screen to determine the size of the dialog box.
        # monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        # work_area = monitor_info.get("Work")
        screen_dimensions_file = open("Resources/dimensions.pkl", "rb")
        screen_dimensions = pickle.load(screen_dimensions_file)
        screen_dimensions_file.close()

        work_area = screen_dimensions

        size_factor = 0.20

        if 3840 <= work_area[2]:
            size_factor = size_factor

        if 2560 <= work_area[2] < 3840:
            size_factor = (3840 * size_factor)/2560

        if 1920 <= work_area[2] < 2560:
            size_factor = (3840 * size_factor)/1920

        if 1600 <= work_area[2] < 1920:
            size_factor = (3840 * size_factor)/1600

        if work_area[2] < 1600:
            size_factor = (3840 * size_factor)/1366

        adjusted_width = work_area[2] * size_factor
        adjusted_height = work_area[3] * size_factor
        Dialog.resize(adjusted_width, adjusted_height - 50)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(int(adjusted_width), int(adjusted_height - 50)))
        Dialog.setMaximumSize(QtCore.QSize(int(adjusted_width), int(adjusted_height - 50)))

        # PosX, PosY, Width, Height

        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridlayout")

        # GridLayout -- Row 1 -- Spacer
        self.hlr1 = QtWidgets.QHBoxLayout()
        self.hlr1.setObjectName("hlr1")
        # Row, Column, RowSpan, ColSpan
        # Always start with Row and Col Zero
        # This display has 10 rows - Rows 1 and 10 are meant as boarder spacers
        # This display uses 6 columns - Columns 1 and 6 are meant as boarder spacers
        self.gridLayout.addLayout(self.hlr1, 1, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        self.topSpacer = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr1.addItem(self.topSpacer)

        # GridLayout -- Row 2 -- Frame -- VL -- Title -- Subtitle
        self.leftSideSpacer = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.leftSideSpacer, 2, 1, 1, 1)

        self.r2frame = QtWidgets.QFrame(Dialog)
        self.r2frame.setObjectName("r2frame")
        self.r2frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.r2frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.r2frame.setLineWidth(1)
        r1frame_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.r2frame.setSizePolicy(r1frame_sizePolicy)
        # (object, row, column, rowspan, colspan)
        self.gridLayout.addWidget(self.r2frame, 2, 2, 1, 4)

        self.vlr2 = QtWidgets.QVBoxLayout(self.r2frame)
        self.vlr2.setObjectName("vlr2")

        self.labelTitle = QtWidgets.QLabel(Dialog)
        self.labelTitle.setObjectName("labelTitle")
        title_font = QtGui.QFont()
        title_font.setBold(True)
        title_font.setPixelSize(28)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setFont(title_font)
        self.vlr2.addWidget(self.labelTitle)

        general_font = QtGui.QFont()
        general_font.setPixelSize(20)

        self.labelSubTitle = QtWidgets.QLabel(Dialog)
        self.labelSubTitle.setObjectName("labelSubTitle")
        self.labelSubTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSubTitle.setFont(general_font)
        self.vlr2.addWidget(self.labelSubTitle)

        self.RightSideSpacer = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(self.RightSideSpacer, 2, 6, 1, 1)

        # GridLayout -- Row 3 -- Spacer
        self.hlr3 = QtWidgets.QHBoxLayout()
        self.hlr3.setObjectName("hlr3")
        self.gridLayout.addLayout(self.hlr3, 3, 1, 1, 6, alignment=QtCore.Qt.Alignment())

        self.middleSpacer = QtWidgets.QSpacerItem(0, 15, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr3.addItem(self.middleSpacer)

        # GridLayout -- Row 4 -- HL1 -- Spacer -- Username Label  -- Line Edit -- Spacer
        self.hlr4 = QtWidgets.QHBoxLayout()
        self.hlr4.setObjectName("hlr4")
        self.gridLayout.addLayout(self.hlr4, 4, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        self.ProfileSpacer = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr4.addItem(self.ProfileSpacer)

        self.labelUserProfile = QtWidgets.QLabel(Dialog)
        self.labelUserProfile.setObjectName("labelUserProfile")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.labelUserProfile.setSizePolicy(sizePolicy)
        self.labelUserProfile.setAlignment(QtCore.Qt.AlignLeft)
        self.labelUserProfile.setFont(general_font)
        self.hlr4.addWidget(self.labelUserProfile)

        self.lineEditUserProfile = QtWidgets.QLineEdit(Dialog)
        self.lineEditUserProfile.setObjectName("lineEditUserProfile")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.lineEditUserProfile.setSizePolicy(sizePolicy)
        self.lineEditUserProfile.setFont(general_font)
        self.hlr4.addWidget(self.lineEditUserProfile)

        self.LineEditUserSpacer = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr4.addItem(self.LineEditUserSpacer)

        # GridLayout -- Row 5 -- HL1 -- Spacer -- Password Label -- Line Edit -- Spacer
        self.hlr5 = QtWidgets.QHBoxLayout()
        self.hlr5.setObjectName("hlr5")
        self.gridLayout.addLayout(self.hlr5, 5, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        self.PasswordSpacer = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr5.addItem(self.PasswordSpacer)

        self.labelPassword = QtWidgets.QLabel(Dialog)
        self.labelPassword.setObjectName("labelPassword")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.labelPassword.setSizePolicy(sizePolicy)
        self.labelPassword.setAlignment(QtCore.Qt.AlignLeft)
        self.labelPassword.setFont(general_font)
        self.hlr5.addWidget(self.labelPassword)

        self.lineEditPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEditPassword.setObjectName("lineEditPassword")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.lineEditPassword.setSizePolicy(sizePolicy)
        self.lineEditPassword.setFont(general_font)
        self.hlr5.addWidget(self.lineEditPassword)

        self.LineEditPassSpacer = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr5.addItem(self.LineEditPassSpacer)

        # GridLayout -- Row 6  -- HL1 -- Spacer -- Confirm Label  -- Line Edit -- Spacer
        self.hlr6 = QtWidgets.QHBoxLayout()
        self.hlr6.setObjectName("hlr6")
        self.gridLayout.addLayout(self.hlr6, 6, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        # keeps alignment for when confirm password is disabled and hidden
        self.r6spacer = QtWidgets.QSpacerItem(75, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        self.hlr6.addSpacerItem(self.r6spacer)

        self.labelConfirmPassword = QtWidgets.QLabel(Dialog)
        self.labelConfirmPassword.setObjectName("labelConfirmPassword")
        self.labelConfirmPassword.setText("Confirm Password:")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.retainSizeWhenHidden()
        self.labelConfirmPassword.setSizePolicy(sizePolicy)
        self.labelConfirmPassword.setAlignment(QtCore.Qt.AlignLeft)
        self.labelConfirmPassword.setFont(general_font)
        self.labelConfirmPassword.setEnabled(True)
        self.labelConfirmPassword.setHidden(True)
        self.hlr6.addWidget(self.labelConfirmPassword)

        self.lineEditConfirmPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditConfirmPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEditConfirmPassword.setObjectName("lineEditConfirmPassword")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.retainSizeWhenHidden()
        self.lineEditConfirmPassword.setSizePolicy(sizePolicy)
        self.lineEditConfirmPassword.setFont(general_font)
        self.lineEditConfirmPassword.setEnabled(False)
        self.lineEditConfirmPassword.setHidden(True)
        self.hlr6.addWidget(self.lineEditConfirmPassword)

        self.LineEditConfirmSpacer = QtWidgets.QSpacerItem(75, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr6.addItem(self.LineEditConfirmSpacer)

        self.labelConfirmPassword.setFixedWidth(200)
        self.labelUserProfile.setFixedWidth(200)
        self.labelPassword.setFixedWidth(200)

        # Grid -- Row 7 -- hlr7 -- Response Label
        self.hlr7 = QtWidgets.QHBoxLayout()
        self.hlr7.setObjectName("hlr8")
        self.gridLayout.addLayout(self.hlr7, 7, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        error_font = QtGui.QFont()
        error_font.setPixelSize(14)

        self.labelResponse = QtWidgets.QLabel()
        self.labelResponse.setObjectName("labelResponse")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.labelResponse.setSizePolicy(sizePolicy)
        self.labelResponse.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.labelResponse.setFont(error_font)
        self.labelResponse.setText("")
        self.hlr7.addWidget(self.labelResponse)

        # GridLayout -- Row 8 -- Buttons -- Login and Quit
        self.hlr8 = QtWidgets.QHBoxLayout()
        self.hlr8.setObjectName("hlr8")
        self.gridLayout.addLayout(self.hlr8, 8, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        self.pushButtonSpacerr8 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hlr8.addSpacerItem(self.pushButtonSpacerr8)

        self.pushButtonLogin = QtWidgets.QPushButton(Dialog)
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.pushButtonLogin.setSizePolicy(sizePolicy)
        self.pushButtonLogin.setEnabled(True)
        self.hlr8.addWidget(self.pushButtonLogin)

        self.pushButtonSubmitProfile = QtWidgets.QPushButton(Dialog)
        self.pushButtonSubmitProfile.setObjectName("pushButtonSubmitProfile")
        self.pushButtonSubmitProfile.setText("Submit")
        self.pushButtonSubmitProfile.setEnabled(False)
        self.pushButtonSubmitProfile.setHidden(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.retainSizeWhenHidden()
        self.pushButtonSubmitProfile.setSizePolicy(sizePolicy)
        self.pushButtonSubmitProfile.setEnabled(True)
        self.hlr8.addWidget(self.pushButtonSubmitProfile)

        self.pushButtonQuit = QtWidgets.QPushButton(Dialog)
        self.pushButtonQuit.setObjectName("pushButtonQuit")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.pushButtonQuit.setSizePolicy(sizePolicy)
        sizePolicy.retainSizeWhenHidden()
        self.pushButtonQuit.setEnabled(True)
        self.hlr8.addWidget(self.pushButtonQuit)

        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName("pushButtonSubmitCancel")
        self.pushButtonCancel.setText("Cancel")
        self.pushButtonCancel.setEnabled(False)
        self.pushButtonCancel.setHidden(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.retainSizeWhenHidden()
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setEnabled(True)
        self.hlr8.addWidget(self.pushButtonCancel)

        self.pushButtonSpacerr9 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hlr8.addSpacerItem(self.pushButtonSpacerr9)

        # GridLayout -- Row 9 -- Button -- New Profile
        self.hlr9 = QtWidgets.QHBoxLayout()
        self.hlr9.setObjectName("hlr9")
        self.gridLayout.addLayout(self.hlr9, 9, 2, 1, 4, alignment=QtCore.Qt.Alignment())

        spacer_width = ((adjusted_width - 100) / 4) - 10
        # Columns 1 and 6 are a set width of 50. Add in the "air" between the spacers and buttons (~9)

        self.pushButtonSpacerr10 = QtWidgets.QSpacerItem(spacer_width, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr9.addSpacerItem(self.pushButtonSpacerr10)

        self.pushButtonNewProfile = QtWidgets.QPushButton(Dialog)
        self.pushButtonNewProfile.setObjectName("pushButtonNewProfile")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.retainSizeWhenHidden()
        self.pushButtonNewProfile.setSizePolicy(sizePolicy)
        self.pushButtonNewProfile.setEnabled(True)
        self.hlr9.addWidget(self.pushButtonNewProfile)

        self.pushButtonSpacerr11 = QtWidgets.QSpacerItem(spacer_width, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr9.addSpacerItem(self.pushButtonSpacerr11)

        # GridLayout -- Row 11 -- Spacer
        self.hlr10 = QtWidgets.QHBoxLayout()
        self.hlr10.setObjectName("hlr10")
        self.gridLayout.addLayout(self.hlr10, 10, 1, 1, 6, alignment=QtCore.Qt.Alignment())

        self.bottomSpacer = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hlr10.addItem(self.bottomSpacer)

        self.labelUserProfile.raise_()
        self.labelPassword.raise_()
        self.lineEditUserProfile.raise_()
        self.lineEditPassword.raise_()
        self.pushButtonLogin.raise_()
        self.pushButtonQuit.raise_()
        self.pushButtonNewProfile.raise_()
        self.labelConfirmPassword.raise_()
        self.lineEditConfirmPassword.raise_()
        self.labelResponse.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEditUserProfile, self.lineEditPassword)
        Dialog.setTabOrder(self.lineEditPassword, self.lineEditConfirmPassword)
        Dialog.setTabOrder(self.lineEditConfirmPassword, self.pushButtonLogin)
        Dialog.setTabOrder(self.pushButtonLogin, self.pushButtonQuit)
        Dialog.setTabOrder(self.pushButtonQuit, self.pushButtonNewProfile)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("LoginScreen", "Alchemical Finances- User Login", None))
        self.labelUserProfile.setText(_translate("Dialog", "Profile Name:"))
        self.labelPassword.setText(_translate("Dialog", "Password:"))
        self.pushButtonLogin.setText(_translate("Dialog", "Login"))
        self.pushButtonQuit.setText(_translate("Dialog", "Quit"))
        self.pushButtonNewProfile.setText(_translate("Dialog", "New Profile"))
        self.labelTitle.setText(_translate("Dialog", "Alchemical Finances"))
        self.labelSubTitle.setText(_translate("Dialog", "\"Hands On Personal Finance\""))


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")


