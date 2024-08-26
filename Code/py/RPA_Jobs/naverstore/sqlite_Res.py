import sqlite3

conn = sqlite3.connect('commRes.db')
cursor = conn.cursor()

postal_code = '11941'
address = '경기도 구리시 원수택로32번길 24'

query = """
SELECT * FROM restaurant
WHERE rdnPostNo LIKE ?
AND rdnWhlAddr LIKE ?;
"""

my_list = []

try:
    cursor.execute(query, ('%' + postal_code + '%', '%' + address + '%'))

    rows = cursor.fetchall()

    if rows:
        print("Found rows:")
        for row in rows:
            my_list.append(str(row[5]) + " " + str(row[6]))
    else:
        print("No rows found matching the criteria.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()

print(my_list)
