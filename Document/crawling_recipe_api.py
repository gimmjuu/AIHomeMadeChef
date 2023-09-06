"""
작성일 : 23/08/25 - 작성자 : 이승신
수정일 : 23/08/27 - 수정자 : 주혜인
내용 :  OpenAPI를 이용해 레시피 데이터를 수집한 후 DataFrame to CSV 형식으로 저장합니다.
"""
import pandas as pd
import requests


# --- DataFrame 생성 후 csv로 저장
def save_dataframe_to_csv(file_nm: str, t_data: dict):
    df = pd.DataFrame(t_data)
    df.to_csv(rf"D:\{file_nm}.csv", sep=",", index=False)


class RecipeCrawling:
    def __init__(self):
        # OpenAPI 키
        self.API_KEY = "aeaaef1f2483999fecab071763879b319ece69e40ba51f12cb115a23ba5389d4"
        # API 엔드포인트 및 요청 파라미터
        self.url_nm = f"http://211.237.50.150:7080/openapi/{self.API_KEY}/json/Grid_20150827000000000226_1"
        self.url_ingr = f"http://211.237.50.150:7080/openapi/{self.API_KEY}/json/Grid_20150827000000000227_1"
        self.url_proc = f"http://211.237.50.150:7080/openapi/{self.API_KEY}/json/Grid_20150827000000000228_1"

    def request_data_parsing(self, t_type: int, start_point: int, end_point: int):
        t_url = ''

        if t_type == 6:
            t_url = self.url_nm
        elif t_type == 7:
            t_url = self.url_ingr
        elif t_type == 8:
            t_url = self.url_proc

        # API 요청 보내기
        response = requests.get(f"{t_url}/{start_point}/{end_point}")
        # 응답 데이터 파싱
        data = response.json()
        data_dict = data[f"Grid_2015082700000000022{t_type}_1"]["row"]

        return data_dict

    def set_recipe_nm_dict(self, t_data_nm):
        # 데이터 저장용
        recipe_nm = dict()
        recipe_nm["RECIPE_ID"] = list()
        recipe_nm["RECIPE_NM"] = list()
        recipe_nm["RECIPE_TY"] = list()

        # --- 레시피 기본정보
        for row in t_data_nm:
            recipe_nm["RECIPE_ID"].append(row["RECIPE_ID"])
            recipe_nm["RECIPE_NM"].append(row["RECIPE_NM_KO"])
            recipe_nm["RECIPE_TY"].append(row["TY_NM"])
        print(len(recipe_nm["RECIPE_ID"]))
        return recipe_nm

    def set_recipe_ingr_data(self, t_data_ingr):
        recipe_ingr = dict()
        recipe_ingr["RECIPE_ID"] = list()
        recipe_ingr["RECIPE_INGR"] = list()

        # --- 레시피 재료정보
        prev_recipe_id = 0

        for row in t_data_ingr:
            t_id = row['RECIPE_ID']

            if t_id != prev_recipe_id:
                if (len(recipe_ingr["RECIPE_ID"]) - 1) >= 0:
                    strip_string = recipe_ingr["RECIPE_INGR"][len(recipe_ingr["RECIPE_ID"]) - 1].rstrip("|")
                    recipe_ingr["RECIPE_INGR"][len(recipe_ingr["RECIPE_ID"]) - 1] = strip_string

                prev_recipe_id = t_id
                recipe_ingr["RECIPE_ID"].append(t_id)
                recipe_ingr["RECIPE_INGR"].append("")

            if row["IRDNT_CPCTY"]:
                recipe_ingr["RECIPE_INGR"][len(recipe_ingr["RECIPE_ID"])-1] += f"{row['IRDNT_NM']}({row['IRDNT_CPCTY']})|"
            else:
                recipe_ingr["RECIPE_INGR"][len(recipe_ingr["RECIPE_ID"])-1] += f"{row['IRDNT_NM']}|"

        return recipe_ingr

    def set_recipe_proc_data(self, t_data_proc):
        recipe_proc = dict()
        recipe_proc["RECIPE_ID"] = list()
        recipe_proc["RECIPE_PROC"] = list()

        # --- 과정정보
        prev_recipe_id = 0
        for row in t_data_proc:
            t_id = row['RECIPE_ID']

            if t_id != prev_recipe_id:
                if (len(recipe_proc["RECIPE_ID"]) - 1) > -1:
                    strip_string = recipe_proc["RECIPE_PROC"][len(recipe_proc["RECIPE_ID"]) - 1].rstrip("|")
                    recipe_proc["RECIPE_PROC"][len(recipe_proc["RECIPE_ID"]) - 1] = strip_string

                prev_recipe_id = t_id
                recipe_proc["RECIPE_ID"].append(t_id)
                recipe_proc["RECIPE_PROC"].append("")

            step_string: str = row['COOKING_DC']
            if "\n" in step_string:
                step_string = step_string.replace("\n", "|/ ")
            recipe_proc["RECIPE_PROC"][len(recipe_proc["RECIPE_ID"]) - 1] += f"/ {step_string}|"

        return recipe_proc


