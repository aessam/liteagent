"""
Configuration loader for tool calling support.

This module provides functions to load and access the model configuration
for tool calling support.
"""

import json
import os
from typing import Dict, Optional

from .tool_calling import ToolCallingType
from .utils import logger

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


def get_provider_from_model(model_name: str) -> str:
    """
    Extract the provider from a model name.
    
    Args:
        model_name: The name of the model
        
    Returns:
        str: The provider name
    """
    model_lower = model_name.lower()
    
    # Check for provider prefixes
    if model_lower.startswith(("gpt-", "text-davinci")):
        return "openai"
    elif model_lower.startswith("claude"):
        return "anthropic"
    elif model_lower.startswith("mistral"):
        return "mistral"
    elif model_lower.startswith(("llama", "qwen", "gemma", "phi")):
        # Could be groq or ollama, need to check if it has a provider prefix
        if "/" in model_lower:
            provider, _ = model_lower.split("/", 1)
            return provider
        # Default to ollama for local models
        return "ollama"
    elif model_lower.startswith("command"):
        return "cohere"
    elif "/" in model_lower:
        # Extract provider from provider/model format
        provider, _ = model_lower.split("/", 1)
        return provider
        
    # Default to "local" if we can't determine the provider
    return "local"


def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Get the tool calling type for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        ToolCallingType: The tool calling type for the model
    """
    config = load_config()
    provider = get_provider_from_model(model_name)
    
    # Get provider config
    provider_config = config["providers"].get(provider)
    if not provider_config:
        logger.warning(f"No configuration found for provider '{provider}', using default")
        provider_config = config["providers"].get("default", {"tool_calling_type": "TEXT_BASED", "models": {}})
    
    # Get model-specific tool calling type
    model_lower = model_name.lower()
    model_type = None
    
    # Check for exact model match
    if "models" in provider_config and model_lower in provider_config["models"]:
        model_type = provider_config["models"][model_lower]
    # Fall back to provider default
    elif "models" in provider_config and "default" in provider_config["models"]:
        model_type = provider_config["models"]["default"]
    # Fall back to provider type
    elif "tool_calling_type" in provider_config:
        model_type = provider_config["tool_calling_type"]
    # Last resort default
    else:
        model_type = "TEXT_BASED"
    
    # Convert string to enum
    try:
        return ToolCallingType[model_type]
    except (KeyError, TypeError):
        logger.warning(f"Invalid tool calling type '{model_type}', using TEXT_BASED")
        return ToolCallingType.TEXT_BASED


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