"""
Provider factory for LiteAgent.

This module provides a factory for creating the appropriate provider based on model names.
"""

import os
from typing import Dict, Optional, Type, Any

from .base import ProviderInterface
from ..utils import logger


class ProviderFactory:
    """Factory for creating provider instances based on model names."""
    
    # Provider mapping based on model prefixes (lazy loaded)
    PROVIDER_MAP = {
        'openai': 'openai_provider.OpenAIProvider',
        'openai_assistants': 'openai_assistants.OpenAIAssistantsProvider',
        'anthropic': 'anthropic_provider.AnthropicProvider',
        'google': 'gemini_chat.GeminiChatProvider',
        'groq': 'groq_provider.GroqProvider',
        'mistral': 'mistral_provider.MistralProvider',
        'deepseek': 'openai_provider.DeepSeekProvider',
        'ollama': 'ollama_provider.OllamaProvider',
        'qwen': 'groq_provider.GroqProvider',  # Qwen models are served by Groq
        'mock': 'mock_provider.MockProvider',
        'deterministic_mock': 'deterministic_mock_provider.DeterministicMockProvider',
    }
    
    # Model name patterns for automatic provider detection
    MODEL_PATTERNS = {
        # OpenAI models
        'gpt-': 'openai',
        'text-davinci': 'openai',
        'text-curie': 'openai',
        'text-babbage': 'openai',
        'text-ada': 'openai',
        'davinci': 'openai',
        'curie': 'openai',
        'babbage': 'openai',
        'ada': 'openai',
        
        # Anthropic models
        'claude': 'anthropic',
        
        # Groq models (often have provider prefix or specific names)
        'llama': 'groq',  # Default for Llama models without prefix
        'mixtral': 'groq',  # Default for Mixtral models without prefix
        'gemma': 'groq',
        'qwen/': 'groq',  # Qwen models on Groq with prefix
        'qwen': 'groq',  # Qwen models on Groq
        
        # Mistral models
        'mistral': 'mistral',
        'open-mixtral': 'mistral',  # For models like open-mixtral-8x22b
        
        # DeepSeek models
        'deepseek': 'deepseek',
    }
    
    @classmethod
    def create_provider(
        cls, 
        model_name, 
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        **kwargs
    ) -> ProviderInterface:
        """
        Create the appropriate provider for the given model.
        
        Args:
            model_name: Full model name (string) or (provider, model) tuple
            api_key: API key for the provider
            provider: Explicit provider name (overrides auto-detection)
            **kwargs: Additional provider-specific configuration
            
        Returns:
            ProviderInterface: The appropriate provider instance
            
        Raises:
            ValueError: If the provider cannot be determined or is not supported
        """
        # Handle tuple input: (provider, model_name)
        if isinstance(model_name, tuple):
            tuple_provider, tuple_model_name = model_name
            # Use tuple provider if no explicit provider given
            if not provider:
                provider = tuple_provider
            clean_model_name = tuple_model_name
            provider_name = provider
        elif provider:
            # Use explicit provider, skip auto-detection
            provider_name = provider
            clean_model_name = model_name
        else:
            # Auto-detect provider from model name
            provider_name, clean_model_name = cls._parse_model_name(model_name)
        
        if provider_name not in cls.PROVIDER_MAP:
            raise ValueError(f"Unsupported provider: {provider_name}")
            
        provider_class = cls._load_provider_class(provider_name)
        
        # Add provider-specific configuration
        provider_config = cls._get_provider_config(provider_name, **kwargs)
        
        logger.info(f"Creating {provider_name} provider for model: {clean_model_name}")
        
        try:
            return provider_class(clean_model_name, api_key, **provider_config)
        except Exception as e:
            logger.error(f"Failed to create {provider_name} provider: {e}")
            raise
            
    @classmethod
    def _parse_model_name(cls, model_name: str) -> tuple[str, str]:
        """
        Parse model name to extract provider and clean model name.
        
        Args:
            model_name: Full model name (may include provider prefix)
            
        Returns:
            tuple: (provider_name, clean_model_name)
        """
        # Check for explicit provider prefix (e.g., "openai/gpt-4o")
        if '/' in model_name:
            provider, clean_name = model_name.split('/', 1)
            provider = provider.lower()
            
            if provider in cls.PROVIDER_MAP:
                # Special case: for Groq models like qwen/qwen3-32b, keep the full name
                if provider == 'qwen':
                    return 'groq', model_name  # Use 'groq' provider but keep full model name
                # Special case: for groq/qwen3-32b format, extract just the model name
                elif provider == 'groq' and 'qwen' in clean_name:
                    return provider, clean_name  # Return clean model name without provider prefix
                return provider, clean_name
            else:
                raise ValueError(f"Unknown provider prefix: {provider}")
                
        # Fall back to pattern matching
        model_lower = model_name.lower()
        
        for pattern, provider in cls.MODEL_PATTERNS.items():
            if model_lower.startswith(pattern):
                return provider, model_name
                
        # Fail fast instead of defaulting
        raise ValueError(f"Could not determine provider for model: {model_name}")
        
    @classmethod
    def _load_provider_class(cls, provider_name: str):
        """
        Dynamically load a provider class.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            The provider class
            
        Raises:
            ImportError: If the provider library is not installed
            ValueError: If the provider is not supported
        """
        if provider_name not in cls.PROVIDER_MAP:
            raise ValueError(f"Unsupported provider: {provider_name}")
            
        module_class_path = cls.PROVIDER_MAP[provider_name]
        module_name, class_name = module_class_path.rsplit('.', 1)
        
        try:
            # Import the module dynamically
            from importlib import import_module
            module = import_module(f".{module_name}", package="liteagent.providers")
            
            # Get the class from the module
            provider_class = getattr(module, class_name)
            return provider_class
            
        except ImportError as e:
            # Check if it's a missing dependency or a real import error
            if "not installed" in str(e):
                raise e
            else:
                logger.error(f"Failed to import provider {provider_name}: {e}")
                raise ImportError(f"Provider {provider_name} is not available: {e}")
        except AttributeError as e:
            logger.error(f"Provider class {class_name} not found in {module_name}: {e}")
            raise ValueError(f"Provider {provider_name} implementation is invalid")
        
    @classmethod
    def _get_provider_config(cls, provider_name: str, **kwargs) -> Dict[str, Any]:
        """
        Get provider-specific configuration.
        
        Args:
            provider_name: Name of the provider
            **kwargs: User-provided configuration
            
        Returns:
            Dict: Provider-specific configuration
        """
        config = kwargs.copy()
        
        # Add provider-specific defaults
        if provider_name == 'deepseek':
            config.setdefault('base_url', 'https://api.deepseek.com')
            
        elif provider_name == 'ollama':
            config.setdefault('host', os.getenv('OLLAMA_HOST', 'http://localhost:11434'))
            
        elif provider_name == 'groq':
            # Groq-specific optimizations
            config.setdefault('timeout', 30)  # Groq is usually fast
            
        elif provider_name == 'anthropic':
            # Anthropic-specific settings
            config.setdefault('timeout', 60)
            
        elif provider_name == 'mistral':
            # Mistral-specific settings
            config.setdefault('timeout', 45)
            
        return config
        
    @classmethod
    def get_supported_providers(cls) -> list[str]:
        """Get list of supported provider names."""
        return list(cls.PROVIDER_MAP.keys())
        
    @classmethod
    def is_provider_supported(cls, provider_name: str) -> bool:
        """Check if a provider is supported and available."""
        if provider_name.lower() not in cls.PROVIDER_MAP:
            return False
            
        try:
            cls._load_provider_class(provider_name.lower())
            return True
        except (ImportError, ValueError):
            return False
        
    @classmethod
    def get_provider_for_model(cls, model_name: str) -> str:
        """Get the provider name for a given model."""
        provider_name, _ = cls._parse_model_name(model_name)
        return provider_name
        
    @classmethod
    def determine_provider(cls, model_name: str) -> str:
        """
        Determine the provider for a given model name.
        
        Args:
            model_name: Model name to analyze
            
        Returns:
            str: Provider name
        """
        return cls.get_provider_for_model(model_name)


# Convenience function for creating providers
def create_provider(model_name, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ProviderInterface:
    """
    Convenience function to create a provider.
    
    Args:
        model_name: Model name (string) or (provider, model) tuple
        api_key: API key for the provider
        provider: Explicit provider name (overrides auto-detection)
        **kwargs: Additional provider configuration
        
    Returns:
        ProviderInterface: The appropriate provider instance
    """
    return ProviderFactory.create_provider(model_name, api_key, provider=provider, **kwargs)