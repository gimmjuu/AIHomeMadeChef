import requests
import csv

# OpenWeatherMap API 키
API_KEY = "457bafd8245f4e2ca529"

# API 엔드포인트 및 요청 파라미터
url = f"http://openapi.foodsafetykorea.go.kr/api/{API_KEY}/COOKRCP01/json/1/1000/RCP_PAT2=반찬"

# API 요청 보내기
response = requests.get(url)

# 응답 데이터 파싱
data = response.json()

# CSV 파일로 저장할 파일명
csv_filename = "recipes_3.csv"

if "COOKRCP01" in data:
    recipes = data["COOKRCP01"]["row"]

    # CSV 파일 작성
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)

        # CSV 헤더 작성
        csv_writer.writerow(["재료", "조리법", "저감조리법"])

        for recipe in recipes:
            rcp_parts = recipe["RCP_PARTS_DTLS"]
            manual_list = []
            for i in range(1, 21):
                manual_ = recipe[f"MANUAL{i:0>2}"]
                if manual_:
                    manual_list.append(manual_)
            rcp_na_tip = recipe["RCP_NA_TIP"]

            # CSV 데이터 작성
            csv_writer.writerow([rcp_parts, "\n".join(manual_list), rcp_na_tip])

    print(f"데이터가 {csv_filename}에 저장되었습니다.")
else:
    print("Error:", data["RESULT"]["MESSAGE"])