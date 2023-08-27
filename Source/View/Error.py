import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class Error(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/ErrorPage.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.btn_lbl_event()
        self.move(813, 412)

    def error_text(self, num):
        """에러 메시지 텍스트 출력"""
        if num == 0:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디 또는 패스워드 입력해주세요")
        if num == 1:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디 또는 패스워드가 일치하지 않습니다.")
        if num == 2:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디를 입력해주세요.")
        if num == 3:
            self.label_2.setPixmap(QPixmap("../../Images/clear.png"))
            self.label_3.setText("사용가능한 아이디입니다.")
        if num == 4:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("중복된 아이디입니다.")
        if num == 5:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디 중복 여부를 확인해주세요.")
        if num == 6:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("패스워드를 8~16자로 입력해주세요.")
        if num == 7:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("패스워드가 일치하지 않습니다.")
        if num == 8:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("닉네임이 너무 길거나 짧습니다.")
        if num == 9:
            self.label_2.setPixmap(QPixmap("../../Images/clear.png"))
            self.label_3.setText("회원가입이 완료되었습니다.")
        if num == 10:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("패스워드에 영문자,숫자,특수기호")
            self.label_5.setText("각 1개 이상 입력해주세요.")

    def btn_lbl_event(self):
        """버튼, 라벨 클릭 이벤트 함수"""
        self.pushButton.clicked.connect(self.close_event)
        self.label.mousePressEvent = self.close_event

    def close_event(self, e):
        """에러 다이얼로그 종료 함수"""
        self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Error()
    myWindow.show()
    app.exec_()