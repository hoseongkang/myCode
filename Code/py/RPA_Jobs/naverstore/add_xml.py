import pyodbc
import json
import datetime
import requests
import time
import bcrypt
import pybase64

def getTimestamp():
    timestamp = str(int((time.time()-3) * 1000))
    return timestamp

def getpw(timestamp):
    client_id = '1jsN26VrBJtCXj99tLj5B6'
    client_secret = '$2a$04$xVQfiokNLKBWULOqjdFDJO'
    pwd = f'{client_id}_{timestamp}'
    hashed = bcrypt.hashpw(pwd.encode('utf-8'), client_secret.encode('utf-8'))
    client_secret_sign = pybase64.standard_b64encode(hashed).decode('utf-8')
    return client_secret_sign

def get_access_token(username):
    token_url = "https://api.commerce.naver.com/external/v1/oauth2/token"

    data = {
        'client_id': username,
        'timestamp': getTimestamp(),
        'grant_type': 'client_credentials',
        'client_secret_sign': getpw(getTimestamp()),
        'type': 'SELF'
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("토큰 요청에 실패했습니다.")
        return None

def get_order(access_token, start_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom={start_date_str}T00:00:00.000%2B09:00"
    accumulated_data = {"productOrderIds": []}
    headers = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        last_changed_date = data["data"]["lastChangeStatuses"][-1]["lastChangedDate"]
        first_last_changed_date = data["data"]["lastChangeStatuses"][0]["lastChangedDate"]
        start_month = start_date.month
        next_url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom={last_changed_date[:19]}.000%2B09:00"
        while datetime.datetime.strptime(first_last_changed_date[:10], "%Y-%m-%d").month == start_month:
            product_order_ids = [order["productOrderId"] for order in data["data"]["lastChangeStatuses"]]
            accumulated_data["productOrderIds"].extend(product_order_ids)
            response = requests.get(next_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                new_last_changed_date = data["data"]["lastChangeStatuses"][-1]["lastChangedDate"]
                first_last_changed_date = data["data"]["lastChangeStatuses"][0]["lastChangedDate"]
                if new_last_changed_date == last_changed_date:
                    break
                last_changed_date = new_last_changed_date
                print(last_changed_date)
                next_url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom={last_changed_date[:19]}.000%2B09:00"
            else:
                print("Error fetching next page:", response.status_code)
                break
        response = requests.get(next_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            next_url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom={last_changed_date[:19]}.000%2B09:00"
            product_order_ids = [order["productOrderId"] for order in data["data"]["lastChangeStatuses"]]
            accumulated_data["productOrderIds"].extend(product_order_ids)
    else:
        print("Error fetching initial page:", response.status_code)
    return accumulated_data

def get_order_details(access_token, json_orderid_list):
    json_orderid_list = json.dumps(json_orderid_list)
    url = "https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/query"
    
    try:
        orderid_data = json.loads(json_orderid_list)
    except json.JSONDecodeError:
        print("Error: Failed to decode json_orderid_list.")
        return None
    
    if "productOrderIds" not in orderid_data:
        print("Error: 'productOrderIds' key not found in json_orderid_list.")
        return None
    
    orderid_list = orderid_data["productOrderIds"]
    accumulated_data = []
    chunked_lists = [orderid_list[i:i+300] for i in range(0, len(orderid_list), 300)]
    
    for chunk in chunked_lists:
        client_id = '1jsN26VrBJtCXj99tLj5B6'
        access_token = get_access_token(client_id)
        payload = {
            "productOrderIds": chunk
        }
        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'content-type': "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]
            formatted_data = format_order_data(data)
            accumulated_data.extend(formatted_data)
        else:
            print("Error:", response.text)
            return None
    
    return json.dumps(accumulated_data, ensure_ascii=False)

def format_order_data(order_items):
    formatted_data = []
    for item in order_items:
        productOrder = item.get("productOrder", {})
        shippingAddress = productOrder.get("shippingAddress", {})
        exchange = item.get("exchange", {})
        delivery = item.get("delivery", {})
        order = item.get("order", {})

        formatted_item = {
            "상품주문번호": productOrder.get("productOrderId"),
            "오더번호": order.get("orderId"),
            "송장번호": delivery.get("trackingNumber"),
            "이름": shippingAddress.get("name"),
            "구매확정일": productOrder.get("decisionDate"),
            "발송일시": delivery.get("sendDate"),
            "결제일시": order.get("paymentDate"),
            "배송방법": delivery.get("deliveryMethod"),
            "채널상품번호": productOrder.get("productId"),
            "상품명": productOrder.get("productName"),
            "판매자상품코드": productOrder.get("sellerProductCode"),
            "판매자옵션코드": productOrder.get("optionManageCode"),
            "상품옵션": productOrder.get("productOption"),
            "수량": productOrder.get("quantity"),
            "옵션금액": productOrder.get("optionPrice"),
            "상품가격": productOrder.get("unitPrice"),
            "상품종류": productOrder.get("productClass"),
            "상품할인액": productOrder.get("productDiscountAmount"),
            "총결제금액_할인적용": productOrder.get("totalPaymentAmount"),
            "총결제금액_할인전": productOrder.get("totalProductAmount"),
            "배송비형태": productOrder.get("shippingFeeType"),
            "배송비정책": productOrder.get("deliveryPolicyType"),
            "배송비": productOrder.get("deliveryFeeAmount"),
            "결제수수료": productOrder.get("paymentCommission"),
            "네이버쇼핑매출연동수수료": productOrder.get("knowledgeShoppingSellingInterlockCommission"),
            "정산예정금액": productOrder.get("expectedSettlementAmount"),
            "주문자이름": order.get("ordererName"),
            "주문자ID": order.get("ordererId"),
            "상품주문상태": productOrder.get("productOrderStatus"),
            "배송완료일시": delivery.get("deliveredDate"),
            "판매자내부코드1": productOrder.get("sellerCustomCode1"),
            "판매자내부코드2": productOrder.get("sellerCustomCode2"),
            "지역추가배송비": productOrder.get("sectionDeliveryFee"),
            "결제수단": order.get("paymentMeans"),
            "결제기기": order.get("payLocationType"),
            "수수료과금구분_결제수수료": productOrder.get("commissionRatingType"),
            "수수료선결제상태": productOrder.get("commissionPrePayStatus"),
            "유입경로": productOrder.get("inflowPath"),
            "전체배송지주소": str(shippingAddress.get("baseAddress")) + " " + str(shippingAddress.get("detailedAddress")),
            "배송지": str(shippingAddress.get("baseAddress")),
            "배송지상세": shippingAddress.get("detailedAddress"),
            "우편번호": shippingAddress.get("zipCode"),
            "수령인연락처": shippingAddress.get("tel1"),
            "주문자연락처": order.get("ordererTel"),
            "판매자부담스토어할인액": productOrder.get("sellerBurdenStoreDiscountAmount"),
            "클레임요청사유": exchange.get("exchangeReason"),
            "배송상태": delivery.get("deliveryStatus")
        }
        if formatted_item["배송상태"] == "DELIVERY_COMPLETION" or formatted_item["배송상태"] == "NOT_TRACKING":
            if formatted_item["구매확정일"] is not None:
                formatted_data.append(formatted_item)
            
    return formatted_data

def updateNew(strInput):
    arrInput2 = strInput.split('/')
    strYear = arrInput2[0]
    strMonth = arrInput2[1]
    client_id = '1jsN26VrBJtCXj99tLj5B6'
    access_token = get_access_token(client_id)
    start_date = datetime.datetime(int(strYear), int(strMonth), 1)
    json_orderid_list = get_order(access_token, start_date)
    total_order = get_order_details(access_token, json_orderid_list)

    server = '130.1.22.33,2433'
    database = 'PowerBI'
    username = 'sa'
    password = '@sygrpa22!'

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = conn.cursor()

    query = f"SELECT [상품주문번호] FROM naverstore_main WHERE 구매확정일 LIKE '{strYear}%'"
    cursor.execute(query)

    rows = cursor.fetchall()
    existing_order_numbers = {row[0] for row in rows}

    all_data = []
    cnt = 0
    data = json.loads(total_order)
    all_data.extend(data)
    print(all_data)
    for item in all_data:
        porductNum = item.get("상품주문번호")
        if porductNum not in existing_order_numbers:
            상품주문번호 = item.get("상품주문번호")
            오더번호 = item.get("오더번호")
            송장번호 = item.get("송장번호")
            이름 = item.get("이름")
            구매확정일 = item.get("구매확정일")
            발송일시 = item.get("발송일시")
            결제일시 = item.get("결제일시")
            배송방법 = item.get("배송방법")
            채널상품번호 = item.get("채널상품번호")
            상품명 = item.get("상품명")
            판매자상품코드 = item.get("판매자상품코드")
            판매자옵션코드 = item.get("판매자옵션코드")
            상품옵션 = item.get("상품옵션")
            수량 = item.get("수량")
            옵션금액 = item.get("옵션금액")
            상품가격 = item.get("상품가격")
            상품종류 = item.get("상품종류")
            상품할인액 = item.get("상품할인액")
            총결제금액_할인적용 = item.get("총결제금액_할인적용")
            총결제금액_할인전 = item.get("총결제금액_할인전")
            배송비형태 = item.get("배송비형태")
            배송비정책 = item.get("배송비정책")
            배송비 = item.get("배송비")
            결제수수료 = item.get("결제수수료")
            네이버쇼핑매출연동수수료 = item.get("네이버쇼핑매출연동수수료")
            정산예정금액 = item.get("정산예정금액")
            주문자이름 = item.get("주문자이름")
            주문자ID = item.get("주문자ID")
            상품주문상태 = item.get("상품주문상태")
            배송완료일시 = item.get("배송완료일시")
            판매자내부코드1 = item.get("판매자내부코드1")
            판매자내부코드2 = item.get("판매자내부코드2")
            지역추가배송비 = item.get("지역추가배송비")
            결제수단 = item.get("결제수단")
            결제기기 = item.get("결제기기")
            수수료과금구분_결제수수료 = item.get("수수료과금구분_결제수수료")
            수수료선결제상태 = item.get("수수료선결제상태")
            유입경로 = item.get("유입경로")
            전체배송지주소 = item.get("전체배송지주소")
            배송지 = item.get("배송지")
            배송지상세 = item.get("배송지상세")
            우편번호 = item.get("우편번호")
            수령인연락처 = item.get("수령인연락처")
            주문자연락처 = item.get("주문자연락처")
            판매자부담스토어할인액 = item.get("판매자부담스토어할인액")
            클레임요청사유 = item.get("클레임요청사유")
            배송상태 = item.get("배송상태")
            cnt = cnt + 1
            
            insert_query = '''INSERT INTO [PowerBI].[dbo].[naverstore_main] (상품주문번호, 오더번호, 송장번호, 이름, 구매확정일, 발송일시, 결제일시, 배송방법, 채널상품번호, 상품명, 판매자상품코드, 판매자옵션코드, 상품옵션, 수량, 옵션금액, 상품가격, 상품종류, 상품할인액, 총결제금액_할인적용, 총결제금액_할인전, 배송비형태, 배송비정책, 배송비, 결제수수료, 네이버쇼핑매출연동수수료, 정산예정금액, 주문자이름, 주문자ID, 상품주문상태, 배송완료일시, 판매자내부코드1, 판매자내부코드2, 지역추가배송비, 결제수단, 결제기기, 수수료과금구분_결제수수료, 수수료선결제상태, 유입경로, 전체배송지주소, 배송지, 배송지상세, 우편번호, 수령인연락처, 주문자연락처, 판매자부담스토어할인액, 클레임요청사유, 배송상태)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            # cursor.execute(insert_query, (상품주문번호, 오더번호, 송장번호, 이름, 구매확정일, 발송일시, 결제일시, 배송방법, 채널상품번호, 상품명, 판매자상품코드, 판매자옵션코드, 상품옵션, 수량, 옵션금액, 상품가격, 상품종류, 상품할인액, 총결제금액_할인적용, 총결제금액_할인전, 배송비형태, 배송비정책, 배송비, 결제수수료, 네이버쇼핑매출연동수수료, 정산예정금액, 주문자이름, 주문자ID, 상품주문상태, 배송완료일시, 판매자내부코드1, 판매자내부코드2, 지역추가배송비, 결제수단, 결제기기, 수수료과금구분_결제수수료, 수수료선결제상태, 유입경로, 전체배송지주소, 배송지, 배송지상세, 우편번호, 수령인연락처, 주문자연락처, 판매자부담스토어할인액, 클레임요청사유, 배송상태))
            # conn.commit()
    conn.close()

strInput = '2024/6'

updateNew(strInput)

