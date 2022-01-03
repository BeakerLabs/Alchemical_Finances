"""
This script is the backend to Frontend.ReceiptUi.py

Future Concepts

"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import shutil
import sys

from pathlib import PurePath
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtGui import QPixmap, QTransform
from Frontend.ReceiptUi import Ui_Receipt
from StyleSheets.StandardCSS import standardAppearance


class Receipt(QDialog):
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, pathway, image):
        super().__init__()
        self.ui = Ui_Receipt()
        self.ui.setupUi(self)
        self.degree = 0
        self.scale = 0.50
        self.receiptPathway = pathway
        self.filename = image
        self.receiptImage = QPixmap(self.receiptPathway)
        self.receiptAdjustment = self.receiptImage.transformed(QTransform().rotate(self.degree).scale(self.scale, self.scale))
        self.ui.lRImage.setPixmap(self.receiptAdjustment)
        self.ui.pBDownload.clicked.connect(self.downloadReceipt)
        self.ui.pBRotateCC.clicked.connect(lambda: self.rotate_image(clockwise=False))
        self.ui.pBZoomIn.clicked.connect(lambda: self.zoom_image("Enlarge"))
        self.ui.pBZoomOut.clicked.connect(lambda: self.zoom_image("Shrink"))
        self.ui.pBRotateC.clicked.connect(lambda: self.rotate_image())

        self.ui.lRName.setText(image)
        self.setStyleSheet(standardAppearance)
        self.setModal(True)
        self.show()

    def downloadReceipt(self):
        copyNum = 0
        nameReady = False
        suffix = PurePath(self.filename).suffix
        noSuffix = self.filename[:-len(suffix)]

        while not nameReady:

            if copyNum == 0:
                newName = self.filename
            elif copyNum == 1:
                newName = f"{noSuffix} (Copy)" + suffix
            else:
                newName = f"{noSuffix} (Copy {copyNum})" + suffix

            destination = os.path.join(os.path.expanduser("~"), f"Downloads/{newName}")

            if os.path.isfile(destination):
                copyNum += 1
            else:
                nameReady = True

        try:
            shutil.copy(self.receiptPathway, destination)
            downloadMSG = f"{self.filename} \n\nHas been downloaded."
            self.input_error_msg(downloadMSG)
        except IOError:
            errorMSG = f"{self.filename} \n\nHas encountered an Error"
            self.input_error_msg(errorMSG)

    def input_error_msg(self, message):
        reply = QMessageBox.information(self, 'Input Error', message, QMessageBox.Ok, QMessageBox.NoButton)
        if reply == QMessageBox.Ok:
            pass
        else:
            pass

    def rotate_image(self, clockwise=True):

        if clockwise is True:
            self.degree += 90
        elif clockwise is False:
            self.degree -= 90

        modifiedImage = self.receiptImage.transformed(QTransform().rotate(self.degree).scale(self.scale, self.scale))
        self.ui.lRImage.setPixmap(modifiedImage)

        if self.degree > 270:
            self.degree = 0
        elif self.degree < 0:
            self.degree = 360

    def zoom_image(self, direction):
        if direction == "Enlarge":
            self.scale += 0.05
        elif direction == "Shrink":
            self.scale -= 0.05
        else:
            pass

        modifiedImage = self.receiptImage.transformed(QTransform().rotate(self.degree).scale(self.scale, self.scale))
        self.ui.lRImage.setPixmap(modifiedImage)

    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
