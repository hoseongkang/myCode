from ast import Return
from operator import mod
import pandas as pd
import math
import time
from datetime import datetime
from dateutil.relativedelta import *

def GetDateTime_M(strDate):
    in_strDate = datetime.strptime(strDate, '%Y-%m-%d')
    if in_strDate.day < 15: #15?ùº Í∏∞Ï???úºÎ°? ?†Ñ?õîÍ≥? ?ãπ?õî Í∏∞Ï?? ?ûë?óÖ ?Ç†Ïß? ?Ñ†?†ï
        str_JobDay = in_strDate + pd.DateOffset(months=0)
        sLastDate = datetime(str_JobDay.year, str_JobDay.month, 1) + relativedelta(seconds=-1)
    else:
        str_JobDay = in_strDate
        NextMonth = datetime(str_JobDay.year, str_JobDay.month, 1) + relativedelta(months=1)
        sLastDate = datetime(NextMonth.year, NextMonth.month, 1) + relativedelta(seconds=-1)
    #sLastDate = datetime(str_JobDay.year, str_JobDay.month, 1) + relativedelta(seconds=-1)
    new_Row_1 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-01')], 'To' : [sLastDate.strftime('%Y-%m-15')]})
    
    if sLastDate.day > 30:
        new_Row_2 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-16')], 'To' : [sLastDate.strftime('%Y-%m-30')]})
        new_Row_3 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-31')], 'To' : [sLastDate.strftime('%Y-%m-31')]})
        dfReult = pd.concat([new_Row_1, new_Row_2, new_Row_3])
    else:
        new_Row_2 = pd.DataFrame({'From' : sLastDate.strftime('%Y-%m-16'), 'To' : [sLastDate.strftime('%Y-%m-{}'.format(sLastDate.day))]})
        dfReult = pd.concat([new_Row_1, new_Row_2])
    return dfReult
    
def Create_dfMonth(iMonth):
        dString = datetime.strptime(iMonth, '%Y-%m-%d')
        NextMonth = datetime(dString.year, dString.month, 1) + relativedelta(months=1)
        sLastDate = datetime(NextMonth.year, NextMonth.month, 1) + relativedelta(seconds=-1)
        new_Row_1 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-01')], 'To' : [sLastDate.strftime('%Y-%m-15')]})

        if sLastDate.day > 30:
            new_Row_2 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-16')], 'To' : [sLastDate.strftime('%Y-%m-30')]})
            new_Row_3 = pd.DataFrame({'From' : [sLastDate.strftime('%Y-%m-31')], 'To' : [sLastDate.strftime('%Y-%m-31')]})
            dfReult = pd.concat([new_Row_1, new_Row_2, new_Row_3])
        else:
            new_Row_2 = pd.DataFrame({'From' : sLastDate.strftime('%Y-%m-16'), 'To' : [sLastDate.strftime('%Y-%m-{}'.format(sLastDate.day))]})
            dfReult = pd.concat([new_Row_1, new_Row_2])
        return dfReult

