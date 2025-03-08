"""
Unit tests for the model interfaces in LiteAgent.

This module contains tests for the different model interfaces that handle
communication with various LLM providers, focusing especially on function calling.
"""

import json
import pytest
from unittest.mock import MagicMock, patch, ANY

# Import LiteAgent components
from liteagent.models import ModelInterface, create_model_interface
from liteagent.tool_calling_types import ToolCallingType, get_provider_from_model
from liteagent.tool_calling import get_tool_calling_handler

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
            "text-davinci-003"
        ]
        
        # Test supported models with OpenAI or Anthropic style function calling
        for model_name in supported_models:
            with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
                if model_name.startswith("gpt"):
                    mock_get_type.return_value = ToolCallingType.OPENAI
                elif model_name.startswith("claude"):
                    mock_get_type.return_value = ToolCallingType.ANTHROPIC
                
                interface = create_model_interface(model_name)
                assert interface.tool_calling_type != ToolCallingType.NONE
                
        # Test unsupported models
        for model_name in unsupported_models:
            with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.NONE
                
                interface = create_model_interface(model_name)
                assert interface.tool_calling_type == ToolCallingType.NONE
    
    def test_create_model_interface_factory(self):
        """Test the factory function for creating model interfaces."""
        # Test that OpenAI-style models get the right tool calling type
        with patch('liteagent.tool_calling_types.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "openai"
            
            with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.OPENAI
                
                interface = create_model_interface("gpt-4")
                assert interface.tool_calling_type == ToolCallingType.OPENAI
        
        # Test that Anthropic-style models get the right tool calling type
        with patch('liteagent.tool_calling_types.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "anthropic"
            
            with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.ANTHROPIC
                
                interface = create_model_interface("claude-3-opus")
                assert interface.tool_calling_type == ToolCallingType.ANTHROPIC
        
        # Test that Ollama models get the right tool calling type
        with patch('liteagent.tool_calling_types.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "ollama"
            with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.OLLAMA
                
                interface = create_model_interface("ollama/phi-2")
                assert interface.tool_calling_type == ToolCallingType.OLLAMA, "ollama/phi-2 should use JSON extraction"
        
        # Test that local models get the right tool calling type
        with patch('liteagent.tool_calling_types.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "local"
            with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.STRUCTURED_OUTPUT
                
                interface = create_model_interface("local/phi-2")
                assert interface.tool_calling_type == ToolCallingType.STRUCTURED_OUTPUT, "local/phi-2 should use text-based tool calling"
    
    def test_function_calling_model_response_extraction(self):
        """Test that ModelInterface correctly extracts tool calls from responses."""
        # Create a model interface with OpenAI tool calling type
        with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
            mock_get_type.return_value = ToolCallingType.OPENAI
            
            with patch('liteagent.tool_calling.get_provider_specific_handler') as mock_get_handler:
                # Mock the handler with a simple implementation that extracts known tool calls
                mock_handler = MagicMock()
                mock_handler.extract_tool_calls.return_value = [
                    {"name": "get_weather", "arguments": {"city": "New York"}}
                ]
                mock_get_handler.return_value = mock_handler
                
                interface = create_model_interface("gpt-4")
                
                # Create a proper mock response object instead of a dictionary
                response = MagicMock()
                response.choices = [MagicMock()]
                response.choices[0].message = MagicMock()
                response.choices[0].message.tool_calls = [MagicMock()]
                response.choices[0].message.tool_calls[0].function = MagicMock()
                response.choices[0].message.tool_calls[0].function.name = "get_weather"
                response.choices[0].message.tool_calls[0].function.arguments = '{"city": "New York"}'
                
                # Check that tool calls are correctly extracted
                tool_calls = interface.extract_tool_calls(response)
                assert len(tool_calls) == 1
                assert tool_calls[0]["name"] == "get_weather"
                assert tool_calls[0]["arguments"]["city"] == "New York"
    
    def test_function_calling_model_content_extraction(self):
        """Test that ModelInterface correctly extracts content from responses."""
        # Create a model interface with OpenAI tool calling type
        with patch('liteagent.tool_calling_types.get_tool_calling_type') as mock_get_type:
            mock_get_type.return_value = ToolCallingType.OPENAI
            
            with patch('liteagent.tool_calling.get_provider_specific_handler') as mock_get_handler:
                # Mock the handler
                mock_handler = MagicMock()
                mock_get_handler.return_value = mock_handler
                
                interface = create_model_interface("gpt-4")
                
                # Create a proper mock response object instead of a dictionary
                response = MagicMock()
                response.choices = [MagicMock()]
                response.choices[0].message = MagicMock()
                response.choices[0].message.content = "Hello world"
                
                content = interface.extract_content(response)
                assert content == "Hello world"
                
                # Test OpenAI response without content
                response = MagicMock()
                response.choices = [MagicMock()]
                response.choices[0].message = MagicMock()
                response.choices[0].message.content = None
                
                content = interface.extract_content(response)
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