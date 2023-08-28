import psycopg2 as pg
import pandas as pd

from Source.Data.Data import *


class DBConnector:
    __instance__ = None
    __HOST__ = "10.10.20.99"
    # __DATABASE__ = "HomemadeChef"
    __DATABASE__ = "HomeChefTest"
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
        self.DB = pg.connect(host=self.__HOST__,
                             dbname=self.__DATABASE__,
                             user=self.__USER__,
                             password=self.__PWD__,
                             port=self.__PORT__)

    def end_conn(self):
        if self.DB is not None:
            self.DB.close()
            self.DB = None

    def commit_db(self):
        self.DB.commit()

    # === CRUD COMMON
    def create_table(self):
        """새로운 테이블 생성"""
        self.start_conn()
        sql = "create"

        with self.DB.cursor() as cur:
            cur.execute(sql)

        self.commit_db()
        self.end_conn()

    def insert_data(self):
        self.start_conn()
        sql = ""

        try:
            with self.DB.cursor() as cur:
                cur.execute(sql)

            self.commit_db()

        except Exception as e:
            self.DB.rollback()
            print("Error : ", e)

        finally:
            self.end_conn()

    # === TB_USER
    def insert_userinfo_to_table(self, t_id: str, t_pwd: str, t_nm: str):
        """회원가입 사용자 정보 저장"""
        self.start_conn()
        sql = f"insert into \"TB_USER\"(\"USER_ID\", \"USER_PWD\", \"USER_NM\") values ('{t_id}', '{t_pwd}', '{t_nm}')"

        with self.DB.cursor() as cur:
            cur.execute(sql)

        self.commit_db()
        self.end_conn()

    def update_user_taste_info(self, t_id: str, t_taste: str):
        """사용자 선호 음식 정보 업데이트"""
        self.start_conn()
        sql = f"update \"TB_USER\" set \"USER_TASTE\"='{t_taste}' where \"USER_ID\" = '{t_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql)

        self.commit_db()
        self.end_conn()

    def login_by_id_pwd(self, t_id: str, t_pwd: str):
        """아이디, 비밀번호로 사용자 정보 조회 후 로그인 결과 반환"""
        self.start_conn()
        sql = f"select \"USER_ID\" from \"TB_USER\" where \"USER_ID\" = '{t_id}' and \"USER_PWD\" = '{t_pwd}'"

        with self.DB.cursor() as cur:
            cur.execute(sql, self.DB)
            data = cur.fetchone()   # -> (user_id, user_pwd, user_name)

        self.end_conn()

        if data:
            result = User(user_id=data[0])
        else:
            result = Result(False)

        return result

    def get_userinfo_by_id(self, t_id: str):
        """아이디로 사용자 닉네임, 선호 음식 정보 조회"""
        self.start_conn()
        sql = f"select \"USER_ID\", \"USER_NM\", \"USER_TASTE\" from \"TB_USER\" where \"USER_ID\" = '{t_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql, self.DB)
            data = cur.fetchone()

        self.end_conn()

        result = User(user_id=data[0], user_name=data[1], user_taste=data[2])
        return result

    def check_id_duplication(self, t_id: str):
        """아이디 중복 확인"""
        self.start_conn()
        sql = f"select count(\"USER_ID\") from \"TB_USER\" where \"USER_ID\" = '{t_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql, self.DB)
            data = cur.fetchone()

        self.end_conn()

        if data[0]:    # 중복 아이디 있을 때
            result = Result(False)
        else:
            result = Result(True)

        return result

    def delete_userinfo_to_table(self):
        """사용자 정보 삭제"""
        self.start_conn()
        sql1 = "delete from \"TB_USER\" where \"USER_ID\" = '{t_id}'"
        sql2 = "delete from \"TB_PREFER\" where \"USER_ID\" = '{t_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql1)
            cur.execute(sql2)

        self.commit_db()
        self.end_conn()

    # === TB_FOOD
    def insert_food_data(self, t_id: str, t_nm: str):
        """음식 클래스 정보 추가"""
        self.start_conn()
        sql = f"insert into \"TB_FOOD\"(\"FOOD_ID\", \"FOOD_NM\") values ('{t_id}', '{t_nm}')"

        with self.DB.cursor() as cur:
            cur.execute(sql)

        self.commit_db()
        self.end_conn()

    def find_recipe_eq_food_nm(self):
        """레시피와 동일한 음식 이름 찾기"""
        self.start_conn()
        sql1 = "select \"RECIPE_ID\", \"RECIPE_NM\" from \"TB_RECIPE\""

        try:
            with self.DB.cursor() as cur:
                cur.execute(sql1)
                recipes = cur.fetchall()
                for recipe_id, recipe_nm in recipes:
                    sql2 = f"update \"TB_FOOD\" set \"RECIPE_ID\"='{recipe_id}' where \"FOOD_NM\" = '{recipe_nm}'"
                    cur.execute(sql2)

            self.commit_db()

        except Exception as e:
            self.DB.rollback()
            print("Error : ", e)

        finally:
            self.end_conn()

    # === TB_PREFER
    def add_preference(self, user_id: str, food_id: str):
        """찜하기 추가"""
        self.start_conn()
        sql = f"insert into \"TB_PREFER\"(\"USER_ID\", \"RECIPE_ID\") values ('{user_id}', '{food_id}')"

        with self.DB.cursor() as cur:
            cur.execute(sql)

        self.commit_db()
        self.end_conn()

    def remove_preference(self, user_id: str, food_id: str):
        """찜하기 취소"""
        self.start_conn()
        sql = f"delete from \"TB_PREFER\" where \"USER_ID\" = '{user_id}' and \"RECIPE_ID\" = '{food_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql)

        self.commit_db()
        self.end_conn()

    # === TB_RECIPE
    def find_all_recipe_list(self):
        """전체 레시피 목록 조회"""
        self.start_conn()
        sql = "select \"RECIPE_ID\", \"RECIPE_NM\", \"RECIPE_TY\" from \"TB_RECIPE\""

        with self.DB.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()

        result_list = list()
        for row in data:
            result = Recipe(recipe_id=row[0], recipe_name=row[1], recipe_type=row[2])
            result_list.append(result)
        return result_list

    def insert_recipe_data(self, t_nm, t_ty, t_ingr, t_proc):
        """레시피 데이터 추가"""
        self.start_conn()
        sql = f"insert into \"TB_RECIPE\"(\"RECIPE_NM\", \"RECIPE_TY\", \"RECIPE_INGR\", \"RECIPE_PROC\") values ('{t_nm}', '{t_ty}', '{t_ingr}', '{t_proc}')"

        try:
            with self.DB.cursor() as cur:
                cur.execute(sql)

            self.commit_db()

        except Exception as e:
            self.DB.rollback()
            print("Error : ", e)

        finally:
            self.end_conn()

    def find_recipe_by_food_id(self, t_id: str):
        """레시피 정보 조회"""
        self.start_conn()
        sql = f"select \"RECIPE_ID\", \"RECIPE_NM\", \"RECIPE_TY\", \"RECIPE_INGR\", \"RECIPE_PROC\" " \
              f"from \"TB_RECIPE\" natural join \"TB_FOOD\" where \"FOOD_ID\" = '{t_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchone()

        self.end_conn()

        result = Recipe(recipe_id=data[0],
                        recipe_name=data[1],
                        recipe_type=data[2],
                        recipe_stuff=data[3],
                        recipe_step=data[4])
        return result

    def find_recipe_by_recipe_id(self, t_id: str):
        """레시피 정보 조회"""
        self.start_conn()
        sql = f"select \"RECIPE_ID\", \"RECIPE_NM\", \"RECIPE_TY\", \"RECIPE_INGR\", \"RECIPE_PROC\" " \
              f"from \"TB_RECIPE\" where \"RECIPE_ID\" = '{t_id}'"

        with self.DB.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchone()

        self.end_conn()

        result = Recipe(recipe_id=data[0],
                        recipe_name=data[1],
                        recipe_type=data[2],
                        recipe_stuff=data[3],
                        recipe_step=data[4])
        return result


