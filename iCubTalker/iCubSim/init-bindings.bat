echo off

for /F "tokens=* USEBACKQ" %%F in (`python --version`) do (
set verbase=%%F
)

for /F "tokens=2,3 delims=. " %%a in ("%verbase%") do (
   set id=%%a
   set subid=%%b
)
set ver=%id%%subid%
echo Python %ver% found

echo on
copy /Y bindings\python%ver%\_yarp.pyd ..
copy /Y bindings\python%ver%\yarp.py ..

@echo.
@echo bindings initialized
@pause
