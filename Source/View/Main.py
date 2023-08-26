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
    member_join_signal = pyqtSignal(str)

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
        self.error_box = Error()
        self.client = clientapp
        self.client.set_widget(self)
        self.telebot = TelegramBot(self.lbl_imgview)
        # 에러 메시지 다이얼로그

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
        self.mypage_btn.clicked.connect(lambda: self.home_page.setCurrentIndex(2))

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.login_check_signal.connect(self.login_check_situation)

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
            self.error_box.error_text(1)
            self.error_box.exec_()

    def member_id_check(self):
        """회원가입 아이디 중복 여부 확인 함수"""
        pass

    def go_main_page(self):
        """메인 페이지 이동 함수"""
        self.stackedWidget.setCurrentIndex(2)
        self.home_page.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()
