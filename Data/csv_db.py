import psycopg2
import csv

# PostgreSQL 연결 설정
conn_params = {
    "host": "10.10.20.99",
    "database": "TB_TEST",
    "user": "postgres",
    "password": "1234"
}

conn = None  # conn 변수를 try 밖에서 미리 정의

# CSV 파일에서 데이터 읽기
csv_filename = "recipes_3.csv"
data = []
with open(csv_filename, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # 첫 줄(헤더) 건너뛰기
    data = [row for row in csv_reader]

try:
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    for row in data:
        STUFF_INFO, LOWSALTY_INFO, RECIPE_CONTENT = row
        cursor.execute('''
            INSERT INTO TB_TEST (재료, 조리법, 저감조리법)
            VALUES (%s, %s, %s)
        ''', (STUFF_INFO, LOWSALTY_INFO, RECIPE_CONTENT))

    conn.commit()
    print("데이터가 PostgreSQL에 저장되었습니다.")
except psycopg2.Error as e:
    print("Error:", e)
finally:
    if conn:
        conn.close()