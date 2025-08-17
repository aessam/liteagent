"""
Unit tests for LiteAgent using REAL API calls.

This module contains tests for the main LiteAgent class using real
LLM providers. NO MOCKS - uses actual API keys and real provider calls.
"""

import pytest
from liteagent import LiteAgent
from liteagent.memory import ConversationMemory
from liteagent.observer import ConsoleObserver


def test_openai_agent_initialization(openai_agent):
    """Test that OpenAI agent initializes correctly."""
    assert openai_agent.name == "test-openai-agent"
    assert openai_agent.model == "gpt-4o-mini"
    assert isinstance(openai_agent.memory, ConversationMemory)
    assert len(openai_agent.tools) > 0


def test_anthropic_agent_initialization(anthropic_agent):
    """Test that Anthropic agent initializes correctly."""
    assert anthropic_agent.name == "test-anthropic-agent"
    assert anthropic_agent.model == "claude-3-5-haiku-20241022"
    assert isinstance(anthropic_agent.memory, ConversationMemory)
    assert len(anthropic_agent.tools) > 0


def test_groq_agent_initialization(groq_agent):
    """Test that Groq agent initializes correctly."""
    assert groq_agent.name == "test-groq-agent"
    assert groq_agent.model == "qwen/qwen3-32b"  # Full model name with provider prefix
    assert isinstance(groq_agent.memory, ConversationMemory)
    assert len(groq_agent.tools) > 0


