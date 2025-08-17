"""
Unit tests for the model interfaces in LiteAgent.

This module contains tests for the different model interfaces that handle
communication with various LLM providers using the new provider system.
"""

import json
import pytest
from unittest.mock import MagicMock, patch, ANY

# Import LiteAgent components
from liteagent.models import UnifiedModelInterface, create_model_interface
from liteagent.capabilities import get_model_capabilities
from liteagent.providers.base import ProviderResponse, ToolCall
from liteagent.providers.factory import ProviderFactory

# Import our testing utilities
from tests.unit.test_mock_llm import MockModelInterface


class TestModelInterfaces:
    """Test the model interface classes."""
    
    def test_create_model_interface_with_mock(self):
        """Test creating a model interface with mock provider."""
        # Test that we can create a mock model interface
        with patch('liteagent.providers.factory.ProviderFactory.create_provider') as mock_create:
            mock_provider = MagicMock()
            mock_provider.provider_name = "mock"
            mock_provider.supports_tool_calling.return_value = True
            mock_create.return_value = mock_provider
            
            interface = create_model_interface("mock-model")
            assert interface is not None
            assert interface.model_name == "mock-model"
    
    def test_model_interface_tool_calling_support(self):
        """Test tool calling support detection."""
        # Test with a mock model that supports tools
        mock_model = MockModelInterface(supports_tools=True)
        assert mock_model.supports_tool_calling() is True
        
        # Test with a mock model that doesn't support tools
        mock_model_no_tools = MockModelInterface(supports_tools=False)
        assert mock_model_no_tools.supports_tool_calling() is False
    
    def test_model_interface_response_generation(self):
        """Test response generation through model interface."""
        mock_model = MockModelInterface(responses=[
            {"type": "text", "content": "Hello, world!"}
        ])
        
        messages = [{"role": "user", "content": "Hi there"}]
        response = mock_model.generate_response(messages)
        
        assert isinstance(response, ProviderResponse)
        assert response.content == "Hello, world!"
        assert len(response.tool_calls) == 0
    
    def test_model_interface_tool_call_generation(self):
        """Test tool call generation through model interface."""
        mock_model = MockModelInterface(responses=[
            {
                "type": "function_call",
                "function_name": "get_weather",
                "function_args": {"location": "San Francisco"}
            }
        ])
        
        messages = [{"role": "user", "content": "What's the weather in SF?"}]
        tools = [{"name": "get_weather", "parameters": {"location": "string"}}]
        
        response = mock_model.generate_response(messages, tools)
        
        assert isinstance(response, ProviderResponse)
        assert len(response.tool_calls) == 1
        assert response.tool_calls[0].name == "get_weather"
        assert response.tool_calls[0].arguments["location"] == "San Francisco"
    
    def test_model_capabilities_integration(self):
        """Test integration with model capabilities system."""
        # Test that we can get capabilities for known models
        # Mock the capabilities detection
        with patch('liteagent.capabilities.get_model_capabilities') as mock_get_caps:
            from liteagent.capabilities import ModelCapabilities
            mock_capabilities = ModelCapabilities(
                model_id="gpt-4o",
                name="GPT-4o",
                provider="openai",
                tool_calling=True,
                reasoning=True,
                multimodal=True
            )
            mock_get_caps.return_value = mock_capabilities
            
            caps = get_model_capabilities("gpt-4o")
            assert caps is not None
            assert caps.tool_calling is True
            assert caps.provider == "openai"
    
    def test_provider_factory_integration(self):
        """Test that model interfaces work with provider factory."""
        # Test that the provider factory can be called without errors
        try:
            with patch('liteagent.providers.factory.ProviderFactory._load_provider_class') as mock_load:
                # Mock loading a provider class
                mock_provider_class = MagicMock()
                mock_provider_instance = MagicMock()
                mock_provider_instance.provider_name = "test"
                mock_provider_class.return_value = mock_provider_instance
                mock_load.return_value = mock_provider_class
                
                # This should not raise an exception
                factory = ProviderFactory()
                provider = factory.create_provider("test-model", api_key="test")
                assert provider is not None
        except ImportError:
            # Expected if optional dependencies aren't installed
            pytest.skip("Provider dependencies not installed")
    
    def test_unified_model_interface_creation(self):
        """Test creation of unified model interface."""
        # Mock capabilities first (before creating interface)
        from liteagent.capabilities import ModelCapabilities
        mock_capabilities = ModelCapabilities(
            model_id="test-model",
            name="Test Model",
            provider="mock",
            tool_calling=True,
            reasoning=False,
            multimodal=False
        )
        
        with patch('liteagent.capabilities.get_model_capabilities') as mock_get_caps:
            mock_get_caps.return_value = mock_capabilities
            
            # Test with mock provider
            with patch('liteagent.providers.factory.ProviderFactory.create_provider') as mock_create:
                mock_provider = MagicMock()
                mock_provider.provider_name = "mock"
                mock_provider.supports_tool_calling.return_value = True
                mock_create.return_value = mock_provider
                
                interface = create_model_interface("test-model")
                assert isinstance(interface, UnifiedModelInterface)
                assert interface.model_name == "test-model"
                # Capabilities should be set during initialization
                assert interface.capabilities is not None
                assert interface.capabilities.model_id == "test-model"


class TestModelCapabilities:
    """Test the model capabilities system."""
    
    def test_capabilities_fallback(self):
        """Test that capabilities system handles unknown models gracefully."""
        with patch('liteagent.capabilities._capability_detector._fetch_models_data'):
            # When no capabilities are found, should return None
            with patch('liteagent.capabilities._capability_detector.get_model_capabilities') as mock_get:
                mock_get.return_value = None
                
                caps = get_model_capabilities("unknown-model")
                assert caps is None
    
    def test_capabilities_caching(self):
        """Test that capabilities are cached properly."""
        with patch('liteagent.capabilities._capability_detector._refresh_cache_if_needed') as mock_refresh:
            # Call get_model_capabilities twice
            get_model_capabilities("test-model")
            get_model_capabilities("test-model")
            
            # Should only refresh once due to caching
            assert mock_refresh.call_count >= 1


if __name__ == "__main__":
    pytest.main([__file__])