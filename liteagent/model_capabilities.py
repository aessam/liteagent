"""
Model capabilities management.

This module provides utilities for managing model capabilities stored in JSON format,
including loading, saving, and retrieving capability information.
"""

import json
import os
from typing import Dict, Any, Optional, List

from .tool_calling_types import ToolCallingType, get_model_capabilities as get_model_caps_from_module
from .utils import logger

# Path to the capabilities configuration file
CAPABILITIES_FILE = os.path.join(os.path.dirname(__file__), "model_capabilities.json")

# Global capabilities cache
_capabilities_cache = None

def get_tool_calling_type_from_str(type_str: str) -> ToolCallingType:
    """
    Convert a string representation of tool calling type to enum.
    
    Args:
        type_str: String representation of tool calling type
        
    Returns:
        ToolCallingType enum value
    """
    type_str = type_str.upper()
    
    if type_str == "OPENAI" or type_str == "OPENAI_FUNCTION_CALLING":
        return ToolCallingType.OPENAI_FUNCTION_CALLING
    elif type_str == "ANTHROPIC" or type_str == "ANTHROPIC_TOOL_CALLING":
        return ToolCallingType.ANTHROPIC_TOOL_CALLING
    elif type_str == "JSON_EXTRACTION" or type_str == "OLLAMA":
        return ToolCallingType.JSON_EXTRACTION
    elif type_str == "TEXT_BASED" or type_str == "PROMPT_BASED":
        return ToolCallingType.PROMPT_BASED
    elif type_str == "NONE":
        return ToolCallingType.NONE
    else:
        logger.warning(f"Unknown tool calling type: {type_str}, using PROMPT_BASED")
        return ToolCallingType.PROMPT_BASED

def get_str_from_tool_calling_type(enum_val: ToolCallingType) -> str:
    """
    Convert a ToolCallingType enum to a string representation for JSON.
    
    Args:
        enum_val: The ToolCallingType enum value
        
    Returns:
        str: String representation of the enum
    """
    if enum_val == ToolCallingType.OPENAI_FUNCTION_CALLING:
        return "OPENAI_FUNCTION_CALLING"
    elif enum_val == ToolCallingType.ANTHROPIC_TOOL_CALLING:
        return "ANTHROPIC_TOOL_CALLING"
    elif enum_val == ToolCallingType.JSON_EXTRACTION:
        return "JSON_EXTRACTION"
    elif enum_val == ToolCallingType.PROMPT_BASED:
        return "PROMPT_BASED"
    elif enum_val == ToolCallingType.NONE:
        return "NONE"
    else:
        return "UNKNOWN"

def save_capabilities_to_json(capabilities_dict: Dict[str, Dict[str, Any]] = None) -> bool:
    """
    Save the given capabilities dictionary (or the current loaded one) to the JSON file.
    
    Args:
        capabilities_dict: Dictionary of model capabilities to save, or None to use current ones
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # If no dict provided, get the current capabilities from the module
        if capabilities_dict is None:
            from .tool_calling_types import MODEL_CAPABILITIES
            capabilities_dict = MODEL_CAPABILITIES
        
        # Convert ToolCallingType enum to string representation for JSON serialization
        serializable_capabilities = {}
        for model, caps in capabilities_dict.items():
            serializable_capabilities[model] = caps.copy()
            if "tool_calling_type" in caps:
                serializable_capabilities[model]["tool_calling_type"] = get_str_from_tool_calling_type(caps["tool_calling_type"])
        
        with open(CAPABILITIES_FILE, "w") as f:
            json.dump({"model_capabilities": serializable_capabilities}, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving model capabilities to JSON: {e}")
        return False

def get_model_capability(model_name: str, capability: str, default=None) -> Any:
    """
    Get a specific capability for a model.
    
    Args:
        model_name: The name of the model
        capability: The capability to get
        default: Default value if capability not found
        
    Returns:
        Any: The capability value or default
    """
    # Get capabilities from tool_calling_types module
    model_caps = get_model_caps_from_module(model_name)
    return model_caps.get(capability, default)

def is_capability_enabled(model_name: str, capability: str) -> bool:
    """
    Check if a capability is enabled for a model.
    
    Args:
        model_name: The name of the model
        capability: The capability to check
        
    Returns:
        bool: True if capability is enabled, False otherwise
    """
    return bool(get_model_capability(model_name, capability, False))

def add_or_update_model_capability(model_name: str, capabilities: Dict[str, Any]) -> bool:
    """
    Add or update capabilities for a model in the JSON file.
    
    Args:
        model_name: The name of the model
        capabilities: Dictionary of capabilities to add/update
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load current capabilities
        with open(CAPABILITIES_FILE, "r") as f:
            current_capabilities = json.load(f)
        
        # Add or update model capabilities
        current_capabilities.setdefault("model_capabilities", {})[model_name] = capabilities
        
        # Save back to file
        with open(CAPABILITIES_FILE, "w") as f:
            json.dump(current_capabilities, f, indent=2)
            
        # Reload capabilities in the module
        from .tool_calling_types import MODEL_CAPABILITIES
        
        # Convert string tool calling type to enum if needed
        if "tool_calling_type" in capabilities and isinstance(capabilities["tool_calling_type"], str):
            capabilities = capabilities.copy()
            capabilities["tool_calling_type"] = get_tool_calling_type_from_str(capabilities["tool_calling_type"])
            
        MODEL_CAPABILITIES[model_name] = capabilities
        
        return True
    except Exception as e:
        logger.error(f"Error updating model capability: {e}")
        return False 