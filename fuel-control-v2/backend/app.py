"""
Advanced Fuel Consumption Forecasting System - Backend API
Version 2.0 with Enhanced Forecasting Capabilities
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pyodbc
import logging
from datetime import datetime, date, timedelta
import json
from decimal import Decimal
import os
from typing import Dict, List, Optional, Any
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:8080', 'http://127.0.0.1:8080',
    'http://localhost:3000', 'http://127.0.0.1:3000',
    'http://localhost:5501', 'http://127.0.0.1:5501'
], supports_credentials=True)

# Database configuration
class DatabaseConfig:
    SERVER = Config.DB_SERVER
    DATABASE = Config.DB_NAME
    DRIVER = Config.DB_DRIVER
    CONNECTION_STRING = Config.get_db_connection_string()

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)

app.json_encoder = DecimalEncoder

def get_db_connection():
    """Get database connection"""
    try:
        conn = pyodbc.connect(DatabaseConfig.CONNECTION_STRING)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

def row_to_dict(row, cursor_description) -> Dict[str, Any]:
    """Convert database row to dictionary"""
    return dict(zip([column[0] for column in cursor_description], row))

def execute_query(query: str, params: tuple = None, fetch_all: bool = True):
    """Execute database query and return results"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_all:
            rows = cursor.fetchall()
            result = [row_to_dict(row, cursor.description) for row in rows]
        else:
            row = cursor.fetchone()
            result = row_to_dict(row, cursor.description) if row else None
        
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise

# =============================================
# HEALTH CHECK AND SYSTEM INFO
# =============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/system/settings', methods=['GET'])
def get_system_settings():
    """Get system settings"""
    query = "SELECT setting_key, setting_value, setting_description, data_type FROM SystemSettings ORDER BY setting_key"
    return jsonify(execute_query(query))

# =============================================
# FUEL TYPES MANAGEMENT
# =============================================

@app.route('/api/fuel-types', methods=['GET'])
def get_fuel_types():
    """Get all fuel types"""
    query = """
    SELECT fuel_type_id, fuel_name, fuel_code, density, energy_content, 
           carbon_factor, is_active, created_date, updated_date
    FROM FuelTypes 
    WHERE is_active = 1
    ORDER BY fuel_name
    """
    return jsonify(execute_query(query))

