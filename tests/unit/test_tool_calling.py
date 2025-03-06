"""
Unit tests for the tool calling system in LiteAgent.

This module contains tests for the different tool calling handlers and configuration.
"""

import json
import os
import pytest
from unittest.mock import MagicMock, patch

from liteagent.tool_calling import (
    ToolCallingType, ToolCallingHandler, 
    OpenAIToolCallingHandler, AnthropicToolCallingHandler,
    OllamaToolCallingHandler, TextBasedToolCallingHandler,
    StructuredOutputHandler, NoopToolCallingHandler,
    get_tool_calling_handler, AutoDetectToolCallingHandler
)
from liteagent.tool_calling_config import (
    get_provider_from_model, get_tool_calling_type,
    get_tool_calling_handler_type
)


class TestToolCallingTypes:
    """Test the tool calling type detection and configuration."""
    
    def test_get_provider_from_model(self):
        """Test extracting provider from model name."""
        # OpenAI models
        assert get_provider_from_model("gpt-4") == "openai"
        assert get_provider_from_model("gpt-3.5-turbo") == "openai"
        assert get_provider_from_model("text-davinci-003") == "openai"
        
        # Anthropic models
        assert get_provider_from_model("claude-3-opus") == "anthropic"
        assert get_provider_from_model("claude-3-sonnet") == "anthropic"
        
        # Groq models
        assert get_provider_from_model("llama-3.1-8b-instant") == "groq"
        
        # Ollama models
        assert get_provider_from_model("ollama/llama2") == "ollama"
        
        # Unknown models
        assert get_provider_from_model("unknown-model") == "unknown"
    
    def test_get_tool_calling_type(self):
        """Test getting tool calling type for models."""
        # OpenAI models
        assert get_tool_calling_type("gpt-4") == ToolCallingType.OPENAI_FUNCTION_CALLING
        assert get_tool_calling_type("gpt-3.5-turbo") == ToolCallingType.OPENAI_FUNCTION_CALLING
        
        # Anthropic models
        assert get_tool_calling_type("claude-3-opus") == ToolCallingType.ANTHROPIC_TOOL_CALLING
        assert get_tool_calling_type("claude-3-sonnet") == ToolCallingType.ANTHROPIC_TOOL_CALLING
        
        # Ollama models
        assert get_tool_calling_type("ollama/llama2") == ToolCallingType.JSON_EXTRACTION
        
        # Groq models
        assert get_tool_calling_type("groq/llama-3.1-8b-instant") == ToolCallingType.OPENAI_FUNCTION_CALLING
        
        # Models without tool calling support
        assert get_tool_calling_type("text-davinci-003") == ToolCallingType.NONE
    
    def test_get_tool_calling_handler_type(self):
        """Test getting tool calling handler type name."""
        assert get_tool_calling_handler_type("gpt-4") == "OPENAI_FUNCTION_CALLING"
        assert get_tool_calling_handler_type("claude-3-opus") == "ANTHROPIC_TOOL_CALLING"
        assert get_tool_calling_handler_type("ollama/llama2") == "JSON_EXTRACTION"
    
    def test_get_tool_calling_handler(self):
        """Test getting the appropriate handler for a tool calling type."""
        # Test with explicit tool calling types
        assert isinstance(get_tool_calling_handler("gpt-4", ToolCallingType.OPENAI_FUNCTION_CALLING), OpenAIToolCallingHandler)
        assert isinstance(get_tool_calling_handler("claude-3-opus", ToolCallingType.ANTHROPIC_TOOL_CALLING), AnthropicToolCallingHandler)
        assert isinstance(get_tool_calling_handler("ollama/llama2", ToolCallingType.JSON_EXTRACTION), OllamaToolCallingHandler)
        assert isinstance(get_tool_calling_handler("unknown-model", ToolCallingType.PROMPT_BASED), AutoDetectToolCallingHandler)
        assert isinstance(get_tool_calling_handler("text-davinci-003", ToolCallingType.NONE), NoopToolCallingHandler)
        
        # Test with model-based detection
        assert isinstance(get_tool_calling_handler("gpt-4"), OpenAIToolCallingHandler)
        assert isinstance(get_tool_calling_handler("claude-3-opus"), AnthropicToolCallingHandler)
        assert isinstance(get_tool_calling_handler("ollama/llama2"), OllamaToolCallingHandler)
        assert isinstance(get_tool_calling_handler("text-davinci-003"), NoopToolCallingHandler)
        
        # Test with unknown model
        assert isinstance(get_tool_calling_handler("unknown-model"), AutoDetectToolCallingHandler)


