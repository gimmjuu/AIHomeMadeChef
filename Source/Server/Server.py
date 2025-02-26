import select

from socket import *
from threading import Thread

from Source.Common.DBConnector import DBConnector
from Source.Common.JSONConverter import ObjEncoder, ObjDecoder
from Source.Data.Data import *
from Source.Server.Nomination import Nomination


class Server:
    # HOST = '10.10.20.113'
    HOST = '127.0.0.1'
    PORT = 3313
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
    like_check = "like_check"
    recipe_hate = "recipe_hate"
    recipe_jjim = "recipe_jjim"
    recipe_random = "recipe_random"
    rd_recipe_id = "rd_recipe_id"
    prefer_food_save = "prefer_food_save"
    pass_encoded = "pass"
    dot_encoded = "."

    def __init__(self, db_conn: DBConnector):
        # 서버 소켓 설정
        self.db_conn = db_conn
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
            print(f"Server RECEIVED: ({request_header})")
        except Exception as e:
            # print("[ Server Error ]", e)
            return False

        # 로그인
        if request_header == self.login_check:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.login_by_id_pwd(object_.user_id, object_.user_pwd)

            if result_ == Result(False):
                response_header = self.login_check
                response_data = self.dot_encoded
                return_result = self.fixed_volume(response_header, response_data)
                self.send_message(client_socket, return_result)
            else:
                response_header = self.login_check
                response_data = self.encoder.to_JSON_as_binary(result_)
                return_result = self.fixed_volume(response_header, response_data)
                self.send_message(client_socket, return_result)

        # 회원가입 아이디 중복 체크
        if request_header == self.member_id_check:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.check_id_duplication(object_.user_id)
            if result_ == Result(False):
                response_header = self.member_id_check
                response_data = self.dot_encoded
                return_result = self.fixed_volume(response_header, response_data)
                self.send_message(client_socket, return_result)
            else:
                response_header = self.member_id_check
                response_data = self.encoder.to_JSON_as_binary(result_)
                return_result = self.fixed_volume(response_header, response_data)
                self.send_message(client_socket, return_result)

        # 회원가입
        if request_header == self.member_join:
            object_ = self.decoder.binary_to_obj(request_data)
            self.db_conn.insert_userinfo_to_table(object_.user_id, object_.user_pwd, object_.user_name)
            response_header = self.member_join
            response_data = self.encoder.to_JSON_as_binary(Result(True))
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 마이페이지 : 추천 레시피 조회
        if request_header == self.recommend_data:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = list()
            result_1 = self.db_conn.get_usertaste_by_id(object_.user_id)
            result_.append(result_1)

            if result_1.user_taste:
                taste_list = result_1.user_taste.split("|")

                # --- 사용자 선호 음식 이름 조회
                recipes = self.db_conn.find_optional_recipe_list(taste_list)
                recipes = [rcp.recipe_name for rcp in recipes]
                result_1.user_taste = "|".join(recipes)

                # --- 사용자 추천 음식 정보 조회
                result_2 = self.get_nomination_result(result_1.user_id, taste_list)
                if result_2:
                    result_.extend(result_2)

            print("[Server : recommend_data]", result_)
            response_header = self.recommend_data
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 전체 데이터 조회
        if request_header == self.recipe_all:
            result_ = self.db_conn.find_all_recipe_list()
            response_header = self.recipe_all
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 아이디로 데이터 조회
        if request_header == self.recipe_id:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.find_recipe_by_recipe_id(object_.recipe_id)
            response_header = self.recipe_id
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 음식 아이디로 데이터 조회
        if request_header == self.food_id:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.find_recipe_by_food_id(object_.food_id)
            response_header = self.recipe_id
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 찜버튼 클릭 여부
        if request_header == self.like_check:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.find_preference(object_.like_user_id, object_.like_recipe_id)
            response_header = self.like_check
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 찜목록 추가
        if request_header == self.recipe_like:
            object_ = self.decoder.binary_to_obj(request_data)
            self.db_conn.add_preference(object_.like_user_id, object_.like_recipe_id)
            response_header = self.recipe_like
            response_data = self.encoder.to_JSON_as_binary(Result(True))
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 찜목록 삭제
        if request_header == self.recipe_hate:
            object_ = self.decoder.binary_to_obj(request_data)
            self.db_conn.remove_preference(object_.like_user_id, object_.like_recipe_id)
            response_header = self.recipe_hate
            response_data = self.encoder.to_JSON_as_binary(Result(True))
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 찜목록 조회/출력
        if request_header == self.recipe_jjim:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.find_all_prefers_by_user_id(object_.user_id)
            response_header = self.recipe_jjim
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 레시피 랜덤 출력
        if request_header == self.recipe_random:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.find_optional_recipe_list(object_.recipe_id)
            response_header = self.recipe_random
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 랜덤 레시피 아이디로 선호 음식 다이얼로그 출력
        if request_header == self.rd_recipe_id:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.find_optional_recipe_list(object_.recipe_id)
            response_header = self.rd_recipe_id
            response_data = self.encoder.to_JSON_as_binary(result_)
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

        # 선호 음식 선택 화면 저장하기 버튼 클릭
        if request_header == self.prefer_food_save:
            object_ = self.decoder.binary_to_obj(request_data)
            self.db_conn.update_user_taste_info(object_.user_id, object_.user_taste)
            response_header = self.prefer_food_save
            response_data = self.encoder.to_JSON_as_binary(Result(True))
            return_result = self.fixed_volume(response_header, response_data)
            self.send_message(client_socket, return_result)

    def get_nomination_result(self, user_id: str, user_taste: list):
        """각 사용자의 선호에 맞는 추천 레시피 반환 -> 6개의 아이디 리스트"""
        result = list()

        nm = Nomination()
        nm.load_dataset()
        recommends = nm.get_recommendation_list(user_id, user_taste)

        for item in recommends:
            data_ = self.db_conn.select_data("\"RECIPE_NM\", \"RECIPE_THUMB\"", "\"TB_RECIPE\"", f"\"RECIPE_ID\" = '{item}'")
            result.append(Recipe(recipe_id=item, recipe_name=data_[0][0], recipe_img=data_[0][1]))

        print("[서버] 추천 음식 개수 :", len(result))
        return result
