from datetime import datetime
from datetime import timedelta
import os

def Between(arrList):
    
    iHour = int(arrList[0])
    sDatetime = arrList[1]
    sDate_Now = datetime.strptime(arrList[2], "%Y.%m.%d")
    CompareDate = datetime.strptime(sDatetime, "%Y.%m.%d %H:%M:%S")
    if iHour <= 10 and iHour > 6:
        dFrom = (sDate_Now - timedelta(days=1)).strftime("%Y.%m.%d 18:00:00")
        dTo = sDate_Now.strftime("%Y.%m.%d 08:00:00")
    elif iHour <= 14 and iHour > 10:
        dFrom = sDate_Now.strftime("%Y.%m.%d 08:00:00")
        dTo = sDate_Now.strftime("%Y.%m.%d 12:00:00")
    elif iHour <= 23 and iHour > 14:
        dFrom = sDate_Now.strftime("%Y.%m.%d 12:00:00")
        dTo = sDate_Now.strftime("%Y.%m.%d 18:00:00")
    bCheckDate = datetime.strptime(dFrom, "%Y.%m.%d %H:%M:%S") < CompareDate and CompareDate < datetime.strptime(dTo, "%Y.%m.%d %H:%M:%S")
    return "True" if bCheckDate == True else "False"

#testarr = ['07', '2022.11.22 07:38:48', '2022.11.22']
testarr = ['8', '2024.01.31 07:00:31', '2024.01.31']

print(Between(testarr))

# def mkdir_path(spath):
#     os.mkdir(spath)

# mkdir_path("C:/Program Files/Automation Anywhere/Bot Agent/8")

'''
from datetime import datetime
from datetime import timedelta

def Between(arrList):
    
    iHour = int(arrList[0])
    sDatetime = arrList[1]
    CompareDate = datetime.strptime(sDatetime, "%Y.%m.%d %H:%M:%S")
    if iHour <= 10 and iHour > 6:
        dFrom = (datetime.now() - timedelta(days=1)).strftime("%Y.%m.%d 18:00:00")
        dTo = datetime.now().strftime("%Y.%m.%d 08:00:00")
    elif iHour <= 14 and iHour > 10:
        dFrom = datetime.now().strftime("%Y.%m.%d 08:00:00")
        dTo = datetime.now().strftime("%Y.%m.%d 12:00:00")
    elif iHour <= 23 and iHour > 14:
        dFrom = datetime.now().strftime("%Y.%m.%d 12:00:00")
        dTo = datetime.now().strftime("%Y.%m.%d 18:00:00")
    bCheckDate = datetime.strptime(dFrom, "%Y.%m.%d %H:%M:%S") < CompareDate and CompareDate < datetime.strptime(dTo, "%Y.%m.%d %H:%M:%S")
    return "True" if bCheckDate == True else "False"

testarr = ['10', '2022.10.06 12:07:12']

print(Between(testarr))
'''