import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer

from Source.View.Main import Main


class Start(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/StartPage.ui', self)
        self.window_option()
        self.timer_event()

    def window_option(self):
        """프로그램 실행시 옵션 설정 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def timer_event(self):
        """큐 타이머 이벤트 함수"""
        self.timer = QTimer(self)
        self.timer.start(1500)  # 1.5초
        self.timer.timeout.connect(self.go_to_main)

    def go_to_main(self):
        """메인 페이지 이동 함수"""
        self.timer.stop()
        main_ = Main()
        self.close()
        main_.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Start()
    myWindow.show()
    app.exec_()
