"""
날짜 : 23/08/25
작성 : 주혜인
내용 : 메인 위젯을 생성 후 실행하는 메인 실행파일입니다.
"""
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    fontDB = QFontDatabase()
    fontDB.addApplicationFont("../../Font/GMARKETSANSTTFBOLD.ttf")
    fontDB.addApplicationFont("../../Font/KIMJUNGCHULSCRIPT-REGULAR.ttf")
    fontDB.addApplicationFont("../../Font/TMONEYROUNDWINDEXTRABOLD.ttf")

    app.exec()


if __name__ == '__main__':
    main()
