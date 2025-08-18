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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ModelInterface(ABC):
    """Abstract base class for model interfaces."""
    
    def xǁModelInterfaceǁ__init____mutmut_orig(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        
    
    def xǁModelInterfaceǁ__init____mutmut_1(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
        """
        Initialize the model interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider
            provider: Explicit provider name (overrides auto-detection)
            **kwargs: Provider-specific configuration
        """
        self.model_name = None
        self.api_key = api_key
        self.config = kwargs
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model_name)
        
        # Create the appropriate provider
        self.provider = create_provider(model_name, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_2(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
        """
        Initialize the model interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider
            provider: Explicit provider name (overrides auto-detection)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = None
        self.config = kwargs
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model_name)
        
        # Create the appropriate provider
        self.provider = create_provider(model_name, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_3(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.config = None
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model_name)
        
        # Create the appropriate provider
        self.provider = create_provider(model_name, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_4(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.capabilities = None
        
        # Create the appropriate provider
        self.provider = create_provider(model_name, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_5(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.capabilities = get_model_capabilities(None)
        
        # Create the appropriate provider
        self.provider = create_provider(model_name, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_6(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = None
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_7(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(None, api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_8(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(model_name, None, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_9(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(model_name, api_key, provider=None, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_10(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(api_key, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_11(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(model_name, provider=provider, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_12(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(model_name, api_key, **kwargs)
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_13(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        self.provider = create_provider(model_name, api_key, provider=provider, )
        
        logger.info(f"Initialized {self.provider.provider_name} model interface for {model_name}")
        
    
    def xǁModelInterfaceǁ__init____mutmut_14(self, model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs):
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
        
        logger.info(None)
        
    
    xǁModelInterfaceǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁModelInterfaceǁ__init____mutmut_1': xǁModelInterfaceǁ__init____mutmut_1, 
        'xǁModelInterfaceǁ__init____mutmut_2': xǁModelInterfaceǁ__init____mutmut_2, 
        'xǁModelInterfaceǁ__init____mutmut_3': xǁModelInterfaceǁ__init____mutmut_3, 
        'xǁModelInterfaceǁ__init____mutmut_4': xǁModelInterfaceǁ__init____mutmut_4, 
        'xǁModelInterfaceǁ__init____mutmut_5': xǁModelInterfaceǁ__init____mutmut_5, 
        'xǁModelInterfaceǁ__init____mutmut_6': xǁModelInterfaceǁ__init____mutmut_6, 
        'xǁModelInterfaceǁ__init____mutmut_7': xǁModelInterfaceǁ__init____mutmut_7, 
        'xǁModelInterfaceǁ__init____mutmut_8': xǁModelInterfaceǁ__init____mutmut_8, 
        'xǁModelInterfaceǁ__init____mutmut_9': xǁModelInterfaceǁ__init____mutmut_9, 
        'xǁModelInterfaceǁ__init____mutmut_10': xǁModelInterfaceǁ__init____mutmut_10, 
        'xǁModelInterfaceǁ__init____mutmut_11': xǁModelInterfaceǁ__init____mutmut_11, 
        'xǁModelInterfaceǁ__init____mutmut_12': xǁModelInterfaceǁ__init____mutmut_12, 
        'xǁModelInterfaceǁ__init____mutmut_13': xǁModelInterfaceǁ__init____mutmut_13, 
        'xǁModelInterfaceǁ__init____mutmut_14': xǁModelInterfaceǁ__init____mutmut_14
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁModelInterfaceǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁModelInterfaceǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁModelInterfaceǁ__init____mutmut_orig)
    xǁModelInterfaceǁ__init____mutmut_orig.__name__ = 'xǁModelInterfaceǁ__init__'
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
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_orig(self, response: Any) -> List[Dict]:
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
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_1(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the model's response.
        
        Args:
            response: The model's response
            
        Returns:
            List of dictionaries with tool call details
        """
        if isinstance(response, ProviderResponse):
            # Convert ToolCall objects to dictionaries
            tool_calls = None
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
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_2(self, response: Any) -> List[Dict]:
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
                tool_calls.append(None)
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_3(self, response: Any) -> List[Dict]:
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
                    'XXidXX': tc.id,
                    'type': 'function',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_4(self, response: Any) -> List[Dict]:
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
                    'ID': tc.id,
                    'type': 'function',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_5(self, response: Any) -> List[Dict]:
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
                    'XXtypeXX': 'function',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_6(self, response: Any) -> List[Dict]:
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
                    'TYPE': 'function',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_7(self, response: Any) -> List[Dict]:
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
                    'type': 'XXfunctionXX',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_8(self, response: Any) -> List[Dict]:
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
                    'type': 'FUNCTION',
                    'function': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_9(self, response: Any) -> List[Dict]:
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
                    'XXfunctionXX': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_10(self, response: Any) -> List[Dict]:
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
                    'FUNCTION': {
                        'name': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_11(self, response: Any) -> List[Dict]:
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
                        'XXnameXX': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_12(self, response: Any) -> List[Dict]:
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
                        'NAME': tc.name,
                        'arguments': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_13(self, response: Any) -> List[Dict]:
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
                        'XXargumentsXX': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    def xǁModelInterfaceǁextract_tool_calls__mutmut_14(self, response: Any) -> List[Dict]:
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
                        'ARGUMENTS': tc.arguments
                    }
                })
            return tool_calls
        return []
        
    
    xǁModelInterfaceǁextract_tool_calls__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁModelInterfaceǁextract_tool_calls__mutmut_1': xǁModelInterfaceǁextract_tool_calls__mutmut_1, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_2': xǁModelInterfaceǁextract_tool_calls__mutmut_2, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_3': xǁModelInterfaceǁextract_tool_calls__mutmut_3, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_4': xǁModelInterfaceǁextract_tool_calls__mutmut_4, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_5': xǁModelInterfaceǁextract_tool_calls__mutmut_5, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_6': xǁModelInterfaceǁextract_tool_calls__mutmut_6, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_7': xǁModelInterfaceǁextract_tool_calls__mutmut_7, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_8': xǁModelInterfaceǁextract_tool_calls__mutmut_8, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_9': xǁModelInterfaceǁextract_tool_calls__mutmut_9, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_10': xǁModelInterfaceǁextract_tool_calls__mutmut_10, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_11': xǁModelInterfaceǁextract_tool_calls__mutmut_11, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_12': xǁModelInterfaceǁextract_tool_calls__mutmut_12, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_13': xǁModelInterfaceǁextract_tool_calls__mutmut_13, 
        'xǁModelInterfaceǁextract_tool_calls__mutmut_14': xǁModelInterfaceǁextract_tool_calls__mutmut_14
    }
    
    def extract_tool_calls(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁModelInterfaceǁextract_tool_calls__mutmut_orig"), object.__getattribute__(self, "xǁModelInterfaceǁextract_tool_calls__mutmut_mutants"), args, kwargs, self)
        return result 
    
    extract_tool_calls.__signature__ = _mutmut_signature(xǁModelInterfaceǁextract_tool_calls__mutmut_orig)
    xǁModelInterfaceǁextract_tool_calls__mutmut_orig.__name__ = 'xǁModelInterfaceǁextract_tool_calls'
    def xǁModelInterfaceǁextract_content__mutmut_orig(self, response: Any) -> str:
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
        
    def xǁModelInterfaceǁextract_content__mutmut_1(self, response: Any) -> str:
        """
        Extract the content from a response.
        
        Args:
            response: The response from the model
            
        Returns:
            str: The text content
        """
        if isinstance(response, ProviderResponse):
            return response.content and ""
        return ""
        
    def xǁModelInterfaceǁextract_content__mutmut_2(self, response: Any) -> str:
        """
        Extract the content from a response.
        
        Args:
            response: The response from the model
            
        Returns:
            str: The text content
        """
        if isinstance(response, ProviderResponse):
            return response.content or "XXXX"
        return ""
        
    def xǁModelInterfaceǁextract_content__mutmut_3(self, response: Any) -> str:
        """
        Extract the content from a response.
        
        Args:
            response: The response from the model
            
        Returns:
            str: The text content
        """
        if isinstance(response, ProviderResponse):
            return response.content or ""
        return "XXXX"
        
    
    xǁModelInterfaceǁextract_content__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁModelInterfaceǁextract_content__mutmut_1': xǁModelInterfaceǁextract_content__mutmut_1, 
        'xǁModelInterfaceǁextract_content__mutmut_2': xǁModelInterfaceǁextract_content__mutmut_2, 
        'xǁModelInterfaceǁextract_content__mutmut_3': xǁModelInterfaceǁextract_content__mutmut_3
    }
    
    def extract_content(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁModelInterfaceǁextract_content__mutmut_orig"), object.__getattribute__(self, "xǁModelInterfaceǁextract_content__mutmut_mutants"), args, kwargs, self)
        return result 
    
    extract_content.__signature__ = _mutmut_signature(xǁModelInterfaceǁextract_content__mutmut_orig)
    xǁModelInterfaceǁextract_content__mutmut_orig.__name__ = 'xǁModelInterfaceǁextract_content'
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
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_orig(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_1(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = True, **kwargs) -> ProviderResponse:
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
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_2(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        tools = ""
        if functions:
            tools = self._convert_functions_to_tools(functions)
            
        # Merge enable_caching with other kwargs
        provider_kwargs = kwargs.copy()
        provider_kwargs['enable_caching'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_3(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
            tools = None
            
        # Merge enable_caching with other kwargs
        provider_kwargs = kwargs.copy()
        provider_kwargs['enable_caching'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_4(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
            tools = self._convert_functions_to_tools(None)
            
        # Merge enable_caching with other kwargs
        provider_kwargs = kwargs.copy()
        provider_kwargs['enable_caching'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_5(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        provider_kwargs = None
        provider_kwargs['enable_caching'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_6(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        provider_kwargs['enable_caching'] = None
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_7(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        provider_kwargs['XXenable_cachingXX'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_8(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        provider_kwargs['ENABLE_CACHING'] = enable_caching
            
        # Generate response using the provider
        response = self.provider.generate_response(messages, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_9(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        response = None
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_10(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        response = self.provider.generate_response(None, tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_11(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        response = self.provider.generate_response(messages, None, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_12(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        response = self.provider.generate_response(tools, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_13(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        response = self.provider.generate_response(messages, **provider_kwargs)
        
        return response
        
    
    def xǁUnifiedModelInterfaceǁgenerate_response__mutmut_14(self, messages: List[Dict], functions: Optional[List[Dict]] = None, enable_caching: bool = False, **kwargs) -> ProviderResponse:
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
        response = self.provider.generate_response(messages, tools, )
        
        return response
        
    
    xǁUnifiedModelInterfaceǁgenerate_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_1': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_1, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_2': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_2, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_3': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_3, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_4': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_4, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_5': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_5, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_6': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_6, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_7': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_7, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_8': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_8, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_9': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_9, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_10': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_10, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_11': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_11, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_12': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_12, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_13': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_13, 
        'xǁUnifiedModelInterfaceǁgenerate_response__mutmut_14': xǁUnifiedModelInterfaceǁgenerate_response__mutmut_14
    }
    
    def generate_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedModelInterfaceǁgenerate_response__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedModelInterfaceǁgenerate_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_response.__signature__ = _mutmut_signature(xǁUnifiedModelInterfaceǁgenerate_response__mutmut_orig)
    xǁUnifiedModelInterfaceǁgenerate_response__mutmut_orig.__name__ = 'xǁUnifiedModelInterfaceǁgenerate_response'
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_orig(self, functions: List[Dict]) -> List[Dict]:
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
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_1(self, functions: List[Dict]) -> List[Dict]:
        """
        Convert function definitions to tools format.
        
        Args:
            functions: List of function definitions
            
        Returns:
            List of tool definitions
        """
        tools = None
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
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_2(self, functions: List[Dict]) -> List[Dict]:
        """
        Convert function definitions to tools format.
        
        Args:
            functions: List of function definitions
            
        Returns:
            List of tool definitions
        """
        tools = []
        for func in functions:
            if 'XXfunctionXX' in func:
                # Already in tools format
                tools.append(func)
            else:
                # Convert from legacy function format
                tools.append({
                    'type': 'function',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_3(self, functions: List[Dict]) -> List[Dict]:
        """
        Convert function definitions to tools format.
        
        Args:
            functions: List of function definitions
            
        Returns:
            List of tool definitions
        """
        tools = []
        for func in functions:
            if 'FUNCTION' in func:
                # Already in tools format
                tools.append(func)
            else:
                # Convert from legacy function format
                tools.append({
                    'type': 'function',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_4(self, functions: List[Dict]) -> List[Dict]:
        """
        Convert function definitions to tools format.
        
        Args:
            functions: List of function definitions
            
        Returns:
            List of tool definitions
        """
        tools = []
        for func in functions:
            if 'function' not in func:
                # Already in tools format
                tools.append(func)
            else:
                # Convert from legacy function format
                tools.append({
                    'type': 'function',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_5(self, functions: List[Dict]) -> List[Dict]:
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
                tools.append(None)
            else:
                # Convert from legacy function format
                tools.append({
                    'type': 'function',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_6(self, functions: List[Dict]) -> List[Dict]:
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
                tools.append(None)
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_7(self, functions: List[Dict]) -> List[Dict]:
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
                    'XXtypeXX': 'function',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_8(self, functions: List[Dict]) -> List[Dict]:
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
                    'TYPE': 'function',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_9(self, functions: List[Dict]) -> List[Dict]:
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
                    'type': 'XXfunctionXX',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_10(self, functions: List[Dict]) -> List[Dict]:
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
                    'type': 'FUNCTION',
                    'function': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_11(self, functions: List[Dict]) -> List[Dict]:
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
                    'XXfunctionXX': func
                })
        return tools
    def xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_12(self, functions: List[Dict]) -> List[Dict]:
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
                    'FUNCTION': func
                })
        return tools
    
    xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_1': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_1, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_2': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_2, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_3': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_3, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_4': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_4, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_5': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_5, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_6': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_6, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_7': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_7, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_8': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_8, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_9': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_9, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_10': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_10, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_11': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_11, 
        'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_12': xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_12
    }
    
    def _convert_functions_to_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _convert_functions_to_tools.__signature__ = _mutmut_signature(xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_orig)
    xǁUnifiedModelInterfaceǁ_convert_functions_to_tools__mutmut_orig.__name__ = 'xǁUnifiedModelInterfaceǁ_convert_functions_to_tools'


# Legacy compatibility class
class LiteLLMInterface(UnifiedModelInterface):
    """
    Legacy compatibility interface that mimics the old LiteLLM interface.
    
    This class provides backward compatibility while using the new provider system.
    """
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_orig(self, model_name: str, drop_params: bool = True, **kwargs):
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
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_1(self, model_name: str, drop_params: bool = False, **kwargs):
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
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_2(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = None
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_3(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop(None, None)
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_4(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop(None)
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_5(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', )
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_6(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('XXapi_keyXX', None)
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_7(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('API_KEY', None)
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_8(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', None)
        
        super().__init__(None, api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_9(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', None)
        
        super().__init__(model_name, None, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_10(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', None)
        
        super().__init__(api_key, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_11(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', None)
        
        super().__init__(model_name, **kwargs)
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_12(self, model_name: str, drop_params: bool = True, **kwargs):
        """
        Initialize with LiteLLM-compatible parameters.
        
        Args:
            model_name: Name of the model to use
            drop_params: Ignored (kept for compatibility)
            **kwargs: Additional configuration
        """
        # Extract API key from various possible sources
        api_key = kwargs.pop('api_key', None)
        
        super().__init__(model_name, api_key, )
        
        # Legacy attributes for backward compatibility
        self.drop_params = drop_params
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_13(self, model_name: str, drop_params: bool = True, **kwargs):
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
        self.drop_params = None
        self.temperature = None
        
    
    def xǁLiteLLMInterfaceǁ__init____mutmut_14(self, model_name: str, drop_params: bool = True, **kwargs):
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
        self.temperature = ""
        
    
    xǁLiteLLMInterfaceǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteLLMInterfaceǁ__init____mutmut_1': xǁLiteLLMInterfaceǁ__init____mutmut_1, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_2': xǁLiteLLMInterfaceǁ__init____mutmut_2, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_3': xǁLiteLLMInterfaceǁ__init____mutmut_3, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_4': xǁLiteLLMInterfaceǁ__init____mutmut_4, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_5': xǁLiteLLMInterfaceǁ__init____mutmut_5, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_6': xǁLiteLLMInterfaceǁ__init____mutmut_6, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_7': xǁLiteLLMInterfaceǁ__init____mutmut_7, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_8': xǁLiteLLMInterfaceǁ__init____mutmut_8, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_9': xǁLiteLLMInterfaceǁ__init____mutmut_9, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_10': xǁLiteLLMInterfaceǁ__init____mutmut_10, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_11': xǁLiteLLMInterfaceǁ__init____mutmut_11, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_12': xǁLiteLLMInterfaceǁ__init____mutmut_12, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_13': xǁLiteLLMInterfaceǁ__init____mutmut_13, 
        'xǁLiteLLMInterfaceǁ__init____mutmut_14': xǁLiteLLMInterfaceǁ__init____mutmut_14
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteLLMInterfaceǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLiteLLMInterfaceǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLiteLLMInterfaceǁ__init____mutmut_orig)
    xǁLiteLLMInterfaceǁ__init____mutmut_orig.__name__ = 'xǁLiteLLMInterfaceǁ__init__'
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_orig(self, kwargs: Dict) -> ProviderResponse:
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
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_1(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = None
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_2(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get(None, [])
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_3(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', None)
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_4(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get([])
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_5(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', )
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_6(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('XXmessagesXX', [])
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_7(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('MESSAGES', [])
        tools = kwargs.get('tools', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_8(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = None
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_9(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get(None, [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_10(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get('tools', None)
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_11(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get([])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_12(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get('tools', )
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_13(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get('XXtoolsXX', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_14(self, kwargs: Dict) -> ProviderResponse:
        """
        Legacy method that mimics LiteLLM's _call_api.
        
        Args:
            kwargs: API call parameters
            
        Returns:
            ProviderResponse: The response from the provider
        """
        messages = kwargs.get('messages', [])
        tools = kwargs.get('TOOLS', [])
        
        # Extract other parameters
        other_params = {k: v for k, v in kwargs.items() 
                       if k not in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_15(self, kwargs: Dict) -> ProviderResponse:
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
        other_params = None
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_16(self, kwargs: Dict) -> ProviderResponse:
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
                       if k in ['model', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_17(self, kwargs: Dict) -> ProviderResponse:
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
                       if k not in ['XXmodelXX', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_18(self, kwargs: Dict) -> ProviderResponse:
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
                       if k not in ['MODEL', 'messages', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_19(self, kwargs: Dict) -> ProviderResponse:
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
                       if k not in ['model', 'XXmessagesXX', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_20(self, kwargs: Dict) -> ProviderResponse:
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
                       if k not in ['model', 'MESSAGES', 'tools']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_21(self, kwargs: Dict) -> ProviderResponse:
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
                       if k not in ['model', 'messages', 'XXtoolsXX']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_22(self, kwargs: Dict) -> ProviderResponse:
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
                       if k not in ['model', 'messages', 'TOOLS']}
        
        return self.provider.generate_response(messages, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_23(self, kwargs: Dict) -> ProviderResponse:
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
        
        return self.provider.generate_response(None, tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_24(self, kwargs: Dict) -> ProviderResponse:
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
        
        return self.provider.generate_response(messages, None, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_25(self, kwargs: Dict) -> ProviderResponse:
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
        
        return self.provider.generate_response(tools, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_26(self, kwargs: Dict) -> ProviderResponse:
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
        
        return self.provider.generate_response(messages, **other_params)
    def xǁLiteLLMInterfaceǁ_call_api__mutmut_27(self, kwargs: Dict) -> ProviderResponse:
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
        
        return self.provider.generate_response(messages, tools, )
    
    xǁLiteLLMInterfaceǁ_call_api__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteLLMInterfaceǁ_call_api__mutmut_1': xǁLiteLLMInterfaceǁ_call_api__mutmut_1, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_2': xǁLiteLLMInterfaceǁ_call_api__mutmut_2, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_3': xǁLiteLLMInterfaceǁ_call_api__mutmut_3, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_4': xǁLiteLLMInterfaceǁ_call_api__mutmut_4, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_5': xǁLiteLLMInterfaceǁ_call_api__mutmut_5, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_6': xǁLiteLLMInterfaceǁ_call_api__mutmut_6, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_7': xǁLiteLLMInterfaceǁ_call_api__mutmut_7, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_8': xǁLiteLLMInterfaceǁ_call_api__mutmut_8, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_9': xǁLiteLLMInterfaceǁ_call_api__mutmut_9, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_10': xǁLiteLLMInterfaceǁ_call_api__mutmut_10, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_11': xǁLiteLLMInterfaceǁ_call_api__mutmut_11, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_12': xǁLiteLLMInterfaceǁ_call_api__mutmut_12, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_13': xǁLiteLLMInterfaceǁ_call_api__mutmut_13, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_14': xǁLiteLLMInterfaceǁ_call_api__mutmut_14, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_15': xǁLiteLLMInterfaceǁ_call_api__mutmut_15, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_16': xǁLiteLLMInterfaceǁ_call_api__mutmut_16, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_17': xǁLiteLLMInterfaceǁ_call_api__mutmut_17, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_18': xǁLiteLLMInterfaceǁ_call_api__mutmut_18, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_19': xǁLiteLLMInterfaceǁ_call_api__mutmut_19, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_20': xǁLiteLLMInterfaceǁ_call_api__mutmut_20, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_21': xǁLiteLLMInterfaceǁ_call_api__mutmut_21, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_22': xǁLiteLLMInterfaceǁ_call_api__mutmut_22, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_23': xǁLiteLLMInterfaceǁ_call_api__mutmut_23, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_24': xǁLiteLLMInterfaceǁ_call_api__mutmut_24, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_25': xǁLiteLLMInterfaceǁ_call_api__mutmut_25, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_26': xǁLiteLLMInterfaceǁ_call_api__mutmut_26, 
        'xǁLiteLLMInterfaceǁ_call_api__mutmut_27': xǁLiteLLMInterfaceǁ_call_api__mutmut_27
    }
    
    def _call_api(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteLLMInterfaceǁ_call_api__mutmut_orig"), object.__getattribute__(self, "xǁLiteLLMInterfaceǁ_call_api__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _call_api.__signature__ = _mutmut_signature(xǁLiteLLMInterfaceǁ_call_api__mutmut_orig)
    xǁLiteLLMInterfaceǁ_call_api__mutmut_orig.__name__ = 'xǁLiteLLMInterfaceǁ_call_api'


def x_create_model_interface__mutmut_orig(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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


def x_create_model_interface__mutmut_1(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(None, api_key, provider=provider, **kwargs)


def x_create_model_interface__mutmut_2(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(model_name, None, provider=provider, **kwargs)


def x_create_model_interface__mutmut_3(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(model_name, api_key, provider=None, **kwargs)


def x_create_model_interface__mutmut_4(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(api_key, provider=provider, **kwargs)


def x_create_model_interface__mutmut_5(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(model_name, provider=provider, **kwargs)


def x_create_model_interface__mutmut_6(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(model_name, api_key, **kwargs)


def x_create_model_interface__mutmut_7(model_name: str, api_key: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> ModelInterface:
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
    return UnifiedModelInterface(model_name, api_key, provider=provider, )

x_create_model_interface__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_model_interface__mutmut_1': x_create_model_interface__mutmut_1, 
    'x_create_model_interface__mutmut_2': x_create_model_interface__mutmut_2, 
    'x_create_model_interface__mutmut_3': x_create_model_interface__mutmut_3, 
    'x_create_model_interface__mutmut_4': x_create_model_interface__mutmut_4, 
    'x_create_model_interface__mutmut_5': x_create_model_interface__mutmut_5, 
    'x_create_model_interface__mutmut_6': x_create_model_interface__mutmut_6, 
    'x_create_model_interface__mutmut_7': x_create_model_interface__mutmut_7
}

def create_model_interface(*args, **kwargs):
    result = _mutmut_trampoline(x_create_model_interface__mutmut_orig, x_create_model_interface__mutmut_mutants, args, kwargs)
    return result 

create_model_interface.__signature__ = _mutmut_signature(x_create_model_interface__mutmut_orig)
x_create_model_interface__mutmut_orig.__name__ = 'x_create_model_interface'


def x_create_legacy_interface__mutmut_orig(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
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


def x_create_legacy_interface__mutmut_1(model_name: str, drop_params: bool = False, **kwargs) -> LiteLLMInterface:
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


def x_create_legacy_interface__mutmut_2(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
    """
    Create a legacy-compatible interface.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters (ignored)
        **kwargs: Additional configuration
        
    Returns:
        LiteLLMInterface: Legacy-compatible interface
    """
    return LiteLLMInterface(None, drop_params, **kwargs)


def x_create_legacy_interface__mutmut_3(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
    """
    Create a legacy-compatible interface.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters (ignored)
        **kwargs: Additional configuration
        
    Returns:
        LiteLLMInterface: Legacy-compatible interface
    """
    return LiteLLMInterface(model_name, None, **kwargs)


def x_create_legacy_interface__mutmut_4(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
    """
    Create a legacy-compatible interface.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters (ignored)
        **kwargs: Additional configuration
        
    Returns:
        LiteLLMInterface: Legacy-compatible interface
    """
    return LiteLLMInterface(drop_params, **kwargs)


def x_create_legacy_interface__mutmut_5(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
    """
    Create a legacy-compatible interface.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters (ignored)
        **kwargs: Additional configuration
        
    Returns:
        LiteLLMInterface: Legacy-compatible interface
    """
    return LiteLLMInterface(model_name, **kwargs)


def x_create_legacy_interface__mutmut_6(model_name: str, drop_params: bool = True, **kwargs) -> LiteLLMInterface:
    """
    Create a legacy-compatible interface.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters (ignored)
        **kwargs: Additional configuration
        
    Returns:
        LiteLLMInterface: Legacy-compatible interface
    """
    return LiteLLMInterface(model_name, drop_params, )

x_create_legacy_interface__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_legacy_interface__mutmut_1': x_create_legacy_interface__mutmut_1, 
    'x_create_legacy_interface__mutmut_2': x_create_legacy_interface__mutmut_2, 
    'x_create_legacy_interface__mutmut_3': x_create_legacy_interface__mutmut_3, 
    'x_create_legacy_interface__mutmut_4': x_create_legacy_interface__mutmut_4, 
    'x_create_legacy_interface__mutmut_5': x_create_legacy_interface__mutmut_5, 
    'x_create_legacy_interface__mutmut_6': x_create_legacy_interface__mutmut_6
}

def create_legacy_interface(*args, **kwargs):
    result = _mutmut_trampoline(x_create_legacy_interface__mutmut_orig, x_create_legacy_interface__mutmut_mutants, args, kwargs)
    return result 

create_legacy_interface.__signature__ = _mutmut_signature(x_create_legacy_interface__mutmut_orig)
x_create_legacy_interface__mutmut_orig.__name__ = 'x_create_legacy_interface'