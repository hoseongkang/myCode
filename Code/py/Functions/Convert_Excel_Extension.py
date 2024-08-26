import win32com.client as win32

def ConvertExcel(arList):
    strReportpath = arList[0]
    print(strReportpath)
    #strReportpath = strReportpath.replace(strReportpath[0:2],"")
    sPathShared = arList[1].replace(arList[1][0:2],"")
    print(sPathShared)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.DisplayAlerts = False
    excel.Visible = True
    wb = excel.Workbooks.Open(strReportpath)
    wb.DoNotPromptForConvert = True
    wb.CheckCompatibility = False
    wb.SaveAs("\\\\"+sPathShared+".xlsx", FileFormat = 51, ConflictResolution=2) 
    wb.Close()
    excel.Application.Quit()

arList = ["C:/RPADATA/RPA_240_SYC_1118/Output/2022-09-28/RPA_회계_홀딩스_판교_Q_202209.xlsm", "//130.1.22.33/a360data/RPA_240_SYC_1118/Output/2022-09-28/RPA_회계_홀딩스_판교_Q_202209"]

ConvertExcel(arList)