#!/usr/bin/env python3
"""
Mutation testing script for LiteAgent using mutmut.

This script provides targeted mutation testing functionality to verify
that our tests can detect meaningful code changes and catch bugs.
"""

import subprocess
import sys
import argparse
import os
from typing import List, Optional


class MutationTester:
    """Manages mutation testing for LiteAgent."""
    
    def __init__(self, target_path: str = "liteagent/", test_path: str = "tests/unit/"):
        self.target_path = target_path
        self.test_path = test_path
        
    def run_mutation_tests(self, 
                          specific_file: Optional[str] = None,
                          max_mutations: int = 50,
                          timeout: int = 300) -> dict:
        """
        Run mutation tests on the specified target.
        
        Args:
            specific_file: Specific file to mutate (optional)
            max_mutations: Maximum number of mutations to test
            timeout: Timeout for each test run in seconds
            
        Returns:
            Dictionary with mutation test results
        """
        cmd_base = [
            "mutmut", "run",
            "--runner", f"python -m pytest {self.test_path} -x --tb=short --disable-warnings",
            "--timeout", str(timeout),
            "--max-mutations", str(max_mutations)
        ]
        
        if specific_file:
            cmd_base.extend(["--paths-to-mutate", specific_file])
        else:
            cmd_base.extend(["--paths-to-mutate", self.target_path])
            
        print(f"Running mutation tests with command: {' '.join(cmd_base)}")
        
        try:
            result = subprocess.run(cmd_base, capture_output=True, text=True, timeout=timeout*10)
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd_base)
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Mutation testing timed out",
                "command": " ".join(cmd_base)
            }
    
    def analyze_results(self) -> dict:
        """Analyze mutation test results."""
        try:
            result = subprocess.run(["mutmut", "results"], capture_output=True, text=True)
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Error analyzing results: {str(e)}"
            }
    
    def show_survivors(self) -> dict:
        """Show mutations that survived (weren't caught by tests)."""
        try:
            result = subprocess.run(["mutmut", "show", "--survived"], capture_output=True, text=True)
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Error showing survivors: {str(e)}"
            }
    
    def cleanup(self):
        """Clean up mutation test artifacts."""
        try:
            subprocess.run(["mutmut", "reset"], capture_output=True)
            print("Cleaned up mutation test artifacts")
        except Exception as e:
            print(f"Warning: Could not clean up mutation artifacts: {e}")


def main():
    parser = argparse.ArgumentParser(description="Run mutation tests on LiteAgent")
    parser.add_argument("--file", help="Specific file to mutate")
    parser.add_argument("--max-mutations", type=int, default=20, 
                       help="Maximum number of mutations to test")
    parser.add_argument("--timeout", type=int, default=300,
                       help="Timeout for each test run in seconds")
    parser.add_argument("--analyze", action="store_true",
                       help="Analyze existing mutation test results")
    parser.add_argument("--show-survivors", action="store_true",
                       help="Show mutations that weren't caught by tests")
    parser.add_argument("--cleanup", action="store_true",
                       help="Clean up mutation test artifacts")
    
    args = parser.parse_args()
    
    tester = MutationTester()
    
    if args.cleanup:
        tester.cleanup()
        return
        
    if args.analyze:
        result = tester.analyze_results()
        print("Mutation Test Analysis:")
        print(result["stdout"])
        if result["stderr"]:
            print("Errors:")
            print(result["stderr"])
        return
        
    if args.show_survivors:
        result = tester.show_survivors()
        print("Surviving Mutations (not caught by tests):")
        print(result["stdout"])
        if result["stderr"]:
            print("Errors:")
            print(result["stderr"])
        return
    
    # Run mutation tests
    print("Starting mutation testing...")
    result = tester.run_mutation_tests(
        specific_file=args.file,
        max_mutations=args.max_mutations,
        timeout=args.timeout
    )
    
    print(f"Mutation testing completed with return code: {result['returncode']}")
    print("\nSTDOUT:")
    print(result["stdout"])
    
    if result["stderr"]:
        print("\nSTDERR:")
        print(result["stderr"])
    
    # Analyze results after running
    print("\n" + "="*50)
    print("MUTATION TEST ANALYSIS")
    print("="*50)
    
    analysis = tester.analyze_results()
    print(analysis["stdout"])
    
    if analysis["returncode"] == 0:
        print("\nShowing surviving mutations...")
        survivors = tester.show_survivors()
        print(survivors["stdout"])


if __name__ == "__main__":
    main()