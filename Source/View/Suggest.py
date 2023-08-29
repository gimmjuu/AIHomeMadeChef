from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class Suggest(QWidget):
    def __init__(self, recipe_name, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Suggest_Item.ui', self)
        self.label_2.setText(f"{recipe_name}")
