import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class Cooking(QWidget):
    def __init__(self, num, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Cooking_Item.ui', self)
        self.label.setText(str(num+1))
        self.textEdit.setText("ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ")


