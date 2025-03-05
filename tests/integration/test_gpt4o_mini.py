"""
Integration tests using gpt-4o-mini model.

These tests run against the actual OpenAI gpt-4o-mini model and validate core functionality.
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
    "OPENAI_API_KEY" not in os.environ,
    reason="OpenAI API key not found in environment variables"
)


@pytest.mark.integration
@pytest.mark.slow
@skip_if_no_api_key
class TestGPT4OMini:
    """Integration tests for LiteAgent with gpt-4o-mini."""
    
    MODEL_NAME = "gpt-4o-mini"
    
    def test_standalone_tools(self, validation_observer):
        """Test standalone function tools from examples.py."""
        # Create agent with standalone tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="TestAgent",
            system_prompt="""You are a helpful assistant that can answer questions using tools.
When you need information that requires using a tool, ALWAYS use the available tools rather than making up information.

For the get_weather tool: Use this when asked about weather in a specific city.
Example: When asked "What's the weather in Tokyo?", call the get_weather tool with {"city": "Tokyo"}.

For the add_numbers tool: Use this when asked to perform addition of two numbers.
Example: When asked "What is 42 + 17?", call the add_numbers tool with {"a": 42, "b": 17}.

For the search_database tool: Use this when asked to search for information in a database.
Example: When asked "Search for climate change", call the search_database tool with {"query": "climate change", "limit": 5}.

IMPORTANT: You MUST use these tools when applicable. Do not try to answer questions that require these tools without calling them first.""",
            tools=[get_weather, add_numbers, search_database],
            observers=[validation_observer]
        )
        
        # Register a custom parser for the weather response
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
            
        validation_observer.register_response_parser("get_weather", parse_weather_response)
        
        # Test weather tool
        response = agent.chat("What's the weather in Tokyo?")
        
        # Verify function calls
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_call_count("get_weather", 1)
        validation_observer.assert_function_called_with("get_weather", city="Tokyo")
        
        # Verify function result structure
        validation_observer.assert_function_result_structure(
            "get_weather", 
            {
                # Using a lambda for flexible validation of the result string
                # This is better than checking for string containment
                "city": lambda x: "Tokyo" in x
            }
        )
        
        # Use structured response validation instead of string matching
        validation_observer.assert_response_contains_structure(
            response,
            {
                "city": "Tokyo",
                "temperature": lambda x: x is not None,
                "condition": lambda x: x in ["sunny", "cloudy", "rainy", "clear", "stormy"]
            },
            function_name="get_weather"
        )
        
        # Reset observer state
        validation_observer.reset()
        
        # Test add_numbers tool
        response = agent.chat("What is 42 + 17?")
        
        # Verify function calls
        validation_observer.assert_function_called("add_numbers")
        validation_observer.assert_function_call_count("add_numbers", 1)
        validation_observer.assert_function_called_with("add_numbers", a=42, b=17)
        
        # Verify function result directly - it's an integer
        result = validation_observer.get_last_function_result("add_numbers")
        assert result == 59, f"Expected result 59, got {result}"
        
        # For number results, create a simple extractor
        def parse_number_response(response: str) -> Dict[str, Any]:
            # Extract numbers from response
            numbers = re.findall(r'\b\d+\b', response)
            result = {}
            if numbers:
                result["result"] = int(numbers[0])
            return result
            
        validation_observer.register_response_parser("add_numbers", parse_number_response)
        
        # Use structured response validation
        validation_observer.assert_response_contains_structure(
            response,
            {"result": 59}
        )
        
        # Reset observer state
        validation_observer.reset()
        
        # Test search_database tool with limit parameter
        response = agent.chat("Search the database for 'climate change' and limit the results to 3.")
        
        # Verify function calls
        validation_observer.assert_function_called("search_database")
        validation_observer.assert_function_call_count("search_database", 1)
        validation_observer.assert_function_called_with("search_database", query="climate change", limit=3)
        
        # Verify list result length
        validation_observer.assert_function_result_list_length("search_database", 3)
        
        # Verify each result has the expected structure
        search_result = validation_observer.get_last_function_result("search_database")
        for item in search_result:
            assert "id" in item, f"Missing 'id' field in result item: {item}"
            assert "title" in item, f"Missing 'title' field in result item: {item}"
            assert "score" in item, f"Missing 'score' field in result item: {item}"
            assert "climate change" in item["title"].lower(), f"Expected 'climate change' in title: {item['title']}"
            
        # Validate the response contains information about climate change
        assert "climate change" in response.lower()
        assert "result" in response.lower() or "found" in response.lower()
        
    def test_class_methods_as_tools(self, validation_observer):
        """Test class methods as tools from examples.py."""
        # Create instance of ToolsForAgents
        tools_instance = ToolsForAgents(api_key="fake-api-key-12345")
        
        # Create agent with class methods as tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="ClassMethodsAgent",
            system_prompt="""You are a helpful assistant that can perform math operations and check the weather.
