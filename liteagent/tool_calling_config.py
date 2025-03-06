"""
Configuration loader for tool calling support.

This module provides functions to load and access the model configuration
for tool calling support.
"""

import json
import os
from typing import Dict, Optional, Any, List, Set

from .tool_calling import ToolCallingType
from .utils import logger
from .tool_calling_types import ToolCallingType as ToolCallingType_from_types
from .tool_calling_types import get_provider_from_model as get_provider_from_types
from litellm import get_llm_provider

# Path to the configuration file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "model_config.json")

# Global configuration cache
_config_cache = None


def load_config() -> Dict:
    """
    Load the model configuration from the JSON file.
    
    Returns:
        Dict: The configuration dictionary
    """
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
        
    try:
        with open(CONFIG_FILE, "r") as f:
            _config_cache = json.load(f)
        return _config_cache
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading model configuration: {e}")
        # Return a minimal default configuration
        return {
            "providers": {
                "openai": {
                    "tool_calling_type": "OPENAI",
                    "models": {"default": "OPENAI"}
                },
                "anthropic": {
                    "tool_calling_type": "ANTHROPIC",
                    "models": {"default": "ANTHROPIC"}
                },
                "default": {
                    "tool_calling_type": "TEXT_BASED",
                    "models": {"default": "TEXT_BASED"}
                }
            }
        }

def get_model_info(model_name: str) -> Dict[str, Any]:
    """
    Get information about a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        Dict with model information
    """
    provider = get_provider_from_model(model_name)
    return {
        "provider": provider,
        "supports_function_calling": provider in ["openai", "groq", "anthropic", "mistral", "deepseek"],
        "tool_calling_type": get_tool_calling_type(model_name),
    }

def get_provider_from_model(model_name: str) -> str:
    """
    Extract the provider from a model name.
    
    Args:
        model_name: The name of the model
        
    Returns:
        Provider name
    """
    # Use the provider detection from tool_calling_types to ensure consistency
    return get_provider_from_types(model_name)


def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Determine the tool calling type for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        ToolCallingType enum value
    """
    from .tool_calling_types import get_tool_calling_type
    from liteagent.utils import logger
    
    tool_calling_type = get_tool_calling_type(model_name)
    logger.debug(f"Selected tool calling type for {model_name}: {tool_calling_type}")
    
    return tool_calling_type


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