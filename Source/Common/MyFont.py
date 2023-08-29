"""
날짜 : 23/08/25
작성 : 주혜인
내용 : 시스템 폰트 이외의 커스텀 폰트 설정을 위한 MyFont Class 파일입니다.
"""
from PyQt5.QtGui import QFont


class MyFont:
    @staticmethod
    def tmoney_font(t_size: int):
        """
        Font 티머니 둥근바람
        :param t_size: font-size
        :return: 티머니 둥근바람 ExtraBold
        """
        font = QFont()
        font.setPointSize(t_size)
        font.setFamily("티머니 둥근바람 ExtraBold")
        return font

    @staticmethod
    def gmarket_font(t_size: int):
        """
        Font 지마켓산스
        :param t_size: font-size
        :return:
        """
        font = QFont()
        font.setPointSize(t_size)
        font.setFamily("G마켓 산스 TTF Bold")
        return font

    @staticmethod
    def retro_font(t_size: int):
        """
        Font 김정철
        :param t_size: font-size
        :return:
        """
        font = QFont()
        font.setPointSize(t_size)
        font.setFamily("Kim jung chul Script Regular")
        return font
