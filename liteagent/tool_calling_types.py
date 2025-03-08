"""
Enhanced tool calling type definitions and model capabilities registry.

This module provides a more structured approach to defining tool calling capabilities
for different language models, with clear separation of concerns and validation strategies.
"""

import json
import os
from enum import Enum, auto
from typing import Dict, Any, Optional, List, Set

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
    from liteagent.utils import logger
    
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
    from liteagent.utils import logger
    
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