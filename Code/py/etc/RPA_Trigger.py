import requests
def runRPA(taskname):
    url = "http://sygrpa.samyang.com/v1/authentication"
    params = {
        "username": "syds_ad_runapi",
        "apiKey": "=1_3Z2VXvSdxyklHx^h0je9}uB0i@buALjsJlYJ`"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=params, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if "token" in response_json:
            token = response_json["token"]
            url = "http://sygrpa.samyang.com/v2/repository/workspaces/public/files/list"
            params = {"filter": {
                    "operator": "substring",
                    "field": "name",
                    "value": taskname
                    }
                    }
            headers = {"X-Authorization": token}

            response = requests.post(url, json=params, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                if "list" in response_json:
                    tasklist = response_json["list"]
                    first_id = tasklist[0]['id']
                    print("ID Values:", first_id)

    url = "http://sygrpa.samyang.com/v1/devices/runasusers/list"
    params = {
                "sort":[
                    {
                        "field":"username",
                        "direction":"asc"
                    }
                ],
                "filter":{},
                "fields":[],
                "page":{}
            }
    headers = {"X-Authorization": token}
    response = requests.post(url, json=params, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if "list" in response_json:
            devicelist = response_json["list"]
            id_values = []
            for item in devicelist:
                if "username" in item and any(keyword in item["username"] for keyword in ["ub01", "ub02", "ub05"]):
                    id_values.append(item['id'])

    url = "http://sygrpa.samyang.com/v2/devices/pools/list"
    params = {
                "filter": {
                    "operator": "substring",
                    "field": "name",
                    "value": "임시 트리거 봇"
                }
            }
    headers = {"X-Authorization": token}
    response = requests.post(url, json=params, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if "list" in response_json:
            devicepool = response_json["list"]
            first_devicepool = devicepool[0]['id']

    url = "http://sygrpa.samyang.com/v3/automations/deploy"
    params = {
                "fileId": first_id,
                "runAsUserIds": id_values,
                "poolIds": [
                    first_devicepool
                ],
                "numOfRunAsUsersToUse": 1
            }
    headers = {"X-Authorization": token}
    response = requests.post(url, json=params, headers=headers)

runRPA("RPA_Test")