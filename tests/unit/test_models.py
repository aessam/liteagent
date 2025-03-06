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
from liteagent.tool_calling_types import ToolCallingType
from liteagent.tool_calling import get_tool_calling_handler
from liteagent.tool_calling_config import get_provider_from_model

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
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                # Mock the function to return a tool calling type that supports function calling
                if "claude" in model_name:
                    mock_get_type.return_value = ToolCallingType.ANTHROPIC_TOOL_CALLING
                else:
                    mock_get_type.return_value = ToolCallingType.OPENAI_FUNCTION_CALLING
                
                model = create_model_interface(model_name)
                
                # Check that the model has the right tool calling type
                assert model.tool_calling_type != ToolCallingType.NONE, f"Model {model_name} should support function calling"
        
        # Test unsupported models
        for model_name in unsupported_models:
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                # Mock the function to return a tool calling type that doesn't support function calling
                mock_get_type.return_value = ToolCallingType.NONE
                
                model = create_model_interface(model_name)
                
                # Check that the model has the right tool calling type
                assert model.tool_calling_type == ToolCallingType.NONE, f"Model {model_name} should not support function calling"
        
        # Note: We're not testing JSON extraction models here because they use a different
        # initialization flow that's covered by other tests.
    
    def test_create_model_interface_factory(self):
        """Test the factory function for creating model interfaces."""
        # Test that OpenAI-style models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "openai"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.OPENAI_FUNCTION_CALLING
                
                model = create_model_interface("gpt-4")
                assert model.tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING, "OpenAI models should use OpenAI-style function calling"
        
        # Test that Anthropic-style models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "anthropic"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.ANTHROPIC_TOOL_CALLING
                
                model = create_model_interface("claude-3-opus")
                assert model.tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING, "claude-3-opus should use Anthropic-style tool calling"
        
        # Test that Ollama models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "ollama"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.OLLAMA_TOOL_CALLING
                
                model = create_model_interface("ollama/phi-2")
                assert model.tool_calling_type == ToolCallingType.OLLAMA_TOOL_CALLING, "ollama/phi-2 should use JSON extraction"
        
        # Test that local models get the right tool calling type
        with patch('liteagent.tool_calling_config.get_provider_from_model') as mock_get_provider:
            mock_get_provider.return_value = "local"
            with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
                mock_get_type.return_value = ToolCallingType.PROMPT_BASED
                
                model = create_model_interface("local/phi-2")
                assert model.tool_calling_type == ToolCallingType.PROMPT_BASED, "local/phi-2 should use text-based tool calling"
    
    def test_function_calling_model_response_extraction(self):
        """Test that ModelInterface correctly extracts tool calls from responses."""
        # Create a model interface with OpenAI tool calling type
        with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
            mock_get_type.return_value = ToolCallingType.OPENAI_FUNCTION_CALLING
            
            model = create_model_interface("gpt-4")
            
            # Create a mock response with function call
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.tool_calls = [MagicMock()]
            mock_response.choices[0].message.tool_calls[0].function = MagicMock()
            mock_response.choices[0].message.tool_calls[0].function.name = "get_weather"
            mock_response.choices[0].message.tool_calls[0].function.arguments = '{"location": "San Francisco"}'
            mock_response.choices[0].message.tool_calls[0].id = "call_123"
            
            # Extract function calls
            function_calls = model.extract_tool_calls(mock_response)
            
            # Verify extraction
            assert len(function_calls) == 1, "Should extract 1 function call"
            assert function_calls[0]["name"] == "get_weather", "Should extract the correct function name"
            assert function_calls[0]["arguments"] == {"location": "San Francisco"}, "Should extract the correct arguments"
            assert function_calls[0]["id"] == "call_123", "Should extract the correct ID"
    
    def test_function_calling_model_content_extraction(self):
        """Test that ModelInterface correctly extracts content from responses."""
        # Create a model interface with OpenAI tool calling type
        with patch('liteagent.tool_calling_config.get_tool_calling_type') as mock_get_type:
            mock_get_type.return_value = ToolCallingType.OPENAI_FUNCTION_CALLING
            
            model = create_model_interface("gpt-4")
            
            # Create a mock response with content
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "This is a test response"
            
            # Extract content
            content = model.extract_content(mock_response)
            
            # Verify extraction
            assert content == "This is a test response", "Should extract the correct content"
    
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