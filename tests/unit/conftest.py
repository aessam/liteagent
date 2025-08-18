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
    # Try latest model first, fallback to available models
    models_to_try = ["gpt-5", "gpt-5-mini", "gpt-4o", "gpt-4o-mini"]
    for model in models_to_try:
        try:
            return create_model_interface(model, api_key=api_keys['openai'])
        except:
            continue
    # If all fail, use the most basic one that should always work
    return create_model_interface("gpt-4o-mini", api_key=api_keys['openai'])


@pytest.fixture
def anthropic_model(api_keys):
    """Create a real Anthropic model interface."""
    if not api_keys['anthropic']:
        pytest.skip("ANTHROPIC_API_KEY not available")
    # Try latest model first, fallback to available models
    models_to_try = ["claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]
    for model in models_to_try:
        try:
            return create_model_interface(model, api_key=api_keys['anthropic'])
        except:
            continue
    # If all fail, use the most basic one that should always work
    return create_model_interface("claude-3-5-haiku-20241022", api_key=api_keys['anthropic'])


@pytest.fixture
def anthropic_sonnet_model(api_keys):
    """Create a real Anthropic Sonnet model interface for comprehensive testing."""
    if not api_keys['anthropic']:
        pytest.skip("ANTHROPIC_API_KEY not available")
    # Try latest Sonnet models first
    models_to_try = ["claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022"]
    for model in models_to_try:
        try:
            return create_model_interface(model, api_key=api_keys['anthropic'])
        except:
            continue
    # Fallback to known working model
    return create_model_interface("claude-3-5-sonnet-20241022", api_key=api_keys['anthropic'])


@pytest.fixture
def groq_model(api_keys):
    """Create a real Groq model interface."""
    if not api_keys['groq']:
        pytest.skip("GROQ_API_KEY not available")
    # Your target model
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
def anthropic_sonnet_agent(api_keys, test_tool):
    """Create a real Anthropic Sonnet agent for comprehensive testing.""" 
    if not api_keys['anthropic']:
        pytest.skip("ANTHROPIC_API_KEY not available")
        
    return LiteAgent(
        model="claude-3-5-sonnet-20241022",
        name="test-sonnet-agent", 
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


@pytest.fixture
def mistral_model(api_keys):
    """Create a real Mistral model interface."""
    if not api_keys['mistral']:
        pytest.skip("MISTRAL_API_KEY not available")
    # Your target model
    return create_model_interface("open-mixtral-8x22b", api_key=api_keys['mistral'])


@pytest.fixture
def mistral_agent(api_keys, test_tool):
    """Create a real Mistral agent with tools."""
    if not api_keys['mistral']:
        pytest.skip("MISTRAL_API_KEY not available")
        
    return LiteAgent(
        model="open-mixtral-8x22b",
        name="test-mistral-agent",
        api_key=api_keys['mistral'],
        tools=[test_tool],
        system_prompt="You are a helpful test assistant. Use tools when needed."
    )


@pytest.fixture
def deepseek_model(api_keys):
    """Create a real DeepSeek model interface."""
    if not api_keys['deepseek']:
        pytest.skip("DEEPSEEK_API_KEY not available")
    # Your target model
    return create_model_interface("deepseek-chat", api_key=api_keys['deepseek'])


@pytest.fixture
def deepseek_agent(api_keys, test_tool):
    """Create a real DeepSeek agent with tools."""
    if not api_keys['deepseek']:
        pytest.skip("DEEPSEEK_API_KEY not available")
        
    return LiteAgent(
        model="deepseek-chat",
        name="test-deepseek-agent",
        api_key=api_keys['deepseek'],
        tools=[test_tool],
        system_prompt="You are a helpful test assistant. Use tools when needed."
    )


@pytest.fixture
def ollama_model(api_keys):
    """Create a real Ollama model interface."""
    # Ollama doesn't need API key, it's local
    # Your target model  
    return create_model_interface("gpt-oss:20b", api_key=None)


@pytest.fixture
def ollama_agent(api_keys, test_tool):
    """Create a real Ollama agent with tools."""
    # Ollama doesn't need API key, it's local
    
    return LiteAgent(
        model="gpt-oss:20b",
        name="test-ollama-agent",
        api_key=None,
        tools=[test_tool],
        system_prompt="You are a helpful test assistant. Use tools when needed."
    )