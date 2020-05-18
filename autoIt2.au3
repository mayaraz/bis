#include <AutoItConstants.au3>

Main()

Func Main()
    Local $hWnd = WinGetHandle("[CLASS:Notepad]")
    WinSetOnTop($hWnd, "", $WINDOWS_ONTOP)
EndFunc
