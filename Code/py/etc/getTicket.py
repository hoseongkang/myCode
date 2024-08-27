import requests
import pyodbc
import time


DatabaseConnection = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': '*****',
        'USER': 'LoginInfo',
        'PASSWORD': '*****',
        'HOST': 'syc-app02.sy.com',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

def sso_legacy():
    ticket = ""
    
    try:
        connection_details = DatabaseConnection['default']
        connection_string = (
            'DRIVER={' + connection_details['OPTIONS']['driver'] + '};'
            'SERVER=' + connection_details['HOST'] + ';'
            'DATABASE=' + connection_details['NAME'] + ';'
            'UID=' + connection_details['USER'] + ';'
            'PWD=' + connection_details['PASSWORD'] + ';'
        )
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        cursor.execute("{call up_Ticket_Select()}")

        row = cursor.fetchone()
        print(row)
        if row:
            ticket = row.TicketID
        connection.commit()
    except pyodbc.Error as e:
        print("Database error:", e)
    finally:
        cursor.close()
        connection.close()    
    return ticket

def sso_get_user_id(ticket):
    time.sleep(1)
    user_id = ""
    connection = None
    cursor = None

    try:
        connection_details = DatabaseConnection['default']
        connection_string = (
            'DRIVER={' + connection_details['OPTIONS']['driver'] + '};'
            'SERVER=' + connection_details['HOST'] + ';'
            'DATABASE=' + connection_details['NAME'] + ';'
            'UID=' + connection_details['USER'] + ';'
            'PWD=' + connection_details['PASSWORD'] + ';'
        )
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("{call up_LoginInfo_Select(?)}", (ticket,))
        row = cursor.fetchone()
        if row:
            user_id = row.EmpCode
            print(user_id)
        connection.commit()
    except pyodbc.Error as e:
        print("Database error:", e)
    finally:
        cursor.close()
        connection.close()
    return user_id

# ticket = sso_legacy()

ticket = sso_legacy()
url = "http://contract.samyang.com:9696/SetInfo.aspx?TicketID=" + ticket
response = requests.get(url)

# sso_get_user_id(ticket)
