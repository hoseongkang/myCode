import os

strPath = 'C:/RPADATA/RPA_240_SYC_1118/Input/2022-09-22/패키징_본사_2022-07-01~2022-07-15.xlsx'
#sPath = 'C:/RPADATA/RPA_240_SYC_1118/Input/2022-09-19/홀딩스_판교_2022-08-31~2022-08-31.xlsx'

def Check_Path(in_sPath):  
    sPath = in_sPath.replace('\\', '/')
    isExist = os.path.exists(sPath)
    return isExist

print(Check_Path(strPath))