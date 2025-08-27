#!/usr/bin/env python3
"""
Comprehensive Test Suite for Advanced Fuel Control & Forecasting System
Tests frontend-backend alignment and functionality
"""

import sys
import os
import subprocess
import time
import requests
import json
from pathlib import Path
import threading
import signal

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.test_results = []
        
    def print_header(self, title):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD} {title}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    def print_test(self, test_name, status, message=""):
        status_color = Colors.GREEN if status == "PASS" else Colors.RED if status == "FAIL" else Colors.YELLOW
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {Colors.BOLD}{test_name}{Colors.END}: {status_color}{status}{Colors.END}")
        if message:
            print(f"   {Colors.WHITE}{message}{Colors.END}")
        
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message
        })
    
    def test_prerequisites(self):
        """Test system prerequisites"""
        self.print_header("Testing Prerequisites")
        
        # Test Python version
        if sys.version_info >= (3, 8):
            self.print_test("Python Version", "PASS", f"Python {sys.version.split()[0]}")
        else:
            self.print_test("Python Version", "FAIL", f"Python {sys.version.split()[0]} < 3.8")
        
        # Test required packages
        required_packages = ['flask', 'flask_cors', 'pyodbc', 'python-dotenv']
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.print_test(f"Package: {package}", "PASS")
            except ImportError:
                self.print_test(f"Package: {package}", "FAIL", "Not installed")
        
        # Test SQL Server drivers
        try:
            import pyodbc
            drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
            if drivers:
                self.print_test("SQL Server Drivers", "PASS", f"Found: {', '.join(drivers)}")
            else:
                self.print_test("SQL Server Drivers", "WARN", "No SQL Server drivers found")
        except Exception as e:
            self.print_test("SQL Server Drivers", "FAIL", str(e))
    
    def test_file_structure(self):
        """Test project file structure"""
        self.print_header("Testing File Structure")
        
        required_files = [
            'backend/app.py',
            'backend/config.py', 
            'backend/requirements.txt',
            'frontend/index.html',
            'frontend/app.js',
            'frontend/styles.css',
            'database/create_database.sql',
            'database/insert_sample_data.sql',
            'database/forecasting_procedures.sql'
        ]
        
        for file_path in required_files:
            if Path(file_path).exists():
                self.print_test(f"File: {file_path}", "PASS")
            else:
                self.print_test(f"File: {file_path}", "FAIL", "Missing")
        
        # Test configuration files
        env_example = Path("backend/.env.example")
        env_file = Path("backend/.env")
        
        if env_example.exists():
            self.print_test("Environment Template", "PASS", ".env.example exists")
        else:
            self.print_test("Environment Template", "FAIL", ".env.example missing")
        
        if env_file.exists():
            self.print_test("Environment Config", "PASS", ".env exists")
        else:
            self.print_test("Environment Config", "WARN", ".env not configured")
    
    def test_backend_syntax(self):
        """Test backend Python syntax"""
        self.print_header("Testing Backend Syntax")
        
        python_files = [
            'backend/app.py',
            'backend/config.py',
            'setup_project.py'
        ]
        
        for file_path in python_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        compile(f.read(), file_path, 'exec')
                    self.print_test(f"Syntax: {file_path}", "PASS")
                except SyntaxError as e:
                    self.print_test(f"Syntax: {file_path}", "FAIL", f"Line {e.lineno}: {e.msg}")
                except Exception as e:
                    self.print_test(f"Syntax: {file_path}", "FAIL", str(e))
    
    def test_frontend_files(self):
        """Test frontend file integrity"""
        self.print_header("Testing Frontend Files")
        
        # Test HTML structure
        try:
            with open('frontend/index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            required_elements = [
                'id="dashboard-section"',
                'id="forecasting-section"',
                'id="stock-section"',
                'id="equipment-section"',
                'id="operational-hours-section"',
                'id="refills-section"',
                'id="usage-section"'
            ]
            
            for element in required_elements:
                if element in html_content:
                    self.print_test(f"HTML Element: {element}", "PASS")
                else:
                    self.print_test(f"HTML Element: {element}", "FAIL", "Missing")
        
        except Exception as e:
            self.print_test("HTML Structure", "FAIL", str(e))
        
        # Test JavaScript structure
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
            
            for class_name in required_classes:
                if class_name in js_content:
                    self.print_test(f"JS Class: {class_name}", "PASS")
                else:
                    self.print_test(f"JS Class: {class_name}", "FAIL", "Missing")
        
        except Exception as e:
            self.print_test("JavaScript Structure", "FAIL", str(e))
    
    def start_backend(self):
        """Start the backend server"""
        try:
            # Change to backend directory and start server
            backend_env = os.environ.copy()
            backend_env['PYTHONPATH'] = os.path.abspath('backend')
            
            self.backend_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                cwd='backend',
                env=backend_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"Backend failed to start:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            print(f"Error starting backend: {e}")
            return False
    
    def test_backend_api(self):
        """Test backend API endpoints"""
        self.print_header("Testing Backend API")
        
        # Start backend server
        if not self.start_backend():
            self.print_test("Backend Startup", "FAIL", "Could not start backend server")
            return
        
        self.print_test("Backend Startup", "PASS", "Server started on port 5000")
        
        # Test API endpoints
        base_url = "http://localhost:5000/api"
        
        endpoints = [
            '/health',
            '/sites',
            '/fuel-types',
            '/equipment',
            '/stock',
            '/forecasts',
            '/operational-hours',
            '/refills',
            '/usage'
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    self.print_test(f"API: {endpoint}", "PASS", f"Status: {response.status_code}")
                elif response.status_code == 500:
                    # Server error - likely database connection issue
                    self.print_test(f"API: {endpoint}", "WARN", f"Status: {response.status_code} (Database issue?)")
                else:
                    self.print_test(f"API: {endpoint}", "FAIL", f"Status: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                self.print_test(f"API: {endpoint}", "FAIL", "Connection refused")
            except requests.exceptions.Timeout:
                self.print_test(f"API: {endpoint}", "FAIL", "Request timeout")
            except Exception as e:
                self.print_test(f"API: {endpoint}", "FAIL", str(e))
    
    def test_database_connection(self):
        """Test database connectivity"""
        self.print_header("Testing Database Connection")
        
        try:
            # Test health endpoint which includes database check
            response = requests.get("http://localhost:5000/api/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get('database') == 'connected':
                    self.print_test("Database Connection", "PASS", "Connected successfully")
                else:
                    self.print_test("Database Connection", "FAIL", "Database disconnected")
            else:
                self.print_test("Database Connection", "FAIL", f"Health check failed: {response.status_code}")
        
        except Exception as e:
            self.print_test("Database Connection", "FAIL", str(e))
    
    def test_frontend_backend_integration(self):
        """Test frontend-backend integration"""
        self.print_header("Testing Frontend-Backend Integration")
        
        # Test CORS configuration
        try:
            headers = {
                'Origin': 'http://localhost:8080',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options("http://localhost:5000/api/health", headers=headers, timeout=5)
            
            if 'Access-Control-Allow-Origin' in response.headers:
                self.print_test("CORS Configuration", "PASS", "CORS headers present")
            else:
                self.print_test("CORS Configuration", "FAIL", "CORS headers missing")
        
        except Exception as e:
            self.print_test("CORS Configuration", "FAIL", str(e))
        
        # Test API response format
        try:
            response = requests.get("http://localhost:5000/api/sites", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.print_test("API Response Format", "PASS", "Returns JSON array")
                else:
                    self.print_test("API Response Format", "WARN", f"Returns: {type(data)}")
            else:
                self.print_test("API Response Format", "FAIL", f"Status: {response.status_code}")
        
        except Exception as e:
            self.print_test("API Response Format", "FAIL", str(e))
    
    def cleanup(self):
        """Clean up test processes"""
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        total_tests = len(self.test_results)
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.test_results if r['status'] == 'WARN'])
        
        print(f"\n{Colors.BOLD}Total Tests: {total_tests}{Colors.END}")
        print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.END}")
        print(f"{Colors.RED}❌ Failed: {failed}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Warnings: {warnings}{Colors.END}")
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.END}")
        
        if failed > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}Failed Tests:{Colors.END}")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  ❌ {result['test']}: {result['message']}")
        
        if warnings > 0:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}Warnings:{Colors.END}")
            for result in self.test_results:
                if result['status'] == 'WARN':
                    print(f"  ⚠️  {result['test']}: {result['message']}")
        
        # Overall assessment
        if failed == 0 and warnings <= 2:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 SYSTEM IS READY FOR USE!{Colors.END}")
        elif failed <= 2:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  SYSTEM HAS MINOR ISSUES{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ SYSTEM NEEDS ATTENTION{Colors.END}")
    
    def run_all_tests(self):
        """Run all tests"""
        try:
            self.print_header("Advanced Fuel Control System - Comprehensive Test Suite")
            
            self.test_prerequisites()
            self.test_file_structure()
            self.test_backend_syntax()
            self.test_frontend_files()
            self.test_backend_api()
            self.test_database_connection()
            self.test_frontend_backend_integration()
            
            self.print_summary()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Test suite error: {e}{Colors.END}")
        finally:
            self.cleanup()

def main():
    """Main test function"""
    runner = TestRunner()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print(f"\n{Colors.YELLOW}Cleaning up...{Colors.END}")
        runner.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    runner.run_all_tests()

if __name__ == "__main__":
    main()