When you need to perform calculations or get weather information, ALWAYS use the available tools rather than making up information.

For the multiply_numbers tool: Use this when asked to multiply two numbers.
Example: When asked "What is 7 times 8?", call the multiply_numbers tool with {"a": 7, "b": 8}.

For the add_numbers tool: Use this when asked to add two numbers.
Example: When asked "What is 5 plus 3?", call the add_numbers tool with {"a": 5, "b": 3}.

For the get_weather tool: Use this when asked about weather in a specific city.
Example: When asked "What's the weather in Paris?", call the get_weather tool with {"city": "Paris"}.

IMPORTANT: You MUST use these tools when applicable. Do not try to answer questions that require these tools without calling them first.""",
            tools=[
                tools_instance.add_numbers,
                tools_instance.multiply_numbers,
                tools_instance.get_weather
            ],
            observers=[validation_observer]
        )
        
        # Test multiply_numbers tool
        response = agent.chat("What is 7 times 8?")
        
        # First, validate the function call
        validation_observer.assert_function_called("multiply_numbers")
        validation_observer.assert_function_call_count("multiply_numbers", 1)
        validation_observer.assert_function_called_with("multiply_numbers", a=7, b=8)
        
        # Then validate the function result directly
        result = validation_observer.get_last_function_result("multiply_numbers")
        assert result == 56, f"Expected result 56, got {result}"
        
        # Register a number result parser
        def parse_number_response(response: str) -> Dict[str, Any]:
            # Extract numbers from response
            numbers = re.findall(r'\b\d+\b', response)
            result = {}
            if numbers:
                result["result"] = int(numbers[0])
            return result
            
        validation_observer.register_response_parser("multiply_numbers", parse_number_response)
        
        # Use structured response validation
        validation_observer.assert_response_contains_structure(
            response,
            {"result": 56}
        )
        
        # Verify internal counter of the tools class matches our observer count
        assert tools_instance.get_call_count() == 1
        
        # Reset observer state
        validation_observer.reset()
        
        # Test weather with API key
        response = agent.chat("What's the weather in Berlin?")
        
        # First, validate the function call
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_call_count("get_weather", 1)
        validation_observer.assert_function_called_with("get_weather", city="Berlin")
        
        # Check internal counter was incremented
        assert tools_instance.get_call_count() == 2, "Tool call count should be 2"
        
        # If the response contains API key information, validate that
        if "API key" in response:
            assert "fake-api-key" in validation_observer.get_last_function_result("get_weather")
        # Otherwise validate it contains information about Berlin
        else:
            assert "Berlin" in validation_observer.get_last_function_result("get_weather")
    
    def test_decorated_class_methods(self, validation_observer):
        """Test decorated class methods as tools."""
        # Create instance of SimplifiedToolsForAgents
        tools_instance = SimplifiedToolsForAgents()
        
        # Create agent with decorated class methods as tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="DecoratedMethodsAgent",
            system_prompt="""You are a helpful assistant that can perform math operations.
