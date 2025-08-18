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
from tests.utils.validation_tool import get_validation_tools


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
def validation_observer(model):
    """
    Fixture that provides a ValidationObserver instance with pre-configured parsers.
    
    The ValidationObserver is reset before each test to ensure a clean state.
    """
    from liteagent.tool_calling_types import get_tool_calling_type
    from tests.utils.validation_helper import ValidationTestHelper
    
    observer = ValidationObserver()
    
    # Extract model name from tuple for tool calling type detection
    provider, model_name = model
    
    # Pre-configure validation strategy and parsers based on model
    tool_calling_type = get_tool_calling_type(model_name)
    observer.set_validation_strategy(tool_calling_type)
    
    # Register parsers for common tools used in tests
    common_tools = ["get_weather", "add_numbers", "multiply_numbers", "get_user_data", "calculate_area"]
    ValidationTestHelper.register_parsers_for_type(
        observer, 
        tool_calling_type, 
        common_tools
    )
    
    yield observer
    # Reset the observer after each test
    observer.reset()


# Standard set of models to test across all providers
# Using (provider, model) tuples
STANDARD_TEST_MODELS = [
    ("openai", "gpt-5-nano"),
    ("anthropic", "claude-3-7-sonnet-20250219"), 
    ("groq", "llama3-70b-8192"),
    ("mistral", "mistral-large-latest"),
    ("deepseek", "deepseek-chat"),
    ("ollama", "gpt-oss:20b")
]


@pytest.fixture(params=STANDARD_TEST_MODELS)
def model(request):
    """
    Parameterized fixture that provides different models to test with.
    
    This fixture automatically skips tests for models where the API key
    is not available or required dependencies are not installed.
    
    Returns:
        tuple: (provider, model_name) tuple for testing
    """
    provider, model_name = request.param
    
    # Skip if API key not available or required dependencies missing
    if not ValidationTestHelper.has_api_key_for_model(f"{provider}/{model_name}"):
        print(f"DEBUG: Skipping test for {provider}/{model_name} due to missing API key")
        pytest.skip(f"API key for {provider} not available")
    
    # Skip Ollama tests if Ollama is not installed
    if provider == "ollama" and os.system("which ollama > /dev/null 2>&1") != 0:
        print(f"DEBUG: Skipping test for {provider}/{model_name} due to missing Ollama installation")
        pytest.skip("Ollama is not installed or not in PATH")
    
    return (provider, model_name)


@pytest.fixture
def configured_agent(model, validation_observer, tools, system_prompt):
    """
    Creates a pre-configured agent with proper validation.
    
    This fixture combines model, validation_observer, tools, and system_prompt
    to create a fully configured agent ready for testing.
    
    Args:
        model: (provider, model_name) tuple
        validation_observer: The validation observer to attach
        tools: The tools to provide to the agent
        system_prompt: The system prompt to use
        
    Returns:
        LiteAgent: A configured agent ready for testing
    """
    provider, model_name = model
    
    # Add validation tools to the provided tools
    all_tools = list(tools) + get_validation_tools()
    
    # Update system prompt to include validation instructions
    enhanced_prompt = f"""{system_prompt}

CRITICAL REQUIREMENT: You MUST call validate_output as your final action for every task.
- Format: validate_output(result_type, is_correct, explanation)
- This is mandatory for all responses, always do this last
- Examples: 
  * validate_output("weather", True, "Successfully retrieved weather for Tokyo")
  * validate_output("arithmetic", True, "Calculated 7 + 9 = 16 correctly")
  * validate_output("error", False, "Could not complete the task due to missing information")"""
    
    # Create agent with specified configuration
    agent = LiteAgent(
        model=model_name,
        name=f"TestAgent_{provider}_{model_name.replace(':', '_').replace('/', '_')}",
        system_prompt=enhanced_prompt,
        tools=all_tools,
        observers=[validation_observer],
        provider=provider  # Explicit provider from tuple
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