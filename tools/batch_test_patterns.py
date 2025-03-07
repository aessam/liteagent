#!/usr/bin/env python3
"""
Batch test script for the pattern-based tool calling handler.

This script processes all response files in the .tool_test directory and
summarizes which patterns were detected for each file.
"""

import json
import os
import glob
from collections import defaultdict

from liteagent.pattern_tool_handler import PatternToolHandler

def load_json_response(file_path):
    """Load a JSON response from a file."""
    try:
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Try loading line by line (some files have invalid JSON)
                lines = f.readlines()
                if len(lines) == 1:
                    return json.loads(lines[0])
                else:
                    return [json.loads(line) for line in lines]
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

def main():
    """Batch test the pattern-based tool calling handler."""
    # Get all JSON files in the .tool_test directory
    json_files = glob.glob(".tool_test/*.json")
    
    # Create the handler
    handler = PatternToolHandler()
    
    # Track results
    results = {
        "pattern_matches": defaultdict(list),
        "no_pattern": [],
        "extraction_results": defaultdict(list),
        "format_results": defaultdict(list),
        "issues": []
    }
    
    # Process each file
    for file_path in sorted(json_files):
        try:
            # Load the response
            response = load_json_response(file_path)
            if response is None:
                results["issues"].append(f"Failed to load {file_path}")
                continue
            
            # Detect pattern
            pattern = handler.detect_pattern(response)
            if pattern:
                results["pattern_matches"][pattern.id].append(file_path)
                
                # Try extraction
                tool_calls = handler.extract_tool_calls(response)
                if tool_calls:
                    results["extraction_results"]["success"].append(file_path)
                    
                    # Test formatting
                    try:
                        mock_results = ["Weather is sunny, 72°F"] * len(tool_calls)
                        handler.format_multiple_tool_results(pattern.id, tool_calls, mock_results)
                        results["format_results"]["success"].append(file_path)
                    except Exception as e:
                        results["format_results"]["failed"].append((file_path, str(e)))
                else:
                    results["extraction_results"]["no_tools"].append(file_path)
            else:
                results["no_pattern"].append(file_path)
                
        except Exception as e:
            results["issues"].append(f"Error processing {file_path}: {e}")
    
    # Print summary
    print("=== PATTERN DETECTION SUMMARY ===")
    print(f"Total files processed: {len(json_files)}")
    print(f"Files with no pattern match: {len(results['no_pattern'])}")
    
    print("\n=== PATTERN MATCHES ===")
    for pattern_id, files in results["pattern_matches"].items():
        print(f"{pattern_id}: {len(files)} files")
    
    print("\n=== EXTRACTION RESULTS ===")
    print(f"Successful extractions: {len(results['extraction_results']['success'])}")
    print(f"No tools found: {len(results['extraction_results']['no_tools'])}")
    
    print("\n=== FORMAT RESULTS ===")
    print(f"Successful formatting: {len(results['format_results']['success'])}")
    print(f"Failed formatting: {len(results['format_results']['failed'])}")
    
    if results["issues"]:
        print("\n=== ISSUES ===")
        for issue in results["issues"]:
            print(f"- {issue}")
    
    # Print detailed results for each pattern
    print("\n=== DETAILED PATTERN MATCHES ===")
    for pattern_id, files in results["pattern_matches"].items():
        print(f"\n== {pattern_id} ==")
        for file in files:
            print(f"- {os.path.basename(file)}")
    
    # Print files with no pattern match
    if results["no_pattern"]:
        print("\n=== FILES WITH NO PATTERN MATCH ===")
        for file in results["no_pattern"]:
            print(f"- {os.path.basename(file)}")

if __name__ == "__main__":
    main() 