#!/usr/bin/env python3
"""
Simple startup script for Fuel Control System
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def start_system():
    print("🚀 Starting Fuel Control System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check for required files
    backend_dir = current_dir / "backend"
    frontend_dir = current_dir / "frontend"
    demo_script = backend_dir / "demo_app.py"
    
    print(f"🔍 Checking files...")
    print(f"   Backend dir: {backend_dir.exists()}")
    print(f"   Frontend dir: {frontend_dir.exists()}")
    print(f"   Demo script: {demo_script.exists()}")
    
    if not demo_script.exists():
        print("❌ Demo script not found!")
        print("📝 Creating demo script...")
        create_demo_script()
    
    # Start backend
    print("\n🔧 Starting backend server...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "demo_app.py"],
            cwd=str(backend_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("✅ Backend server started")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return
    
    # Wait for backend
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    print("🌐 Starting frontend server...")
    try:
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8080"],
            cwd=str(frontend_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("✅ Frontend server started")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return
    
    # Wait for frontend
    print("⏳ Waiting for frontend to initialize...")
    time.sleep(2)
    
    # Open browser
    print("🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:8080")
        print("✅ Browser opened")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
    
    print("\n" + "🎉" * 50)
    print("🚀 FUEL CONTROL SYSTEM IS RUNNING!")
    print("🎉" * 50)
    print("\n📊 Backend API:  http://localhost:5000")
    print("🌐 Frontend UI:  http://localhost:8080")
    print("\n⚠️  Close the console windows to stop the servers")
    print("✨ Enjoy exploring your fuel control system!")

def create_demo_script():
    """Create the demo script if it doesn't exist"""
    demo_content = '''#!/usr/bin/env python3
"""
Demo Fuel Control Backend - No Database Required
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json

app = Flask(__name__)
CORS(app)

# Sample data
sites = [
    {"site_id": 1, "site_name": "Main Warehouse", "site_code": "WH001"},
    {"site_id": 2, "site_name": "Construction Site Alpha", "site_code": "CS001"},
    {"site_id": 3, "site_name": "Mining Operation Gamma", "site_code": "MO001"},
    {"site_id": 4, "site_name": "Power Plant Delta", "site_code": "PP001"}
]

equipment = [
    {"equipment_id": 1, "site_id": 1, "equipment_name": "Forklift Unit 1", "consumption_rate": 3.5, "site_name": "Main Warehouse", "fuel_name": "Diesel", "is_active": True},
    {"equipment_id": 2, "site_id": 2, "equipment_name": "Excavator Alpha 1", "consumption_rate": 18.5, "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "is_active": True},
    {"equipment_id": 3, "site_id": 3, "equipment_name": "Mining Truck 1", "consumption_rate": 45.0, "site_name": "Mining Operation Gamma", "fuel_name": "Diesel", "is_active": True},
    {"equipment_id": 4, "site_id": 4, "equipment_name": "Main Generator 1", "consumption_rate": 180.0, "site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil", "is_active": True}
]

stock = [
    {"site_name": "Main Warehouse", "fuel_name": "Diesel", "current_quantity": 350000, "available_quantity": 340000, "fill_percentage": 70.0, "stock_status": "Normal", "last_updated": datetime.now().isoformat()},
    {"site_name": "Construction Site Alpha", "fuel_name": "Diesel", "current_quantity": 8000, "available_quantity": 7500, "fill_percentage": 16.0, "stock_status": "Critical", "last_updated": datetime.now().isoformat()},
    {"site_name": "Mining Operation Gamma", "fuel_name": "Diesel", "current_quantity": 65000, "available_quantity": 60000, "fill_percentage": 65.0, "stock_status": "Normal", "last_updated": datetime.now().isoformat()},
    {"site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil", "current_quantity": 45000, "available_quantity": 40000, "fill_percentage": 22.5, "stock_status": "Low", "last_updated": datetime.now().isoformat()}
]

forecasts = [
    {"forecast_id": 1, "site_name": "Main Warehouse", "fuel_name": "Diesel", "current_balance": 350000, "daily_consumption_rate": 2500, "forecast_days_remaining": 140, "confidence_level": 85},
    {"forecast_id": 2, "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "current_balance": 8000, "daily_consumption_rate": 1200, "forecast_days_remaining": 6, "confidence_level": 92},
    {"forecast_id": 3, "site_name": "Mining Operation Gamma", "fuel_name": "Diesel", "current_balance": 65000, "daily_consumption_rate": 3500, "forecast_days_remaining": 18, "confidence_level": 88},
    {"forecast_id": 4, "site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil", "current_balance": 45000, "daily_consumption_rate": 4320, "forecast_days_remaining": 10, "confidence_level": 90}
]

alerts = [
    {"alert_name": "Construction Alpha Low Stock", "severity_level": "Critical", "alert_message": "Construction Site Alpha diesel stock is critically low"},
    {"alert_name": "Power Plant Forecast Warning", "severity_level": "High", "alert_message": "Power Plant Delta estimated to run out of fuel in 10 days"}
]

# API Routes
@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "database": "demo_mode", "version": "2.0-demo"})

@app.route('/api/sites')
def get_sites():
    return jsonify(sites)

@app.route('/api/equipment')
def get_equipment():
    return jsonify(equipment)

@app.route('/api/stock')
def get_stock():
    return jsonify(stock)

@app.route('/api/forecasts')
def get_forecasts():
    return jsonify(forecasts)

@app.route('/api/operational-hours')
def get_hours():
    return jsonify([])

@app.route('/api/operational-hours', methods=['POST'])
def post_hours():
    return jsonify({"message": "Demo: Hours logged successfully"})

@app.route('/api/refills')
def get_refills():
    return jsonify([])

@app.route('/api/usage')
def get_usage():
    return jsonify([])

@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts)

@app.route('/api/forecasts/calculate', methods=['POST'])
def calculate_forecasts():
    return jsonify({"message": "Demo: Forecasts calculated"})

if __name__ == '__main__':
    print("🚀 Fuel Control Demo Backend Starting...")
    print("📊 API: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    backend_dir = Path("backend")
    demo_file = backend_dir / "demo_app.py"
    
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(demo_content)
    
    print(f"✅ Created demo script: {demo_file}")

if __name__ == "__main__":
    start_system()