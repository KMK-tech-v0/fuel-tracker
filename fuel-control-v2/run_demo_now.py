#!/usr/bin/env python3
"""
Quick launcher for the Fuel Control Demo
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def print_banner():
    print("🔥" * 60)
    print("🚀 FUEL CONTROL SYSTEM - STARTING DEMO")
    print("🔥" * 60)
    print()

def check_requirements():
    """Check if required packages are available"""
    try:
        import flask
        import flask_cors
        print("✅ Flask packages available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Installing required packages...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors"], check=True)
            print("✅ Packages installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages")
            return False

def start_backend():
    """Start the backend server"""
    print("🔧 Starting backend server...")
    backend_dir = Path("backend")
    demo_script = backend_dir / "demo_app.py"
    
    if not demo_script.exists():
        print("❌ Demo script not found")
        return None
    
    try:
        # Start backend in a new process
        process = subprocess.Popen(
            [sys.executable, str(demo_script)],
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Backend server starting...")
        print("   URL: http://localhost:5000")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    print("🌐 Starting frontend server...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    try:
        # Start frontend HTTP server
        process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8080"],
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Frontend server starting...")
        print("   URL: http://localhost:8080")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def open_browser():
    """Open the application in browser"""
    print("🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:8080")
        print("✅ Browser opened")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("   Please manually open: http://localhost:8080")

def main():
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Cannot start demo - missing requirements")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot start demo - backend failed")
        return
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Cannot start demo - frontend failed")
        backend_process.terminate()
        return
    
    # Wait for frontend to start
    print("⏳ Waiting for frontend to initialize...")
    time.sleep(2)
    
    # Open browser
    open_browser()
    
    print()
    print("🎉" * 60)
    print("🚀 FUEL CONTROL SYSTEM DEMO IS RUNNING!")
    print("🎉" * 60)
    print()
    print("📊 Backend API:  http://localhost:5000")
    print("🌐 Frontend UI:  http://localhost:8080")
    print()
    print("✨ Features to explore:")
    print("   • Dashboard with KPIs and charts")
    print("   • Fuel consumption forecasting")
    print("   • Stock management")
    print("   • Equipment tracking")
    print("   • Operational hours logging")
    print("   • Refills and usage transactions")
    print()
    print("⚠️  Press Ctrl+C to stop the demo")
    print()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping demo...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Demo stopped")

if __name__ == "__main__":
    main()