import requests

def runRPA(taskname):
    url = "http://sygrpa.samyang.com/v1/authentication"
    params = {
        "username": "syds_ad_runapi",
        "apiKey": "=1_3Z2VXvSdxyklHx^h0je9}uB0i@buALjsJlYJ`"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=params, headers=headers)
    print(response)
    if response.status_code == 200:
        response_json = response.json()
        if "token" in response_json:
            token = response_json["token"]
            print(token)
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
    
    url = "http://sygrpa.samyang.com/v1/schedule/automations"

    #####################################  monthly 실행 param
    # params = {
    #             "name": str(taskname),
    #             "fileId": int(first_id),
    #             "fileName": str(taskname),
    #             "status": "ACTIVE",
    #             "deviceIds": [
    #                 24
    #             ],
    #             "scheduleType": "MONTHLY",
    #             "monthlyDateRecurrence": {
    #                 "monthsOfYear": ['JAN', 'FEB', 'MAR'],
    #                 "dateOfMonth": 1
    #             },
    #             "timeZone": "Asia/Seoul",
    #             "startDate": "2024-05-19",
    #             "startTime": "10:00",
    #             "runAsUserIds": [
    #                 18
    #             ],
    #             "poolIds": [
    #                 2
    #             ],
    #             }

    
    #####################################  weekly 실행 param
    params = {
                "name": str(taskname),
                "fileId": int(first_id),
                "fileName": str(taskname),
                "status": "ACTIVE",
                "deviceIds": [
                    24
                ],
                "scheduleType": "WEEKLY",
                "weeklyRecurrence": {
                    "interval": 1,
                    "daysOfWeek":  ['MON', 'TUE']
                },
                "timeZone": "Asia/Seoul",
                "startDate": "2024-05-19",
                "startTime": "10:00",
                "repeatEnabled": False,
                "repeatOccurrence": {
                "runEvery": 2,
                "timeUnit": "HOURS",
                "endTime": "23:59"
                },
                "runAsUserIds": [
                    18
                ],
                "poolIds": [
                    2
                ],
                }
    
    
    #####################################  Daily 실행 param
    # params = {
    #             "name": str(taskname),
    #             "fileId": int(first_id),
    #             "fileName": str(taskname),
    #             "status": "ACTIVE",
    #             "deviceIds": [
    #                 24
    #             ],
    #             "scheduleType": "DAILY",
    #             "dailyRecurrence": {
    #                 "interval": 1
    #             },
    #             "timeZone": "Asia/Seoul",
    #             "startDate": "2024-05-19",
    #             "startTime": "10:00",
    #             "runAsUserIds": [
    #                 18
    #             ],
    #             "poolIds": [
    #                 2
    #             ],
    #             }
    
    #####################################단일 실행 param
    # params = {
    #             "name": str(taskname),
    #             "fileId": int(first_id),
    #             "fileName": str(taskname),
    #             "status": "ACTIVE",
    #             "deviceIds": [
    #                 24
    #             ],
    #             "scheduleType": "NONE",
    #             "timeZone": "Asia/Seoul",
    #             "startDate": "2024-05-19",
    #             "endDate": "2024-05-19",
    #             "startTime": "10:00",
    #             "runAsUserIds": [
    #                 18
    #             ],
    #             "poolIds": [
    #                 2
    #             ],
    #             }
    headers = {"X-Authorization": token,
                "Content-Type": "application/json"}
    
    response = requests.post(url, json=params, headers=headers)
    print(response)

runRPA("RPA_Test")