import pandas as pd
import os
import psutil

for proc in psutil.process_iter():
    if proc.name() == "excel.exe":
        proc.kill()

#sPath = "C:/Users/syc720584/Desktop/RPA/etc"
sPath = "C:\\Users\\syc720584\\Desktop\\Code\\py\\Test.xlsx"
#print(sPath)
#sPath = os.path.join(sPath, "CR_DB.csv")
df = pd.read_excel(sPath, engine='openpyxl')
