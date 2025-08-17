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


class MockProvider:
    """Mock provider for testing."""
    
    def __init__(self, supports_tools: bool = True):
        self.provider_name = "mock"
        self.supports_tools = supports_tools
    
    def supports_tool_calling(self) -> bool:
        return self.supports_tools


class MockModelInterface:
    """Mock implementation of ModelInterface for testing purposes."""
    
    def __init__(self, model_name: str = "mock-model", supports_tools: bool = True, 
                 responses: List[Dict] = None, api_key: str = None):
        """
        Initialize the mock model interface.
        
        Args:
            model_name: Name of the model to mock
            supports_tools: Whether this mock model supports function calling
            responses: Predefined responses to return. If None, a default response is used.
            api_key: Mock API key (not used)
        """
        self.model_name = model_name
        self.provider = MockProvider(supports_tools)
        self.supports_tools = supports_tools
        self.responses = responses or []
        self.response_index = 0
        
        # Mock capabilities
        self.capabilities = ModelCapabilities(
            model_id=model_name,
            name=model_name,
            provider="mock",
            tool_calling=supports_tools,
            reasoning=True,
            multimodal=False
        )
        
        # For tracking calls
        self.generate_response_calls = []
    
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        return self.supports_tools
    
    def generate_response(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """
        Generate a response from the model.
        
        Args:
            messages: List of conversation messages
            tools: Optional list of tool definitions
            
        Returns:
            ProviderResponse containing the model's response
        """
        kwargs = {"model": self.model_name, "messages": messages}
        
        if tools:
            kwargs["tools"] = tools
        
        # Record the call for later assertions
        self.generate_response_calls.append(kwargs)
        
        # Return the next predefined response if available
        if self.responses and self.response_index < len(self.responses):
            response_data = self.responses[self.response_index]
            self.response_index += 1
            return self._create_provider_response(response_data)
        
        # Default to a text response
        return ProviderResponse(
            content="This is a mock response.",
            tool_calls=[],
            usage={"input_tokens": 10, "output_tokens": 5},
            model=self.model_name,
            provider="mock",
            raw_response={"mock": "response"}
        )
    
    def _create_provider_response(self, response_spec: Dict) -> ProviderResponse:
        """
        Create a ProviderResponse based on the response specification.
        
        Args:
            response_spec: Specification of the response to generate
            
        Returns:
            ProviderResponse object
        """
        response_type = response_spec.get("type", "text")
        
        if response_type == "function_call" or response_type == "tool_call":
            # Tool call response
            function_name = response_spec.get("function_name", "test_function")
            function_args = response_spec.get("function_args", {})
            tool_call_id = response_spec.get("id", "call_mock_123")
            
            tool_call = ToolCall(
                id=tool_call_id,
                name=function_name,
                arguments=function_args
            )
            
            return ProviderResponse(
                content=response_spec.get("content"),  # Can be None for tool calls
                tool_calls=[tool_call],
                usage={"input_tokens": 10, "output_tokens": 5},
                model=self.model_name,
                provider="mock",
                raw_response={"mock": "tool_call_response"}
            )
        else:
            # Text response
            return ProviderResponse(
                content=response_spec.get("content", "This is a mock response."),
                tool_calls=[],
                usage={"input_tokens": 10, "output_tokens": 5},
                model=self.model_name,
                provider="mock",
                raw_response={"mock": "text_response"}
            )


class TestMockModelInterface(unittest.TestCase):
    """Test the MockModelInterface implementation."""
    
    def test_mock_model_text_response(self):
        """Test that the mock model correctly generates text responses."""
        mock_model = MockModelInterface(responses=[
            {"type": "text", "content": "Hello, I am a mock model!"}
        ])
        
        messages = [{"role": "user", "content": "Hello!"}]
        response = mock_model.generate_response(messages)
        
        self.assertIsInstance(response, ProviderResponse)
        self.assertEqual(response.content, "Hello, I am a mock model!")
        self.assertEqual(len(response.tool_calls), 0)
    
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
        tools = [{"name": "get_weather", "parameters": {"location": "string", "unit": "string"}}]
        
        response = mock_model.generate_response(messages, tools)
        
        self.assertIsInstance(response, ProviderResponse)
        self.assertEqual(len(response.tool_calls), 1)
        self.assertEqual(response.tool_calls[0].name, "get_weather")
        self.assertEqual(response.tool_calls[0].arguments["location"], "New York")
        self.assertEqual(response.tool_calls[0].arguments["unit"], "celsius")
    
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
        self.assertEqual(response1.content, "First response")
        self.assertEqual(len(response1.tool_calls), 0)
        
        # Second response
        response2 = mock_model.generate_response(messages)
        self.assertEqual(len(response2.tool_calls), 1)
        self.assertEqual(response2.tool_calls[0].name, "test_func")
        self.assertEqual(response2.tool_calls[0].arguments["arg1"], 123)
        
        # Third response
        response3 = mock_model.generate_response(messages)
        self.assertEqual(response3.content, "Third response")
        self.assertEqual(len(response3.tool_calls), 0)
    
    def test_tracks_calls(self):
        """Test that the mock model correctly tracks calls for later assertions."""
        mock_model = MockModelInterface()
        
        messages1 = [{"role": "user", "content": "First message"}]
        tools1 = [{"name": "func1"}]
        
        messages2 = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
            {"role": "user", "content": "Second message"}
        ]
        
        mock_model.generate_response(messages1, tools1)
        mock_model.generate_response(messages2)
        
        self.assertEqual(len(mock_model.generate_response_calls), 2)
        self.assertEqual(mock_model.generate_response_calls[0]["messages"], messages1)
        self.assertEqual(mock_model.generate_response_calls[0]["tools"], tools1)
        self.assertEqual(mock_model.generate_response_calls[1]["messages"], messages2)
    
    def test_supports_tool_calling(self):
        """Test tool calling support detection."""
        mock_model_with_tools = MockModelInterface(supports_tools=True)
        mock_model_without_tools = MockModelInterface(supports_tools=False)
        
        self.assertTrue(mock_model_with_tools.supports_tool_calling())
        self.assertFalse(mock_model_without_tools.supports_tool_calling())


if __name__ == "__main__":
    unittest.main()