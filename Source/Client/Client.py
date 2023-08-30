import socket
from threading import *

from Source.Common.JSONConverter import ObjEncoder, ObjDecoder
from Source.Data.Data import *
from Source.Model.Classification import Classification


class ClientApp:
    # HOST = '10.10.20.113'
    HOST = '127.0.0.1'
    PORT = 9090
    BUFFER = 300000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    login_check = "login_check"
    member_id_check = "member_id_check"
    member_join = "member_join"
    recommend_data = "recommend_data"
    recipe_all = "recipe_all"
    recipe_id = "recipe_id"
    food_id = "food_id"
    recipe_like = "recipe_like"
    recipe_hate = "recipe_hate"
    like_check = "like_check"
    recipe_jjim = "recipe_jjim"
    recipe_random = "recipe_random"
    rd_recipe_id = "rd_recipe_id"
    prefer_food_save = "prefer_food_save"

    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.client_socket = None
        self.config = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

        self.receive_thread = Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def set_widget(self, widget_):
        self.client_widget = widget_

    def classify_food_id_from_img(self, file_nm: str):
        """이미지에서 음식 아이디 분류"""
        cf = Classification()
        result = cf.classify_obj_from_img(file_nm)
        print("[Yolo Result]", result)

        if result:
            self.send_food_id_access(result[0])
        else:
            self.client_widget.yolo_false_signal.emit(False)

    def send_login_check_access(self, user_id, user_pwd):
        """로그인 데이터 서버로 전송"""
        data_msg = User(user_id, user_pwd)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.login_check
        self.fixed_volume(header_data, data_msg_str)

    def send_member_id_check_access(self, user_id):
        """회원가입 아이디 중복 여부 데이터 서버로 전송"""
        data_msg = User(user_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.member_id_check
        self.fixed_volume(header_data, data_msg_str)

    def send_member_join_access(self, user_id, user_pwd, user_name):
        """회원가입 데이터 서버로 전송"""
        data_msg = User(user_id, user_pwd, user_name)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.member_join
        self.fixed_volume(header_data, data_msg_str)

    def send_recommend_data_access(self, user_id, user_taste):
        """마이 페이지 데이터 서버로 전송"""
        data_msg = User(user_id, user_taste=user_taste)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recommend_data
        self.fixed_volume(header_data, data_msg_str)

    def send_recipe_all_access(self, recipe_):
        """레시피 데이터 조회 서버로 전송"""
        data_msg = recipe_
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_all
        self.fixed_volume(header_data, data_msg_str)

    def send_recipe_id_access(self, recipe_id):
        """레시피 아이디로 데이터 조회 서버로 전송"""
        data_msg = Recipe(recipe_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_id
        self.fixed_volume(header_data, data_msg_str)

    def send_food_id_access(self, food_id: str):
        """음식 아이디로 데이터 조회 서버로 전송"""
        data_msg = Food(food_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.food_id
        self.fixed_volume(header_data, data_msg_str)

    def send_like_check(self, user_id, recipe_id):
        """찜하기 버튼 클릭 여부 조회 서버로 전송"""
        data_msg = Like(user_id, recipe_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.like_check
        self.fixed_volume(header_data, data_msg_str)

    def send_hate_access(self, user_id, recipe_id):
        """찜한 버튼 클릭시 데이터 서버로 전송"""
        data_msg = Like(user_id, recipe_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_hate
        self.fixed_volume(header_data, data_msg_str)

    def send_like_access(self, user_id, recipe_id):
        """찜하기 버튼 클릭시 찜목록 데이터 서버로 전송"""
        data_msg = Like(user_id, recipe_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_like
        self.fixed_volume(header_data, data_msg_str)

    def send_recipe_jjim_access(self, user_id):
        """레시피 찜 목록 출력을 위해 서버로 전송"""
        data_msg = User(user_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_jjim
        self.fixed_volume(header_data, data_msg_str)

    def send_recipe_random_access(self, recipe_):
        """홈화면 켜질때 추천 레시피 출력을 위해 서버로 데이터 전송"""
        data_msg = Recipe(recipe_)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_random
        self.fixed_volume(header_data, data_msg_str)

    def send_random_recipe_id_access(self, random_recipe_id):
        """선호 음식 추가 다이얼로그 버튼 출력을 위해 서버로 데이터 전송"""
        data_msg = Recipe(random_recipe_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.rd_recipe_id
        self.fixed_volume(header_data, data_msg_str)

    def send_prefer_food_save_access(self, recipe_id_list):
        """선호 음식 추가 다이얼로그에서 저장하기 버튼 클릭 시 서버로 레시피 아이디 리스트 전송"""
        taste_string = "|".join(recipe_id_list)
        data_msg = User(user_id=self.user_id, user_taste=taste_string)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.prefer_food_save
        self.fixed_volume(header_data, data_msg_str)

    def fixed_volume(self, header, data):
        """데이터 길이 맞춰서 서버로 전송"""
        header_msg = f"{header:<{self.HEADER_LENGTH}}".encode(self.FORMAT)
        data_msg = f"{data:<{self.BUFFER - self.HEADER_LENGTH}}".encode(self.FORMAT)
        self.client_socket.send(header_msg + data_msg)

    def receive_message(self):
        """서버에서 데이터 받아옴"""
        while True:
            return_result_ = self.client_socket.recv(self.BUFFER).decode(self.FORMAT)
            response_header = return_result_[:self.HEADER_LENGTH].strip()
            response_data = return_result_[self.HEADER_LENGTH:].strip()

            # 로그인
            if response_header == self.login_check:
                if response_data == '.':
                    self.client_widget.login_check_signal.emit(False)
                else:
                    object_data = self.decoder.binary_to_obj(response_data)
                    self.user_id = object_data.user_id
                    self.user_name = object_data.user_name
                    self.client_widget.login_check_signal.emit(True)

            # 회원가입 아이디 중복 확인
            if response_header == self.member_id_check:
                if response_data == '.':
                    self.client_widget.member_id_check_signal.emit(False)
                else:
                    self.client_widget.member_id_check_signal.emit(True)

            # 회원가입
            if response_header == self.member_join:
                self.client_widget.member_join_signal.emit(True)

            # 마이 페이지 추천 레시피 데이터
            if response_header == self.recommend_data:
                self.client_widget.recommend_data_signal.emit(response_data)

            # 레시피 전체 데이터
            if response_header == self.recipe_all:
                self.client_widget.recipe_all_signal.emit(response_data)

            # 레시피 아이디로 데이터 조회
            if response_header == self.recipe_id:
                self.client_widget.recipe_id_signal.emit(response_data)

            # 레시피 찜목록 버튼 클릭 여부 조회
            if response_header == self.like_check:
                object_data = self.decoder.binary_to_obj(response_data)
                self.client_widget.like_check_signal.emit(object_data.true_or_false)

            # 레시피 찜목록 추가 데이터 조회
            if response_header == self.recipe_like:
                print("찜하기 완료")

            # 레시피 찜목록 삭제
            if response_header == self.recipe_hate:
                print("찜삭제 완료")

            # 레시피 찜목록 출력
            if response_header == self.recipe_jjim:
                self.client_widget.recipe_jjim_signal.emit(response_data)

            # 레시피 랜덤으로 추천 출력
            if response_header == self.recipe_random:
                self.client_widget.recipe_random_signal.emit(response_data)

            # 랜덤 레시피 아이디 값으로 선호 음식 추가 다이얼로그 출력
            if response_header == self.rd_recipe_id:
                self.client_widget.rd_recipe_id_signal.emit(response_data)

            # 선호 음식 추가 다이얼로그에서 저장하기 버튼 클릭
            if response_header == self.prefer_food_save:
                self.client_widget.prefer_food_save_signal.emit(response_data)

