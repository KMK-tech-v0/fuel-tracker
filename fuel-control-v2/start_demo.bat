@echo off
echo ========================================
echo  Starting Fuel Control System - DEMO
echo ========================================
echo.
echo This demo runs without requiring a database
echo Perfect for immediate viewing and testing
echo.
echo Starting demo backend server...
start "Fuel Control Demo Backend" cmd /k "cd backend && python demo_app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting frontend server...
start "Fuel Control Frontend" cmd /k "start_frontend.bat"

echo.
echo ========================================
echo  DEMO SYSTEM STARTED!
echo ========================================
echo.
echo Backend API: http://localhost:5000 (Demo Mode)
echo Frontend UI: http://localhost:8080
echo.
echo The system is now running with sample data.
echo No database setup required for demo!
echo.
echo Close the server windows to stop the demo.
echo.
pause