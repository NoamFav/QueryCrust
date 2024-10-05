@echo off

:: Start Flask backend
echo Starting Flask backend...
cd backend
set FLASK_APP=app.py  :: Replace with your Flask entry point
set FLASK_ENV=development  :: Or 'production'
start cmd /k "flask run"

:: Start npm frontend
echo Starting npm frontend...
cd ..\frontend
start cmd /k "npm start"
