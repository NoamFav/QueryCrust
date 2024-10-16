@echo off

:: Start Flask backend
echo Starting Flask backend...
cd backend
start cmd /k "python app.py"

:: Start npm frontend
echo Starting npm frontend...
cd ..\frontend
start cmd /k "npm start"
