import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class Error(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/ErrorPage.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.btn_lbl_event()

    def error_text(self, num):
        """에러 메시지 텍스트 출력"""
        if num == 0:
            self.label_3.setText("아이디 또는 비밀번호를 입력해주세요")
        if num == 1:
            self.label_3.setText("아이디 또는 비밀번호가 일치하지 않습니다.")

    def btn_lbl_event(self):
        """버튼, 라벨 클릭 이벤트 함수"""
        self.pushButton.clicked.connect(self.close_event)
        self.label.mousePressEvent = self.close_event

    def close_event(self):
        """에러 다이얼로그 종료 함수"""
        self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Error()
    myWindow.show()
    app.exec_()