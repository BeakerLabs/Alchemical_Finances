#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_SaveDF(object):
    def setupUi(self, Dialog):
        # Dialog Settings
        Dialog.setObjectName("Save_DataFrames")

        Dialog.resize(800, 150)
        Dialog.setMinimumSize(800, 150)
        Dialog.setMaximumSize(800, 150)

        # Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.FramelessWindowHint)

        # Core Layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("HorizontalLayout")

        text_font = QtGui.QFont()
        text_font.setPixelSize(24)
        text_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.retainSizeWhenHidden()

        # Outer Horizontal Layout
        self.hSpacer1 = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout.addItem(self.hSpacer1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.hSpacer2 = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.horizontalLayout.addItem(self.hSpacer2)

        # Inner Vertical Layout
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(self.vSpacer1)

        self.labelActionInProgress = QtWidgets.QLabel()
        self.labelActionInProgress.setObjectName("labelActionInProgress")
        self.labelActionInProgress.setText("In Progress of Saving:  ")
        self.labelActionInProgress.setFont(text_font)
        self.labelActionInProgress.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.labelActionInProgress.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.labelActionInProgress)

        self.saveProgressBar = QtWidgets.QProgressBar()
        self.saveProgressBar.setMinimum(0)
        self.saveProgressBar.setMaximum(100)
        self.saveProgressBar.setProperty("value", 0)
        self.verticalLayout.addWidget(self.saveProgressBar)

        self.vSpacer2 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(self.vSpacer2)


if __name__ == "__main__":
    print("Error: Check Executable")

