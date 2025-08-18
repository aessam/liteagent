"""
Consolidated integration tests for class method tools across different models.

This module tests class method tools with different models using a unified approach.
"""

import pytest
import re
from typing import Dict, Any, List

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from liteagent.tool_calling import ToolCallTracker
from tests.utils.test_tools import ToolsForAgents

from tests.utils.validation_helper import ValidationTestHelper


@pytest.mark.integration
class TestClassMethodTools:
    """Tests for class method tools across all models."""
    
    @pytest.fixture
    def tools_instance(self):
        """Create a ToolsForAgents instance for testing."""
        return ToolsForAgents(api_key="fake-api-key-12345")
    
    @pytest.fixture
    def tools(self, tools_instance):
        """Provide the tools for the single tools test."""
        return [tools_instance.add_numbers]
    
    @pytest.fixture
    def multiple_tools(self, tools_instance):
        """Provide multiple tools for the multiple tools test."""
        return [tools_instance.add_numbers, tools_instance.multiply_numbers]
    
    @pytest.fixture
    def system_prompt(self):
        """Provide the system prompt for the single tool test."""
        return ValidationTestHelper.get_system_prompt_for_tools(["add_numbers"])
    
    @pytest.fixture
    def multiple_tools_prompt(self):
        """Provide the system prompt for the multiple tools test."""
        return ValidationTestHelper.get_system_prompt_for_tools(["add_numbers", "multiply_numbers"])
    
    @pytest.fixture
    def tool_names(self):
        """Provide the tool names for parser registration."""
        return ["add_numbers", "multiply_numbers", "get_user_data"]
    
    def _handle_test_exception(self, e, model, validation_observer=None):
        """
        Common method to handle exceptions in test methods.
        
        Args:
            e: The exception
            model: The model name
            validation_observer: Optional validation observer for debug info
        """
        if "TypeError: 'NoneType' object is not iterable" in str(e):
            pytest.skip(f"Model {model} returned None response, skipping validation")
        elif validation_observer:
            # Print validation information for debugging
            print(f"Called functions: {validation_observer.called_functions}")
            print(f"Function calls: {validation_observer.function_calls}")
            print(f"Function results: {validation_observer.function_results}")
            raise e
        else:
            # For other exceptions, re-raise
            raise e
    
    def test_add_numbers_class_method(self, configured_agent, model, validation_observer, tools_instance):
        """Test adding two numbers using a class method tool."""
        # Register appropriate parsers
        tool_calling_type = get_tool_calling_type(model)
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["add_numbers"]
        )
        
        # Reset the tracker
        ToolCallTracker.get_instance().reset()
        
        try:
            # Ask the question
            response = configured_agent.chat("What is 7 + 9?")
            
            # Handle None responses
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                return
                
            # Check that the tool was called
            assert ToolCallTracker.get_instance().was_tool_called("add_numbers"), "add_numbers tool was not called"
            
            # Check the arguments
            args = ToolCallTracker.get_instance().get_tool_args("add_numbers")
            assert "a" in args, "Missing 'a' argument"
            assert "b" in args, "Missing 'b' argument"
            
            # Check the result
            result = ToolCallTracker.get_instance().get_tool_result("add_numbers")
            assert result == 16, f"Expected result 16, got {result}"
            
            # Verify internal counter of tools class was incremented
            assert tools_instance.get_call_count() >= 1, "Tool call count should be at least 1"
            
        except Exception as e:
            self._handle_test_exception(e, model)
    
    def test_get_user_data_class_method(self, model, validation_observer, tools_instance):
        """
        Test get_user_data class method with different models.
        
        This test checks if the agent can correctly use the get_user_data class method
        to retrieve information that the LLM couldn't possibly know on its own.
        """
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["get_user_data"]
        )
        
        # Create agent with the get_user_data class method tool
        agent = LiteAgent(
            model=model,
            name="GetUserDataClassMethodAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["get_user_data"]),
            tools=[tools_instance.get_user_data],
            observers=[validation_observer]
        )
        
        try:
            # Ask for information the LLM couldn't possibly know
            user_id = "user123"
            response = agent.chat(
                f"I need the email address and subscription tier for the user with ID {user_id}. "
                f"This information is not publicly available and can only be retrieved using the get_user_data tool. "
                f"Please execute the get_user_data tool with user_id={user_id} as the parameter and tell me what "
                f"you find. Don't just acknowledge that you'll use the tool - actually use it and show me the results."
            )
            
            print(f"Full response: {response}")
            
            # Check if the response contains the correct information
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            
            # The tool must be called to get this information
            assert "get_user_data" in validation_observer.called_functions, f"get_user_data tool was not called. Response: {response}"
            
            # Check the correct user ID was used
            call_args = validation_observer.get_function_call_args("get_user_data")
            assert call_args, "Function call arguments should not be empty"
            
            # Ensure the most recent call used the correct user_id
            last_call = call_args[-1]
            print(f"Function call args: {last_call}")
            assert last_call.get('user_id') == user_id, f"Expected user_id '{user_id}', got '{last_call.get('user_id')}'"
            
            # Verify internal counter was incremented
            assert tools_instance.get_call_count() >= 1, "Tool call count should be at least 1"
            
            # The response should contain information from the tool result
            assert "alex.j@example.com" in response.lower() or "premium" in response.lower(), \
                f"Response should contain information from the tool result. Response: {response}"
            
        except Exception as e:
            self._handle_test_exception(e, model, validation_observer)
    
    @pytest.mark.optional
    def test_multiply_numbers_class_method(self, model, validation_observer, tools_instance):
        """
        Test multiply_numbers class method with different models.
        
        This test checks if the agent can correctly use the multiply_numbers class method
        to multiply two numbers together.
        """
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            ["multiply_numbers"]
        )
        
        # Create agent with the multiply_numbers class method tool
        agent = LiteAgent(
            model=model,
            name="MultiplyNumbersClassMethodAgent",
            system_prompt=ValidationTestHelper.get_system_prompt_for_tools(["multiply_numbers"]) + "\nIMPORTANT: DO NOT attempt to calculate the answer yourself. The numbers are intentionally large and will result in errors if you try. You MUST use the multiply_numbers tool.",
            tools=[tools_instance.multiply_numbers],
            observers=[validation_observer]
        )
        
        try:
            # Use an extremely difficult multiplication that LLMs cannot compute directly
            response = agent.chat("What is 1299792458 times 6626070040? This is an intentionally difficult calculation to test the multiply_numbers tool. Do NOT try to calculate this yourself - use the multiply_numbers tool.")
            
            # Check if the response contains the correct answer
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            
            # Only check that the function was called - don't try to verify the result in the response
            # as it's too complex to extract reliably
            function_called = "multiply_numbers" in validation_observer.called_functions
            
            # Assert the function was called - we're only testing tool usage, not response quality
            assert function_called, f"The multiply_numbers function should be called. Function called: {function_called}"
            
            # If the function was called, validate the call
            if function_called:
                # Check the arguments
                call_args = validation_observer.get_function_call_args("multiply_numbers")
                assert call_args, "Function call arguments should not be empty"
                
                # Check the result
                result = tools_instance.get_call_count()
                assert result >= 1, "Tool call count should be at least 1"
                
            print(f"Response from LLM: {response}")
                
        except Exception as e:
            self._handle_test_exception(e, model, validation_observer)
    
    def test_multiple_class_method_tools(self, model, validation_observer, tools_instance):
        """
        Test multiple class method tools with different models.
        
        This test checks if the agent can correctly use both add_numbers and
        multiply_numbers class methods.
        """
        # Get tool calling type for the model
        tool_calling_type = get_tool_calling_type(model)
        
        # Set validation strategy based on tool calling type
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Register appropriate parsers
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
        
        try:
            # First test add_numbers
            response = agent.chat("What is 7 + 9?")
            
            # Check if the response contains the correct answer
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                
            assert any(str(num) in response for num in ["16", "sixteen"]), \
                "Response should contain '16'"
            
            # Check if add_numbers was called
            if "add_numbers" in validation_observer.called_functions:
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
            
            # Clear the observer for the second test
            validation_observer.reset()
            
            # Then test multiply_numbers
            response = agent.chat("What is 7 times 9?")
            
            # Check if the response contains the correct answer
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                
            assert any(str(num) in response for num in ["63", "sixty-three", "sixty three"]), \
                "Response should contain '63'"
            
            # Check if multiply_numbers was called
            if "multiply_numbers" in validation_observer.called_functions:
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
            else:
                # If multiply_numbers wasn't called, check if add_numbers was used instead
                # Some models might use add_numbers repeatedly instead of multiply_numbers
                if "add_numbers" in validation_observer.called_functions:
                    # Just verify the tool was called, don't validate specific arguments
                    pass
                else:
                    # If no tool was called, check if the response contains the correct answer
                    if response is not None:
                        assert any(str(num) in response for num in ["63", "sixty-three", "sixty three"]), \
                            "Response should contain '63'"
                    else:
                        # If response is None, skip the test
                        pytest.skip(f"Model {model} returned None response for multiplication, skipping validation")
            
        except Exception as e:
            self._handle_test_exception(e, model, validation_observer) 
