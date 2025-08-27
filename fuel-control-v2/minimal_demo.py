#!/usr/bin/env python3
"""
Minimal Fuel Control Demo - Single File
"""

import os
import sys
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

# Simple Flask-like server
class DemoHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.send_api_response()
        else:
            # Serve frontend files
            if self.path == '/':
                self.path = '/index.html'
            
            # Change to frontend directory
            os.chdir('frontend')
            super().do_GET()
            os.chdir('..')
    
    def send_api_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Simple API responses
        if '/api/health' in self.path:
            response = {"status": "healthy", "version": "demo"}
        elif '/api/sites' in self.path:
            response = [
                {"site_id": 1, "site_name": "Main Warehouse"},
                {"site_id": 2, "site_name": "Construction Site Alpha"},
                {"site_id": 3, "site_name": "Mining Operation"},
                {"site_id": 4, "site_name": "Power Plant"}
            ]
        elif '/api/equipment' in self.path:
            response = [
                {"equipment_id": 1, "equipment_name": "Forklift Unit 1", "site_name": "Main Warehouse", "fuel_name": "Diesel", "consumption_rate": 3.5, "is_active": True},
                {"equipment_id": 2, "equipment_name": "Excavator Alpha 1", "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "consumption_rate": 18.5, "is_active": True},
                {"equipment_id": 3, "equipment_name": "Mining Truck 1", "site_name": "Mining Operation", "fuel_name": "Diesel", "consumption_rate": 45.0, "is_active": True},
                {"equipment_id": 4, "equipment_name": "Main Generator 1", "site_name": "Power Plant", "fuel_name": "Heavy Fuel Oil", "consumption_rate": 180.0, "is_active": True}
            ]
        elif '/api/stock' in self.path:
            response = [
                {"site_name": "Main Warehouse", "fuel_name": "Diesel", "current_quantity": 350000, "available_quantity": 340000, "fill_percentage": 70.0, "stock_status": "Normal", "last_updated": "2025-01-03T12:00:00"},
                {"site_name": "Construction Site Alpha", "fuel_name": "Diesel", "current_quantity": 8000, "available_quantity": 7500, "fill_percentage": 16.0, "stock_status": "Critical", "last_updated": "2025-01-03T12:00:00"},
                {"site_name": "Mining Operation", "fuel_name": "Diesel", "current_quantity": 65000, "available_quantity": 60000, "fill_percentage": 65.0, "stock_status": "Normal", "last_updated": "2025-01-03T12:00:00"},
                {"site_name": "Power Plant", "fuel_name": "Heavy Fuel Oil", "current_quantity": 45000, "available_quantity": 40000, "fill_percentage": 22.5, "stock_status": "Low", "last_updated": "2025-01-03T12:00:00"}
            ]
        elif '/api/forecasts' in self.path:
            response = [
                {"forecast_id": 1, "site_name": "Main Warehouse", "fuel_name": "Diesel", "current_balance": 350000, "daily_consumption_rate": 2500, "forecast_days_remaining": 140, "next_refill_date_estimate": "2025-05-01", "confidence_level": 85},
                {"forecast_id": 2, "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "current_balance": 8000, "daily_consumption_rate": 1200, "forecast_days_remaining": 6, "next_refill_date_estimate": "2025-01-09", "confidence_level": 92},
                {"forecast_id": 3, "site_name": "Mining Operation", "fuel_name": "Diesel", "current_balance": 65000, "daily_consumption_rate": 3500, "forecast_days_remaining": 18, "next_refill_date_estimate": "2025-01-21", "confidence_level": 88},
                {"forecast_id": 4, "site_name": "Power Plant", "fuel_name": "Heavy Fuel Oil", "current_balance": 45000, "daily_consumption_rate": 4320, "forecast_days_remaining": 10, "next_refill_date_estimate": "2025-01-13", "confidence_level": 90}
            ]
        elif '/api/operational-hours' in self.path:
            response = [
                {"log_id": 1, "site_name": "Construction Site Alpha", "equipment_name": "Excavator Alpha 1", "log_date": "2025-01-03", "running_hours": 8.5, "fuel_consumed": 157.25, "recorded_by": "Site Supervisor", "notes": "Normal operation"},
                {"log_id": 2, "site_name": "Mining Operation", "equipment_name": "Mining Truck 1", "log_date": "2025-01-03", "running_hours": 12.0, "fuel_consumed": 540.0, "recorded_by": "Mining Chief", "notes": "Heavy load transport"}
            ]
        elif '/api/refills' in self.path:
            response = [
                {"transaction_id": "REF-2025-001", "refill_date": "2025-01-03", "site_name": "Main Warehouse", "fuel_name": "Diesel", "quantity": 100000, "supplier_name": "Myanmar Petroleum", "unit_cost": 1850.00, "total_cost": 185000000, "created_by": "System"}
            ]
        elif '/api/usage' in self.path:
            response = [
                {"transaction_id": "USE-2025-001", "usage_date": "2025-01-03", "site_name": "Construction Site Alpha", "fuel_name": "Diesel", "equipment_name": "Excavator Alpha 1", "quantity": 157.25, "purpose": "Excavation work", "operator_name": "John Operator", "created_by": "Site Supervisor"}
            ]
        elif '/api/alerts' in self.path:
            response = [
                {"alert_name": "Construction Alpha Low Stock", "severity_level": "Critical", "alert_message": "Construction Site Alpha diesel stock is critically low (8,000L remaining)", "triggered_date": "2025-01-03T12:00:00", "site_name": "Construction Site Alpha", "fuel_name": "Diesel"},
                {"alert_name": "Power Plant Forecast Warning", "severity_level": "High", "alert_message": "Power Plant estimated to run out of fuel in 10 days", "triggered_date": "2025-01-03T12:00:00", "site_name": "Power Plant", "fuel_name": "Heavy Fuel Oil"}
            ]
        else:
            response = {"error": "Not found"}
        
        self.wfile.write(json.dumps(response).encode())

def start_server():
    """Start the demo server"""
    print("🚀 Starting Fuel Control Demo Server...")
    print("📊 Server: http://localhost:8080")
    print("📊 API: http://localhost:8080/api/")
    print()
    
    try:
        server = HTTPServer(('localhost', 8080), DemoHandler)
        print("✅ Server started successfully!")
        print("🌐 Opening browser...")
        
        # Open browser after a short delay
        threading.Timer(2.0, lambda: webbrowser.open('http://localhost:8080')).start()
        
        print("🎉 Fuel Control System is running!")
        print("⚠️  Press Ctrl+C to stop")
        print()
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server.shutdown()
        print("✅ Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if frontend directory exists
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found!")
        print("📁 Make sure you're in the fuel-control-v2 directory")
        sys.exit(1)
    
    start_server()