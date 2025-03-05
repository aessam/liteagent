"""
Unit tests for the model interfaces in LiteAgent.

This module contains tests for the different model interfaces that handle
communication with various LLM providers, focusing especially on function calling.
"""

import json
import pytest
from unittest.mock import MagicMock, patch

# Import LiteAgent components
from liteagent.models import ModelInterface, create_model_interface
from liteagent.tool_calling import ToolCallingType, get_tool_calling_handler

# Import our testing utilities
from tests.unit.test_mock_llm import MockModelInterface


class TestModelInterfaces:
    """Test the model interface classes."""
    
    def test_function_calling_model_detection(self):
        """Test the detection of function calling support."""
        # Models that should support function calling
        supported_models = [
            "gpt-4",
            "gpt-3.5-turbo",
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku"
        ]
        
        # Models that should NOT support function calling
        unsupported_models = [
            "text-davinci-003",
            "ollama/llama2",
            "phi-2",
            "mistral-7b-instruct"
        ]
        
        # Test supported models
        for model_name in supported_models:
            tool_calling_type = ToolCallingType.NONE
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                # Mock the function to return a tool calling type that supports function calling
                mock_get_type.return_value = ToolCallingType.OPENAI
                from liteagent.tool_calling_config import get_tool_calling_type
                tool_calling_type = get_tool_calling_type(model_name)
            
            assert tool_calling_type != ToolCallingType.NONE, f"{model_name} should support function calling"
        
        # Test unsupported models
        for model_name in unsupported_models:
            tool_calling_type = ToolCallingType.OPENAI
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                # Mock the function to return a tool calling type that doesn't support function calling
                mock_get_type.return_value = ToolCallingType.NONE
                from liteagent.tool_calling_config import get_tool_calling_type
                tool_calling_type = get_tool_calling_type(model_name)
            
            assert tool_calling_type == ToolCallingType.NONE, f"{model_name} should not support function calling"
    
    def test_create_model_interface_factory(self):
        """Test the factory function for creating model interfaces."""
        # Test that OpenAI-style models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "openai"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.OPENAI
                model = create_model_interface("gpt-4")
                assert isinstance(model, ModelInterface), "gpt-4 should use ModelInterface"
                assert model.tool_calling_type == ToolCallingType.OPENAI, "gpt-4 should use OpenAI-style tool calling"
        
        # Test that Anthropic-style models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "anthropic"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.ANTHROPIC
                model = create_model_interface("claude-3-opus")
                assert isinstance(model, ModelInterface), "claude-3-opus should use ModelInterface"
                assert model.tool_calling_type == ToolCallingType.ANTHROPIC, "claude-3-opus should use Anthropic-style tool calling"
        
        # Test that text-based models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "local"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.TEXT_BASED
                model = create_model_interface("local/phi-2")
                assert isinstance(model, ModelInterface), "local/phi-2 should use ModelInterface"
                assert model.tool_calling_type == ToolCallingType.TEXT_BASED, "local/phi-2 should use text-based tool calling"
    
    def test_function_calling_model_response_extraction(self):
        """Test that ModelInterface correctly extracts tool calls from responses."""
        # Create a model interface with OpenAI tool calling type
        with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
            mock_get_type.return_value = ToolCallingType.OPENAI
            model = create_model_interface("gpt-4")
        
        # Create a mock response with a function call
        mock_response = MagicMock()
        mock_response.id = "response-123"
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.tool_calls = [MagicMock()]
        mock_response.choices[0].message.tool_calls[0].type = "function"
        mock_response.choices[0].message.tool_calls[0].id = "call-123"
        mock_response.choices[0].message.tool_calls[0].function = MagicMock()
        mock_response.choices[0].message.tool_calls[0].function.name = "test_function"
        mock_response.choices[0].message.tool_calls[0].function.arguments = '{"param1": "value1", "param2": 123}'
        
        # Extract the tool calls
        tool_calls = model.extract_tool_calls(mock_response)
        
        # Verify the extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "test_function"
        assert tool_calls[0]["arguments"]["param1"] == "value1"
        assert tool_calls[0]["arguments"]["param2"] == 123
        assert tool_calls[0]["id"] == "call-123"
    
    def test_function_calling_model_content_extraction(self):
        """Test that ModelInterface correctly extracts content from responses."""
        # Create a model interface with OpenAI tool calling type
        with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
            mock_get_type.return_value = ToolCallingType.OPENAI
            model = create_model_interface("gpt-4")
        
        # Create a mock response with content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "This is the response content."
        
        # Extract the content
        content = model.extract_content(mock_response)
        
        # Verify the extraction
        assert content == "This is the response content."
        
        # Test a response with no content
        mock_response.choices[0].message.content = None
        content = model.extract_content(mock_response)
        assert content == ""
    
    def test_text_based_function_calling_model_tool_description(self):
        """Test that TextBasedToolCallingHandler correctly generates tool descriptions."""
        # Create a TextBasedToolCallingHandler
        from liteagent.tool_calling import TextBasedToolCallingHandler
        handler = TextBasedToolCallingHandler()
        
        # Create some function definitions
        functions = [
            {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "parameters": {
                    "properties": {
                        "location": {"type": "string"},
                        "unit": {"type": "string"}
                    }
                }
            },
            {
                "name": "search_web",
                "description": "Search the web for information",
                "parameters": {
                    "properties": {
                        "query": {"type": "string"}
                    }
                }
            }
        ]
        
        # Generate the tool description
        tool_description = handler.format_tools_for_model(functions)
        
        # Verify the description
        assert "get_weather" in tool_description
        assert "search_web" in tool_description
        assert "location" in tool_description
        assert "query" in tool_description
        assert "[FUNCTION_CALL]" in tool_description
    
    def test_text_based_function_calling_model_response_extraction(self):
        """Test that TextBasedToolCallingHandler correctly extracts function calls from text responses."""
        # Create a TextBasedToolCallingHandler
        from liteagent.tool_calling import TextBasedToolCallingHandler
        handler = TextBasedToolCallingHandler()
        
        # Create a mock response with a text-based function call
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = """
        I'll help you find the weather.
        
        [FUNCTION_CALL] get_weather(location="New York", unit="celsius") [/FUNCTION_CALL]
        
        This will give you the current weather in New York.
        """
        
        # Extract the function call
        tool_calls = handler.extract_tool_calls(mock_response)
        
        # Verify the extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "get_weather"
        assert tool_calls[0]["arguments"]["location"] == "New York"
        assert tool_calls[0]["arguments"]["unit"] == "celsius"
        
        # Test a response with no function call
        mock_response.choices[0].message.content = "I don't know how to help with that."
        tool_calls = handler.extract_tool_calls(mock_response)
        assert len(tool_calls) == 0


if __name__ == "__main__":
    pytest.main(["-v", "test_models.py"]) 