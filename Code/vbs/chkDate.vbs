Function FindFirstMonday(referenceDateStr)
    Dim referenceDate
    referenceDate = CDate(referenceDateStr)

    Dim firstDayOfWeek
    firstDayOfWeek = referenceDate - (Weekday(referenceDate, vbMonday) - 1)

    Dim firstMonday
    If Weekday(firstDayOfWeek, vbMonday) = 1 Then
        firstMonday = firstDayOfWeek
    Else
        firstMonday = firstDayOfWeek + (8 - Weekday(firstDayOfWeek, vbMonday))
    End If

    FindFirstMonday = FormatDateTime(firstMonday, 2)
End Function

Dim firstMonday
firstMonday = FindFirstMonday("2024-02-13")

WScript.Echo "first Mon " & firstMonday
