from datetime import datetime
from dateutil.relativedelta import *

def CheckTodo(sToday):
    dString = datetime.strptime(sToday, '%Y-%m-%d')
    NextMonth = datetime(dString.year, dString.month, 1) + relativedelta(months=1)
    sLastday = datetime(NextMonth.year, NextMonth.month, 1) + relativedelta(seconds=-1)
    sResult = sLastday - datetime.strptime(sToday,'%Y-%m-%d')

    if sResult.days < 4 or dString.day < 4:
        strCheck = 'Y'
    else:
        strCheck = 'N'
    return strCheck