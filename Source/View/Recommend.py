from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from Source.Common.Common import set_pixmap_from_url


class Recommend(QWidget):
    def __init__(self, recipe_name, recipe_img, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Recommend_Item.ui', self)
        self.label_2.setText(f"{recipe_name}")
        set_pixmap_from_url(self.label, recipe_img)