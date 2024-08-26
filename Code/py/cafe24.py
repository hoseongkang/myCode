import pymysql

def fetch_access_tokens():
    db_host = "121.189.58.66"
    port = 3306
    db_username = "syds"
    db_password = "syds123!@$"
    db_name = "serveq"

    try:
        connection = pymysql.connect(
            host=db_host,
            port=port,
            user=db_username,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        query = "SELECT * FROM saved_token_cafe24_valid;"

        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            access_tokens = row['access_token']

        cursor.close()
        connection.close()

        return access_tokens

    except pymysql.Error as e:
        print("Error connecting to MariaDB:", e)
        return []

access_token = fetch_access_tokens()
print(access_token)
