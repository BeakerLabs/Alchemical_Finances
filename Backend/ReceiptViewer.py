"""
This script is the backend to Frontend.ReceiptUi.py

Future Concepts

"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QPixmap, QTransform
from Frontend.ReceiptUi import Ui_Receipt
# from Frontend.StyleSheets import UniversalStyleSheet


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
        self.receiptImage = QPixmap(pathway)
        self.receiptAdjustment = self.receiptImage.transformed(QTransform().rotate(self.degree).scale(self.scale, self.scale))
        self.ui.lRImage.setPixmap(self.receiptAdjustment)
        self.ui.pBRotateCC.clicked.connect(lambda: self.rotate_image(clockwise=False))
        self.ui.pBZoomIn.clicked.connect(lambda: self.zoom_image("Enlarge"))
        self.ui.pBZoomOut.clicked.connect(lambda: self.zoom_image("Shrink"))
        self.ui.pBRotateC.clicked.connect(lambda: self.rotate_image())

        self.ui.lRName.setText(image)
        # self.setStyleSheet(UniversalStyleSheet)
        self.setModal(True)
        self.show()

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
    print("error")