When you need to perform calculations, ALWAYS use the available tools rather than calculating manually.

For the add_numbers tool: Use this when asked to add two numbers.
Example: When asked "What is 10 plus 20?", call the add_numbers tool with {"a": 10, "b": 20}.

For the multiply_numbers tool: Use this when asked to multiply two numbers.
Example: When asked "What is 6 times 7?", call the multiply_numbers tool with {"a": 6, "b": 7}.

For the calculate_area tool: Use this when asked to calculate the area of a rectangle.
Example: When asked "Calculate the area of a rectangle with width 5 and height 3", call the calculate_area tool with {"width": 5, "height": 3}.

IMPORTANT: You MUST use these tools when applicable. Do not try to answer questions that require these tools without calling them first.""",
            tools=[
                tools_instance.add_numbers,
                tools_instance.multiply_numbers,
                calculate_area
            ],
            observers=[validation_observer]
        )
        
        # Instead of a complex multi-step test, test each tool individually
        # Test add_numbers first
        response = agent.chat("Add 25 and 18 using the add_numbers tool")
        # Verify the tool was called
        print(f"\nCalled functions after add: {validation_observer.called_functions}")
        assert "add_numbers" in validation_observer.called_functions
        assert "43" in response
        
        # Reset observer state
        validation_observer.reset()
        
        # Test multiply_numbers next
        response = agent.chat("Multiply 7 and 9 using the multiply_numbers tool")
        # Verify the tool was called
        print(f"\nCalled functions after multiply: {validation_observer.called_functions}")
        assert "multiply_numbers" in validation_observer.called_functions
        assert "63" in response
        
        # Reset observer state
        validation_observer.reset()
        
        # Test calculate_area last
        response = agent.chat("Calculate the area of a rectangle with width 8 and height 5 using the calculate_area tool")
        # Verify the tool was called
        print(f"\nCalled functions after area: {validation_observer.called_functions}")
        assert "calculate_area" in validation_observer.called_functions
        assert "40" in response

    def test_multi_step_reasoning(self, validation_observer):
        """Test multi-step reasoning with tools."""
        # Create agent with tools for multi-step reasoning
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="MultiStepAgent",
            system_prompt="""You are a helpful assistant that can solve complex problems using tools.
When solving problems that require multiple steps, break down the problem and use the appropriate tools for each step.

For the add_numbers tool: Use this when you need to add two numbers.
Example: When asked "What is 3 plus 4?", call the add_numbers tool with {"a": 3, "b": 4}.

For the calculate_area tool: Use this when you need to calculate the area of a rectangle.
Example: When asked "Calculate the area of a rectangle with width 5 and height 3", call the calculate_area tool with {"width": 5, "height": 3}.

IMPORTANT: You MUST use these tools when applicable. Do not try to answer questions that require these tools without calling them first.""",
            tools=[add_numbers, calculate_area],
            observers=[validation_observer]
        )
        
        # Ask a multi-step question with integers instead of floating point to avoid validation errors
        response = agent.chat(
            "I have a rectangle with width 6 meters and height 4 meters. "
            "If I add 2 meters to the width and 3 meters to the height, "
            "what will be the area of the new rectangle? Use the tools to calculate this."
        )
        
        # Print function calls for debugging
        print(f"\nCalled functions: {validation_observer.called_functions}")
        print(f"Response: {response}")
        
        # Check for results in the response
        assert "6" in response and "4" in response  # Original dimensions
        assert "2" in response and "3" in response  # Added dimensions
        assert "8" in response and "7" in response  # New dimensions
        # The correct answer should be (6+2)*(4+3) = 8*7 = 56
        assert "56" in response
        
        # Verify at least one tool was called
        assert len(validation_observer.called_functions) > 0 