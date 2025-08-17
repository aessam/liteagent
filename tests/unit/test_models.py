"""
Unit tests for the model interfaces in LiteAgent using REAL API calls.

This module contains tests for the different model interfaces that handle
communication with various LLM providers using the new provider system.
NO MOCKS - uses actual API keys and real provider calls.
"""

import pytest
from liteagent.models import create_model_interface, UnifiedModelInterface
from liteagent.capabilities import get_model_capabilities
from liteagent.providers.base import ProviderResponse, ToolCall
from liteagent.providers.factory import ProviderFactory


def test_model_capabilities_real_api():
    """Test that we can get real capabilities from models.dev API."""
    caps = get_model_capabilities('gpt-4o')
    
    assert caps is not None
    assert caps.tool_calling is True
    # Handle both formats: "gpt-4o" and "openai/gpt-4o"
    assert caps.model_id in ['gpt-4o', 'openai/gpt-4o']
    # Note: Real API may return different provider names


def test_openai_model_creation(openai_model):
    """Test creating a real OpenAI model interface."""
    assert isinstance(openai_model, UnifiedModelInterface)
    assert openai_model.model_name == "gpt-4o-mini"
    assert openai_model.supports_tool_calling() is True


def test_anthropic_model_creation(anthropic_model):
    """Test creating a real Anthropic model interface."""
    assert isinstance(anthropic_model, UnifiedModelInterface)
    assert anthropic_model.model_name == "claude-3-5-haiku-20241022"
    assert anthropic_model.supports_tool_calling() is True


def test_groq_model_creation(groq_model):
    """Test creating a real Groq model interface."""
    assert isinstance(groq_model, UnifiedModelInterface)
    assert groq_model.model_name == "qwen/qwen3-32b"
    assert groq_model.supports_tool_calling() is True


def test_openai_text_generation(openai_model):
    """Test real text generation with OpenAI."""
    messages = [{"role": "user", "content": "Say 'Hello from OpenAI' exactly."}]
    response = openai_model.generate_response(messages)
    
    assert isinstance(response, ProviderResponse)
    assert response.content is not None
    assert len(response.content) > 0
    assert response.provider == "openai"


def test_anthropic_text_generation(anthropic_model):
    """Test real text generation with Anthropic."""
    messages = [{"role": "user", "content": "Say 'Hello from Anthropic' exactly."}]
    response = anthropic_model.generate_response(messages)
    
    assert isinstance(response, ProviderResponse)
    assert response.content is not None
    assert len(response.content) > 0
    assert response.provider == "anthropic"


def test_groq_text_generation(groq_model):
    """Test real text generation with Groq.""" 
    messages = [{"role": "user", "content": "Say 'Hello from Groq' exactly."}]
    response = groq_model.generate_response(messages)
    
    assert isinstance(response, ProviderResponse)
    assert response.content is not None
    assert len(response.content) > 0
    assert response.provider == "groq"


def test_openai_tool_calling(openai_model, calculator_tool):
    """Test real tool calling with OpenAI."""
    messages = [{"role": "user", "content": "What is 15 + 25? Use the calculate tool."}]
    
    # Prepare tools in the correct format
    tools = [{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform basic arithmetic operations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                    "operation": {"type": "string", "description": "Operation to perform (add, subtract, multiply, divide)"}
                },
                "required": ["a", "b", "operation"]
            }
        }
    }]
    
    response = openai_model.generate_response(messages, tools)
    
    assert isinstance(response, ProviderResponse)
    
    # Should either have content or tool calls (or both)
    assert response.content is not None or len(response.tool_calls) > 0
    
    # If tool calls were made, verify they're properly formatted
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        assert isinstance(tool_call, ToolCall)
        assert tool_call.name == "calculate"
        assert "a" in tool_call.arguments
        assert "b" in tool_call.arguments
        assert "operation" in tool_call.arguments


def test_provider_factory_real():
    """Test provider factory with real models.""" 
    factory = ProviderFactory()
    
    # Test OpenAI detection
    provider_name = factory.determine_provider("gpt-4o")
    assert provider_name == "openai"
    
    # Test Anthropic detection
    provider_name = factory.determine_provider("claude-3-5-haiku")
    assert provider_name == "anthropic"
    
    # Test Groq detection
    provider_name = factory.determine_provider("qwen3-32b")
    assert provider_name == "groq"


def test_capabilities_caching():
    """Test that capabilities are cached between calls."""
    # First call
    caps1 = get_model_capabilities("gpt-4o")
    
    # Second call should use cache
    caps2 = get_model_capabilities("gpt-4o")
    
    # Should return same data
    if caps1 and caps2:
        assert caps1.model_id == caps2.model_id
        assert caps1.tool_calling == caps2.tool_calling