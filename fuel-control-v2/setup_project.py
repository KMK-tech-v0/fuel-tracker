#!/usr/bin/env python3
"""
Setup script for Advanced Fuel Control & Forecasting System
This script helps configure the project for first-time use
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    print(f"\n[{step}] {description}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_sql_server():
    """Check if SQL Server is available"""
    try:
        import pyodbc
        # Try to list available drivers
        drivers = [driver for driver in pyodbc.drivers() if 'SQL Server' in driver]
        if drivers:
            print(f"✅ SQL Server drivers found: {', '.join(drivers)}")
            return True
        else:
            print("❌ No SQL Server drivers found")
            print("   Please install ODBC Driver 17 for SQL Server")
            return False
    except ImportError:
        print("❌ pyodbc not installed")
        return False

def install_backend_dependencies():
    """Install Python dependencies"""
    print_step("1", "Installing backend dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Backend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup environment configuration"""
    print_step("2", "Setting up environment configuration...")
    
    env_example = Path("backend/.env.example")
    env_file = Path("backend/.env")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("   Please edit backend/.env to configure your database connection")
        return True
    elif env_file.exists():
        print("✅ Environment file already exists")
        return True
    else:
        print("❌ Could not create environment file")
        return False

def create_database_setup_script():
    """Create a database setup script"""
    print_step("3", "Creating database setup script...")
    
    script_content = '''@echo off
echo Setting up FuelControlV2 Database...
echo.
echo Make sure SQL Server is running and you have appropriate permissions.
echo.
pause

sqlcmd -S "localhost\\SQLEXPRESS" -E -i "database\\create_database.sql"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create database. Please check your SQL Server connection.
    pause
    exit /b 1
)

sqlcmd -S "localhost\\SQLEXPRESS" -E -i "database\\insert_sample_data.sql"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to insert sample data.
    pause
    exit /b 1
)

sqlcmd -S "localhost\\SQLEXPRESS" -E -i "database\\forecasting_procedures.sql"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create procedures.
    pause
    exit /b 1
)

echo.
echo Database setup completed successfully!
pause
'''
    
    with open("setup_database.bat", "w") as f:
        f.write(script_content)
    
    print("✅ Created setup_database.bat script")
    return True

def create_startup_scripts():
    """Create startup scripts for development"""
    print_step("4", "Creating startup scripts...")
    
    # Backend startup script
    backend_script = '''@echo off
echo Starting Fuel Control Backend...
cd backend
python app.py
pause
'''
    
    with open("start_backend.bat", "w") as f:
        f.write(backend_script)
    
    # Frontend startup script  
    frontend_script = '''@echo off
echo Starting Fuel Control Frontend...
cd frontend
echo Frontend will be available at: http://localhost:8080
python -m http.server 8080
pause
'''
    
    with open("start_frontend.bat", "w") as f:
        f.write(frontend_script)
    
    # Combined startup script
    combined_script = '''@echo off
echo Starting Fuel Control System...
echo.
echo Starting backend server...
start "Backend" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak > nul

echo Starting frontend server...
start "Frontend" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo System is starting up...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Press any key to exit...
pause > nul
'''
    
    with open("start_system.bat", "w") as f:
        f.write(combined_script)
    
    print("✅ Created startup scripts:")
    print("   - start_backend.bat")
    print("   - start_frontend.bat") 
    print("   - start_system.bat")
    return True

def main():
    print_header("Advanced Fuel Control & Forecasting System Setup")
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_sql_server():
        print("\n⚠️  SQL Server issues detected. Please install SQL Server and ODBC drivers.")
        print("   You can continue setup, but the application won't work until this is resolved.")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # Setup steps
    success = True
    success &= install_backend_dependencies()
    success &= setup_environment()
    success &= create_database_setup_script()
    success &= create_startup_scripts()
    
    if success:
        print_header("Setup Complete!")
        print("\n✅ Project setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit backend/.env to configure your database connection")
        print("2. Run setup_database.bat to create the database")
        print("3. Run start_system.bat to start both frontend and backend")
        print("\nFor manual startup:")
        print("- Backend: run start_backend.bat")
        print("- Frontend: run start_frontend.bat")
    else:
        print_header("Setup Failed")
        print("\n❌ Setup encountered errors. Please resolve the issues above and try again.")
    
    return success

if __name__ == "__main__":
    main()