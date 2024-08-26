Set objExcel = CreateObject("Excel.Application")
Set objWorkbook = objExcel.Workbooks.Open("C:\RPADATA\RPA_240_SYC_1118\Output\2022-09-27\asd.xlsm")

objExcel.Application.Visible = True
'objExcel.Workbooks.Add

'objExcel.Application.Run "Report0165.xlsm"
'objWorkbook.SaveAs Filename:="C:\RPADATA\RPA_240_SYC_1118\Output\2022-09-27\asd.xlsx", FileFormat = 51
'objWorkbook.Close saveChanges:=True
objExcel.ActiveWorkbook.SaveAs Filename:="C:\RPADATA\RPA_240_SYC_1118\Output\2022-09-27\asd.xlsx", FileFormat:=51

objExcel.Application.Quit