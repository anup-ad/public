; Admin Control Center
; Version = 1.0
; Author = Anup Adhikari
; Unshared Secret Info -  
;   1. Root
;   2. iLO
;   3. Drac
ahksystem = C:\Users\aadhikari003\AppData\Local\ahkSystem\bin
FileReadLine, DefIloPw, %ahksystem%\init1, 1 



Gui, Font, S16, Times New Roman
Gui, Add, Text, x210 y18 w488 h41 +Center, ADMIN CONTROL CENTER
Gui, Font, S9, Verdana
Gui, Add, Button, x60 y89 w200 h40 , HP iLO Remote Console
Gui, Add, Button, x60 y179 w200 h40 , SSH to Jump Server
Gui, Add, Button, x60 y259 w200 h40 , Multiple SSHs to Jump Server
Gui, Add, Button, x60 y349 w200 h40 , RDP to Scottsdale Lab
Gui, Add, Button, x345 y89 w200 h40 , Button5
Gui, Add, Button, x620 y89 w200 h40 , Edit Admin Command Center Script
Gui, Add, Button, x620 y179 w200 h40 , Kill all Running PuTTY Sessions
Gui, Add, Button, x620 y259 w200 h40 , Button8
Gui, Add, Button, x620 y349 w200 h40 , Button9
Gui, Add, Button, x345 y349 w200 h40 , Test Button
Gui, Add, Edit, x345 y199 w200 h30 vUname, %USERNAME%
Gui, Add, Button, x365 y439 w160 h30 , EXIT
;Gui, Add, Text, 
; Generated using SmartGUI Creator 4.0
Gui, Show, x354 y257 h508 w895, Admin Control Center v1.0
;Gui, Show, xCenter yCenter, ADMIN CONTROL CENTER
Return

ButtonHPiLORemoteConsole:
 Gui, Destroy
 Gui, Font, S9, Verdana
 Gui, Add, Edit, x182 y69 w140 h20 vUserName, Administrator
 Gui, Add, Edit, x182 y109 w140 h20 +Password vPassWord, %DefIloPw%
 Gui, Add, Edit, x182 y29 w140 h20 vHostName, %clipboard%
 Gui, Add, Button, x122 y139 w100 h30 , GO
 Gui, Add, Text, x42 y29 w120 h20 , Hostname
 Gui, Add, Text, x42 y69 w120 h20 , Username
 Gui, Add, Text, x42 y109 w120 h20 , Password
 ; Generated using SmartGUI Creator 4.0
 Gui, Show, x679 y397 h178 w344, HP iLO Details
 Return

 ButtonGO:
 GUI, Submit, NoHide
 Run, C:\Program Files (x86)\Hewlett-Packard\HP iLO Integrated Remote Console\HPLOCONS.exe -addr %HostName% -name %UserName% -password %PassWord%
 ;MsgBox, %Uname%
 ExitApp
 Return
ExitApp  

ButtonTestButton:
GUI, Submit, NoHide
MsgBox, , TestButton, Nothing Right Now
ExitApp
Return

ButtonKillallRunningPuTTYSessions:
GUI, Submit, NoHide
Run, taskkill /F /IM "putty.exe"
ExitApp
Return

ButtonSSHtoJumpServer:
Run, C:\Program Files\PuTTY\putty.exe -load "Jump Box"
ExitApp
return

ButtonMultipleSSHstoJumpServer:
 Gui, Destroy
 Gui, Font, S9, Verdana
 Gui, Add, Text, x22 y9 w185 h20 , Number of Windows (Max. 4)
 Gui, Add, Edit, x220 y9 w40 h20 vSpawn, 2
 Gui, Add, Button, x102 y39 w100 h30 , Spawn
 ; Generated using SmartGUI Creator 4.0
 Gui, Show, xCenter yCenter h78 w290, How many?
 Return
 ButtonSpawn:
  GUI, Submit, NoHide
  if (Spawn > 4) {
    MsgBox, Max Number Exceeded
    ;ExitApp
	}
  else {
    Loop, %Spawn%
	{
    Run, C:\Program Files\PuTTY\putty.exe -load "Jump Box"
	}
	ExitApp
  }
  Return

ButtonEditAdminCommandCenterScript:
 Run, notepad++.exe C:\Users\aadhikari003\Documents\Scripts\GUI\admin_control_center.ahk
 ExitApp
 Return

ButtonRDPtoScottsdaleLab:
 Run, mstsc C:\Users\aadhikari003\Documents\Scripts\DHLab.rdp
 ExitApp
 Return

ButtonExit:
ExitApp

GuiClose:
ExitApp