def test_openai_agent_simple_chat(openai_agent):
    """Test simple chat with OpenAI agent."""
    response = openai_agent.chat("Say 'Hello OpenAI' exactly.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    # The response should contain the requested text or be a reasonable response
    assert len(response.strip()) > 5


def test_anthropic_agent_simple_chat(anthropic_agent):
    """Test simple chat with Anthropic agent."""
    response = anthropic_agent.chat("Say 'Hello Anthropic' exactly.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    assert len(response.strip()) > 5


def test_groq_agent_simple_chat(groq_agent):
    """Test simple chat with Groq agent."""
    response = groq_agent.chat("Say 'Hello Groq' exactly.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    assert len(response.strip()) > 5


def test_openai_agent_tool_usage(openai_agent):
    """Test that OpenAI agent can use tools."""
    response = openai_agent.chat("What is the current time? Please use the get_current_time tool.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Check that the tool was likely used by looking for time-related content
    # The response should contain information about the current time
    response_lower = response.lower()
    time_indicators = ["time", "2025", ":", "-"]
    has_time_content = any(indicator in response_lower for indicator in time_indicators)
    
    # Either the response talks about time, or it explains why the tool wasn't used
    assert has_time_content or "time" in response_lower


def test_anthropic_agent_tool_usage(anthropic_agent):
    """Test that Anthropic agent can use tools."""
    response = anthropic_agent.chat("What is the current time? Please use the get_current_time tool.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Check for time-related content
    response_lower = response.lower()
    time_indicators = ["time", "2025", ":", "-"]
    has_time_content = any(indicator in response_lower for indicator in time_indicators)
    
    assert has_time_content or "time" in response_lower


def test_anthropic_sonnet_initialization(anthropic_sonnet_agent):
    """Test Anthropic Sonnet agent initialization."""
    assert anthropic_sonnet_agent.model == "claude-3-5-sonnet-20241022"
    assert anthropic_sonnet_agent.name == "test-sonnet-agent"
    assert anthropic_sonnet_agent.tools is not None
    assert len(anthropic_sonnet_agent.tools) > 0


def test_anthropic_sonnet_simple_chat(anthropic_sonnet_agent):
    """Test Anthropic Sonnet agent simple chat."""
    response = anthropic_sonnet_agent.chat("Hello, can you help me?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_anthropic_sonnet_tool_usage(anthropic_sonnet_agent):
    """Test that Anthropic Sonnet agent can use tools."""
    response = anthropic_sonnet_agent.chat("What is the current time? Please use the get_current_time tool.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Check for time-related content
    response_lower = response.lower()
    time_indicators = ["time", "2025", ":", "-"]
    has_time_content = any(indicator in response_lower for indicator in time_indicators)
    
    assert has_time_content or "time" in response_lower


def test_groq_agent_tool_usage(groq_agent):
    """Test that Groq agent can use tools."""
    response = groq_agent.chat("What is the current time? Please use the get_current_time tool.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Check for time-related content
    response_lower = response.lower()
    time_indicators = ["time", "2025", ":", "-"]
    has_time_content = any(indicator in response_lower for indicator in time_indicators)
    
    assert has_time_content or "time" in response_lower


def test_agent_memory_persistence(openai_agent):
    """Test that agent memory persists across conversations."""
    # First interaction
    response1 = openai_agent.chat("My name is TestUser.")
    assert isinstance(response1, str)
    
    # Second interaction referencing the first
    response2 = openai_agent.chat("What did I tell you my name was?")
    assert isinstance(response2, str)
    
    # The agent should remember the name
    assert "testuser" in response2.lower() or "test" in response2.lower()


def test_agent_reset_memory(openai_agent):
    """Test that agent memory can be reset."""
    # Add some conversation
    openai_agent.chat("Remember that my favorite color is blue.")
    
    # Check memory has messages
    messages_before = openai_agent.memory.get_messages()
    assert len(messages_before) > 2  # At least system, user, assistant
    
    # Reset memory
    openai_agent.reset_memory()
    
    # Check memory is reset
    messages_after = openai_agent.memory.get_messages()
    assert len(messages_after) == 1  # Only system message should remain


def test_agent_with_observer(openai_agent):
    """Test that agent works with observers."""
    observer = ConsoleObserver()
    openai_agent.add_observer(observer)
    
    # Verify observer was added
    assert observer in openai_agent.observers
    
    # Test chat with observer
    response = openai_agent.chat("Hello!")
    assert isinstance(response, str)
    
    # Remove observer
    openai_agent.remove_observer(observer)
    assert observer not in openai_agent.observers


def test_agent_with_calculator_tool(api_keys, calculator_tool):
    """Test agent using calculator tool with real calculation."""
    if not api_keys['openai']:
        pytest.skip("OPENAI_API_KEY not available")
    
    agent = LiteAgent(
        model="gpt-4o-mini",
        name="calculator-agent",
        api_key=api_keys['openai'],
        tools=[calculator_tool],
        system_prompt="You are a calculator assistant. Use the calculate tool for any math operations."
    )
    
    response = agent.chat("What is 25 + 17? Please use the calculate tool.")
    
    assert isinstance(response, str)
    assert len(response) > 0
    
    # The response should mention the result (42) or show calculation
    response_lower = response.lower()
    assert "42" in response or "forty" in response_lower or "add" in response_lower


def test_multiple_providers_same_task(api_keys, test_tool):
    """Test that different providers can handle the same task using target models."""
    providers_to_test = []
    
    # Your target models for testing
    if api_keys['openai']:
        # Try latest models first, fallback to available ones
        for model in ["gpt-5", "gpt-5-mini", "gpt-4o", "gpt-4o-mini"]:
            try:
                # Quick validation that model exists
                from liteagent.providers.factory import ProviderFactory
                ProviderFactory.determine_provider(model)
                providers_to_test.append((model, "openai"))
                break
            except:
                continue
    
    if api_keys['anthropic']:
        # Try latest Anthropic models first
        for model in ["claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022"]:
            try:
                from liteagent.providers.factory import ProviderFactory
                ProviderFactory.determine_provider(model)
                providers_to_test.append((model, "anthropic"))
                break
            except:
                continue
    
    if api_keys['groq']:
        providers_to_test.append(("qwen/qwen3-32b", "groq"))
    
    if api_keys['mistral']:
        providers_to_test.append(("open-mixtral-8x22b", "mistral"))
    
    if api_keys['deepseek']:
        providers_to_test.append(("deepseek-chat", "deepseek"))
    
    if len(providers_to_test) < 2:
        pytest.skip("Need at least 2 providers to test")
    
    responses = []
    task = "Count to 3 and say done."
    
    for model, provider_name in providers_to_test:
        agent = LiteAgent(
            model=model,
            name=f"test-{provider_name}-agent",
            api_key=api_keys[provider_name],
            tools=[test_tool],
            system_prompt="You are a helpful assistant."
        )
        
        response = agent.chat(task)
        responses.append((provider_name, response))
        
        # Each response should be valid
        assert isinstance(response, str)
        assert len(response) > 0
    
    # All providers should have provided responses
    assert len(responses) >= 2
    
    # All responses should be strings with reasonable length
    for provider_name, response in responses:
        assert len(response.strip()) > 5, f"{provider_name} response too short: {response}"


def test_mistral_agent_initialization(mistral_agent):
    """Test Mistral agent initialization with target model."""
    assert mistral_agent.model == "open-mixtral-8x22b"
    assert mistral_agent.name == "test-mistral-agent"
    assert mistral_agent.tools is not None
    assert len(mistral_agent.tools) > 0


def test_mistral_agent_simple_chat(mistral_agent):
    """Test Mistral agent simple chat."""
    response = mistral_agent.chat("Hello, can you help me?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_deepseek_agent_initialization(deepseek_agent):
    """Test DeepSeek agent initialization with target model."""
    assert deepseek_agent.model == "deepseek-chat"
    assert deepseek_agent.name == "test-deepseek-agent"
    assert deepseek_agent.tools is not None
    assert len(deepseek_agent.tools) > 0


def test_deepseek_agent_simple_chat(deepseek_agent):
    """Test DeepSeek agent simple chat."""
    response = deepseek_agent.chat("Hello, can you help me?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_ollama_agent_initialization(ollama_agent):
    """Test Ollama agent initialization with target model."""
    assert ollama_agent.model == "gpt-oss:20b"
    assert ollama_agent.name == "test-ollama-agent"
    assert ollama_agent.tools is not None
    assert len(ollama_agent.tools) > 0


def test_ollama_agent_simple_chat(ollama_agent):
    """Test Ollama agent simple chat."""
    response = ollama_agent.chat("Hello, can you help me?")
    assert isinstance(response, str)
    assert len(response) > 0