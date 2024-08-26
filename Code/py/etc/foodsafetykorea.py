import os
import requests
import xml.etree.ElementTree as ET
import json

def fetch_data_from_api():
    base_url = "http://openapi.foodsafetykorea.go.kr/api/0b3a06962bed45a9b42f/I0300/xml/"
    year = "2019"  # This should match the expected format and be a valid year
    start_index = 1
    end_index = 1000

    file_exists = os.path.isfile('api_data.json')

    with open('api_data.json', 'a', encoding='utf-8') as f:
        if not file_exists:
            f.write('[')  # Start the list in the JSON file
        else:
            f.seek(0, os.SEEK_END)  # Move to the end of the file
            f.seek(f.tell() - 1, os.SEEK_SET)  # Move back one character
            f.truncate()  # Remove the trailing ']'

    first_entry = not file_exists  # Adjust first_entry based on file existence

    while True:
        url = f"{base_url}{start_index}/{end_index}/EVL_YR={year}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch data")
            break

        root = ET.fromstring(response.content)
        result_code = root.find(".//CODE").text
        result_msg = root.find(".//MSG").text

        if result_code != "INFO-000" or result_msg != "정상처리되었습니다.":
            print("No more data available or error occurred")
            break

        rows = root.findall(".//row")
        for row in rows:
            data = {
                "SITE_ADDR": row.find("SITE_ADDR").text,
                "PRDLST_REPORT_NO": row.find("PRDLST_REPORT_NO").text,
                "EVL_YR": row.find("EVL_YR").text,
                "LCNS_NO": row.find("LCNS_NO").text,
                "PRDLST_NM": row.find("PRDLST_NM").text,
                "PRDCTN_QY": row.find("PRDCTN_QY").text,
                "BSSH_NM": row.find("BSSH_NM").text,
                "H_ITEM_NM": row.find("H_ITEM_NM").text,
                "FYER_PRDCTN_ABRT_QY": row.find("FYER_PRDCTN_ABRT_QY").text
            }
            with open('api_data.json', 'a', encoding='utf-8') as f:
                if not first_entry:
                    f.write(',')
                json.dump(data, f, ensure_ascii=False)
                first_entry = False

        print(str(start_index) + "~" + str(end_index))

        start_index += 1000
        end_index += 1000

    with open('api_data.json', 'a', encoding='utf-8') as f:
        f.write(']')

    print("Data fetching complete")

fetch_data_from_api()
