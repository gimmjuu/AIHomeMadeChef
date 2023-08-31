from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from Source.Common.Common import set_pixmap_from_url


class Prefer(QWidget):
    def __init__(self, recipe_name, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Prefer_Item.ui', self)
        self.label_2.setText(f"{recipe_name}")
