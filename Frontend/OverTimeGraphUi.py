# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_Dialog(object):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(1210, 801)
#         self.labelTest = QtWidgets.QLabel(Dialog)
#         self.labelTest.setGeometry(QtCore.QRect(20, 740, 1170, 20))
#         self.labelTest.setObjectName('testLabel')
#
#         self.retranslateUi(Dialog)
#         QtCore.QMetaObject.connectSlotsByName(Dialog)
#
#     def retranslateUi(self, Dialog):
#         _translate = QtCore.QCoreApplication.translate
#         Dialog.setWindowTitle(_translate("Dialog", "Net Worth Graph"))
#         self.labelTest.setText(_translate("Dialog", "TextLabel"))

# This Dialog is a Subwindow for the Mainwindow MdiArea
# This will generate a stacked networth graph

from PySide6 import QtCore, QtGui, QtWidgets
from win32api import GetMonitorInfo, MonitorFromPoint


class Ui_OverTimeGraph(object):
    def setupUi(self, Dialog):
        # Dialog settings
        Dialog.setObjectName("NetWorthGraph")
        Dialog.setWindowTitle("Value Over Time Graphs")  # Will be dynamically changed in the backend
        Dialog.setWindowIcon(QtGui.QIcon("AF Logo.png"))  # Consider hiring an artist to make different icons for different account types

        # Dialog size
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        adjusted_width = work_area[2] * 0.5  # for non full screen sizing
        adjusted_height = work_area[3] * 0.5
        Dialog.resize(adjusted_width, adjusted_height)

        # Font and Size Policy
        header_font = QtGui.QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)

        general_font = QtGui.QFont()
        general_font.setPointSize(12)
        general_font.setBold(False)

        legend_font = QtGui.QFont()
        legend_font.setPointSize(8)
        legend_font.setBold(False)

        pushButton_font = QtGui.QFont()
        pushButton_font.setPointSize(12)
        pushButton_font.setBold(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        altSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # hBLayout1
        self.hBLayout1 = QtWidgets.QHBoxLayout(Dialog)
        self.hBLayout1.setObjectName("hBLayout1")

        # hBLayout1 --> hSpacer -- vBLayout1 -- hSpacer
        self.hSpacer1 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer1)

        self.vBLayout1 = QtWidgets.QVBoxLayout()
        self.vBLayout1.setObjectName("vBLayout1")
        self.hBLayout1.addLayout(self.vBLayout1)

        self.hSpacer2 = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer2)

        # vBLayout1 --> vSpacer -- Label, hBLayout2, hBLayout3, hBLayout4, hBLayout5 -- vSpacer
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer1)

        self.lGraphTitle = QtWidgets.QLabel()
        self.lGraphTitle.setObjectName("lGraphTitle")
        self.lGraphTitle.setText("Net Worth Over Time")
        self.lGraphTitle.setFont(header_font)
        self.lGraphTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.lGraphTitle.setSizePolicy(sizePolicy)
        self.vBLayout1.addWidget(self.lGraphTitle)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBLayout2")
        self.vBLayout1.addLayout(self.hBLayout2)

        self.hBLayout3 = QtWidgets.QHBoxLayout()
        self.hBLayout3.setObjectName("hBLayout3")
        self.vBLayout1.addLayout(self.hBLayout3)

        self.hBLayout4 = QtWidgets.QHBoxLayout()
        self.hBLayout4.setObjectName("hBLayout4")
        self.vBLayout1.addLayout(self.hBLayout4)

        self.hBLayout5 = QtWidgets.QHBoxLayout()
        self.hBLayout5.setObjectName("hBLayout5")
        self.vBLayout1.addLayout(self.hBLayout5)

        self.vSpacer2 = QtWidgets.QSpacerItem(0, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer2)

        # vBLayout1 --> hBlayout2 --> --> combobox -- vSpacer
        self.graphAccountComboBox = QtWidgets.QComboBox()
        self.graphAccountComboBox.setObjectName("graphAccountComboBox")
        self.graphAccountComboBox.setFont(general_font)
        self.graphAccountComboBox.setFixedWidth(350)
        self.graphAccountComboBox.setFixedHeight(25)
        self.hBLayout2.addWidget(self.graphAccountComboBox)

        self.hspacer6 = QtWidgets.QSpacerItem(adjusted_width - 350, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout2.addItem(self.hspacer6)

        # vBLayout1 --> hBLayout3 --> --> vSpacer3 -- nWFrame
        self.vSpacer2 = QtWidgets.QSpacerItem(0, adjusted_height * 0.66, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout3.addItem(self.vSpacer2)

        self.nWFrame = QtWidgets.QFrame()
        self.nWFrame.setObjectName("nWFrame")
        self.nWFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.nWFrame.setLineWidth(1)
        self.hBLayout3.addWidget(self.nWFrame)

        # vBLayout1 --> hBLayout4
        self.legendSpacer1 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout4.addItem(self.legendSpacer1)

        self.lGrossLegend = QtWidgets.QLabel()
        self.lGrossLegend.setObjectName("lGrossLegend")
        self.lGrossLegend.setFixedWidth(75)
        self.lGrossLegend.setFixedHeight(15)
        self.lGrossLegend.setStyleSheet("background: rgb(39, 89, 41)")
        self.hBLayout4.addWidget(self.lGrossLegend)

        self.lGrossValue = QtWidgets.QLabel()
        self.lGrossValue.setObjectName("lGrossValue")
        self.lGrossValue.setText("Gross Worth")
        self.lGrossValue.setFont(legend_font)
        self.lGrossValue.setSizePolicy(altSizePolicy)
        self.hBLayout4.addWidget(self.lGrossValue)

        self.lNetLegend = QtWidgets.QLabel()
        self.lNetLegend.setObjectName("lNetLegend")
        self.lNetLegend.setFixedWidth(75)
        self.lNetLegend.setFixedHeight(15)
        self.lNetLegend.setStyleSheet("background: rgb(56, 128, 59)")
        self.hBLayout4.addWidget(self.lNetLegend)

        self.lNetValue = QtWidgets.QLabel()
        self.lNetValue.setObjectName("lNetValue")
        self.lNetValue.setText("Net Worth")
        self.lNetValue.setFont(legend_font)
        self.lNetValue.setSizePolicy(altSizePolicy)
        self.hBLayout4.addWidget(self.lNetValue)

        self.lLiabilitiesLegend = QtWidgets.QLabel()
        self.lLiabilitiesLegend.setObjectName("lLiabilitiesLegend ")
        self.lLiabilitiesLegend.setFixedWidth(75)
        self.lLiabilitiesLegend.setFixedHeight(15)
        self.lLiabilitiesLegend.setStyleSheet("background: rgb(128, 56, 56)")
        self.hBLayout4.addWidget(self.lLiabilitiesLegend)

        self.lLiabilitiesValue = QtWidgets.QLabel()
        self.lLiabilitiesValue.setObjectName("lLiabilitiesValue")
        self.lLiabilitiesValue.setText("Active Liabilities")
        self.lLiabilitiesValue.setFont(legend_font)
        self.lLiabilitiesValue.setSizePolicy(altSizePolicy)
        self.hBLayout4.addWidget(self.lLiabilitiesValue)

        self.legendSpacer2 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout4.addItem(self.legendSpacer2)

        # hBLayout5 --> hspacer3 -- peakFrame -- hspacer4 -- lowFrame -- hspacer5
        self.hSpacer3 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout5.addItem(self.hSpacer3)

        self.peakFrame = QtWidgets.QFrame()
        self.peakFrame.setObjectName("peakFrame")
        self.peakFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.peakFrame.setLineWidth(1)
        self.peakFrame.setSizePolicy(altSizePolicy)
        self.hBLayout5.addWidget(self.peakFrame)

        self.hSpacer4 = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout5.addItem(self.hSpacer4)

        self.lowFrame = QtWidgets.QFrame()
        self.lowFrame.setObjectName("lowFrame")
        self.lowFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.lowFrame.setLineWidth(1)
        self.lowFrame.setSizePolicy(altSizePolicy)
        self.hBLayout5.addWidget(self.lowFrame)

        self.hSpacer5 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout5.addItem(self.hSpacer5)

        # hBLayout4 --> peakFrame --> --> vBLayout2
        self.vBLayout2 = QtWidgets.QVBoxLayout(self.peakFrame)
        self.vBLayout2.setObjectName("vBLayout2")

        # hBLayout4 --> peakFrame --> vBLayout2 ---> 3x Label
        self.lPGWorth = QtWidgets.QLabel()
        self.lPGWorth.setObjectName("lPGWorth")
        self.lPGWorth.setText("Peak Gross Worth of $10,000,000.00 on 03/07/2021")
        self.lPGWorth.setFont(general_font)
        self.lPGWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lPGWorth.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPGWorth)

        self.lPNWorth = QtWidgets.QLabel()
        self.lPNWorth.setObjectName("lPNWorth")
        self.lPNWorth.setText("Peak Net Worth of $10,000,000.00 on 03/07/2021")
        self.lPNWorth.setFont(general_font)
        self.lPNWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lPNWorth.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPNWorth)

        self.lPLWorth = QtWidgets.QLabel()
        self.lPGWorth.setObjectName("lPGWorth")
        self.lPLWorth.setText("Peak Liabilities Worth $10,000,000.00 on 03/07/2021")
        self.lPLWorth.setFont(general_font)
        self.lPLWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lPLWorth.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPLWorth)

        # hBLayout4 --> lowFrame --> vBLayout3
        self.vBLayout3 = QtWidgets.QVBoxLayout(self.lowFrame)
        self.vBLayout3.setObjectName("vBLayout3")

        # hBLayout4 --> lowFrame --> vBLayout3 --->  3x Label
        self.lLGWorth = QtWidgets.QLabel()
        self.lLGWorth.setObjectName("lLGWorth")
        self.lLGWorth.setText("Lowest Gross Worth of $10,000,000.00 on 03/07/2021")
        self.lLGWorth.setFont(general_font)
        self.lLGWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lLGWorth.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLGWorth)

        self.lLNWorth = QtWidgets.QLabel()
        self.lLNWorth.setObjectName("lPNWorth")
        self.lLNWorth.setText("Lowest Net Worth of $10,000,000.00 on 03/07/2021")
        self.lLNWorth.setFont(general_font)
        self.lLNWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lLNWorth.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLNWorth)

        self.lLLWorth = QtWidgets.QLabel()
        self.lLLWorth.setObjectName("lPGWorth")
        self.lLLWorth.setText("Lowest Liabilities Worth $10,000,000.00 on 03/07/2021")
        self.lLLWorth.setFont(general_font)
        self.lLLWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lLLWorth.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLLWorth)


if __name__ == "__main__":
    print("error")