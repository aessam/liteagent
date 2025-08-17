"""
Compatibility module for tool calling types.

This module provides backward compatibility for tests that reference
the old tool calling type system.
"""

from enum import Enum
from typing import Optional
from .capabilities import get_model_capabilities


class ToolCallingType(Enum):
    """Enum representing different tool calling capabilities."""
    NONE = "none"
    BASIC = "basic"
    PARALLEL = "parallel"
    ADVANCED = "advanced"


def get_tool_calling_type(model_name: str) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = get_model_capabilities(model_name)
    
    if not capabilities or not capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC