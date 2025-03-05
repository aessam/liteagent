"""
Integration tests for standalone tools across different models.

This module tests standalone function tools with different models and tool calling types.
"""

import pytest
import os
from typing import Dict, Any

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from liteagent.tools import get_weather, add_numbers
from tests.integration.validation_observer import ValidationObserver
from tests.utils.validation_helper import ValidationTestHelper

# Skip tests if API key is not set
def skip_if_no_api_key(model_name):
    """Skip test if API key is not set for the model."""
    return pytest.mark.skipif(
        not ValidationTestHelper.has_api_key_for_model(model_name),
        reason=f"API key for {model_name} not found in environment variables"
    )

@pytest.mark.integration
class TestStandaloneTools:
    """Test standalone function tools across different models and tool calling types."""
    
    # Test models - one from each major provider
    TEST_MODELS = [
        "gpt-4o-mini",  # OpenAI
        "anthropic/claude-3-haiku-20240307",  # Anthropic
        "groq/llama-3.1-8b-instant",  # Groq
    ]
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_weather_tool(self, model, validation_observer):
        """Test weather tool with different models."""
        # Skip if API key not available
        if not ValidationTestHelper.has_api_key_for_model(model):
            pytest.skip(f"API key for {model} not available")
        
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["get_weather"]
        )
        
        # Create agent with the weather tool
        agent = LiteAgent(
            model=model,
            name="WeatherAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["get_weather"]),
            tools=[get_weather],
            observers=[validation_observer]
        )
        
        # Test the tool
        response = agent.chat("What's the weather like in Tokyo?")
        
        # Use validation helper to validate weather tool usage
        ValidationTestHelper.validate_weather_tool_usage(
            validation_observer, 
            response, 
            "Tokyo", 
            tool_calling_type
        )
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_add_numbers_tool(self, model, validation_observer):
        """Test add_numbers tool with different models."""
        # Skip if API key not available
        if not ValidationTestHelper.has_api_key_for_model(model):
            pytest.skip(f"API key for {model} not available")
        
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["add_numbers"]
        )
        
        # Create agent with the add_numbers tool
        agent = LiteAgent(
            model=model,
            name="AddNumbersAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["add_numbers"]),
            tools=[add_numbers],
            observers=[validation_observer]
        )
        
        # Test the tool
        response = agent.chat("What is 25 plus 17?")
        
        # Use validation helper to validate add_numbers tool usage
        ValidationTestHelper.validate_number_tool_usage(
            validation_observer, 
            response, 
            "add_numbers", 
            {"a": 25, "b": 17}, 
            42, 
            tool_calling_type
        )
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_multiple_standalone_tools(self, model, validation_observer):
        """Test multiple standalone tools with different models."""
        # Skip if API key not available
        if not ValidationTestHelper.has_api_key_for_model(model):
            pytest.skip(f"API key for {model} not available")
        
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["get_weather", "add_numbers"]
        )
        
        # Create agent with multiple tools
        agent = LiteAgent(
            model=model,
            name="MultiToolAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["get_weather", "add_numbers"]),
            tools=[get_weather, add_numbers],
            observers=[validation_observer]
        )
        
        # Test the weather tool
        response = agent.chat("What's the weather like in Tokyo?")
        
        # Use validation helper to validate weather tool usage
        ValidationTestHelper.validate_weather_tool_usage(
            validation_observer, 
            response, 
            "Tokyo", 
            tool_calling_type
        )
        
        # Reset the observer
        validation_observer.reset()
        
        # Test the add_numbers tool
        response = agent.chat("What is 25 plus 17?")
        
        # Use validation helper to validate add_numbers tool usage
        ValidationTestHelper.validate_number_tool_usage(
            validation_observer, 
            response, 
            "add_numbers", 
            {"a": 25, "b": 17}, 
            42, 
            tool_calling_type
        ) 