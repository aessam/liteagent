"""
Tool management module for LiteAgent.

This module provides functionality for registering and managing tools 
that can be used by the agent to perform various tasks.
"""

from pydantic import create_model, BaseModel
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union
import functools
import random

# Global registry for tools
TOOLS = {}

class ToolsForAgents:
    """
    A class containing tools that can be used by agents.
    
    DEPRECATED: This class has been moved to tests.utils.test_tools.ToolsForAgents as it
    is primarily intended for testing purposes. Use that version instead.
    """
    
    def __init__(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return self._instance.add_numbers(a, b)
        
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return self._instance.multiply_numbers(a, b)
        
    def get_weather(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        return self._instance.get_weather(city)
    
    def get_user_data(self, user_id: str) -> Dict:
        """
        Retrieves user data for a specific user ID.
        This tool returns information the LLM couldn't possibly know.
        """
        return self._instance.get_user_data(user_id)
            
    def get_call_count(self) -> int:
        """Returns the number of times a tool was called."""
        return self._instance.get_call_count()

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
        return self.func(**validated_args.model_dump())
    
    def to_function_definition(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.schema.model_json_schema()  # Convert Pydantic model to JSON schema
        }
        
    def to_dict(self) -> Dict:
        """Alias for to_function_definition for compatibility with new tool calling system."""
        return self.to_function_definition()


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
        """Execute the tool with the given arguments."""
        # Validate arguments using the schema
        validated_args = self.schema(**kwargs)
        
        # The wrapper function created in __init__ already handles the instance correctly
        return self.func(**validated_args.model_dump())


class StaticMethodTool(BaseTool):
    """Tool implementation for static methods."""
    
    def __init__(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, name, description)


def get_function_definitions(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
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
    
    This is the preferred way to register tools in LiteAgent.
    
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