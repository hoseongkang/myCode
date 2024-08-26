import os
import json

def secondone():
    directory_path = "C:/python"

    all_data = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.json'):
            with open(file_path, encoding='utf-8') as file:
                data = json.load(file)
                all_data.extend(data)

    order_ids = set()

    filtered_data = []

    for item in all_data: 
        order_id = item.get("상품주문번호")
        # order_id = item.get("productOrderId")
        if order_id and order_id not in order_ids:
            order_ids.add(order_id)
            filtered_data.append(item)

    output_file_path = "C:/python/combined_data.json"

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(filtered_data, output_file)

secondone()
