Function FormatNumber(inputString)
    parts = Split(inputString, "/")
  	quantity = parts(0)
    price = parts(1)
  	total = quantity * price

    numberString = CStr(total)
  	length = Len(numberString)

  	For i = length To 1 Step -1
        formattedNumber = Mid(numberString, i, 1) & formattedNumber
        If (length - i + 1) Mod 3 = 0 And i <> 1 Then
            formattedNumber = "." & formattedNumber
        End If
    Next
    FormatNumber = formattedNumber
End Function

msgbox FormatNumber("5/50000")