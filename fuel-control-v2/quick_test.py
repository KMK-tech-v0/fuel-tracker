#!/usr/bin/env python3
"""
Quick Test for Fuel Control System
Tests basic functionality without starting servers
"""

import sys
import os
from pathlib import Path
import json

def test_python_version():
    """Test Python version"""
    print("🔍 Testing Python Version...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version.split()[0]} - Compatible")
        return True
    else:
        print(f"❌ Python {sys.version.split()[0]} - Requires 3.8+")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing File Structure...")
    
    required_files = [
        'backend/app.py',
        'backend/config.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/app.js',
        'frontend/styles.css',
        'database/create_database.sql'
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def test_backend_imports():
    """Test if backend can import required modules"""
    print("\n🔍 Testing Backend Dependencies...")
    
    # Add backend to path
    sys.path.insert(0, 'backend')
    
    try:
        # Test basic imports
        import flask
        print("✅ Flask - Available")
        
        import flask_cors
        print("✅ Flask-CORS - Available")
        
        try:
            import pyodbc
            print("✅ pyodbc - Available")
        except ImportError:
            print("⚠️  pyodbc - Not available (SQL Server driver needed)")
        
        # Test config import
        try:
            from config import Config
            print("✅ Config class - Available")
        except Exception as e:
            print(f"❌ Config class - Error: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_backend_syntax():
    """Test backend Python syntax"""
    print("\n🔍 Testing Backend Syntax...")
    
    try:
        # Test app.py syntax
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            compile(f.read(), 'backend/app.py', 'exec')
        print("✅ backend/app.py - Syntax OK")
        
        # Test config.py syntax
        with open('backend/config.py', 'r', encoding='utf-8') as f:
            compile(f.read(), 'backend/config.py', 'exec')
        print("✅ backend/config.py - Syntax OK")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_frontend_structure():
    """Test frontend file structure"""
    print("\n🔍 Testing Frontend Structure...")
    
    try:
        # Test HTML structure
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        required_sections = [
            'dashboard-section',
            'forecasting-section', 
            'stock-section',
            'equipment-section',
            'operational-hours-section',
            'refills-section',
            'usage-section'
        ]
        
        missing_sections = []
        for section in required_sections:
            if f'id="{section}"' in html_content:
                print(f"✅ {section}")
            else:
                print(f"❌ {section} - Missing")
                missing_sections.append(section)
        
        # Test JavaScript structure
        with open('frontend/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        required_classes = [
            'class Utils',
            'class ApiService', 
            'class Dashboard',
            'class Forecasting',
            'class Stock',
            'class Equipment',
            'class OperationalHours',
            'class Refills',
            'class Usage'
        ]
        
        missing_classes = []
        for class_name in required_classes:
            if class_name in js_content:
                print(f"✅ {class_name}")
            else:
                print(f"❌ {class_name} - Missing")
                missing_classes.append(class_name)
        
        return len(missing_sections) == 0 and len(missing_classes) == 0
        
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def test_configuration():
    """Test configuration files"""
    print("\n🔍 Testing Configuration...")
    
    # Check if .env.example exists
    if Path('backend/.env.example').exists():
        print("✅ .env.example - Available")
    else:
        print("❌ .env.example - Missing")
    
    # Check if .env exists
    if Path('backend/.env').exists():
        print("✅ .env - Configured")
    else:
        print("⚠️  .env - Not configured (will use defaults)")
    
    # Test if setup scripts exist
    setup_files = ['setup_project.py', 'QUICK_START.md']
    for file_name in setup_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - Missing")
    
    return True

def test_database_scripts():
    """Test database setup scripts"""
    print("\n🔍 Testing Database Scripts...")
    
    db_files = [
        'database/create_database.sql',
        'database/insert_sample_data.sql', 
        'database/forecasting_procedures.sql'
    ]
    
    all_exist = True
    for file_path in db_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all quick tests"""
    print("🚀 Fuel Control System - Quick Test Suite")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Backend Dependencies", test_backend_imports),
        ("Backend Syntax", test_backend_syntax),
        ("Frontend Structure", test_frontend_structure),
        ("Configuration", test_configuration),
        ("Database Scripts", test_database_scripts)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - Error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready for use.")
        print("\nNext steps:")
        print("1. Configure database connection in backend/.env")
        print("2. Run setup_database.bat to create database")
        print("3. Start system with start_system.bat")
    elif passed >= total * 0.8:
        print("\n⚠️  MOSTLY WORKING - Minor issues detected")
        print("System should work with some limitations")
    else:
        print("\n❌ MAJOR ISSUES DETECTED")
        print("Please fix the failed tests before proceeding")

if __name__ == "__main__":
    main()