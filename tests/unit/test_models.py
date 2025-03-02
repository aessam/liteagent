"""
Unit tests for the model interfaces in LiteAgent.

This module contains tests for the different model interfaces that handle
communication with various LLM providers, focusing especially on function calling.
"""

import json
import pytest
from unittest.mock import MagicMock, patch

# Import LiteAgent components
from liteagent.models import (ModelInterface, FunctionCallingModel, 
                             TextBasedFunctionCallingModel, create_model_interface)

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
            model = FunctionCallingModel(model_name)
            assert model.supports_function_calling(), f"{model_name} should support function calling"
        
        # Test unsupported models
        for model_name in unsupported_models:
            model = FunctionCallingModel(model_name)
            assert not model.supports_function_calling(), f"{model_name} should not support function calling"
    
    def test_create_model_interface_factory(self):
        """Test the factory function for creating model interfaces."""
        # Models that should get a FunctionCallingModel
        function_calling_models = [
            "gpt-4",
            "claude-3-opus",
            "gemini-pro"
        ]
        
        # Models that should get a TextBasedFunctionCallingModel
        text_based_models = [
            "text-davinci-003",
            "ollama/llama2",
            "mistral-7b-instruct"
        ]
        
        # Test that function calling models get the right interface
        for model_name in function_calling_models:
            model = create_model_interface(model_name)
            assert isinstance(model, FunctionCallingModel), f"{model_name} should use FunctionCallingModel"
            assert model.supports_function_calling(), f"{model_name} should support function calling"
        
        # Test that text-based models get the right interface
        for model_name in text_based_models:
            model = create_model_interface(model_name)
            assert isinstance(model, TextBasedFunctionCallingModel), f"{model_name} should use TextBasedFunctionCallingModel"
            assert not model.supports_function_calling(), f"{model_name} should not support function calling"
    
    def test_function_calling_model_response_extraction(self):
        """Test that FunctionCallingModel correctly extracts function calls from responses."""
        model = FunctionCallingModel("gpt-4")
        
        # Create a mock response with a function call
        mock_response = MagicMock()
        mock_response.id = "response-123"
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.function_call = MagicMock()
        mock_response.choices[0].message.function_call.name = "test_function"
        mock_response.choices[0].message.function_call.arguments = '{"param1": "value1", "param2": 123}'
        
        # Extract the function call
        function_call = model.extract_function_call(mock_response)
        
        # Verify the extraction
        assert function_call is not None
        assert function_call["name"] == "test_function"
        assert function_call["arguments"]["param1"] == "value1"
        assert function_call["arguments"]["param2"] == 123
        assert function_call["model_id"] == "response-123"
        
        # Test a response with no function call
        mock_response.choices[0].message.function_call = None
        function_call = model.extract_function_call(mock_response)
        assert function_call is None
    
    def test_function_calling_model_content_extraction(self):
        """Test that FunctionCallingModel correctly extracts content from responses."""
        model = FunctionCallingModel("gpt-4")
        
        # Create a mock response with content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "This is the response content."
        
        # Extract the content
        content = model.extract_content(mock_response)
        
        # Verify the extraction
        assert content == "This is the response content."
        
        # Test a response with empty content
        mock_response.choices[0].message.content = ""
        content = model.extract_content(mock_response)
        assert content == ""
        
        # Test a response with None content
        mock_response.choices[0].message.content = None
        content = model.extract_content(mock_response)
        assert content == ""
    
    def test_text_based_function_calling_model_tool_description(self):
        """Test that TextBasedFunctionCallingModel correctly generates tool descriptions."""
        model = TextBasedFunctionCallingModel("llama2")
        
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
        tool_description = model.get_tool_description_in_prompt(functions)
        
        # Verify the description
        assert "[FUNCTION_CALL]" in tool_description
        assert "[/FUNCTION_CALL]" in tool_description
        assert "get_weather" in tool_description
        assert "search_web" in tool_description
        assert "location (string)" in tool_description
        assert "query (string)" in tool_description
    
    def test_text_based_function_calling_model_response_extraction(self):
        """Test that TextBasedFunctionCallingModel correctly extracts function calls from text responses."""
        model = TextBasedFunctionCallingModel("llama2")
        
        # Create a mock response with a text-based function call
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = """
        I'll help you find the weather.
        
        [FUNCTION_CALL] get_weather(location="New York", unit="celsius") [/FUNCTION_CALL]
        
        This will give us the weather information for New York.
        """
        
        # Extract the function call
        function_call = model.extract_function_call(mock_response)
        
        # Verify the extraction
        assert function_call is not None
        assert function_call["name"] == "get_weather"
        assert function_call["arguments"]["location"] == "New York"
        assert function_call["arguments"]["unit"] == "celsius"
        
        # Test a response with no function call
        mock_response.choices[0].message.content = "There's no function call in this response."
        function_call = model.extract_function_call(mock_response)
        assert function_call is None
        
        # Test a response with an invalid function call format
        mock_response.choices[0].message.content = "[FUNCTION_CALL] invalid format [/FUNCTION_CALL]"
        function_call = model.extract_function_call(mock_response)
        assert function_call is None


if __name__ == "__main__":
    pytest.main(["-v", "test_models.py"]) 