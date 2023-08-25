"""
날짜 : 23/08/25
작성 : 주혜인
내용 : 시스템 폰트 이외의 폰트 설정을 위한 MyFont Class 파일입니다.
"""
from PyQt5.QtGui import QFont


class MyFont:
    @staticmethod
    def title(t_size: int = 48):
        """
        Font for title text
        :param t_size: font-size
        :return: 나눔스퀘어라운드 ExtraBold
        """
        font = QFont()
        font.setPointSize(t_size)
        font.setFamily("나눔스퀘어라운드 ExtraBold")
        return font

    @staticmethod
    def button(t_size: int = 13):
        """
        Font for button text
        :param t_size: font-size
        :return: 나눔스퀘어라운드 ExtraBold
        """
        font = QFont()
        font.setPointSize(t_size)
        font.setFamily("나눔스퀘어라운드 ExtraBold")
        return font

    @staticmethod
    def text(t_size: int = 13, t_bold: bool = True):
        """
        Font for button text
        :param t_size: font-size
        :param t_bold: default = True
        :return: 나눔스퀘어라운드 Bold | Regular
        """
        font = QFont()
        font.setPointSize(t_size)

        if t_bold:
            font.setFamily("나눔스퀘어라운드 Bold")
        else:
            font.setFamily("나눔스퀘어라운드 Regular")

        return font
