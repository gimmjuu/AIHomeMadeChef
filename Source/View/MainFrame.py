"""
날짜 : 23/08/25
작성 : 주혜인
내용 : 메인위젯(MainFrame) 관련 Class 작성 파일입니다.
"""
from PyQt5.QtWidgets import QWidget

from Source.Common.MyFont import MyFont
from Source.View.UI_MainFrame import Ui_MainFrame


class MainFrame(QWidget, Ui_MainFrame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # --- 초기화
        self.set_myfont()
        self.set_ui()
        self.set_val()
        self.set_method()
        self.set_signal()

    # === 폰트 설정
    def set_myfont(self):
        button_font = MyFont.button(11)

        self.lbl_maintitle.setFont(MyFont.title(36))
        self.btn_dupli_check.setFont(button_font)
        self.btn_mmb_reject.setFont(button_font)
        self.btn_mmb_accept.setFont(button_font)

    # === 위젯 설정 초기화
    def set_ui(self):
        # --- 최초 로그인 화면 구성
        self.btn_dupli_check.setVisible(False)
        self.lbl_id_info.setVisible(False)
        self.lbl_pwd_info.setVisible(False)
        self.lbl_nick_info.setVisible(False)
        self.stack_main.setCurrentIndex(0)

    # === 변수 선언
    def set_val(self):
        # 로그인 화면 타입 확인
        self.mmb_check = True
        # 로그인 사용자 아이디
        self.current_user = -1

    # === 함수 연결 설정
    def set_method(self):
        # --- 로그인 관련
        self.btn_mmb_reject.clicked.connect(self.close)
        self.btn_mmb_accept.clicked.connect(self.check_mmb_situation)

        # --- 상단 메뉴바 관련
        self.btn_close.clicked.connect(self.close)
        self.btn_prev.clicked.connect(lambda: self.stack_contents.setCurrentWidget(self.page_search))
        self.btn_usermenu.clicked.connect(self.load_userinfo)
        # self.btn_preferlist.clicked.connect()

    # === 시그널 연결 설정 -> pyqtsignal 여기에 작성!
    def set_signal(self):
        pass

    # ============================== 로그인 화면 ==============================
    def check_mmb_situation(self):
        if self.mmb_check:
            self.btn_preferlist.setVisible(False)
            self.stack_main.setCurrentIndex(1)

    # ============================== 상단 메뉴 버튼 ==============================

    def load_userinfo(self):
        self.btn_close.setVisible(False)
        self.btn_preferlist.setVisible(True)
        self.stack_contents.setCurrentWidget(self.page_userinfo)
