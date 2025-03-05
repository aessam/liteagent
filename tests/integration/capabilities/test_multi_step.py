"""
Integration tests for multi-step reasoning across different models.

This module tests multi-step reasoning with different models and tool calling types.
"""

import pytest
import os
from typing import Dict, Any

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from liteagent.tools import get_weather, add_numbers, calculate_area
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
class TestMultiStepReasoning:
    """Test multi-step reasoning across different models and tool calling types."""
    
    # Test models - one from each major provider
    TEST_MODELS = [
        "gpt-4o-mini",  # OpenAI
        "anthropic/claude-3-haiku-20240307",  # Anthropic
        "groq/llama-3.1-8b-instant",  # Groq
    ]
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_weather_and_addition(self, model, validation_observer):
        """Test multi-step reasoning with weather and addition tools."""
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
            name="MultiStepAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["get_weather", "add_numbers"]),
            tools=[get_weather, add_numbers],
            observers=[validation_observer]
        )
        
        # Test multi-step reasoning
        response = agent.chat("What's the weather like in Tokyo and what is 25 plus 17?")
        
        # Validate function calls - should call get_weather at minimum
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_called_with("get_weather", city="Tokyo")
        
        # Check weather function result
        weather_result = validation_observer.get_last_function_result("get_weather")
        assert weather_result is not None, "Weather function result should not be None"
        assert "Tokyo" in weather_result, "Result should mention Tokyo"
        
        # If add_numbers was also called, validate its result
        if "add_numbers" in validation_observer.called_functions:
            validation_observer.assert_function_called_with("add_numbers", a=25, b=17)
            add_result = validation_observer.get_last_function_result("add_numbers")
            assert add_result == 42, f"Expected add_numbers result to be 42, got {add_result}"
        
        # Validate response contains relevant information
        assert "Tokyo" in response, "Response should mention Tokyo"
        
        # If add_numbers was called or the model included the calculation in its response,
        # verify the result is mentioned
        if "add_numbers" in validation_observer.called_functions or "42" in response:
            parsed_response = validation_observer.parse_response(response, "add_numbers")
            if "result" in parsed_response:
                assert parsed_response["result"] == 42, f"Expected result 42, got {parsed_response['result']}"
            else:
                # Check for presence of calculation result in response
                assert any(num in response for num in ["42", "forty-two", "forty two"]) or \
                       ("25" in response and "17" in response), "Response should mention calculation result"
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_area_calculation(self, model, validation_observer):
        """Test multi-step reasoning with area calculation."""
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
            ["calculate_area", "add_numbers"]
        )
        
        # Create agent with multiple tools
        agent = LiteAgent(
            model=model,
            name="AreaCalculationAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["calculate_area", "add_numbers"]),
            tools=[calculate_area, add_numbers],
            observers=[validation_observer]
        )
        
        # Test multi-step reasoning with area calculation
        response = agent.chat("What's the area of a rectangle with width 6 and height 4, and what's the sum of the width and height?")
        
        # Validate function calls - should call calculate_area at minimum
        validation_observer.assert_function_called("calculate_area")
        validation_observer.assert_function_called_with("calculate_area", width=6, height=4)
        
        # Check area calculation result
        area_result = validation_observer.get_last_function_result("calculate_area")
        assert area_result == 24, f"Expected area result to be 24, got {area_result}"
        
        # If add_numbers was also called, validate its result
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
                assert add_result == 10, f"Expected add_numbers result to be 10, got {add_result}"
        
        # Validate response contains relevant information
        assert "24" in response or "twenty-four" in response.lower() or "twenty four" in response.lower(), \
            "Response should mention area result (24)"
        
        # Check if the sum is mentioned
        assert "10" in response or "ten" in response.lower(), \
            "Response should mention sum result (10)" 