cd iCubSim
start run-iCubSim.bat
timeout /t 45
cd ..
start run-renew.bat
timeout /t 8
start run-speak-lips.bat
timeout /t 2
start run-actions.bat
timeout /t 2
start run-main.bat
