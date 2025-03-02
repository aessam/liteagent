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
from liteagent.models import ModelInterface, create_model_interface


class MockModelInterface(ModelInterface):
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
    
    def supports_function_calling(self) -> bool:
        """
        Check if this model supports native function calling.
        
        Returns:
            bool: Whether the model supports function calling
        """
        return self.supports_tools
    
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Dict:
        """
        Generate a mock response.
        
        Args:
            messages: List of conversation messages
            functions: Optional list of function definitions
            
        Returns:
            Dict containing the mocked model's response
        """
        # Record the call for later assertions
        self.generate_response_calls.append({
            "messages": messages,
            "functions": functions
        })
        
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
    
    def extract_function_call(self, response: Any) -> Optional[Dict]:
        """
        Extract function call information from the mock response.
        
        Args:
            response: The mock model's response
            
        Returns:
            Dict with function call details or None if no function call
        """
        if not hasattr(response, "choices") or not response.choices:
            return None
            
        message = response.choices[0].message
        
        if not hasattr(message, "function_call") or not message.function_call:
            return None
            
        function_call = message.function_call
        
        try:
            function_args = json.loads(function_call.arguments)
        except (json.JSONDecodeError, AttributeError):
            function_args = {}
            
        return {
            "name": function_call.name,
            "arguments": function_args,
            "model_id": getattr(response, "id", "mock-response-id")
        }
    
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
            
        return message.content or ""
    
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
            
            mock_function_call = MagicMock()
            mock_function_call.name = function_name
            mock_function_call.arguments = json.dumps(function_args)
            
            mock_message.function_call = mock_function_call
            mock_message.content = None
        else:
            # Text response
            mock_message.content = response_spec.get("content", "Mock response content")
            mock_message.function_call = None
        
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices.append(mock_choice)
        
        return mock_response


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
        self.assertIsNone(mock_model.extract_function_call(response))
    
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
        
        function_call = mock_model.extract_function_call(response)
        self.assertIsNotNone(function_call)
        self.assertEqual(function_call["name"], "get_weather")
        self.assertEqual(function_call["arguments"]["location"], "New York")
        self.assertEqual(function_call["arguments"]["unit"], "celsius")
    
    def test_supports_function_calling(self):
        """Test the supports_function_calling method."""
        mock_model_with_tools = MockModelInterface(supports_tools=True)
        mock_model_without_tools = MockModelInterface(supports_tools=False)
        
        self.assertTrue(mock_model_with_tools.supports_function_calling())
        self.assertFalse(mock_model_without_tools.supports_function_calling())
    
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
        function_call = mock_model.extract_function_call(response2)
        self.assertEqual(function_call["name"], "test_func")
        self.assertEqual(function_call["arguments"]["arg1"], 123)
        
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
        functions2 = [{"name": "func1"}, {"name": "func2"}]
        
        mock_model.generate_response(messages1, functions1)
        mock_model.generate_response(messages2, functions2)
        
        self.assertEqual(len(mock_model.generate_response_calls), 2)
        self.assertEqual(mock_model.generate_response_calls[0]["messages"], messages1)
        self.assertEqual(mock_model.generate_response_calls[0]["functions"], functions1)
        self.assertEqual(mock_model.generate_response_calls[1]["messages"], messages2)
        self.assertEqual(mock_model.generate_response_calls[1]["functions"], functions2)


if __name__ == "__main__":
    unittest.main() 