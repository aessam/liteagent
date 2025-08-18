#!/usr/bin/env python3
"""
Test runner for LiteAgent with mutation testing support.

This script provides a unified interface to run different types of tests:
- Unit tests
- Integration tests  
- Mutation tests
"""

import argparse
import subprocess
import sys
import time
import os
from pathlib import Path


def run_unit_tests(verbose=False):
    """Run standard unit tests."""
    print("🧪 Running Unit Tests...")
    cmd = ["python", "-m", "pytest", "tests/unit/", "-v" if verbose else "-q", "--tb=short"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"Unit Tests: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")
    if verbose or result.returncode != 0:
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_integration_tests(verbose=False, provider=None):
    """Run integration tests, optionally for specific provider."""
    print("🔌 Running Integration Tests...")
    
    cmd = ["python", "-m", "pytest", "tests/integration/", "-v" if verbose else "-q", "--tb=short"]
    
    if provider:
        # Filter by provider using pytest markers or model names
        cmd.extend(["-k", provider])
        print(f"   Filtering for provider: {provider}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
    
    print(f"Integration Tests: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")
    if verbose or result.returncode != 0:
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_mutation_tests(max_mutations=20, specific_file=None, verbose=False):
    """Run mutation tests using the mutation testing framework."""
    print("🧬 Running Mutation Tests...")
    
    cmd = ["python", "tests/mutation_test.py"]
    
    if specific_file:
        cmd.extend(["--file", specific_file])
    
    cmd.extend(["--max-mutations", str(max_mutations)])
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
        
        print(f"Mutation Tests: {'✅ COMPLETED' if result.returncode == 0 else '❌ FAILED'}")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Mutation tests timed out after 1 hour")
        return False
    except Exception as e:
        print(f"❌ Error running mutation tests: {e}")
        return False




def run_quick_smoke_tests():
    """Run a quick smoke test to verify basic functionality."""
    print("💨 Running Quick Smoke Tests...")
    
    cmd = [
        "python", "-m", "pytest", 
        "tests/integration/consolidated/test_standalone_tools.py::TestStandaloneTools::test_weather_tool[model0]",
        "tests/integration/consolidated/test_class_method_tools.py::TestClassMethodTools::test_add_numbers_class_method[model0]",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    
    print(f"Smoke Tests: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")
    if result.returncode != 0:
        print(result.stdout[-1000:])  # Last 1000 chars
    
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="LiteAgent Test Runner")
    
    # Test type selection
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--mutation", action="store_true", help="Run mutation tests")
    parser.add_argument("--smoke", action="store_true", help="Run quick smoke tests")
    parser.add_argument("--all", action="store_true", help="Run all test types")
    
    # Options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--provider", help="Filter tests by provider (openai, anthropic, groq, etc.)")
    parser.add_argument("--max-mutations", type=int, default=20, help="Max mutations for mutation testing")
    parser.add_argument("--mutation-file", help="Specific file for mutation testing")
    
    args = parser.parse_args()
    
    if not any([args.unit, args.integration, args.mutation, args.smoke, args.all]):
        print("❌ No test type specified. Use --help for options.")
        return 1
    
    print("🚀 LiteAgent Test Runner")
    print("=" * 60)
    
    results = []
    start_time = time.time()
    
    if args.all or args.smoke:
        results.append(("Smoke Tests", run_quick_smoke_tests()))
    
    if args.all or args.unit:
        results.append(("Unit Tests", run_unit_tests(args.verbose)))
    
    if args.all or args.integration:
        results.append(("Integration", run_integration_tests(args.verbose, args.provider)))
    
    if args.all or args.mutation:
        results.append(("Mutation", run_mutation_tests(args.max_mutations, args.mutation_file, args.verbose)))
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    print(f"\n📈 Overall: {passed}/{total} test suites passed ({passed/total*100:.1f}%)")
    print(f"⏱️  Duration: {duration:.1f} seconds")
    
    if passed == total:
        print("🎉 All test suites passed!")
        return 0
    else:
        print("💥 Some test suites failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())