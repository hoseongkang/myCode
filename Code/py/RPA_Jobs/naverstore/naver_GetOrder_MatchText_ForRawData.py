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

            "productOrderId": productOrder.get("productOrderId"),
            "orderId": order.get("orderId"),
            "trackingNumber": delivery.get("trackingNumber"),
            "name": shippingAddress.get("name"),
            "decisionDate": productOrder.get("decisionDate"),
            "sendDate": delivery.get("sendDate"),
            "paymentDate": order.get("paymentDate"),
            "deliveryMethod": delivery.get("deliveryMethod"),
            "productId": productOrder.get("productId"),
            "productName": productOrder.get("productName"),
            "sellerProductCode": productOrder.get("sellerProductCode"),
            "optionManageCode": productOrder.get("optionManageCode"),
            "productOption": productOrder.get("productOption"),
            "quantity": productOrder.get("quantity"),
            "optionPrice": productOrder.get("optionPrice"),
            "unitPrice": productOrder.get("unitPrice"),
            "productClass": productOrder.get("productClass"),
            "productDiscountAmount": productOrder.get("productDiscountAmount"),
            "totalPaymentAmount": productOrder.get("totalPaymentAmount"),
            "shippingFeeType": productOrder.get("shippingFeeType"),
            "deliveryPolicyType": productOrder.get("deliveryPolicyType"),
            "deliveryFeeAmount": productOrder.get("deliveryFeeAmount"),
            "paymentCommission": productOrder.get("paymentCommission"),
            "knowledgeShoppingSellingInterlockCommission": productOrder.get("knowledgeShoppingSellingInterlockCommission"),
            "expectedSettlementAmount": productOrder.get("expectedSettlementAmount"),
            "ordererName": order.get("ordererName"),
            "ordererId": order.get("ordererId"),
            "productOrderStatus": productOrder.get("productOrderStatus"),
            "deliveredDate": delivery.get("deliveredDate"),
            "sellerCustomCode1": productOrder.get("sellerCustomCode1"),
            "sellerCustomCode2": productOrder.get("sellerCustomCode2"),
            "sectionDeliveryFee": productOrder.get("sectionDeliveryFee"),
            "paymentMeans": order.get("paymentMeans"),
            "payLocationType": order.get("payLocationType"),
            "commissionRatingType": productOrder.get("commissionRatingType"),
            "commissionPrePayStatus": productOrder.get("commissionPrePayStatus"),
            "inflowPath": productOrder.get("inflowPath"),
            "baseAddress": str(shippingAddress.get("baseAddress")) + " " + str(shippingAddress.get("detailedAddress")),
            # "detailedAddress": shippingAddress.get("detailedAddress"),
            "zipCode": shippingAddress.get("zipCode"),
            "tel1": shippingAddress.get("tel1"),
            "ordererTel": order.get("ordererTel"),
            "commissionRatingType": productOrder.get("commissionRatingType"),
            "sellerBurdenStoreDiscountAmount": productOrder.get("sellerBurdenStoreDiscountAmount"),
            "exchangeReason": exchange.get("exchangeReason"),
            "deliveryStatus": delivery.get("deliveryStatus")
        }
        formatted_data.append(formatted_item)
    return formatted_data

access_token = get_access_token(client_id)
total_order = get_order_details(access_token, json_orderid_list)
with open("order_details_" + str(strYear) + "." + str(strMonth) + ".json", "w", encoding='utf-8') as file:
        file.write(total_order)