from PyQt5.QtWidgets import QWidget, QLayout, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QByteArray, QTimer
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.uic import loadUi
from tkinter import *
from tkinter import filedialog


from Source.Common.JSONConverter import *
from Source.View.Cooking import Cooking
from Source.View.Ingredient import Ingredient
from Source.View.Like import Likes
from Source.View.Recipes import Recipes
from Source.View.Recommend import Recommend
from Source.View.Suggest import Suggest
from Source.View.Telegram import TelegramBot
from Source.View.Error import Error
from threading import Thread
import random


class Main(QWidget):
    login_check_signal = pyqtSignal(bool)
    member_id_check_signal = pyqtSignal(bool)
    member_join_signal = pyqtSignal(bool)
    recommend_data_signal = pyqtSignal(str)
    recipe_all_signal = pyqtSignal(str)
    recipe_id_signal = pyqtSignal(str)
    recipe_like_signal = pyqtSignal(str)
    recipe_hate_signal = pyqtSignal(str)
    like_check_signal = pyqtSignal(bool)
    recipe_jjim_signal = pyqtSignal(str)
    recipe_random_signal = pyqtSignal(str)
    yolo_false_signal = pyqtSignal(bool)
    rd_recipe_id_signal = pyqtSignal(str)

    def __init__(self, clientapp):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.window_option(clientapp)
        self.btn_event()
        self.lbl_event()
        self.signal_event()

    def window_option(self, clientapp):
        """프로그램 실행시 옵션 설정 함수"""
        self.setWindowFlags(Qt.FramelessWindowHint)
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

        # gif 실행 코드
        self.movie = QMovie('../../Images/cafe.gif', QByteArray(), self)
        self.movie_2 = QMovie('../../Images/trip.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_2.setCacheMode(QMovie.CacheAll)
        self.label_33.setMovie(self.movie) # 샌드위치 gif
        self.label_35.setMovie(self.movie_2) # 요리 여행 gif
        self.movie.start()
        self.movie_2.start()

        # 광고 배너 qtimer
        self.timer = QTimer(self)
        self.timer.start(5000)  # 5초 반복
        self.timer.timeout.connect(self.timer_event)
        self.ad.setCurrentIndex(0)
        self.ad_count = 1

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
        self.picture_btn.clicked.connect(self.picture_page_show)
        self.search_btn.clicked.connect(self.classify_food_image)
        self.mypage_btn.clicked.connect(self.my_page_request)
        self.request_btn.clicked.connect(self.member_join_request)
        self.home_btn.clicked.connect(self.home_menu)
        self.name_search_btn.clicked.connect(self.name_search_page)
        self.like_btn.clicked.connect(self.like_true_situation)
        self.like_btn_2.clicked.connect(self.like_false_situation)
        self.choice_btn.clicked.connect(self.jjim_situation)
        self.search_btn_2.clicked.connect(self.search_recipe_by_name)
        self.upload_btn.clicked.connect(self.open_file_dialog)
        self.add_btn.clicked.connect(self.add_prefer_food)
        self.retry_btn.clicked.connect(self.add_prefer_food_2)

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.login_check_signal.connect(self.login_check_situation)
        self.member_id_check_signal.connect(self.member_id_check_situation)
        self.member_join_signal.connect(self.member_join_clear)
        self.recommend_data_signal.connect(self.my_page_show)
        self.recipe_all_signal.connect(self.name_search_recipe_show)
        self.recipe_id_signal.connect(self.search_recipe)
        self.like_check_signal.connect(self.recipe_like_check)
        self.recipe_jjim_signal.connect(self.recipe_jjim_show)
        self.recipe_random_signal.connect(self.go_main_page)
        self.yolo_false_signal.connect(self.show_search_fail_dlg)
        self.rd_recipe_id_signal.connect(self.prefer_food_show)

    # ============================= 메인화면 광고배너 =================================
    def timer_event(self):
        """광고배너 타이머 이벤트 함수"""
        ad_list = [0, 1]
        self.ad.setCurrentIndex(ad_list[self.ad_count])
        self.ad_count += 1
        if self.ad_count == 2:
            self.ad_count = 0

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
        user_name = self.client.user_name
        self.lbl_user_name.setText(user_name)
        self.lbl_user_id.setText(user_id)
        self.client.send_recipe_random_access(user_id)

    def go_main_page(self, random_):
        """메인페이지 출력 / 추천 레시피 랜덤으로 출력해주는 함수"""
        random_recipe = self.decoder.binary_to_obj(random_)
        self.name_search_recipe_show(random_)
        random.shuffle(random_recipe)
        self.clear_layout(self.horizontalLayout)
        spacer = QSpacerItem(20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacer)
        name_list = list()
        id_list = list()
        img_list = list()
        for recipe_ in random_recipe[:3]:
            recipe_id = recipe_.recipe_id
            id_list.append(recipe_id)
            recipe_name = recipe_.recipe_name
            name_list.append(recipe_name)
            recipe_img = recipe_.recipe_img
            img_list.append(recipe_img)
        for i in range(len(name_list)):
            recommend = Recommend(name_list[i], img_list[i])
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
        recipe_ = -1
        self.client.send_recipe_all_access(recipe_)

    #### ★★★★★★★★★★★★★★★★★★★증 요★★★★★★★★★★★★★★★★★★★★★★★★★
    #### ★★★★★★★★★★★★★★★★★★★스 크 롤★★★★★★★★★★★★★★★★★★★★★★★★★
    def name_search_recipe_show(self, recipes_):
        """이름 검색 화면 레시피 출력 함수"""
        self.clear_layout(self.verticalLayout_4)
        spacer = QSpacerItem(20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacer)
        recipe_datas = self.decoder.binary_to_obj(recipes_)
        for i in recipe_datas:
            recipe_id = i.recipe_id
            recipe_name = i.recipe_name
            recipe_type = i.recipe_type
            recipe_img = i.recipe_img
            recipe = Recipes(recipe_name, recipe_type, recipe_img)
            self.verticalLayout_4.insertWidget(len(self.verticalLayout_4) - 1, recipe)
            recipe.mousePressEvent = lambda x=None, y=recipe_id: self.recipe_page_clicked(y)

    # ================================ 이미지 검색 =====================================
    def picture_page_show(self):
        """이미지 검색 화면 초기화 함수"""
        self.lbl_imgview: QLabel
        self.lbl_imgview.setObjectName("")
        self.home_page.setCurrentIndex(0)

    def classify_food_image(self):
        """음식 이미지 검색 함수 호출"""
        file_nm = self.lbl_imgview.objectName()

        if file_nm:
            self.client.classify_food_id_from_img(file_nm)
        else:
            self.error_box.error_text(100, "업로드 이미지가 없습니다.")
            self.error_box.exec_()

    def show_search_fail_dlg(self, e):
        """이미지 분류 실패 시 검색 실패 다이얼로그 출력"""
        self.error_box.error_text(100, "검색 결과가 없습니다.\n이미지를 확인해주세요.")
        self.error_box.exec_()

    def open_file_dialog(self):
        """파일 다이얼로그 출력 함수"""
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir=r"C:\Users\KDT113\Desktop\AIHomeMadeChef\Document",
                                               filetypes=(('Image files', '*.jpg;*.png'), ('All files', '*.*')))
        self.lbl_imgview.setPixmap(QPixmap(f'{file_path}'))

    # ================================ 마이 페이지 =====================================
    def my_page_request(self):
        """마이 페이지용 추천 음식 데이터 서버에 요청 함수"""
        user_id = self.client.user_id
        # 임시 데이터
        user_taste = ["11", "222", "3"]

        if user_taste:
            self.client.send_recommend_data_access(user_id, user_taste)
        else:
            self.home_page.setCurrentIndex(2)

    def my_page_show(self, recommend_list):
        """마이 페이지 추천 음식 데이터 출력 함수"""
        recipes = self.decoder.binary_to_obj(recommend_list)
        self.clear_layout(self.gridLayout)
        r, c = 0, 0
        for rcp in recipes:
            recipe_id = rcp.recipe_id
            recipe_name = rcp.recipe_name
            recipe_img = rcp.recipe_img
            suggest = Suggest(recipe_name, recipe_img)
            self.gridLayout.addWidget(suggest, r, c)
            c += 1
            if c == 3:
                c = 0
                r = 1
        self.home_page.setCurrentIndex(2)

    def add_prefer_food(self):
        """선호 음식 추가 버튼 클릭시 이벤트 함수 함수"""
        self.recipe_id_list = [n for n in range(1, 541)]
        self.add_prefer_food_2()

    def add_prefer_food_2(self):
        if len(self.recipe_id_list) > 12:
            random_id = random.sample(self.recipe_id_list, 12)
            for ran_id in random_id:
                if ran_id in self.recipe_id_list:
                    self.recipe_id_list.remove(ran_id)
            self.client.send_random_recipe_id_access(random_id)
        else:
            self.add_prefer_food()

    def prefer_food_show(self, prefer_):
        """선호 음식 12개 랜덤으로 받아오는 이벤트 함수"""
        prefer_data = self.decoder.binary_to_obj(prefer_)
        food_btn_list = [self.food_btn_1, self.food_btn_2, self.food_btn_3, self.food_btn_4, self.food_btn_5, self.food_btn_6,
                         self.food_btn_7, self.food_btn_8, self.food_btn_9, self.food_btn_10, self.food_btn_11, self.food_btn_12]
        for i, data in enumerate(prefer_data):
            recipe_id = data.recipe_id
            recipe_name = data.recipe_name
            food_btn_list[i].setText(recipe_name)
            food_btn_list[i].clicked.connect(lambda x=None, y=(recipe_id, recipe_name): self.food_name_text(y))
        self.home_page.setCurrentIndex(6)

    def food_name_text(self, data_):
        """선호 음식 추가 다이얼로그에서 음식 버튼 클릭시 이벤트 함수"""
        if len(self.label_38.text()) == 0:
            id_1 = data_[0]
            self.label_38.setText(f'{data_[1]}')
        elif len(self.label_46.text()) == 0:
            id_2 = data_[0]
            self.label_46.setText(f'{data_[1]}')
        elif len(self.label_51.text()) == 0:
            id_3 = data_[0]
            self.label_51.setText(f'{data_[1]}')

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
            recipe_img = rcp.recipe_img
            like_page = Likes(recipe_name, recipe_img)
            self.verticalLayout_5.insertWidget(len(self.verticalLayout_5) - 1, like_page)
            like_page.mousePressEvent = lambda x=None, y=recipe_id: self.recipe_page_clicked(y)
            like_page.jjim_btn.clicked.connect(lambda x=None, y=recipe_id: self.jjim_del(y))
        self.home_page.setCurrentIndex(3)

    def jjim_del(self, recipe_id):
        """찜페이지에서 하트버튼 클릭시 찜목록에서 삭제"""
        user_id = self.client.user_id
        self.client.send_hate_access(user_id, recipe_id)
        self.jjim_situation()
