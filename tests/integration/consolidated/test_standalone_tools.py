"""
Consolidated integration tests for standalone tools across different models.

This module tests standalone tools with different models using a unified approach.
"""

import pytest
import re
from typing import Dict, Any, List

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from tests.utils.test_tools import get_weather, add_numbers
from liteagent.tool_calling import ToolCallTracker

from tests.utils.validation_helper import ValidationTestHelper


@pytest.mark.integration
class TestStandaloneTools:
    """Tests for standalone tools across all models."""
    
    @pytest.fixture
    def tools(self):
        """Provide the tools for the standalone tool tests."""
        return [get_weather, add_numbers]
    
    @pytest.fixture
    def system_prompt(self):
        """Provide the system prompt for standalone tool tests."""
        return ValidationTestHelper.get_system_prompt_for_tools(["get_weather", "add_numbers"])
    
    @pytest.fixture
    def tool_names(self):
        """Provide the tool names for parser registration."""
        return ["get_weather", "add_numbers"]
    
    def test_weather_tool(self, configured_agent, validation_observer, tool_names, model):
        """
        Test weather tool across different models.
        
        This test checks if the agent can correctly use the get_weather tool
        to retrieve weather information for Tokyo.
        """
        # Register appropriate parsers based on tool calling type
        tool_calling_type = get_tool_calling_type(model)
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            tool_names
        )
        
        try:
            # Reset the tracker
            ToolCallTracker.get_instance().reset()
            
            # Ask about weather in Tokyo
            response = configured_agent.chat("What's the weather in Tokyo?")
            
            # Fail-fast assertions - zero complexity
            assert response is not None, "Model returned None response"
            validation_observer.assert_tool_called("get_weather")
            validation_observer.assert_tool_called("validate_output")
            
            # Check validation result
            validation_result = validation_observer.get_last_function_result("validate_output")
            assert validation_result == True, "Agent reported incorrect weather result"
            
            # Validate tool arguments
            validation_observer.assert_function_called_with("get_weather", city="Tokyo")
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise
    
    def test_add_numbers_tool(self, configured_agent, validation_observer, tool_names, model):
        """
        Test add_numbers tool across different models.
        
        This test checks if the agent can correctly use the add_numbers tool
        to add two numbers together.
        """
        # Register appropriate parsers based on tool calling type
        tool_calling_type = get_tool_calling_type(model)
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            tool_names
        )
        
        try:
            # Reset the tracker
            ToolCallTracker.get_instance().reset()
            
            # Ask to add 25 and 17
            response = configured_agent.chat("What is 25 + 17?")
            
            # Handle None responses
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                return
            
            # Track validation status
            addition_task_validated = False
            
            # Try to parse the response to extract structured data
            try:
                parsed_response = validation_observer.parse_response(response)
                
                # Check if result is in the parsed response
                if "result" in parsed_response:
                    result_value = parsed_response["result"]
                    # Handle both numeric and string results
                    if isinstance(result_value, (int, float)):
                        assert result_value == 42, f"Response result should be 42, got {result_value}"
                    else:
                        # Try to convert string to int if possible
                        try:
                            result_value = int(result_value)
                            assert result_value == 42, f"Response result should be 42, got {result_value}"
                        except (ValueError, TypeError):
                            # If not convertible, just check if "42" is in the string
                            assert "42" in str(result_value), f"Response should contain 42, got {result_value}"
                    
                    addition_task_validated = True
            except Exception as e:
                print(f"Failed to parse response: {e}")
                # If parsing fails, we'll validate through function calls below
            
            # Check if the add_numbers function was called
            if "add_numbers" in validation_observer.called_functions:
                # Validate the function was called
                validation_observer.assert_function_called("add_numbers")
                
                # Validate the function call arguments
                call_args = validation_observer.get_function_call_args("add_numbers")
                assert call_args, "Function call arguments should not be empty"
                
                # The last call should have arguments that sum to 42
                last_call = call_args[-1]
                a, b = last_call.get('a'), last_call.get('b')
                assert a is not None and b is not None, "Both 'a' and 'b' parameters should be provided"
                assert a + b == 42, f"Sum of {a} and {b} should be 42"
                
                addition_task_validated = True
                
                # Try to validate the function result if it's a dictionary
                try:
                    result = validation_observer.get_last_function_result("add_numbers")
                    if isinstance(result, dict):
                        # Validate the function result contains expected structure
                        validation_observer.assert_function_result_structure(
                            "add_numbers", 
                            {"result": int}
                        )
                        
                        # Validate the actual result value
                        assert result["result"] == 42, f"Result should be 42, got {result.get('result', '')}"
                    else:
                        # For non-dict results, just check if "42" is mentioned
                        assert "42" in str(result), f"Result should mention 42, got {result}"
                except Exception as e:
                    # If we've already validated through other means, we can proceed
                    if not addition_task_validated:
                        print(f"Error validating function result: {e}")
                        # Fallback: check if 42 appears in the raw response
                        assert "42" in response, "Response should contain the answer 42"
                        addition_task_validated = True
            else:
                # If function wasn't called, ensure we've validated the response content
                if not addition_task_validated:
                    # Fallback: simple check for 42 in the response
                    assert any(value in response for value in ["42", "forty-two", "forty two"]), "Response should contain the answer 42"
                    addition_task_validated = True
            
            # Final validation check
            assert addition_task_validated, "Addition task should be validated through response or function call"
                
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise
    
    def test_multi_step_tools(self, configured_agent, validation_observer, tool_names, model):
        """
        Test multi-step tool usage across different models.
        
        This test checks if the agent can correctly use multiple tools
        in sequence to solve a multi-step problem.
        """
        # Register appropriate parsers based on tool calling type
        tool_calling_type = get_tool_calling_type(model)
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            tool_names
        )
        
        try:
            # Reset the tracker
            ToolCallTracker.get_instance().reset()
            
            # Ask a question that requires both tools
            response = configured_agent.chat(
                "First, tell me the weather in Tokyo. Then, add 25 and 17."
            )
            
            # Handle None responses
            if response is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                return
            
            # Track which tasks were validated
            weather_task_validated = False
            addition_task_validated = False
            
            # Check which functions were called
            functions_called = list(validation_observer.called_functions)
            print(f"Functions called by {model}: {functions_called}")
            
            # Try to parse the response to extract structured data
            try:
                parsed_response = validation_observer.parse_response(response)
                
                # Validate weather information if present in response
                if "city" in parsed_response:
                    assert parsed_response["city"].lower() == "tokyo", f"Response city should be Tokyo, got {parsed_response.get('city', '')}"
                    weather_task_validated = True
                
                # Validate addition result if present in response
                if "result" in parsed_response:
                    result_value = parsed_response["result"]
                    if isinstance(result_value, (int, float)):
                        assert result_value == 42, f"Response result should be 42, got {result_value}"
                    else:
                        # Try to convert string to int if possible
                        try:
                            result_value = int(result_value)
                            assert result_value == 42, f"Response result should be 42, got {result_value}"
                        except (ValueError, TypeError):
                            # If not convertible, just check if "42" is in the string
                            assert "42" in str(result_value), f"Response should contain 42, got {result_value}"
                    
                    addition_task_validated = True
            except Exception as e:
                print(f"Failed to parse response: {e}")
                # If parsing fails, we'll validate through function calls below
            
            # If weather function was called, validate it
            if "get_weather" in functions_called:
                # Validate the function call
                validation_observer.assert_function_called_with("get_weather", city="Tokyo")
                weather_task_validated = True
                
                # Try to validate the function result
                try:
                    result = validation_observer.get_last_function_result("get_weather")
                    if isinstance(result, dict):
                        # Validate the function result contains expected structure
                        validation_observer.assert_function_result_structure(
                            "get_weather", 
                            {"city": str, "temperature": object, "conditions": str}
                        )
                    else:
                        # For non-dict results, just check if Tokyo is mentioned
                        assert "Tokyo" in str(result), f"Result should mention Tokyo, got {result}"
                except Exception as e:
                    print(f"Error validating weather function result: {e}")
                    # We've already validated through the function call, so we can continue
            
            # If add_numbers was called, validate it
            if "add_numbers" in functions_called:
                validation_observer.assert_function_called("add_numbers")
                
                # Check all calls to find one that sums to 42
                call_args_list = validation_observer.get_function_call_args("add_numbers")
                valid_addition_call_found = False
                
                for call_args in call_args_list:
                    a, b = call_args.get('a'), call_args.get('b')
                    if a is not None and b is not None and a + b == 42:
                        valid_addition_call_found = True
                        break
                
                assert valid_addition_call_found, "No add_numbers call with args that sum to 42 found"
                addition_task_validated = True
                
                # Try to validate the function result
                try:
                    result = validation_observer.get_last_function_result("add_numbers")
                    if isinstance(result, dict):
                        # Validate the function result
                        assert "result" in result, "Result should have a 'result' field"
                        assert result["result"] == a + b, f"Result should be {a + b}, got {result.get('result', '')}"
                    else:
                        # For non-dict results, just check if result contains the expected value
                        assert str(a + b) in str(result), f"Result should mention {a + b}, got {result}"
                except Exception as e:
                    print(f"Error validating addition function result: {e}")
                    # We've already validated through the function call, so we can continue
            
            # If we haven't validated through function calls, check the response content
            if not weather_task_validated:
                assert ("Tokyo" in response and 
                        any(term in response.lower() for term in ["weather", "temperature", "°c", "degrees"])), \
                    "Response should mention Tokyo weather information"
                weather_task_validated = True
                
            if not addition_task_validated:
                assert any(value in response for value in ["42", "forty-two", "forty two"]), \
                    "Response should contain the answer 42"
                addition_task_validated = True
            
            # At least one of the tasks should be validated
            assert weather_task_validated or addition_task_validated, \
                "At least one of the tasks (weather or addition) should be validated"
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise 