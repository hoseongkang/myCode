import requests
import time
import bcrypt
import pybase64
import json
import datetime

client_id = '1jsN26VrBJtCXj99tLj5B6'
client_secret = '$2a$04$xVQfiokNLKBWULOqjdFDJO'

strYear = 2024
strMonth = 8

def getTimestamp():
  timestamp = str(int((time.time()-3) * 1000))
  return timestamp

def getpw(timestamp):
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
    
access_token = get_access_token(client_id)

def get_order(access_token, start_date):
    start_date_str = start_date.strftime("%Y-%m-%d")
    url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom={start_date_str}T00:00:00.000%2B09:00"
    accumulated_data = {"productOrderIds": []}
    headers = {
        'Authorization': 'Bearer ' + access_token
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
            
        print(last_changed_date)
        response = requests.get(next_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            next_url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses?lastChangedFrom={last_changed_date[:19]}.000%2B09:00"
            product_order_ids = [order["productOrderId"] for order in data["data"]["lastChangeStatuses"]]
            accumulated_data["productOrderIds"].extend(product_order_ids)
    else:
        print("Error fetching initial page:", response.status_code)
    return accumulated_data

start_date = datetime.datetime(strYear, strMonth, 1)
json_orderid_list = get_order(access_token, start_date)

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
    print(str(len(orderid_list)) + "개 주문 데이터 확인")
    chunked_lists = [orderid_list[i:i+300] for i in range(0, len(orderid_list), 300)]
    
    for chunk in chunked_lists:
        access_token = get_access_token(client_id)
        payload = {
            "productOrderIds": chunk
        }
        headers = {
            'Authorization': 'Bearer ' + access_token,
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
        if formatted_item["배송상태"] == "DELIVERY_COMPLETION":
            formatted_data.append(formatted_item)
        formatted_data.append(formatted_item)
    return formatted_data

access_token = get_access_token(client_id)
total_order = get_order_details(access_token, json_orderid_list)
print(total_order)

with open("order_details_" + str(strYear) + "." + str(strMonth) + ".json", "w", encoding='utf-8') as file:
        file.write(total_order)