taskkill /IM simFaceExpressions.exe
taskkill /IM yarpmotorgui.exe
taskkill /IM iCub_SIM.exe
taskkill /IM yarpserver.exe
taskkill /IM emotionInterface.exe
taskkill /IM python.exe

call getCmdPID
set "current_pid=%errorlevel%"

for /f "skip=3 tokens=2 delims= " %%a in ('tasklist /fi "imagename eq cmd.exe"') do (
    if "%%a" neq "%current_pid%" (
        TASKKILL /PID %%a /f >nul 2>nul
    )
)
