@echo off
echo ========================================
echo  FUEL CONTROL SYSTEM - SIMPLE START
echo ========================================
echo.

echo Step 1: Installing Flask...
pip install flask flask-cors

echo.
echo Step 2: Starting Backend...
cd backend
start "Backend Server" cmd /k "python -c "
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return {'status': 'ok'}

@app.route('/api/sites')  
def sites():
    return [{'site_id': 1, 'site_name': 'Test Site'}]

@app.route('/api/equipment')
def equipment():
    return [{'equipment_id': 1, 'equipment_name': 'Test Equipment'}]

@app.route('/api/stock')
def stock():
    return [{'site_name': 'Test', 'current_quantity': 1000}]

@app.route('/api/forecasts')
def forecasts():
    return [{'site_name': 'Test', 'days_remaining': 30}]

@app.route('/api/operational-hours')
def hours():
    return []

@app.route('/api/refills')
def refills():
    return []

@app.route('/api/usage')
def usage():
    return []

@app.route('/api/alerts')
def alerts():
    return []

if __name__ == '__main__':
    print('Backend running on http://localhost:5000')
    app.run(host='0.0.0.0', port=5000)
""

cd ..

echo.
echo Step 3: Starting Frontend...
cd frontend
start "Frontend Server" cmd /k "python -m http.server 8080"

echo.
echo Step 4: Opening Browser...
timeout /t 3 /nobreak > nul
start http://localhost:8080

echo.
echo ========================================
echo  SYSTEM STARTED!
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
echo.
pause