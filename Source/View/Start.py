import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontDatabase

from Source.Client.Client import ClientApp
from Source.View.Main import Main


class Start(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/StartPage.ui', self)
        fontDB = QFontDatabase()
        fontDB.addApplicationFont("../../Font/GMARKETSANSTTFBOLD.ttf")
        fontDB.addApplicationFont("../../Font/KIMJUNGCHULSCRIPT-REGULAR.ttf")
        fontDB.addApplicationFont("../../Font/TMONEYROUNDWINDEXTRABOLD.ttf")
        fontDB.addApplicationFont("../../Font/THE_Nakseo.ttf")
        self.window_option()
        self.timer_event()

    def window_option(self):
        """프로그램 실행시 옵션 설정 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def timer_event(self):
        """큐 타이머 이벤트 함수"""
        self.timer = QTimer(self)
        self.timer.start(1000)  # 1초
        self.timer.timeout.connect(self.go_to_main)

    def go_to_main(self):
        """메인 페이지 이동 함수"""
        self.timer.stop()
        main_ = Main(client)
        self.close()
        main_.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ClientApp()
    myWindow = Start()
    myWindow.show()
    app.exec_()