class TestOpenAIToolCallingHandler:
    """Test the OpenAI tool calling handler."""
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from an OpenAI response."""
        handler = OpenAIToolCallingHandler()
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.tool_calls = [MagicMock()]
        mock_response.choices[0].message.tool_calls[0].type = "function"
        mock_response.choices[0].message.tool_calls[0].function = MagicMock()
        mock_response.choices[0].message.tool_calls[0].function.name = "get_weather"
        mock_response.choices[0].message.tool_calls[0].function.arguments = '{"location": "San Francisco"}'
        mock_response.choices[0].message.tool_calls[0].id = "call_123"
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(mock_response)
        
        # Verify extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "get_weather"
        assert tool_calls[0]["arguments"]["location"] == "San Francisco"
        assert tool_calls[0]["id"] == "call_123"
        
        # Test with no tool calls
        mock_response.choices[0].message.tool_calls = []
        # Also ensure function_call is not present
        mock_response.choices[0].message.function_call = None
        assert handler.extract_tool_calls(mock_response) == []
        
        # Test with invalid response
        invalid_response = MagicMock()
        invalid_response.choices = []
        assert handler.extract_tool_calls(invalid_response) == []
    
    def test_format_tools_for_model(self):
        """Test formatting tools for OpenAI models."""
        handler = OpenAIToolCallingHandler()
        
        # Create some tools
        tools = [
            {
                "name": "get_weather",
                "description": "Get the weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location"}
                    },
                    "required": ["location"]
                }
            }
        ]
        
        # Format tools
        formatted_tools = handler.format_tools_for_model(tools)
        
        # Check that the tools have been properly formatted with type and function fields
        assert len(formatted_tools) == 1
        assert formatted_tools[0]["type"] == "function"
        assert "function" in formatted_tools[0]
        assert formatted_tools[0]["function"]["name"] == "get_weather"
        assert formatted_tools[0]["function"]["description"] == "Get the weather for a location"
        assert formatted_tools[0]["function"]["parameters"]["type"] == "object"
        assert "location" in formatted_tools[0]["function"]["parameters"]["properties"]
    
    def test_format_tool_results(self):
        """Test formatting tool results for OpenAI models."""
        handler = OpenAIToolCallingHandler()
        
        # Format a result
        result = {"temperature": 72, "conditions": "sunny"}
        formatted_result = handler.format_tool_results("get_weather", result, tool_call_id="call_123")
        
        # Verify format
        assert formatted_result["role"] == "tool"
        assert formatted_result["tool_call_id"] == "call_123"
        assert formatted_result["name"] == "get_weather"
        assert formatted_result["content"] == '{"temperature": 72, "conditions": "sunny"}'


class TestAnthropicToolCallingHandler:
    """Test the Anthropic tool calling handler."""
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from an Anthropic response."""
        handler = AnthropicToolCallingHandler()
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(), MagicMock()]
        mock_response.content[0].type = "text"
        mock_response.content[0].text = "I'll help you with that."
        mock_response.content[1].type = "tool_use"
        mock_response.content[1].name = "get_weather"
        mock_response.content[1].input = {"location": "San Francisco"}
        mock_response.content[1].id = "toolu_123"
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(mock_response)
        
        # Verify extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "get_weather"
        assert tool_calls[0]["arguments"]["location"] == "San Francisco"
        assert tool_calls[0]["id"] == "toolu_123"
        
        # Test with no tool calls
        mock_response.content = [mock_response.content[0]]  # Only text content
        assert handler.extract_tool_calls(mock_response) == []
        
        # Test with invalid response
        invalid_response = MagicMock()
        invalid_response.content = "not a list"
        assert handler.extract_tool_calls(invalid_response) == []
    
    def test_format_tools_for_model(self):
        """Test formatting tools for Anthropic models."""
        handler = AnthropicToolCallingHandler()
        
        # Create some tools
        tools = [
            {
                "name": "get_weather",
                "description": "Get the weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location"}
                    },
                    "required": ["location"]
                }
            }
        ]
        
        # Format tools
        formatted_tools = handler.format_tools_for_model(tools)
        
        # Verify Anthropic format
        assert len(formatted_tools) == 1
        assert formatted_tools[0]["name"] == "get_weather"
        assert formatted_tools[0]["description"] == "Get the weather for a location"
        assert "input_schema" in formatted_tools[0]
    
    def test_format_tool_results(self):
        """Test formatting tool results for Anthropic models."""
        handler = AnthropicToolCallingHandler()
        
        # Format a result
        result = {"temperature": 72, "conditions": "sunny"}
        formatted_result = handler.format_tool_results("get_weather", result, tool_id="toolu_123")
        
        # Verify format
        assert formatted_result["role"] == "user"
        assert "content" in formatted_result
        assert isinstance(formatted_result["content"], str)
        assert "get_weather" in formatted_result["content"]
        assert "72" in formatted_result["content"]
        assert "sunny" in formatted_result["content"]


