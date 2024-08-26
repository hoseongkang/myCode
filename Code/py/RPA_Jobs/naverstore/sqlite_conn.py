import sqlite3

conn = sqlite3.connect('restaurant_data.db')
cursor = conn.cursor()

cursor.execute('SELECT rdnPostNo FROM restaurant WHERE rdnPostNo = "611675"')
rows = cursor.fetchall()

if rows:
    print("exists!")
else:
    print("does not exists!")

conn.close()
