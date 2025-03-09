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
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
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
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku-20240307",
    "groq/gemma2-9b-it",
    "mistral/mistral-tiny",
    "deepseek/deepseek-chat",
    "ollama/llama3.3", 
    "ollama/phi4"
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
        pytest.skip(f"API key for {model_name} not available")
    
    # Skip Ollama tests if Ollama is not installed
    if model_name.startswith("ollama/") and os.system("which ollama > /dev/null 2>&1") != 0:
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
    # Set validation strategy based on model
    tool_calling_type = get_tool_calling_type(model)
    validation_observer.set_validation_strategy(tool_calling_type)
    
    # Create agent with specified configuration
    agent = LiteAgent(
        model=model,
        name=f"TestAgent_{model.replace('/', '_')}",
        system_prompt=system_prompt,
        tools=tools,
        observers=[validation_observer]
    )
    
    return agent


@pytest.fixture
def register_tool_parsers(validation_observer, model, tool_names):
    """
    Registers response parsers for the specified tools.
    
    This fixture automatically registers the appropriate parsers
    for the specified tools based on the model's tool calling type.
    
    Args:
        validation_observer: The validation observer
        model: The model name
        tool_names: List of tool names to register parsers for
    """
    tool_calling_type = get_tool_calling_type(model)
    ValidationTestHelper.register_parsers_for_type(
        validation_observer,
        tool_calling_type,
        tool_names
    ) 