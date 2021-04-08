# This file will be used to generate the About Alcehmical Finances SubWindow

import codecs
import pickle

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPixmap
from win32api import GetMonitorInfo, MonitorFromPoint


class Ui_AboutScreen(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("AboutScreen")
        Dialog.setWindowTitle("About A.F.")
        Dialog.setWindowIcon(QtGui.QIcon('AF Logo.png'))

        # Obtain and use the monitor screen to determine the width of the dialog box
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        adjusted_width = work_area[2] * 0.5  # for non full screen sizing
        adjusted_height = work_area[3] * 0.5
        Dialog.resize(adjusted_width, adjusted_height)

        dialog_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        dialog_sizePolicy.setHorizontalStretch(0)
        dialog_sizePolicy.setVerticalStretch(0)

        self.outerHLayout = QtWidgets.QHBoxLayout(Dialog)
        self.outerHLayout.setObjectName("outerHLayout")

        # Left Horizontal Spacer
        self.hSpacer0 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.outerHLayout.addItem(self.hSpacer0)

        self.coreVLayout = QtWidgets.QVBoxLayout()
        self.coreVLayout.setObjectName("coreVLayout")
        self.outerHLayout.addLayout(self.coreVLayout)

        # Right Horizontal Spacer
        self.hSpacerInfinity = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.outerHLayout.addItem(self.hSpacerInfinity)

        # Core QVBoxLayout --> Spacer -- QHBoxLayout #1 -- spacer -- QHBoxLayout #2 -- spacer -- QVBoxLayout # 1

        self.vSpacer0 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.coreVLayout.addItem(self.vSpacer0)

        # Contains the logo and title layout widgets. However not visually used.
        self.testFrame = QtWidgets.QFrame()
        self.testFrame.setObjectName("testframe")
        # self.testFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.testFrame.setLineWidth(3)
        testlFrame_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.testFrame.setSizePolicy(testlFrame_sizePolicy)
        self.coreVLayout.addWidget(self.testFrame)

        self.hLayoutOne = QtWidgets.QHBoxLayout(self.testFrame)
        self.hLayoutOne.setObjectName("HLayoutOne")

        self.vSpacer1 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.coreVLayout.addItem(self.vSpacer1)

        self.hLayoutTwo = QtWidgets.QHBoxLayout()
        self.hLayoutTwo.setObjectName("HLayoutTwo")
        self.coreVLayout.addLayout(self.hLayoutTwo)

        self.vSpacer2 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.coreVLayout.addItem(self.vSpacer2)

        self.vLayoutOne = QtWidgets.QVBoxLayout()
        self.hLayoutOne.setObjectName("hLayoutOne")
        self.coreVLayout.addLayout(self.vLayoutOne)

        self.vSpacer3 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.coreVLayout.addItem(self.vSpacer3)

        # QHBoxLayout #1 --> Logo -- QVBoxLayout #2
        # Logo
        self.logoImage = QtWidgets.QLabel()
        self.logoImage.setObjectName("logoImage")
        Image = QPixmap("AF Logo.png")
        logoAdjustment = Image.scaled(248, 248)
        self.logoImage.setPixmap(logoAdjustment)
        image_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.logoImage.setSizePolicy(image_sizePolicy)
        self.hLayoutOne.addWidget(self.logoImage)

        self.vLayoutTwo = QtWidgets.QVBoxLayout()
        self.vLayoutTwo.setObjectName("VLayoutTwo")
        self.hLayoutOne.addLayout(self.vLayoutTwo)

        # QVBoxLayout #2 --> Label -- Label
        # Program Name
        # Program Tagline

        name_font = QtGui.QFont()
        name_font.setPointSize(36)
        name_font.setBold(True)

        tag_font = QtGui.QFont()
        tag_font.setPointSize(28)
        tag_font.setItalic(True)

        self.staticProgramName = QtWidgets.QLabel()
        self.staticProgramName.setObjectName("ProgramName")
        self.staticProgramName.setText("    Alchemical Finances -- Reformulated")
        self.staticProgramName.setAlignment(QtCore.Qt.AlignLeft)
        self.staticProgramName.setFont(name_font)
        self.vLayoutTwo.addWidget(self.staticProgramName)

        self.staticTagLine = QtWidgets.QLabel()
        self.staticTagLine.setObjectName("TagLine")
        self.staticTagLine.setText("     -- Hands on Personal Finance --")
        self.staticTagLine.setAlignment(QtCore.Qt.AlignLeft)
        self.staticTagLine.setFont(tag_font)
        self.vLayoutTwo.addWidget(self.staticTagLine)

        self.vSpacer5 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.vLayoutTwo.addItem(self.vSpacer5)

        # QHBoxLayout #2 --> QVBoxLayout #3 -- Horizontal Spacer (0 height // 100 width) --QVBoxLayout #4
        self.vLayoutThree = QtWidgets.QVBoxLayout()
        self.vLayoutThree.setObjectName("VLayoutThree")
        self.hLayoutTwo.addLayout(self.vLayoutThree)

        self.hSpacer1 = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hLayoutTwo.addItem(self.hSpacer1)

        self.vLayoutFour = QtWidgets.QVBoxLayout()
        self.vLayoutFour.setObjectName("VLayoutFour")
        self.hLayoutTwo.addLayout(self.vLayoutFour)

        self.hSpacer2 = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hLayoutTwo.addItem(self.hSpacer2)

        # QVBoxLayout #3 --> Horizontal spacer (0 height // 150 width) -- 4x Label
        # staticVersion
        # staticDeveloper
        # staticReleaseDate
        # StaticContact

        static_font = QtGui.QFont()
        static_font.setPointSize(18)
        static_font.setBold(True)

        self.staticVersion = QtWidgets.QLabel()
        self.staticVersion.setObjectName("staticVersion")
        self.staticVersion.setText(" Version:")
        self.staticVersion.setAlignment(QtCore.Qt.AlignLeft)
        self.staticVersion.setFont(static_font)
        self.vLayoutThree.addWidget(self.staticVersion)

        self.staticDeveloper = QtWidgets.QLabel()
        self.staticDeveloper.setObjectName("staticDeveloper")
        self.staticDeveloper.setText(" Developer:")
        self.staticDeveloper.setAlignment(QtCore.Qt.AlignLeft)
        self.staticDeveloper.setFont(static_font)
        self.vLayoutThree.addWidget(self.staticDeveloper)

        self.staticReleaseDate = QtWidgets.QLabel()
        self.staticReleaseDate.setObjectName("staticReleaseDate")
        self.staticReleaseDate.setText(" Release Date:")
        self.staticReleaseDate.setAlignment(QtCore.Qt.AlignLeft)
        self.staticReleaseDate.setFont(static_font)
        self.vLayoutThree.addWidget(self.staticReleaseDate)

        self.staticContact = QtWidgets.QLabel()
        self.staticContact.setObjectName("staticContact")
        self.staticContact.setText(" Contact:")
        self.staticContact.setAlignment(QtCore.Qt.AlignLeft)
        self.staticContact.setFont(static_font)
        self.vLayoutThree.addWidget(self.staticContact)

        # QVBoxLayout #3 --> 4x Label
        # version
        # developer
        # releaseDate
        # contact

        kinetic_font = QtGui.QFont()
        kinetic_font.setPointSize(18)
        kinetic_font.setBold(False)

        self.versionFile = codecs.open("Spoon/version", "r", "utf-8-sig")
        self.version = self.versionFile.read().replace('\n', '')
        self.versionFile.close()

        self.aboutFile = open("Spoon/AboutInfo.pkl", "rb")
        self.aboutDict = pickle.load(self.aboutFile)
        self.aboutFile.close()

        self.kineticVersion = QtWidgets.QLabel()
        self.kineticVersion.setObjectName("kineticVersion")
        self.kineticVersion.setText(self.version)
        self.kineticVersion.setAlignment(QtCore.Qt.AlignLeft)
        self.kineticVersion.setFont(kinetic_font)
        self.vLayoutFour.addWidget(self.kineticVersion)

        self.kineticDeveloper = QtWidgets.QLabel()
        self.kineticDeveloper.setObjectName("kineticDeveloper")
        self.kineticDeveloper.setText(self.aboutDict[self.version][0])
        self.kineticDeveloper.setAlignment(QtCore.Qt.AlignLeft)
        self.kineticDeveloper.setFont(kinetic_font)
        self.vLayoutFour.addWidget(self.kineticDeveloper)

        self.kineticReleaseDate = QtWidgets.QLabel()
        self.kineticReleaseDate.setObjectName("kineticReleaseDate")
        self.kineticReleaseDate.setText(self.aboutDict[self.version][1])
        self.kineticReleaseDate.setAlignment(QtCore.Qt.AlignLeft)
        self.kineticReleaseDate.setFont(kinetic_font)
        self.vLayoutFour.addWidget(self.kineticReleaseDate)

        self.kineticContact = QtWidgets.QLabel()
        self.kineticContact.setObjectName("kineticContact")
        self.kineticContact.setText(self.aboutDict[self.version][2])
        self.kineticContact.setAlignment(QtCore.Qt.AlignLeft)
        self.kineticContact.setFont(kinetic_font)
        self.vLayoutFour.addWidget(self.kineticContact)

        # QVBoxLayout# 1 --> 2x Label
        # staticBackground
        # Background
        self.staticBackground = QtWidgets.QLabel()
        self.staticBackground.setObjectName("staticBackground")
        self.staticBackground.setText(" Program History")
        self.staticBackground.setAlignment(QtCore.Qt.AlignLeft)
        self.staticBackground.setFont(static_font)
        self.vLayoutOne.addWidget(self.staticBackground)

        self.backgroundScroll = QtWidgets.QScrollArea()
        self.backgroundScroll.adjustSize()
        self.backgroundScroll.setFrameStyle(0)
        self.backgroundScroll.horizontalScrollBar().setEnabled(False)
        self.backgroundScroll.setWidgetResizable(True)
        self.vLayoutOne.addWidget(self.backgroundScroll)

        widget = QtWidgets.QWidget()
        self.backgroundScroll.setWidget(widget)
        self.scrollLayout = QtWidgets.QVBoxLayout(widget)

        self.kineticBackground = QtWidgets.QLabel()
        self.kineticBackground.setObjectName("kineticBackground")
        # text = "This text will surely aggrivate someone. " * 1000
        self.kineticBackground.setText(self.aboutDict[self.version][3])
        self.kineticBackground.setAlignment(QtCore.Qt.AlignLeft)
        self.kineticBackground.setFont(kinetic_font)
        self.kineticBackground.setWordWrap(True)
        self.scrollLayout.addWidget(self.kineticBackground)


if __name__ == "__main__":
    print("error")