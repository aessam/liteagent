"""
Tool management module for LiteAgent.

This module provides functionality for registering and managing tools 
that can be used by the agent to perform various tasks.
"""

from pydantic import create_model
import inspect

# Global registry for tools
TOOLS = {}

def tool(func):
    """
    Decorator to auto-register a function as a tool.
    Dynamically creates a Pydantic model from the function signature.
    
    Args:
        func: The function to register as a tool
        
    Returns:
        The original function (unchanged)
    """
    sig = inspect.signature(func)
    fields = {name: (param.annotation, ...) for name, param in sig.parameters.items()}
    ToolSchema = create_model(func.__name__ + "Schema", **fields)
    # Add the function's docstring to the schema
    ToolSchema.__doc__ = func.__doc__ or f"Execute {func.__name__}"
    TOOLS[func.__name__] = {"schema": ToolSchema, "function": func}
    return func

def get_tools():
    """
    Get all registered tools.
    
    Returns:
        dict: Dictionary of registered tools
    """
    return TOOLS

def get_function_definitions():
    """
    Convert registered tools to function definitions compatible with LLM APIs.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    for tool_name, tool_data in TOOLS.items():
        schema = tool_data["schema"]
        function_definitions.append({
            "name": tool_name,
            "description": schema.__doc__,
            "parameters": schema.schema()  # Convert Pydantic model to JSON schema
        })
    return function_definitions