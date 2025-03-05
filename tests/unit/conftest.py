"""
Pytest fixtures for LiteAgent tests.

This module provides fixtures for setting up dependency injection
in LiteAgent unit tests, focusing on creating mock LLMs.
"""

import json
import pytest
from typing import Any, Dict, List, Optional, Union
from unittest.mock import MagicMock, patch

# Import LiteAgent components
from liteagent.models import ModelInterface, create_model_interface
from liteagent.agent import LiteAgent
from liteagent.observer import ConsoleObserver, AgentObserver
from liteagent.tools import BaseTool, FunctionTool
from liteagent.tool_calling import ToolCallingType

# Import our mock model interface
from tests.unit.test_mock_llm import MockModelInterface


@pytest.fixture
def mock_model_interface():
    """
    Create a basic MockModelInterface instance for testing.
    
    Returns:
        MockModelInterface: A mock model interface with default settings
    """
    return MockModelInterface()


@pytest.fixture
def mock_model_with_function_calling():
    """
    Create a MockModelInterface instance that supports function calling.
    
    Returns:
        MockModelInterface: A mock model interface with function calling support
    """
    return MockModelInterface(supports_tools=True)


@pytest.fixture
def mock_model_without_function_calling():
    """
    Create a MockModelInterface instance that doesn't support function calling.
    
    Returns:
        MockModelInterface: A mock model interface without function calling support
    """
    return MockModelInterface(supports_tools=False)


@pytest.fixture
def mock_text_only_model():
    """
    Create a MockModelInterface that only returns text responses.
    
    Returns:
        MockModelInterface: A mock model that only responds with text
    """
    return MockModelInterface(responses=[
        {"type": "text", "content": "This is a text-only response"}
    ])


@pytest.fixture
def mock_function_calling_model():
    """
    Create a MockModelInterface that returns a function call.
    
    Returns:
        MockModelInterface: A mock model that responds with a function call
    """
    return MockModelInterface(responses=[
        {
            "type": "function_call",
            "function_name": "test_function",
            "function_args": {"param1": "value1", "param2": 123}
        }
    ])


@pytest.fixture
def mock_conversation_model():
    """
    Create a MockModelInterface that simulates a conversation with function calls.
    
    Returns:
        MockModelInterface: A mock model that simulates a full conversation
    """
    return MockModelInterface(responses=[
        {"type": "text", "content": "I'll help you with that."},
        {
            "type": "function_call",
            "function_name": "get_data",
            "function_args": {"query": "example"}
        },
        {"type": "text", "content": "Based on the data, here's your answer..."}
    ])


@pytest.fixture
def mock_observer():
    """
    Create a mock observer for testing event emission.
    
    Returns:
        MagicMock: A mock observer that tracks event calls
    """
    observer = MagicMock(spec=AgentObserver)
    return observer


@pytest.fixture
def test_function():
    """
    Create a simple test function that can be used as a tool.
    
    Returns:
        function: A function that returns a predefined response
    """
    def example_function(param1: str, param2: int = 0) -> str:
        """Example function for testing."""
        return f"Function called with param1={param1}, param2={param2}"
    
    return example_function


@pytest.fixture
def test_tool(test_function):
    """
    Create a BaseTool instance for testing.
    
    Args:
        test_function: The test function fixture
        
    Returns:
        BaseTool: A tool based on the test function
    """
    return FunctionTool(test_function)


@pytest.fixture
def agent_with_mock_model(mock_model_interface):
    """
    Create a LiteAgent with a mock model interface injected.
    
    Args:
        mock_model_interface: The mock model interface fixture
        
    Returns:
        LiteAgent: An agent instance with the mock model
    """
    # Patch the create_model_interface function to return our mock
    with patch('liteagent.agent.create_model_interface', return_value=mock_model_interface):
        agent = LiteAgent(
            model="mock-model",
            name="test-agent",
            system_prompt="You are a test agent."
        )
        yield agent


@pytest.fixture
def agent_with_tools(mock_model_with_function_calling, test_function):
    """
    Create a LiteAgent with a mock model and tools.
    
    Args:
        mock_model_with_function_calling: The mock model interface with function calling
        test_function: The test function fixture
        
    Returns:
        LiteAgent: An agent instance with the mock model and tools
    """
    # Patch the create_model_interface function to return our mock
    with patch('liteagent.agent.create_model_interface', return_value=mock_model_with_function_calling):
        agent = LiteAgent(
            model="mock-model",
            name="test-agent",
            system_prompt="You are a test agent.",
            tools=[test_function]
        )
        yield agent


@pytest.fixture
def agent_with_conversation_model(mock_conversation_model, test_function):
    """
    Create a LiteAgent with a mock model that simulates a conversation.
    
    Args:
        mock_conversation_model: The mock conversation model fixture
        test_function: The test function fixture
        
    Returns:
        LiteAgent: An agent instance with the mock conversation model
    """
    # Patch the create_model_interface function to return our mock
    with patch('liteagent.agent.create_model_interface', return_value=mock_conversation_model):
        agent = LiteAgent(
            model="mock-model",
            name="test-agent",
            system_prompt="You are a test agent.",
            tools=[test_function]
        )
        yield agent 