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
    
    # OpenAI-style function calling (includes Groq and compatible models)
    OPENAI_FUNCTION_CALLING = auto()
    
    # Anthropic-style tool calling
    ANTHROPIC_TOOL_CALLING = auto()
    
    # Generic JSON output parsing (for models like Ollama that use text-based approaches)
    JSON_EXTRACTION = auto()
    
    # Handles models that need specific prompting to return structured outputs
    PROMPT_BASED = auto()


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
    }
}

# Try to load capabilities from JSON
try:
    if os.path.exists(CAPABILITIES_FILE):
        with open(CAPABILITIES_FILE, "r") as f:
            capabilities_json = json.load(f)
            json_capabilities = capabilities_json.get("model_capabilities", {})
            
            # Convert string representation of tool calling type to enum
            for model, caps in json_capabilities.items():
                model_caps = caps.copy()
                if "tool_calling_type" in caps:
                    type_str = caps["tool_calling_type"].upper()
                    if type_str == "OPENAI" or type_str == "OPENAI_FUNCTION_CALLING":
                        model_caps["tool_calling_type"] = ToolCallingType.OPENAI_FUNCTION_CALLING
                    elif type_str == "ANTHROPIC" or type_str == "ANTHROPIC_TOOL_CALLING":
                        model_caps["tool_calling_type"] = ToolCallingType.ANTHROPIC_TOOL_CALLING
                    elif type_str == "JSON_EXTRACTION" or type_str == "OLLAMA":
                        model_caps["tool_calling_type"] = ToolCallingType.JSON_EXTRACTION
                    elif type_str == "TEXT_BASED" or type_str == "PROMPT_BASED":
                        model_caps["tool_calling_type"] = ToolCallingType.PROMPT_BASED
                    elif type_str == "NONE":
                        model_caps["tool_calling_type"] = ToolCallingType.NONE
                    
                # Update the model capabilities
                MODEL_CAPABILITIES[model] = model_caps
except Exception as e:
    # If there's an error loading from JSON, we'll use the hardcoded defaults
    print(f"Error loading model capabilities from JSON: {e}")


def get_model_capabilities(model_name: str) -> Dict[str, Any]:
    """
    Get the capabilities for a specific model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        Dict[str, Any]: The capabilities for the model
    """
    # Try exact match first
    if model_name in MODEL_CAPABILITIES:
        return MODEL_CAPABILITIES[model_name]
    
    # Try prefix match (for models with versions)
    for key in MODEL_CAPABILITIES:
        if model_name.startswith(key):
            return MODEL_CAPABILITIES[key]
    
    # Try provider/model format
    if "/" in model_name:
        provider, _ = model_name.split("/", 1)
        provider_models = {k: v for k, v in MODEL_CAPABILITIES.items() if k.startswith(f"{provider}/")}
        if provider_models:
            # Return the first model from this provider as a reasonable default
            return next(iter(provider_models.values()))
    
    # Return default capabilities
    return DEFAULT_MODEL_CAPABILITIES.copy()


def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Get the tool calling type for a model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        ToolCallingType: The appropriate tool calling type for the model
    """
    if not model_name:
        return ToolCallingType.NONE
    
    # Check direct mapping from model name
    model_lower = model_name.lower()
    if model_lower in MODEL_CAPABILITIES:
        return MODEL_CAPABILITIES[model_lower]["tool_calling_type"]
    
    # Try prefix matching for models with versions or variants
    for key in MODEL_CAPABILITIES:
        if model_lower.startswith(key):
            return MODEL_CAPABILITIES[key]["tool_calling_type"]
    
    # Check for provider prefix (e.g., anthropic/, groq/, etc.)
    if '/' in model_lower:
        provider, model = model_lower.split('/', 1)
        provider_models = [key for key in MODEL_CAPABILITIES if key.startswith(f"{provider}/")]
        if provider_models:
            # Use the first model with matching provider as a fallback
            return MODEL_CAPABILITIES[provider_models[0]]["tool_calling_type"]
    
    # Default
    return MODEL_CAPABILITIES["default"]["tool_calling_type"]


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