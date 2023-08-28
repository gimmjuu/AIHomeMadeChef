import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class Ingredient(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Ingredient_Item.ui', self)
        self.textEdit.setText("하이,  하이,  하이")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Ingredient()
    myWindow.show()
    app.exec_()