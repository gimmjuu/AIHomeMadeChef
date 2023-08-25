"""
Date : 23/08/24
Author : LSS & JHI
Detail : OpenAPI를 활용하여 수집한 데이터를 DataFrame에서 .csv파일로 저장합니다.
"""
import pandas as pd
import requests

# OpenWeatherMap API 키
API_KEY = "457bafd8245f4e2ca529"

# API 엔드포인트 및 요청 파라미터
url = f"http://openapi.foodsafetykorea.go.kr/api/{API_KEY}/COOKRCP01/json/1/50/RCP_PAT2=반찬"

# API 요청 보내기
response = requests.get(url)

# 응답 데이터 파싱
data = response.json()

RECIPE_NAME = list()
STUFF_INFO = list()
LOWSALTY_INFO = list()
RECIPE_CONTENT = list()

# 데이터 가공 및 출력
recipes = data["COOKRCP01"]["row"]

# print(recipes)
# print(len(recipes))     # 데이터 수

# DataFrame 생성용 데이터 리스트 저장
for recipe in recipes:
    RECIPE_NAME.append(recipe['RCP_NM'])
    STUFF_INFO.append(recipe["RCP_PARTS_DTLS"].replace("\n", " "))
    LOWSALTY_INFO.append(recipe["RCP_NA_TIP"].replace("\n", " "))
    contents = list()
    for i in range(1, 21):
        manual_: str = recipe[f"MANUAL{i:0>2}"]
        if manual_:
            contents.append(manual_.replace("\n", " "))
    RECIPE_CONTENT.append("--".join(contents))

recipe_data = {
    "RECIPE_NAME": RECIPE_NAME,
    "STUFF_INFO": STUFF_INFO,
    "LOWSALTY_INFO": LOWSALTY_INFO,
    "RECIPE_CONTENT": RECIPE_CONTENT
}

# --- DataFrame 생성 후 csv로 저장
df = pd.DataFrame(recipe_data)
df.to_csv("./recipes_dish.csv", sep="|", index=False)
