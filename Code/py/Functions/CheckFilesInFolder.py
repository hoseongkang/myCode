import os

def CheckFileExist(arList):
    arrFolder = os.listdir(arList[0])
    arrFilterd = list(filter(lambda k: 'xlsx' in k and arList[1] in k, arrFolder)) 
    return len(arrFilterd)
#print(arrFilterd)
#for sfile in arrFilterd:
#    print(sfile)

arList = ['C:/RPADATA/RPA_240_SYC_1118/Input/2022-09-22', '이노켐']

print(CheckFileExist(arList))


#$io_strWorkingPathLocal$/Input/$io_strTodayDate$/$io_strCompany$_회계자료.xlsx