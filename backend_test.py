#!/usr/bin/env python3
"""
Backend Test for Flight Management System
Tests the HTTP server and file accessibility
"""

import requests
import sys
import os
from datetime import datetime

class FlightSystemTester:
    def __init__(self, base_url="http://localhost:8081"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
            else:
                print(f"❌ Failed")
            return success
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_server_accessibility(self):
        """Test if the HTTP server is accessible"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def test_main_page_content(self):
        """Test if main page contains expected content"""
        try:
            response = requests.get(self.base_url, timeout=5)
            content = response.text
            return (
                "New Dubai International Airport" in content and
                "Backup" in content and
                "Importar Voos" in content
            )
        except Exception:
            return False

    def test_csv_file_exists(self):
        """Test if the flights.csv file exists"""
        return os.path.exists("/app/flights.csv")

    def test_csv_file_content(self):
        """Test if CSV file has expected content"""
        try:
            with open("/app/flights.csv", 'r') as f:
                content = f.read()
                lines = content.strip().split('\n')
                # Should have header + 9 data lines
                return (
                    len(lines) == 10 and
                    "VIRGIN ATLANTIC USA" in content and
                    "VARESH AIRLINES" in content and
                    "IRAN" in content
                )
        except Exception:
            return False

    def test_javascript_files(self):
        """Test if required JavaScript files exist"""
        return os.path.exists("/app/unified_import_export.js")

    def test_logos_directory(self):
        """Test if logos directory exists with some files"""
        try:
            logos_dir = "/app/logos"
            if not os.path.exists(logos_dir):
                return False
            files = os.listdir(logos_dir)
            return len(files) > 0
        except Exception:
            return False

    def test_flags_directory(self):
        """Test if flags directory exists with some files"""
        try:
            flags_dir = "/app/flags"
            if not os.path.exists(flags_dir):
                return False
            files = os.listdir(flags_dir)
            return len(files) > 0
        except Exception:
            return False

def main():
    """Run all tests"""
    print("🚀 Starting Flight Management System Backend Tests")
    print("=" * 60)
    
    tester = FlightSystemTester()
    
    # Run tests
    tests = [
        ("HTTP Server Accessibility", tester.test_server_accessibility),
        ("Main Page Content", tester.test_main_page_content),
        ("CSV File Exists", tester.test_csv_file_exists),
        ("CSV File Content", tester.test_csv_file_content),
        ("JavaScript Files", tester.test_javascript_files),
        ("Logos Directory", tester.test_logos_directory),
        ("Flags Directory", tester.test_flags_directory),
    ]
    
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
    
    # Print results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All backend tests passed! System is ready for frontend testing.")
        return 0
    else:
        print("⚠️  Some backend tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())