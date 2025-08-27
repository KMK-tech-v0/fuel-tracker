@echo off
echo ========================================
echo  Starting Fuel Control System
echo ========================================
echo.
echo This will start both backend and frontend servers
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Starting backend server...
start "Fuel Control Backend" cmd /k "start_backend.bat"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting frontend server...
start "Fuel Control Frontend" cmd /k "start_frontend.bat"

echo.
echo ========================================
echo  System Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:8080
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause