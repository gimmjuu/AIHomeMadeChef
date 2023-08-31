import sys
import time
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie, QPainter
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDesktopWidget


class Splash(QWidget):
    __PATH__ = r"../../Images/spinner.gif"
    # __PATH__ = r"../../Images/spinner_multi.gif"
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance__, cls):
            cls.__instance__ = QWidget.__new__(cls)
        return cls.__instance__

    def __init__(self, t_parent=None):
        super().__init__()

        if t_parent:
            self.setParent(t_parent)

        self.set_ui()
        self.set_movie()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400, 400)
        # self.setStyleSheet("background: none; border: none;")
        self.center()
        self.gif_viewer = QLabel(self)
        # self.gif_viewer.setGeometry(0, 0, 400, 400)

    def set_movie(self):
        # --- gif 추가
        self.movie = QMovie(self.__PATH__)
        self.movie.jumpToFrame(0)
        pixmap = QPixmap(self.movie.frameRect().size())
        # --- 위젯에 QMovie 삽입
        self.gif_viewer.setPixmap(pixmap)
        self.movie.frameChanged.connect(self.repaint)

    def paintEvent(self, e):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def showEvent(self, e):
        self.movie.start()

    def closeEvent(self, e):
        self.movie.stop()


def start_splash():
    """로딩 화면 출력용 스레드 함수"""
    sp = Splash()
    sp.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = Splash()
    sp.show()
    # app.processEvents()
    # sp.close()
    app.exec()

