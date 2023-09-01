import os
import random
from threading import Thread

from PyQt5.QtWidgets import QWidget, QLayout, QLabel, QFileDialog, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.uic import loadUi

from Source.Common.JSONConverter import *
from Source.View.Splash import SplashScreen, SplashThread
from Source.View.Cooking import Cooking
from Source.View.Ingredient import Ingredient
from Source.View.Like import Likes
from Source.View.Recipes import Recipes
from Source.View.Recommend import Recommend
from Source.View.Suggest import Suggest
from Source.View.Telegram import TelegramBot
from Source.View.Error import Error


class Main(QWidget):
    login_check_signal = pyqtSignal(bool)
    member_id_check_signal = pyqtSignal(bool)
    member_join_signal = pyqtSignal(bool)
    recommend_data_signal = pyqtSignal(list)
    recipe_all_signal = pyqtSignal(str)
    recipe_id_signal = pyqtSignal(str)
    recipe_like_signal = pyqtSignal(str)
    recipe_hate_signal = pyqtSignal(str)
    like_check_signal = pyqtSignal(bool)
    recipe_jjim_signal = pyqtSignal(str)
    recipe_random_signal = pyqtSignal(str)
    yolo_false_signal = pyqtSignal(bool)
    rd_recipe_id_signal = pyqtSignal(str)
    prefer_food_save_signal = pyqtSignal(str)

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
        self.selected_items = list()
        self.food_btn_list = self.food_btn_area.findChildren(QPushButton)
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

        # 에러 메시지 다이얼로그
        self.error_box = Error()

        # 텔레그램 쓰레드
        self.img_thread = Thread(target=self.telebot.start_polling, daemon=True)
        self.img_thread.start()

        # gif 실행 코드
        self.movie = QMovie('../../Images/cafe.gif')
        self.movie_2 = QMovie('../../Images/trip.gif')
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_2.setCacheMode(QMovie.CacheAll)
        self.label_33.setMovie(self.movie) # 샌드위치 gif
        self.label_35.setMovie(self.movie_2) # 요리 여행 gif
        self.movie.start()
        self.movie_2.start()

        # 광고 배너 qtimer
        self.timer = QTimer(self)
        self.timer.setInterval(5000)  # 5초 반복
        self.timer.timeout.connect(self.timer_event)
        self.ad.setCurrentIndex(0)
        self.ad_count = 1
        self.home_page.currentChanged.connect(self.timer_check)

        # 이름 검색 라인 에딧 엔터
        self.lineEdit.returnPressed.connect(self.on_enter_pressed)

    def on_enter_pressed(self):
        self.search_btn_2.click()

    def lbl_event(self):
        """라벨 클릭 이벤트 함수"""
        self.label_11.mousePressEvent = self.close_event

    def close_event(self, e):
        """프로그램 종료 이벤트 함수"""
        self.client.client_socket.close()

        files_ = os.listdir(r'../Model/Temp')
        for file_ in files_:
            if '.jpg' in file_ or '.png' in file_ or '.jpeg' in file_:
                os.remove(fr'../Model/Temp/{file_}')

        self.close()

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        # 로그인 화면 버튼
        self.close_btn.clicked.connect(self.close_event)
        self.join_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.login_btn.clicked.connect(self.login_check)

        # 회원가입 화면 버튼
        self.back_btn.clicked.connect(self.back_join_page)
        self.id_check.clicked.connect(self.member_id_check)

        # 선호 음식 버튼
        for i, btn in enumerate(self.food_btn_list):
            btn.released.connect(lambda x=i: self.add_food_name_prefer_list(x))

        # 메인화면 버튼
        self.picture_btn.clicked.connect(self.picture_page_show)
        self.search_btn.clicked.connect(self.classify_food_image)
        self.mypage_btn.clicked.connect(self.my_page_request)
        self.request_btn.clicked.connect(self.member_join_request)
        self.home_btn.clicked.connect(self.home_menu)
        self.name_search_btn.clicked.connect(self.name_search_recipe_show)
        self.like_btn.clicked.connect(self.like_true_situation)
        self.like_btn_2.clicked.connect(self.like_false_situation)
        self.choice_btn.clicked.connect(self.jjim_situation)
        self.search_btn_2.clicked.connect(self.search_recipe_by_name)
        self.upload_btn.clicked.connect(self.open_file_dialog)
        self.add_btn.clicked.connect(self.add_prefer_food)
        self.retry_btn.clicked.connect(self.request_prefer_food)
        self.save_btn.clicked.connect(self.prefer_food_save)
        self.back_page_btn.clicked.connect(self.prefer_back_page)
        self.all_del_btn.clicked.connect(self.prefer_text_del)

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.login_check_signal.connect(self.login_check_situation)
        self.member_id_check_signal.connect(self.member_id_check_situation)
        self.member_join_signal.connect(self.member_join_clear)
        self.recommend_data_signal.connect(self.recommendation_item_check)
        self.recipe_id_signal.connect(self.search_recipe)
        self.like_check_signal.connect(self.recipe_like_check)
        self.recipe_jjim_signal.connect(self.recipe_jjim_show)
        self.recipe_random_signal.connect(self.go_main_page)
        self.recipe_all_signal.connect(self.set_all_recipe_list)
        self.yolo_false_signal.connect(self.show_search_fail_dlg)
        self.rd_recipe_id_signal.connect(self.prefer_food_show)
        self.prefer_food_save_signal.connect(self.prefer_list_show)

    # ============================= 메인화면 광고배너 =================================
    def timer_event(self):
        """광고배너 타이머 이벤트 함수"""
        ad_list = [0, 1]
        self.ad.setCurrentIndex(ad_list[self.ad_count])
        self.ad_count += 1
        if self.ad_count == 2:
            self.ad_count = 0

    def timer_check(self):
        """현재 홈화면을 확인한 후 타이머를 실행시키는 함수"""
        if self.home_page.currentIndex() == 4:
            self.timer.start()
        else:
            if self.timer.isActive():
                self.timer.stop()

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
        self.home_page: QStackedWidget
        self.home_page.setCurrentIndex(4)

    # ================================= 회원가입 ================================
    def back_join_page(self):
        """회원가입 페이지에서 뒤로가기 버튼 클릭 이벤트"""
        self.stackedWidget.setCurrentIndex(0)
        self.join_id.clear()
        self.join_pw.clear()
        self.check_pw.clear()
        self.join_name.clear()

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
        self.lbl_user_name.setText(self.client.user_id)
        self.lbl_user_id.setText(self.client.user_name)

        all_recipe_id = [n for n in range(1, 541)]
        target_id_list = random.sample(all_recipe_id, 3)
        self.client.send_recipe_random_access(target_id_list)

    def go_main_page(self, random_):
        """메인페이지 출력 / 추천 레시피 랜덤으로 출력해주는 함수"""
        random_list = self.decoder.binary_to_obj(random_)

        for recipe_ in random_list:
            recommend = Recommend(recipe_.recipe_name, recipe_.recipe_img)
            recommend.mousePressEvent = lambda x=None, y=recipe_.recipe_id: self.recipe_page_clicked(y)
            self.horizontalLayout.addWidget(recommend)

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
    def name_search_recipe_show(self):
        """이름 검색 화면 전체 레시피 요청 함수"""
        self.home_page.setCurrentWidget(self.page_7)
        if self.widget_14.findChildren(Recipes):
            return

        self.client.send_recipe_all_access(Recipe(0))

    def set_all_recipe_list(self, t_list):
        """이름 검색 화면 전체 레시피 출력 함수"""
        # ------------------------------------------- 로딩 화면 -------------------------------------------
        # loading_thread = SplashThread(loading)
        # loading_thread.start()
        all_recipe = self.decoder.binary_to_obj(t_list)

        for i, rcp_ in enumerate(all_recipe):
            recipe = Recipes(rcp_.recipe_name, rcp_.recipe_type, rcp_.recipe_img)
            self.verticalLayout_4.addWidget(recipe)
            recipe.mousePressEvent = lambda x, y=rcp_.recipe_id: self.recipe_page_clicked(y)

        # loading_thread.start()
        # loading_thread.quit()
        # --------------------------------------------------------------------------------------------

    def search_recipe_by_name(self):
        """레시피 이름 검색 버튼 클릭시 이벤트 함수"""
        search_name = self.lineEdit.text()
        recipe_list = self.scrollAreaWidgetContents_5.findChildren(Recipes)

        base_size, item_cnt = 80, 0

        for recipe_ in recipe_list:
            if search_name in recipe_.label_2.text():
                recipe_.setVisible(True)
                item_cnt += 1
            else:
                recipe_.setVisible(False)

        self.scrollAreaWidgetContents_5.setMaximumHeight(base_size * item_cnt)

    # ================================ 이미지 검색 =====================================
    def picture_page_show(self):
        """이미지 검색 화면 초기화 함수"""
        if self.home_page.currentIndex() != 0:
            self.lbl_imgview: QLabel
            self.lbl_imgview.setText("Image Preview")
            self.lbl_imgview.setObjectName("")
            self.lbl_imgview.setPixmap(QPixmap(""))
            self.home_page.setCurrentIndex(0)

    def classify_food_image(self):
        """음식 이미지 검색 함수 호출"""
        file_path = self.lbl_imgview.objectName()

        if file_path:
            self.client.classify_food_id_from_img(file_path)
        else:
            self.error_box.error_text(100, "업로드 이미지가 없습니다.")
            self.error_box.exec_()

    def show_search_fail_dlg(self, e):
        """이미지 분류 실패 시 검색 실패 다이얼로그 출력"""
        self.error_box.error_text(100, "검색 결과가 없습니다.\n이미지를 확인해주세요.")
        self.error_box.exec_()

    def open_file_dialog(self):
        """파일 다이얼로그 출력 함수"""
        fname = QFileDialog.getOpenFileNames(self, 'Open File', r'../Model/Temp', 'Image files(*.jpg *.png)')

        if fname[0]:
            self.lbl_imgview.setObjectName(fname[0][0])
            self.lbl_imgview.setPixmap(QPixmap(fr'{fname[0][0]}'))

    # ================================ 마이 페이지 =====================================
    def my_page_request(self):
        """마이 페이지용 사용자 선호 음식 정보, 추천 음식 데이터 서버에 요청 함수"""
        user_id = self.client.user_id
        self.client.send_recommend_data_access(user_id)

    def recommendation_item_check(self, resp_list: list):
        """마이 페이지 관련 응답 데이터 처리 함수"""
        user_taste = resp_list[0].user_taste.split("|")
        self.set_prefer_list(user_taste)
        self.home_page.setCurrentIndex(2)

        if len(resp_list) > 1:
            # 추천 음식 데이터가 있을 때
            self.my_page_show(resp_list[1:])

    def prefer_list_show(self, prefer_list):
        """선호 음식 박스 위젯 출력 이벤트 함수"""
        result_ = self.decoder.binary_to_obj(prefer_list)
        if result_.true_or_false:
            self.my_page_request()

    def set_prefer_list(self, t_list: list):
        """유저의 선호 음식 리스트 받아와서 라벨에 출력해주는 함수"""
        prefer_lbl_list = [[self.prefer_lbl_1, self.prefer_lbl_2],
                           [self.prefer2_lbl_1, self.prefer2_lbl_2],
                           [self.prefer3_lbl_1, self.prefer3_lbl_2]]

        if t_list[0] == '':
            t_list[0] = '없음'

        for i in range(3 - len(t_list)):
            t_list.append('없음')

        for nm, lb in zip(t_list, prefer_lbl_list):
            print(len(nm))
            if len(nm) > 8:
                lb[0].setText(f"{nm[:7]}\n{nm[7:]}")
            else:
                lb[0].setText(nm)
            if len(nm) > 8:
                lb[1].setText(f"{nm[:7]}\n{nm[7:]}")
            else:
                lb[1].setText(nm)


    def my_page_show(self, recipes):
        """마이 페이지 추천 음식 데이터 출력 함수"""
        self.clear_layout(self.gridLayout)
        r, c = 0, 0
        for rcp in recipes:
            suggest = Suggest(rcp.recipe_name, rcp.recipe_img)
            suggest.mousePressEvent = lambda x, y=rcp.recipe_id: self.recipe_page_clicked(y)
            self.gridLayout.addWidget(suggest, r, c)
            c += 1
            if c == 3:
                c = 0
                r = 1

    def add_prefer_food(self):
        """선호 음식 추가 화면 초기화 함수"""
        self.recipe_id_list = [n for n in range(1, 541)]
        self.request_prefer_food()

    def request_prefer_food(self):
        """선호 음식 추가 버튼 클릭시 이벤트 함수"""
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
        prefer_data: list
        self.food_btn_list: list

        for btn, rcp in zip(self.food_btn_list, prefer_data):
            btn.setChecked(False)
            btn.setObjectName(f"{rcp.recipe_id}")
            btn.setText(rcp.recipe_name)

        self.home_page.setCurrentIndex(6)

    def add_food_name_prefer_list(self, idx: int):
        """선호 음식 추가 다이얼로그에서 음식 버튼 클릭시 이벤트 함수"""
        btn = self.food_btn_list[idx]
        target_ = [int(btn.objectName()), btn.text()]
        labels = [self.label_38, self.label_46, self.label_51]

        if btn.isChecked():
            if self.selected_items and len(self.selected_items) == 3:
                btn.setChecked(False)
                return
            self.selected_items.append(target_)

        else:
            self.selected_items.remove(target_)

        for i, lbl in enumerate(labels):
            if (i+1) <= len(self.selected_items):
                lbl.setText(self.selected_items[i][1])
            else:
                lbl.setText("")

    def prefer_food_save(self):
        """선호 음식 추가 다이얼로그에서 저장하기 버튼 클릭 시 이벤트 함수"""
        if len(self.selected_items) == 0:
            self.error_box.error_text(100, "선택한 음식이 없습니다.")
            self.error_box.exec_()
            return

        self.error_box.error_text(11)
        self.error_box.exec_()
        self.client.send_prefer_food_save_access([str(item[0]) for item in self.selected_items])
        self.home_page.setCurrentIndex(2)
        self.label_38.clear()
        self.label_46.clear()
        self.label_51.clear()

    def prefer_text_del(self):
        """선호 음식 추천 다이얼로그에서 전체 삭제 버튼 클릭시 선택 내용 초기화"""
        self.selected_items.clear()
        self.label_38.clear()
        self.label_46.clear()
        self.label_51.clear()

        for btn in self.food_btn_list:
            btn.setChecked(False)

    def prefer_back_page(self):
        """선호음식 추가 다이얼로그에서 뒤로가기 버튼 클릭시 이벤트 함수"""
        self.label_38.clear()
        self.label_46.clear()
        self.label_51.clear()
        self.home_page.setCurrentIndex(2)

    # ============================================ 레시피  ===========================================
    def recipe_page_clicked(self, recipe_id):
        """서버로 레시피 아이디 전송"""
        self.client.send_recipe_id_access(recipe_id)

    def search_recipe(self, recipe_data):
        """레시피 검색시 출력 함수"""
        recipe_datas = self.decoder.binary_to_obj(recipe_data)
        recipe_id = recipe_datas.recipe_id
        recipe_step = recipe_datas.recipe_step

        # --- 레이아웃 비우기
        self.clear_layout(self.verticalLayout)
        self.clear_layout(self.verticalLayout_3)

        # --- 재료 출력
        self.lbl_recipe_name.setText(f'<{recipe_datas.recipe_name}> 레시피')
        self.like_btn.setObjectName(f"{recipe_id}")
        self.like_btn_2.setObjectName(f"{recipe_id}")
        ingredient = Ingredient(recipe_datas.recipe_stuff)
        self.verticalLayout.addWidget(ingredient)

        # --- 조리법 출력
        recipe_step = recipe_step.replace("/ ", "")
        step_split = recipe_step.split("|")

        for i, v in enumerate(step_split):
            cooking = Cooking(i, v)
            self.verticalLayout_3.addWidget(cooking)

        self.client.send_like_check(self.client.user_id, recipe_id)

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
        recipes = self.decoder.binary_to_obj(recipe_data)

        for rcp in recipes:
            recipe_id = rcp.recipe_id
            like_page = Likes(rcp.recipe_name, rcp.recipe_img)
            self.verticalLayout_5.addWidget(like_page)
            like_page.mousePressEvent = lambda x=None, y=recipe_id: self.recipe_page_clicked(y)
            like_page.jjim_btn.clicked.connect(lambda x=None, y=recipe_id: self.jjim_del(y))

        self.scrollAreaWidgetContents_4.setMaximumHeight(len(recipes) * 100)
        self.home_page.setCurrentIndex(3)

    def jjim_del(self, recipe_id):
        """찜 페이지에서 하트 버튼 클릭시 찜목록에서 삭제"""
        user_id = self.client.user_id
        self.client.send_hate_access(user_id, recipe_id)
        self.jjim_situation()
