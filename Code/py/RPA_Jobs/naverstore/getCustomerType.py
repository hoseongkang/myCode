import requests

def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return None

def main():
    api_url = "http://127.0.0.1:8000/classify_address/칼국수/!1samyang/"
    data = fetch_data_from_api(api_url)
    if data:
        bChk = data.get("classification", "B2B")
    else:
        bChk = "B2B"
    print(bChk)
if __name__ == "__main__":
    main()