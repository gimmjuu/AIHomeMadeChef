from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.uic import loadUi


class SplashScreen(QWidget):
    __PATH__ = r"../../Images/spinner.gif"
    # __PATH__ = r"../../Images/spinner_multi.gif"
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance__, cls):
            cls.__instance__ = QWidget.__new__(cls)
        return cls.__instance__

    def __init__(self):
        super().__init__()
        loadUi('../../UI/SplashScreen.ui', self)
        self.set_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.center()

        self.movie = QMovie(self.__PATH__)
        self.splash_label.setMovie(self.movie)
        self.movie.start()
        print("movie.start")
        # self.hide()


class SplashThread(QThread):
    finished_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.finished_signal.connect()
        self.screen = SplashScreen()
        self.screen.show()

    def run(self):
        print("SplashScreen show")


if __name__ == '__main__':
    pass
