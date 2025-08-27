#!/usr/bin/env python3
"""
Basic Test for Fuel Control System
Tests file structure and syntax without dependencies
"""

import sys
import os
from pathlib import Path

def test_file_structure():
    """Test if all required files exist"""
    print("🔍 Testing File Structure...")
    
    required_files = {
        'backend/app.py': 'Backend main application',
        'backend/config.py': 'Backend configuration',
        'backend/requirements.txt': 'Python dependencies',
        'backend/.env.example': 'Environment template',
        'frontend/index.html': 'Frontend main page',
        'frontend/app.js': 'Frontend JavaScript',
        'frontend/styles.css': 'Frontend styles',
        'frontend/assets/placeholder-logo.svg': 'Placeholder logo',
        'database/create_database.sql': 'Database creation script',
        'database/insert_sample_data.sql': 'Sample data script',
        'database/forecasting_procedures.sql': 'Stored procedures',
        'setup_project.py': 'Setup script',
        'QUICK_START.md': 'Quick start guide'
    }
    
    results = {}
    for file_path, description in required_files.items():
        exists = Path(file_path).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file_path} - {description}")
        results[file_path] = exists
    
    return results

def test_backend_syntax():
    """Test backend Python syntax"""
    print("\n🔍 Testing Backend Syntax...")
    
    python_files = [
        'backend/app.py',
        'backend/config.py',
        'setup_project.py'
    ]
    
    results = {}
    for file_path in python_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_path, 'exec')
                print(f"✅ {file_path} - Syntax OK")
                results[file_path] = True
            except SyntaxError as e:
                print(f"❌ {file_path} - Syntax Error: Line {e.lineno}: {e.msg}")
                results[file_path] = False
            except Exception as e:
                print(f"❌ {file_path} - Error: {e}")
                results[file_path] = False
        else:
            print(f"❌ {file_path} - File not found")
            results[file_path] = False
    
    return results

