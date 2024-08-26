from ast import Return
from operator import mod
import pandas as pd
import math
import time
from datetime import datetime
from dateutil.relativedelta import *

def GetDateTime_M(strDate):
    in_strDate = datetime.strptime(strDate, '%Y-%m-%d')
    if in_strDate.day < 15: 
        str_JobDay = in_strDate + pd.DateOffset(months=0)
        sLastDate = datetime(str_JobDay.year, str_JobDay.month, 1) + relativedelta(seconds=-1)
    else:
        str_JobDay = in_strDate
        NextMonth = datetime(str_JobDay.year, str_JobDay.month, 1) + relativedelta(months=1)
        sLastDate = datetime(NextMonth.year, NextMonth.month, 1) + relativedelta(seconds=-1)
    #sLastDate = datetime(str_JobDay.year, str_JobDay.month, 1) + relativedelta(seconds=-1)
    new_Row_1 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-01')], 'To' : [sLastDate.strftime('%Y-%m-15')]})
    #new_Row_2 = pd.DataFrame({'From' : sLastDate.strftime('%Y-%m-16'), 'To' : [sLastDate.strftime('%Y-%m-{}'.format(sLastDate.day))]})
    dfReult = pd.concat([new_Row_1]) #, new_Row_2
    
    if sLastDate.day > 30:
        new_Row_2 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-16')], 'To' : [sLastDate.strftime('%Y-%m-30')]})
        new_Row_3 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-31')], 'To' : [sLastDate.strftime('%Y-%m-31')]})
        dfReult = pd.concat([new_Row_1, new_Row_2, new_Row_3])
    else:
        new_Row_2 = pd.DataFrame({'From' : sLastDate.strftime('%Y-%m-16'), 'To' : [sLastDate.strftime('%Y-%m-{}'.format(sLastDate.day))]})
        dfReult = pd.concat([new_Row_1, new_Row_2])

    return dfReult

print(GetDateTime_M('2022-08-12'))