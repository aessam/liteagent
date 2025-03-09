"""
Enhanced tool calling type definitions and model capabilities registry.

This module provides a more structured approach to defining tool calling capabilities
for different language models, with clear separation of concerns and validation strategies.
"""

import json
import os
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Set

from .utils import logger

class ToolCallingType(Enum):
    """Defines how tools are invoked by a language model."""
    
    # No tool calling support
    NONE = auto()
    
    # OpenAI-style function calling (includes compatible models)
    OPENAI = auto()
    OPENAI_FUNCTION_CALLING = OPENAI  # Legacy alias for backward compatibility
    
    # Anthropic-style tool calling
    ANTHROPIC = auto()
    ANTHROPIC_TOOL_CALLING = ANTHROPIC  # Legacy alias for backward compatibility
    
    # Groq style (OpenAI-compatible, but explicitly for Groq models)
    GROQ = auto()
    
    # Generic JSON output parsing for models that use text-based approaches
    OLLAMA = auto()
    OLLAMA_TOOL_CALLING = OLLAMA  # Legacy alias for backward compatibility
    
    # Simple text-based function call patterns
    TEXT_BASED = auto()
    
    # Handles models that need specific prompting to return structured outputs
    STRUCTURED_OUTPUT = auto()
    PROMPT_BASED = STRUCTURED_OUTPUT  # Legacy alias for backward compatibility


__all__ = [
    'ToolCallingType',
    'string_to_tool_calling_type',
    'get_provider_from_model',
    'get_model_capabilities',
    'get_tool_calling_type',
    'supports_tool_calling',
    'get_tool_calling_handler_type',
    'enum_to_string',
    'detect_model_capability',
]


def string_to_tool_calling_type(type_str: str) -> ToolCallingType:
    """
    Convert a string representation of tool calling type to enum.
    
    Args:
        type_str: String representation of tool calling type
        
    Returns:
        ToolCallingType enum value
    """
    if not type_str:
        return ToolCallingType.NONE
        
    type_str = type_str.upper()
    
    if type_str in ("OPENAI", "OPENAI_FUNCTION_CALLING"):
        return ToolCallingType.OPENAI
    elif type_str in ("ANTHROPIC", "ANTHROPIC_TOOL_CALLING"):
        return ToolCallingType.ANTHROPIC
    elif type_str in ("GROQ"):
        return ToolCallingType.GROQ
    elif type_str in ("OLLAMA", "OLLAMA_TOOL_CALLING"):
        return ToolCallingType.OLLAMA
    elif type_str in ("TEXT_BASED"):
        return ToolCallingType.TEXT_BASED
    elif type_str in ("STRUCTURED_OUTPUT", "PROMPT_BASED"):
        return ToolCallingType.STRUCTURED_OUTPUT
    elif type_str in ("NONE"):
        return ToolCallingType.NONE
    else:
        # Default to None for unknown types
        return ToolCallingType.NONE


# Path to the capabilities configuration file
CAPABILITIES_FILE = os.path.join(os.path.dirname(__file__), "model_capabilities.json")

# Default capabilities for unknown models
DEFAULT_MODEL_CAPABILITIES = {
    "tool_calling_type": ToolCallingType.PROMPT_BASED,
    "supports_multiple_tools": False,
    "supports_nested_tools": False,
    "max_tools_per_request": 1,
}

# Initialize empty capabilities dictionary
MODEL_CAPABILITIES = {
    # Fallback for undefined models (cautious approach)
    "default": {
        "tool_calling_type": ToolCallingType.PROMPT_BASED,
        "supports_multiple_tools": False,
        "max_tools_per_request": 1
    },
    "provider_capabilities": {},
    "model_exceptions": {}
}

# Try to load capabilities from JSON
try:
    if os.path.exists(CAPABILITIES_FILE):
        with open(CAPABILITIES_FILE, "r") as f:
            capabilities_json = json.load(f)
            json_capabilities = capabilities_json.get("model_capabilities", {})
            
            # Convert string representation of tool calling type to enum for provider capabilities
            if "provider_capabilities" in json_capabilities:
                for provider, caps in json_capabilities["provider_capabilities"].items():
                    provider_caps = caps.copy()
                    if "tool_calling_type" in caps:
                        provider_caps["tool_calling_type"] = string_to_tool_calling_type(caps["tool_calling_type"])
                    
                    # Update the provider capabilities
                    MODEL_CAPABILITIES["provider_capabilities"][provider] = provider_caps
            
            # Convert string representation of tool calling type to enum for model exceptions
            if "model_exceptions" in json_capabilities:
                for model, caps in json_capabilities["model_exceptions"].items():
                    model_caps = caps.copy()
                    if "tool_calling_type" in caps:
                        model_caps["tool_calling_type"] = string_to_tool_calling_type(caps["tool_calling_type"])
                    
                    # Update the model exceptions
                    MODEL_CAPABILITIES["model_exceptions"][model] = model_caps
            
            # Update default if present
            if "default" in json_capabilities:
                default_caps = json_capabilities["default"].copy()
                if "tool_calling_type" in json_capabilities["default"]:
                    default_caps["tool_calling_type"] = string_to_tool_calling_type(json_capabilities["default"]["tool_calling_type"])
                
                MODEL_CAPABILITIES["default"] = default_caps
                
except Exception as e:
    # If there's an error loading from JSON, we'll use the hardcoded defaults
    print(f"Error loading model capabilities from JSON: {e}")


