#!/usr/bin/env python3
"""
Simple browser opener for Fuel Control System
"""

import webbrowser
import time
import sys

def open_fuel_control():
    print("🌐 Opening Fuel Control System in your browser...")
    print()
    
    # URLs to try
    urls = [
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    for url in urls:
        try:
            print(f"🔗 Trying to open: {url}")
            webbrowser.open(url)
            print(f"✅ Browser opened successfully!")
            print()
            print("🎯 You should now see:")
            print("   • Advanced Fuel Control & Forecasting System")
            print("   • Professional blue header")
            print("   • Sidebar navigation")
            print("   • Dashboard with KPI cards")
            print("   • Charts and data tables")
            print()
            print("📱 If the page doesn't load:")
            print("   1. Make sure the backend server is running")
            print("   2. Make sure the frontend server is running")
            print("   3. Try refreshing the page")
            print()
            return True
        except Exception as e:
            print(f"⚠️  Could not open {url}: {e}")
            continue
    
    print("❌ Could not open browser automatically")
    print("📝 Please manually open your browser and go to:")
    print("   http://localhost:8080")
    return False

if __name__ == "__main__":
    open_fuel_control()