"""
Tool management module for LiteAgent.

This module provides functionality for registering and managing tools 
that can be used by the agent to perform various tasks.
"""

from pydantic import create_model, BaseModel
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union
import functools

# Global registry for tools
TOOLS = {}

class BaseTool:
    """Base class for all tools."""
    
    def __init__(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__ or f"Execute {self.name}"
        self.schema = self._create_schema()
        
    def _create_schema(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "Schema", **fields)
        ToolSchema.__doc__ = self.description
        return ToolSchema
    
    def _get_schema_fields(self, sig: inspect.Signature) -> Dict:
        """Extract fields from function signature for schema creation."""
        fields = {}
        for name, param in sig.parameters.items():
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Validate arguments using the schema
        validated_args = self.schema(**kwargs)
        # Execute the function with validated arguments
        return self.func(**validated_args.dict())
    
    def to_function_definition(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.schema.schema()  # Convert Pydantic model to JSON schema
        }


class FunctionTool(BaseTool):
    """Tool implementation for standalone functions."""
    
    def __init__(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(func, name, description)


class InstanceMethodTool(BaseTool):
    """Tool implementation for instance methods."""
    
    def __init__(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def _get_schema_fields(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def execute(self, **kwargs) -> Any:
        """Execute the instance method with the given arguments."""
        # Validate arguments using the schema
        validated_args = self.schema(**kwargs)
        
        # Check if this is a class method or static method
        if isinstance(self.instance, type):
            # For class methods and static methods, don't pass the instance
            return self.func(**validated_args.dict())
        else:
            # For instance methods, the wrapper already handles passing the instance
            return self.func(**validated_args.dict())


class StaticMethodTool(BaseTool):
    """Tool implementation for static methods."""
    
    def __init__(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, name, description)


def tool(func):
    """
    Decorator to auto-register a function as a tool.
    
    Args:
        func: The function to register as a tool
        
    Returns:
        The original function (unchanged)
    """
    # Determine the appropriate tool type
    if inspect.ismethod(func):
        # For bound methods
        if func.__self__ is not None:
            tool_instance = InstanceMethodTool(func, func.__self__)
        else:
            # For static/class methods
            tool_instance = StaticMethodTool(func)
    else:
        # For regular functions
        tool_instance = FunctionTool(func)
    
    # Register the tool
    TOOLS[tool_instance.name] = {
        "schema": tool_instance.schema,
        "function": tool_instance.func
    }
    
    return func


def register_tool(func=None, *, name=None, description=None):
    """
    Enhanced decorator to register a function as a tool with optional customization.
    
    Args:
        func: The function to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        TOOLS[tool_instance.name] = {
            "schema": tool_instance.schema,
            "function": tool_instance.func
        }
        
        return f
    
    # Handle both @register_tool and @register_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


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


def liteagent_tool(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)