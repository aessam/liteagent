"""
Test the mock LLM implementation that can be used for testing the LiteAgent.

This module contains tests for the MockModelInterface class which allows
testing agent functionality without making actual LLM API calls.
"""

import json
import unittest
from typing import Any, Dict, List, Optional, Union
from unittest.mock import MagicMock, patch

# Import from the liteagent module
from liteagent.models import UnifiedModelInterface, create_model_interface
from liteagent.providers.base import ProviderResponse, ToolCall
from liteagent.capabilities import ModelCapabilities


class MockModelInterface(UnifiedModelInterface):
    """Mock implementation of ModelInterface for testing purposes."""
    
    def __init__(self, model_name: str = "mock-model", drop_params: bool = True,
                 supports_tools: bool = True, responses: List[Dict] = None):
        """
        Initialize the mock model interface.
        
        Args:
            model_name: Name of the model to mock
            drop_params: Whether to drop unsupported parameters
            supports_tools: Whether this mock model supports function calling
            responses: Predefined responses to return. If None, a default response is used.
        """
        super().__init__(model_name, drop_params)
        self.supports_tools = supports_tools
        self.responses = responses or []
        self.response_index = 0
        
        # For tracking calls
        self.generate_response_calls = []
    
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Any:
        """
        Generate a response from the model.
        
        Args:
            messages: List of conversation messages
            functions: Optional list of function definitions
            
        Returns:
            Dict containing the model's response
        """
        kwargs = {"model": self.model_name, "messages": messages}
        
        if functions:
            # For mock model, just pass functions directly
            kwargs["functions"] = functions
        
        # Record the call for later assertions
        self.generate_response_calls.append(kwargs)
        
        # Return the next predefined response if available
        if self.responses and self.response_index < len(self.responses):
            response = self.responses[self.response_index]
            self.response_index += 1
            return self._create_mock_response(response)
        
        # Default to a text response if no function calls are specified
        return self._create_mock_response({
            "type": "text",
            "content": "This is a mock response."
        })
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the mock response.
        
        Args:
            response: The mock model's response
            
        Returns:
            List of dictionaries with tool call details
        """
        if not hasattr(response, "choices") or not response.choices:
            return []
            
        message = response.choices[0].message
        
        # Check for OpenAI-style function calls
        if hasattr(message, "function_call") and message.function_call:
            function_call = message.function_call
            
            # Handle MagicMock objects
            if hasattr(function_call, "arguments"):
                if isinstance(function_call.arguments, str):
                    try:
                        function_args = json.loads(function_call.arguments)
                    except json.JSONDecodeError:
                        function_args = {}
                else:
                    # For MagicMock objects, just use an empty dict
                    function_args = {}
                    
            return [{
                "name": function_call.name,
                "arguments": function_args,
                "id": getattr(response, "id", "mock-response-id")
            }]
        
        # Check for OpenAI-style tool calls
        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_calls = []
            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    function_call = tool_call.function
                    
                    # Handle MagicMock objects
                    if hasattr(function_call, "arguments"):
                        if isinstance(function_call.arguments, str):
                            try:
                                arguments = json.loads(function_call.arguments)
                            except json.JSONDecodeError:
                                arguments = {}
                        else:
                            # For MagicMock objects, just use an empty dict
                            arguments = {}
                            
                    tool_calls.append({
                        "name": function_call.name,
                        "arguments": arguments,
                        "id": tool_call.id
                    })
            return tool_calls
            
        return []
    
    def extract_content(self, response: Any) -> str:
        """
        Extract text content from the mock response.
        
        Args:
            response: The mock model's response
            
        Returns:
            str: The text content
        """
        if not hasattr(response, "choices") or not response.choices:
            return ""
            
        message = response.choices[0].message
        
        if not hasattr(message, "content"):
            return ""
            
        # Return the exact content from the message
        return message.content if message.content is not None else ""
    
    def _create_mock_response(self, response_spec: Dict) -> Any:
        """
        Create a mock LiteLLM completion response object based on the response specification.
        
        Args:
            response_spec: Specification of the response to generate
            
        Returns:
            A mock response object similar to what LiteLLM would return
        """
        response_type = response_spec.get("type", "text")
        
        # Create a MagicMock to mimic the LiteLLM response
        mock_response = MagicMock()
        mock_response.id = response_spec.get("id", "mock-response-id")
        mock_response.choices = []
        
        mock_message = MagicMock()
        
        if response_type == "function_call":
            # Function call response
            function_name = response_spec.get("function_name", "test_function")
            function_args = response_spec.get("function_args", {})
            
            # Create function_call for OpenAI format
            mock_function_call = MagicMock()
            mock_function_call.name = function_name
            mock_function_call.arguments = json.dumps(function_args)
            mock_message.function_call = mock_function_call
            
            # Create tool_calls array for OpenAI format
            mock_function = MagicMock()
            mock_function.name = function_name
            mock_function.arguments = json.dumps(function_args)
            
            mock_tool_call = MagicMock()
            mock_tool_call.id = response_spec.get("id", "call_" + mock_response.id)
            mock_tool_call.type = "function"
            mock_tool_call.function = mock_function
            
            mock_message.tool_calls = [mock_tool_call]
            # Set content to None for function calls
            mock_message.content = None
        else:
            # Text response - use the exact content from the response_spec
            mock_message.content = response_spec.get("content", "This is a mock response.")
            mock_message.tool_calls = None
            mock_message.function_call = None
        
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices.append(mock_choice)
        
        return mock_response

    def _call_api(self, kwargs: Dict) -> Any:
        """
        Make the actual API call to the model provider.
        
        Args:
            kwargs: Dictionary of arguments for the API call
            
        Returns:
            The model's response
        """
        # For the mock, we just use the predefined responses
        if self.responses and self.response_index < len(self.responses):
            response = self.responses[self.response_index]
            self.response_index += 1
            return self._create_mock_response(response)
        
        # Default to a text response if no function calls are specified
        return self._create_mock_response({
            "type": "text",
            "content": "This is a mock response."
        })


class TestMockModelInterface(unittest.TestCase):
    """Test the MockModelInterface implementation."""
    
    def test_mock_model_text_response(self):
        """Test that the mock model correctly generates text responses."""
        mock_model = MockModelInterface(responses=[
            {"type": "text", "content": "Hello, I am a mock model!"}
        ])
        
        messages = [{"role": "user", "content": "Hello!"}]
        response = mock_model.generate_response(messages)
        
        content = mock_model.extract_content(response)
        self.assertEqual(content, "Hello, I am a mock model!")
        self.assertEqual(mock_model.extract_tool_calls(response), [])
    
    def test_mock_model_function_call(self):
        """Test that the mock model correctly generates function calls."""
        mock_model = MockModelInterface(responses=[
            {
                "type": "function_call",
                "function_name": "get_weather",
                "function_args": {"location": "New York", "unit": "celsius"}
            }
        ])
        
        messages = [{"role": "user", "content": "What's the weather in New York?"}]
        functions = [{"name": "get_weather", "parameters": {"location": "string", "unit": "string"}}]
        
        response = mock_model.generate_response(messages, functions)
        
        tool_calls = mock_model.extract_tool_calls(response)
        self.assertEqual(len(tool_calls), 1)
        self.assertEqual(tool_calls[0]["name"], "get_weather")
        self.assertEqual(tool_calls[0]["arguments"]["location"], "New York")
        self.assertEqual(tool_calls[0]["arguments"]["unit"], "celsius")
    
    def test_multiple_responses(self):
        """Test that the mock model correctly cycles through multiple responses."""
        mock_model = MockModelInterface(responses=[
            {"type": "text", "content": "First response"},
            {"type": "function_call", "function_name": "test_func", "function_args": {"arg1": 123}},
            {"type": "text", "content": "Third response"}
        ])
        
        messages = [{"role": "user", "content": "Test message"}]
        
        # First response
        response1 = mock_model.generate_response(messages)
        self.assertEqual(mock_model.extract_content(response1), "First response")
        
        # Second response
        response2 = mock_model.generate_response(messages)
        tool_calls = mock_model.extract_tool_calls(response2)
        self.assertEqual(len(tool_calls), 1)
        self.assertEqual(tool_calls[0]["name"], "test_func")
        self.assertEqual(tool_calls[0]["arguments"]["arg1"], 123)
        
        # Third response
        response3 = mock_model.generate_response(messages)
        self.assertEqual(mock_model.extract_content(response3), "Third response")
    
    def test_tracks_calls(self):
        """Test that the mock model correctly tracks calls for later assertions."""
        mock_model = MockModelInterface()
        
        messages1 = [{"role": "user", "content": "First message"}]
        functions1 = [{"name": "func1"}]
        
        messages2 = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
            {"role": "user", "content": "Second message"}
        ]
        
        mock_model.generate_response(messages1, functions1)
        mock_model.generate_response(messages2)
        
        self.assertEqual(len(mock_model.generate_response_calls), 2)
        self.assertEqual(mock_model.generate_response_calls[0]["messages"], messages1)
        self.assertEqual(mock_model.generate_response_calls[0]["functions"], functions1)
        self.assertEqual(mock_model.generate_response_calls[1]["messages"], messages2)


if __name__ == "__main__":
    unittest.main() 