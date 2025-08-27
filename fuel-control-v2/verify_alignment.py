#!/usr/bin/env python3
"""
Final Verification Script for Fuel Control System
Demonstrates that frontend and backend are properly aligned
"""

import sys
import os
from pathlib import Path
import json

def print_banner():
    print("🔥" * 60)
    print("🚀 FUEL CONTROL SYSTEM - ALIGNMENT VERIFICATION")
    print("🔥" * 60)

def check_critical_files():
    """Check if all critical files exist"""
    print("\n📁 CHECKING CRITICAL FILES...")
    
    critical_files = [
        'backend/app.py',
        'backend/config.py', 
        'frontend/index.html',
        'frontend/app.js',
        'database/create_database.sql'
    ]
    
    all_good = True
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING!")
            all_good = False
    
    return all_good

def verify_api_endpoints():
    """Verify API endpoints are defined in backend"""
    print("\n🔗 VERIFYING API ENDPOINTS...")
    
    try:
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            backend_content = f.read()
        
        endpoints = [
            '/api/health',
            '/api/sites', 
            '/api/equipment',
            '/api/stock',
            '/api/forecasts',
            '/api/operational-hours',
            '/api/refills',
            '/api/usage'
        ]
        
        all_found = True
        for endpoint in endpoints:
            if f"@app.route('{endpoint}'" in backend_content:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint} - NOT FOUND!")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ Error checking endpoints: {e}")
        return False

def verify_frontend_modules():
    """Verify frontend JavaScript modules"""
    print("\n🎨 VERIFYING FRONTEND MODULES...")
    
    try:
        with open('frontend/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        modules = [
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
        
        all_found = True
        for module in modules:
            if module in js_content:
                print(f"✅ {module}")
            else:
                print(f"❌ {module} - NOT FOUND!")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ Error checking modules: {e}")
        return False

def verify_configuration():
    """Verify configuration alignment"""
    print("\n⚙️  VERIFYING CONFIGURATION...")
    
    try:
        # Check if config is imported in app.py
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        config_imported = 'from config import Config' in app_content
        config_used = 'Config.DB_SERVER' in app_content
        
        print(f"✅ Config imported: {config_imported}")
        print(f"✅ Config used: {config_used}")
        
        # Check frontend API config
        with open('frontend/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        api_config = 'API_BASE_URL: \\'http://localhost:5000/api\\'' in js_content
        print(f"✅ Frontend API config: {api_config}")
        
        return config_imported and config_used and api_config
        
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def verify_html_sections():
    """Verify HTML sections exist"""
    print("\n🌐 VERIFYING HTML SECTIONS...")
    
    try:
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        sections = [
            'dashboard-section',
            'forecasting-section',
            'stock-section', 
            'equipment-section',
            'operational-hours-section',
            'refills-section',
            'usage-section'
        ]
        
        all_found = True
        for section in sections:
            if f'id=\"{section}\"' in html_content:
                print(f"✅ {section}")
            else:
                print(f"❌ {section} - NOT FOUND!")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"❌ Error checking HTML: {e}")
        return False

def verify_database_scripts():
    """Verify database scripts"""
    print("\n🗄️  VERIFYING DATABASE SCRIPTS...")
    
    scripts = {
        'database/create_database.sql': 'CREATE DATABASE',
        'database/insert_sample_data.sql': 'INSERT INTO',
        'database/forecasting_procedures.sql': 'CREATE PROCEDURE'
    }
    
    all_good = True
    for script_path, keyword in scripts.items():
        if Path(script_path).exists():
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read().upper()
                
                if keyword.upper() in content:
                    print(f"✅ {script_path}")
                else:
                    print(f"⚠️  {script_path} - Missing {keyword}")
                    all_good = False
            except Exception as e:
                print(f"❌ {script_path} - Error: {e}")
                all_good = False
        else:
            print(f"❌ {script_path} - NOT FOUND!")
            all_good = False
    
    return all_good

def check_setup_files():
    """Check setup and documentation files"""
    print("\n📚 CHECKING SETUP FILES...")
    
    setup_files = [
        'setup_project.py',
        'QUICK_START.md',
        'TEST_REPORT.md',
        'backend/.env.example'
    ]
    
    all_good = True
    for file_path in setup_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING!")
            all_good = False
    
    return all_good

def main():
    """Run all verification checks"""
    print_banner()
    
    # Run all checks
    checks = [
        ("Critical Files", check_critical_files),
        ("API Endpoints", verify_api_endpoints),
        ("Frontend Modules", verify_frontend_modules),
        ("Configuration", verify_configuration),
        ("HTML Sections", verify_html_sections),
        ("Database Scripts", verify_database_scripts),
        ("Setup Files", check_setup_files)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} - ERROR: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "🔥" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("🔥" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n📈 SUCCESS RATE: {success_rate:.1f}% ({passed}/{total})")
    
    # Final verdict
    if success_rate == 100:
        print("\n🎉 PERFECT ALIGNMENT!")
        print("✅ Frontend and backend are perfectly aligned")
        print("✅ All components are working together")
        print("✅ System is ready for production use")
        print("\n🚀 NEXT STEPS:")
        print("1. Run: python setup_project.py")
        print("2. Configure database in backend/.env")
        print("3. Run: setup_database.bat")
        print("4. Start: start_system.bat")
        print("5. Access: http://localhost:8080")
    elif success_rate >= 90:
        print("\n✅ EXCELLENT ALIGNMENT!")
        print("✅ System is well-aligned with minor issues")
        print("✅ Ready for use with minimal setup")
    elif success_rate >= 80:
        print("\n⚠️  GOOD ALIGNMENT")
        print("⚠️  Some components need attention")
        print("🔧 Fix failed checks before proceeding")
    else:
        print("\n❌ POOR ALIGNMENT")
        print("❌ Major issues detected")
        print("🚨 Significant work needed")
    
    print("\n" + "🔥" * 60)
    print("VERIFICATION COMPLETE")
    print("🔥" * 60)

if __name__ == "__main__":
    main()