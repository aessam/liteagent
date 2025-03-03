"""
Integration tests using gpt-4o-mini model.

These tests run against the actual OpenAI gpt-4o-mini model and validate core functionality.
They are marked as integration and slow tests since they make real API calls.
"""

import pytest
import os
import time
from typing import List, Dict

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
            system_prompt="You are a helpful assistant that can answer questions using tools.",
            tools=[get_weather, add_numbers, search_database],
            observers=[validation_observer]
        )
        
        # Test weather tool
        response = agent.chat("What's the weather in Tokyo?")
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_called_with("get_weather", city="Tokyo")
        assert "Tokyo" in response
        
        # Reset observer state
        validation_observer.reset()
        
        # Test add_numbers tool
        response = agent.chat("What is 42 + 17?")
        validation_observer.assert_function_called("add_numbers")
        validation_observer.assert_function_called_with("add_numbers", a=42, b=17)
        assert "59" in response
        
        # Reset observer state
        validation_observer.reset()
        
        # Test search_database tool with limit parameter
        response = agent.chat("Search the database for 'climate change' and limit the results to 3.")
        validation_observer.assert_function_called("search_database")
        validation_observer.assert_function_called_with("search_database", query="climate change", limit=3)
        assert len(validation_observer.function_results[0]["result"]) == 3
    
    def test_class_methods_as_tools(self, validation_observer):
        """Test class methods as tools from examples.py."""
        # Create instance of ToolsForAgents
        tools_instance = ToolsForAgents(api_key="fake-api-key-12345")
        
        # Create agent with class methods as tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="ClassMethodsAgent",
            system_prompt="You are a helpful assistant that can perform math operations and check the weather.",
            tools=[
                tools_instance.add_numbers,
                tools_instance.multiply_numbers,
                tools_instance.get_weather
            ],
            observers=[validation_observer]
        )
        
        # Test multiply_numbers tool
        response = agent.chat("What is 7 times 8?")
        validation_observer.assert_function_called("multiply_numbers")
        validation_observer.assert_function_called_with("multiply_numbers", a=7, b=8)
        assert "56" in response
        
        # Verify that the counter was incremented
        assert tools_instance.get_call_count() > 0
        
        # Reset observer state
        validation_observer.reset()
        
        # Test weather with API key
        response = agent.chat("What's the weather in Berlin?")
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_called_with("get_weather", city="Berlin")
        assert "API key" in response or "Berlin" in response
    
    def test_decorated_class_methods(self, validation_observer):
        """Test decorated class methods from examples.py."""
        # Create instance of SimplifiedToolsForAgents
        tools_instance = SimplifiedToolsForAgents(api_key="fake-api-key-12345")
        
        # Create agent with decorated class methods
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="DecoratedMethodsAgent",
            system_prompt="You are a helpful assistant that can perform math operations.",
            tools=[
                tools_instance.add_numbers,
                tools_instance.multiply_numbers,
                calculate_area
            ],
            observers=[validation_observer]
        )
        
        # Test with a query that should use multiple tools
        response = agent.chat(
            "Can you add 25 and 18, then multiply the result by 3, and finally "
            "calculate the area of a rectangle with width 4 and height 7?"
        )
        
        # Verify that all tools were called
        validation_observer.assert_function_called("add_numbers")
        validation_observer.assert_function_called("multiply_numbers")
        validation_observer.assert_function_called("calculate_area")
        
        # Verify counter
        assert tools_instance.get_call_count() >= 2  # At least add and multiply were called
        
        # Check for specific results in the response
        assert "43" in response or "129" in response or "28" in response

    def test_multi_step_reasoning(self, validation_observer):
        """Test multi-step reasoning with function calls."""
        # Create agent with tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="ReasoningAgent",
            system_prompt="You are a helpful assistant that can solve complex problems.",
            tools=[add_numbers, calculate_area],
            observers=[validation_observer]
        )
        
        # Ask a multi-step question
        response = agent.chat(
            "I have a rectangle with width 5.5 meters and height 3.2 meters. "
            "If I add 2.3 meters to the width and 1.7 meters to the height, "
            "what will be the area of the new rectangle?"
        )
        
        # Verify that the agent used both tools
        # First to add the dimensions
        validation_observer.assert_function_called("add_numbers")
        # Then to calculate the area
        validation_observer.assert_function_called("calculate_area")
        
        # The correct answer should be (5.5+2.3)*(3.2+1.7) = 7.8*4.9 = 38.22
        assert "38.22" in response or "38.2" in response or "38" in response 