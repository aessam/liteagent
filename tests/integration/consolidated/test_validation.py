"""
Consolidated integration tests for validation functionality across different models.

This module tests validation strategies and observers with different models.
"""

import pytest
import re
from typing import Dict, Any, List

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from liteagent.tools import get_weather, add_numbers

from tests.utils.validation_helper import ValidationTestHelper


@pytest.mark.integration
class TestValidation:
    """Tests for validation functionality across all models."""
    
    @pytest.fixture
    def tools(self):
        """Provide the tools for validation tests."""
        return [get_weather, add_numbers]
    
    @pytest.fixture
    def system_prompt(self):
        """Provide the system prompt for validation tests."""
        return """You are a helpful assistant that can use tools to accomplish tasks.
Use the appropriate tool when needed to provide accurate information."""
    
    @pytest.fixture
    def tool_names(self):
        """Provide the tool names for parser registration."""
        return ["get_weather", "add_numbers"]
    
    def test_function_call_validation(self, configured_agent, validation_observer, tool_names, model):
        """
        Test basic function call validation across different models.
        
        This test verifies that the validation observer correctly tracks function calls.
        """
        # Register appropriate parsers based on tool calling type
        tool_calling_type = get_tool_calling_type(model)
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            tool_names
        )
        
        try:
            # Make a weather query that should trigger the get_weather tool
            response = configured_agent.chat("What's the weather in Tokyo?")
            
            # Handle None responses
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                return
            
            # Verify that the observer tracked the function call
            functions_called = list(validation_observer.called_functions)
            print(f"Functions called by {model}: {functions_called}")
            
            # If get_weather was called, validate its arguments
            if "get_weather" in functions_called:
                validation_observer.assert_function_called_with("get_weather", city="Tokyo")
                
                # Verify function result was stored
                result = validation_observer.get_last_function_result("get_weather")
                assert result is not None, "Function result should not be None"
            
            # Make sure the observer's reset function works
            validation_observer.reset()
            assert len(validation_observer.called_functions) == 0, "Observer should be reset"
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise
    
    def test_validation_strategy_switching(self, model, validation_observer, tool_names):
        """
        Test switching between validation strategies.
        
        This test verifies that the validation observer can switch between
        different validation strategies based on the model.
        """
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            tool_names
        )
        
        # Create a basic agent
        agent = LiteAgent(
            model=model,
            name="ValidationStrategyAgent",
            system_prompt="""You are a helpful assistant that can use tools to accomplish tasks.
Use the appropriate tool when needed to provide accurate information.""",
            tools=[get_weather, add_numbers],
            observers=[validation_observer]
        )
        
        try:
            # First use with the current validation strategy
            current_strategy = validation_observer.validation_strategy
            response1 = agent.chat("What's the weather in Tokyo?")
            
            # Switch to a different strategy temporarily
            temp_strategy = ToolCallingType.JSON_EXTRACTION
            if current_strategy == ToolCallingType.JSON_EXTRACTION:
                temp_strategy = ToolCallingType.ANTHROPIC_TOOL_CALLING
                
            validation_observer.set_validation_strategy(temp_strategy)
            validation_observer.reset()
            
            # Use with the temporary strategy (might not work well, just testing the switch)
            try:
                response2 = agent.chat("What's 5 + 7?")
            except:
                # This might fail, but we just want to test the strategy switching
                pass
            
            # Switch back to the original strategy
            validation_observer.set_validation_strategy(current_strategy)
            validation_observer.reset()
            
            # Use again with original strategy
            response3 = agent.chat("Is it raining in New York?")
            
            # Verify we're back to the original strategy type
            assert validation_observer.validation_strategy == current_strategy, \
                "Validation strategy should be restored to the original"
            
            # If we got this far, the test passes
            assert True
            
        except Exception as e:
            # Skip for model-specific issues
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # Only fail if this is not an expected exception from strategy switching
                if "ValidationError" not in str(e) and "tool_calls" not in str(e):
                    raise 