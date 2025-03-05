"""
Enhanced tool calling type definitions and model capabilities registry.

This module provides a more structured approach to defining tool calling capabilities
for different language models, with clear separation of concerns and validation strategies.
"""

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


# Model capabilities registry
MODEL_CAPABILITIES = {
    # OpenAI models
    "gpt-4": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": True,
        "max_tools_per_request": 128,
    },
    "gpt-4o": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": True,
        "max_tools_per_request": 128,
    },
    "gpt-4o-mini": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": True,
        "max_tools_per_request": 64,
    },
    "gpt-3.5-turbo": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    
    # Anthropic models
    "anthropic/claude-3-opus-20240229": {
        "tool_calling_type": ToolCallingType.ANTHROPIC_TOOL_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    "anthropic/claude-3-sonnet-20240229": {
        "tool_calling_type": ToolCallingType.ANTHROPIC_TOOL_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    "anthropic/claude-3-haiku-20240307": {
        "tool_calling_type": ToolCallingType.ANTHROPIC_TOOL_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    "anthropic/claude-3.5-sonnet": {
        "tool_calling_type": ToolCallingType.ANTHROPIC_TOOL_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    
    # Groq models (use OpenAI-compatible format)
    "groq/llama-3.1-8b-instant": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    "groq/llama-3.2-1b-preview": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    "groq/llama-3.2-3b-preview": {
        "tool_calling_type": ToolCallingType.OPENAI_FUNCTION_CALLING,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 64,
    },
    
    # Ollama models
    "ollama/llama3": {
        "tool_calling_type": ToolCallingType.JSON_EXTRACTION,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 16,
    },
    "ollama/phi3": {
        "tool_calling_type": ToolCallingType.JSON_EXTRACTION,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 16,
    },
    
    # Mistral models
    "mistral/mistral-small": {
        "tool_calling_type": ToolCallingType.PROMPT_BASED,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 16,
    },
    "mistral/mistral-medium": {
        "tool_calling_type": ToolCallingType.PROMPT_BASED,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 16,
    },
    
    # Cohere models
    "cohere/command": {
        "tool_calling_type": ToolCallingType.PROMPT_BASED,
        "supports_multiple_tools": True,
        "supports_nested_tools": False,
        "max_tools_per_request": 16,
    },
}

# Default capabilities for unknown models
DEFAULT_MODEL_CAPABILITIES = {
    "tool_calling_type": ToolCallingType.PROMPT_BASED,
    "supports_multiple_tools": False,
    "supports_nested_tools": False,
    "max_tools_per_request": 1,
}


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
    Get the tool calling type for a specific model.
    
    Args:
        model_name: The name of the model
        
    Returns:
        ToolCallingType: The tool calling type for the model
    """
    capabilities = get_model_capabilities(model_name)
    return capabilities["tool_calling_type"]


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