class TestOllamaToolCallingHandler:
    """Test the Ollama tool calling handler."""
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from an Ollama response."""
        handler = OllamaToolCallingHandler()
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.message = MagicMock()
        mock_response.message.tool_calls = [MagicMock()]
        mock_response.message.tool_calls[0].function = MagicMock()
        mock_response.message.tool_calls[0].function.name = "get_weather"
        mock_response.message.tool_calls[0].function.arguments = {"location": "San Francisco"}
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(mock_response)
        
        # Verify extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "get_weather"
        assert tool_calls[0]["arguments"]["location"] == "San Francisco"
        assert "id" in tool_calls[0]  # Should generate a UUID
        
        # Test with invalid response
        invalid_response = MagicMock()
        invalid_response.message = "not an object"
        assert handler.extract_tool_calls(invalid_response) == []
    
    def test_format_tools_for_model(self):
        """Test formatting tools for Ollama models."""
        handler = OllamaToolCallingHandler()
        
        # Create some tools
        tools = [
            {
                "name": "get_weather",
                "description": "Get the weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location"}
                    },
                    "required": ["location"]
                }
            }
        ]
        
        # Format tools
        formatted_tools = handler.format_tools_for_model(tools)
        
        # Verify Ollama format
        assert len(formatted_tools) == 1
        assert formatted_tools[0]["type"] == "function"
        assert formatted_tools[0]["function"]["name"] == "get_weather"
        assert formatted_tools[0]["function"]["description"].startswith("Get the weather for a location")
        assert "[FUNCTION_CALL]" in formatted_tools[0]["function"]["description"]
        assert "parameters" in formatted_tools[0]["function"]
    
    def test_format_tool_results(self):
        """Test formatting tool results for Ollama models."""
        handler = OllamaToolCallingHandler()
        
        # Format a result
        result = {"temperature": 72, "conditions": "sunny"}
        formatted_result = handler.format_tool_results("get_weather", result)
        
        # Verify format
        assert formatted_result["role"] == "user"
        assert "The result of calling get_weather is:" in formatted_result["content"]
        assert '{"temperature": 72, "conditions": "sunny"}' in formatted_result["content"]


class TestTextBasedToolCallingHandler:
    """Test the text-based tool calling handler."""
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from a text-based response."""
        handler = TextBasedToolCallingHandler()
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = """
        I'll help you find the weather.
        
        [FUNCTION_CALL] get_weather(location="San Francisco", unit="celsius") [/FUNCTION_CALL]
        
        This will give us the weather information for San Francisco.
        """
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(mock_response)
        
        # Verify extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "get_weather"
        assert tool_calls[0]["arguments"]["location"] == "San Francisco"
        assert tool_calls[0]["arguments"]["unit"] == "celsius"
        assert "id" in tool_calls[0]  # Should generate a UUID
        
        # Test with no function call
        mock_response.choices[0].message.content = "There's no function call in this response."
        assert handler.extract_tool_calls(mock_response) == []
        
        # Test with invalid function call format
        mock_response.choices[0].message.content = "[FUNCTION_CALL] invalid format [/FUNCTION_CALL]"
        assert handler.extract_tool_calls(mock_response) == []
    
    def test_format_tools_for_model(self):
        """Test formatting tools for text-based models."""
        handler = TextBasedToolCallingHandler()
        
        # Create some tools
        tools = [
            {
                "name": "get_weather",
                "description": "Get the weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location"},
                        "unit": {"type": "string", "description": "The temperature unit"}
                    },
                    "required": ["location"]
                }
            }
        ]
        
        # Format tools
        formatted_tools = handler.format_tools_for_model(tools)
        
        # Verify text-based format
        assert isinstance(formatted_tools, str)
        assert "[FUNCTION_CALL]" in formatted_tools
        assert "[/FUNCTION_CALL]" in formatted_tools
        assert "get_weather" in formatted_tools
        assert "location (string)" in formatted_tools
        assert "unit (string)" in formatted_tools
    
    def test_format_tool_results(self):
        """Test formatting tool results for text-based models."""
        handler = TextBasedToolCallingHandler()
        
        # Format a result
        result = {"temperature": 72, "conditions": "sunny"}
        formatted_result = handler.format_tool_results("get_weather", result)
        
        # Verify format
        assert formatted_result["role"] == "user"
        assert "The result of calling get_weather is:" in formatted_result["content"]
        assert '{"temperature": 72, "conditions": "sunny"}' in formatted_result["content"]


