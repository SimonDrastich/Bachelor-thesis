set PATH=C:\Windows\System32
cd bin
start yarpserver.exe --write
::Sometimes yarpserver.exe need --write flag to work properly.
timeout /t 4
start iCub_SIM.exe
timeout /t 8
set QT_QPA_PLATFORM_PLUGIN_PATH=.
start yarpmotorgui.exe --name icubSim --from robotMotorGui.ini
timeout /t 2
start simFaceExpressions.exe
timeout /t 2
start emotionInterface.exe
timeout /t 2
yarp.exe connect /face/eyelids /icubSim/face/eyelids
yarp.exe connect /face/image/out /icubSim/texture/face
yarp.exe connect /emotion/out /icubSim/face/raw/in
cd ..
rem cd BallControll
rem set PATH=..\bin
rem start BallControll.exe
rem cd ..