@app.route('/api/fuel-types', methods=['POST'])
def create_fuel_type():
    """Create new fuel type"""
    data = request.get_json()
    
    query = """
    INSERT INTO FuelTypes (fuel_name, fuel_code, density, energy_content, carbon_factor)
    VALUES (?, ?, ?, ?, ?)
    """
    params = (
        data['fuel_name'],
        data['fuel_code'],
        data.get('density', 0.850),
        data.get('energy_content'),
        data.get('carbon_factor')
    )
    
    try:
        execute_query(query, params)
        return jsonify({'message': 'Fuel type created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =============================================
# SITES MANAGEMENT
# =============================================

@app.route('/api/sites', methods=['GET'])
def get_sites():
    """Get all sites"""
    query = """
    SELECT site_id, site_name, site_code, site_type, location_address,
           latitude, longitude, contact_person, contact_phone, contact_email,
           storage_capacity, safety_stock_days, is_active, created_date
    FROM Sites 
    WHERE is_active = 1
    ORDER BY site_name
    """
    return jsonify(execute_query(query))

@app.route('/api/sites', methods=['POST'])
def create_site():
    """Create new site"""
    data = request.get_json()
    
    query = """
    INSERT INTO Sites (site_name, site_code, site_type, location_address,
                      contact_person, contact_phone, storage_capacity, safety_stock_days)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data['site_name'],
        data['site_code'],
        data['site_type'],
        data.get('location_address'),
        data.get('contact_person'),
        data.get('contact_phone'),
        data.get('storage_capacity', 0),
        data.get('safety_stock_days', 7)
    )
    
    try:
        execute_query(query, params)
        return jsonify({'message': 'Site created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =============================================
# EQUIPMENT MANAGEMENT
# =============================================

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    """Get all equipment"""
    site_id = request.args.get('site_id')
    
    query = """
    SELECT e.equipment_id, e.site_id, e.equipment_name, e.equipment_code,
           e.fuel_type_id, e.consumption_rate, e.equipment_type,
           e.manufacturer, e.model, e.is_active,
           s.site_name, ft.fuel_name
    FROM Equipment e
    JOIN Sites s ON e.site_id = s.site_id
    JOIN FuelTypes ft ON e.fuel_type_id = ft.fuel_type_id
    WHERE e.is_active = 1
    """
    
    params = None
    if site_id:
        query += " AND e.site_id = ?"
        params = (site_id,)
    
    query += " ORDER BY s.site_name, e.equipment_name"
    
    return jsonify(execute_query(query, params))

@app.route('/api/equipment', methods=['POST'])
def create_equipment():
    """Create new equipment"""
    data = request.get_json()
    
    query = """
    INSERT INTO Equipment (site_id, equipment_name, equipment_code, fuel_type_id,
                          consumption_rate, equipment_type, manufacturer, model)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data['site_id'],
        data['equipment_name'],
        data['equipment_code'],
        data['fuel_type_id'],
        data['consumption_rate'],
        data.get('equipment_type'),
        data.get('manufacturer'),
        data.get('model')
    )
    
    try:
        execute_query(query, params)
        return jsonify({'message': 'Equipment created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =============================================
# OPERATIONAL HOURS LOGGING
# =============================================

@app.route('/api/operational-hours', methods=['GET'])
def get_operational_hours():
    """Get operational hours log"""
    site_id = request.args.get('site_id')
    equipment_id = request.args.get('equipment_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = """
    SELECT oh.log_id, oh.site_id, oh.equipment_id, oh.log_date,
           oh.running_hours, oh.fuel_consumed, oh.recorded_by, oh.notes,
           s.site_name, e.equipment_name
    FROM OperationalHoursLog oh
    JOIN Sites s ON oh.site_id = s.site_id
    JOIN Equipment e ON oh.equipment_id = e.equipment_id
    WHERE 1=1
    """
    
    params = []
    if site_id:
        query += " AND oh.site_id = ?"
        params.append(site_id)
    if equipment_id:
        query += " AND oh.equipment_id = ?"
        params.append(equipment_id)
    if start_date:
        query += " AND oh.log_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND oh.log_date <= ?"
        params.append(end_date)
    
    query += " ORDER BY oh.log_date DESC, s.site_name, e.equipment_name"
    
    return jsonify(execute_query(query, tuple(params) if params else None))

@app.route('/api/operational-hours', methods=['POST'])
def log_operational_hours():
    """Log operational hours for equipment"""
    data = request.get_json()
    
    query = """
    INSERT INTO OperationalHoursLog (site_id, equipment_id, log_date, running_hours,
                                   fuel_consumed, recorded_by, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data['site_id'],
        data['equipment_id'],
        data['log_date'],
        data['running_hours'],
        data.get('fuel_consumed'),
        data.get('recorded_by'),
        data.get('notes')
    )
    
    try:
        execute_query(query, params)
        
        # Recalculate forecast after logging hours
        recalculate_forecast(data['site_id'])
        
        return jsonify({'message': 'Operational hours logged successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =============================================
# STOCK MANAGEMENT
# =============================================

@app.route('/api/stock', methods=['GET'])
def get_stock():
    """Get current stock levels"""
    return jsonify(execute_query("SELECT * FROM vw_CurrentStockStatus ORDER BY site_name, fuel_name"))

@app.route('/api/stock/summary', methods=['GET'])
def get_stock_summary():
    """Get stock summary with consumption data"""
    return jsonify(execute_query("SELECT * FROM vw_SiteConsumptionSummary ORDER BY site_name, fuel_name"))

# =============================================
# FORECASTING ENDPOINTS
# =============================================

@app.route('/api/forecasts', methods=['GET'])
def get_forecasts():
    """Get consumption forecasts"""
    site_id = request.args.get('site_id')
    forecast_date = request.args.get('forecast_date', date.today().isoformat())
    
    query = """
    SELECT cf.*, s.site_name, ft.fuel_name
    FROM ConsumptionForecast cf
    JOIN Sites s ON cf.site_id = s.site_id
    JOIN FuelTypes ft ON cf.fuel_type_id = ft.fuel_type_id
    WHERE cf.forecast_date = ?
    """
    
    params = [forecast_date]
    if site_id:
        query += " AND cf.site_id = ?"
        params.append(site_id)
    
    query += " ORDER BY s.site_name, ft.fuel_name"
    
    return jsonify(execute_query(query, tuple(params)))

@app.route('/api/forecasts/calculate', methods=['POST'])
def calculate_forecasts():
    """Calculate forecasts for all sites or specific site"""
    data = request.get_json() or {}
    site_id = data.get('site_id')
    fuel_type_id = data.get('fuel_type_id')
    forecast_date = data.get('forecast_date', date.today().isoformat())
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if site_id and fuel_type_id:
            # Calculate for specific site and fuel type
            cursor.execute("EXEC sp_CalculateSiteForecast ?, ?, ?", 
                         (site_id, fuel_type_id, forecast_date))
        else:
            # Calculate for all sites
            cursor.execute("EXEC sp_CalculateAllForecasts ?", (forecast_date,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Forecasts calculated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/forecasts/scenarios', methods=['POST'])
def create_forecast_scenario():
    """Create forecast scenario"""
    data = request.get_json()
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            EXEC sp_CreateForecastScenario ?, ?, ?, ?
        """, (
            data['forecast_id'],
            data['scenario_name'],
            data.get('adjusted_consumption_rate'),
            data.get('adjusted_safety_factor')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Forecast scenario created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/forecasts/<int:forecast_id>/scenarios', methods=['GET'])
def get_forecast_scenarios(forecast_id):
    """Get scenarios for a forecast"""
    query = "SELECT * FROM ForecastScenarios WHERE forecast_id = ? ORDER BY created_date"
    return jsonify(execute_query(query, (forecast_id,)))

# =============================================
# ALERTS AND NOTIFICATIONS
# =============================================

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    days = request.args.get('days', 7)
    try:
        days = int(days)
    except (ValueError, TypeError):
        days = 7
    
    query = """
    SELECT ah.*, ac.alert_name, ac.alert_type, s.site_name, ft.fuel_name
    FROM AlertHistory ah
    JOIN AlertConfigurations ac ON ah.alert_id = ac.alert_id
    LEFT JOIN Sites s ON ac.site_id = s.site_id
    LEFT JOIN FuelTypes ft ON ac.fuel_type_id = ft.fuel_type_id
    WHERE ah.triggered_date >= DATEADD(day, -?, GETDATE())
    ORDER BY ah.triggered_date DESC
    """
    
    return jsonify(execute_query(query, (days,)))

@app.route('/api/alerts/check', methods=['POST'])
def check_alerts():
    """Manually trigger alert check"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_CheckForecastAlerts")
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Alert check completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =============================================
# TRANSACTIONS
# =============================================

@app.route('/api/refills', methods=['GET'])
def get_refills():
    """Get refill transactions"""
    site_id = request.args.get('site_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = """
    SELECT rt.*, s.site_name, ft.fuel_name, sup.supplier_name
    FROM RefillTransactions rt
    JOIN Sites s ON rt.site_id = s.site_id
    JOIN FuelTypes ft ON rt.fuel_type_id = ft.fuel_type_id
    LEFT JOIN Suppliers sup ON rt.supplier_id = sup.supplier_id
    WHERE 1=1
    """
    
    params = []
    if site_id:
        query += " AND rt.site_id = ?"
        params.append(site_id)
    if start_date:
        query += " AND rt.refill_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND rt.refill_date <= ?"
        params.append(end_date)
    
    query += " ORDER BY rt.refill_date DESC"
    
    return jsonify(execute_query(query, tuple(params) if params else None))

@app.route('/api/refills', methods=['POST'])
def create_refill():
    """Create refill transaction"""
    data = request.get_json()
    
    # Generate transaction ID
    transaction_id = f"REF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    query = """
    INSERT INTO RefillTransactions (transaction_id, site_id, fuel_type_id, supplier_id,
                                  quantity, unit_cost, total_cost, refill_date, created_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        transaction_id,
        data['site_id'],
        data['fuel_type_id'],
        data.get('supplier_id'),
        data['quantity'],
        data.get('unit_cost'),
        data.get('total_cost'),
        data.get('refill_date', datetime.now()),
        data.get('created_by', 'System')
    )
    
    try:
        execute_query(query, params)
        
        # Update stock
        update_stock_after_transaction(data['site_id'], data['fuel_type_id'], data['quantity'])
        
        return jsonify({'message': 'Refill transaction created successfully', 'transaction_id': transaction_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/usage', methods=['GET'])
def get_usage():
    """Get usage transactions"""
    site_id = request.args.get('site_id')
    equipment_id = request.args.get('equipment_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = """
    SELECT ut.*, s.site_name, ft.fuel_name, e.equipment_name
    FROM UsageTransactions ut
    JOIN Sites s ON ut.site_id = s.site_id
    JOIN FuelTypes ft ON ut.fuel_type_id = ft.fuel_type_id
    LEFT JOIN Equipment e ON ut.equipment_id = e.equipment_id
    WHERE 1=1
    """
    
    params = []
    if site_id:
        query += " AND ut.site_id = ?"
        params.append(site_id)
    if equipment_id:
        query += " AND ut.equipment_id = ?"
        params.append(equipment_id)
    if start_date:
        query += " AND ut.usage_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND ut.usage_date <= ?"
        params.append(end_date)
    
    query += " ORDER BY ut.usage_date DESC"
    
    return jsonify(execute_query(query, tuple(params) if params else None))

@app.route('/api/usage', methods=['POST'])
def create_usage():
    """Create usage transaction"""
    data = request.get_json()
    
    # Generate transaction ID
    transaction_id = f"USE-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    query = """
    INSERT INTO UsageTransactions (transaction_id, site_id, fuel_type_id, equipment_id,
                                 department, quantity, usage_date, purpose, created_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        transaction_id,
        data['site_id'],
        data['fuel_type_id'],
        data.get('equipment_id'),
        data.get('department'),
        data['quantity'],
        data.get('usage_date', datetime.now()),
        data.get('purpose'),
        data.get('created_by', 'System')
    )
    
    try:
        execute_query(query, params)
        
        # Update stock (negative quantity for usage)
        update_stock_after_transaction(data['site_id'], data['fuel_type_id'], -data['quantity'])
        
        return jsonify({'message': 'Usage transaction created successfully', 'transaction_id': transaction_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# =============================================
# REPORTING ENDPOINTS
# =============================================

@app.route('/api/reports/consumption-summary', methods=['GET'])
def get_consumption_summary():
    """Get consumption summary report"""
    site_id = request.args.get('site_id')
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    
    query = """
    SELECT 
        s.site_name,
        ft.fuel_name,
        SUM(ut.quantity) as total_consumed,
        AVG(ut.quantity) as avg_daily_consumption,
        COUNT(*) as transaction_count,
        MIN(ut.usage_date) as first_usage,
        MAX(ut.usage_date) as last_usage
    FROM UsageTransactions ut
    JOIN Sites s ON ut.site_id = s.site_id
    JOIN FuelTypes ft ON ut.fuel_type_id = ft.fuel_type_id
    WHERE ut.usage_date BETWEEN ? AND ?
    """
    
    params = [start_date, end_date]
    if site_id:
        query += " AND ut.site_id = ?"
        params.append(site_id)
    
    query += """
    GROUP BY s.site_name, ft.fuel_name
    ORDER BY s.site_name, ft.fuel_name
    """
    
    return jsonify(execute_query(query, tuple(params)))

@app.route('/api/reports/equipment-efficiency', methods=['GET'])
def get_equipment_efficiency():
    """Get equipment efficiency report"""
    return jsonify(execute_query("SELECT * FROM vw_EquipmentConsumptionSummary ORDER BY site_name, equipment_name"))

# =============================================
# UTILITY FUNCTIONS
# =============================================

def update_stock_after_transaction(site_id: int, fuel_type_id: int, quantity_change: float):
    """Update stock after transaction"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_UpdateStockAfterTransaction ?, ?, ?, ?", 
                      (site_id, fuel_type_id, quantity_change, 'REFILL' if quantity_change > 0 else 'USAGE'))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to update stock: {e}")
        raise

def recalculate_forecast(site_id: int):
    """Recalculate forecast for a site"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all fuel types for this site
        cursor.execute("SELECT DISTINCT fuel_type_id FROM FuelStock WHERE site_id = ?", (site_id,))
        fuel_types = cursor.fetchall()
        
        for fuel_type in fuel_types:
            cursor.execute("EXEC sp_CalculateSiteForecast ?, ?, ?", 
                          (site_id, fuel_type[0], date.today()))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to recalculate forecast: {e}")

# =============================================
# ERROR HANDLERS
# =============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# =============================================
# MAIN APPLICATION
# =============================================

if __name__ == '__main__':
    logger.info("Starting Advanced Fuel Consumption Forecasting System API")
    app.run(debug=True, host='0.0.0.0', port=5000)
