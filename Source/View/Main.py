import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSignal

from Source.View.Telegram import TelegramBot
from Source.View.Error import Error
from threading import Thread


class Main(QWidget):
    login_check_signal = pyqtSignal(bool)
    member_id_check_signal = pyqtSignal(bool)
    member_join_signal = pyqtSignal(bool)
    my_page_data_signal = pyqtSignal(str)

    def __init__(self, clientapp):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.window_option(clientapp)
        self.btn_event()
        self.lbl_event()
        self.signal_event()

    def window_option(self, clientapp):
        """프로그램 실행시 옵션 설정 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.stackedWidget.setCurrentIndex(0)

        # 변수 설정
        self.client = clientapp
        self.client.set_widget(self)
        self.telebot = TelegramBot(self.lbl_imgview)
        self.check = -1
        self.pw_check = -1

        # 에러 메시지 다이얼로그
        self.error_box = Error()

        # 텔레그램 쓰레드
        self.img_thread = Thread(target=self.telebot.start_polling, daemon=True)
        self.img_thread.start()

    def lbl_event(self):
        """라벨 클릭 이벤트 함수"""
        self.label_11.mousePressEvent = self.close_event

    def close_event(self, e):
        """프로그램 종료 이벤트 함수"""
        self.close()

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        # 로그인 화면 버튼
        self.close_btn.clicked.connect(self.close_event)
        self.join_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.login_btn.clicked.connect(self.login_check)
        # 회원가입 화면 버튼
        self.back_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.id_check.clicked.connect(self.member_id_check)
        # 메인화면 버튼
        self.home_btn.clicked.connect(lambda: self.home_page.setCurrentIndex(0))
        self.search_btn.clicked.connect(lambda: self.home_page.setCurrentIndex(1))
        self.choice_btn.clicked.connect(lambda: self.home_page.setCurrentIndex(3))
        self.mypage_btn.clicked.connect(self.my_page_request)
        self.request_btn.clicked.connect(self.member_join_request)

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.login_check_signal.connect(self.login_check_situation)
        self.member_id_check_signal.connect(self.member_id_check_situation)
        self.member_join_signal.connect(self.member_join_clear)
        self.my_page_data_signal.connect(self.my_page_show)

    # ============================= 로그인 ==================================
    def login_check(self):
        """로그인 데이터 클라이언트에 전송 함수"""
        user_id = self.id_line.text()
        user_pwd = self.pw_line.text()
        if len(user_id) == 0 or len(user_pwd) == 0:
            self.error_box.error_text(0)
            self.error_box.exec_()
        else:
            self.client.send_login_check_access(user_id, user_pwd)

    def login_check_situation(self, login_):
        """로그인 성공 여부 시그널 받는 함수"""
        if login_:
            self.go_main_page()
        else:
            self.id_line.clear()
            self.pw_line.clear()
            self.error_box.error_text(1)
            self.error_box.exec_()

    # ================================= 회원가입 ================================
    def member_id_check(self):
        """회원가입 아이디 중복 여부 확인 함수"""
        user_id = self.join_id.text()
        if len(user_id) == 0:
            self.error_box.error_text(2)
            self.error_box.exec_()
        else:
            self.client.send_member_id_check_access(user_id)

    def member_id_check_situation(self, member_):
        """서버에서 회원가입 아이디 중복 결과 받는 함수"""
        check_id = member_
        if check_id:
            self.check = 1
            self.error_box.error_text(3)
            self.error_box.exec_()

        else:
            self.join_id.clear()
            self.error_box.error_text(4)
            self.error_box.exec_()

    def member_join_request(self):
        """서버에 회원가입 요청 보내는 함수"""
        join_id = self.join_id.text()
        join_pwd = self.join_pw.text()
        check_pwd = self.check_pw.text()
        user_name = self.join_name.text()

        if self.check != 1:
            self.error_box.error_text(5)
            self.error_box.exec_()
            return

        if len(join_pwd) < 8 or len(join_pwd) > 16:
            self.join_pw.clear()
            self.check_pw.clear()
            self.error_box.error_text(6)
            self.error_box.exec_()
            return

        if join_pwd != check_pwd:
            self.error_box.error_text(7)
            self.error_box.exec_()
            return

        # 비밀번호에 영문자, 숫자, 특수기호 각각 1개 이상 사용하는지 확인
        pw_valid_result = self.is_valid_password(join_pwd)

        if pw_valid_result == -1:
            self.error_box.error_text(10)
            self.error_box.exec_()
            return

        if len(user_name) > 20 or len(user_name) == 0:
            self.error_box.error_text(8)
            self.error_box.exec_()
            return

        self.client.send_member_join_access(join_id, join_pwd, user_name)

    def member_join_clear(self, join_):
        """서버로부터 회원가입 완료 시그널 받는 함수"""
        if join_:
            self.error_box.error_text(9)
            self.error_box.exec_()
            self.stackedWidget.setCurrentIndex(0)

    def go_main_page(self):
        """로그인 페이지에서 메인 페이지 이동 함수"""
        self.stackedWidget.setCurrentIndex(2)
        self.home_page.setCurrentIndex(0)

    # ======================== 마이 페이지 =====================================
    def my_page_request(self):
        """마이 페이지 데이터 서버에 요청 함수"""
        user_id = self.client.user_id
        self.client.send_my_page_data_access(user_id)

    def my_page_show(self, user_data):
        """마이 페이지 이동 함수"""
        print(user_data)
        self.home_page.setCurrentIndex(2)
        # self.lbl_user_name.setText(self.client.user_name)
        # self.lbl_user_id.setText(self.client.user_id)

    def is_valid_password(self, password):
        """비밀번호 영문자, 숫자, 특수기호 각각 1개 이상 사용하는지 확인하는 함수"""
        has_lowercase = any(c.islower() for c in password)
        has_uppercase = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c for c in password if c in "!@#$%^&*()_+[]{}|;:,.<>?")

        # 모든 조건을 만족하는지 검사
        if (has_lowercase or has_uppercase) and has_digit and has_special:
            return 1
        else:
            return -1



