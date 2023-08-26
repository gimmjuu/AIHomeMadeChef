import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class Main(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.window_option()
        self.btn_event()

    def window_option(self):
        """프로그램 실행시 옵션 설정 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.stackedWidget.setCurrentIndex(0)

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.close_btn.clicked.connect(lambda: self.close())
        self.join_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.back_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.id_check.clicked.connect(self.member_id_check)

    def member_id_check(self):
        """회원가입 아이디 중복 여부 확인 함수"""
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()
