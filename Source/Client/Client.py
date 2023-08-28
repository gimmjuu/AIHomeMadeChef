import socket
from threading import *

from Source.Common.JSONConverter import ObjEncoder, ObjDecoder
from Source.Data.Data import *


class ClientApp:
    HOST = '10.10.20.113'
    # HOST = '127.0.0.1'
    PORT = 9070
    BUFFER = 150000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    login_check = "login_check"
    member_id_check = "member_id_check"
    member_join = "member_join"
    my_page_data = "my_page_data"
    recipe_all = "recipe_all"
    recipe_id = "recipe_id"

    def __init__(self):
        self.user_id = None
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

    def send_my_page_data_access(self, user_id):
        """마이 페이지 데이터 서버로 전송"""
        data_msg = User(user_id)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.my_page_data
        self.fixed_volume(header_data, data_msg_str)

    def send_recipe_all_access(self, recipe_):
        """레시피 데이터 조회 서버로 전송"""
        data_msg = recipe_
        header_data = self.recipe_all
        self.fixed_volume(header_data, data_msg)

    def send_recipe_id_access(self, recipe_id):
        """레시피 아이디로 데이터 조회 서버로 전송"""
        data_msg = Recipe(recipe_id, None)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.recipe_id
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

            # 마이 페이지 데이터
            if response_header == self.my_page_data:
                self.client_widget.my_page_data_signal.emit(response_data)

            # 레시피 전체 데이터
            if response_header == self.recipe_all:
                self.client_widget.recipe_all_signal.emit(response_data)

            # 레시피 아이디로 데이터 조회
            if response_header == self.recipe_id:
                self.client_widget.recipe_id_signal.emit(response_data)

