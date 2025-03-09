"""
Dynamic model capabilities detection for LiteAgent.

This module automatically detects model capabilities from responses,
eliminating the need for static configuration files.
"""

import re
from typing import Dict, Any, Optional
from .tool_calling_types import ToolCallingType, string_to_tool_calling_type, enum_to_string
from .tool_calling_detection import detect_tool_calling_format

# In-memory cache for detected capabilities
_MODEL_CAPABILITIES_CACHE = {}

# Define patterns for model types using regex
_MODEL_PATTERNS = [
    (re.compile(r'(?i)^(openai/|gpt-)'), ToolCallingType.OPENAI),
    (re.compile(r'(?i)(claude|anthropic)'), ToolCallingType.ANTHROPIC),
    (re.compile(r'(?i)^ollama/'), ToolCallingType.OLLAMA),
    (re.compile(r'(?i)(groq|llama-3)'), ToolCallingType.OPENAI),
]

def get_model_capabilities(model_name: str) -> Dict[str, Any]:
    """
    Get the capabilities of a model, either from cache or by detection.
    
    Args:
        model_name: The name of the model
        
    Returns:
        A dictionary of model capabilities
    """
    # Check cache first
    cached = _MODEL_CAPABILITIES_CACHE.get(model_name.lower())
    if cached:
        return cached
        
    # Default capabilities with detected tool calling type
    capabilities = {
        "tool_calling_type": get_tool_calling_type(model_name),
        "supports_image_input": False,
        "supports_multiple_tools": True,
        "max_tools": 128,
    }
    
    # Cache the capabilities
    _MODEL_CAPABILITIES_CACHE[model_name.lower()] = capabilities
    return capabilities

def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Determine the tool calling type for a model based on pattern matching.
    
    Args:
        model_name: The name of the model
        
    Returns:
        The appropriate tool calling type
    """
    if not model_name:
        return ToolCallingType.STRUCTURED_OUTPUT
    
    # Check against known patterns
    for pattern, tool_type in _MODEL_PATTERNS:
        if pattern.search(model_name):
            return tool_type
    
    # For unknown models, default to structured output
    return ToolCallingType.STRUCTURED_OUTPUT

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

def update_model_capabilities(model_name: str, response: Any) -> None:
    """
    Update the cached capabilities for a model based on an actual response.
    
    Args:
        model_name: The name of the model
        response: A response from the model to analyze
    """
    detected_type = detect_tool_calling_format(response)
    
    # Update cache with detected capabilities
    capabilities = get_model_capabilities(model_name)
    capabilities["tool_calling_type"] = detected_type
    _MODEL_CAPABILITIES_CACHE[model_name.lower()] = capabilities 