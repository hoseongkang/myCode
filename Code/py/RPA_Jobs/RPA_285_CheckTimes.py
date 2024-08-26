from datetime import datetime
import os 

def WhatTime_Folder(sTime):
    iHour = int(sTime)
    if iHour <= 10 and iHour > 6:
        sNewFolderName = '8'
    elif iHour <= 14 and iHour > 10:
        sNewFolderName = '12'
    elif iHour <= 23 and iHour > 14:
        sNewFolderName = '18'
    return sNewFolderName

def CreateFolder(arrList):
    i_sPath = arrList[0]
    i_sHour = WhatTime_Folder(arrList[1])
    sPath = os.path.join(i_sPath, i_sHour)
    if not os.path.exists(sPath):
        os.mkdir(sPath)
    return sPath

arrList = ['C:/RPADATA/RPA_285_SYP_1531/Input/2022-10-07', '11']