if __name__ == '__main__':
    db = DBConnector()

    # db.insert_userinfo_to_table('admin', '1234', '관리자')
    # user_ = db.get_userinfo_by_id_pwd('admin', '1234')
    # result_ = db.check_id_duplication('admin')
    # db.insert_userinfo_to_table('joo', '1234', '주선생')
    # db.update_user_taste_info('joo', '갈비찜|오이소박이')

    # --- tb_food 데이터 넣기------------
    # food_id = ['01011001', '01012001', '01012002', '01012003', '01012004', '01012005', '01012006', '01013001', '01013002', '01014001', '01014002', '01014003', '01014004', '01014005', '01014006', '01014007', '01014008', '01014009', '01014010', '01014011', '01014012', '01014013', '01015002', '01015003', '01015004', '01015005', '01015006', '01015007', '01015008', '01015009', '01015010', '01015011', '01015012', '01015013', '01015014', '01015015', '01015016', '01015017', '01015018', '01015019', '01016001', '01016002', '01016003', '01016004', '01016005', '01016006', '01016007', '01016008', '01016009', '01016010', '01016011', '01016012', '01016013', '01016014', '01016015', '01016017', '01016018', '01016019', '01016020', '02011001', '02011002', '02011003', '02011004', '02011005', '02011006', '02011007', '02011008', '02011009', '02011010', '02011011', '02011012', '02011013', '02011014', '02011015', '02011016', '02011017', '02011018', '02011019', '02011020', '02011021', '02011023', '02011024', '02011025', '02011027', '02011028', '02011029', '02011030', '02011031', '02011032', '02011033', '02011034', '02011035', '02011036', '02011037', '02011038', '02011039', '02011040', '02012001', '02012002', '02012003', '02012004', '02012005', '03011001', '03011002', '03011003', '03011004', '03011005', '03011006', '03011007', '03011008', '03011009', '03011010', '03011011', '03012001', '03012002', '04011001', '04011002', '04011003', '04011004', '04011005', '04011006', '04011007', '04011008', '04011010', '04011011', '04011012', '04011013', '04011014', '04011015', '04011016', '04012001', '04012002', '04012003', '04012004', '04012005', '04012006', '04012007', '04012008', '04012009', '04012010', '04012011', '04012012', '04012013', '04013002', '04013003', '04013004', '04013005', '04013006', '04013007', '04013008', '04013009', '04013010', '04013011', '04013012', '04013013', '04013014', '04013015', '04013017', '04013018', '04013019', '04013020', '04013021', '04013022', '04013023', '04013024', '04014001', '04015001', '04015002', '04015003', '04016001', '04017001', '04017002', '04018001', '04018002', '04018003', '04018004', '04019001', '04019002', '04019003', '04019004', '04019005', '04019006', '04019007', '04019008', '05011001', '05011002', '05011004', '05011008', '05011010', '05011011', '05011012', '05012001', '05012002', '05012003', '05012004', '05012005', '05013001', '06012001', '06012002', '06012003', '06012004', '06012005', '06012006', '06012007', '06012008', '06012009', '06012010', '06012011', '06012012', '06012013', '06013001', '06013002', '06013003', '06014001', '07011001', '07011002', '07011003', '07011004', '07012001', '07012002', '07012003', '07013001', '07013002', '07013003', '07013004', '07013005', '07013006', '07013007', '07013008', '07013009', '07013010', '07013011', '07013012', '07013013', '07014001', '07014002', '07014003', '08011001', '08011002', '08011003', '08011004', '08011005', '08011006', '08011007', '08011008', '08012001', '08012002', '08012003', '08012004', '08012005', '08012006', '08012007', '08012008', '08012009', '08012010', '08013001', '08013002', '08013003', '08013004', '08013005', '08013006', '08014001', '08014002', '08014003', '09011001', '09011002', '09011003', '09011004', '09011005', '09011006', '09011007', '09011008', '09012001', '09012002', '09013001', '09013002', '09014001', '09014002', '09014003', '09014004', '09015001', '09015002', '09015003', '09016001', '10011001', '10011002', '10011003', '10011004', '10011005', '10012001', '10012002', '10012003', '10012004', '10012005', '10012006', '10012007', '10012008', '10012009', '10014001', '10014002', '10014003', '10014004', '10014005', '10014006', '11011001', '11011002', '11011003', '11011004', '11011005', '11011006', '11011007', '11011008', '11011009', '11011010', '11011011', '11012001', '11012002', '11012003', '11012004', '11013001', '11013002', '11013003', '11013004', '11013005', '11013006', '11013007', '11013009', '11013010', '11013011', '11013012', '11014001', '11014002', '11014003', '11014004', '11014005', '11014006', '11014007', '11014008', '11014009', '11014010', '11015001', '11015002', '12011001', '12011002', '12011003', '12011004', '12011005', '12011006', '12011007', '12011008', '12011009', '12011010', '12011011', '12011012', '12011013', '12011014', '12011015', '13011001', '13011002', '13011003', '13011004', '13011005', '13011006', '13011007', '13011008', '13011009', '13011010', '13011011', '13011012', '13012001', '13012002', '14011001', '14011002', '14011004', '14011005', '14012001', '14012002', '15011001', '15011002', '15011003', '15011004', '15011005', '15011006', '15011007', '15011008', '15011009', '15011010', '15011011', '15011012', '15011013', '15011014', '15011015', '15011016', '15011017', '16011001', '16011002', '16011003', '16011004', '16011005', '16011006']
    # df = pd.read_csv(r"D:\food_nm_data.csv")
    # food_nm = df.values.tolist()
    # for i, nm in zip(food_id, food_nm):
    #     print(i, nm[0])
    #     db.insert_food_data(i, nm[0])
    # ---------------------------------

    # db.add_preference('joo', '08013004')
    # db.remove_preference('joo', '08013004')
    # db.find_recipe_eq_food_nm()

    # recipe_ = db.find_recipe_by_food_id('08011004')
    # print(recipe_.recipe_name)

    # --- tb_recipe 데이터 넣기 ---------------
    # df_nm = pd.read_csv(r"D:\Recipe_NM.csv")
    # recipe_nm = df_nm.values.tolist()
    # df_ig = pd.read_csv(r"D:\Recipe_INGR.csv")
    # recipe_ig = df_ig.values.tolist()
    # df_pr = pd.read_csv(r"D:\Recipe_PROC.csv")
    # recipe_pr = df_pr.values.tolist()
    #
    # t_id = None
    # _ty = None
    # _nm = None
    # t_ig = None
    # t_pr = None
    #
    # for row in recipe_nm:
    #     t_id = row[0]
    #     _nm = row[1]
    #     _ty = row[2]
    #
    #     for ig in recipe_ig:
    #         if ig[0] == t_id:
    #             t_ig = ig[1]
    #             break
    #
    #     for pr in recipe_pr:
    #         if pr[0] == t_id:
    #             t_pr = pr[1]
    #
    #     db.insert_recipe_data(_nm, _ty, t_ig, t_pr)
    # -----------------------------------------

    # --- TB_RECIPE 누락 데이터 수기 추가 : 학습 진행 데이터에 한해 추가
    # db.insert_recipe_data("건새우볶음", "볶음", "", "")
    # db.insert_recipe_data("오징어볶음", "볶음", "", "")
    # db.insert_recipe_data("주꾸미볶음", "볶음", "", "")
    # db.insert_recipe_data("해물볶음", "볶음", "", "")
    # db.insert_recipe_data("감자볶음", "볶음", "", "")
    # db.insert_recipe_data("김치볶음", "볶음", "", "")
    # db.insert_recipe_data("깻잎나물볶음", "볶음", "", "")
    # db.insert_recipe_data("느타리버섯볶음", "볶음", "", "")
    # db.insert_recipe_data("머위나물볶음", "볶음", "", "")
    # db.insert_recipe_data("양송이버섯볶음", "볶음", "", "")
    # db.insert_recipe_data("표고버섯볶음", "볶음", "", "")
    # db.insert_recipe_data("고추잡채", "볶음", "", "")
    # db.insert_recipe_data("호박볶음", "볶음", "", "")
    # db.insert_recipe_data("돼지고기볶음", "볶음", "", "")
    # db.insert_recipe_data("돼지껍데기볶음", "볶음", "", "")
    # db.insert_recipe_data("소세지볶음", "볶음", "", "")
    # db.insert_recipe_data("오리불고기", "볶음", "", "")
    # db.insert_recipe_data("오삼불고기", "볶음", "", "")
    # db.insert_recipe_data("마파두부", "볶음", "", "")
