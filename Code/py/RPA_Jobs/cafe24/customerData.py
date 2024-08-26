import csv
import requests

def get_json_data(api_url, headers):
    response = requests.get(api_url, headers=headers)
    return response.json()

def json_to_csv(json_data, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)

        # Get headers from JSON data
        headers = set()
        for item in json_data:
            if isinstance(json_data[item], list):
                for sub_item in json_data[item]:
                    headers.update(sub_item.keys())
            else:
                headers.update(json_data[item].keys())

        # Write headers to CSV file
        writer.writerow(headers)

        # Write data to CSV file
        for item in json_data:
            if isinstance(json_data[item], list):
                for sub_item in json_data[item]:
                    row = []
                    for header in headers:
                        row.append(sub_item.get(header, ''))
                    writer.writerow(row)
                    print(item, sub_item)  # 노드 출력
            else:
                row = []
                for header in headers:
                    row.append(json_data[item].get(header, ''))
                writer.writerow(row)
                print(item, json_data[item])  # 노드 출력

# API URL 및 헤더 정보
api_url = "https://serveq.cafe24api.com/api/v2/admin/customersprivacy/3933833097@n"
bearer_token = "VHoXFYwgNBeA9qADGsNwJD"
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}


# JSON 데이터 가져오기
json_data = get_json_data(api_url, headers)

# CSV 파일로 변환
json_to_csv(json_data, 'output.csv')
