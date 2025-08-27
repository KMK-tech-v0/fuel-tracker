#!/usr/bin/env python3
"""
Demo version of Fuel Control System Backend
Works without database for immediate demonstration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json
from decimal import Decimal

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080', 'http://127.0.0.1:8080', 'http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5501', 'http://127.0.0.1:5501'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)

app.json_encoder = DecimalEncoder

# Demo data
demo_sites = [
    {"site_id": 1, "site_name": "Main Warehouse", "site_code": "WH001", "site_type": "Warehouse", "is_active": True},
    {"site_id": 2, "site_name": "Construction Site Alpha", "site_code": "CS001", "site_type": "Site", "is_active": True},
    {"site_id": 3, "site_name": "Mining Operation Gamma", "site_code": "MO001", "site_type": "Site", "is_active": True},
    {"site_id": 4, "site_name": "Power Plant Delta", "site_code": "PP001", "site_type": "Site", "is_active": True}
]

demo_fuel_types = [
    {"fuel_type_id": 1, "fuel_name": "Diesel", "fuel_code": "DSL", "density": 0.832, "is_active": True},
    {"fuel_type_id": 2, "fuel_name": "Gasoline", "fuel_code": "GSL", "density": 0.745, "is_active": True},
    {"fuel_type_id": 3, "fuel_name": "Heavy Fuel Oil", "fuel_code": "HFO", "density": 0.960, "is_active": True}
]

demo_equipment = [
    {"equipment_id": 1, "site_id": 1, "equipment_name": "Forklift Unit 1", "equipment_code": "FL001", "fuel_type_id": 1, "consumption_rate": 3.5, "equipment_type": "Forklift", "manufacturer": "Toyota", "model": "FD25", "is_active": True, "site_name": "Main Warehouse", "fuel_name": "Diesel"},
    {"equipment_id": 2, "site_id": 2, "equipment_name": "Excavator Alpha 1", "equipment_code": "EX001", "fuel_type_id": 1, "consumption_rate": 18.5, "equipment_type": "Excavator", "manufacturer": "Komatsu", "model": "PC200", "is_active": True, "site_name": "Construction Site Alpha", "fuel_name": "Diesel"},
    {"equipment_id": 3, "site_id": 3, "equipment_name": "Mining Truck 1", "equipment_code": "MT001", "fuel_type_id": 1, "consumption_rate": 45.0, "equipment_type": "Mining Truck", "manufacturer": "Caterpillar", "model": "777D", "is_active": True, "site_name": "Mining Operation Gamma", "fuel_name": "Diesel"},
    {"equipment_id": 4, "site_id": 4, "equipment_name": "Main Generator 1", "equipment_code": "PG001", "fuel_type_id": 3, "consumption_rate": 180.0, "equipment_type": "Power Generator", "manufacturer": "GE", "model": "LM6000", "is_active": True, "site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil"}
]

demo_stock = [
    {"site_name": "Main Warehouse", "fuel_name": "Diesel", "current_quantity": 350000, "available_quantity": 340000, "minimum_threshold": 50000, "maximum_capacity": 500000, "fill_percentage": 70.0, "stock_status": "Normal", "last_updated": datetime.now().isoformat()},
    {"site_name": "Construction Site Alpha", "fuel_name": "Diesel", "current_quantity": 8000, "available_quantity": 7500, "minimum_threshold": 5000, "maximum_capacity": 50000, "fill_percentage": 16.0, "stock_status": "Critical", "last_updated": datetime.now().isoformat()},
    {"site_name": "Mining Operation Gamma", "fuel_name": "Diesel", "current_quantity": 65000, "available_quantity": 60000, "minimum_threshold": 15000, "maximum_capacity": 100000, "fill_percentage": 65.0, "stock_status": "Normal", "last_updated": datetime.now().isoformat()},
    {"site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil", "current_quantity": 45000, "available_quantity": 40000, "minimum_threshold": 25000, "maximum_capacity": 200000, "fill_percentage": 22.5, "stock_status": "Low", "last_updated": datetime.now().isoformat()}
]

demo_forecasts = [
    {"forecast_id": 1, "site_id": 1, "fuel_type_id": 1, "site_name": "Main Warehouse", "fuel_name": "Diesel", "current_balance": 350000, "daily_consumption_rate": 2500, "forecast_days_remaining": 140, "next_refill_date_estimate": (date.today() + timedelta(days=120)).isoformat(), "confidence_level": 85},
    {"forecast_id": 2, "site_id": 2, "fuel_type_id": 1, "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "current_balance": 8000, "daily_consumption_rate": 1200, "forecast_days_remaining": 6, "next_refill_date_estimate": (date.today() + timedelta(days=5)).isoformat(), "confidence_level": 92},
    {"forecast_id": 3, "site_id": 3, "fuel_type_id": 1, "site_name": "Mining Operation Gamma", "fuel_name": "Diesel", "current_balance": 65000, "daily_consumption_rate": 3500, "forecast_days_remaining": 18, "next_refill_date_estimate": (date.today() + timedelta(days=15)).isoformat(), "confidence_level": 88},
    {"forecast_id": 4, "site_id": 4, "fuel_type_id": 3, "site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil", "current_balance": 45000, "daily_consumption_rate": 4320, "forecast_days_remaining": 10, "next_refill_date_estimate": (date.today() + timedelta(days=8)).isoformat(), "confidence_level": 90}
]

demo_operational_hours = [
    {"log_id": 1, "site_id": 2, "equipment_id": 2, "log_date": date.today().isoformat(), "running_hours": 8.5, "fuel_consumed": 157.25, "recorded_by": "Site Supervisor A", "notes": "Normal operation", "site_name": "Construction Site Alpha", "equipment_name": "Excavator Alpha 1"},
    {"log_id": 2, "site_id": 3, "equipment_id": 3, "log_date": date.today().isoformat(), "running_hours": 12.0, "fuel_consumed": 540.0, "recorded_by": "Mining Chief", "notes": "Heavy load transport", "site_name": "Mining Operation Gamma", "equipment_name": "Mining Truck 1"},
    {"log_id": 3, "site_id": 4, "equipment_id": 4, "log_date": date.today().isoformat(), "running_hours": 24.0, "fuel_consumed": 4320.0, "recorded_by": "Plant Engineer", "notes": "Continuous operation", "site_name": "Power Plant Delta", "equipment_name": "Main Generator 1"}
]

demo_refills = [
    {"transaction_id": "REF-2025-001", "refill_date": date.today().isoformat(), "site_name": "Main Warehouse", "fuel_name": "Diesel", "quantity": 100000, "supplier_name": "Myanmar Petroleum Corporation", "unit_cost": 1850.00, "total_cost": 185000000, "created_by": "System"},
    {"transaction_id": "REF-2025-002", "refill_date": (date.today() - timedelta(days=1)).isoformat(), "site_name": "Mining Operation Gamma", "fuel_name": "Diesel", "quantity": 50000, "supplier_name": "Asia Fuel Trading", "unit_cost": 1820.00, "total_cost": 91000000, "created_by": "Mining Chief"}
]

demo_usage = [
    {"transaction_id": "USE-2025-001", "usage_date": date.today().isoformat(), "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "equipment_name": "Excavator Alpha 1", "quantity": 157.25, "purpose": "Excavation work", "operator_name": "John Operator", "created_by": "Site Supervisor A"},
    {"transaction_id": "USE-2025-002", "usage_date": date.today().isoformat(), "site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil", "equipment_name": "Main Generator 1", "quantity": 4320.0, "purpose": "Electricity generation", "operator_name": "Plant Operator", "created_by": "Plant Engineer"}
]

demo_alerts = [
    {"alert_history_id": 1, "alert_name": "Construction Alpha Low Stock", "alert_type": "Low Stock", "alert_message": "Construction Site Alpha diesel stock is critically low (8,000L remaining)", "severity_level": "Critical", "triggered_date": datetime.now().isoformat(), "site_name": "Construction Site Alpha", "fuel_name": "Diesel"},
    {"alert_history_id": 2, "alert_name": "Power Plant Forecast Warning", "alert_type": "Forecast Shortage", "alert_message": "Power Plant Delta estimated to run out of fuel in 10 days", "severity_level": "High", "triggered_date": datetime.now().isoformat(), "site_name": "Power Plant Delta", "fuel_name": "Heavy Fuel Oil"}
]

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'database': 'demo_mode',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0-demo'
    })

@app.route('/api/sites', methods=['GET'])
def get_sites():
    return jsonify(demo_sites)

@app.route('/api/fuel-types', methods=['GET'])
def get_fuel_types():
    return jsonify(demo_fuel_types)

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    site_id = request.args.get('site_id')
    if site_id:
        filtered_equipment = [eq for eq in demo_equipment if eq['site_id'] == int(site_id)]
        return jsonify(filtered_equipment)
    return jsonify(demo_equipment)

@app.route('/api/stock', methods=['GET'])
def get_stock():
    return jsonify(demo_stock)

@app.route('/api/forecasts', methods=['GET'])
def get_forecasts():
    return jsonify(demo_forecasts)

@app.route('/api/forecasts/calculate', methods=['POST'])
def calculate_forecasts():
    return jsonify({'message': 'Demo: Forecasts calculated successfully'})

@app.route('/api/operational-hours', methods=['GET'])
def get_operational_hours():
    return jsonify(demo_operational_hours)

@app.route('/api/operational-hours', methods=['POST'])
def log_operational_hours():
    return jsonify({'message': 'Demo: Operational hours logged successfully'})

@app.route('/api/refills', methods=['GET'])
def get_refills():
    return jsonify(demo_refills)

@app.route('/api/usage', methods=['GET'])
def get_usage():
    return jsonify(demo_usage)

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify(demo_alerts)

@app.route('/api/system/settings', methods=['GET'])
def get_system_settings():
    return jsonify([
        {"setting_key": "default_safety_factor", "setting_value": "1.2", "setting_description": "Default safety factor for forecasting"},
        {"setting_key": "demo_mode", "setting_value": "true", "setting_description": "Running in demo mode"}
    ])

if __name__ == '__main__':
    print("🚀 Starting Fuel Control System - DEMO MODE")
    print("=" * 50)
    print("Backend API: http://localhost:5000")
    print("Demo mode: No database required")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)