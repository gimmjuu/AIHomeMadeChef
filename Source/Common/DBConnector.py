import psycopg2 as pg
import pandas as pd


class DBConnector:
    __instance__ = None
    __HOST__ = "10.10.20.99"
    __DATABASE__ = "HomemadeChef"
    __USER__ = "postgres"
    __PWD__ = 1234
    __PORT__ = 5432

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance__, cls):
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        self.DB = None

    # === connect
    def start_conn(self):
        connect_string = f"host={self.__HOST__}, dbname={self.__DATABASE__}, user={self.__USER__}, password={self.__PWD__}, port={self.__PORT__}"
        self.DB = pg.connect(connect_string)

    def end_conn(self):
        if self.DB is not None:
            self.DB.close()
            self.DB = None

    def commit_db(self):
        self.DB.commit()

    # === TB_USER
    def get_userinfo_by_id(self, t_id: str):
        """아이디로 사용자 정보 조회"""
        self.start_conn()
        sql = f"select * from \"TB_USER\" where \"USER_ID\" = {t_id}"
        with self.DB.cursor() as cur:
            cur.execute(sql, self.DB)
            data = cur.fetchone()   # -> (user_id, user_pwd, user_name)

        self.end_conn()
        return 

    def check_id_duplication(self, t_id: str):
        """아이디 중복 조회"""
        self.start_conn()
        sql = f"select * from \"TB_USER\" where \"USER_ID\" = {t_id}"
        with self.DB.cursor() as cur:
            cur.execute(sql, self.DB)
            data = cur.fetchone()

        if data:
            # 아이디 중복
            return False
        else:
            return True
