"""
Integration tests for class method tools across different models.

This module tests class method tools with different models and tool calling types.
"""

import pytest
import os
from typing import Dict, Any

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from liteagent.tools import ToolsForAgents
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
class TestClassMethodTools:
    """Test class method tools across different models and tool calling types."""
    
    # Test models - one from each major provider
    TEST_MODELS = [
        "gpt-4o-mini",  # OpenAI
        "anthropic/claude-3-haiku-20240307",  # Anthropic
        "groq/llama-3.1-8b-instant",  # Groq
    ]
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_add_numbers_class_method(self, model, validation_observer):
        """Test add_numbers class method with different models."""
        # Skip if API key not available
        if not ValidationTestHelper.has_api_key_for_model(model):
            pytest.skip(f"API key for {model} not available")
        
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Create tools class instance
        tools_instance = ToolsForAgents()
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["add_numbers"]
        )
        
        # Create agent with the add_numbers class method tool
        agent = LiteAgent(
            model=model,
            name="AddNumbersClassMethodAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["add_numbers"]),
            tools=[tools_instance.add_numbers],
            observers=[validation_observer]
        )
        
        # Test the tool
        response = agent.chat("What is 7 plus 9?")
        
        # Use validation helper to validate add_numbers tool usage
        ValidationTestHelper.validate_number_tool_usage(
            validation_observer, 
            response, 
            "add_numbers", 
            {"a": 7, "b": 9}, 
            16, 
            tool_calling_type
        )
        
        # Verify internal counter of tools class was incremented
        assert tools_instance.get_call_count() >= 1, "Tool call count should be at least 1"
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_multiply_numbers_class_method(self, model, validation_observer):
        """Test multiply_numbers class method with different models."""
        # Skip if API key not available
        if not ValidationTestHelper.has_api_key_for_model(model):
            pytest.skip(f"API key for {model} not available")
        
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Create tools class instance
        tools_instance = ToolsForAgents()
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["multiply_numbers"]
        )
        
        # Create agent with the multiply_numbers class method tool
        agent = LiteAgent(
            model=model,
            name="MultiplyNumbersClassMethodAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["multiply_numbers"]),
            tools=[tools_instance.multiply_numbers],
            observers=[validation_observer]
        )
        
        # Test the tool
        response = agent.chat("What is 7 times 9?")
        
        # Use validation helper to validate multiply_numbers tool usage
        ValidationTestHelper.validate_number_tool_usage(
            validation_observer, 
            response, 
            "multiply_numbers", 
            {"a": 7, "b": 9}, 
            63, 
            tool_calling_type
        )
        
        # Verify internal counter of tools class was incremented
        assert tools_instance.get_call_count() >= 1, "Tool call count should be at least 1"
    
    @pytest.mark.parametrize("model", TEST_MODELS)
    def test_multiple_class_method_tools(self, model, validation_observer):
        """Test multiple class method tools with different models."""
        # Skip if API key not available
        if not ValidationTestHelper.has_api_key_for_model(model):
            pytest.skip(f"API key for {model} not available")
        
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Create tools class instance
        tools_instance = ToolsForAgents()
        
        # Register appropriate parsers based on tool calling type
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["add_numbers", "multiply_numbers"]
        )
        
        # Create agent with multiple class method tools
        agent = LiteAgent(
            model=model,
            name="MultipleClassMethodToolsAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["add_numbers", "multiply_numbers"]),
            tools=[
                tools_instance.add_numbers,
                tools_instance.multiply_numbers
            ],
            observers=[validation_observer]
        )
        
        # Test the add_numbers tool
        response = agent.chat("What is 7 plus 9?")
        
        # Use validation helper to validate add_numbers tool usage
        ValidationTestHelper.validate_number_tool_usage(
            validation_observer, 
            response, 
            "add_numbers", 
            {"a": 7, "b": 9}, 
            16, 
            tool_calling_type
        )
        
        # Verify internal counter of tools class was incremented
        assert tools_instance.get_call_count() >= 1, "Tool call count should be at least 1"
        
        # Reset the observer
        validation_observer.reset()
        
        # Test the multiply_numbers tool
        response = agent.chat("What is 7 times 9?")
        
        # Use validation helper to validate multiply_numbers tool usage
        ValidationTestHelper.validate_number_tool_usage(
            validation_observer, 
            response, 
            "multiply_numbers", 
            {"a": 7, "b": 9}, 
            63, 
            tool_calling_type
        )
        
        # Verify internal counter of tools class increased further
        assert tools_instance.get_call_count() >= 2, "Tool call count should be at least 2" 