def GetDateTime_Q(strDate):
    in_strDate = datetime.strptime(strDate, '%Y-%m-%d') 
    dfResult_Output = pd.DataFrame(index=range(0,0), columns={'From', 'To'})

    if mod(in_strDate.month ,3) == 1:
        if in_strDate.day < 15:
            lMonth = [
                        datetime.strftime(in_strDate + pd.DateOffset(months=-1),'%Y-%m-01'), 
                        datetime.strftime(in_strDate + pd.DateOffset(months=-2),'%Y-%m-01'), 
                        datetime.strftime(in_strDate + pd.DateOffset(months=-3),'%Y-%m-01')
                    ]
            for imonth in lMonth:
                dfTemp = Create_dfMonth(imonth)
                dfResult_Output = pd.concat([dfTemp, dfResult_Output])
        else: #Î∂ÑÍ∏∞?ùò Ï≤? ?ã¨?ù¥Ïß?Îß? ÎßêÏùº?ù∏ Í≤ΩÏö∞ ?ï¥?ãπ ?õîÎß? Dataframe Í∞?Í≥?
            dfResult_Output = Create_dfMonth(datetime.strftime(in_strDate + pd.DateOffset(months=0),'%Y-%m-01'))

    elif mod(in_strDate.month ,3) == 2:
        if in_strDate.day < 15:
            dfResult_Output = Create_dfMonth(datetime.strftime(in_strDate + pd.DateOffset(months=-1),'%Y-%m-01'))
        else :
            lMonth = [
                        datetime.strftime(in_strDate + pd.DateOffset(months=0),'%Y-%m-01'), 
                        datetime.strftime(in_strDate + pd.DateOffset(months=-1),'%Y-%m-01')
                    ]
            for imonth in lMonth:
                dfTemp = Create_dfMonth(imonth)
                dfResult_Output = pd.concat([dfTemp, dfResult_Output])
                
    elif mod(in_strDate.month ,3) == 0:
        if in_strDate.day < 15:
            lMonth = [
                        datetime.strftime(in_strDate + pd.DateOffset(months=-1),'%Y-%m-01'), 
                        datetime.strftime(in_strDate + pd.DateOffset(months=-2),'%Y-%m-01')
                    ]
        else:
            lMonth = [
                        datetime.strftime(in_strDate + pd.DateOffset(months=0),'%Y-%m-01'), 
                        datetime.strftime(in_strDate + pd.DateOffset(months=-1),'%Y-%m-01'),
                        datetime.strftime(in_strDate + pd.DateOffset(months=-2),'%Y-%m-01')
                    ]
        for imonth in lMonth:
            dfTemp = Create_dfMonth(imonth)
            dfResult_Output = pd.concat([dfTemp, dfResult_Output])

    return dfResult_Output

def Run_Code(list_test):
    #in_strDate = datetime.strptime(strDate, '%Y-%m-%d') 
    if list_test[1] == 'M':
        OutDataFrame = GetDateTime_M(list_test[0])
    else:
        OutDataFrame = GetDateTime_Q(list_test[0])
    list_result = []
    for index, drtemp in OutDataFrame.iterrows():
        list_result.append('{0}/{1}'.format(drtemp['From'], drtemp['To']))
    return list_result

asd = ['2022-09-10', 'M']

dfResult = Run_Code(asd)

print(dfResult)
'''
list_result = []

for index, drtemp in dfResult.iterrows():
    list_result.append('{0}/{1}'.format(drtemp['From'], drtemp['To']))

print(list_result)'''
#list_test = ['2022-11-01', 'Q']
#asd = Run_Code(list_test)
#print(asd)

#strDate = '2022-05-20'
#in_strDate = datetime.strptime(strDate, '%Y-%m-%d') 
#dfResult = GetDateTime_Q(strDate)

#print(dfResult)

'''
#Date_Str = datetime.now() + pd.DateOffset(months=-1)

def GetDateTime_Q():
    strInt = 1

#dtResult_M = GetDateTime_M(dfHeader)


testArg = 'Q'

if testArg == 'M':
    List_Result = GetDateTime_M()
else:
    List_Result = GetDateTime_Q()

test_List = ['Q', '2022-09-03']

def quarterYear(month):
  return math.ceil( month / 3.0 )

def currentMonth():
    if datetime.today().day > 15:
        now = time.localtime()
        return now.tm_mon - 1 # ?òÑ?û¨ ?õîÎß? Î∞òÌôò

#print("?ù¥Î≤? ?ã¨??? : {}Î∂ÑÍ∏∞ ?ûÖ?ãà?ã§.".format(quarterYear(currentMonth())))
#print(datetime.today().day)
print(time.localtime().tm_mon -1)

#print(dfResult_Output)

for imonth in ['2022-03-01', '2022-02-01', '2022-01-01']:#,'2022-03-01']:
    dfTemp = Create_dfMonth(imonth)
    dfResult_Output = pd.concat([dfTemp, dfResult_Output])

#dfResult_Output['From'] =pd.to_datetime(dfResult_Output.From)
#dfResult_Output.sort_values(by='From', ascending=True)

'''