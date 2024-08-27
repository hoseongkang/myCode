import requests
import time
import bcrypt
import pybase64
import urllib.request
import urllib.parse
import json
import datetime
import sqlite3
from difflib import SequenceMatcher
import re
import joblib
text_clf = joblib.load('classify_address.pkl')

client_id = '*****'
client_secret = '$2a$04$*****'

strYear = 2024
strMonth = 5
    
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
        idRdn = str(shippingAddress.get("isRoadNameAddress"))
        keywords_chk = ["커피", "카페","디저트","아이스크림", "coffee", "cafe","빵", "베이커리","상가","간판","점","떡","버터","베이글","에스프레소","스위트","제과","브런치",
                        "달콩","달콤","샐러드","버거","sand","샌드","당","역사"]
        detailed_address = str(shippingAddress.get("detailedAddress"))
        search_text = str(shippingAddress.get("baseAddress")) + " " + str(shippingAddress.get("detailedAddress"))
        target = search_text
        # target = detailed_address
        postal_code = str(shippingAddress.get("zipCode"))
        address = str(shippingAddress.get("baseAddress")).split('(')[0].strip()
        print("=============================================================================")
        print("검색 주소 : " + address)
        print("검색 우편번호 : " + postal_code)
        def chkMatches():
            conn = sqlite3.connect('commRes.db')
            cursor = conn.cursor()
            if idRdn == 'True':
                query = """
                SELECT * FROM restaurant
                WHERE rdnPostNo LIKE ?
                AND rdnWhlAddr LIKE ?;
                """
            else:
                query = """
                SELECT * FROM restaurant
                WHERE rdnPostNo LIKE ?
                AND siteWhlAddr LIKE ?;
                """
            keywords = []
            uptaeNms = []
            try:
                cursor.execute(query, ('%' + postal_code + '%', '%' + address + '%'))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        # keywords.append(str(row[6]))
                        if idRdn == 'True':
                            keywords.append(str(row[6]) + " " + str(row[7]))
                        else:
                            keywords.append(str(row[5]) + " " + str(row[7]))
                        uptaeNms.append(str(row[3]))
                else:
                    return [], []
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

            finally:
                conn.close()
                return keywords, uptaeNms
        
        def match_ratio(s1, s2):
            return SequenceMatcher(None, s1, s2).ratio()

        keywords, uptaeNms = chkMatches()
        uptaeNm = ""
        bChk = "B2C"
        best_match_ratio = 0
        if keywords:
            print("키워드 검색됨")
            ratios = {keyword: match_ratio(target, keyword) for keyword in keywords}
            best_match = max(ratios, key=ratios.get)
            best_match_ratio = ratios[best_match]
            best_match_index = keywords.index(best_match)
            print("검색 값 : " +  str(best_match))
            print("정확도 : " + str(best_match_ratio))
            if best_match_ratio < 0.7:
                if detailed_address:
                    pattern = re.compile("|".join(keywords_chk))
                    if pattern.search(detailed_address):
                        uptaeNm = "기타"
                        bChk = "B2B"
                else:
                    bChk = "B2C"
                    uptaeNm = ""
            else:
                bChk = "B2B"
                uptaeNm = uptaeNms[int(best_match_index)]

        modified_text = re.sub(r'\d+동\s*\d+호', '', detailed_address)
        modified_text2 = re.sub(r'\d+-\d+', '', detailed_address)
        trimmed_text = modified_text.strip()
        if len(trimmed_text) == 0 or len(modified_text2) == 0:
            bChk = "B2C"
        else:
            is_dong_present = "동" in detailed_address
            is_ho_present = "호" in detailed_address
            is_apartment_present = "아파트" in detailed_address
            is_sg_present = "상가" in detailed_address
            pattern = r'\d+-\d+'
            match = re.search(pattern, detailed_address)
            if is_dong_present and is_ho_present or match:
                if is_sg_present:
                    bChk = "B2B"
                else:
                    new_data = [detailed_address]
                    predicted_labels = text_clf.predict(new_data)
                    predicted_probabilities = text_clf.predict_proba(new_data)
                    for data, label, probs in zip(new_data, predicted_labels, predicted_probabilities):
                        bChk = label
            else:
                new_data = [detailed_address]
                predicted_labels = text_clf.predict(new_data)
                predicted_probabilities = text_clf.predict_proba(new_data)
                for data, label, probs in zip(new_data, predicted_labels, predicted_probabilities):
                    max_prob = max(probs)
                if max_prob > 0.9 and best_match_ratio < 0.7: # 90%이상 확신이 있는 경우 고객 유형 확정하기
                    bChk = label

            # 키워드가 포함되어 있으면 무조건 B2B로 구분
            if detailed_address:
                pattern = re.compile("|".join(keywords_chk))
                if pattern.search(detailed_address):
                    uptaeNm = "기타"
                    bChk = "B2B"
        print("배송지 전체 : " + search_text)
        print("상세주소 : " + detailed_address)
        print("고객 구분 : " + bChk)

        formatted_item = {
            "구매확정일": productOrder.get("decisionDate"),
            "주문번호": order.get("orderId"),
            "상품주문번호": productOrder.get("productOrderId"),
            "상품주문상태": productOrder.get("productOrderStatus"),
            "상품명": productOrder.get("productName"),
            "채널상품번호": productOrder.get("productId"),
            "옵션코드": productOrder.get("optionManageCode"),
            "원상품번호": productOrder.get("originalProductId"),
            "판매자상품코드": productOrder.get("sellerProductCode"),
            "옵션코드": productOrder.get("optionCode"),
            "옵션금액": productOrder.get("optionPrice"),
            "상품옵션": productOrder.get("productOption"),
            "배송지": shippingAddress.get("baseAddress"),
            "상세주소": shippingAddress.get("detailedAddress"),
            "고객구분": bChk,
            "업태": uptaeNm,
            "우편번호": postal_code,
            "도로명": shippingAddress.get("isRoadNameAddress"),
            "수령인번호": shippingAddress.get("tel1"),
            "주문자번호": order.get("ordererTel"),
            "수령인": shippingAddress.get("name"),
            "수량": productOrder.get("quantity"),
            "상품주문금액": productOrder.get("totalProductAmount"),
            "총결제금액": productOrder.get("totalPaymentAmount"),
            "할인액": productOrder.get("productDiscountAmount"),
            "유입경로": productOrder.get("inflowPath"),
            "교환사유": exchange.get("exchangeReason"),
            "배송상태": delivery.get("deliveryStatus"),
            "배송완료일": delivery.get("deliveredDate"),
            "결제기기": order.get("payLocationType"),
            "결제수단": order.get("paymentMeans")
        }
        formatted_data.append(formatted_item)
    return formatted_data

access_token = get_access_token(client_id)
total_order = get_order_details(access_token, json_orderid_list)
with open("order_details_" + str(strYear) + "." + str(strMonth) + ".json", "w", encoding='utf-8') as file:
        file.write(total_order)
