@echo off
echo ========================================
echo  Starting Fuel Control Frontend Server
echo ========================================
echo.
cd frontend
echo Frontend will be available at: http://localhost:8080
echo Press Ctrl+C to stop the server
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak > nul
start http://localhost:8080
python -m http.server 8080
pause