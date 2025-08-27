@echo off
echo ========================================
echo  Starting Fuel Control Backend Server
echo ========================================
echo.
echo Installing dependencies...
cd backend
pip install -r requirements.txt
echo.
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
pause