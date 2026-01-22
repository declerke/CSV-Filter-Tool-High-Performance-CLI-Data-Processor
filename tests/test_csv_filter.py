import subprocess
import os
import sys
import csv
from pathlib import Path

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
        self.script_name = 'csv_filter.py'
    
    def create_test_data(self):
        data = [
            ['name', 'age', 'city', 'department', 'salary'],
            ['Alice', '25', 'New York', 'Engineering', '75000'],
            ['Bob', '30', 'Los Angeles', 'Sales', '65000'],
            ['Charlie', '25', 'New York', 'Marketing', '60000'],
            ['Diana', '28', 'Chicago', 'Engineering', '80000'],
            ['Eve', '32', 'New York', 'Sales', '70000'],
            ['Frank', '25', 'Boston', 'Engineering', '72000'],
            ['Grace', '29', 'San Francisco', 'Marketing', '68000'],
            ['Henry', '31', 'New York', 'Engineering', '85000'],
        ]
        
        with open('test_data.csv', 'w', newline='') as f:
            csv.writer(f).writerows(data)
        
        print(f"{BLUE}Created test_data.csv (8 rows){RESET}")
    
    def cleanup(self):
        files_to_remove = [
            'test_data.csv', 'test_output.csv', 'filtered.csv',
            'preview_test.csv', 'exact_match.csv', 'contains_match.csv'
        ]
        for filename in files_to_remove:
            if os.path.exists(filename):
                os.remove(filename)

    def run_command(self, cmd):
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return result.returncode, result.stdout, result.stderr
    
    def test(self, test_name, cmd, expected_file=None, expected_rows=None):
        self.tests_run += 1
        print(f"\n{YELLOW}Test {self.tests_run}: {test_name}{RESET}")
        print(f"Command: {cmd}")
        
        rc, stdout, stderr = self.run_command(cmd)
        
        if rc != 0 and expected_file is not None:
            print(f"{RED}✗ FAILED - Command returned error code {rc}{RESET}")
            if stderr: print(f"Error: {stderr}")
            self.failed += 1
            return False
        
        if expected_file:
            if not os.path.exists(expected_file):
                print(f"{RED}✗ FAILED - Expected file '{expected_file}' not created{RESET}")
                self.failed += 1
                return False
            
            if expected_rows is not None:
                with open(expected_file, 'r') as f:
                    row_count = sum(1 for _ in f) - 1
                
                if row_count != expected_rows:
                    print(f"{RED}✗ FAILED - Expected {expected_rows} rows, got {row_count}{RESET}")
                    self.failed += 1
                    return False
        
        print(f"{GREEN}✓ PASSED{RESET}")
        self.passed += 1
        return True

    def run_all_tests(self):
        print("=" * 80)
        print(f"{BLUE}CSV Filter Tool - Test Suite{RESET}")
        print("=" * 80)
        
        self.create_test_data()
        
        self.test(
            "Exact match on numeric column (age=25)",
            f'python {self.script_name} test_data.csv --column age --value 25 --output exact_match.csv',
            expected_file="exact_match.csv",
            expected_rows=3
        )
        
        self.test(
            "Exact match on string column (city='New York')",
            f'python {self.script_name} test_data.csv --column city --value "New York" --output test_output.csv',
            expected_file="test_output.csv",
            expected_rows=4
        )
        
        self.test(
            "Partial match with --contains (city contains 'York')",
            f'python {self.script_name} test_data.csv --column city --value York --contains --output contains_match.csv',
            expected_file="contains_match.csv",
            expected_rows=4
        )
        
        self.test(
            "Preview mode (should not create file)",
            f'python {self.script_name} test_data.csv --column department --value Engineering --preview',
            expected_file=None
        )
        
        self.test(
            "Default output filename (filtered.csv)",
            f'python {self.script_name} test_data.csv --column department --value Sales',
            expected_file="filtered.csv",
            expected_rows=2
        )
        
        print(f"\n{YELLOW}Test {self.tests_run + 1}: Error handling - column not found{RESET}")
        rc, out, err = self.run_command(f'python {self.script_name} test_data.csv --column nonexistent --value test')
        if rc != 0 and "not found" in (out + err).lower():
            print(f"{GREEN}✓ PASSED - Correctly handled missing column{RESET}")
            self.passed += 1
        else:
            print(f"{RED}✗ FAILED - Did not handle missing column correctly{RESET}")
            self.failed += 1
        self.tests_run += 1
        
        print(f"\n{YELLOW}Test {self.tests_run + 1}: Error handling - file not found{RESET}")
        rc, out, err = self.run_command(f'python {self.script_name} nonexistent.csv --column test --value test')
        if rc != 0 and "not found" in (out + err).lower():
            print(f"{GREEN}✓ PASSED - Correctly handled missing file{RESET}")
            self.passed += 1
        else:
            print(f"{RED}✗ FAILED - Did not handle missing file correctly{RESET}")
            self.failed += 1
        self.tests_run += 1
        
        self.test(
            "Case-insensitive contains (city contains 'york' lowercase)",
            f'python {self.script_name} test_data.csv --column city --value york --contains --output test_output.csv',
            expected_file="test_output.csv",
            expected_rows=4
        )
        
        print("\n" + "=" * 80)
        print(f"{BLUE}📊 Test Summary{RESET}")
        print("=" * 80)
        print(f"Total tests run: {self.tests_run}")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        print(f"{RED}Failed: {self.failed}{RESET}")
        
        if self.failed == 0:
            print(f"\n{GREEN}All tests passed!{RESET}")
        else:
            print(f"\n{RED}Some tests failed{RESET}")
        
        self.cleanup()
        return self.failed == 0

def main():
    if not os.path.exists('csv_filter.py'):
        sys.exit(1)
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()