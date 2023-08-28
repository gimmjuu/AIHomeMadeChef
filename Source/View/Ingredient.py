from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class Ingredient(QWidget):
    def __init__(self, ingredient, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Ingredient_Item.ui', self)
        self.stuff = ingredient
        print(self.stuff, "재료 페이지")
        self.textEdit.setText(f"{self.stuff.replace('|', ',  ')}")

