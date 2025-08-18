"""
Groq provider implementation for LiteAgent.

This provider uses the official Groq Python client library.
"""

import os
import time
from typing import Any, Dict, List, Optional

try:
    from groq import Groq
    from groq.types.chat import ChatCompletion
except ImportError:
    raise ImportError("Groq library not installed. Install with: pip install groq")

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


class GroqProvider(ProviderInterface):
    """Groq provider using the official Groq client library."""
    
    def xǁGroqProviderǁ__init____mutmut_orig(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_1(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = None
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_2(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get(None, 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_3(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', None)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_4(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get(3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_5(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', )
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_6(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('XXmax_retriesXX', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_7(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('MAX_RETRIES', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_8(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 4)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_9(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = None
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_10(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get(None, 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_11(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', None)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_12(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get(60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_13(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', )
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_14(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('XXtimeoutXX', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_15(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('TIMEOUT', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_16(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 61)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_17(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(None, api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_18(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, None, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_19(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(api_key, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_20(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, **kwargs)
        
    
    def xǁGroqProviderǁ__init____mutmut_21(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Groq provider.
        
        Args:
            model_name: Name of the Groq model (e.g., 'qwen3-32b')
            api_key: Groq API key (will use GROQ_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, )
        
    
    xǁGroqProviderǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁ__init____mutmut_1': xǁGroqProviderǁ__init____mutmut_1, 
        'xǁGroqProviderǁ__init____mutmut_2': xǁGroqProviderǁ__init____mutmut_2, 
        'xǁGroqProviderǁ__init____mutmut_3': xǁGroqProviderǁ__init____mutmut_3, 
        'xǁGroqProviderǁ__init____mutmut_4': xǁGroqProviderǁ__init____mutmut_4, 
        'xǁGroqProviderǁ__init____mutmut_5': xǁGroqProviderǁ__init____mutmut_5, 
        'xǁGroqProviderǁ__init____mutmut_6': xǁGroqProviderǁ__init____mutmut_6, 
        'xǁGroqProviderǁ__init____mutmut_7': xǁGroqProviderǁ__init____mutmut_7, 
        'xǁGroqProviderǁ__init____mutmut_8': xǁGroqProviderǁ__init____mutmut_8, 
        'xǁGroqProviderǁ__init____mutmut_9': xǁGroqProviderǁ__init____mutmut_9, 
        'xǁGroqProviderǁ__init____mutmut_10': xǁGroqProviderǁ__init____mutmut_10, 
        'xǁGroqProviderǁ__init____mutmut_11': xǁGroqProviderǁ__init____mutmut_11, 
        'xǁGroqProviderǁ__init____mutmut_12': xǁGroqProviderǁ__init____mutmut_12, 
        'xǁGroqProviderǁ__init____mutmut_13': xǁGroqProviderǁ__init____mutmut_13, 
        'xǁGroqProviderǁ__init____mutmut_14': xǁGroqProviderǁ__init____mutmut_14, 
        'xǁGroqProviderǁ__init____mutmut_15': xǁGroqProviderǁ__init____mutmut_15, 
        'xǁGroqProviderǁ__init____mutmut_16': xǁGroqProviderǁ__init____mutmut_16, 
        'xǁGroqProviderǁ__init____mutmut_17': xǁGroqProviderǁ__init____mutmut_17, 
        'xǁGroqProviderǁ__init____mutmut_18': xǁGroqProviderǁ__init____mutmut_18, 
        'xǁGroqProviderǁ__init____mutmut_19': xǁGroqProviderǁ__init____mutmut_19, 
        'xǁGroqProviderǁ__init____mutmut_20': xǁGroqProviderǁ__init____mutmut_20, 
        'xǁGroqProviderǁ__init____mutmut_21': xǁGroqProviderǁ__init____mutmut_21
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁGroqProviderǁ__init____mutmut_orig)
    xǁGroqProviderǁ__init____mutmut_orig.__name__ = 'xǁGroqProviderǁ__init__'
    def xǁGroqProviderǁ_get_provider_name__mutmut_orig(self) -> str:
        """Return the provider name."""
        return 'groq'
        
    def xǁGroqProviderǁ_get_provider_name__mutmut_1(self) -> str:
        """Return the provider name."""
        return 'XXgroqXX'
        
    def xǁGroqProviderǁ_get_provider_name__mutmut_2(self) -> str:
        """Return the provider name."""
        return 'GROQ'
        
    
    xǁGroqProviderǁ_get_provider_name__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁ_get_provider_name__mutmut_1': xǁGroqProviderǁ_get_provider_name__mutmut_1, 
        'xǁGroqProviderǁ_get_provider_name__mutmut_2': xǁGroqProviderǁ_get_provider_name__mutmut_2
    }
    
    def _get_provider_name(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁ_get_provider_name__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁ_get_provider_name__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_provider_name.__signature__ = _mutmut_signature(xǁGroqProviderǁ_get_provider_name__mutmut_orig)
    xǁGroqProviderǁ_get_provider_name__mutmut_orig.__name__ = 'xǁGroqProviderǁ_get_provider_name'
    def xǁGroqProviderǁ_setup_client__mutmut_orig(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('GROQ_API_KEY'),
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_1(self) -> None:
        """Setup the Groq client."""
        self.client = None
        
    def xǁGroqProviderǁ_setup_client__mutmut_2(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=None,
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_3(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('GROQ_API_KEY'),
            max_retries=None,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_4(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('GROQ_API_KEY'),
            max_retries=self.max_retries,
            timeout=None,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_5(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_6(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('GROQ_API_KEY'),
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_7(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('GROQ_API_KEY'),
            max_retries=self.max_retries,
            )
        
    def xǁGroqProviderǁ_setup_client__mutmut_8(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key and os.getenv('GROQ_API_KEY'),
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_9(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv(None),
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_10(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('XXGROQ_API_KEYXX'),
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def xǁGroqProviderǁ_setup_client__mutmut_11(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('groq_api_key'),
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    
    xǁGroqProviderǁ_setup_client__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁ_setup_client__mutmut_1': xǁGroqProviderǁ_setup_client__mutmut_1, 
        'xǁGroqProviderǁ_setup_client__mutmut_2': xǁGroqProviderǁ_setup_client__mutmut_2, 
        'xǁGroqProviderǁ_setup_client__mutmut_3': xǁGroqProviderǁ_setup_client__mutmut_3, 
        'xǁGroqProviderǁ_setup_client__mutmut_4': xǁGroqProviderǁ_setup_client__mutmut_4, 
        'xǁGroqProviderǁ_setup_client__mutmut_5': xǁGroqProviderǁ_setup_client__mutmut_5, 
        'xǁGroqProviderǁ_setup_client__mutmut_6': xǁGroqProviderǁ_setup_client__mutmut_6, 
        'xǁGroqProviderǁ_setup_client__mutmut_7': xǁGroqProviderǁ_setup_client__mutmut_7, 
        'xǁGroqProviderǁ_setup_client__mutmut_8': xǁGroqProviderǁ_setup_client__mutmut_8, 
        'xǁGroqProviderǁ_setup_client__mutmut_9': xǁGroqProviderǁ_setup_client__mutmut_9, 
        'xǁGroqProviderǁ_setup_client__mutmut_10': xǁGroqProviderǁ_setup_client__mutmut_10, 
        'xǁGroqProviderǁ_setup_client__mutmut_11': xǁGroqProviderǁ_setup_client__mutmut_11
    }
    
    def _setup_client(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁ_setup_client__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁ_setup_client__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _setup_client.__signature__ = _mutmut_signature(xǁGroqProviderǁ_setup_client__mutmut_orig)
    xǁGroqProviderǁ_setup_client__mutmut_orig.__name__ = 'xǁGroqProviderǁ_setup_client'
    def xǁGroqProviderǁgenerate_response__mutmut_orig(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_1(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = None
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_2(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(None, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_3(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, None)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_4(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_5(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, )
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_6(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = None
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_7(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'XXtemperatureXX', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_8(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'TEMPERATURE', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_9(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'XXmax_tokensXX', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_10(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'MAX_TOKENS', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_11(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'XXtop_pXX', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_12(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'TOP_P', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_13(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'XXstreamXX', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_14(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'STREAM', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_15(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'XXstopXX',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_16(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'STOP',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_17(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'XXfrequency_penaltyXX', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_18(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'FREQUENCY_PENALTY', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_19(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'XXpresence_penaltyXX', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_20(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'PRESENCE_PENALTY', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_21(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'XXnXX', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_22(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'N', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_23(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'XXuserXX',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_24(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'USER',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_25(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'XXresponse_formatXX', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_26(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'RESPONSE_FORMAT', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_27(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'XXseedXX', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_28(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'SEED', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_29(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'XXmax_completion_tokensXX'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_30(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'MAX_COMPLETION_TOKENS'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_31(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = None
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_32(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_33(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = None
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_34(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'XXmodelXX': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_35(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'MODEL': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_36(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'XXmessagesXX': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_37(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'MESSAGES': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_38(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools or self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_39(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) >= 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_40(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 129:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_41(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(None)
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_42(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = None
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_43(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['XXtoolsXX'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_44(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['TOOLS'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_45(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = None
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_46(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['XXtool_choiceXX'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_47(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['TOOL_CHOICE'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_48(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'XXautoXX'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_49(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'AUTO'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_50(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = None
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_51(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['XXparallel_tool_callsXX'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_52(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['PARALLEL_TOOL_CALLS'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_53(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = False
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_54(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = None
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_55(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = None
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_56(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(None)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_57(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = None
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_58(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() + start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_59(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(None, elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_60(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, None)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_61(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(elapsed_time)
        
        return provider_response
            
    def xǁGroqProviderǁgenerate_response__mutmut_62(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Groq's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for Groq
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'stream', 'stop',
            'frequency_penalty', 'presence_penalty', 'n', 'user',
            'response_format', 'seed', 'max_completion_tokens'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **filtered_kwargs  # Include only supported parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            # Groq has a limit of 128 tools per request
            if len(tools) > 128:
                raise ValueError(f"Too many tools for Groq provider: {len(tools)}. Maximum allowed: 128")
                
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        # Make the API call
        response: ChatCompletion = self.client.chat.completions.create(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, )
        
        return provider_response
            
    
    xǁGroqProviderǁgenerate_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁgenerate_response__mutmut_1': xǁGroqProviderǁgenerate_response__mutmut_1, 
        'xǁGroqProviderǁgenerate_response__mutmut_2': xǁGroqProviderǁgenerate_response__mutmut_2, 
        'xǁGroqProviderǁgenerate_response__mutmut_3': xǁGroqProviderǁgenerate_response__mutmut_3, 
        'xǁGroqProviderǁgenerate_response__mutmut_4': xǁGroqProviderǁgenerate_response__mutmut_4, 
        'xǁGroqProviderǁgenerate_response__mutmut_5': xǁGroqProviderǁgenerate_response__mutmut_5, 
        'xǁGroqProviderǁgenerate_response__mutmut_6': xǁGroqProviderǁgenerate_response__mutmut_6, 
        'xǁGroqProviderǁgenerate_response__mutmut_7': xǁGroqProviderǁgenerate_response__mutmut_7, 
        'xǁGroqProviderǁgenerate_response__mutmut_8': xǁGroqProviderǁgenerate_response__mutmut_8, 
        'xǁGroqProviderǁgenerate_response__mutmut_9': xǁGroqProviderǁgenerate_response__mutmut_9, 
        'xǁGroqProviderǁgenerate_response__mutmut_10': xǁGroqProviderǁgenerate_response__mutmut_10, 
        'xǁGroqProviderǁgenerate_response__mutmut_11': xǁGroqProviderǁgenerate_response__mutmut_11, 
        'xǁGroqProviderǁgenerate_response__mutmut_12': xǁGroqProviderǁgenerate_response__mutmut_12, 
        'xǁGroqProviderǁgenerate_response__mutmut_13': xǁGroqProviderǁgenerate_response__mutmut_13, 
        'xǁGroqProviderǁgenerate_response__mutmut_14': xǁGroqProviderǁgenerate_response__mutmut_14, 
        'xǁGroqProviderǁgenerate_response__mutmut_15': xǁGroqProviderǁgenerate_response__mutmut_15, 
        'xǁGroqProviderǁgenerate_response__mutmut_16': xǁGroqProviderǁgenerate_response__mutmut_16, 
        'xǁGroqProviderǁgenerate_response__mutmut_17': xǁGroqProviderǁgenerate_response__mutmut_17, 
        'xǁGroqProviderǁgenerate_response__mutmut_18': xǁGroqProviderǁgenerate_response__mutmut_18, 
        'xǁGroqProviderǁgenerate_response__mutmut_19': xǁGroqProviderǁgenerate_response__mutmut_19, 
        'xǁGroqProviderǁgenerate_response__mutmut_20': xǁGroqProviderǁgenerate_response__mutmut_20, 
        'xǁGroqProviderǁgenerate_response__mutmut_21': xǁGroqProviderǁgenerate_response__mutmut_21, 
        'xǁGroqProviderǁgenerate_response__mutmut_22': xǁGroqProviderǁgenerate_response__mutmut_22, 
        'xǁGroqProviderǁgenerate_response__mutmut_23': xǁGroqProviderǁgenerate_response__mutmut_23, 
        'xǁGroqProviderǁgenerate_response__mutmut_24': xǁGroqProviderǁgenerate_response__mutmut_24, 
        'xǁGroqProviderǁgenerate_response__mutmut_25': xǁGroqProviderǁgenerate_response__mutmut_25, 
        'xǁGroqProviderǁgenerate_response__mutmut_26': xǁGroqProviderǁgenerate_response__mutmut_26, 
        'xǁGroqProviderǁgenerate_response__mutmut_27': xǁGroqProviderǁgenerate_response__mutmut_27, 
        'xǁGroqProviderǁgenerate_response__mutmut_28': xǁGroqProviderǁgenerate_response__mutmut_28, 
        'xǁGroqProviderǁgenerate_response__mutmut_29': xǁGroqProviderǁgenerate_response__mutmut_29, 
        'xǁGroqProviderǁgenerate_response__mutmut_30': xǁGroqProviderǁgenerate_response__mutmut_30, 
        'xǁGroqProviderǁgenerate_response__mutmut_31': xǁGroqProviderǁgenerate_response__mutmut_31, 
        'xǁGroqProviderǁgenerate_response__mutmut_32': xǁGroqProviderǁgenerate_response__mutmut_32, 
        'xǁGroqProviderǁgenerate_response__mutmut_33': xǁGroqProviderǁgenerate_response__mutmut_33, 
        'xǁGroqProviderǁgenerate_response__mutmut_34': xǁGroqProviderǁgenerate_response__mutmut_34, 
        'xǁGroqProviderǁgenerate_response__mutmut_35': xǁGroqProviderǁgenerate_response__mutmut_35, 
        'xǁGroqProviderǁgenerate_response__mutmut_36': xǁGroqProviderǁgenerate_response__mutmut_36, 
        'xǁGroqProviderǁgenerate_response__mutmut_37': xǁGroqProviderǁgenerate_response__mutmut_37, 
        'xǁGroqProviderǁgenerate_response__mutmut_38': xǁGroqProviderǁgenerate_response__mutmut_38, 
        'xǁGroqProviderǁgenerate_response__mutmut_39': xǁGroqProviderǁgenerate_response__mutmut_39, 
        'xǁGroqProviderǁgenerate_response__mutmut_40': xǁGroqProviderǁgenerate_response__mutmut_40, 
        'xǁGroqProviderǁgenerate_response__mutmut_41': xǁGroqProviderǁgenerate_response__mutmut_41, 
        'xǁGroqProviderǁgenerate_response__mutmut_42': xǁGroqProviderǁgenerate_response__mutmut_42, 
        'xǁGroqProviderǁgenerate_response__mutmut_43': xǁGroqProviderǁgenerate_response__mutmut_43, 
        'xǁGroqProviderǁgenerate_response__mutmut_44': xǁGroqProviderǁgenerate_response__mutmut_44, 
        'xǁGroqProviderǁgenerate_response__mutmut_45': xǁGroqProviderǁgenerate_response__mutmut_45, 
        'xǁGroqProviderǁgenerate_response__mutmut_46': xǁGroqProviderǁgenerate_response__mutmut_46, 
        'xǁGroqProviderǁgenerate_response__mutmut_47': xǁGroqProviderǁgenerate_response__mutmut_47, 
        'xǁGroqProviderǁgenerate_response__mutmut_48': xǁGroqProviderǁgenerate_response__mutmut_48, 
        'xǁGroqProviderǁgenerate_response__mutmut_49': xǁGroqProviderǁgenerate_response__mutmut_49, 
        'xǁGroqProviderǁgenerate_response__mutmut_50': xǁGroqProviderǁgenerate_response__mutmut_50, 
        'xǁGroqProviderǁgenerate_response__mutmut_51': xǁGroqProviderǁgenerate_response__mutmut_51, 
        'xǁGroqProviderǁgenerate_response__mutmut_52': xǁGroqProviderǁgenerate_response__mutmut_52, 
        'xǁGroqProviderǁgenerate_response__mutmut_53': xǁGroqProviderǁgenerate_response__mutmut_53, 
        'xǁGroqProviderǁgenerate_response__mutmut_54': xǁGroqProviderǁgenerate_response__mutmut_54, 
        'xǁGroqProviderǁgenerate_response__mutmut_55': xǁGroqProviderǁgenerate_response__mutmut_55, 
        'xǁGroqProviderǁgenerate_response__mutmut_56': xǁGroqProviderǁgenerate_response__mutmut_56, 
        'xǁGroqProviderǁgenerate_response__mutmut_57': xǁGroqProviderǁgenerate_response__mutmut_57, 
        'xǁGroqProviderǁgenerate_response__mutmut_58': xǁGroqProviderǁgenerate_response__mutmut_58, 
        'xǁGroqProviderǁgenerate_response__mutmut_59': xǁGroqProviderǁgenerate_response__mutmut_59, 
        'xǁGroqProviderǁgenerate_response__mutmut_60': xǁGroqProviderǁgenerate_response__mutmut_60, 
        'xǁGroqProviderǁgenerate_response__mutmut_61': xǁGroqProviderǁgenerate_response__mutmut_61, 
        'xǁGroqProviderǁgenerate_response__mutmut_62': xǁGroqProviderǁgenerate_response__mutmut_62
    }
    
    def generate_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁgenerate_response__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁgenerate_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_response.__signature__ = _mutmut_signature(xǁGroqProviderǁgenerate_response__mutmut_orig)
    xǁGroqProviderǁgenerate_response__mutmut_orig.__name__ = 'xǁGroqProviderǁgenerate_response'
    def xǁGroqProviderǁ_convert_response__mutmut_orig(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_1(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = None
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_2(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[1].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_3(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = None
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_4(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = None
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_5(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = None
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_6(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = None
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_7(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(None)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_8(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(None) from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_9(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(None)
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_10(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=None,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_11(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=None,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_12(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=None
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_13(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_14(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_15(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_16(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = ""
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_17(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = None
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_18(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'XXprompt_tokensXX': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_19(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'PROMPT_TOKENS': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_20(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'XXcompletion_tokensXX': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_21(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'COMPLETION_TOKENS': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_22(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'XXtotal_tokensXX': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_23(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'TOTAL_TOKENS': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_24(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_25(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=None,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_26(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=None,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_27(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=None,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_28(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=None,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_29(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=None,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_30(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=None
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_31(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_32(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_33(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_34(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_35(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            raw_response=response,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_36(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            finish_reason=response.choices[0].finish_reason
        )
        
    def xǁGroqProviderǁ_convert_response__mutmut_37(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            )
        
    def xǁGroqProviderǁ_convert_response__mutmut_38(self, response: ChatCompletion) -> ProviderResponse:
        """Convert Groq response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments if they're a string
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                        
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
            
        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.choices[1].finish_reason
        )
        
    
    xǁGroqProviderǁ_convert_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁ_convert_response__mutmut_1': xǁGroqProviderǁ_convert_response__mutmut_1, 
        'xǁGroqProviderǁ_convert_response__mutmut_2': xǁGroqProviderǁ_convert_response__mutmut_2, 
        'xǁGroqProviderǁ_convert_response__mutmut_3': xǁGroqProviderǁ_convert_response__mutmut_3, 
        'xǁGroqProviderǁ_convert_response__mutmut_4': xǁGroqProviderǁ_convert_response__mutmut_4, 
        'xǁGroqProviderǁ_convert_response__mutmut_5': xǁGroqProviderǁ_convert_response__mutmut_5, 
        'xǁGroqProviderǁ_convert_response__mutmut_6': xǁGroqProviderǁ_convert_response__mutmut_6, 
        'xǁGroqProviderǁ_convert_response__mutmut_7': xǁGroqProviderǁ_convert_response__mutmut_7, 
        'xǁGroqProviderǁ_convert_response__mutmut_8': xǁGroqProviderǁ_convert_response__mutmut_8, 
        'xǁGroqProviderǁ_convert_response__mutmut_9': xǁGroqProviderǁ_convert_response__mutmut_9, 
        'xǁGroqProviderǁ_convert_response__mutmut_10': xǁGroqProviderǁ_convert_response__mutmut_10, 
        'xǁGroqProviderǁ_convert_response__mutmut_11': xǁGroqProviderǁ_convert_response__mutmut_11, 
        'xǁGroqProviderǁ_convert_response__mutmut_12': xǁGroqProviderǁ_convert_response__mutmut_12, 
        'xǁGroqProviderǁ_convert_response__mutmut_13': xǁGroqProviderǁ_convert_response__mutmut_13, 
        'xǁGroqProviderǁ_convert_response__mutmut_14': xǁGroqProviderǁ_convert_response__mutmut_14, 
        'xǁGroqProviderǁ_convert_response__mutmut_15': xǁGroqProviderǁ_convert_response__mutmut_15, 
        'xǁGroqProviderǁ_convert_response__mutmut_16': xǁGroqProviderǁ_convert_response__mutmut_16, 
        'xǁGroqProviderǁ_convert_response__mutmut_17': xǁGroqProviderǁ_convert_response__mutmut_17, 
        'xǁGroqProviderǁ_convert_response__mutmut_18': xǁGroqProviderǁ_convert_response__mutmut_18, 
        'xǁGroqProviderǁ_convert_response__mutmut_19': xǁGroqProviderǁ_convert_response__mutmut_19, 
        'xǁGroqProviderǁ_convert_response__mutmut_20': xǁGroqProviderǁ_convert_response__mutmut_20, 
        'xǁGroqProviderǁ_convert_response__mutmut_21': xǁGroqProviderǁ_convert_response__mutmut_21, 
        'xǁGroqProviderǁ_convert_response__mutmut_22': xǁGroqProviderǁ_convert_response__mutmut_22, 
        'xǁGroqProviderǁ_convert_response__mutmut_23': xǁGroqProviderǁ_convert_response__mutmut_23, 
        'xǁGroqProviderǁ_convert_response__mutmut_24': xǁGroqProviderǁ_convert_response__mutmut_24, 
        'xǁGroqProviderǁ_convert_response__mutmut_25': xǁGroqProviderǁ_convert_response__mutmut_25, 
        'xǁGroqProviderǁ_convert_response__mutmut_26': xǁGroqProviderǁ_convert_response__mutmut_26, 
        'xǁGroqProviderǁ_convert_response__mutmut_27': xǁGroqProviderǁ_convert_response__mutmut_27, 
        'xǁGroqProviderǁ_convert_response__mutmut_28': xǁGroqProviderǁ_convert_response__mutmut_28, 
        'xǁGroqProviderǁ_convert_response__mutmut_29': xǁGroqProviderǁ_convert_response__mutmut_29, 
        'xǁGroqProviderǁ_convert_response__mutmut_30': xǁGroqProviderǁ_convert_response__mutmut_30, 
        'xǁGroqProviderǁ_convert_response__mutmut_31': xǁGroqProviderǁ_convert_response__mutmut_31, 
        'xǁGroqProviderǁ_convert_response__mutmut_32': xǁGroqProviderǁ_convert_response__mutmut_32, 
        'xǁGroqProviderǁ_convert_response__mutmut_33': xǁGroqProviderǁ_convert_response__mutmut_33, 
        'xǁGroqProviderǁ_convert_response__mutmut_34': xǁGroqProviderǁ_convert_response__mutmut_34, 
        'xǁGroqProviderǁ_convert_response__mutmut_35': xǁGroqProviderǁ_convert_response__mutmut_35, 
        'xǁGroqProviderǁ_convert_response__mutmut_36': xǁGroqProviderǁ_convert_response__mutmut_36, 
        'xǁGroqProviderǁ_convert_response__mutmut_37': xǁGroqProviderǁ_convert_response__mutmut_37, 
        'xǁGroqProviderǁ_convert_response__mutmut_38': xǁGroqProviderǁ_convert_response__mutmut_38
    }
    
    def _convert_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁ_convert_response__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁ_convert_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _convert_response.__signature__ = _mutmut_signature(xǁGroqProviderǁ_convert_response__mutmut_orig)
    xǁGroqProviderǁ_convert_response__mutmut_orig.__name__ = 'xǁGroqProviderǁ_convert_response'
    def xǁGroqProviderǁsupports_tool_calling__mutmut_orig(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.tool_calling if capabilities else False
        
    def xǁGroqProviderǁsupports_tool_calling__mutmut_1(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.tool_calling if capabilities else False
        
    def xǁGroqProviderǁsupports_tool_calling__mutmut_2(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.tool_calling if capabilities else False
        
    def xǁGroqProviderǁsupports_tool_calling__mutmut_3(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.tool_calling if capabilities else True
        
    
    xǁGroqProviderǁsupports_tool_calling__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁsupports_tool_calling__mutmut_1': xǁGroqProviderǁsupports_tool_calling__mutmut_1, 
        'xǁGroqProviderǁsupports_tool_calling__mutmut_2': xǁGroqProviderǁsupports_tool_calling__mutmut_2, 
        'xǁGroqProviderǁsupports_tool_calling__mutmut_3': xǁGroqProviderǁsupports_tool_calling__mutmut_3
    }
    
    def supports_tool_calling(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁsupports_tool_calling__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁsupports_tool_calling__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_tool_calling.__signature__ = _mutmut_signature(xǁGroqProviderǁsupports_tool_calling__mutmut_orig)
    xǁGroqProviderǁsupports_tool_calling__mutmut_orig.__name__ = 'xǁGroqProviderǁsupports_tool_calling'
    def xǁGroqProviderǁsupports_parallel_tools__mutmut_orig(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else False
        
    def xǁGroqProviderǁsupports_parallel_tools__mutmut_1(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.supports_parallel_tools if capabilities else False
        
    def xǁGroqProviderǁsupports_parallel_tools__mutmut_2(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.supports_parallel_tools if capabilities else False
        
    def xǁGroqProviderǁsupports_parallel_tools__mutmut_3(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else True
        
    
    xǁGroqProviderǁsupports_parallel_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁsupports_parallel_tools__mutmut_1': xǁGroqProviderǁsupports_parallel_tools__mutmut_1, 
        'xǁGroqProviderǁsupports_parallel_tools__mutmut_2': xǁGroqProviderǁsupports_parallel_tools__mutmut_2, 
        'xǁGroqProviderǁsupports_parallel_tools__mutmut_3': xǁGroqProviderǁsupports_parallel_tools__mutmut_3
    }
    
    def supports_parallel_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁsupports_parallel_tools__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁsupports_parallel_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_parallel_tools.__signature__ = _mutmut_signature(xǁGroqProviderǁsupports_parallel_tools__mutmut_orig)
    xǁGroqProviderǁsupports_parallel_tools__mutmut_orig.__name__ = 'xǁGroqProviderǁsupports_parallel_tools'
    def xǁGroqProviderǁget_max_tokens__mutmut_orig(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.output_limit if capabilities else None
        
    def xǁGroqProviderǁget_max_tokens__mutmut_1(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.output_limit if capabilities else None
        
    def xǁGroqProviderǁget_max_tokens__mutmut_2(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.output_limit if capabilities else None
        
    
    xǁGroqProviderǁget_max_tokens__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁget_max_tokens__mutmut_1': xǁGroqProviderǁget_max_tokens__mutmut_1, 
        'xǁGroqProviderǁget_max_tokens__mutmut_2': xǁGroqProviderǁget_max_tokens__mutmut_2
    }
    
    def get_max_tokens(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁget_max_tokens__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁget_max_tokens__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_max_tokens.__signature__ = _mutmut_signature(xǁGroqProviderǁget_max_tokens__mutmut_orig)
    xǁGroqProviderǁget_max_tokens__mutmut_orig.__name__ = 'xǁGroqProviderǁget_max_tokens'
    def xǁGroqProviderǁget_context_window__mutmut_orig(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.context_limit if capabilities else None
    def xǁGroqProviderǁget_context_window__mutmut_1(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.context_limit if capabilities else None
    def xǁGroqProviderǁget_context_window__mutmut_2(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.context_limit if capabilities else None
    
    xǁGroqProviderǁget_context_window__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGroqProviderǁget_context_window__mutmut_1': xǁGroqProviderǁget_context_window__mutmut_1, 
        'xǁGroqProviderǁget_context_window__mutmut_2': xǁGroqProviderǁget_context_window__mutmut_2
    }
    
    def get_context_window(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGroqProviderǁget_context_window__mutmut_orig"), object.__getattribute__(self, "xǁGroqProviderǁget_context_window__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_context_window.__signature__ = _mutmut_signature(xǁGroqProviderǁget_context_window__mutmut_orig)
    xǁGroqProviderǁget_context_window__mutmut_orig.__name__ = 'xǁGroqProviderǁget_context_window'