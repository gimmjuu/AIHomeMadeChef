import os
import threading
from socket import *
from threading import Thread, Event, Timer
from Source.Common.JsonEncoder import *
import select

# from db.class_dbconnect import DBConnector


class Server:
    HOST = '10.10.20.113'
    # HOST = '127.0.0.1'
    PORT = 9090
    BUFFER = 100000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    login_check = "login_ckeck"
    member_join = "member_join"
    pass_encoded = "pass"
    dot_encoded = "."

    # def __init__(self, db_conn: DBConnector):
    def __init__(self):
        # 서버 소켓 설정
        # self.db_conn = db_conn
        self.server_socket = None
        self.config = None
        self.sockets_list = list()
        self.clients = dict()
        self.thread_for_run = None
        self.run_signal = True
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

    def start(self):
        if self.thread_for_run is not None:  # 실행중이면 종료 시키기
            return
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # AF_INET(ipv4를 의미)
        self.server_socket.bind((self.HOST, self.PORT))  # 바인딩
        self.server_socket.listen()  # 리슨 시작
        self.sockets_list.clear()  # 소켓리스트 클리어
        self.sockets_list.append(self.server_socket)
        self.run_signal = True
        self.thread_for_run = Thread(target=self.run)
        self.thread_for_run.start()

    def stop(self):
        self.run_signal = False
        if self.thread_for_run is not None:
            self.thread_for_run.join()
        self.server_socket.close()
        self.thread_for_run = None

    def run(self):
        while True:
            if self.run_signal is False:
                break
            try:
                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.1)
            except Exception:
                continue
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.sockets_list.append(client_socket)

                else:
                    message = self.receive_message(notified_socket)

                    if message is False:
                        continue

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    def send_message(self, client_socket: socket, result_):
        """클라이언트로 데이터 전달"""
        client_socket.send(result_)

    def fixed_volume(self, header, data):
        """데이터 규격 맞추기"""
        header_msg = f"{header:<{self.HEADER_LENGTH}}".encode(self.FORMAT)
        data_msg = f"{data:<{self.BUFFER - self.HEADER_LENGTH}}".encode(self.FORMAT)
        return header_msg + data_msg

    def receive_message(self, client_socket: socket):
        """클라이언트로부터 받은 데이터"""
        try:
            recv_message = client_socket.recv(self.BUFFER)
            request_header = recv_message[:self.HEADER_LENGTH].strip().decode(self.FORMAT)
            request_data = recv_message[self.HEADER_LENGTH:].strip().decode(self.FORMAT)
            print(f"Server RECEIVED: ({request_header},{request_data})")
            print(request_header)
            print(type(request_header))
        except:
            return False

        if request_header == self.login_check:
            pass
        # --- 참고 자료
        #     result_ = self.db_conn.find_tourist_info(request_data)
        #     if result_ is False:
        #         response_header = self.tourist_name
        #         response_data = self.dot_encoded
        #         return_result = self.fixed_volume(response_header, response_data)
        #         self.send_message(client_socket, return_result)
        #     else:
        #         response_header = self.tourist_name
        #         response_data = self.encoder.toJSON_as_binary(result_)
        #         return_result = self.fixed_volume(response_header, response_data)
        #         self.send_message(client_socket, return_result)
        #
        #     result_2 = self.db_conn.find_realty_info(request_data)
        #     if result_2 is False:
        #         response_header = self.realty_info
        #         response_data = self.dot_encoded
        #         return_result = self.fixed_volume(response_header, response_data)
        #         self.send_message(client_socket, return_result)
        #     else:
        #         response_header = self.realty_info
        #         response_data = self.encoder.toJSON_as_binary(result_2)
        #         return_result = self.fixed_volume(response_header, response_data)
        #         self.send_message(client_socket, return_result)
        # elif request_header == self.realty_data:
        #     obj_ = self.decoder.binary_to_obj(request_data)
        #     result_ = self.db_conn.search_addr(obj_, "year")
        #     response_header = self.year_data
        #     response_data = self.encoder.toJSON_as_binary(result_)
        #     return_result = self.fixed_volume(response_header, response_data)
        #     self.send_message(client_socket, return_result)
