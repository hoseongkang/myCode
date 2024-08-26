from datetime import datetime
import math
import time

def quarterYear(month):
  return math.ceil( month / 3.0 )

def getMonth(in_Date):
    in_strDate = datetime.strptime(in_Date, '%Y-%m-%d')
    sMonth = in_strDate.month
    return sMonth # 현재 월만 반환

def Run_Code(arList):
    out_List = [getMonth(arList),quarterYear(getMonth(arList))]
    out_Str = '{0}/{1}'.format(out_List[0], out_List[1])
    return out_Str

print('2022-09-22'.replace('-','.'))

#print("이번 달은 : {}분기 입니다.".format(quarterYear(getMonth('2022-09-22'))))

