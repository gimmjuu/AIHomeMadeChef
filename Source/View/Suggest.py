from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class Suggest(QWidget):
    def __init__(self, recipe_name, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Suggest_Item.ui', self)
        self.label_2.hide()

        if len(recipe_name) <= 6:
            self.label_2.setText(recipe_name)
        elif 6 < len(recipe_name) <= 8:
            self.label_2.setText(f"{recipe_name[:6]}\n{recipe_name[6:]}")
        else:
            self.label_2.setText(f"{recipe_name[:7]}\n{recipe_name[7:]}")

    def enterEvent(self, event):
        """마수스가 위젯 위에 올라올 때 라벨 보이기"""
        self.label_2.show()

    def leaveEvent(self, event):
        """마우스가 위젯 위에서 떠났을때 라벨 숨기기"""
        self.label_2.hide()


