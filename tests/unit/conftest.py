"""
Pytest fixtures for LiteAgent tests using REAL API calls.

This module provides fixtures for setting up real LLM testing.
NO MOCKS - uses actual API keys and real provider calls.
"""

import pytest
import os
from typing import List, Dict, Any
from liteagent import LiteAgent
from liteagent.models import create_model_interface
from liteagent.observer import ConsoleObserver, AgentObserver
from liteagent.tools import BaseTool, FunctionTool, liteagent_tool


def pytest_configure(config):
    """Configure pytest to load environment variables."""
    from dotenv import load_dotenv
    load_dotenv()


@pytest.fixture(scope="session")
def api_keys():
    """Get API keys from environment."""
    keys = {
        'openai': os.getenv('OPENAI_API_KEY'),
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'groq': os.getenv('GROQ_API_KEY'),
        'mistral': os.getenv('MISTRAL_API_KEY'),
        'deepseek': os.getenv('DEEPSEEK_API_KEY')
    }
    return keys


@pytest.fixture
def openai_model(api_keys):
    """Create a real OpenAI model interface."""
    if not api_keys['openai']:
        pytest.skip("OPENAI_API_KEY not available")
    return create_model_interface("gpt-4o-mini", api_key=api_keys['openai'])


@pytest.fixture
def anthropic_model(api_keys):
    """Create a real Anthropic model interface."""
    if not api_keys['anthropic']:
        pytest.skip("ANTHROPIC_API_KEY not available")
    return create_model_interface("claude-3-5-haiku-20241022", api_key=api_keys['anthropic'])


@pytest.fixture
def groq_model(api_keys):
    """Create a real Groq model interface."""
    if not api_keys['groq']:
        pytest.skip("GROQ_API_KEY not available")
    return create_model_interface("qwen/qwen3-32b", api_key=api_keys['groq'])


@pytest.fixture
def test_tool():
    """Create a simple test tool function."""
    @liteagent_tool
    def get_current_time() -> str:
        """Get the current time."""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return get_current_time


@pytest.fixture
def calculator_tool():
    """Create a calculator tool for testing."""
    @liteagent_tool
    def calculate(a: float, b: float, operation: str) -> float:
        """
        Perform basic arithmetic operations.
        
        Args:
            a: First number
            b: Second number  
            operation: Operation to perform (add, subtract, multiply, divide)
            
        Returns:
            Result of the calculation
        """
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    return calculate


@pytest.fixture 
def openai_agent(api_keys, test_tool):
    """Create a real OpenAI agent with tools."""
    if not api_keys['openai']:
        pytest.skip("OPENAI_API_KEY not available")
    
    return LiteAgent(
        model="gpt-4o-mini",
        name="test-openai-agent",
        api_key=api_keys['openai'],
        tools=[test_tool],
        system_prompt="You are a helpful test assistant. Use tools when needed."
    )


@pytest.fixture
def anthropic_agent(api_keys, test_tool):
    """Create a real Anthropic agent with tools.""" 
    if not api_keys['anthropic']:
        pytest.skip("ANTHROPIC_API_KEY not available")
        
    return LiteAgent(
        model="claude-3-5-haiku-20241022",
        name="test-anthropic-agent", 
        api_key=api_keys['anthropic'],
        tools=[test_tool],
        system_prompt="You are a helpful test assistant. Use tools when needed."
    )


@pytest.fixture
def groq_agent(api_keys, test_tool):
    """Create a real Groq agent with tools."""
    if not api_keys['groq']:
        pytest.skip("GROQ_API_KEY not available")
        
    return LiteAgent(
        model="qwen/qwen3-32b", 
        name="test-groq-agent",
        api_key=api_keys['groq'],
        tools=[test_tool],
        system_prompt="You are a helpful test assistant. Use tools when needed."
    )