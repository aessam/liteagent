#!/usr/bin/env python3
"""
Test script for the pattern-based tool calling handler.

This script loads a sample response from a file and tests the pattern-based handler
to verify that it can correctly extract tool calls and format results.
"""

import json
import os
import argparse
import logging
from pprint import pprint

from liteagent.pattern_tool_handler import PatternToolHandler

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(message)s')

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
    """Test the pattern-based tool calling handler."""
    parser = argparse.ArgumentParser(description="Test the pattern-based tool calling handler")
    parser.add_argument("file", help="Path to the response file")
    args = parser.parse_args()
    
    # Load the response
    response = load_json_response(args.file)
    if response is None:
        print(f"Failed to load response from {args.file}")
        return
    
    # Create the handler
    handler = PatternToolHandler()
    
    # Extract tool calls
    print(f"Processing response from {args.file}")
    pattern = handler.detect_pattern(response)
    if pattern:
        print(f"Detected pattern: {pattern.id}")
        print(f"Response structure: {json.dumps(response, indent=2)[:500]}...")
        
        # Debug the extraction configuration
        extraction = pattern.extraction
        print(f"\nExtraction configuration:")
        pprint(extraction)
        
        # For Anthropic responses, manually check for tool_use items
        if "content" in response and isinstance(response["content"], list):
            tool_use_items = []
            for i, item in enumerate(response["content"]):
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    tool_use_items.append(item)
            
            if tool_use_items:
                print(f"\nFound {len(tool_use_items)} tool_use items in content:")
                pprint(tool_use_items)
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(response)
        print(f"\nExtracted {len(tool_calls)} tool calls:")
        pprint(tool_calls)
        
        # Test formatting results
        if tool_calls:
            # Mock results
            results = ["Weather is sunny, 72°F"] * len(tool_calls)
            
            # Format results
            formatted_results = handler.format_multiple_tool_results(pattern.id, tool_calls, results)
            print("\nFormatted results:")
            pprint(formatted_results)
    else:
        print("No pattern detected for this response")

if __name__ == "__main__":
    main() 