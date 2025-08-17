"""
Pytest configuration for integration tests.

This module provides fixtures and setup for integration tests,
including loading environment variables from .env file.
"""

import os
import pytest
import dotenv
from pathlib import Path
from typing import List, Dict, Any, Optional

from liteagent import LiteAgent
from liteagent.capabilities import get_model_capabilities, ModelCapabilities
from liteagent.tools import liteagent_tool
from tests.integration.validation_observer import ValidationObserver
from tests.utils.validation_helper import ValidationTestHelper


# Load environment variables from .env file if it exists
def pytest_configure(config):
    """
    Load environment variables from .env file before running tests.
    
    This ensures API keys are available for integration tests.
    """
    # Find the project root (where .env file should be located)
    project_root = Path(__file__).parent.parent.parent
    dotenv_path = project_root / '.env'
    
    if dotenv_path.exists():
        print(f"Loading environment variables from {dotenv_path}")
        dotenv.load_dotenv(dotenv_path)
    else:
        print("Warning: .env file not found. Make sure API keys are set in your environment.")
    
    # Print a message if API keys are missing
    if "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY not found in environment variables. Tests requiring OpenAI will be skipped.")
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Warning: ANTHROPIC_API_KEY not found in environment variables. Tests requiring Anthropic will be skipped.")
    if "GROQ_API_KEY" not in os.environ:
        print("Warning: GROQ_API_KEY not found in environment variables. Tests requiring Groq will be skipped.")
    if "MISTRAL_API_KEY" not in os.environ:
        print("Warning: MISTRAL_API_KEY not found in environment variables. Tests requiring Mistral will be skipped.")
    if "DEEPSEEK_API_KEY" not in os.environ:
        print("Warning: DEEPSEEK_API_KEY not found in environment variables. Tests requiring DeepSeek will be skipped.")


@pytest.fixture
def validation_observer():
    """
    Fixture that provides a ValidationObserver instance.
    
    The ValidationObserver is reset before each test to ensure a clean state.
    """
    observer = ValidationObserver()
    yield observer
    # Reset the observer after each test
    observer.reset()


# Standard set of models to test across all providers
STANDARD_TEST_MODELS = [
    "openai/gpt-5",
    "openai/gpt-5-nano",
    "openai/gpt-5-mini",
    "anthropic/claude-3-7-sonnet-20250219",
    "anthropic/claude-3-5-sonnet-20241022",
    "groq/qwen3-32b",
    "mistral/open-mixtral-8x22b",
    "deepseek/deepseek-chat",
    "ollama/gpt-oss:20b"
]


@pytest.fixture(params=STANDARD_TEST_MODELS)
def model(request):
    """
    Parameterized fixture that provides different models to test with.
    
    This fixture automatically skips tests for models where the API key
    is not available or required dependencies are not installed.
    
    Returns:
        str: The model name to use for testing
    """
    model_name = request.param
    
    # Skip if API key not available or required dependencies missing
    if not ValidationTestHelper.has_api_key_for_model(model_name):
        print(f"DEBUG: Skipping test for {model_name} due to missing API key")
        pytest.skip(f"API key for {model_name} not available")
    
    # Skip Ollama tests if Ollama is not installed
    if model_name.startswith("ollama/") and os.system("which ollama > /dev/null 2>&1") != 0:
        print(f"DEBUG: Skipping test for {model_name} due to missing Ollama installation")
        pytest.skip("Ollama is not installed or not in PATH")
    
    return model_name


@pytest.fixture
def configured_agent(model, validation_observer, tools, system_prompt):
    """
    Creates a pre-configured agent with proper validation.
    
    This fixture combines model, validation_observer, tools, and system_prompt
    to create a fully configured agent ready for testing.
    
    Args:
        model: The model name to use
        validation_observer: The validation observer to attach
        tools: The tools to provide to the agent
        system_prompt: The system prompt to use
        
    Returns:
        LiteAgent: A configured agent ready for testing
    """
    # Create agent with specified configuration
    agent = LiteAgent(
        model=model,
        name=f"TestAgent_{model.replace('/', '_')}",
        system_prompt=system_prompt,
        tools=tools,
        observers=[validation_observer]
    )
    
    return agent


# Add agent fixtures for observer integration tests
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
def test_tool():
    """Create a simple test tool function."""
    @liteagent_tool
    def get_current_time() -> str:
        """Get the current time."""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return get_current_time


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