def test_frontend_structure():
    """Test frontend file structure"""
    print("\n🔍 Testing Frontend Structure...")
    
    results = {}
    
    # Test HTML structure
    if Path('frontend/index.html').exists():
        try:
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
            
            html_results = {}
            for section in required_sections:
                exists = f'id="{section}"' in html_content
                status = "✅" if exists else "❌"
                print(f"{status} HTML Section: {section}")
                html_results[section] = exists
            
            results['html_sections'] = html_results
            
        except Exception as e:
            print(f"❌ Error reading HTML: {e}")
            results['html_sections'] = False
    
    # Test JavaScript structure
    if Path('frontend/app.js').exists():
        try:
            with open('frontend/app.js', 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            required_classes = [
                'class Utils',
                'class ApiService',
                'class Navigation',
                'class Dashboard',
                'class Forecasting',
                'class Stock',
                'class Equipment',
                'class OperationalHours',
                'class Refills',
                'class Usage'
            ]
            
            js_results = {}
            for class_name in required_classes:
                exists = class_name in js_content
                status = "✅" if exists else "❌"
                print(f"{status} JS Class: {class_name}")
                js_results[class_name] = exists
            
            results['js_classes'] = js_results
            
        except Exception as e:
            print(f"❌ Error reading JavaScript: {e}")
            results['js_classes'] = False
    
    return results

def test_api_endpoints():
    """Test if API endpoints are defined in backend"""
    print("\n🔍 Testing API Endpoints...")
    
    if not Path('backend/app.py').exists():
        print("❌ backend/app.py not found")
        return False
    
    try:
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        required_endpoints = [
            '@app.route(\'/api/health\'',
            '@app.route(\'/api/sites\'',
            '@app.route(\'/api/fuel-types\'',
            '@app.route(\'/api/equipment\'',
            '@app.route(\'/api/stock\'',
            '@app.route(\'/api/forecasts\'',
            '@app.route(\'/api/operational-hours\'',
            '@app.route(\'/api/refills\'',
            '@app.route(\'/api/usage\'',
            '@app.route(\'/api/alerts\''
        ]
        
        results = {}
        for endpoint in required_endpoints:
            exists = endpoint in app_content
            status = "✅" if exists else "❌"
            endpoint_name = endpoint.split("'")[1]
            print(f"{status} API Endpoint: {endpoint_name}")
            results[endpoint_name] = exists
        
        return results
        
    except Exception as e:
        print(f"❌ Error reading backend app: {e}")
        return False

def test_database_scripts():
    """Test database script structure"""
    print("\n🔍 Testing Database Scripts...")
    
    scripts = {
        'database/create_database.sql': ['CREATE DATABASE', 'CREATE TABLE'],
        'database/insert_sample_data.sql': ['INSERT INTO'],
        'database/forecasting_procedures.sql': ['CREATE PROCEDURE', 'CREATE VIEW']
    }
    
    results = {}
    for script_path, required_keywords in scripts.items():
        if Path(script_path).exists():
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read().upper()
                
                script_results = {}
                for keyword in required_keywords:
                    exists = keyword in content
                    status = "✅" if exists else "❌"
                    print(f"{status} {script_path}: {keyword}")
                    script_results[keyword] = exists
                
                results[script_path] = script_results
                
            except Exception as e:
                print(f"❌ Error reading {script_path}: {e}")
                results[script_path] = False
        else:
            print(f"❌ {script_path} - Not found")
            results[script_path] = False
    
    return results

def test_configuration():
    """Test configuration alignment"""
    print("\n🔍 Testing Configuration Alignment...")
    
    results = {}
    
    # Check if config.py is imported in app.py
    if Path('backend/app.py').exists():
        try:
            with open('backend/app.py', 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            config_imported = 'from config import Config' in app_content
            config_used = 'Config.DB_SERVER' in app_content
            
            status1 = "✅" if config_imported else "❌"
            status2 = "✅" if config_used else "❌"
            
            print(f"{status1} Config import in app.py")
            print(f"{status2} Config usage in app.py")
            
            results['config_import'] = config_imported
            results['config_usage'] = config_used
            
        except Exception as e:
            print(f"❌ Error checking config usage: {e}")
            results['config_check'] = False
    
    # Check frontend API configuration
    if Path('frontend/app.js').exists():
        try:
            with open('frontend/app.js', 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            api_config = 'API_BASE_URL: \'http://localhost:5000/api\'' in js_content
            cors_origins = 'localhost:8080' in js_content  # Check if CORS is configured
            
            status1 = "✅" if api_config else "❌"
            print(f"{status1} Frontend API configuration")
            
            results['frontend_api_config'] = api_config
            
        except Exception as e:
            print(f"❌ Error checking frontend config: {e}")
            results['frontend_config_check'] = False
    
    return results

def main():
    """Run all basic tests"""
    print("🚀 Fuel Control System - Basic Test Suite")
    print("=" * 60)
    
    all_results = {}
    
    # Run tests
    all_results['file_structure'] = test_file_structure()
    all_results['backend_syntax'] = test_backend_syntax()
    all_results['frontend_structure'] = test_frontend_structure()
    all_results['api_endpoints'] = test_api_endpoints()
    all_results['database_scripts'] = test_database_scripts()
    all_results['configuration'] = test_configuration()
    
    # Calculate summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    
    def count_results(results, prefix=""):
        nonlocal total_tests, passed_tests
        if isinstance(results, dict):
            for key, value in results.items():
                if isinstance(value, bool):
                    total_tests += 1
                    if value:
                        passed_tests += 1
                elif isinstance(value, dict):
                    count_results(value, f"{prefix}{key}.")
    
    count_results(all_results)
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Overall assessment
    if success_rate >= 95:
        print("\n🎉 EXCELLENT! System is well-aligned and ready.")
        print("✅ Frontend and backend are properly aligned")
        print("✅ All critical files are present")
        print("✅ Configuration is consistent")
    elif success_rate >= 85:
        print("\n✅ GOOD! System is mostly aligned with minor issues.")
        print("⚠️  Some non-critical components may need attention")
    elif success_rate >= 70:
        print("\n⚠️  FAIR! System has some alignment issues.")
        print("🔧 Several components need fixing")
    else:
        print("\n❌ POOR! Major alignment issues detected.")
        print("🚨 Significant work needed before system can function")
    
    print(f"\nNext steps:")
    if success_rate >= 85:
        print("1. Install dependencies: pip install -r backend/requirements.txt")
        print("2. Configure database in backend/.env")
        print("3. Run database setup scripts")
        print("4. Start the system")
    else:
        print("1. Fix the failed tests above")
        print("2. Re-run this test")
        print("3. Proceed with setup once tests pass")

if __name__ == "__main__":
    main()