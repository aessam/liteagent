"""
Model capabilities registry and detection module.

This module provides functions for detecting and registering model capabilities,
including tool calling support and other features.
"""

import json
import os
import re
from enum import Enum
from typing import Dict, Optional, Any, List, Union, Set

from .tool_calling_types import ToolCallingType

# Load model capabilities from JSON file
_CAPABILITIES_FILE = os.path.join(os.path.dirname(__file__), "model_capabilities.json")
_MODEL_CAPABILITIES = {}

try:
    with open(_CAPABILITIES_FILE, "r") as f:
        _MODEL_CAPABILITIES = json.load(f)
except Exception as e:
    # Fail gracefully and use empty dict if file can't be loaded
    print(f"Error loading model capabilities: {e}")


def enum_to_string(enum_val: Enum) -> str:
    """
    Convert an enum value to its string representation.
    
    Args:
        enum_val: The enum value to convert
        
    Returns:
        The string representation of the enum value
    """
    if enum_val == ToolCallingType.OPENAI:
        return "OPENAI"
    elif enum_val == ToolCallingType.ANTHROPIC:
        return "ANTHROPIC"
    elif enum_val == ToolCallingType.OLLAMA:
        return "OLLAMA"
    elif enum_val == ToolCallingType.STRUCTURED_OUTPUT:
        return "STRUCTURED_OUTPUT"
    elif enum_val == ToolCallingType.TEXT_BASED:
        return "TEXT_BASED"
    elif enum_val == ToolCallingType.GROQ:
        return "GROQ"
    elif enum_val == ToolCallingType.NONE:
        return "NONE"
    else:
        return str(enum_val)


def _matches_pattern(model_name: str, pattern: str) -> bool:
    """
    Check if a model name matches a pattern using regular expressions.
    
    Args:
        model_name: The model name to check
        pattern: The pattern to match against
        
    Returns:
        True if the model name matches the pattern
    """
    try:
        return bool(re.match(pattern, model_name))
    except:
        # If the pattern is invalid, return False
        return False
        

def get_model_capabilities(model_name: str) -> Dict[str, Any]:
    """
    Get the capabilities of a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        A dictionary of model capabilities
    """
    # Normalize model name
    model_name = model_name.lower()
    
    # Check for model matches by exact name
    for config_name, config in _MODEL_CAPABILITIES.items():
        if "exact_match" in config and config_name.lower() == model_name:
            return config
            
    # Check for pattern matches
    for config_name, config in _MODEL_CAPABILITIES.items():
        if "pattern" in config and _matches_pattern(model_name, config["pattern"]):
            return config
    
    # Default capabilities
    default_capabilities = {
        "tool_calling_type": ToolCallingType.NONE,
        "supports_image_input": False,
        "supports_multiple_tools": False,
        "max_tools": 0,
        "tools_schema": "openai"
    }
    
    # Return default capabilities for unknown models
    return default_capabilities


def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Determine the tool calling type for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        The appropriate tool calling type
    """
    model_name = model_name.lower()
    
    # Special case models
    if "gpt-4" in model_name or "gpt-3.5" in model_name:
        return ToolCallingType.OPENAI
        
    if "claude" in model_name:
        return ToolCallingType.ANTHROPIC
        
    if model_name.startswith("ollama/") or "/phi" in model_name:
        return ToolCallingType.OLLAMA
        
    if "groq" in model_name or "llama-3" in model_name:
        return ToolCallingType.OPENAI  # Groq uses OpenAI-compatible format
        
    # Lookup from capabilities registry
    capabilities = get_model_capabilities(model_name)
    tool_calling_type = capabilities.get("tool_calling_type", ToolCallingType.NONE)
    
    # Handle string or enum values
    if isinstance(tool_calling_type, str):
        from .tool_calling_types import string_to_tool_calling_type
        return string_to_tool_calling_type(tool_calling_type)
    
    return tool_calling_type


def supports_tool_calling(model_name: str) -> bool:
    """
    Check if a model supports tool calling.
    
    Args:
        model_name: The name of the model
        
    Returns:
        True if the model supports tool calling
    """
    tool_calling_type = get_tool_calling_type(model_name)
    return tool_calling_type != ToolCallingType.NONE


def get_tool_calling_handler_type(model_name: str) -> str:
    """
    Get the tool calling handler type name for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        The string representation of the tool calling type
    """
    tool_calling_type = get_tool_calling_type(model_name)
    return enum_to_string(tool_calling_type) 