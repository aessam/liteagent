"""
Tool calling format detection module.

This module provides functionality to detect the tool calling format used by a model
by analyzing its response. This is useful for models with unknown capabilities or
for implementing automatic detection.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .tool_calling_types import ToolCallingType
from .utils import logger


def detect_tool_calling_format(response: Any) -> ToolCallingType:
    """
    Detect the tool calling format used in a model's response.
    
    Args:
        response: The model's response object or string
        
    Returns:
        ToolCallingType: The detected tool calling type
    """
    # Convert response to string if it's not already
    response_text = _extract_content(response)
    
    # Try different detection strategies in priority order
    
    # 1. Check for OpenAI-style function calling format
    if _detect_openai_format(response):
        return ToolCallingType.OPENAI_FUNCTION_CALLING
    
    # 2. Check for Anthropic-style tool calling format
    if _detect_anthropic_format(response):
        return ToolCallingType.ANTHROPIC_TOOL_CALLING
    
    # 3. Check for JSON extraction format
    if _detect_json_extraction_format(response_text):
        return ToolCallingType.JSON_EXTRACTION
    
    # 4. Default to prompt-based for unrecognized formats
    return ToolCallingType.PROMPT_BASED


def _extract_content(response: Any) -> str:
    """
    Extract text content from various response formats.
    
    Args:
        response: Response object or string
        
    Returns:
        str: Extracted text content
    """
    if isinstance(response, str):
        return response
    
    # Handle OpenAI-style response
    if isinstance(response, dict):
        if "choices" in response:
            choices = response.get("choices", [])
            if choices and isinstance(choices[0], dict):
                message = choices[0].get("message", {})
                if isinstance(message, dict) and "content" in message:
                    return message.get("content") or ""
        
        # Handle Anthropic-style response
        if "content" in response:
            content = response.get("content", [])
            if isinstance(content, list):
                text_parts = [item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"]
                return " ".join(text_parts)
        
        # Generic content extraction
        if "text" in response:
            return response.get("text", "")
    
    # For any other format, convert to string
    try:
        return str(response)
    except Exception:
        return ""


def _detect_openai_format(response: Any) -> bool:
    """
    Detect if the response uses OpenAI-style function calling format.
    
    Args:
        response: The model's response
        
    Returns:
        bool: True if OpenAI format is detected
    """
    if not isinstance(response, dict):
        return False
    
    # Check for OpenAI API response structure
    if "choices" in response:
        choices = response.get("choices", [])
        if choices and isinstance(choices[0], dict):
            message = choices[0].get("message", {})
            
            # Look for tool_calls in the message
            if isinstance(message, dict) and "tool_calls" in message:
                return True
            
            # Look for function_call in the message (older format)
            if isinstance(message, dict) and "function_call" in message:
                return True
    
    return False


def _detect_anthropic_format(response: Any) -> bool:
    """
    Detect if the response uses Anthropic-style tool calling format.
    
    Args:
        response: The model's response
        
    Returns:
        bool: True if Anthropic format is detected
    """
    if not isinstance(response, dict):
        return False
    
    # Check for Anthropic API response structure
    if "content" in response:
        content = response.get("content", [])
        
        # Look for tool_use blocks in content
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    return True
    
    return False


def _detect_json_extraction_format(response_text: str) -> bool:
    """
    Detect if the response contains JSON that can be extracted.
    
    Args:
        response_text: The model's response as text
        
    Returns:
        bool: True if JSON format is detected
    """
    # Look for JSON-like patterns in the text
    json_pattern = r'```(?:json)?\s*({[\s\S]*?})```'
    matches = re.findall(json_pattern, response_text)
    
    if matches:
        for match in matches:
            try:
                parsed = json.loads(match)
                # If it has function/name/args structure, it's likely a tool call
                if isinstance(parsed, dict) and ('function' in parsed or 'name' in parsed or 'args' in parsed):
                    return True
            except json.JSONDecodeError:
                continue
    
    # Look for direct JSON objects without code blocks
    direct_json_pattern = r'{[\s\S]*?"(?:function|name)"[\s\S]*?}'
    matches = re.findall(direct_json_pattern, response_text)
    
    if matches:
        for match in matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, dict) and ('function' in parsed or 'name' in parsed or 'args' in parsed):
                    return True
            except json.JSONDecodeError:
                continue
    
    return False


def extract_tool_calls_from_response(response: Any) -> List[Dict]:
    """
    Extract tool calls from a model response regardless of format.
    
    Args:
        response: The model's response
        
    Returns:
        List[Dict]: Extracted tool calls with unified format
    """
    # Detect the format
    tool_calling_type = detect_tool_calling_format(response)
    
    # Extract using the appropriate method based on detected format
    if tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
        return _extract_openai_tool_calls(response)
    elif tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
        return _extract_anthropic_tool_calls(response)
    elif tool_calling_type == ToolCallingType.JSON_EXTRACTION:
        return _extract_json_tool_calls(_extract_content(response))
    
    # For PROMPT_BASED or NONE, return empty list
    return []


def _extract_openai_tool_calls(response: Any) -> List[Dict]:
    """
    Extract tool calls from OpenAI-style response.
    
    Args:
        response: OpenAI API response
        
    Returns:
        List[Dict]: Extracted tool calls
    """
    result = []
    
    if not isinstance(response, dict):
        return result
    
    try:
        choices = response.get("choices", [])
        if not choices:
            return result
        
        message = choices[0].get("message", {})
        
        # Check for new tool_calls format
        if "tool_calls" in message:
            tool_calls = message.get("tool_calls", [])
            for tool_call in tool_calls:
                if not isinstance(tool_call, dict):
                    continue
                
                tool_id = tool_call.get("id")
                function = tool_call.get("function", {})
                
                if not function:
                    continue
                
                name = function.get("name")
                arguments = function.get("arguments", "{}")
                
                try:
                    args_dict = json.loads(arguments) if isinstance(arguments, str) else arguments
                except json.JSONDecodeError:
                    args_dict = {}
                
                result.append({
                    "name": name,
                    "arguments": args_dict,
                    "id": tool_id
                })
        
        # Check for old function_call format
        elif "function_call" in message:
            function_call = message.get("function_call", {})
            if function_call:
                name = function_call.get("name")
                arguments = function_call.get("arguments", "{}")
                
                try:
                    args_dict = json.loads(arguments) if isinstance(arguments, str) else arguments
                except json.JSONDecodeError:
                    args_dict = {}
                
                result.append({
                    "name": name,
                    "arguments": args_dict,
                    "id": f"call_{name}"
                })
    
    except Exception as e:
        logger.error(f"Error extracting OpenAI tool calls: {e}")
    
    return result


def _extract_anthropic_tool_calls(response: Any) -> List[Dict]:
    """
    Extract tool calls from Anthropic-style response.
    
    Args:
        response: Anthropic API response
        
    Returns:
        List[Dict]: Extracted tool calls
    """
    result = []
    
    if not isinstance(response, dict):
        return result
    
    try:
        content = response.get("content", [])
        
        for item in content:
            if not isinstance(item, dict):
                continue
            
            if item.get("type") == "tool_use":
                tool_use = item.get("tool_use", {})
                if not tool_use:
                    continue
                
                name = tool_use.get("name")
                tool_id = tool_use.get("id", f"call_{name}")
                input_data = tool_use.get("input", {})
                
                if not name:
                    continue
                
                result.append({
                    "name": name,
                    "arguments": input_data,
                    "id": tool_id
                })
    
    except Exception as e:
        logger.error(f"Error extracting Anthropic tool calls: {e}")
    
    return result


def _extract_json_tool_calls(text: str) -> List[Dict]:
    """
    Extract tool calls from text with JSON formats.
    
    Args:
        text: Response text containing JSON
        
    Returns:
        List[Dict]: Extracted tool calls
    """
    result = []
    
    try:
        # Try to find JSON blocks in code fences
        json_pattern = r'```(?:json)?\s*({[\s\S]*?})```'
        matches = re.findall(json_pattern, text)
        
        for match in matches:
            try:
                parsed = json.loads(match)
                
                # Handle various JSON formats
                if isinstance(parsed, dict):
                    if "function" in parsed and "arguments" in parsed:
                        result.append({
                            "name": parsed["function"],
                            "arguments": parsed["arguments"],
                            "id": f"json_{len(result)}"
                        })
                    elif "name" in parsed and "args" in parsed:
                        result.append({
                            "name": parsed["name"],
                            "arguments": parsed["args"],
                            "id": f"json_{len(result)}"
                        })
                    elif "name" in parsed and "arguments" in parsed:
                        result.append({
                            "name": parsed["name"],
                            "arguments": parsed["arguments"],
                            "id": f"json_{len(result)}"
                        })
            except json.JSONDecodeError:
                continue
        
        # If no valid JSON blocks were found, try direct JSON objects
        if not result:
            direct_json_pattern = r'{[\s\S]*?"(?:function|name)"[\s\S]*?}'
            matches = re.findall(direct_json_pattern, text)
            
            for match in matches:
                try:
                    parsed = json.loads(match)
                    
                    # Handle various JSON formats (same logic as above)
                    if isinstance(parsed, dict):
                        if "function" in parsed and "arguments" in parsed:
                            result.append({
                                "name": parsed["function"],
                                "arguments": parsed["arguments"],
                                "id": f"json_{len(result)}"
                            })
                        elif "name" in parsed and "args" in parsed:
                            result.append({
                                "name": parsed["name"],
                                "arguments": parsed["args"],
                                "id": f"json_{len(result)}"
                            })
                        elif "name" in parsed and "arguments" in parsed:
                            result.append({
                                "name": parsed["name"],
                                "arguments": parsed["arguments"],
                                "id": f"json_{len(result)}"
                            })
                except json.JSONDecodeError:
                    continue
    
    except Exception as e:
        logger.error(f"Error extracting JSON tool calls: {e}")
    
    return result 