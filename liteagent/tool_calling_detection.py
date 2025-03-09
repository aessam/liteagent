"""
Auto-detection of tool calling formats from model responses.

This module provides helper functions to detect which type of tool calling format
a model response is using, making it possible to automatically handle different
model outputs without explicitly specifying their type.
"""

import json
import re
from typing import Union, Any, Optional, List, Dict, Set

from .xpath_extractor import XPathExtractor
from .tool_calling_types import ToolCallingType

def detect_tool_calling_format(response: Any) -> ToolCallingType:
    """
    Auto-detect the tool calling format used in a model response.
    
    Args:
        response: The model response object
        
    Returns:
        The detected ToolCallingType
    """
    extractor = XPathExtractor()
    
    # Check for OpenAI format: choices/*/message/tool_calls
    # We need to confirm the tool_calls array is non-empty and present
    openai_tool_calls = extractor.get_nodes(response, 'choices/*/message/tool_calls')
    if openai_tool_calls and isinstance(openai_tool_calls, list) and len(openai_tool_calls) > 0:
        return ToolCallingType.OPENAI
    
    # Check for Anthropic format: content blocks with type='tool_use'
    anthropic_tool_calls = extractor.get_nodes(response, 'content/type=tool_use/name')
    if anthropic_tool_calls and isinstance(anthropic_tool_calls, list) and len(anthropic_tool_calls) > 0:
        return ToolCallingType.ANTHROPIC
    
    # Try to detect Ollama-style tool calling in text response
    ollama_tool_calls = extractor.get_nodes(response, 'message/tool_calls/function')
    if ollama_tool_calls and isinstance(ollama_tool_calls, list) and len(ollama_tool_calls) > 0:
        return ToolCallingType.OLLAMA
    
    # Default to structured output format
    return ToolCallingType.STRUCTURED_OUTPUT


def _extract_tools(response_text: str) -> List[Dict]:
    """
    Extract Ollama-style tool calls from text.
    
    Args:
        response_text: The text to extract from
        
    Returns:
        List of extracted tool calls
    """
    tool_calls = []
    
    # Check for [FUNCTION_CALL] format
    function_call_pattern = r'\[FUNCTION_CALL\]\s*(\w+)\((.*?)\)\s*\[/FUNCTION_CALL\]'
    matches = re.findall(function_call_pattern, response_text, re.DOTALL)
    
    if matches:
        for func_name, args_str in matches:
            # Parse the arguments
            args_dict = {}
            
            # Try key=value format
            arg_pattern = r'(\w+)\s*=\s*(?:"([^"]*?)"|\'([^\']*?)\'|([^,\s\)]+))'
            arg_matches = re.findall(arg_pattern, args_str)
            
            if arg_matches:
                for arg_match in arg_matches:
                    key = arg_match[0]
                    # Find the first non-empty value
                    value = next((v for v in arg_match[1:] if v), "")
                    # Convert to appropriate type
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                        value = float(value)
                    args_dict[key] = value
            else:
                # Try positional arguments
                pos_args = [arg.strip() for arg in args_str.split(',')]
                if len(pos_args) > 0:
                    for i, arg in enumerate(pos_args):
                        args_dict[f"arg{i+1}"] = arg
            
            tool_call = {
                "name": func_name,
                "arguments": args_dict,
                "id": f"call_{uuid.uuid4()}"
            }
            
            tool_calls.append(tool_call)
    
    # Also check for code block format
    code_block_pattern = r'```(?:python|json)?(.+?)```'
    matches = re.findall(code_block_pattern, response_text, re.DOTALL)
    
    if matches and not tool_calls:
        for code_block in matches:
            # Look for function calls in the code block
            func_pattern = r'(\w+)\((.*?)\)'
            func_matches = re.findall(func_pattern, code_block)
            
            if func_matches:
                for func_name, args_str in func_matches:
                    # Similar argument parsing as above
                    args_dict = {}
                    
                    # Try key=value format
                    arg_pattern = r'(\w+)\s*=\s*(?:"([^"]*?)"|\'([^\']*?)\'|([^,\s\)]+))'
                    arg_matches = re.findall(arg_pattern, args_str)
                    
                    if arg_matches:
                        for arg_match in arg_matches:
                            key = arg_match[0]
                            value = next((v for v in arg_match[1:] if v), "")
                            if value.isdigit():
                                value = int(value)
                            elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                                value = float(value)
                            args_dict[key] = value
                    else:
                        # Try positional arguments
                        pos_args = [arg.strip() for arg in args_str.split(',')]
                        if len(pos_args) > 0:
                            for i, arg in enumerate(pos_args):
                                args_dict[f"arg{i+1}"] = arg
                    
                    tool_call = {
                        "name": func_name,
                        "arguments": args_dict
                    }
                    
                    tool_calls.append(tool_call)
    
    return tool_calls 