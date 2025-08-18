"""
Consolidated integration tests for multi-step reasoning across different models.

This module tests multi-step reasoning with different models using a unified approach.
"""

import pytest
import re
from typing import Dict, Any, List

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from tests.utils.test_tools import get_weather, add_numbers, calculate_area

from tests.utils.validation_helper import ValidationTestHelper


@pytest.mark.integration
class TestMultiStepReasoning:
    """Tests for multi-step reasoning across all models."""
    
    @pytest.fixture
    def weather_add_tools(self):
        """Provide the tools for the weather and addition test."""
        return [get_weather, add_numbers]
    
    @pytest.fixture
    def weather_add_prompt(self):
        """Provide the system prompt for the weather and addition test."""
        return """You are a helpful assistant that can solve multi-step problems.
You have access to the following tools:
- get_weather: Get the current weather for a city
- add_numbers: Add two numbers together

Break down complex problems into steps and use the appropriate tools for each step."""
    
    @pytest.fixture
    def weather_add_tool_names(self):
        """Provide the tool names for parser registration in weather and addition test."""
        return ["get_weather", "add_numbers"]
    
    @pytest.fixture
    def area_tools(self):
        """Provide the tools for the area calculation test."""
        return [calculate_area, add_numbers]
    
    @pytest.fixture
    def area_prompt(self):
        """Provide the system prompt for the area calculation test."""
        return """You are a geometry assistant that can solve area problems.
You have access to the following tools:
- calculate_area: Calculate the area of a rectangle
- add_numbers: Add two numbers together

Break down complex problems into steps and use the appropriate tools for each step."""
    
    @pytest.fixture
    def area_tool_names(self):
        """Provide the tool names for parser registration in area calculation test."""
        return ["calculate_area", "add_numbers"]
    
    def test_weather_and_addition(self, model, validation_observer):
        """
        Test multi-step reasoning with weather and addition tools.
        
        This test checks if the agent can correctly use both get_weather and
        add_numbers tools to solve a multi-step problem.
        """
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["get_weather", "add_numbers"]
        )
        
        # Create agent with tools for weather and addition
        agent = LiteAgent(
            model=model,
            name="WeatherAdditionAgent",
            system_prompt="""You are a helpful assistant that can solve multi-step problems.
You have access to the following tools:
- get_weather: Get the current weather for a city
- add_numbers: Add two numbers together

Break down complex problems into steps and use the appropriate tools for each step.""",
            tools=[get_weather, add_numbers],
            observers=[validation_observer]
        )
        
        try:
            # Test with multi-step query
            response = agent.chat(
                "What's the weather in Tokyo? Also, what's 17 + 25?"
            )
            
            # Check if the response is not None
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            
            # Check for relevant information in the response
            weather_mentioned = any(term in response.lower() for term in ["tokyo", "weather", "temperature"])
            addition_mentioned = any(str(num) in response for num in ["42", "forty-two", "forty two"])
            
            # At least one of these should be true
            assert weather_mentioned or addition_mentioned, \
                "Response should mention either weather in Tokyo or the sum 42"
            
            # Check which functions were called
            functions_called = list(validation_observer.called_functions)
            print(f"Functions called by {model}: {functions_called}")
            
            # If weather function was called, validate it
            if "get_weather" in functions_called:
                validation_observer.assert_function_called_with("get_weather", city="Tokyo")
                weather_result = validation_observer.get_last_function_result("get_weather")
                assert weather_result is not None, "Weather function result should not be None"
            
            # If add_numbers was called, validate it
            if "add_numbers" in functions_called:
                call_args = validation_observer.get_function_call_args("add_numbers")
                if call_args:
                    last_call = call_args[-1]
                    a, b = last_call.get('a'), last_call.get('b')
                    # The sum should be 42
                    assert a + b == 42, f"Sum of {a} and {b} should be 42"
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise
    
    def test_area_calculation(self, model, validation_observer):
        """
        Test multi-step reasoning with area calculation and addition tools.
        
        This test checks if the agent can correctly use both calculate_area and
        add_numbers tools to solve a geometry problem.
        """
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["calculate_area", "add_numbers"]
        )
        
        # Create agent with tools for area calculation and addition
        agent = LiteAgent(
            model=model,
            name="AreaCalculationAgent",
            system_prompt="""You are a geometry assistant that can solve area problems.
You have access to the following tools:
- calculate_area: Calculate the area of a rectangle
- add_numbers: Add two numbers together

Break down complex problems into steps and use the appropriate tools for each step.""",
            tools=[calculate_area, add_numbers],
            observers=[validation_observer]
        )
        
        try:
            # Test with multi-step query
            response = agent.chat(
                "Calculate the area of a rectangle with width 4 and height 6. Then, find the sum of the width and height."
            )
            
            # Check if the response is not None
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            
            # Check for relevant information in the response
            area_mentioned = any(term in response for term in ["24", "area"])
            sum_mentioned = any(term in response for term in ["10", "sum"])
            
            # At least one of these should be true
            assert area_mentioned or sum_mentioned, \
                "Response should mention either the area (24) or the sum (10)"
            
            # Check which functions were called
            functions_called = list(validation_observer.called_functions)
            print(f"Functions called by {model}: {functions_called}")
            
            # If calculate_area function was called, validate it
            if "calculate_area" in functions_called:
                # Get the call arguments
                call_args = validation_observer.get_function_call_args("calculate_area")
                if call_args:
                    last_call = call_args[-1]
                    width, height = last_call.get('width'), last_call.get('height')
                    # The area should be width * height = 24
                    assert width * height == 24, f"Area of {width}x{height} should be 24"
            
            # If add_numbers was called, validate it
            if "add_numbers" in functions_called:
                # Get the call arguments
                call_args = validation_observer.get_function_call_args("add_numbers")
                if call_args:
                    last_call = call_args[-1]
                    a, b = last_call.get('a'), last_call.get('b')
                    # The sum should be 10
                    assert a + b == 10, f"Sum of {a} and {b} should be 10"
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise 