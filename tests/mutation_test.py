#!/usr/bin/env python3
"""
Simple mutation testing script for LiteAgent using mutmut.

This script provides basic mutation testing functionality to verify
that our tests can detect meaningful code changes.
"""

import subprocess
import sys
import argparse
import os
from typing import Optional


class MutationTester:
    """Simple mutation testing for LiteAgent."""
    
    def __init__(self):
        self.config_file = ".mutmut_config"
        
    def create_config(self, target_path: str = "liteagent/", 
                     test_command: str = "python -m pytest tests/unit/ -x --tb=short --disable-warnings --reruns=3",
                     timeout: int = 60):
        """Create mutmut configuration file."""
        config_content = f"""[mutmut]
paths_to_mutate = {target_path}
runner = {test_command}
timeout = {timeout}
"""
        with open(self.config_file, "w") as f:
            f.write(config_content)
        print(f"Created config file: {self.config_file}")
        
    def run_mutations(self, max_mutations: int = 10) -> dict:
        """Run mutation testing."""
        print(f"Running up to {max_mutations} mutations...")
        
        try:
            # Run mutmut
            cmd = ["mutmut", "run"]
            if max_mutations < 20:  # Only limit for small numbers
                cmd.extend(["--max-children", str(max_mutations)])
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Mutation testing timed out"
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Error: {str(e)}"
            }
    
    def show_results(self) -> dict:
        """Show mutation test results."""
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
                "stderr": f"Error showing results: {str(e)}"
            }
    
    def cleanup(self):
        """Clean up mutation artifacts."""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            if os.path.exists(".mutmut_cache"):
                subprocess.run(["rm", "-rf", ".mutmut_cache"])
            print("Cleanup completed")
        except Exception as e:
            print(f"Cleanup warning: {e}")


def main():
    parser = argparse.ArgumentParser(description="Simple mutation testing for LiteAgent")
    parser.add_argument("--file", help="Specific file to mutate")
    parser.add_argument("--max-mutations", type=int, default=10, 
                       help="Maximum number of mutations to test")
    parser.add_argument("--timeout", type=int, default=60,
                       help="Timeout for each test run in seconds")
    parser.add_argument("--analyze", action="store_true",
                       help="Show results from previous run")
    parser.add_argument("--cleanup", action="store_true",
                       help="Clean up mutation artifacts")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    tester = MutationTester()
    
    if args.cleanup:
        tester.cleanup()
        return 0
    
    if args.analyze:
        print("Showing mutation test results...")
        result = tester.show_results()
        print(result["stdout"])
        if result["stderr"]:
            print("Errors:", result["stderr"])
        return result["returncode"]
    
    # Setup and run mutations
    target = args.file if args.file else "liteagent/"
    tester.create_config(target, timeout=args.timeout)
    
    print("="*50)
    print("MUTATION TESTING")
    print("="*50)
    
    result = tester.run_mutations(args.max_mutations)
    
    print(f"Mutation testing completed (exit code: {result['returncode']})")
    
    if result["stdout"]:
        print("\nOutput:")
        print(result["stdout"])
    
    if result["stderr"]:
        print("\nErrors:")
        print(result["stderr"])
    
    # Show results
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    
    results = tester.show_results()
    if results["stdout"]:
        print(results["stdout"])
    
    return 0 if result["returncode"] in [0, 2] else 1  # mutmut returns 2 for some mutations killed


if __name__ == "__main__":
    sys.exit(main())