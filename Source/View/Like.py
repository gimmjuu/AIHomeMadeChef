from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class Like(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Like_Item.ui', self)
