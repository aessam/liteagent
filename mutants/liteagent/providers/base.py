"""
Base provider interface for LiteAgent.

This module defines the abstract interface that all LLM providers must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import time

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


@dataclass
class ToolCall:
    """Represents a tool call from the model."""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass 
class ProviderResponse:
    """Standardized response format across all providers."""
    content: Optional[str]
    tool_calls: List[ToolCall]
    usage: Optional[Dict[str, Any]]
    model: str
    provider: str
    raw_response: Any
    finish_reason: Optional[str] = None


class ProviderInterface(ABC):
    """Abstract base class for all LLM provider implementations."""
    
    def xǁProviderInterfaceǁ__init____mutmut_orig(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = api_key
        self.provider_name = self._get_provider_name()
        self.config = kwargs
        self._setup_client()
        
    
    def xǁProviderInterfaceǁ__init____mutmut_1(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            **kwargs: Provider-specific configuration
        """
        self.model_name = None
        self.api_key = api_key
        self.provider_name = self._get_provider_name()
        self.config = kwargs
        self._setup_client()
        
    
    def xǁProviderInterfaceǁ__init____mutmut_2(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = None
        self.provider_name = self._get_provider_name()
        self.config = kwargs
        self._setup_client()
        
    
    def xǁProviderInterfaceǁ__init____mutmut_3(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = api_key
        self.provider_name = None
        self.config = kwargs
        self._setup_client()
        
    
    def xǁProviderInterfaceǁ__init____mutmut_4(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = api_key
        self.provider_name = self._get_provider_name()
        self.config = None
        self._setup_client()
        
    
    xǁProviderInterfaceǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProviderInterfaceǁ__init____mutmut_1': xǁProviderInterfaceǁ__init____mutmut_1, 
        'xǁProviderInterfaceǁ__init____mutmut_2': xǁProviderInterfaceǁ__init____mutmut_2, 
        'xǁProviderInterfaceǁ__init____mutmut_3': xǁProviderInterfaceǁ__init____mutmut_3, 
        'xǁProviderInterfaceǁ__init____mutmut_4': xǁProviderInterfaceǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProviderInterfaceǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProviderInterfaceǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProviderInterfaceǁ__init____mutmut_orig)
    xǁProviderInterfaceǁ__init____mutmut_orig.__name__ = 'xǁProviderInterfaceǁ__init__'
    @abstractmethod
    def _get_provider_name(self) -> str:
        """Return the name of the provider."""
        pass
        
    @abstractmethod 
    def _setup_client(self) -> None:
        """Setup the provider-specific client."""
        pass
        
    @abstractmethod
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional provider-specific parameters
            
        Returns:
            ProviderResponse: Standardized response object
        """
        pass
        
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        pass
        
    @abstractmethod
    def supports_parallel_tools(self) -> bool:
        """Check if the model supports parallel tool execution."""
        pass
        
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        # Default implementation - providers can override
        return None
        
    def get_context_window(self) -> Optional[int]:
        """Get the context window size for this model."""
        # Default implementation - providers can override  
        return None
        
    def xǁProviderInterfaceǁ_log_request__mutmut_orig(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_1(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(None)
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_2(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(None)
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_3(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = None
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_4(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get(None, 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_5(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', None) for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_6(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_7(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', ) for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_8(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get(None, {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_9(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', None).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_10(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get({}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_11(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', ).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_12(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('XXfunctionXX', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_13(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('FUNCTION', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_14(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('XXnameXX', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_15(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('NAME', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_16(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'XXunknownXX') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_17(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'UNKNOWN') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_18(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'unknown') for tool in tools]
            logger.info(None)
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def xǁProviderInterfaceǁ_log_request__mutmut_19(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(None)
            
    
    xǁProviderInterfaceǁ_log_request__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProviderInterfaceǁ_log_request__mutmut_1': xǁProviderInterfaceǁ_log_request__mutmut_1, 
        'xǁProviderInterfaceǁ_log_request__mutmut_2': xǁProviderInterfaceǁ_log_request__mutmut_2, 
        'xǁProviderInterfaceǁ_log_request__mutmut_3': xǁProviderInterfaceǁ_log_request__mutmut_3, 
        'xǁProviderInterfaceǁ_log_request__mutmut_4': xǁProviderInterfaceǁ_log_request__mutmut_4, 
        'xǁProviderInterfaceǁ_log_request__mutmut_5': xǁProviderInterfaceǁ_log_request__mutmut_5, 
        'xǁProviderInterfaceǁ_log_request__mutmut_6': xǁProviderInterfaceǁ_log_request__mutmut_6, 
        'xǁProviderInterfaceǁ_log_request__mutmut_7': xǁProviderInterfaceǁ_log_request__mutmut_7, 
        'xǁProviderInterfaceǁ_log_request__mutmut_8': xǁProviderInterfaceǁ_log_request__mutmut_8, 
        'xǁProviderInterfaceǁ_log_request__mutmut_9': xǁProviderInterfaceǁ_log_request__mutmut_9, 
        'xǁProviderInterfaceǁ_log_request__mutmut_10': xǁProviderInterfaceǁ_log_request__mutmut_10, 
        'xǁProviderInterfaceǁ_log_request__mutmut_11': xǁProviderInterfaceǁ_log_request__mutmut_11, 
        'xǁProviderInterfaceǁ_log_request__mutmut_12': xǁProviderInterfaceǁ_log_request__mutmut_12, 
        'xǁProviderInterfaceǁ_log_request__mutmut_13': xǁProviderInterfaceǁ_log_request__mutmut_13, 
        'xǁProviderInterfaceǁ_log_request__mutmut_14': xǁProviderInterfaceǁ_log_request__mutmut_14, 
        'xǁProviderInterfaceǁ_log_request__mutmut_15': xǁProviderInterfaceǁ_log_request__mutmut_15, 
        'xǁProviderInterfaceǁ_log_request__mutmut_16': xǁProviderInterfaceǁ_log_request__mutmut_16, 
        'xǁProviderInterfaceǁ_log_request__mutmut_17': xǁProviderInterfaceǁ_log_request__mutmut_17, 
        'xǁProviderInterfaceǁ_log_request__mutmut_18': xǁProviderInterfaceǁ_log_request__mutmut_18, 
        'xǁProviderInterfaceǁ_log_request__mutmut_19': xǁProviderInterfaceǁ_log_request__mutmut_19
    }
    
    def _log_request(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProviderInterfaceǁ_log_request__mutmut_orig"), object.__getattribute__(self, "xǁProviderInterfaceǁ_log_request__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log_request.__signature__ = _mutmut_signature(xǁProviderInterfaceǁ_log_request__mutmut_orig)
    xǁProviderInterfaceǁ_log_request__mutmut_orig.__name__ = 'xǁProviderInterfaceǁ_log_request'
    def xǁProviderInterfaceǁ_log_response__mutmut_orig(self, response: ProviderResponse, elapsed_time: float) -> None:
        """Log the response details."""
        logger.info(f"[{self.provider_name}] Response received in {elapsed_time:.2f}s")
        if response.tool_calls:
            logger.info(f"[{self.provider_name}] Tool calls: {[tc.name for tc in response.tool_calls]}")
        if response.usage:
            logger.info(f"[{self.provider_name}] Token usage: {response.usage}")
            
    def xǁProviderInterfaceǁ_log_response__mutmut_1(self, response: ProviderResponse, elapsed_time: float) -> None:
        """Log the response details."""
        logger.info(None)
        if response.tool_calls:
            logger.info(f"[{self.provider_name}] Tool calls: {[tc.name for tc in response.tool_calls]}")
        if response.usage:
            logger.info(f"[{self.provider_name}] Token usage: {response.usage}")
            
    def xǁProviderInterfaceǁ_log_response__mutmut_2(self, response: ProviderResponse, elapsed_time: float) -> None:
        """Log the response details."""
        logger.info(f"[{self.provider_name}] Response received in {elapsed_time:.2f}s")
        if response.tool_calls:
            logger.info(None)
        if response.usage:
            logger.info(f"[{self.provider_name}] Token usage: {response.usage}")
            
    def xǁProviderInterfaceǁ_log_response__mutmut_3(self, response: ProviderResponse, elapsed_time: float) -> None:
        """Log the response details."""
        logger.info(f"[{self.provider_name}] Response received in {elapsed_time:.2f}s")
        if response.tool_calls:
            logger.info(f"[{self.provider_name}] Tool calls: {[tc.name for tc in response.tool_calls]}")
        if response.usage:
            logger.info(None)
            
    
    xǁProviderInterfaceǁ_log_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProviderInterfaceǁ_log_response__mutmut_1': xǁProviderInterfaceǁ_log_response__mutmut_1, 
        'xǁProviderInterfaceǁ_log_response__mutmut_2': xǁProviderInterfaceǁ_log_response__mutmut_2, 
        'xǁProviderInterfaceǁ_log_response__mutmut_3': xǁProviderInterfaceǁ_log_response__mutmut_3
    }
    
    def _log_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProviderInterfaceǁ_log_response__mutmut_orig"), object.__getattribute__(self, "xǁProviderInterfaceǁ_log_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log_response.__signature__ = _mutmut_signature(xǁProviderInterfaceǁ_log_response__mutmut_orig)
    xǁProviderInterfaceǁ_log_response__mutmut_orig.__name__ = 'xǁProviderInterfaceǁ_log_response'
    # Removed _handle_error - all providers should fail fast without error handling