class TestStructuredOutputHandler:
    """Test the structured output handler."""
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from a structured output response."""
        handler = StructuredOutputHandler()
        
        # Create a mock response with JSON content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = """
        {
          "function": {
            "name": "get_weather",
            "arguments": {
              "location": "San Francisco",
              "unit": "celsius"
            }
          }
        }
        """
        
        # Extract tool calls
        tool_calls = handler.extract_tool_calls(mock_response)
        
        # Verify extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "get_weather"
        assert tool_calls[0]["arguments"]["location"] == "San Francisco"
        assert tool_calls[0]["arguments"]["unit"] == "celsius"
        assert "id" in tool_calls[0]  # Should generate a UUID
        
        # Test with non-JSON content
        mock_response.choices[0].message.content = "This is not JSON"
        assert handler.extract_tool_calls(mock_response) == []
        
        # Test with JSON but not a function call
        mock_response.choices[0].message.content = '{"result": "This is not a function call"}'
        assert handler.extract_tool_calls(mock_response) == []
    
    def test_format_tools_for_model(self):
        """Test formatting tools for structured output models."""
        handler = StructuredOutputHandler()
        
        # Create some tools
        tools = [
            {
                "name": "get_weather",
                "description": "Get the weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location"},
                        "unit": {"type": "string", "description": "The temperature unit"}
                    },
                    "required": ["location"]
                }
            }
        ]
        
        # Format tools
        formatted_tools = handler.format_tools_for_model(tools)
        
        # Verify structured output format
        assert isinstance(formatted_tools, str)
        assert "function" in formatted_tools
        assert "arguments" in formatted_tools
        assert "get_weather" in formatted_tools
        assert "location" in formatted_tools
        assert "unit" in formatted_tools
    
    def test_format_tool_results(self):
        """Test formatting tool results for structured output models."""
        handler = StructuredOutputHandler()
        
        # Format a result
        result = {"temperature": 72, "conditions": "sunny"}
        formatted_result = handler.format_tool_results("get_weather", result)
        
        # Verify format
        assert formatted_result["role"] == "user"
        assert "The result of calling get_weather is:" in formatted_result["content"]
        assert '{"temperature": 72, "conditions": "sunny"}' in formatted_result["content"]


class TestNoopToolCallingHandler:
    """Test the noop tool calling handler."""
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from a noop handler."""
        handler = NoopToolCallingHandler()
        
        # Should always return empty list
        assert handler.extract_tool_calls(MagicMock()) == []
    
    def test_format_tools_for_model(self):
        """Test formatting tools for noop handler."""
        handler = NoopToolCallingHandler()
        
        # Should always return None
        assert handler.format_tools_for_model([]) is None
    
    def test_format_tool_results(self):
        """Test formatting tool results for noop handler."""
        handler = NoopToolCallingHandler()
        
        # Format a result
        result = {"temperature": 72, "conditions": "sunny"}
        formatted_result = handler.format_tool_results("get_weather", result)
        
        # Verify format
        assert formatted_result["role"] == "user"
        assert "The result of calling get_weather is:" in formatted_result["content"]
        assert '{"temperature": 72, "conditions": "sunny"}' in formatted_result["content"]


if __name__ == "__main__":
    pytest.main(["-v", "test_tool_calling.py"]) 