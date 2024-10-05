@echo off

:: Stop Flask process
echo Stopping Flask backend...
taskkill /F /IM python.exe  :: Assuming Flask is running with python.exe

:: Stop npm process
echo Stopping npm frontend...
taskkill /F /IM node.exe  :: Assuming npm is running with node.exe
