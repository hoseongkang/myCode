import json
import pyodbc

json_file_path = 'C:/python/test/19-22.json'

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

server = '130.1.22.33,2433'
database = 'PowerBI'
username = 'sa'
password = '@sygrpa22!'
table_name = 'FoodAdditivesReport'

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

insert_query = f"""
INSERT INTO {table_name} (
    주소 , 품목제조번호 , 보고년도 , 인허가번호 , 품목명 , 생산량_KG , 업소명 , 품목유형 , 연간생산능력_KG 
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for item in data:
    cursor.execute(insert_query, (
        item["SITE_ADDR"], item["PRDLST_REPORT_NO"], item["EVL_YR"], item["LCNS_NO"],
        item["PRDLST_NM"], item["PRDCTN_QY"], item["BSSH_NM"], item["H_ITEM_NM"],
        item["FYER_PRDCTN_ABRT_QY"]
    ))

print("커밋 전")
conn.commit()

cursor.close()
conn.close()

print("데이터 삽입이 완료되었습니다.")
