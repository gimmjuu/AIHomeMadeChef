"""
작성자 : 주혜인
작성일 : 23/08/31
내용 : SplashScreen을 화면에 출력하기 위한 QWidget, QThread Class입니다.
"""
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal as QSignal
from PyQt5.QtGui import QMovie
from PyQt5.uic import loadUi


class SplashScreen(QWidget):
    __PATH__ = r"../../Images/spinner.gif"

    def __init__(self, ):
        super().__init__()
        loadUi('../../UI/SplashScreen.ui', self)
        # self.setParent(t_parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.center()

        # self.movie = QMovie(self.__PATH__)
        self.movie = QMovie(r"../../Images/spinner.gif")
        print(self.movie.frameCount())
        # self.movie = QMovie(r"../../Document/loading.gif")
        self.splash_label.setMovie(self.movie)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class SplashThread(QThread):
    finished_signal = QSignal()

    def __init__(self):
        super().__init__()
        self.screen = SplashScreen()
        self.screen.show()
        self.screen.movie.start()

    def run(self):
        while self.screen.isVisible():
            print(self.screen.movie.currentFrameNumber())
            self.screen.movie.jumpToNextFrame()
            self.screen.splash_label.update()
            # self.screen.update()

        self.finished_signal.emit()

    def close_screen(self):
        self.screen.close()


if __name__ == '__main__':
    pass
