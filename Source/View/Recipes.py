from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class Recipes(QWidget):
    def __init__(self, recipe_name, recipe_type, parent=None):
        super().__init__(parent)
        loadUi('../../UI/Recipe_Item.ui', self)
        self.label_2.setText(f'{recipe_name}')
        if recipe_type == '밥':
            self.label_3.setPixmap(QPixmap('../../Images/rice.png'))
        if recipe_type == '떡/한과':
            self.label_3.setPixmap(QPixmap('../../Images/dduk.png'))
        if recipe_type == '만두/면류':
            self.label_3.setPixmap(QPixmap('../../Images/noodle.png'))
        if recipe_type == '볶음':
            self.label_3.setPixmap(QPixmap('../../Images/bokum.png.png'))
        if recipe_type == '국':
            self.label_3.setPixmap(QPixmap('../../Images/guk.png'))
        if recipe_type == '나물/생채/샐러드':
            self.label_3.setPixmap(QPixmap('../../Images/salad.png'))
        if recipe_type == '구이':
            self.label_3.setPixmap(QPixmap('../../Images/gui.png'))
        if recipe_type == '조림':
            self.label_3.setPixmap(QPixmap('../../Images/jorim.png'))
        if recipe_type == '찜':
            self.label_3.setPixmap(QPixmap('../../Images/jjim.png'))
        if recipe_type == '튀김/커틀릿':
            self.label_3.setPixmap(QPixmap('../../Images/tui.png'))
        if recipe_type == '찌개/전골/스튜':
            self.label_3.setPixmap(QPixmap('../../Images/jjigae.png'))
        if recipe_type == '도시락/간식':
            self.label_3.setPixmap(QPixmap('../../Images/dosirak.png'))
        if recipe_type == '부침':
            self.label_3.setPixmap(QPixmap('../../Images/buchim.png'))
        if recipe_type == '양식':
            self.label_3.setPixmap(QPixmap('../../Images/steak.png'))
        if recipe_type == '음료':
            self.label_3.setPixmap(QPixmap('../../Images/cola.png'))
        if recipe_type == '빵/과자':
            self.label_3.setPixmap(QPixmap('../../Images/bread.png'))
        if recipe_type == '양념장':
            self.label_3.setPixmap(QPixmap('../../Images/sourse.png'))
        if recipe_type == '피자':
            self.label_3.setPixmap(QPixmap('../../Images/pizza.png'))
        if recipe_type == '그라탕/리조또':
            self.label_3.setPixmap(QPixmap('../../Images/grt.png.jpg'))
        if recipe_type == '햄버거':
            self.label_3.setPixmap(QPixmap('../../Images/hamburger.png'))
        if recipe_type == '볶음':
            self.label_3.setPixmap(QPixmap('../../Images/bokum.png'))
        if recipe_type == '밑반찬/김치':
            self.label_3.setPixmap(QPixmap('../../Images/banchan.png'))

