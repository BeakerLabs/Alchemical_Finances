# Dialog object created to be a canvas for the Code Generate the Summary Report

# Some static layout attributes will be generated here and have the visuals added later.
# This should allow for cleaning flowing code.

from PySide6 import QtCore, QtGui, QtWidgets
from win32api import GetMonitorInfo, MonitorFromPoint


class Ui_Summary(object):
    def setupUi(self, Dialog):
        # Dialog Settings
        Dialog.setObjectName("SummaryDialog")
        Dialog.setWindowTitle("Summary")
        Dialog.setWindowIcon(QtGui.QIcon('AF Logo.png'))

        # Obtain and use the monitor screen to determine with width of the dialog box
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")
        adjusted_width = work_area[2] * 0.5  # for non full screen sizing
        adjusted_height = work_area[3] * 0.5
        Dialog.resize(adjusted_width, adjusted_height)

        # Font and Size Policy
        general_font = QtGui.QFont()
        general_font.setPointSize(12)
        general_font.setBold(False)

        header_font = QtGui.QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # CentralWidget and hBoxLayout1
        self.hBLayout1 = QtWidgets.QHBoxLayout(Dialog)
        self.hBLayout1.setObjectName("hBoxLayout1")

        # hBoxLayout1 --> hSpacer1 -- vBoxLayout1 -- hSpacer2
        self.hSpacer1 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer1)

        self.vBLayout1 = QtWidgets.QVBoxLayout()
        self.vBLayout1.setObjectName("vBLayout1")
        self.hBLayout1.addLayout(self.vBLayout1)

        self.hSpacer2 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout1.addItem(self.hSpacer2)

        # vBoxLayout1 --> vSpacer 1 -- QScrollArea -- vSpacer2
        self.vSpacer1 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer1)

        self.summaryScroll = QtWidgets.QScrollArea()
        self.summaryScroll.setObjectName("summaryScroll")
        self.summaryScroll.horizontalScrollBar().setEnabled(False)
        self.summaryScroll.setFrameStyle(1)
        self.vBLayout1.addWidget(self.summaryScroll)

        widget = QtWidgets.QWidget()
        self.summaryScroll.setWidget(widget)
        self.summaryScroll.setWidgetResizable(True)
        self.summaryScroll.move(3, 3)
        self.scrollLayout = QtWidgets.QVBoxLayout(widget)

        self.vSpacer2 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.vBLayout1.addItem(self.vSpacer2)

        # scrollLayout (vBLayout2) --> vSpacer3 -- hBoxLayout2 -- vSpacer4 -- HBLayout3
        self.vSpacer3 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.scrollLayout.addSpacerItem(self.vSpacer3)

        self.hBLayout2 = QtWidgets.QHBoxLayout()
        self.hBLayout2.setObjectName("hBlayout2")
        self.scrollLayout.addLayout(self.hBLayout2)

        self.vSpacer4 = QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.scrollLayout.addSpacerItem(self.vSpacer4)

        self.hBLayout3 = QtWidgets.QHBoxLayout()
        self.hBLayout3.setObjectName("hbLayout3")
        self.scrollLayout.addLayout(self.hBLayout3)

        # hBoxLayout2 --> FrameAsset -- FrameLiability
        self.hSpacer3 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout2.addSpacerItem(self.hSpacer3)

        self.frameAsset = QtWidgets.QFrame()
        self.frameAsset.setObjectName("FrameAsset")
        self.frameAsset.setFrameShape(QtWidgets.QFrame.Panel)
        self.frameAsset.setLineWidth(1)
        self.hBLayout2.addWidget(self.frameAsset)

        self.hSpacer4 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout2.addSpacerItem(self.hSpacer4)

        self.frameLiability = QtWidgets.QFrame()
        self.frameLiability.setObjectName("FrameLiability")
        self.frameLiability.setFrameShape(QtWidgets.QFrame.Panel)
        self.frameLiability.setLineWidth(1)
        self.hBLayout2.addWidget(self.frameLiability)

        self.hSpacer5 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout2.addSpacerItem(self.hSpacer5)

        # FrameAsset --> vBoxLayout3
        self.vBLayout3 = QtWidgets.QVBoxLayout(self.frameAsset)
        self.vBLayout3.setObjectName("vBLayout3")

        # vBoxLayout3 --> lAsset -- frameAGraph
        self.lAsset = QtWidgets.QLabel()
        self.lAsset.setObjectName("lAsset")
        self.lAsset.setText("Asset Distribution")
        self.lAsset.setFont(header_font)
        self.lAsset.setAlignment(QtCore.Qt.AlignHCenter)
        self.lAsset.setSizePolicy(sizePolicy)
        self.vBLayout3.addWidget(self.lAsset)

        self.frameAGraph = QtWidgets.QFrame()
        self.frameAGraph.setObjectName("frameAGraph")
        self.frameAGraph.setFrameShape(QtWidgets.QFrame.Panel)
        self.frameAGraph.setLineWidth(3)
        self.vBLayout3.addWidget(self.frameAGraph)

        # FrameLiability --> vBoxLayout4
        self.vBLayout4 = QtWidgets.QVBoxLayout(self.frameLiability)
        self.vBLayout4.setObjectName("vBLayout4")

        # vBoxLayout4 --> lLiability -- frameLGraph
        self.lLiability = QtWidgets.QLabel()
        self.lLiability.setObjectName("lLiability")
        self.lLiability.setText("Liability Distribution")
        self.lLiability.setFont(header_font)
        self.lLiability.setAlignment(QtCore.Qt.AlignHCenter)
        self.lLiability.setSizePolicy(sizePolicy)
        self.vBLayout4.addWidget(self.lLiability)

        self.frameAGraph = QtWidgets.QFrame()
        self.frameAGraph.setObjectName("frameALiability")
        self.frameAGraph.setFrameShape(QtWidgets.QFrame.Panel)
        self.frameAGraph.setLineWidth(3)
        self.vBLayout3.addWidget(self.frameAGraph)

        # hBLayout3 --> hspacer6 -- FrameSummary -- hspacer7
        self.hSpacer6 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout3.addSpacerItem(self.hSpacer6)

        self.frameSummary = QtWidgets.QFrame()
        self.frameSummary.setObjectName("frameSummary")
        self.frameSummary.setFrameShape(QtWidgets.QFrame.Panel)
        self.frameSummary.setLineWidth(1)
        self.hBLayout3.addWidget(self.frameSummary)

        self.hSpacer7 = QtWidgets.QSpacerItem(25, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.hBLayout3.addSpacerItem(self.hSpacer7)

        # vBoxLayout5 --> FrameSummary
        self.vBLayout5 = QtWidgets.QVBoxLayout(self.frameSummary)
        self.vBLayout5.setObjectName("vBLayout5")

        # self.debugmessage = QtWidgets.QLabel()
        # self.debugmessage.setObjectName("DebugLabel")
        # self.debugmessage.setWordWrap(True)
        # self.debugmessage.move(5, 5)
        # self.debugmessage.setSizePolicy(sizePolicy)
        # debugText = "This is the Scroll test message the goes on and on. " * 1000
        # self.debugmessage.setText(debugText)
        # self.vBLayout5.addWidget(self.debugmessage)

        # vBoxLayout5 --> will be generated by Backend.


if __name__ == "__main__":
    print("error")
