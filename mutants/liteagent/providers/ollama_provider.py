"""
Ollama provider implementation for LiteAgent.

This provider uses the official Ollama Python client library for local model inference.
"""

import os
import time
import json
from typing import Any, Dict, List, Optional

try:
    from ollama import Client
except ImportError:
    raise ImportError("Ollama library not installed. Install with: pip install ollama")

from .base import ProviderInterface, ProviderResponse, ToolCall
from ..utils import logger
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


class OllamaProvider(ProviderInterface):
    """Ollama provider using the official Ollama client library."""
    
    def xǁOllamaProviderǁ__init____mutmut_orig(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_1(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = None
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_2(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get(None, 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_3(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', None)
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_4(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_5(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', )
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_6(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('XXhostXX', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_7(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('HOST', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_8(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'XXhttp://localhost:11434XX')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_9(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'HTTP://LOCALHOST:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_10(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = None  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_11(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get(None, 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_12(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', None)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_13(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get(120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_14(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', )  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_15(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('XXtimeoutXX', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_16(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('TIMEOUT', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_17(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 121)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_18(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(None, api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_19(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, None, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_20(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(api_key, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_21(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, **kwargs)
        
    
    def xǁOllamaProviderǁ__init____mutmut_22(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Name of the Ollama model (e.g., 'llama3.1:8b')
            api_key: Not used for Ollama (local models)
            **kwargs: Additional configuration
                - host: Ollama server host (default: http://localhost:11434)
                - timeout: Request timeout in seconds
        """
        self.host = kwargs.get('host', 'http://localhost:11434')
        self.timeout = kwargs.get('timeout', 120)  # Ollama can be slow for large models
        
        super().__init__(model_name, api_key, )
        
    
    xǁOllamaProviderǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ__init____mutmut_1': xǁOllamaProviderǁ__init____mutmut_1, 
        'xǁOllamaProviderǁ__init____mutmut_2': xǁOllamaProviderǁ__init____mutmut_2, 
        'xǁOllamaProviderǁ__init____mutmut_3': xǁOllamaProviderǁ__init____mutmut_3, 
        'xǁOllamaProviderǁ__init____mutmut_4': xǁOllamaProviderǁ__init____mutmut_4, 
        'xǁOllamaProviderǁ__init____mutmut_5': xǁOllamaProviderǁ__init____mutmut_5, 
        'xǁOllamaProviderǁ__init____mutmut_6': xǁOllamaProviderǁ__init____mutmut_6, 
        'xǁOllamaProviderǁ__init____mutmut_7': xǁOllamaProviderǁ__init____mutmut_7, 
        'xǁOllamaProviderǁ__init____mutmut_8': xǁOllamaProviderǁ__init____mutmut_8, 
        'xǁOllamaProviderǁ__init____mutmut_9': xǁOllamaProviderǁ__init____mutmut_9, 
        'xǁOllamaProviderǁ__init____mutmut_10': xǁOllamaProviderǁ__init____mutmut_10, 
        'xǁOllamaProviderǁ__init____mutmut_11': xǁOllamaProviderǁ__init____mutmut_11, 
        'xǁOllamaProviderǁ__init____mutmut_12': xǁOllamaProviderǁ__init____mutmut_12, 
        'xǁOllamaProviderǁ__init____mutmut_13': xǁOllamaProviderǁ__init____mutmut_13, 
        'xǁOllamaProviderǁ__init____mutmut_14': xǁOllamaProviderǁ__init____mutmut_14, 
        'xǁOllamaProviderǁ__init____mutmut_15': xǁOllamaProviderǁ__init____mutmut_15, 
        'xǁOllamaProviderǁ__init____mutmut_16': xǁOllamaProviderǁ__init____mutmut_16, 
        'xǁOllamaProviderǁ__init____mutmut_17': xǁOllamaProviderǁ__init____mutmut_17, 
        'xǁOllamaProviderǁ__init____mutmut_18': xǁOllamaProviderǁ__init____mutmut_18, 
        'xǁOllamaProviderǁ__init____mutmut_19': xǁOllamaProviderǁ__init____mutmut_19, 
        'xǁOllamaProviderǁ__init____mutmut_20': xǁOllamaProviderǁ__init____mutmut_20, 
        'xǁOllamaProviderǁ__init____mutmut_21': xǁOllamaProviderǁ__init____mutmut_21, 
        'xǁOllamaProviderǁ__init____mutmut_22': xǁOllamaProviderǁ__init____mutmut_22
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOllamaProviderǁ__init____mutmut_orig)
    xǁOllamaProviderǁ__init____mutmut_orig.__name__ = 'xǁOllamaProviderǁ__init__'
    def xǁOllamaProviderǁ_get_provider_name__mutmut_orig(self) -> str:
        """Return the provider name."""
        return 'ollama'
        
    def xǁOllamaProviderǁ_get_provider_name__mutmut_1(self) -> str:
        """Return the provider name."""
        return 'XXollamaXX'
        
    def xǁOllamaProviderǁ_get_provider_name__mutmut_2(self) -> str:
        """Return the provider name."""
        return 'OLLAMA'
        
    
    xǁOllamaProviderǁ_get_provider_name__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_get_provider_name__mutmut_1': xǁOllamaProviderǁ_get_provider_name__mutmut_1, 
        'xǁOllamaProviderǁ_get_provider_name__mutmut_2': xǁOllamaProviderǁ_get_provider_name__mutmut_2
    }
    
    def _get_provider_name(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_get_provider_name__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_get_provider_name__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_provider_name.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_get_provider_name__mutmut_orig)
    xǁOllamaProviderǁ_get_provider_name__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_get_provider_name'
    def xǁOllamaProviderǁ_setup_client__mutmut_orig(self) -> None:
        """Setup the Ollama client."""
        self.client = Client(host=self.host)
        
    def xǁOllamaProviderǁ_setup_client__mutmut_1(self) -> None:
        """Setup the Ollama client."""
        self.client = None
        
    def xǁOllamaProviderǁ_setup_client__mutmut_2(self) -> None:
        """Setup the Ollama client."""
        self.client = Client(host=None)
        
    
    xǁOllamaProviderǁ_setup_client__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_setup_client__mutmut_1': xǁOllamaProviderǁ_setup_client__mutmut_1, 
        'xǁOllamaProviderǁ_setup_client__mutmut_2': xǁOllamaProviderǁ_setup_client__mutmut_2
    }
    
    def _setup_client(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_setup_client__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_setup_client__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _setup_client.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_setup_client__mutmut_orig)
    xǁOllamaProviderǁ_setup_client__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_setup_client'
    def xǁOllamaProviderǁgenerate_response__mutmut_orig(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_1(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = None
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_2(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(None, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_3(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, None)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_4(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_5(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, )
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_6(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = None
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_7(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(None)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_8(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = None
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_9(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'XXmodelXX': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_10(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'MODEL': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_11(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'XXmessagesXX': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_12(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'MESSAGES': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_13(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'XXstreamXX': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_14(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'STREAM': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_15(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': True,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_16(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = None
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_17(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'XXtemperatureXX' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_18(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'TEMPERATURE' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_19(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' not in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_20(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = None
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_21(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['XXtemperatureXX'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_22(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['TEMPERATURE'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_23(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['XXtemperatureXX']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_24(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['TEMPERATURE']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_25(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'XXtop_pXX' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_26(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'TOP_P' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_27(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' not in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_28(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = None
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_29(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['XXtop_pXX'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_30(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['TOP_P'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_31(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['XXtop_pXX']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_32(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['TOP_P']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_33(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'XXtop_kXX' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_34(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'TOP_K' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_35(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' not in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_36(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = None
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_37(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['XXtop_kXX'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_38(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['TOP_K'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_39(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['XXtop_kXX']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_40(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['TOP_K']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_41(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = None
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_42(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['XXoptionsXX'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_43(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['OPTIONS'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_44(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools or self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_45(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = None
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_46(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['XXtoolsXX'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_47(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['TOOLS'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_48(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(None)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_49(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(None)
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_50(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(None, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_51(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=None)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_52(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_53(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, )}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_54(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=3)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_55(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = None
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_56(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = None
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_57(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(None, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_58(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, None)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_59(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_60(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, )
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_61(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = None
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_62(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() + start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_63(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(None, elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_64(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, None)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_65(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(elapsed_time)
        
        return provider_response
            
    def xǁOllamaProviderǁgenerate_response__mutmut_66(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Ollama's chat API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Prepare request parameters
        # Preprocess messages to convert tool call arguments from strings to dicts for Ollama
        processed_messages = self._preprocess_messages_for_ollama(messages)
        
        request_params = {
            'model': self.model_name,
            'messages': processed_messages,
            'stream': False,  # We want complete responses
        }
        
        # Add optional parameters
        options = {}
        if 'temperature' in kwargs:
            options['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            options['top_p'] = kwargs['top_p']
        if 'top_k' in kwargs:
            options['top_k'] = kwargs['top_k']
            
        if options:
            request_params['options'] = options
            
        # Handle tools for Ollama using native tool calling
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
                
        # Debug: Log the processed messages before API call
        logger.debug(f"Ollama API call with processed messages: {json.dumps(processed_messages, indent=2)}")
        
        # Make the API call
        response = self.client.chat(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response, tools)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, )
        
        return provider_response
            
    
    xǁOllamaProviderǁgenerate_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁgenerate_response__mutmut_1': xǁOllamaProviderǁgenerate_response__mutmut_1, 
        'xǁOllamaProviderǁgenerate_response__mutmut_2': xǁOllamaProviderǁgenerate_response__mutmut_2, 
        'xǁOllamaProviderǁgenerate_response__mutmut_3': xǁOllamaProviderǁgenerate_response__mutmut_3, 
        'xǁOllamaProviderǁgenerate_response__mutmut_4': xǁOllamaProviderǁgenerate_response__mutmut_4, 
        'xǁOllamaProviderǁgenerate_response__mutmut_5': xǁOllamaProviderǁgenerate_response__mutmut_5, 
        'xǁOllamaProviderǁgenerate_response__mutmut_6': xǁOllamaProviderǁgenerate_response__mutmut_6, 
        'xǁOllamaProviderǁgenerate_response__mutmut_7': xǁOllamaProviderǁgenerate_response__mutmut_7, 
        'xǁOllamaProviderǁgenerate_response__mutmut_8': xǁOllamaProviderǁgenerate_response__mutmut_8, 
        'xǁOllamaProviderǁgenerate_response__mutmut_9': xǁOllamaProviderǁgenerate_response__mutmut_9, 
        'xǁOllamaProviderǁgenerate_response__mutmut_10': xǁOllamaProviderǁgenerate_response__mutmut_10, 
        'xǁOllamaProviderǁgenerate_response__mutmut_11': xǁOllamaProviderǁgenerate_response__mutmut_11, 
        'xǁOllamaProviderǁgenerate_response__mutmut_12': xǁOllamaProviderǁgenerate_response__mutmut_12, 
        'xǁOllamaProviderǁgenerate_response__mutmut_13': xǁOllamaProviderǁgenerate_response__mutmut_13, 
        'xǁOllamaProviderǁgenerate_response__mutmut_14': xǁOllamaProviderǁgenerate_response__mutmut_14, 
        'xǁOllamaProviderǁgenerate_response__mutmut_15': xǁOllamaProviderǁgenerate_response__mutmut_15, 
        'xǁOllamaProviderǁgenerate_response__mutmut_16': xǁOllamaProviderǁgenerate_response__mutmut_16, 
        'xǁOllamaProviderǁgenerate_response__mutmut_17': xǁOllamaProviderǁgenerate_response__mutmut_17, 
        'xǁOllamaProviderǁgenerate_response__mutmut_18': xǁOllamaProviderǁgenerate_response__mutmut_18, 
        'xǁOllamaProviderǁgenerate_response__mutmut_19': xǁOllamaProviderǁgenerate_response__mutmut_19, 
        'xǁOllamaProviderǁgenerate_response__mutmut_20': xǁOllamaProviderǁgenerate_response__mutmut_20, 
        'xǁOllamaProviderǁgenerate_response__mutmut_21': xǁOllamaProviderǁgenerate_response__mutmut_21, 
        'xǁOllamaProviderǁgenerate_response__mutmut_22': xǁOllamaProviderǁgenerate_response__mutmut_22, 
        'xǁOllamaProviderǁgenerate_response__mutmut_23': xǁOllamaProviderǁgenerate_response__mutmut_23, 
        'xǁOllamaProviderǁgenerate_response__mutmut_24': xǁOllamaProviderǁgenerate_response__mutmut_24, 
        'xǁOllamaProviderǁgenerate_response__mutmut_25': xǁOllamaProviderǁgenerate_response__mutmut_25, 
        'xǁOllamaProviderǁgenerate_response__mutmut_26': xǁOllamaProviderǁgenerate_response__mutmut_26, 
        'xǁOllamaProviderǁgenerate_response__mutmut_27': xǁOllamaProviderǁgenerate_response__mutmut_27, 
        'xǁOllamaProviderǁgenerate_response__mutmut_28': xǁOllamaProviderǁgenerate_response__mutmut_28, 
        'xǁOllamaProviderǁgenerate_response__mutmut_29': xǁOllamaProviderǁgenerate_response__mutmut_29, 
        'xǁOllamaProviderǁgenerate_response__mutmut_30': xǁOllamaProviderǁgenerate_response__mutmut_30, 
        'xǁOllamaProviderǁgenerate_response__mutmut_31': xǁOllamaProviderǁgenerate_response__mutmut_31, 
        'xǁOllamaProviderǁgenerate_response__mutmut_32': xǁOllamaProviderǁgenerate_response__mutmut_32, 
        'xǁOllamaProviderǁgenerate_response__mutmut_33': xǁOllamaProviderǁgenerate_response__mutmut_33, 
        'xǁOllamaProviderǁgenerate_response__mutmut_34': xǁOllamaProviderǁgenerate_response__mutmut_34, 
        'xǁOllamaProviderǁgenerate_response__mutmut_35': xǁOllamaProviderǁgenerate_response__mutmut_35, 
        'xǁOllamaProviderǁgenerate_response__mutmut_36': xǁOllamaProviderǁgenerate_response__mutmut_36, 
        'xǁOllamaProviderǁgenerate_response__mutmut_37': xǁOllamaProviderǁgenerate_response__mutmut_37, 
        'xǁOllamaProviderǁgenerate_response__mutmut_38': xǁOllamaProviderǁgenerate_response__mutmut_38, 
        'xǁOllamaProviderǁgenerate_response__mutmut_39': xǁOllamaProviderǁgenerate_response__mutmut_39, 
        'xǁOllamaProviderǁgenerate_response__mutmut_40': xǁOllamaProviderǁgenerate_response__mutmut_40, 
        'xǁOllamaProviderǁgenerate_response__mutmut_41': xǁOllamaProviderǁgenerate_response__mutmut_41, 
        'xǁOllamaProviderǁgenerate_response__mutmut_42': xǁOllamaProviderǁgenerate_response__mutmut_42, 
        'xǁOllamaProviderǁgenerate_response__mutmut_43': xǁOllamaProviderǁgenerate_response__mutmut_43, 
        'xǁOllamaProviderǁgenerate_response__mutmut_44': xǁOllamaProviderǁgenerate_response__mutmut_44, 
        'xǁOllamaProviderǁgenerate_response__mutmut_45': xǁOllamaProviderǁgenerate_response__mutmut_45, 
        'xǁOllamaProviderǁgenerate_response__mutmut_46': xǁOllamaProviderǁgenerate_response__mutmut_46, 
        'xǁOllamaProviderǁgenerate_response__mutmut_47': xǁOllamaProviderǁgenerate_response__mutmut_47, 
        'xǁOllamaProviderǁgenerate_response__mutmut_48': xǁOllamaProviderǁgenerate_response__mutmut_48, 
        'xǁOllamaProviderǁgenerate_response__mutmut_49': xǁOllamaProviderǁgenerate_response__mutmut_49, 
        'xǁOllamaProviderǁgenerate_response__mutmut_50': xǁOllamaProviderǁgenerate_response__mutmut_50, 
        'xǁOllamaProviderǁgenerate_response__mutmut_51': xǁOllamaProviderǁgenerate_response__mutmut_51, 
        'xǁOllamaProviderǁgenerate_response__mutmut_52': xǁOllamaProviderǁgenerate_response__mutmut_52, 
        'xǁOllamaProviderǁgenerate_response__mutmut_53': xǁOllamaProviderǁgenerate_response__mutmut_53, 
        'xǁOllamaProviderǁgenerate_response__mutmut_54': xǁOllamaProviderǁgenerate_response__mutmut_54, 
        'xǁOllamaProviderǁgenerate_response__mutmut_55': xǁOllamaProviderǁgenerate_response__mutmut_55, 
        'xǁOllamaProviderǁgenerate_response__mutmut_56': xǁOllamaProviderǁgenerate_response__mutmut_56, 
        'xǁOllamaProviderǁgenerate_response__mutmut_57': xǁOllamaProviderǁgenerate_response__mutmut_57, 
        'xǁOllamaProviderǁgenerate_response__mutmut_58': xǁOllamaProviderǁgenerate_response__mutmut_58, 
        'xǁOllamaProviderǁgenerate_response__mutmut_59': xǁOllamaProviderǁgenerate_response__mutmut_59, 
        'xǁOllamaProviderǁgenerate_response__mutmut_60': xǁOllamaProviderǁgenerate_response__mutmut_60, 
        'xǁOllamaProviderǁgenerate_response__mutmut_61': xǁOllamaProviderǁgenerate_response__mutmut_61, 
        'xǁOllamaProviderǁgenerate_response__mutmut_62': xǁOllamaProviderǁgenerate_response__mutmut_62, 
        'xǁOllamaProviderǁgenerate_response__mutmut_63': xǁOllamaProviderǁgenerate_response__mutmut_63, 
        'xǁOllamaProviderǁgenerate_response__mutmut_64': xǁOllamaProviderǁgenerate_response__mutmut_64, 
        'xǁOllamaProviderǁgenerate_response__mutmut_65': xǁOllamaProviderǁgenerate_response__mutmut_65, 
        'xǁOllamaProviderǁgenerate_response__mutmut_66': xǁOllamaProviderǁgenerate_response__mutmut_66
    }
    
    def generate_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁgenerate_response__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁgenerate_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_response.__signature__ = _mutmut_signature(xǁOllamaProviderǁgenerate_response__mutmut_orig)
    xǁOllamaProviderǁgenerate_response__mutmut_orig.__name__ = 'xǁOllamaProviderǁgenerate_response'
    def xǁOllamaProviderǁ_supports_native_tools__mutmut_orig(self) -> bool:
        """Check if the model supports native tool calling."""
        # Modern Ollama supports tool calling for most models
        return True
        
    def xǁOllamaProviderǁ_supports_native_tools__mutmut_1(self) -> bool:
        """Check if the model supports native tool calling."""
        # Modern Ollama supports tool calling for most models
        return False
        
    
    xǁOllamaProviderǁ_supports_native_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_supports_native_tools__mutmut_1': xǁOllamaProviderǁ_supports_native_tools__mutmut_1
    }
    
    def _supports_native_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_supports_native_tools__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_supports_native_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _supports_native_tools.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_supports_native_tools__mutmut_orig)
    xǁOllamaProviderǁ_supports_native_tools__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_supports_native_tools'
    def xǁOllamaProviderǁ_convert_tools__mutmut_orig(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_1(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = None
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_2(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'XXfunctionXX' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_3(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'FUNCTION' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_4(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' not in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_5(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append(None)
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_6(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'XXtypeXX': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_7(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'TYPE': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_8(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'XXfunctionXX',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_9(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'FUNCTION',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_10(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'XXfunctionXX': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_11(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'FUNCTION': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_12(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['XXfunctionXX']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_13(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['FUNCTION']
                })
            else:
                # Already in correct format
                ollama_tools.append(tool)
                
        return ollama_tools
        
    def xǁOllamaProviderǁ_convert_tools__mutmut_14(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Ollama format."""
        ollama_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Ollama-style
                ollama_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                ollama_tools.append(None)
                
        return ollama_tools
        
    
    xǁOllamaProviderǁ_convert_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_convert_tools__mutmut_1': xǁOllamaProviderǁ_convert_tools__mutmut_1, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_2': xǁOllamaProviderǁ_convert_tools__mutmut_2, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_3': xǁOllamaProviderǁ_convert_tools__mutmut_3, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_4': xǁOllamaProviderǁ_convert_tools__mutmut_4, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_5': xǁOllamaProviderǁ_convert_tools__mutmut_5, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_6': xǁOllamaProviderǁ_convert_tools__mutmut_6, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_7': xǁOllamaProviderǁ_convert_tools__mutmut_7, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_8': xǁOllamaProviderǁ_convert_tools__mutmut_8, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_9': xǁOllamaProviderǁ_convert_tools__mutmut_9, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_10': xǁOllamaProviderǁ_convert_tools__mutmut_10, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_11': xǁOllamaProviderǁ_convert_tools__mutmut_11, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_12': xǁOllamaProviderǁ_convert_tools__mutmut_12, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_13': xǁOllamaProviderǁ_convert_tools__mutmut_13, 
        'xǁOllamaProviderǁ_convert_tools__mutmut_14': xǁOllamaProviderǁ_convert_tools__mutmut_14
    }
    
    def _convert_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_convert_tools__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_convert_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _convert_tools.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_convert_tools__mutmut_orig)
    xǁOllamaProviderǁ_convert_tools__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_convert_tools'
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_orig(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_1(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = None
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_2(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = None
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_3(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get(None, tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_4(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', None)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_5(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get(tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_6(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', )
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_7(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('XXfunctionXX', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_8(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('FUNCTION', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_9(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = None
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_10(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get(None, 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_11(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', None)
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_12(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_13(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', )
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_14(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('XXnameXX', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_15(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('NAME', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_16(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'XXunknownXX')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_17(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'UNKNOWN')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_18(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = None
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_19(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get(None, 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_20(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', None)
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_21(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_22(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', )
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_23(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('XXdescriptionXX', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_24(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('DESCRIPTION', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_25(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'XXNo description availableXX')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_26(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'no description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_27(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'NO DESCRIPTION AVAILABLE')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_28(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = None
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_29(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get(None, {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_30(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', None)
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_31(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get({})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_32(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', )
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_33(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('XXparametersXX', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_34(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('PARAMETERS', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_35(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = None
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_36(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(None, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_37(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=None)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_38(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_39(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, )}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_40(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=3)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_41(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(None)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_42(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = None
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_43(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(None)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_44(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(None).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_45(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(11).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_46(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = None
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_47(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages or modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_48(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[1]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_49(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['XXroleXX'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_50(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['ROLE'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_51(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] != 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_52(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'XXsystemXX':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_53(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'SYSTEM':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_54(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] = tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_55(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] -= tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_56(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[1]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_57(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['XXcontentXX'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_58(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['CONTENT'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_59(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(None, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_60(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, None)
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_61(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert({'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_62(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, )
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_63(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(1, {'role': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_64(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'XXroleXX': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_65(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'ROLE': 'system', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_66(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'XXsystemXX', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_67(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'SYSTEM', 'content': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_68(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'XXcontentXX': tool_prompt})
            
        return modified_messages
    def xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_69(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Embed tool definitions in the system prompt for models without native tool support."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in tools:
            func = tool.get('function', tool)
            name = func.get('name', 'unknown')
            description = func.get('description', 'No description available')
            parameters = func.get('parameters', {})
            
            tool_desc = f"Tool: {name}\nDescription: {description}\nParameters: {json.dumps(parameters, indent=2)}"
            tool_descriptions.append(tool_desc)
            
        tool_prompt = f"""
You have access to the following tools. To use a tool, respond with a JSON object in this exact format:
{{"tool_call": {{"name": "tool_name", "arguments": {{"param1": "value1", "param2": "value2"}}}}}}

Available tools:
{chr(10).join(tool_descriptions)}

If you don't need to use any tools, respond normally without the JSON format.
"""
        
        # Add tool prompt to system message or create one
        modified_messages = messages.copy()
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0]['content'] += tool_prompt
        else:
            modified_messages.insert(0, {'role': 'system', 'CONTENT': tool_prompt})
            
        return modified_messages
    
    xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_1': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_1, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_2': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_2, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_3': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_3, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_4': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_4, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_5': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_5, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_6': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_6, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_7': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_7, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_8': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_8, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_9': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_9, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_10': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_10, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_11': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_11, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_12': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_12, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_13': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_13, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_14': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_14, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_15': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_15, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_16': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_16, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_17': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_17, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_18': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_18, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_19': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_19, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_20': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_20, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_21': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_21, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_22': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_22, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_23': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_23, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_24': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_24, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_25': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_25, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_26': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_26, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_27': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_27, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_28': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_28, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_29': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_29, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_30': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_30, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_31': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_31, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_32': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_32, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_33': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_33, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_34': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_34, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_35': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_35, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_36': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_36, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_37': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_37, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_38': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_38, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_39': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_39, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_40': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_40, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_41': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_41, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_42': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_42, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_43': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_43, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_44': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_44, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_45': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_45, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_46': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_46, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_47': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_47, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_48': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_48, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_49': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_49, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_50': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_50, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_51': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_51, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_52': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_52, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_53': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_53, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_54': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_54, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_55': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_55, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_56': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_56, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_57': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_57, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_58': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_58, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_59': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_59, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_60': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_60, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_61': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_61, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_62': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_62, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_63': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_63, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_64': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_64, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_65': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_65, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_66': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_66, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_67': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_67, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_68': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_68, 
        'xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_69': xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_69
    }
    
    def _embed_tools_in_prompt(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _embed_tools_in_prompt.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_orig)
    xǁOllamaProviderǁ_embed_tools_in_prompt__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_embed_tools_in_prompt'
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_orig(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_1(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = None
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_2(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = None
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_3(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(None)
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_4(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(None))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_5(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message or processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_6(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'XXtool_callsXX' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_7(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'TOOL_CALLS' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_8(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' not in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_9(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['XXtool_callsXX']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_10(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['TOOL_CALLS']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_11(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['XXtool_callsXX']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_12(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['TOOL_CALLS']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_13(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call or 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_14(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'XXfunctionXX' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_15(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'FUNCTION' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_16(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' not in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_17(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'XXargumentsXX' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_18(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'ARGUMENTS' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_19(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' not in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_20(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['XXfunctionXX']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_21(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['FUNCTION']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_22(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = None
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_23(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['XXfunctionXX']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_24(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['FUNCTION']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_25(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['XXargumentsXX']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_26(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['ARGUMENTS']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_27(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = None
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_28(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(None)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_29(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = None
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_30(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['XXfunctionXX']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_31(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['FUNCTION']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_32(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['XXargumentsXX'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_33(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['ARGUMENTS'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_34(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(None)
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_35(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(None)
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_36(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = None
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_37(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['XXfunctionXX']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_38(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['FUNCTION']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_39(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['XXargumentsXX'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_40(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['ARGUMENTS'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_41(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_42(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(None)
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_43(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(None)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_44(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = None
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_45(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['XXfunctionXX']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_46(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['FUNCTION']['arguments'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_47(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['XXargumentsXX'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_48(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['ARGUMENTS'] = {}
            
            processed_messages.append(processed_message)
        
        return processed_messages
        
    
    def xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_49(self, messages: List[Dict]) -> List[Dict]:
        """
        Preprocess messages to ensure tool call arguments are dicts for Ollama client.
        The memory stores arguments as JSON strings, but Ollama expects dicts.
        """
        processed_messages = []
        
        for message in messages:
            # Deep copy the message to avoid modifying the original
            processed_message = json.loads(json.dumps(message))
            
            # Check if this message has tool calls
            if 'tool_calls' in processed_message and processed_message['tool_calls']:
                for tool_call in processed_message['tool_calls']:
                    # Convert arguments from string to dict if needed
                    if 'function' in tool_call and 'arguments' in tool_call['function']:
                        arguments = tool_call['function']['arguments']
                        if isinstance(arguments, str):
                            try:
                                # Parse JSON string to dict
                                parsed_args = json.loads(arguments)
                                tool_call['function']['arguments'] = parsed_args
                                logger.debug(f"Converted string arguments to dict: {arguments} -> {parsed_args}")
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse tool call arguments '{arguments}': {e}")
                                # Keep as empty dict if parsing fails
                                tool_call['function']['arguments'] = {}
                        elif not isinstance(arguments, dict):
                            # Handle any other non-dict types
                            logger.warning(f"Tool call arguments not string or dict: {type(arguments)} -> {arguments}")
                            tool_call['function']['arguments'] = {}
            
            processed_messages.append(None)
        
        return processed_messages
        
    
    xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_1': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_1, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_2': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_2, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_3': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_3, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_4': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_4, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_5': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_5, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_6': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_6, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_7': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_7, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_8': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_8, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_9': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_9, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_10': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_10, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_11': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_11, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_12': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_12, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_13': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_13, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_14': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_14, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_15': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_15, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_16': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_16, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_17': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_17, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_18': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_18, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_19': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_19, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_20': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_20, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_21': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_21, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_22': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_22, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_23': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_23, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_24': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_24, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_25': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_25, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_26': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_26, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_27': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_27, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_28': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_28, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_29': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_29, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_30': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_30, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_31': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_31, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_32': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_32, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_33': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_33, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_34': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_34, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_35': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_35, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_36': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_36, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_37': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_37, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_38': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_38, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_39': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_39, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_40': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_40, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_41': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_41, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_42': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_42, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_43': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_43, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_44': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_44, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_45': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_45, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_46': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_46, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_47': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_47, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_48': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_48, 
        'xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_49': xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_49
    }
    
    def _preprocess_messages_for_ollama(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _preprocess_messages_for_ollama.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_orig)
    xǁOllamaProviderǁ_preprocess_messages_for_ollama__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_preprocess_messages_for_ollama'
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_orig(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_1(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = None
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_2(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if 'XX"tool_call"XX' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_3(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"TOOL_CALL"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_4(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' not in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_5(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = None
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_6(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split(None)
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_7(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('XX\nXX')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_8(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if 'XX"tool_call"XX' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_9(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"TOOL_CALL"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_10(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' not in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_11(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = None
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_12(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(None)
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_13(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'XXtool_callXX' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_14(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'TOOL_CALL' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_15(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' not in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_16(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = None
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_17(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['XXtool_callXX']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_18(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['TOOL_CALL']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_19(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(None)
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_20(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=None,
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_21(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=None,
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_22(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=None
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_23(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_24(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_25(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_26(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get(None, ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_27(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', None),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_28(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get(''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_29(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_30(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('XXnameXX', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_31(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('NAME', ''),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_32(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', 'XXXX'),
                            arguments=call_data.get('arguments', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_33(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get(None, {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_34(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', None)
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_35(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get({})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_36(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('arguments', )
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_37(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('XXargumentsXX', {})
                        ))
                            
        return tool_calls
        
    def xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_38(self, text: str) -> List[ToolCall]:
        """Extract tool calls from text response for non-native tool models."""
        tool_calls = []
        
        # Look for JSON tool call format
        if '"tool_call"' in text:
            lines = text.split('\n')
            for line in lines:
                if '"tool_call"' in line:
                    tool_data = json.loads(line.strip())
                    if 'tool_call' in tool_data:
                        call_data = tool_data['tool_call']
                        tool_calls.append(ToolCall(
                            id=f"ollama_tool_{len(tool_calls)}",
                            name=call_data.get('name', ''),
                            arguments=call_data.get('ARGUMENTS', {})
                        ))
                            
        return tool_calls
        
    
    xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_1': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_1, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_2': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_2, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_3': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_3, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_4': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_4, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_5': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_5, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_6': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_6, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_7': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_7, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_8': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_8, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_9': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_9, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_10': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_10, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_11': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_11, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_12': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_12, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_13': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_13, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_14': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_14, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_15': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_15, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_16': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_16, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_17': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_17, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_18': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_18, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_19': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_19, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_20': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_20, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_21': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_21, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_22': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_22, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_23': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_23, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_24': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_24, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_25': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_25, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_26': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_26, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_27': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_27, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_28': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_28, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_29': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_29, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_30': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_30, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_31': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_31, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_32': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_32, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_33': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_33, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_34': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_34, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_35': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_35, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_36': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_36, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_37': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_37, 
        'xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_38': xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_38
    }
    
    def _extract_tool_calls_from_text(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_tool_calls_from_text.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_orig)
    xǁOllamaProviderǁ_extract_tool_calls_from_text__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_extract_tool_calls_from_text'
    def xǁOllamaProviderǁ_convert_response__mutmut_orig(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_1(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = None
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_2(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get(None, {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_3(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', None)
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_4(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get({})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_5(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', )
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_6(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('XXmessageXX', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_7(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('MESSAGE', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_8(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = None
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_9(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get(None, '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_10(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', None)
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_11(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_12(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', )
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_13(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('XXcontentXX', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_14(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('CONTENT', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_15(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', 'XXXX')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_16(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = None
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_17(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'XXtool_callsXX' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_18(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'TOOL_CALLS' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_19(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' not in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_20(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['XXtool_callsXX']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_21(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['TOOL_CALLS']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_22(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = None
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_23(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['XXfunctionXX']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_24(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['FUNCTION']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_25(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['XXargumentsXX']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_26(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['ARGUMENTS']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_27(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = None
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_28(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(None)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_29(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(None)
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_30(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = None
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_31(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(None)
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_32(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=None,
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_33(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=None,
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_34(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=None
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_35(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_36(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_37(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_38(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get(None, f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_39(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', None),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_40(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get(f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_41(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', ),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_42(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('XXidXX', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_43(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('ID', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_44(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['XXfunctionXX']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_45(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['FUNCTION']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_46(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['XXnameXX'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_47(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['NAME'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_48(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = ""
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_49(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response and 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_50(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'XXprompt_eval_countXX' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_51(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'PROMPT_EVAL_COUNT' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_52(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' not in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_53(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'XXeval_countXX' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_54(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'EVAL_COUNT' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_55(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' not in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_56(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = None
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_57(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get(None, 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_58(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', None)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_59(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get(0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_60(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', )
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_61(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('XXprompt_eval_countXX', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_62(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('PROMPT_EVAL_COUNT', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_63(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 1)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_64(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = None
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_65(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get(None, 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_66(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', None)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_67(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get(0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_68(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', )
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_69(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('XXeval_countXX', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_70(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('EVAL_COUNT', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_71(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 1)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_72(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = None
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_73(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'XXprompt_tokensXX': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_74(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'PROMPT_TOKENS': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_75(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'XXcompletion_tokensXX': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_76(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'COMPLETION_TOKENS': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_77(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'XXtotal_tokensXX': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_78(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'TOTAL_TOKENS': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_79(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens - completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_80(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_81(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=None,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_82(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=None,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_83(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=None,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_84(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=None,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_85(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=None,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_86(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=None
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_87(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_88(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_89(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_90(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_91(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_92(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_93(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_94(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get(None, self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_95(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', None),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_96(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get(self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_97(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', ),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_98(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('XXmodelXX', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_99(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('MODEL', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_100(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get(None, 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_101(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', None)
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_102(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_103(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', )
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_104(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('XXdone_reasonXX', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_105(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('DONE_REASON', 'stop')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_106(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'XXstopXX')
        )
        
    def xǁOllamaProviderǁ_convert_response__mutmut_107(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
        """Convert Ollama response to standardized format."""
        message = response.get('message', {})
        content = message.get('content', '')
        
        # Extract tool calls from native tool calling
        tool_calls = []
        
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                # Parse arguments if they're a JSON string
                arguments = tc['function']['arguments']
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool call arguments: {arguments}")
                        arguments = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get('id', f"ollama_tool_{len(tool_calls)}"),
                    name=tc['function']['name'],
                    arguments=arguments
                ))
            
        # Extract usage info (Ollama provides token counts)
        usage = None
        if 'prompt_eval_count' in response or 'eval_count' in response:
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            usage = {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens,
            }
            
        return ProviderResponse(
            content=content if content else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.get('model', self.model_name),
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.get('done_reason', 'STOP')
        )
        
    
    xǁOllamaProviderǁ_convert_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁ_convert_response__mutmut_1': xǁOllamaProviderǁ_convert_response__mutmut_1, 
        'xǁOllamaProviderǁ_convert_response__mutmut_2': xǁOllamaProviderǁ_convert_response__mutmut_2, 
        'xǁOllamaProviderǁ_convert_response__mutmut_3': xǁOllamaProviderǁ_convert_response__mutmut_3, 
        'xǁOllamaProviderǁ_convert_response__mutmut_4': xǁOllamaProviderǁ_convert_response__mutmut_4, 
        'xǁOllamaProviderǁ_convert_response__mutmut_5': xǁOllamaProviderǁ_convert_response__mutmut_5, 
        'xǁOllamaProviderǁ_convert_response__mutmut_6': xǁOllamaProviderǁ_convert_response__mutmut_6, 
        'xǁOllamaProviderǁ_convert_response__mutmut_7': xǁOllamaProviderǁ_convert_response__mutmut_7, 
        'xǁOllamaProviderǁ_convert_response__mutmut_8': xǁOllamaProviderǁ_convert_response__mutmut_8, 
        'xǁOllamaProviderǁ_convert_response__mutmut_9': xǁOllamaProviderǁ_convert_response__mutmut_9, 
        'xǁOllamaProviderǁ_convert_response__mutmut_10': xǁOllamaProviderǁ_convert_response__mutmut_10, 
        'xǁOllamaProviderǁ_convert_response__mutmut_11': xǁOllamaProviderǁ_convert_response__mutmut_11, 
        'xǁOllamaProviderǁ_convert_response__mutmut_12': xǁOllamaProviderǁ_convert_response__mutmut_12, 
        'xǁOllamaProviderǁ_convert_response__mutmut_13': xǁOllamaProviderǁ_convert_response__mutmut_13, 
        'xǁOllamaProviderǁ_convert_response__mutmut_14': xǁOllamaProviderǁ_convert_response__mutmut_14, 
        'xǁOllamaProviderǁ_convert_response__mutmut_15': xǁOllamaProviderǁ_convert_response__mutmut_15, 
        'xǁOllamaProviderǁ_convert_response__mutmut_16': xǁOllamaProviderǁ_convert_response__mutmut_16, 
        'xǁOllamaProviderǁ_convert_response__mutmut_17': xǁOllamaProviderǁ_convert_response__mutmut_17, 
        'xǁOllamaProviderǁ_convert_response__mutmut_18': xǁOllamaProviderǁ_convert_response__mutmut_18, 
        'xǁOllamaProviderǁ_convert_response__mutmut_19': xǁOllamaProviderǁ_convert_response__mutmut_19, 
        'xǁOllamaProviderǁ_convert_response__mutmut_20': xǁOllamaProviderǁ_convert_response__mutmut_20, 
        'xǁOllamaProviderǁ_convert_response__mutmut_21': xǁOllamaProviderǁ_convert_response__mutmut_21, 
        'xǁOllamaProviderǁ_convert_response__mutmut_22': xǁOllamaProviderǁ_convert_response__mutmut_22, 
        'xǁOllamaProviderǁ_convert_response__mutmut_23': xǁOllamaProviderǁ_convert_response__mutmut_23, 
        'xǁOllamaProviderǁ_convert_response__mutmut_24': xǁOllamaProviderǁ_convert_response__mutmut_24, 
        'xǁOllamaProviderǁ_convert_response__mutmut_25': xǁOllamaProviderǁ_convert_response__mutmut_25, 
        'xǁOllamaProviderǁ_convert_response__mutmut_26': xǁOllamaProviderǁ_convert_response__mutmut_26, 
        'xǁOllamaProviderǁ_convert_response__mutmut_27': xǁOllamaProviderǁ_convert_response__mutmut_27, 
        'xǁOllamaProviderǁ_convert_response__mutmut_28': xǁOllamaProviderǁ_convert_response__mutmut_28, 
        'xǁOllamaProviderǁ_convert_response__mutmut_29': xǁOllamaProviderǁ_convert_response__mutmut_29, 
        'xǁOllamaProviderǁ_convert_response__mutmut_30': xǁOllamaProviderǁ_convert_response__mutmut_30, 
        'xǁOllamaProviderǁ_convert_response__mutmut_31': xǁOllamaProviderǁ_convert_response__mutmut_31, 
        'xǁOllamaProviderǁ_convert_response__mutmut_32': xǁOllamaProviderǁ_convert_response__mutmut_32, 
        'xǁOllamaProviderǁ_convert_response__mutmut_33': xǁOllamaProviderǁ_convert_response__mutmut_33, 
        'xǁOllamaProviderǁ_convert_response__mutmut_34': xǁOllamaProviderǁ_convert_response__mutmut_34, 
        'xǁOllamaProviderǁ_convert_response__mutmut_35': xǁOllamaProviderǁ_convert_response__mutmut_35, 
        'xǁOllamaProviderǁ_convert_response__mutmut_36': xǁOllamaProviderǁ_convert_response__mutmut_36, 
        'xǁOllamaProviderǁ_convert_response__mutmut_37': xǁOllamaProviderǁ_convert_response__mutmut_37, 
        'xǁOllamaProviderǁ_convert_response__mutmut_38': xǁOllamaProviderǁ_convert_response__mutmut_38, 
        'xǁOllamaProviderǁ_convert_response__mutmut_39': xǁOllamaProviderǁ_convert_response__mutmut_39, 
        'xǁOllamaProviderǁ_convert_response__mutmut_40': xǁOllamaProviderǁ_convert_response__mutmut_40, 
        'xǁOllamaProviderǁ_convert_response__mutmut_41': xǁOllamaProviderǁ_convert_response__mutmut_41, 
        'xǁOllamaProviderǁ_convert_response__mutmut_42': xǁOllamaProviderǁ_convert_response__mutmut_42, 
        'xǁOllamaProviderǁ_convert_response__mutmut_43': xǁOllamaProviderǁ_convert_response__mutmut_43, 
        'xǁOllamaProviderǁ_convert_response__mutmut_44': xǁOllamaProviderǁ_convert_response__mutmut_44, 
        'xǁOllamaProviderǁ_convert_response__mutmut_45': xǁOllamaProviderǁ_convert_response__mutmut_45, 
        'xǁOllamaProviderǁ_convert_response__mutmut_46': xǁOllamaProviderǁ_convert_response__mutmut_46, 
        'xǁOllamaProviderǁ_convert_response__mutmut_47': xǁOllamaProviderǁ_convert_response__mutmut_47, 
        'xǁOllamaProviderǁ_convert_response__mutmut_48': xǁOllamaProviderǁ_convert_response__mutmut_48, 
        'xǁOllamaProviderǁ_convert_response__mutmut_49': xǁOllamaProviderǁ_convert_response__mutmut_49, 
        'xǁOllamaProviderǁ_convert_response__mutmut_50': xǁOllamaProviderǁ_convert_response__mutmut_50, 
        'xǁOllamaProviderǁ_convert_response__mutmut_51': xǁOllamaProviderǁ_convert_response__mutmut_51, 
        'xǁOllamaProviderǁ_convert_response__mutmut_52': xǁOllamaProviderǁ_convert_response__mutmut_52, 
        'xǁOllamaProviderǁ_convert_response__mutmut_53': xǁOllamaProviderǁ_convert_response__mutmut_53, 
        'xǁOllamaProviderǁ_convert_response__mutmut_54': xǁOllamaProviderǁ_convert_response__mutmut_54, 
        'xǁOllamaProviderǁ_convert_response__mutmut_55': xǁOllamaProviderǁ_convert_response__mutmut_55, 
        'xǁOllamaProviderǁ_convert_response__mutmut_56': xǁOllamaProviderǁ_convert_response__mutmut_56, 
        'xǁOllamaProviderǁ_convert_response__mutmut_57': xǁOllamaProviderǁ_convert_response__mutmut_57, 
        'xǁOllamaProviderǁ_convert_response__mutmut_58': xǁOllamaProviderǁ_convert_response__mutmut_58, 
        'xǁOllamaProviderǁ_convert_response__mutmut_59': xǁOllamaProviderǁ_convert_response__mutmut_59, 
        'xǁOllamaProviderǁ_convert_response__mutmut_60': xǁOllamaProviderǁ_convert_response__mutmut_60, 
        'xǁOllamaProviderǁ_convert_response__mutmut_61': xǁOllamaProviderǁ_convert_response__mutmut_61, 
        'xǁOllamaProviderǁ_convert_response__mutmut_62': xǁOllamaProviderǁ_convert_response__mutmut_62, 
        'xǁOllamaProviderǁ_convert_response__mutmut_63': xǁOllamaProviderǁ_convert_response__mutmut_63, 
        'xǁOllamaProviderǁ_convert_response__mutmut_64': xǁOllamaProviderǁ_convert_response__mutmut_64, 
        'xǁOllamaProviderǁ_convert_response__mutmut_65': xǁOllamaProviderǁ_convert_response__mutmut_65, 
        'xǁOllamaProviderǁ_convert_response__mutmut_66': xǁOllamaProviderǁ_convert_response__mutmut_66, 
        'xǁOllamaProviderǁ_convert_response__mutmut_67': xǁOllamaProviderǁ_convert_response__mutmut_67, 
        'xǁOllamaProviderǁ_convert_response__mutmut_68': xǁOllamaProviderǁ_convert_response__mutmut_68, 
        'xǁOllamaProviderǁ_convert_response__mutmut_69': xǁOllamaProviderǁ_convert_response__mutmut_69, 
        'xǁOllamaProviderǁ_convert_response__mutmut_70': xǁOllamaProviderǁ_convert_response__mutmut_70, 
        'xǁOllamaProviderǁ_convert_response__mutmut_71': xǁOllamaProviderǁ_convert_response__mutmut_71, 
        'xǁOllamaProviderǁ_convert_response__mutmut_72': xǁOllamaProviderǁ_convert_response__mutmut_72, 
        'xǁOllamaProviderǁ_convert_response__mutmut_73': xǁOllamaProviderǁ_convert_response__mutmut_73, 
        'xǁOllamaProviderǁ_convert_response__mutmut_74': xǁOllamaProviderǁ_convert_response__mutmut_74, 
        'xǁOllamaProviderǁ_convert_response__mutmut_75': xǁOllamaProviderǁ_convert_response__mutmut_75, 
        'xǁOllamaProviderǁ_convert_response__mutmut_76': xǁOllamaProviderǁ_convert_response__mutmut_76, 
        'xǁOllamaProviderǁ_convert_response__mutmut_77': xǁOllamaProviderǁ_convert_response__mutmut_77, 
        'xǁOllamaProviderǁ_convert_response__mutmut_78': xǁOllamaProviderǁ_convert_response__mutmut_78, 
        'xǁOllamaProviderǁ_convert_response__mutmut_79': xǁOllamaProviderǁ_convert_response__mutmut_79, 
        'xǁOllamaProviderǁ_convert_response__mutmut_80': xǁOllamaProviderǁ_convert_response__mutmut_80, 
        'xǁOllamaProviderǁ_convert_response__mutmut_81': xǁOllamaProviderǁ_convert_response__mutmut_81, 
        'xǁOllamaProviderǁ_convert_response__mutmut_82': xǁOllamaProviderǁ_convert_response__mutmut_82, 
        'xǁOllamaProviderǁ_convert_response__mutmut_83': xǁOllamaProviderǁ_convert_response__mutmut_83, 
        'xǁOllamaProviderǁ_convert_response__mutmut_84': xǁOllamaProviderǁ_convert_response__mutmut_84, 
        'xǁOllamaProviderǁ_convert_response__mutmut_85': xǁOllamaProviderǁ_convert_response__mutmut_85, 
        'xǁOllamaProviderǁ_convert_response__mutmut_86': xǁOllamaProviderǁ_convert_response__mutmut_86, 
        'xǁOllamaProviderǁ_convert_response__mutmut_87': xǁOllamaProviderǁ_convert_response__mutmut_87, 
        'xǁOllamaProviderǁ_convert_response__mutmut_88': xǁOllamaProviderǁ_convert_response__mutmut_88, 
        'xǁOllamaProviderǁ_convert_response__mutmut_89': xǁOllamaProviderǁ_convert_response__mutmut_89, 
        'xǁOllamaProviderǁ_convert_response__mutmut_90': xǁOllamaProviderǁ_convert_response__mutmut_90, 
        'xǁOllamaProviderǁ_convert_response__mutmut_91': xǁOllamaProviderǁ_convert_response__mutmut_91, 
        'xǁOllamaProviderǁ_convert_response__mutmut_92': xǁOllamaProviderǁ_convert_response__mutmut_92, 
        'xǁOllamaProviderǁ_convert_response__mutmut_93': xǁOllamaProviderǁ_convert_response__mutmut_93, 
        'xǁOllamaProviderǁ_convert_response__mutmut_94': xǁOllamaProviderǁ_convert_response__mutmut_94, 
        'xǁOllamaProviderǁ_convert_response__mutmut_95': xǁOllamaProviderǁ_convert_response__mutmut_95, 
        'xǁOllamaProviderǁ_convert_response__mutmut_96': xǁOllamaProviderǁ_convert_response__mutmut_96, 
        'xǁOllamaProviderǁ_convert_response__mutmut_97': xǁOllamaProviderǁ_convert_response__mutmut_97, 
        'xǁOllamaProviderǁ_convert_response__mutmut_98': xǁOllamaProviderǁ_convert_response__mutmut_98, 
        'xǁOllamaProviderǁ_convert_response__mutmut_99': xǁOllamaProviderǁ_convert_response__mutmut_99, 
        'xǁOllamaProviderǁ_convert_response__mutmut_100': xǁOllamaProviderǁ_convert_response__mutmut_100, 
        'xǁOllamaProviderǁ_convert_response__mutmut_101': xǁOllamaProviderǁ_convert_response__mutmut_101, 
        'xǁOllamaProviderǁ_convert_response__mutmut_102': xǁOllamaProviderǁ_convert_response__mutmut_102, 
        'xǁOllamaProviderǁ_convert_response__mutmut_103': xǁOllamaProviderǁ_convert_response__mutmut_103, 
        'xǁOllamaProviderǁ_convert_response__mutmut_104': xǁOllamaProviderǁ_convert_response__mutmut_104, 
        'xǁOllamaProviderǁ_convert_response__mutmut_105': xǁOllamaProviderǁ_convert_response__mutmut_105, 
        'xǁOllamaProviderǁ_convert_response__mutmut_106': xǁOllamaProviderǁ_convert_response__mutmut_106, 
        'xǁOllamaProviderǁ_convert_response__mutmut_107': xǁOllamaProviderǁ_convert_response__mutmut_107
    }
    
    def _convert_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁ_convert_response__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁ_convert_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _convert_response.__signature__ = _mutmut_signature(xǁOllamaProviderǁ_convert_response__mutmut_orig)
    xǁOllamaProviderǁ_convert_response__mutmut_orig.__name__ = 'xǁOllamaProviderǁ_convert_response'
    def xǁOllamaProviderǁsupports_tool_calling__mutmut_orig(self) -> bool:
        """Check if the model supports tool calling."""
        # Ollama models can always support tool calling via prompt embedding
        # even if they don't have native tool support or aren't in the capabilities database
        return True
        
    def xǁOllamaProviderǁsupports_tool_calling__mutmut_1(self) -> bool:
        """Check if the model supports tool calling."""
        # Ollama models can always support tool calling via prompt embedding
        # even if they don't have native tool support or aren't in the capabilities database
        return False
        
    
    xǁOllamaProviderǁsupports_tool_calling__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁsupports_tool_calling__mutmut_1': xǁOllamaProviderǁsupports_tool_calling__mutmut_1
    }
    
    def supports_tool_calling(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁsupports_tool_calling__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁsupports_tool_calling__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_tool_calling.__signature__ = _mutmut_signature(xǁOllamaProviderǁsupports_tool_calling__mutmut_orig)
    xǁOllamaProviderǁsupports_tool_calling__mutmut_orig.__name__ = 'xǁOllamaProviderǁsupports_tool_calling'
    def xǁOllamaProviderǁsupports_parallel_tools__mutmut_orig(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else False
        
    def xǁOllamaProviderǁsupports_parallel_tools__mutmut_1(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.supports_parallel_tools if capabilities else False
        
    def xǁOllamaProviderǁsupports_parallel_tools__mutmut_2(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.supports_parallel_tools if capabilities else False
        
    def xǁOllamaProviderǁsupports_parallel_tools__mutmut_3(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else True
        
    
    xǁOllamaProviderǁsupports_parallel_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁsupports_parallel_tools__mutmut_1': xǁOllamaProviderǁsupports_parallel_tools__mutmut_1, 
        'xǁOllamaProviderǁsupports_parallel_tools__mutmut_2': xǁOllamaProviderǁsupports_parallel_tools__mutmut_2, 
        'xǁOllamaProviderǁsupports_parallel_tools__mutmut_3': xǁOllamaProviderǁsupports_parallel_tools__mutmut_3
    }
    
    def supports_parallel_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁsupports_parallel_tools__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁsupports_parallel_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_parallel_tools.__signature__ = _mutmut_signature(xǁOllamaProviderǁsupports_parallel_tools__mutmut_orig)
    xǁOllamaProviderǁsupports_parallel_tools__mutmut_orig.__name__ = 'xǁOllamaProviderǁsupports_parallel_tools'
    def xǁOllamaProviderǁget_max_tokens__mutmut_orig(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.output_limit if capabilities else None
        
    def xǁOllamaProviderǁget_max_tokens__mutmut_1(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.output_limit if capabilities else None
        
    def xǁOllamaProviderǁget_max_tokens__mutmut_2(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.output_limit if capabilities else None
        
    
    xǁOllamaProviderǁget_max_tokens__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁget_max_tokens__mutmut_1': xǁOllamaProviderǁget_max_tokens__mutmut_1, 
        'xǁOllamaProviderǁget_max_tokens__mutmut_2': xǁOllamaProviderǁget_max_tokens__mutmut_2
    }
    
    def get_max_tokens(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁget_max_tokens__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁget_max_tokens__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_max_tokens.__signature__ = _mutmut_signature(xǁOllamaProviderǁget_max_tokens__mutmut_orig)
    xǁOllamaProviderǁget_max_tokens__mutmut_orig.__name__ = 'xǁOllamaProviderǁget_max_tokens'
    def xǁOllamaProviderǁget_context_window__mutmut_orig(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.context_limit if capabilities else None
    def xǁOllamaProviderǁget_context_window__mutmut_1(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.context_limit if capabilities else None
    def xǁOllamaProviderǁget_context_window__mutmut_2(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.context_limit if capabilities else None
    
    xǁOllamaProviderǁget_context_window__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaProviderǁget_context_window__mutmut_1': xǁOllamaProviderǁget_context_window__mutmut_1, 
        'xǁOllamaProviderǁget_context_window__mutmut_2': xǁOllamaProviderǁget_context_window__mutmut_2
    }
    
    def get_context_window(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaProviderǁget_context_window__mutmut_orig"), object.__getattribute__(self, "xǁOllamaProviderǁget_context_window__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_context_window.__signature__ = _mutmut_signature(xǁOllamaProviderǁget_context_window__mutmut_orig)
    xǁOllamaProviderǁget_context_window__mutmut_orig.__name__ = 'xǁOllamaProviderǁget_context_window'