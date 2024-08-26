# from dataclasses import replace
# from datetime import datetime
# import sys 
# import win32com.client
# import math
# import time

# def quarterYear(month):
#   return math.ceil( month / 3.0 )

# def Main(arLlist):
#         SapGuiAuto = win32com.client.GetObject("SAPGUI")
#         if not type(SapGuiAuto) == win32com.client.CDispatch:
#             return

#         application = SapGuiAuto.GetScriptingEngine
#         if not type(application) == win32com.client.CDispatch:
#             SapGuiAuto = None
#             return

#         connection = application.Children(0)
#         if not type(connection) == win32com.client.CDispatch:
#             application = None
#             SapGuiAuto = None
#             return

#         session = connection.Children(0)
#         if not type(session) == win32com.client.CDispatch:
#             connection = None
#             application = None
#             SapGuiAuto = None
#             return
        
#         sCompanyCode = arLlist[0]
#         sYear = arLlist[1]
#         sMonth = quarterYear(datetime.strptime(arLlist[3].replace('-','.'), '%Y.%m.%d').month)
#         sFrom = arLlist[2].replace('-','.')
#         sTo = arLlist[3].replace('-','.')

#         session.findById("wnd[0]/usr/ctxtP_BUKRS").text = sCompanyCode
#         session.findById("wnd[0]").sendVKey
#         session.findById("wnd[0]/usr/txtP_VYEAR").text = sYear
#         session.findById("wnd[0]/usr/ctxtP_VQUAR").text = sMonth #Quarter

#         session.findById("wnd[0]/usr/ctxtS_BLDAT-LOW").text = sFrom
#         session.findById("wnd[0]/usr/ctxtS_BLDAT-HIGH").text = sTo
#         session.findById("wnd[0]/usr/ctxtS_BUDAT-LOW").text = sFrom
#         session.findById("wnd[0]/usr/ctxtS_BUDAT-HIGH").text = sTo

#         session.findById("wnd[0]/usr/ctxtS_MWSKZ-LOW").text = "A7" #Fixed

#         session.findById("wnd[0]/tbar[1]/btn[8]").press()
        
#         session = None
#         connection = None
#         application = None
#         SapGuiAuto = None

# arLlist = ['1100', '2022', '2022-07-01', '2022-09-30']

# Main(arLlist)





from datetime import datetime, timedelta

# 입력 받은 날짜 문자열
input_date = "2024-05-16"

# 문자열을 datetime 형식으로 변환
date_obj = datetime.strptime(input_date, "%Y-%m-%d")

# 하루를 더함
new_date_obj = date_obj + timedelta(days=1)

# 다시 문자열로 변환
new_date = new_date_obj.strftime("%Y-%m-%d")

print("하루 더한 날짜:", new_date)

