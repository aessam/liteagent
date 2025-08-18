"""
Unit tests for the tools module.

This module contains tests for the core tool functionality of LiteAgent,
including the BaseTool and InstanceMethodTool classes.
"""

import pytest
import inspect
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from liteagent.tools import BaseTool, InstanceMethodTool, FunctionTool, TOOLS

class TestBaseTool:
    """Test the BaseTool class."""
    
    def test_base_tool_initialization(self):
        """Test that a BaseTool can be initialized correctly."""
        # Define a simple function to wrap
        def test_function(param1: str, param2: int) -> str:
            """Test function docstring."""
            return f"{param1} {param2}"
        
        # Create a BaseTool
        tool = BaseTool(test_function)
        
        # Check that the tool has the correct properties
        assert tool.name == "test_function"
        assert tool.description == "Test function docstring."
        assert tool.func == test_function
        
        # Check that the schema was created correctly
        assert tool.schema.__name__ == "test_functionSchema"
        field_types = {name: field.annotation for name, field in tool.schema.model_fields.items()}
        assert field_types["param1"] == str
        assert field_types["param2"] == int
        
        # Check that the function definition is correct
        func_def = tool.to_function_definition()
        assert func_def["name"] == "test_function"
        assert func_def["description"] == "Test function docstring."
        assert "parameters" in func_def
        
        # Test execution
        result = tool.execute(param1="hello", param2=42)
        assert result == "hello 42"
    
    def test_base_tool_with_custom_name_and_description(self):
        """Test that a BaseTool can be created with custom name and description."""
        def test_function(param: str) -> str:
            """Original docstring."""
            return f"Result: {param}"
        
        custom_name = "custom_name"
        custom_desc = "Custom description."
        
        tool = BaseTool(test_function, name=custom_name, description=custom_desc)
        
        assert tool.name == custom_name
        assert tool.description == custom_desc
        
        # Check function definition
        func_def = tool.to_function_definition()
        assert func_def["name"] == custom_name
        assert func_def["description"] == custom_desc
        
    def test_base_tool_without_annotations(self):
        """Test that a BaseTool can handle functions without type annotations."""
        # Define a function without type annotations
        def test_function(param1, param2):
            """Function without annotations."""
            return f"{param1} {param2}"
        
        # Create a BaseTool
        tool = BaseTool(test_function)
        
        # Check that the schema was created with Any types
        field_types = {name: field.annotation for name, field in tool.schema.model_fields.items()}
        assert field_types["param1"] == Any
        assert field_types["param2"] == Any
        
        # Test execution
        result = tool.execute(param1="hello", param2=42)
        assert result == "hello 42"
    
    def test_base_tool_without_docstring(self):
        """Test that a BaseTool handles functions without docstrings."""
        # Function without docstring
        def no_doc_func(param1: str):
            return f"Result: {param1}"
        
        # Create a BaseTool
        tool = BaseTool(no_doc_func)
        
        # Check description falls back to default
        assert tool.description == f"Execute {tool.name}"
    
    def test_base_tool_to_function_definition(self):
        """Test that a BaseTool can generate a proper function definition."""
        # Function with various parameter types
        def complex_func(
            text: str,
            number: int,
            flag: bool = False,
            items: Optional[List[str]] = None,
            data: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Any]:
            """Complex function with multiple parameter types."""
            return {"result": text}
        
        # Create a BaseTool
        tool = BaseTool(complex_func)
        
        # Generate function definition
        func_def = tool.to_function_definition()
        
        # Check function definition properties
        assert func_def["name"] == "complex_func"
        assert func_def["description"] == "Complex function with multiple parameter types."
        assert "parameters" in func_def
        
        # Check parameters
        params = func_def["parameters"]
        assert params["type"] == "object"
        assert "properties" in params
        assert "text" in params["properties"]
        assert "number" in params["properties"]
        assert "flag" in params["properties"]
        assert "items" in params["properties"]
        assert "data" in params["properties"]
    
    def test_base_tool_execute(self):
        """Test that a BaseTool can execute its function correctly."""
        # Test function
        def add_numbers(a: int, b: int) -> int:
            """Add two numbers together."""
            return a + b
        
        # Create a BaseTool
        tool = BaseTool(add_numbers)
        
        # Execute the tool
        result = tool.execute(a=5, b=3)
        
        # Check the result
        assert result == 8
        
        # Test with invalid arguments
        with pytest.raises(Exception):
            tool.execute(a="not_a_number", b=3)


class TestInstanceMethodTool:
    """Test the InstanceMethodTool class."""
    
    def test_instance_method_tool_with_instance_method(self):
        """Test that a InstanceMethodTool can wrap an instance method correctly."""
        # Test class with instance method
        class TestClass:
            def __init__(self, base_value: int):
                self.base_value = base_value
                
            def add_to_base(self, value: int) -> int:
                """Add a value to the base value."""
                return self.base_value + value
        
        # Create an instance
        instance = TestClass(10)
        
        # Create a InstanceMethodTool from the instance method
        tool = InstanceMethodTool(instance.add_to_base, instance)
        
        # Check tool properties
        assert tool.name == "add_to_base"
        assert tool.description == "Add a value to the base value."
        
        # Execute the tool
        result = tool.execute(value=5)
        
        # Check that the method was correctly bound to the instance
        assert result == 15
    
    def test_instance_method_tool_with_class_method(self):
        """Test that a InstanceMethodTool can wrap a class method correctly."""
        # Test class with class method
        class TestClass:
            base_value = 10
            
            @classmethod
            def multiply_base(cls, value: int) -> int:
                """Multiply a value by the base value."""
                return cls.base_value * value
        
        # Create a InstanceMethodTool from the class method
        tool = InstanceMethodTool(TestClass.multiply_base, TestClass)
        
        # Check tool properties
        assert tool.name == "multiply_base"
        assert tool.description == "Multiply a value by the base value."
        
        # Execute the tool
        result = tool.execute(value=5)
        
        # Check that the method was correctly bound to the class
        assert result == 50
    
    def test_instance_method_tool_with_static_method(self):
        """Test that a InstanceMethodTool can wrap a static method correctly."""
        # Test class with static method
        class TestClass:
            @staticmethod
            def add_numbers(a: int, b: int) -> int:
                """Add two numbers together."""
                return a + b
        
        # Create a InstanceMethodTool from the static method
        tool = InstanceMethodTool(TestClass.add_numbers, TestClass)
        
        # Check tool properties
        assert tool.name == "add_numbers"
        assert tool.description == "Add two numbers together."
        
        # Execute the tool
        result = tool.execute(a=5, b=3)
        
        # Check that the static method was executed correctly
        assert result == 8
    
    def test_instance_method_tool_with_custom_name_description(self):
        """Test that a InstanceMethodTool can be created with custom name and description."""
        # Test class
        class TestClass:
            def test_method(self, param: str) -> str:
                """Original docstring."""
                return f"Result: {param}"
        
        # Create an instance
        instance = TestClass()
        
        # Create a InstanceMethodTool with custom name and description
        custom_name = "custom_method_name"
        custom_desc = "Custom method description."
        tool = InstanceMethodTool(instance.test_method, instance, name=custom_name, description=custom_desc)
        
        # Check custom properties
        assert tool.name == custom_name
        assert tool.description == custom_desc
        
        # Execute the tool
        result = tool.execute(param="test")
        
        # Check that the method still works correctly
        assert result == "Result: test"


if __name__ == "__main__":
    pytest.main(["-v", "test_tools.py"]) 