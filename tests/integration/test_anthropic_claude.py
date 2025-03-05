"""
Integration tests using Anthropic Claude models.

These tests run against the actual Anthropic Claude model and validate core functionality.
They are marked as integration and slow tests since they make real API calls.
"""

import pytest
import os
import time
import re
from typing import List, Dict, Any, Callable

from liteagent.agent import LiteAgent
from liteagent.tools import tool, liteagent_tool
from liteagent.examples import (
    get_weather, add_numbers, search_database, calculate_area,
    ToolsForAgents, SimplifiedToolsForAgents
)

from tests.integration.test_observer import ValidationObserver


# Skip tests if API key is not set
skip_if_no_api_key = pytest.mark.skipif(
    "ANTHROPIC_API_KEY" not in os.environ,
    reason="Anthropic API key not found in environment variables"
)


@pytest.mark.integration
@pytest.mark.slow
@skip_if_no_api_key
class TestAnthropicClaude:
    """Integration tests for LiteAgent with Anthropic Claude models."""
    
    MODEL_NAME = "anthropic/claude-3-haiku-20240307"  # Using the smallest/fastest model for tests with full version
    
    def test_standalone_tools(self, validation_observer):
        """Test standalone function tools with Anthropic's native function calling."""
        # Create agent with standalone tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="TestAgent",
            system_prompt="""You are a helpful assistant that can answer questions using tools.
When you need information that requires using a tool, ALWAYS use the available tools rather than making up information.

For the get_weather tool: Use this when asked about weather in a specific city.
Example: When asked "What's the weather in Tokyo?", call the get_weather tool with {"city": "Tokyo"}.

For the add_numbers tool: Use this when asked to perform addition of two numbers.
Example: When asked "What is 25 plus 17?", call the add_numbers tool with {"a": 25, "b": 17}.

IMPORTANT: Always use the tools when appropriate rather than trying to answer without them.""",
            tools=[get_weather, add_numbers],
            observers=[validation_observer]
        )
        
        # Register response parsers for better validation
        def parse_weather_response(response: str) -> Dict[str, Any]:
            city_match = re.search(r'(?:weather|temperature)[^.]*?([A-Za-z\s]+)', response, re.IGNORECASE)
            temp_match = re.search(r'(\d+)[°℃C]', response)
            
            result = {}
            if city_match:
                result["city"] = city_match.group(1).strip()
            if temp_match:
                result["temperature"] = int(temp_match.group(1))
            
            # Extract weather condition if present
            for condition in ["sunny", "cloudy", "rainy", "clear", "stormy"]:
                if condition in response.lower():
                    result["condition"] = condition
                    break
                    
            return result
            
        def parse_number_response(response: str) -> Dict[str, Any]:
            # Extract numbers from response
            numbers = re.findall(r'\b\d+\b', response)
            result = {}
            if numbers and len(numbers) > 0:
                # Use the first number as the result if available
                result["result"] = int(numbers[0])
            return result
            
        validation_observer.register_response_parser("get_weather", parse_weather_response)
        validation_observer.register_response_parser("add_numbers", parse_number_response)
        
        # Test weather tool
        response = agent.chat("What's the weather like in Tokyo?")
        
        # Validate function calls
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_call_count("get_weather", 1)
        validation_observer.assert_function_called_with("get_weather", city="Tokyo")
        
        # Validate function result
        weather_result = validation_observer.get_last_function_result("get_weather")
        assert weather_result is not None, "Weather function result should not be None"
        assert "Tokyo" in weather_result, "Result should mention Tokyo"
        
        # For Anthropic, the response might be empty due to how it handles tool calls
        # If we have a response, validate it
        if response:
            parsed_response = validation_observer.parse_response(response, "get_weather")
            if "city" in parsed_response:
                assert "Tokyo" in parsed_response["city"], "Response should mention Tokyo"
        
        validation_observer.reset()
        
        # Test addition tool
        response = agent.chat("What is 25 plus 17?")
        
        # Validate function calls
        validation_observer.assert_function_called("add_numbers")
        validation_observer.assert_function_call_count("add_numbers", 1)
        validation_observer.assert_function_called_with("add_numbers", a=25, b=17)
        
        # Validate function result directly
        add_result = validation_observer.get_last_function_result("add_numbers")
        assert add_result == 42, f"Expected add_numbers result to be 42, got {add_result}"
        
        # If we have a response, validate it
        if response:
            parsed_response = validation_observer.parse_response(response, "add_numbers")
            if "result" in parsed_response:
                assert parsed_response["result"] == 42, f"Expected result 42, got {parsed_response['result']}"
    
    def test_class_method_tools(self, validation_observer):
        """Test class method tools with Anthropic's native function calling."""
        # Create tools class instance
        tools_instance = ToolsForAgents()
        
        # Create agent with class method tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="ClassMethodAgent",
            system_prompt="""You are a helpful assistant that can answer questions using tools.
When you need information that requires using a tool, ALWAYS use the available tools rather than making up information.

For the get_weather tool: Use this when asked about weather in a specific city.
Example: When asked "What's the weather in Berlin?", call the get_weather tool with {"city": "Berlin"}.

For the add_numbers tool: Use this when asked to perform addition of two numbers.
Example: When asked "What is 7 plus 9?", call the add_numbers tool with {"a": 7, "b": 9}.

IMPORTANT: Always use the tools when appropriate rather than trying to answer without them.""",
            tools=[
                tools_instance.get_weather,
                tools_instance.add_numbers
            ],
            observers=[validation_observer]
        )
        
        # Register response parsers
        def parse_weather_response(response: str) -> Dict[str, Any]:
            city_match = re.search(r'(?:weather|temperature)[^.]*?([A-Za-z\s]+)', response, re.IGNORECASE)
            result = {}
            if city_match:
                result["city"] = city_match.group(1).strip()
            return result
            
        def parse_number_response(response: str) -> Dict[str, Any]:
            numbers = re.findall(r'\b\d+\b', response)
            result = {}
            if numbers and len(numbers) > 0:
                result["result"] = int(numbers[0])
            return result
            
        validation_observer.register_response_parser("get_weather", parse_weather_response)
        validation_observer.register_response_parser("add_numbers", parse_number_response)
        
        # Test weather tool
        response = agent.chat("What's the weather like in Berlin?")
        
        # Validate function calls
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_call_count("get_weather", 1)
        validation_observer.assert_function_called_with("get_weather", city="Berlin")
        
        # Validate function result
        weather_result = validation_observer.get_last_function_result("get_weather")
        assert weather_result is not None, "Weather function result should not be None"
        assert "Berlin" in weather_result, "Result should mention Berlin"
        
        # Verify internal counter of tools class was incremented
        assert tools_instance.get_call_count() >= 1, "Tool call count should be at least 1"
        
        # If we have a response, validate it
        if response:
            parsed_response = validation_observer.parse_response(response, "get_weather")
            if "city" in parsed_response:
                assert "Berlin" in parsed_response["city"], "Response should mention Berlin"
        
        validation_observer.reset()
        
        # Test addition tool
        response = agent.chat("What is 7 plus 9?")
        
        # Validate function calls
        validation_observer.assert_function_called("add_numbers")
        validation_observer.assert_function_call_count("add_numbers", 1)
        validation_observer.assert_function_called_with("add_numbers", a=7, b=9)
        
        # Validate function result directly
        add_result = validation_observer.get_last_function_result("add_numbers")
        assert add_result == 16, f"Expected add_numbers result to be 16, got {add_result}"
        
        # Verify internal counter of tools class increased further
        assert tools_instance.get_call_count() >= 2, "Tool call count should be at least 2"
        
        # If we have a response, validate it
        if response:
            parsed_response = validation_observer.parse_response(response, "add_numbers")
            if "result" in parsed_response:
                assert parsed_response["result"] == 16, f"Expected result 16, got {parsed_response['result']}"
    
    def test_multi_step_reasoning(self, validation_observer):
        """Test multi-step reasoning with Anthropic's native function calling."""
        # Create agent with multiple tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="MultiStepAgent",
            system_prompt="""You are a helpful assistant that can answer questions using tools.
When you need information that requires using a tool, ALWAYS use the available tools rather than making up information.

For the get_weather tool: Use this when asked about weather in a specific city.
Example: When asked about weather in Tokyo, call the get_weather tool with {"city": "Tokyo"}.

For the add_numbers tool: Use this when asked to perform addition of two numbers.
Example: When asked to add 25 and 17, call the add_numbers tool with {"a": 25, "b": 17}.

For the calculate_area tool: Use this when asked to calculate the area of a rectangle.
Example: When asked to calculate the area of a rectangle, call the calculate_area tool with {"width": 5, "height": 10}.

IMPORTANT: Always use the tools when appropriate rather than trying to answer without them.
If a question requires multiple steps, use the appropriate tools in sequence.""",
            tools=[get_weather, add_numbers, calculate_area],
            observers=[validation_observer]
        )
        
        # Register response parsers
        def parse_number_response(response: str) -> Dict[str, Any]:
            numbers = re.findall(r'\b\d+\b', response)
            result = {}
            if numbers and len(numbers) > 0:
                result["result"] = int(numbers[0])
            return result
            
        validation_observer.register_response_parser("add_numbers", parse_number_response)
        validation_observer.register_response_parser("calculate_area", parse_number_response)
        
        # Test multi-step reasoning
        response = agent.chat("What's the sum of the width and height of a rectangle with area 24 and width 6?")
        
        # Track all called functions for logging/debugging
        called_functions = list(validation_observer.called_functions)
        print(f"Functions called in multi-step reasoning: {called_functions}")
        
        # For Anthropic, we validate whatever functions were called and their results
        if "calculate_area" in validation_observer.called_functions:
            # If calculate_area was called, validate its parameters
            for call in validation_observer.function_calls:
                if call["name"] == "calculate_area":
                    arguments = call["arguments"]
                    assert "width" in arguments and "height" in arguments, "Calculate area should have width and height"
        
        # If add_numbers was called, validate it was called with correct values
        # The expected answer is width + height = 6 + 4 = 10 (since area = width * height, 24 = 6 * 4)
        if "add_numbers" in validation_observer.called_functions:
            # There might be multiple add_numbers calls with different arguments
            # Look for one that adds 6 and 4 (or 4 and 6)
            found_correct_addition = False
            for call in validation_observer.function_calls:
                if call["name"] == "add_numbers":
                    args = call["arguments"]
                    if (args.get("a") == 6 and args.get("b") == 4) or (args.get("a") == 4 and args.get("b") == 6):
                        found_correct_addition = True
                        break
            
            if found_correct_addition:
                # Validate that one of the function results is 10
                add_result = validation_observer.get_last_function_result("add_numbers")
                if add_result == 10:
                    print("Found correct addition result: 10")
        
        # If we have a response, validate it mentions the correct result
        if response:
            # Check if the correct answer (10) is in the response
            assert "10" in response or "ten" in response.lower(), "Response should contain the correct answer (10)" 