#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabs.com

# This Dialog is a Subwindow for the Mainwindow MdiArea
# This will generate a stacked networth graph
import pickle

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_OverTimeGraph(object):
    def setupUi(self, Dialog):
        # Dialog settings
        Dialog.setObjectName("NetWorthGraph")
        Dialog.setWindowTitle("Value Over Time Graphs")  # Will be dynamically changed in the backend
        Dialog.setWindowIcon(QtGui.QIcon('Resources/AF Logo.png'))  # Consider hiring an artist to make different icons for different account types

        # Dialog size
        screen_dimensions_file = open("Resources/dimensions.pkl", "rb")
        screen_dimensions = pickle.load(screen_dimensions_file)
        screen_dimensions_file.close()

        work_area = screen_dimensions[1]

        size_factor = 0.50

        if 3840 <= work_area[2]:
            size_factor = size_factor

        if 2560 <= work_area[2] < 3840:
            size_factor = (3840 * size_factor) / 2560

        if 1920 <= work_area[2] < 2560:
            size_factor = (3840 * size_factor) / 1920

        if 1600 <= work_area[2] < 1920:
            size_factor = (3840 * size_factor) / 1600

        if work_area[2] < 1600:
            size_factor = (3840 * size_factor) / 1366

        adjusted_width = work_area[2] * size_factor  # for non full screen sizing
        adjusted_height = work_area[3] * size_factor
        Dialog.resize(adjusted_width, adjusted_height)

        # Font and Size Policy
        header_font = QtGui.QFont()
        header_font.setPixelSize(24)
        header_font.setBold(True)

        general_font = QtGui.QFont()
        general_font.setPixelSize(14)
        general_font.setBold(False)

        subheader_font = QtGui.QFont()
        subheader_font.setPixelSize(14)
        subheader_font.setBold(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        titleSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # hBLayout1
        self.hBLayout1 = QtWidgets.QHBoxLayout(Dialog)
        self.hBLayout1.setObjectName("hBLayout1")

        # hBLayout1 --> hSpacer -- vBLayout1 -- hSpacer
        self.hSpacer1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer1)

        self.vBLayout1 = QtWidgets.QVBoxLayout()
        self.vBLayout1.setObjectName("vBLayout1")
        self.hBLayout1.addLayout(self.vBLayout1)

        self.hSpacer2 = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer2)

        # vBLayout1 --> vSpacer -- Label, hBLayout2, hBLayout3
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 15, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer1)

        self.lGraphTitle = QtWidgets.QLabel()
        self.lGraphTitle.setObjectName("lGraphTitle")
        self.lGraphTitle.setText("Net Worth Over Time")
        self.lGraphTitle.setFont(header_font)
        self.lGraphTitle.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.lGraphTitle.setSizePolicy(titleSizePolicy)
        self.vBLayout1.addWidget(self.lGraphTitle)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBLayout2")
        self.vBLayout1.addLayout(self.hBLayout2)

        self.hBLayout3 = QtWidgets.QHBoxLayout()
        self.hBLayout3.setObjectName("hBLayout3")
        self.vBLayout1.addLayout(self.hBLayout3)

        # vBLayout1 --> hBlayout2 --> --> combobox -- vSpacer
        self.graphAccountComboBox = QtWidgets.QComboBox()
        self.graphAccountComboBox.setObjectName("graphAccountComboBox")
        self.graphAccountComboBox.setFont(general_font)
        self.graphAccountComboBox.setFixedWidth(350)
        self.graphAccountComboBox.setFixedHeight(25)
        self.hBLayout2.addWidget(self.graphAccountComboBox)

        self.hspacer6 = QtWidgets.QSpacerItem(adjusted_width - 350, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.hBLayout2.addItem(self.hspacer6)

        # vBLayout1 --> hBLayout3 --> --> vSpacer3 -- nWFrame -- infoFrame
        self.vSpacer2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout3.addItem(self.vSpacer2)

        self.nWFrame = QtWidgets.QFrame()
        self.nWFrame.setObjectName("nWFrame")
        # self.nWFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.nWFrame.setLineWidth(1)
        self.hBLayout3.addWidget(self.nWFrame)

        self.infoFrame = QtWidgets.QFrame()
        self.infoFrame.setObjectName("inforFrame")
        self.infoFrame.setFixedWidth(adjusted_width * 0.15)
        # self.infoFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.infoFrame.setLineWidth(3)
        self.hBLayout3.addWidget(self.infoFrame)

        # vBLayout1 --> hBLayout3 --> infoFrame --> vBLayout4
        self.vBLayout4 = QtWidgets.QVBoxLayout(self.infoFrame)
        self.vBLayout4.setObjectName("vBLayout4")

        # vBLayout1 --> hBLayout3 --> infoFrame --> vBLayout4 --> --> spacer -- Label -- hBLayout4 -- hBLayout5 -- hBLayout6 -- Label -- Peak Frame -- Spacer -- Low Frame
        self.vSpacer3 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout4.addItem(self.vSpacer3)

        self.lLegend = QtWidgets.QLabel()
        self.lLegend.setObjectName("lLengend")
        self.lLegend.setText("Legend")
        self.lLegend.setFont(header_font)
        self.lLegend.setAlignment(QtCore.Qt.AlignHCenter)
        self.lLegend.setSizePolicy(sizePolicy)
        self.vBLayout4.addWidget(self.lLegend)

        # Holds Gross Legend Information
        self.hBLayout4 = QtWidgets.QHBoxLayout()
        self.hBLayout4.setObjectName("hBLayout4")
        self.vBLayout4.addLayout(self.hBLayout4)

        self.lGrossLegend = QtWidgets.QLabel()
        self.lGrossLegend.setObjectName("lGrossLegend")
        self.lGrossLegend.setFixedWidth(75)
        self.lGrossLegend.setFixedHeight(15)
        self.lGrossLegend.setStyleSheet("background: rgb(39, 89, 41)")
        self.hBLayout4.addWidget(self.lGrossLegend)

        self.lGrossValue = QtWidgets.QLabel()
        self.lGrossValue.setObjectName("lGrossValue")
        self.lGrossValue.setText("Gross Worth")
        self.lGrossValue.setFont(general_font)
        self.lGrossValue.setSizePolicy(sizePolicy)
        self.hBLayout4.addWidget(self.lGrossValue)

        # Holds Asset Legend Information
        self.hBLayout5 = QtWidgets.QHBoxLayout()
        self.hBLayout5.setObjectName("hBLayout5")
        self.vBLayout4.addLayout(self.hBLayout5)

        self.lNetLegend = QtWidgets.QLabel()
        self.lNetLegend.setObjectName("lNetLegend")
        self.lNetLegend.setFixedWidth(75)
        self.lNetLegend.setFixedHeight(15)
        self.lNetLegend.setStyleSheet("background: rgb(56, 128, 59)")
        self.hBLayout5.addWidget(self.lNetLegend)

        self.lNetValue = QtWidgets.QLabel()
        self.lNetValue.setObjectName("lNetValue")
        self.lNetValue.setText("Net Worth")
        self.lNetValue.setFont(general_font)
        self.lNetValue.setSizePolicy(sizePolicy)
        self.hBLayout5.addWidget(self.lNetValue)

        # Holds Liabilities Legend Information
        self.hBLayout6 = QtWidgets.QHBoxLayout()
        self.hBLayout6.setObjectName("hBLayout6")
        self.vBLayout4.addLayout(self.hBLayout6)

        self.lLiabilitiesLegend = QtWidgets.QLabel()
        self.lLiabilitiesLegend.setObjectName("lLiabilitiesLegend ")
        self.lLiabilitiesLegend.setFixedWidth(75)
        self.lLiabilitiesLegend.setFixedHeight(15)
        self.lLiabilitiesLegend.setStyleSheet("background: rgb(128, 56, 56)")
        self.hBLayout6.addWidget(self.lLiabilitiesLegend)

        self.lLiabilitiesValue = QtWidgets.QLabel()
        self.lLiabilitiesValue.setObjectName("lLiabilitiesValue")
        self.lLiabilitiesValue.setText("Active Liabilities")
        self.lLiabilitiesValue.setFont(general_font)
        self.lLiabilitiesValue.setSizePolicy(sizePolicy)
        self.hBLayout6.addWidget(self.lLiabilitiesValue)

        self.vSpacer4 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout4.addItem(self.vSpacer4)

        self.lHighlights = QtWidgets.QLabel()
        self.lHighlights.setObjectName("lHeighlights")
        self.lHighlights.setText("Peak Values")
        self.lHighlights.setFont(header_font)
        self.lHighlights.setAlignment(QtCore.Qt.AlignHCenter)
        self.lHighlights.setSizePolicy(sizePolicy)
        self.vBLayout4.addWidget(self.lHighlights)

        self.peakFrame = QtWidgets.QFrame()
        self.peakFrame.setObjectName("peakFrame")
        # self.peakFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.peakFrame.setLineWidth(1)
        self.peakFrame.setSizePolicy(sizePolicy)
        self.vBLayout4.addWidget(self.peakFrame)

        self.vSpacer5 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout4.addItem(self.vSpacer5)

        self.lLowPoints = QtWidgets.QLabel()
        self.lLowPoints.setObjectName("lLowPoints")
        self.lLowPoints.setText("Lowest Points")
        self.lLowPoints.setFont(header_font)
        self.lLowPoints.setAlignment(QtCore.Qt.AlignHCenter)
        self.lLowPoints.setSizePolicy(sizePolicy)
        self.vBLayout4.addWidget(self.lLowPoints)

        self.lowFrame = QtWidgets.QFrame()
        self.lowFrame.setObjectName("lowFrame")
        # self.lowFrame.setFrameShape(QtWidgets.QFrame.Panel)
        # self.lowFrame.setLineWidth(1)
        self.lowFrame.setSizePolicy(sizePolicy)
        self.vBLayout4.addWidget(self.lowFrame)

        self.vSpacer6 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.vBLayout4.addItem(self.vSpacer6)

        # vBLayout4 --> peakFrame --> hBlayout7 -- > vBLayout vBLayout
        self.vBLayout2 = QtWidgets.QVBoxLayout(self.peakFrame)
        self.vBLayout2.setObjectName("vBLayout2")

        # vBLayout4 --> peakFrame --> hBlayout7 --> vBLayout2 --->Label
        self.lPeakGWLabel = QtWidgets.QLabel()
        self.lPeakGWLabel.setObjectName("lPeakGWLabel")
        self.lPeakGWLabel.setText("Gross Worth:")
        self.lPeakGWLabel.setFont(subheader_font)
        self.lPeakGWLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lPeakGWLabel.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPeakGWLabel)

        self.lPGWorth = QtWidgets.QLabel()
        self.lPGWorth.setObjectName("lPGWorth")
        self.lPGWorth.setText(" $10,000,000.00 on 03/07/2021")
        self.lPGWorth.setFont(general_font)
        self.lPGWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lPGWorth.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPGWorth)

        self.lPeakLVLabel = QtWidgets.QLabel()
        self.lPeakLVLabel.setObjectName("lPeakLVLabel")
        self.lPeakLVLabel.setText("Liability:")
        self.lPeakLVLabel.setFont(subheader_font)
        self.lPeakLVLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lPeakLVLabel.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPeakLVLabel)

        self.lPLWorth = QtWidgets.QLabel()
        self.lPLWorth.setObjectName("lPLWorth")
        self.lPLWorth.setText("$10,000,000.00 on 03/07/2021")
        self.lPLWorth.setFont(general_font)
        self.lPLWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lPLWorth.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPLWorth)

        self.lPeakNWLabel = QtWidgets.QLabel()
        self.lPeakNWLabel.setObjectName("lPeakNWLabel")
        self.lPeakNWLabel.setText("Net Worth:")
        self.lPeakNWLabel.setFont(subheader_font)
        self.lPeakNWLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lPeakNWLabel.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPeakNWLabel)

        self.lPNWorth = QtWidgets.QLabel()
        self.lPNWorth.setObjectName("lPNWorth")
        self.lPNWorth.setText("$10,000,000.00 on 03/07/2021")
        self.lPNWorth.setFont(general_font)
        self.lPNWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lPNWorth.setSizePolicy(sizePolicy)
        self.vBLayout2.addWidget(self.lPNWorth)

        # vBLayout4 --> lowFrame --> hBlayout8 -- > vBLayout vBLayout
        self.vBLayout3 = QtWidgets.QVBoxLayout(self.lowFrame)
        self.vBLayout3.setObjectName("vBLayout3")

        # vBLayout4 --> peakFrame --> hBlayout7 --> vBLayout2 --->Label
        self.lLowGWLabel = QtWidgets.QLabel()
        self.lLowGWLabel.setObjectName("lLowGWLabel")
        self.lLowGWLabel.setText("Gross Worth:")
        self.lLowGWLabel.setFont(subheader_font)
        self.lLowGWLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lLowGWLabel.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLowGWLabel)

        self.lLGWorth = QtWidgets.QLabel()
        self.lLGWorth.setObjectName("lLGWorth")
        self.lLGWorth.setText("$10,000,000.00 on 03/07/2021")
        self.lLGWorth.setFont(general_font)
        self.lLGWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lLGWorth.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLGWorth)

        self.lLowLVLabel = QtWidgets.QLabel()
        self.lLowLVLabel.setObjectName("lLowLVLabel")
        self.lLowLVLabel.setText("Liability:")
        self.lLowLVLabel.setFont(subheader_font)
        self.lLowLVLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lLowLVLabel.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLowLVLabel)

        self.lLLWorth = QtWidgets.QLabel()
        self.lLLWorth.setObjectName("lLLWorth")
        self.lLLWorth.setText("$10,000,000.00 on 03/07/2021")
        self.lLLWorth.setFont(general_font)
        self.lLLWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lLLWorth.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLLWorth)

        self.lLowNWLabel = QtWidgets.QLabel()
        self.lLowNWLabel.setObjectName("lLowNWLabel")
        self.lLowNWLabel.setText("Net Worth:")
        self.lLowNWLabel.setFont(subheader_font)
        self.lLowNWLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.lLowNWLabel.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLowNWLabel)

        self.lLNWorth = QtWidgets.QLabel()
        self.lLNWorth.setObjectName("lPNWorth")
        self.lLNWorth.setText("$10,000,000.00 on 03/07/2021")
        self.lLNWorth.setFont(general_font)
        self.lLNWorth.setAlignment(QtCore.Qt.AlignLeft)
        self.lLNWorth.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lLNWorth)


if __name__ == "__main__":
    print("error")