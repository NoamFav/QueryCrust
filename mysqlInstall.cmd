@echo off
setlocal

:: Set the MySQL installer file name
set MYSQL_INSTALLER=mysql-installer-web-community-8.0.30.0.msi

:: Download MySQL Installer using PowerShell
echo Downloading MySQL Installer...
powershell -Command "Invoke-WebRequest -Uri 'https://dev.mysql.com/get/Downloads/MySQLInstaller/%MYSQL_INSTALLER%' -OutFile '%MYSQL_INSTALLER%'"

:: Run the MySQL installer
echo Running the MySQL installer...
start /wait msiexec /i %MYSQL_INSTALLER% /qn

:: Optionally, you can add commands to configure MySQL after installation

echo MySQL has been installed.
endlocal
