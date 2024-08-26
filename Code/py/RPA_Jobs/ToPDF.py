import base64
from io import BytesIO
from PIL import Image
import pyodbc


server = '130.1.22.33,2433'
database = 'rpaportal_dev'
username = 'sa'
password = '@sygrpa22!'

conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = conn.cursor()

query = f"SELECT [PRSN_PIC_BYTE] FROM [INPL_DB].[OUTBOUND].[dbo].[VIEW_ADSYNC_PHOTO] where EMPNO = 'syc223351';"
cursor.execute(query)

rows = cursor.fetchall()
for row in rows:
    byte_data = row[0]

hex_string = '0x' + byte_data.hex().upper()

def hex_string_to_base64_image(hex_string):
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]
    image_bytes = bytes.fromhex(hex_string)
    
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string

base64_image = hex_string_to_base64_image(hex_string)
print('Base64 String:', base64_image)