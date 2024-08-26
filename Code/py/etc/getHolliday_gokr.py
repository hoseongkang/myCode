import requests
import xml.etree.ElementTree as ET

# url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo'
url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?solYear=2024&solMonth=09&ServiceKey=y8kFjV9pFGF3hAdiNpSwDkKNzkLtaTdt4tjhn%2BQJLJhhdRpU2kJV9h74%2BtyhojgTD5iYyaZwZI0Aby%2FBNA5QAg%3D%3D'

# params ={'serviceKey' : 'y8kFjV9pFGF3hAdiNpSwDkKNzkLtaTdt4tjhn+QJLJhhdRpU2kJV9h74+tyhojgTD5iYyaZwZI0Aby/BNA5QAg==', 'pageNo' : '1', 'numOfRows' : '10', 'solYear' : '2024', 'solMonth' : '08' }

response = requests.get(url)
xml_string = response.content
root = ET.fromstring(xml_string)

locdates = [item.find('locdate').text for item in root.findall('.//item')]

locdate_str = ', '.join(locdates)

print(locdate_str)