from PyQt5.QtWidgets import QWidget, QLayout, QSpacerItem, QSizePolicy, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSignal

from Source.Common.JSONConverter import *
from Source.View.Cooking import Cooking
from Source.View.Ingredient import Ingredient
from Source.View.Like import Likes
from Source.View.Recipe import Recipes
from Source.View.Recommend import Recommend
from Source.View.Telegram import TelegramBot
from Source.View.Error import Error
from threading import Thread
import random


class Main(QWidget):
    login_check_signal = pyqtSignal(bool)
    member_id_check_signal = pyqtSignal(bool)
    member_join_signal = pyqtSignal(bool)
    my_page_data_signal = pyqtSignal(str)
    recipe_all_signal = pyqtSignal(str)
    recipe_id_signal = pyqtSignal(str)
    recipe_like_signal = pyqtSignal(str)
    recipe_hate_signal = pyqtSignal(str)
    like_check_signal = pyqtSignal(bool)
    recipe_jjim_signal = pyqtSignal(str)
    recipe_random_signal = pyqtSignal(str)

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
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

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
        self.picture_btn.clicked.connect(lambda: self.home_page.setCurrentIndex(0))
        self.search_btn.clicked.connect(self.search_recipe)
        self.mypage_btn.clicked.connect(self.my_page_request)
        self.request_btn.clicked.connect(self.member_join_request)
        self.home_btn.clicked.connect(self.home_menu)
        self.name_search_btn.clicked.connect(self.name_search_page)
        self.like_btn.clicked.connect(self.like_true_situation)
        self.like_btn_2.clicked.connect(self.like_false_situation)
        self.choice_btn.clicked.connect(self.jjim_situation)
        self.search_btn_2.clicked.connect(self.search_recipe_by_name)

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.login_check_signal.connect(self.login_check_situation)
        self.member_id_check_signal.connect(self.member_id_check_situation)
        self.member_join_signal.connect(self.member_join_clear)
        self.my_page_data_signal.connect(self.my_page_show)
        self.recipe_all_signal.connect(self.name_search_recipe_show)
        self.recipe_id_signal.connect(self.search_recipe)
        self.like_check_signal.connect(self.recipe_like_check)
        self.recipe_jjim_signal.connect(self.recipe_jjim_show)
        self.recipe_random_signal.connect(self.go_main_page)

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
            self.random_recipe_show()

        else:
            self.id_line.clear()
            self.pw_line.clear()
            self.error_box.error_text(1)
            self.error_box.exec_()

    # ================================== 홈 화면 ===============================
    def home_menu(self):
        """홈 버튼 클릭시 이벤트 함수"""
        self.home_page.setCurrentIndex(4)

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

    def random_recipe_show(self):
        """로그인 페이지에서 메인 페이지 이동하기 전 홈 화면 추천 레시피 출력 서버에 보내는 함수"""
        user_id = self.client.user_id
        self.client.send_recipe_random_access(user_id)

    def go_main_page(self, random_):
        """메인페이지 출력 / 추천 레시피 랜덤으로 출력해주는 함수"""
        random_recipe = self.decoder.binary_to_obj(random_)
        random.shuffle(random_recipe)
        self.clear_layout(self.horizontalLayout)
        spacer = QSpacerItem(20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacer)
        name_list = list()
        id_list = list()
        for recipe_ in random_recipe[:5]:
            recipe_id = recipe_.recipe_id
            id_list.append(recipe_id)
            recipe_name = recipe_.recipe_name
            name_list.append(recipe_name)
        for i in range(len(name_list)):
            recommend = Recommend(name_list[i])
            self.horizontalLayout.insertWidget(len(self.horizontalLayout) - 1, recommend)
            recommend.mousePressEvent = lambda x=None, y=id_list[i]: self.recipe_page_clicked(y)
        self.stackedWidget.setCurrentIndex(2)
        self.home_page.setCurrentIndex(4)

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

    # =============================== 이름 검색 페이지 =================================
    def name_search_page(self):
        """이름 검색 버튼 클릭시 서버로 데이터 전송"""
        recipe_ = 123
        self.client.send_recipe_all_access(recipe_)

    def name_search_recipe_show(self, recipes_):
        """이름 검색 화면 레시피 출력 함수"""
        self.clear_layout(self.verticalLayout_4)
        spacer = QSpacerItem(20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacer)
        self.home_page.setCurrentIndex(5)
        recipe_datas = self.decoder.binary_to_obj(recipes_)
        for i in recipe_datas:
            recipe_id = i.recipe_id
            recipe_name = i.recipe_name
            recipe_type = i.recipe_type
            recipe = Recipes(recipe_name, recipe_type)
            self.verticalLayout_4.insertWidget(len(self.verticalLayout_4) - 1, recipe)
            recipe.mousePressEvent = lambda x=None, y=recipe_id: self.recipe_page_clicked(y)

    # ================================ 마이 페이지 =====================================
    def my_page_request(self):
        """마이 페이지 데이터 서버에 요청 함수"""
        user_id = self.client.user_id
        self.client.send_my_page_data_access(user_id)

    def my_page_show(self, user_data):
        """마이 페이지 이동 함수"""
        user_ = self.decoder.binary_to_obj(user_data)
        user_id = user_.user_id
        user_name = user_.user_name
        user_taste = user_.user_taste
        self.home_page.setCurrentIndex(2)
        self.lbl_user_name.setText(user_name)
        self.lbl_user_id.setText(user_id)

    # ============================================ 레시피  ===========================================
    def recipe_page_clicked(self, recipe_id):
        """서버로 레시피 아이디 전송"""
        self.client.send_recipe_id_access(recipe_id)

    def search_recipe(self, recipe_data):
        """레시피 검색시 출력 함수"""
        recipe_datas = self.decoder.binary_to_obj(recipe_data)
        recipe_id = recipe_datas.recipe_id
        recipe_name = recipe_datas.recipe_name
        recipe_stuff = recipe_datas.recipe_stuff
        recipe_step = recipe_datas.recipe_step
        # 재료 출력
        self.lbl_recipe_name.setText(f'<{recipe_name}> 레시피')
        self.lbl_recipe_name: QLabel
        self.like_btn.setObjectName(f"{recipe_id}")
        self.like_btn_2.setObjectName(f"{recipe_id}")
        self.clear_layout(self.verticalLayout)
        ingredient = Ingredient(recipe_stuff)
        self.verticalLayout.addWidget(ingredient)
        # --- 레이아웃 비우기
        self.clear_layout(self.verticalLayout_3)
        spacer = QSpacerItem(20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer)
        # 조리법 출력
        recipe_step = recipe_step.replace("/ ", "")
        step_split = recipe_step.split("|")
        for i, v in enumerate(step_split):
            cooking = Cooking(i, v)
            self.verticalLayout_3.insertWidget(len(self.verticalLayout_3) - 1, cooking)
        user_id = self.client.user_id
        self.client.send_like_check(user_id, recipe_id)

    def clear_layout(self, layout: QLayout):
        """레이아웃 안의 모든 객체를 지우는 함수"""
        if layout is None or not layout.count():
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())

    def search_recipe_by_name(self):
        """레시피 페이지 이름 검색버특 클릭시 이벤트 함수"""
        search_name = self.lineEdit.text()
        recipe_list = self.scrollAreaWidgetContents_5.findChildren(Recipes)

        for recipe_ in recipe_list:
            if search_name in recipe_.label_2.text():
                recipe_.setVisible(True)
            else:
                recipe_.setVisible(False)

   # ======================================== 찜하기 =========================================
    def recipe_like_check(self, like_):
        """찜버튼 클릭 여부 확인"""
        if like_:
            self.like_btn.hide()    # 찜하기
            self.like_btn_2.show()  # 찜한
        else:
            self.like_btn.show()
            self.like_btn_2.hide()
        self.home_page.setCurrentIndex(1)

    def like_true_situation(self):
        """찜하기 버튼 클릭시 서버에 데이터 요청 함수"""
        user_id = self.client.user_id
        target_id = int(self.like_btn.objectName())
        self.client.send_like_access(user_id, target_id)
        self.like_btn.hide()
        self.like_btn_2.show()

    def like_false_situation(self):
        """찜한 버튼 클릭시 서버에 데이터 요청 함수"""
        user_id = self.client.user_id
        target_id = int(self.like_btn_2.objectName())
        self.client.send_hate_access(user_id, target_id)
        self.like_btn_2.hide()
        self.like_btn.show()

    def jjim_situation(self):
        """찜 페이지 버튼 클릭시 서버에 데이터 요청 함수"""
        user_id = self.client.user_id
        self.client.send_recipe_jjim_access(user_id)

    def recipe_jjim_show(self, recipe_data):
        """레시피 찜목록 출력 이벤트 함수"""
        user_name = self.client.user_name
        self.label_23.setText(f"{user_name} 님의 찜목록")
        self.clear_layout(self.verticalLayout_5)
        spacer = QSpacerItem(20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacer)
        recipes = self.decoder.binary_to_obj(recipe_data)

        for rcp in recipes:
            recipe_id = rcp.recipe_id
            recipe_name = rcp.recipe_name
            like_page = Likes(recipe_name)
            self.verticalLayout_5.insertWidget(len(self.verticalLayout_5) - 1, like_page)
            like_page.mousePressEvent = lambda x=None, y=recipe_id: self.recipe_page_clicked(y)
            like_page.jjim_btn.clicked.connect(lambda x=None, y=recipe_id: self.jjim_del(y))
        self.home_page.setCurrentIndex(3)

    def jjim_del(self, recipe_id):
        """찜페이지에서 하트버튼 클릭시 찜목록에서 삭제"""
        user_id = self.client.user_id
        self.client.send_hate_access(user_id, recipe_id)
        self.jjim_situation()





