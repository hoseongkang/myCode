from asyncio.windows_events import NULL
from multiprocessing.util import is_exiting
import sys 
import win32com.client
  
def Main():
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

        #print(session.findById("wnd[0]/tbar[1]/btn[33]", False))

        print(session.findById("wnd[0]/sbar").Text)

        session = None
        connection = None
        application = None
        SapGuiAuto = None

Main()