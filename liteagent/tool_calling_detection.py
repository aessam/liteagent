"""
Auto-detection of tool calling formats from model responses.

This module provides helper functions to detect which type of tool calling format
a model response is using, making it possible to automatically handle different
model outputs without explicitly specifying their type.
"""

import json
import re
from typing import Union, Any, Optional, List, Dict, Set

from .tool_calling_types import ToolCallingType

def detect_tool_calling_format(response: Any) -> ToolCallingType:
    """
    Auto-detect the tool calling format used in a model response.
    
    Args:
        response: The model response object
        
    Returns:
        The detected ToolCallingType
    """
    # Extract response text if available
    response_text = _extract_response_text(response)
    
    # Try to detect OpenAI-style tool calling
    if _detect_openai_format(response):
        return ToolCallingType.OPENAI
    
    # Try to detect Anthropic-style tool calling
    if _detect_anthropic_format(response):
        return ToolCallingType.ANTHROPIC
    
    # Try to detect Ollama-style tool calling in text response
    if _detect_ollama_format(response_text):
        return ToolCallingType.OLLAMA
    
    # Default to structured output format
    return ToolCallingType.STRUCTURED_OUTPUT


def _extract_response_text(response: Any) -> str:
    """
    Extract the text content from a model response.
    
    Args:
        response: The model response object
        
    Returns:
        The extracted text or empty string if no text is found
    """
    # Try various response formats that might contain text
    try:
        # OpenAI/LiteLLM wrapped response format
        if hasattr(response, 'choices') and response.choices:
            if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                if response.choices[0].message.content:
                    return response.choices[0].message.content
        
        # Anthropic direct API format
        if hasattr(response, 'content') and isinstance(response.content, list):
            content_text = ""
            for item in response.content:
                if hasattr(item, 'type') and item.type == 'text':
                    if hasattr(item, 'text'):
                        content_text += item.text + "\n"
            if content_text:
                return content_text
                
        # Ollama format
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            return response.message.content
            
        # Raw string or dict
        if isinstance(response, str):
            return response
        if isinstance(response, dict) and 'content' in response:
            if isinstance(response['content'], str):
                return response['content']
                
    except:
        # Fallback for any errors during extraction
        pass
        
    return ""


def _detect_openai_format(response: Any) -> bool:
    """
    Detect if the response uses OpenAI-style function calling.
    
    Args:
        response: The model response
        
    Returns:
        True if OpenAI format is detected
    """
    # Check for OpenAI-style tool_calls in the response
    try:
        if hasattr(response, 'choices') and response.choices:
            if hasattr(response.choices[0], 'message'):
                message = response.choices[0].message
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    return True
    except:
        pass
    
    return False


def _detect_anthropic_format(response: Any) -> bool:
    """
    Detect if the response uses Anthropic-style tool calling.
    
    Args:
        response: The model response
        
    Returns:
        True if Anthropic format is detected
    """
    # Check for Anthropic-style tool_use blocks
    try:
        # Direct Anthropic API format
        if hasattr(response, 'content') and isinstance(response.content, list):
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'tool_use':
                    return True
        
        # LiteLLM wrapped format
        if hasattr(response, 'choices') and response.choices:
            if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                if isinstance(response.choices[0].message.content, list):
                    for block in response.choices[0].message.content:
                        if hasattr(block, 'type') and block.type == 'tool_use':
                            return True
    except:
        pass
        
    return False


def _detect_ollama_format(response_text: str) -> bool:
    """
    Detect if the response uses Ollama-style function calling in text.
    
    Args:
        response_text: The text response from the model
        
    Returns:
        True if Ollama format is detected
    """
    # Check for common patterns that indicate text-based function calls
    
    # Check for [FUNCTION_CALL] format
    if "[FUNCTION_CALL]" in response_text and "[/FUNCTION_CALL]" in response_text:
        return True
    
    # Check for code block format that might be used
    if "```" in response_text and "(" in response_text and ")" in response_text:
        # This might be a code block with a function call
        return True
    
    # Check for direct function call patterns
    function_call_pattern = r'(\w+)\s*\(\s*[\'\"a-zA-Z0-9_]+\s*[=:]\s*[\'\"a-zA-Z0-9_]+\s*\)'
    if re.search(function_call_pattern, response_text):
        return True
    
    return False


def extract_tool_calls_from_text(tool_calling_type: ToolCallingType, response_text: str) -> List[Dict]:
    """
    Extract tool calls from text based on the specified tool calling type.
    
    Args:
        tool_calling_type: The tool calling type to use for extraction
        response_text: The text to extract tool calls from
        
    Returns:
        List of extracted tool calls
    """
    # Handle different extraction strategies based on tool calling type
    if tool_calling_type == ToolCallingType.OPENAI:
        return _extract_tools_from_openai_text(response_text)
    elif tool_calling_type == ToolCallingType.ANTHROPIC:
        return _extract_tools_from_anthropic_text(response_text)
    elif tool_calling_type == ToolCallingType.OLLAMA:
        return _extract_tools_from_ollama_text(response_text)
    
    # For STRUCTURED_OUTPUT or NONE, return empty list
    return []


def _extract_tools_from_openai_text(response_text: str) -> List[Dict]:
    """
    Extract OpenAI-style tool calls from text.
    
    Args:
        response_text: The text to extract from
        
    Returns:
        List of extracted tool calls
    """
    # Look for JSON objects that look like function calls
    tool_calls = []
    
    # Find all JSON objects in the text
    json_pattern = r'{.*?}'
    json_matches = re.findall(json_pattern, response_text, re.DOTALL)
    
    for json_str in json_matches:
        try:
            # Try to parse as JSON
            data = json.loads(json_str)
            
            # Check if it looks like a function call
            if 'function' in data and 'name' in data['function']:
                name = data['function']['name']
                arguments = data['function'].get('arguments', {})
                
                # Convert string arguments to dict if needed
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except:
                        arguments = {}
                
                tool_call_id = data.get('id', str(uuid.uuid4()))
                
                tool_call = {
                    "name": name,
                    "arguments": arguments,
                    "id": tool_call_id
                }
                
                tool_calls.append(tool_call)
        except:
            pass
    
    return tool_calls


def _extract_tools_from_anthropic_text(response_text: str) -> List[Dict]:
    """
    Extract Anthropic-style tool calls from text.
    
    Args:
        response_text: The text to extract from
        
    Returns:
        List of extracted tool calls
    """
    # For Anthropic, look for <tool></tool> blocks or similar patterns
    tool_calls = []
    
    # Look for <tool:NAME> or similar patterns
    tool_pattern = r'<tool(?::|name=|:name=)([^>]+)>(.*?)</tool>'
    tool_matches = re.findall(tool_pattern, response_text, re.DOTALL)
    
    for name, content in tool_matches:
        try:
            # Try to parse content as JSON
            arguments = json.loads(content.strip())
            
            tool_call = {
                "name": name.strip(),
                "arguments": arguments,
                "id": f"call_{uuid.uuid4()}"
            }
            
            tool_calls.append(tool_call)
        except:
            # If JSON parsing fails, use the raw content
            tool_call = {
                "name": name.strip(),
                "arguments": {"input": content.strip()},
                "id": f"call_{uuid.uuid4()}"
            }
            
            tool_calls.append(tool_call)
    
    return tool_calls


def _extract_tools_from_ollama_text(response_text: str) -> List[Dict]:
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
                        "arguments": args_dict,
                        "id": f"call_{uuid.uuid4()}"
                    }
                    
                    tool_calls.append(tool_call)
    
    return tool_calls 