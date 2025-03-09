#!/usr/bin/env python3
"""
Tool for detecting the tool calling format in LLM responses.

This tool takes a JSON file containing a response from an LLM and determines
what style of tool calling it uses (OpenAI, Anthropic, Ollama, etc.).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to sys.path to allow importing liteagent
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liteagent.handlers.auto_detect_handler import AutoDetectToolCallingHandler
from liteagent.tool_calling_detection import detect_tool_calling_format
from liteagent.tool_calling_types import ToolCallingType


def main():
    """
    Main entry point for the tool.
    """
    parser = argparse.ArgumentParser(description="Detect tool calling format from LLM response JSON files")
    parser.add_argument("file", help="Path to the JSON file containing the LLM response")
    parser.add_argument("--json", action="store_true", help="Output the result as JSON")
    args = parser.parse_args()
    
    try:
        # Load the JSON file
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Use the existing detector function
        detected_type = detect_tool_calling_format(data)
        # Format the result
        result = {
            "file": args.file,
            "type": detected_type.name,
            "description": {
                ToolCallingType.NONE: "No tool calling support detected",
                ToolCallingType.OPENAI: "OpenAI-style function calling format",
                ToolCallingType.ANTHROPIC: "Anthropic-style tool calling format",
                ToolCallingType.GROQ: "Groq-style tool calling format (OpenAI-compatible)",
                ToolCallingType.OLLAMA: "Ollama-style tool calling format (text-based JSON)",
                ToolCallingType.TEXT_BASED: "Generic text-based function call pattern",
                ToolCallingType.STRUCTURED_OUTPUT: "Structured output format (non-specific tool calling)"
            }.get(detected_type, "Unknown format")
        }
        
        # Output the result
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {args.file}")
            print(f"Detected tool calling format: {result['type']}")
            print(f"Description: {result['description']}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 