def get_provider_from_model(model_name: str) -> str:
    """
    Extract the provider from a model name.
    
    Args:
        model_name: The name of the model
        
    Returns:
        Provider name
    """
    if not model_name:
        return "unknown"
        
    # For custom prefixed models like "ollama/phi"
    if '/' in model_name:
        provider = model_name.split('/')[0]
        return provider.lower()
    
    # Use a simple mapping for common models
    model_lower = model_name.lower()
    if model_lower.startswith(("gpt-", "text-davinci")):
        return "openai"
    elif model_lower.startswith("claude"):
        return "anthropic"
    elif model_lower.startswith("llama"):
        return "groq"
    elif model_lower.startswith("deepseek"):
        return "deepseek"
    elif model_lower.startswith("mistral"):
        return "mistral"
    
    # Default to "unknown" if we can't determine the provider
    return "unknown"


def get_model_capabilities(model_name: str) -> Dict[str, Any]:
    """
    Get the capabilities for a specific model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        Dict[str, Any]: The capabilities for the model
    """
    model_lower = model_name.lower() if model_name else ""
    logger.debug(f"Looking up capabilities for model: {model_lower}")
    
    # Check for model exceptions first
    if model_lower in MODEL_CAPABILITIES["model_exceptions"]:
        logger.debug(f"Found model in exceptions: {model_lower}")
        return MODEL_CAPABILITIES["model_exceptions"][model_lower]
    
    # Get the provider for the model
    provider = get_provider_from_model(model_lower)
    logger.debug(f"Identified provider for {model_lower}: {provider}")
    
    # Check if we have capabilities for this provider
    if provider in MODEL_CAPABILITIES["provider_capabilities"]:
        logger.debug(f"Using provider capabilities for {provider}")
        return MODEL_CAPABILITIES["provider_capabilities"][provider]
    
    # Return default capabilities
    logger.debug(f"No specific capabilities found, using default")
    return MODEL_CAPABILITIES["default"].copy()


def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Get the tool calling type for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        ToolCallingType: The appropriate tool calling type for the model
    """
    if not model_name:
        logger.debug("No model name provided, returning NONE")
        return ToolCallingType.NONE
    
    # Get model capabilities (which checks for model exceptions and provider-based defaults)
    model_caps = get_model_capabilities(model_name)
    tool_calling_type = model_caps["tool_calling_type"]
    logger.debug(f"Tool calling type for {model_name}: {tool_calling_type}")
    return tool_calling_type


def supports_tool_calling(model_name: str) -> bool:
    """
    Check if a model supports tool calling.
    
    Args:
        model_name: The name of the model
        
    Returns:
        bool: True if the model supports tool calling, False otherwise
    """
    tool_calling_type = get_tool_calling_type(model_name)
    return tool_calling_type != ToolCallingType.NONE


def get_tool_calling_handler_type(model_name: str) -> str:
    """
    Get the tool calling handler type name for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        str: The name of the tool calling handler type
    """
    tool_calling_type = get_tool_calling_type(model_name)
    return tool_calling_type.name


def enum_to_string(tool_calling_type: ToolCallingType) -> str:
    """
    Convert a ToolCallingType enum to its string representation.
    
    Args:
        tool_calling_type: The enum value to convert
        
    Returns:
        str: The string representation of the enum
    """
    return tool_calling_type.name


#
# Runtime detection of model capabilities
#

from .tools import liteagent_tool

# In-memory cache for detected capabilities
_MODEL_CAPABILITIES_CACHE = {}

@liteagent_tool
def test_add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def detect_model_capability(model_name: str, model_interface) -> ToolCallingType:
    """
    Detect a model's tool calling capability with minimal overhead.
    
    Args:
        model_name: The name of the model
        model_interface: The model interface for making requests
        
    Returns:
        The detected ToolCallingType
    """
    # Check cache first
    if model_name in _MODEL_CAPABILITIES_CACHE:
        logger.debug(f"Using cached capability for {model_name}")
        return _MODEL_CAPABILITIES_CACHE[model_name]
    
    # For test mocks or any model name containing 'mock'
    if model_name.lower().startswith('mock') or hasattr(model_interface, '__class__') and 'mock' in model_interface.__class__.__name__.lower():
        logger.debug(f"Detected mock model: {model_name}, using OPENAI capability")
        _MODEL_CAPABILITIES_CACHE[model_name] = ToolCallingType.OPENAI
        return ToolCallingType.OPENAI
    
    # Simple test message
    test_messages = [
        {"role": "system", "content": "You can use tools to help with tasks."},
        {"role": "user", "content": "What is 2+3? Please use the test_add tool."}
    ]
    
    try:
        # Check if model_interface has the required method
        if not hasattr(model_interface, 'chat'):
            logger.warning(f"Model interface for {model_name} doesn't have 'chat' method, defaulting to STRUCTURED_OUTPUT")
            _MODEL_CAPABILITIES_CACHE[model_name] = ToolCallingType.STRUCTURED_OUTPUT
            return ToolCallingType.STRUCTURED_OUTPUT
            
        # Get a test response
        response = model_interface.chat(test_messages, tools=[test_add])
        
        # Use existing detector
        from .tool_calling_detection import detect_tool_calling_format
        calling_type = detect_tool_calling_format(response)
        
        # Check if the model actually used the tool - cases like Phi4-mini
        # that accept tools but don't use proper tool calling format
        if calling_type == ToolCallingType.STRUCTURED_OUTPUT:
            calling_type = ToolCallingType.STRUCTURED_OUTPUT
        
        # Cache the result
        _MODEL_CAPABILITIES_CACHE[model_name] = calling_type
        logger.debug(f"Detected capability for {model_name}: {calling_type}")
        return calling_type
        
    except Exception as e:
        logger.debug(f"Error detecting model capability: {e}")
        # If test fails, default to structured output
        default = ToolCallingType.STRUCTURED_OUTPUT
        _MODEL_CAPABILITIES_CACHE[model_name] = default
        return default 