if __name__ == '__main__':
    rc = RecipeCrawling()

    # --- 기본정보
    # nm_dict = rc.request_data_parsing(6, 1, 1000)
    # result = rc.set_recipe_nm_dict(nm_dict)
    # save_dataframe_to_csv(result, 'Recipe_NM')
    
    # --- 재료정보
    # ingr_dict = rc.request_data_parsing(7, 1, 999)
    # ingr_1 = rc.set_recipe_ingr_data(ingr_dict)
    # ingr_dict = rc.request_data_parsing(7, 1000, 1993)
    # ingr_2 = rc.set_recipe_ingr_data(ingr_dict)
    # ingr_dict = rc.request_data_parsing(7, 1994, 2990)
    # ingr_3 = rc.set_recipe_ingr_data(ingr_dict)
    # ingr_dict = rc.request_data_parsing(7, 2991, 3985)
    # ingr_4 = rc.set_recipe_ingr_data(ingr_dict)
    # ingr_dict = rc.request_data_parsing(7, 3985, 4981)
    # ingr_5 = rc.set_recipe_ingr_data(ingr_dict)
    # ingr_dict = rc.request_data_parsing(7, 4982, 5980)
    # ingr_6 = rc.set_recipe_ingr_data(ingr_dict)
    # ingr_dict = rc.request_data_parsing(7, 5981, 6105)
    # ingr_7 = rc.set_recipe_ingr_data(ingr_dict)
    # --- dataframe concat
    # df_1 = pd.DataFrame(ingr_1)
    # df_2 = pd.DataFrame(ingr_2)
    # df_3 = pd.DataFrame(ingr_3)
    # df_4 = pd.DataFrame(ingr_4)
    # df_5 = pd.DataFrame(ingr_5)
    # df_6 = pd.DataFrame(ingr_6)
    # df_7 = pd.DataFrame(ingr_7)
    # df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7])
    # df.to_csv(rf"D:\Recipe_INGR.csv", sep=",", index=False)
    
    # --- 과정정보
    # proc_dict = rc.request_data_parsing(8, 1, 994)
    # proc_1 = rc.set_recipe_proc_data(proc_dict)
    # proc_dict = rc.request_data_parsing(8, 995, 1990)
    # proc_2 = rc.set_recipe_proc_data(proc_dict)
    # proc_dict = rc.request_data_parsing(8, 1991, 2987)
    # proc_3 = rc.set_recipe_proc_data(proc_dict)
    # proc_dict = rc.request_data_parsing(8, 2988, 3022)
    # proc_4 = rc.set_recipe_proc_data(proc_dict)
    # --- dataframe concat
    # df_1 = pd.DataFrame(proc_1)
    # df_2 = pd.DataFrame(proc_2)
    # df_3 = pd.DataFrame(proc_3)
    # df_4 = pd.DataFrame(proc_4)
    # df = pd.concat([df_1, df_2, df_3, df_4])
    # df.to_csv(rf"D:\Recipe_PROC.csv", sep=",", index=False)
