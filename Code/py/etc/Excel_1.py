from openpyxl import workbook

wb = workbook()
ws = wb.activate
ws.title = 'Hoseong'
wb.save('hskang.xlsx')
wb.close