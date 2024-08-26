import pymysql
import pandas as pd

con = pymysql.connect(host='localhost', user='mysql_user_id', password='_password_', db='access_db', charset='utf8') # �ѱ�ó�� (charset = 'utf8')
 
# STEP 3: Connection ���κ��� Cursor ����
cur = con.cursor()
 
# STEP 4: SQL�� ���� �� Fetch
sql = "SELECT player, birth FROM baseball"
cur.execute(sql)
 
# ����Ÿ Fetch
rows = cur.fetchall()
print(rows)     # ��ü rows

# STEP 5: DB ���� ����
con.close()