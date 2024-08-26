Function GetPreviousMonthFirstDay(dateStr)
    Dim inputDate, prevMonthFirstDay
    Dim year, month, day

    inputDate = CDate(dateStr)

    year = Year(inputDate)
    month = Month(inputDate)
    day = Day(inputDate)

    If month = 1 Then
        prevMonthFirstDay = DateSerial(year - 1, 12, 1)
    Else
        prevMonthFirstDay = DateSerial(year, month - 1, 1)
    End If

    GetPreviousMonthFirstDay = Year(prevMonthFirstDay) & "-" & _
                               Right("0" & Month(prevMonthFirstDay), 2) & "-" & _
                               Right("0" & Day(prevMonthFirstDay), 2)
End Function

Dim inputDate
inputDate = "2024-08-09"
WScript.Echo GetPreviousMonthFirstDay(inputDate)
