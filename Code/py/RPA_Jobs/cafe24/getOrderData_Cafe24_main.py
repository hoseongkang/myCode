import requests, pymysql, json
from datetime import datetime, timedelta
import calendar

def get_dates_from_month(month_str):
    year_month = datetime.strptime(month_str, '%Y-%m')
    year = year_month.year
    month = year_month.month

    first_day = datetime(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    last_day_of_month = datetime(year, month, last_day)

    dates = []
    current_date = first_day

    while current_date <= last_day_of_month:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return dates

loopMon = get_dates_from_month('2024-06')

# strDate = '2024-07-02'

def fetch_access_tokens():
    db_host = "*****"
    port = 3306
    db_username = "syds"
    db_password = "*****"
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
        return []

def get_json_data(strDate, cnt, limit):
    api_url = f"https://serveq.cafe24api.com/api/v2/admin/orders?start_date={strDate}&end_date={strDate}&offset={cnt}&limit={limit}"
    return api_get(api_url)

def get_json_data_type(type, sInput):
    if type == 'receivers':
        api_url = f'https://serveq.cafe24api.com/api/v2/admin/orders/{sInput}/receivers'
    elif type == 'items':
        api_url = f'https://serveq.cafe24api.com/api/v2/admin/orders/{sInput}/items?date_type=purchaseconfirmation_date'
    return api_get(api_url)

def api_get(api_url):
    bearer_token = fetch_access_tokens()
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        'X-Cafe24-Api-Version': '2024-06-01'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    
limit = 10
formatted_data = []

for strDate in loopMon:
    chklimit = False
    cnt = 0
    print(strDate, " API Get")
    while not chklimit:
        json_orders = get_json_data(strDate, cnt, limit)
        order_data = json_orders.get('orders')
        for item in order_data:
            orderID = item.get("order_id")
            json_receivers = get_json_data_type('receivers', orderID)
            receivers_item = json_receivers.get('receivers')
            json_items = get_json_data_type('items', orderID)
            items_item = json_items.get('items')
            initial_order_data = item.get('initial_order_amount')
            
            for item_no in items_item:
                if item_no.get("status_text") == '구매확정':
                    print(item.get("order_id"), item_no.get("product_price"), initial_order_data.get("order_price_amount"), receivers_item[0].get("name"), receivers_item[0].get("address1"), receivers_item[0].get("address2"))
                    formatted_item = {
                        "order_data": item.get("order_id"), # 오더번호
                        "purchaseconfirmation_date": item_no.get("purchaseconfirmation_date"), # 구매확정일
                        "order_item_code": item_no.get("order_item_code"), # 오더번호_상품별
                        "item_no": item_no.get("item_no"),
                        "variant_code": item_no.get("variant_code"),
                        "product_code": item_no.get("product_code"), # 상품번호 
                        "internal_product_name": item_no.get("internal_product_name"), # 상품명 (관리용)
                        "custom_product_code": item_no.get("custom_product_code"), # 상품코드
                        "option_id": item_no.get("option_id"), # 옵션코드
                        "product_name": item_no.get("product_name"), # 상품명
                        "product_price": item_no.get("product_price"), # 결제 금액
                        "option_price": item_no.get("option_price"), # 옵션 금액
                        "shipping_fee": item_no.get("shipping_fee"), # 베송비
                        # 쿠폰 부분
                        "order_price_amount": initial_order_data.get("order_price_amount"),
                        "points_spent_amount" : initial_order_data.get("points_spent_amount"),
                        "membership_discount_amount" : initial_order_data.get("membership_discount_amount"),
                        "coupon_discount_price" : initial_order_data.get("coupon_discount_price"),
                        "payment_amount": item.get("payment_amount"), # 최종 결제 금액
                        "commission": item.get("commission"), # 수수료
                        "additional_discount_price": item_no.get("additional_discount_price"),
                        "quantity": item_no.get("quantity"), # 수량
                        "status_text": item_no.get("status_text"), # 주문상태 (ex 구매확정, 입금전취소 등)
                        "member_id": item.get("member_id"),  # 아이디
                        "member_email": item.get("member_email"),  # 메일주소
                        "member_authen": item.get("member_authentication"), # 회원 등급
                        
                        "additional_shipping_fee": item.get("additional_shipping_fee"), # 추가 배송비
                        "shipping_status": item.get("shipping_status"), # 배송상태
                        "naver_point": item.get("naver_point"), # 네이버포인트
                        "name" : receivers_item[0].get("name"), # 수령인
                        "cellphone" : receivers_item[0].get("cellphone"), # 수령인 전화번호
                        "address" : receivers_item[0].get("address1"), # 주소
                        "address_details" : receivers_item[0].get("address2"), # 수령인 전화번호
                    }
                    formatted_data.append(formatted_item)
        if len(order_data) == 0: # 조회된 건이 없는 경우 Loop 끝
            chklimit = True
        cnt += 10

with open(f"cafe24_orders_{strDate}.json", "w", encoding='utf-8') as file:
     json.dump(formatted_data, file, indent=4)
