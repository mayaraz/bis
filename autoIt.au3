Const $PROG = "calc"
Const $PASS = "ch@11@"
# hello world
$pass1 = InputBox("Enter the password", "Password", "", "*")

If $pass1 == $PASS Then
	RunProgram()
Else
	# prints error message indicates password is wrong
	MsgBox(0, "Error", "Incorrect password! ")
EndIf

Func RunProgram()
	Run($PROG)
EndFunc


