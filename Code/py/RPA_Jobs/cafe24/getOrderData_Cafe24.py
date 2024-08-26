import requests
import pymysql
import time
import json

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

def get_json_data(api_url, headers):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()

api_url = "https://serveq.cafe24api.com/api/v2/admin/orders?start_date=2024-06-01&end_date=2024-06-01&offset=0&limit=10"
bearer_token = fetch_access_tokens()
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json",
    'X-Cafe24-Api-Version': '2024-01-01'
}

chkp = False
formatted_data = []
while not chkp:
    json_data = get_json_data(api_url, headers)
    print(json_data)
    try:
        if 'links' in json_data:
            link_data = json_data.get('links')
            for link in link_data:
                if link.get('rel') == 'next':
                    next_link = link.get('href')
                    print(next_link)
                    chkp = True
                    break
        else:
            chkp = False
    except:
        chkp = False
    finally:
        time.sleep(0.1)


order_data = json_data.get('orders')
# for item in order_data:
#     order_data = item.get("order_id", {})
#     print(order_data)
formatted_data.append(order_data)
chkp = False

if next_link:
    api_url = next_link
    while not chkp:
        json_data = get_json_data(api_url, headers)
        order_data = json_data.get('orders')
        # for item in order_data:
        #     order_data = item.get("order_id", {})
        #     print(order_data)
        formatted_data.append(order_data)
        link_data = json_data.get('links', {})
        for link in link_data:
            if link.get('rel') == 'next':
                next_link = link.get('href')
                api_url = next_link
                chkp = False
                break
            else:
                chkp = True

# print(len(formatted_data))
with open("cafe24_orders.json", "w", encoding='utf-8') as file:
     json.dump(formatted_data, file, indent=4)