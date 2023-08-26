import socket
from threading import *

from Source.Common.JSONConverter import ObjEncoder, ObjDecoder
from Source.Data.Data import *


class ClientApp:
    HOST = '10.10.20.113'
    # HOST = '127.0.0.1'
    PORT = 9090
    BUFFER = 100000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    login_check = "login_check"
    member_join = "member_join"

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
        print("send")
        data_msg = User(user_id, user_pwd)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.login_check
        self.fixed_volume(header_data, data_msg_str)

    def send_member_join_access(self, user_id, user_pwd, user_name):
        """회원가입 데이터 서버로 전송"""
        data_msg = User(user_id, user_pwd, user_name)
        data_msg_str = self.encoder.to_JSON_as_binary(data_msg)
        header_data = self.member_join
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
            # 회원가입
            if response_header == self.member_join:
                self.client_widget.abcdef.emit(response_data)

