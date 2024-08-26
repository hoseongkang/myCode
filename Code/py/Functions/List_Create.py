import sys 
import win32com.client

def item_SearchDate(sSearchMonth, sSearchQuarter, Quarter_or_Month):
    if Quarter_or_Month == 'M':
        o_str = sSearchMonth
    else:
        o_str = sSearchQuarter
    return o_str

def Main(arList):
        #LOptions = [arList[0], arList[1], arList[2], arList[3], arList[4], item_SearchDate(arList[4], arList[5], arList[6]), arList[6]]
        #LOptions = List_Option('1500', '2022', '2022.09.01', '2022.09.31', 9, 7, 'M')
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return

        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return

        connection = application.Children(0)
        if not type(connection) == win32com.client.CDispatch:
            application = None
            SapGuiAuto = None
            return

        session = connection.Children(0)
        if not type(session) == win32com.client.CDispatch:
            connection = None
            application = None
            SapGuiAuto = None
            return

        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/usr/ctxtP_BUKRS").Text = arList[0]
        session.findById("wnd[0]").sendVKey
        session.findById("wnd[0]/usr/txtP_VYEAR").Text = arList[1]

        if arList[6] == 'M':
            session.findById("wnd[0]/usr/txtP_VMON").Text = arList[4]
        else:
            session.findById("wnd[0]/usr/ctxtP_VQUAR").Text = arList[5]
    
        session.findById("wnd[0]/usr/ctxtS_BLDAT-LOW").Text = arList[2] #From
        session.findById("wnd[0]/usr/ctxtS_BLDAT-HIGH").Text = arList[3] #To
        session.findById("wnd[0]/usr/chkP_ALL").Selected = True
        session.findById("wnd[0]/usr/chkP_A6").selected = False
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        session = None
        connection = None
        application = None
        SapGuiAuto = None

'''
iarList = ['1500', '2022', '2022.09.01', '2022.09.30', '9', '7', 'M']
Main(iarList)
'''