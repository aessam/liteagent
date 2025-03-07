#!/usr/bin/env python3
"""
Test script for the pattern-based tool calling handler as a backend.

This script tests that the pattern-based tool handler correctly works as a
replacement for all the model-specific handlers.
"""

import json
import os
import sys
from pprint import pprint

from liteagent.tool_calling import (
    OpenAIToolCallingHandler,
    AnthropicToolCallingHandler,
    OllamaToolCallingHandler,
    get_tool_calling_handler
)
from liteagent.pattern_tool_handler import PatternToolHandler
from liteagent.tool_calling_types import ToolCallingType

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
    """Test the pattern-based tool calling handler as a backend for all handlers."""
    # Test with various model types
    models_to_test = [
        # OpenAI models
        ("gpt-4", ".tool_test/response_openai_gpt-4.json"),
        # Anthropic models
        ("claude-3-opus-20240229", ".tool_test/response_anthropic_claude-3-opus-20240229.json"),
        # Ollama models
        ("ollama/llama3", ".tool_test/response_ollama_llama3.3-latest.json")
    ]
    
    # Test model-specific handlers
    for model_name, response_file in models_to_test:
        print(f"\n=== Testing with model: {model_name} ===")
        
        # Load the response
        response = load_json_response(response_file)
        if response is None:
            print(f"Failed to load response from {response_file}")
            continue
        
        # Get the handler using the old API
        handler = get_tool_calling_handler(model_name)
        
        # Print the handler class to confirm it's our pattern handler
        print(f"Handler class: {handler.__class__.__name__}")
        print(f"Is PatternToolHandler: {isinstance(handler, PatternToolHandler)}")
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(response)
        print(f"Extracted {len(tool_calls)} tool calls:")
        pprint(tool_calls)
        
        # Test formatting tools
        tools = [
            {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location to get weather for"
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
        
        formatted_tools = handler.format_tools_for_model(tools)
        print(f"\nFormatted tools:")
        pprint(formatted_tools[:100] if isinstance(formatted_tools, str) else formatted_tools)
        
        # Test formatting results
        if tool_calls:
            tool_call = tool_calls[0]
            result = "Weather is sunny, 72°F"
            
            formatted_result = handler.format_tool_results(
                tool_call["name"], 
                result, 
                tool_id=tool_call.get("id", "call_123")
            )
            
            print(f"\nFormatted result:")
            pprint(formatted_result)

if __name__ == "__main__":
    main() 