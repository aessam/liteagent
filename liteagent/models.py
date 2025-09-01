"""
New model interfaces for LiteAgent using official provider clients.

This module provides a unified interface for different LLM providers using their
official client libraries instead of LiteLLM.
"""

import time
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

from .providers import create_provider, ProviderInterface, ProviderResponse, ToolCall
from .capabilities import get_model_capabilities, ModelCapabilities
from .utils import logger


class ModelInterface(ABC):
    """Abstract base class for model interfaces."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
        """
        Initialize the model interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider
            provider: Explicit provider name (overrides auto-detection)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = api_key
        self.config = kwargs
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model_name)
        
        # Create the appropriate provider
        self.provider = create_provider(model_name, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    @abstractmethod
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None, **kwargs) -> Any:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message dictionaries
            functions: Optional list of function definitions
            **kwargs: Additional parameters (e.g. enable_caching)
            
        Returns:
            The model's response
        """
        pass
        
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the model's response.
        
        Args:
            response: The model's response
            
        Returns:
            List of dictionaries with tool call details
        """
        if isinstance(response, ProviderResponse):
            # Convert ToolCall objects to dictionaries
            tool_calls = []
            for tc in response.tool_calls:
                tool_calls.append({
                    'id': tc.id,
                    'type': 'function',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def extract_content(self, response: Any) -> str:
        """
        Extract the content from a response.
        
        Args:
            response: The response from the model
            
        Returns:
            str: The text content
        """
        if isinstance(response, ProviderResponse):
            return response.content or ""
        return ""
        
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        if self.capabilities:
            return self.capabilities.tool_calling
        return self.provider.supports_tool_calling()
        
    def supports_parallel_tools(self) -> bool:
        """Check if the model supports parallel tool execution."""
        if self.capabilities:
            return self.capabilities.supports_parallel_tools
        return self.provider.supports_parallel_tools()
        
    def get_context_window(self) -> Optional[int]:
        """Get the context window size for this model."""
        if self.capabilities:
            return self.capabilities.context_limit
        return self.provider.get_context_window()
        
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum output tokens for this model."""
        if self.capabilities:
            return self.capabilities.output_limit
        return self.provider.get_max_tokens()


class UnifiedModelInterface(ModelInterface):
    """
    Unified model interface that works with any supported provider.
    
    This is the main interface that should be used by agents.
    """
    
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message dictionaries
            functions: Optional list of function definitions
            enable_caching: Whether to enable caching (for supported models)
            **kwargs: Additional parameters to pass to the provider
            
        Returns:
            ProviderResponse: Standardized response object
        """
        # Convert function definitions to tools format if needed
        tools = None
        if functions:
            tools = self._convert_functions_to_tools(functions)
            
        # Merge enable_caching with other kwargs
        provider_kwargs = kwargs.copy()
        provider_kwargs['enable_caching'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
    
    def supports_caching(self) -> bool:
        """Check if the model supports caching."""
        if self.capabilities:
            return self.capabilities.supports_caching
        return self.provider.supports_caching()
        
    def _convert_functions_to_tools(self, functions: List[Dict]) -> List[Dict]:
        """
        Convert function definitions to tools format.
        
        Args:
            functions: List of function definitions
            
        Returns:
            List of tool definitions
        """
        tools = []
        for func in functions:
            if 'function' in func:
                # Already in tools format
                tools.append(func)
            else:
                # Convert from legacy function format
                tools.append({
                    'type': 'function',
                    'function': func
                })
        return tools
    
    def get_mock_stats(self) -> Dict[str, Any]:
        """Get mock provider statistics if available."""
        if hasattr(self.provider, 'get_mock_stats'):
            return self.provider.get_mock_stats()
        else:
            # Return empty stats for non-mock providers
            return {
                'total_requests': 0,
                'total_tokens_used': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'cache_hit_rate': 0.0,
                'simulated_cost': 0.0,
                'avg_tokens_per_request': 0.0
            }


# Legacy compatibility class
class LiteLLMInterface(UnifiedModelInterface):
    """
    Legacy compatibility interface that mimics the old LiteLLM interface.
    
    This class provides backward compatibility while using the new provider system.
    """
    
    def __init__(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', None)
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    def _call_api(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)


def create_model_interface(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
    """
    Create a model interface for the given model.
    
    Args:
        model_name: Name of the model
        api_key: API key for the provider
        provider: Explicit provider name (overrides auto-detection)
        **kwargs: Additional configuration
        
    Returns:
        ModelInterface: The appropriate model interface
    """
    return UnifiedModelInterface(model_name, api_key, provider=provider, **kwargs)


def create_legacy_interface(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
    """
    Create a legacy-compatible interface.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters (ignored)
        **kwargs: Additional configuration
        
    Returns:
        LiteLLMInterface: Legacy-compatible interface
    """
    return LiteLLMInterface(model_name, drop_params, **kwargs)