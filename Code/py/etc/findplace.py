import json
import urllib.request
import urllib.parse

query = '바스락카페앤펍'
client_id = "Y8NErU46MCQ2Oq0lI4Xu"
client_secret = "JRQrbocncG"

encText = urllib.parse.quote(query)
url = "https://openapi.naver.com/v1/search/local.json?query=" + str(encText)

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    result = json.loads(response_body)
    print(result)
else:
    print("Error Code:" + rescode)