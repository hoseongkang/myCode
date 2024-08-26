import requests
import pymysql
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
    return response.json()

order_id = "20240501-0001076"

api_url = f"https://serveq.cafe24api.com/api/v2/admin/orders/{order_id}"
# api_url = f'https://serveq.cafe24api.com/api/v2/admin/orders/{order_id}/receivers'
# api_url = f'https://serveq.cafe24api.com/api/v2/admin/orders/{order_id}/items'

bearer_token = access_token
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json",
    'X-Cafe24-Api-Version': '2024-06-01'
}

json_data = get_json_data(api_url, headers)

order_data = json_data.get('order')
initial_order_amount = order_data.get('initial_order_amount')
print(order_data)
# print(initial_order_amount.get('order_price_amount'))

# with open("cafe24_order_details.json", "w", encoding='utf-8') as file:
#     json.dump(order_data, file, indent=4)

# if json_data.get('links') and len(json_data['links']) > 0:
#     first_link = json_data['links'][0]
#     if 'href' in first_link:
#         print(True)
#         print("href 값:", first_link['href'])
#     else:
#         print(False)
# else:
#     print(False)