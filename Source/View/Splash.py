import sys

from PyQt5.QtGui import QPixmap, QMovie, QPainter
from PyQt5.QtWidgets import QSplashScreen, QApplication


class SplashScreen(QSplashScreen):
    __PATH__ = r"../../Images/spinner.gif"
    # __PATH__ = r"../Images/spinner_multi.gif"

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: none; border: none;")
        # gif 추가
        self.movie = QMovie(self.__PATH__)
        self.movie.jumpToFrame(0)
        pixmap = QPixmap(self.movie.frameRect().size())
        # 위젯에 QMovie 삽입
        self.setPixmap(pixmap)
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, e):
        self.movie.start()

    def hideEvent(self, e):
        self.movie.stop()

    def paintEvent(self, e):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # splash = SplashScreen()
    # splash.show()
    # app.processEvents()
    #
    # window = QMainWindow()
    # QTimer.singleShot(3500, lambda: splash.finish(window))
    # window.show()
    #
    # app.exec()
