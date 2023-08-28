from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class Recipes(QWidget):
    def __init__(self, recipe_name, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Recipe_Item.ui', self)
        self.label_2.setText(recipe_name)