"""
OpenAI provider implementation for LiteAgent.

This provider uses the official OpenAI Python client library and also supports
OpenAI-compatible APIs like DeepSeek by setting a different base_url.
"""

import os
import time
from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
    from openai.types.chat import ChatCompletion, ChatCompletionMessage
    from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
except ImportError:
    raise ImportError("OpenAI library not installed. Install with: pip install openai")

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


class OpenAIProvider(ProviderInterface):
    """OpenAI provider using the official OpenAI client library."""
    
    def xǁOpenAIProviderǁ__init____mutmut_orig(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_1(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = None
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_2(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get(None)
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_3(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('XXbase_urlXX')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_4(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('BASE_URL')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_5(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = None
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_6(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get(None)
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_7(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('XXorganizationXX')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_8(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('ORGANIZATION')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_9(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = None
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_10(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get(None)
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_11(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('XXprojectXX')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_12(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('PROJECT')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_13(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = None
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_14(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get(None, 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_15(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', None)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_16(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get(3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_17(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', )
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_18(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('XXmax_retriesXX', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_19(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('MAX_RETRIES', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_20(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 4)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_21(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = None
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_22(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get(None, 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_23(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', None)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_24(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get(60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_25(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', )
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_26(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('XXtimeoutXX', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_27(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('TIMEOUT', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_28(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 61)
        
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_29(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(None, api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_30(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, None, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_31(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(api_key, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_32(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, **kwargs)
        
    
    def xǁOpenAIProviderǁ__init____mutmut_33(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI provider.
        
        Args:
            model_name: Name of the OpenAI model (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - base_url: Custom base URL (for OpenAI-compatible APIs like DeepSeek)
                - organization: OpenAI organization ID
                - project: OpenAI project ID
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.base_url = kwargs.get('base_url')
        self.organization = kwargs.get('organization')
        self.project = kwargs.get('project')
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, )
        
    
    xǁOpenAIProviderǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁ__init____mutmut_1': xǁOpenAIProviderǁ__init____mutmut_1, 
        'xǁOpenAIProviderǁ__init____mutmut_2': xǁOpenAIProviderǁ__init____mutmut_2, 
        'xǁOpenAIProviderǁ__init____mutmut_3': xǁOpenAIProviderǁ__init____mutmut_3, 
        'xǁOpenAIProviderǁ__init____mutmut_4': xǁOpenAIProviderǁ__init____mutmut_4, 
        'xǁOpenAIProviderǁ__init____mutmut_5': xǁOpenAIProviderǁ__init____mutmut_5, 
        'xǁOpenAIProviderǁ__init____mutmut_6': xǁOpenAIProviderǁ__init____mutmut_6, 
        'xǁOpenAIProviderǁ__init____mutmut_7': xǁOpenAIProviderǁ__init____mutmut_7, 
        'xǁOpenAIProviderǁ__init____mutmut_8': xǁOpenAIProviderǁ__init____mutmut_8, 
        'xǁOpenAIProviderǁ__init____mutmut_9': xǁOpenAIProviderǁ__init____mutmut_9, 
        'xǁOpenAIProviderǁ__init____mutmut_10': xǁOpenAIProviderǁ__init____mutmut_10, 
        'xǁOpenAIProviderǁ__init____mutmut_11': xǁOpenAIProviderǁ__init____mutmut_11, 
        'xǁOpenAIProviderǁ__init____mutmut_12': xǁOpenAIProviderǁ__init____mutmut_12, 
        'xǁOpenAIProviderǁ__init____mutmut_13': xǁOpenAIProviderǁ__init____mutmut_13, 
        'xǁOpenAIProviderǁ__init____mutmut_14': xǁOpenAIProviderǁ__init____mutmut_14, 
        'xǁOpenAIProviderǁ__init____mutmut_15': xǁOpenAIProviderǁ__init____mutmut_15, 
        'xǁOpenAIProviderǁ__init____mutmut_16': xǁOpenAIProviderǁ__init____mutmut_16, 
        'xǁOpenAIProviderǁ__init____mutmut_17': xǁOpenAIProviderǁ__init____mutmut_17, 
        'xǁOpenAIProviderǁ__init____mutmut_18': xǁOpenAIProviderǁ__init____mutmut_18, 
        'xǁOpenAIProviderǁ__init____mutmut_19': xǁOpenAIProviderǁ__init____mutmut_19, 
        'xǁOpenAIProviderǁ__init____mutmut_20': xǁOpenAIProviderǁ__init____mutmut_20, 
        'xǁOpenAIProviderǁ__init____mutmut_21': xǁOpenAIProviderǁ__init____mutmut_21, 
        'xǁOpenAIProviderǁ__init____mutmut_22': xǁOpenAIProviderǁ__init____mutmut_22, 
        'xǁOpenAIProviderǁ__init____mutmut_23': xǁOpenAIProviderǁ__init____mutmut_23, 
        'xǁOpenAIProviderǁ__init____mutmut_24': xǁOpenAIProviderǁ__init____mutmut_24, 
        'xǁOpenAIProviderǁ__init____mutmut_25': xǁOpenAIProviderǁ__init____mutmut_25, 
        'xǁOpenAIProviderǁ__init____mutmut_26': xǁOpenAIProviderǁ__init____mutmut_26, 
        'xǁOpenAIProviderǁ__init____mutmut_27': xǁOpenAIProviderǁ__init____mutmut_27, 
        'xǁOpenAIProviderǁ__init____mutmut_28': xǁOpenAIProviderǁ__init____mutmut_28, 
        'xǁOpenAIProviderǁ__init____mutmut_29': xǁOpenAIProviderǁ__init____mutmut_29, 
        'xǁOpenAIProviderǁ__init____mutmut_30': xǁOpenAIProviderǁ__init____mutmut_30, 
        'xǁOpenAIProviderǁ__init____mutmut_31': xǁOpenAIProviderǁ__init____mutmut_31, 
        'xǁOpenAIProviderǁ__init____mutmut_32': xǁOpenAIProviderǁ__init____mutmut_32, 
        'xǁOpenAIProviderǁ__init____mutmut_33': xǁOpenAIProviderǁ__init____mutmut_33
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOpenAIProviderǁ__init____mutmut_orig)
    xǁOpenAIProviderǁ__init____mutmut_orig.__name__ = 'xǁOpenAIProviderǁ__init__'
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_orig(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_1(self) -> str:
        """Return the provider name."""
        if self.base_url or 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_2(self) -> str:
        """Return the provider name."""
        if self.base_url and 'XXdeepseekXX' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_3(self) -> str:
        """Return the provider name."""
        if self.base_url and 'DEEPSEEK' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_4(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' not in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_5(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.upper():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_6(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'XXdeepseekXX'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_7(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'DEEPSEEK'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_8(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'XXopenai-compatibleXX'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_9(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'OPENAI-COMPATIBLE'
        return 'openai'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_10(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'XXopenaiXX'
        
    def xǁOpenAIProviderǁ_get_provider_name__mutmut_11(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'OPENAI'
        
    
    xǁOpenAIProviderǁ_get_provider_name__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁ_get_provider_name__mutmut_1': xǁOpenAIProviderǁ_get_provider_name__mutmut_1, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_2': xǁOpenAIProviderǁ_get_provider_name__mutmut_2, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_3': xǁOpenAIProviderǁ_get_provider_name__mutmut_3, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_4': xǁOpenAIProviderǁ_get_provider_name__mutmut_4, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_5': xǁOpenAIProviderǁ_get_provider_name__mutmut_5, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_6': xǁOpenAIProviderǁ_get_provider_name__mutmut_6, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_7': xǁOpenAIProviderǁ_get_provider_name__mutmut_7, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_8': xǁOpenAIProviderǁ_get_provider_name__mutmut_8, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_9': xǁOpenAIProviderǁ_get_provider_name__mutmut_9, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_10': xǁOpenAIProviderǁ_get_provider_name__mutmut_10, 
        'xǁOpenAIProviderǁ_get_provider_name__mutmut_11': xǁOpenAIProviderǁ_get_provider_name__mutmut_11
    }
    
    def _get_provider_name(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁ_get_provider_name__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁ_get_provider_name__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_provider_name.__signature__ = _mutmut_signature(xǁOpenAIProviderǁ_get_provider_name__mutmut_orig)
    xǁOpenAIProviderǁ_get_provider_name__mutmut_orig.__name__ = 'xǁOpenAIProviderǁ_get_provider_name'
    def xǁOpenAIProviderǁ_setup_client__mutmut_orig(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_1(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = None
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_2(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'XXapi_keyXX': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_3(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'API_KEY': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_4(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key and os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_5(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv(None),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_6(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('XXOPENAI_API_KEYXX'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_7(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('openai_api_key'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_8(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'XXmax_retriesXX': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_9(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'MAX_RETRIES': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_10(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'XXtimeoutXX': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_11(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'TIMEOUT': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_12(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = None
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_13(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['XXbase_urlXX'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_14(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['BASE_URL'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_15(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = None
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_16(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['XXorganizationXX'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_17(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['ORGANIZATION'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_18(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = None
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_19(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['XXprojectXX'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_20(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['PROJECT'] = self.project
            
        self.client = OpenAI(**client_kwargs)
        
    def xǁOpenAIProviderǁ_setup_client__mutmut_21(self) -> None:
        """Setup the OpenAI client."""
        client_kwargs = {
            'api_key': self.api_key or os.getenv('OPENAI_API_KEY'),
            'max_retries': self.max_retries,
            'timeout': self.timeout,
        }
        
        if self.base_url:
            client_kwargs['base_url'] = self.base_url
            
        if self.organization:
            client_kwargs['organization'] = self.organization
            
        if self.project:
            client_kwargs['project'] = self.project
            
        self.client = None
        
    
    xǁOpenAIProviderǁ_setup_client__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁ_setup_client__mutmut_1': xǁOpenAIProviderǁ_setup_client__mutmut_1, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_2': xǁOpenAIProviderǁ_setup_client__mutmut_2, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_3': xǁOpenAIProviderǁ_setup_client__mutmut_3, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_4': xǁOpenAIProviderǁ_setup_client__mutmut_4, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_5': xǁOpenAIProviderǁ_setup_client__mutmut_5, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_6': xǁOpenAIProviderǁ_setup_client__mutmut_6, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_7': xǁOpenAIProviderǁ_setup_client__mutmut_7, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_8': xǁOpenAIProviderǁ_setup_client__mutmut_8, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_9': xǁOpenAIProviderǁ_setup_client__mutmut_9, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_10': xǁOpenAIProviderǁ_setup_client__mutmut_10, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_11': xǁOpenAIProviderǁ_setup_client__mutmut_11, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_12': xǁOpenAIProviderǁ_setup_client__mutmut_12, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_13': xǁOpenAIProviderǁ_setup_client__mutmut_13, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_14': xǁOpenAIProviderǁ_setup_client__mutmut_14, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_15': xǁOpenAIProviderǁ_setup_client__mutmut_15, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_16': xǁOpenAIProviderǁ_setup_client__mutmut_16, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_17': xǁOpenAIProviderǁ_setup_client__mutmut_17, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_18': xǁOpenAIProviderǁ_setup_client__mutmut_18, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_19': xǁOpenAIProviderǁ_setup_client__mutmut_19, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_20': xǁOpenAIProviderǁ_setup_client__mutmut_20, 
        'xǁOpenAIProviderǁ_setup_client__mutmut_21': xǁOpenAIProviderǁ_setup_client__mutmut_21
    }
    
    def _setup_client(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁ_setup_client__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁ_setup_client__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _setup_client.__signature__ = _mutmut_signature(xǁOpenAIProviderǁ_setup_client__mutmut_orig)
    xǁOpenAIProviderǁ_setup_client__mutmut_orig.__name__ = 'xǁOpenAIProviderǁ_setup_client'
    def xǁOpenAIProviderǁgenerate_response__mutmut_orig(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_1(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = None
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_2(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(None, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_3(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, None)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_4(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_5(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, )
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_6(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_7(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'XXtemperatureXX', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_8(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'TEMPERATURE', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_9(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'XXmax_tokensXX', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_10(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'MAX_TOKENS', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_11(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'XXtop_pXX', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_12(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'TOP_P', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_13(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'XXfrequency_penaltyXX', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_14(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'FREQUENCY_PENALTY', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_15(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'XXpresence_penaltyXX', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_16(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'PRESENCE_PENALTY', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_17(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'XXstopXX', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_18(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'STOP', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_19(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'XXstreamXX', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_20(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'STREAM', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_21(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'XXlogit_biasXX',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_22(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'LOGIT_BIAS',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_23(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'XXmax_completion_tokensXX', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_24(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'MAX_COMPLETION_TOKENS', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_25(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'XXnXX', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_26(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'N', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_27(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'XXresponse_formatXX', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_28(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'RESPONSE_FORMAT', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_29(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'XXseedXX',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_30(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'SEED',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_31(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'XXservice_tierXX', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_32(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'SERVICE_TIER', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_33(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'XXstream_optionsXX', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_34(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'STREAM_OPTIONS', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_35(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'XXtop_logprobsXX', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_36(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'TOP_LOGPROBS', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_37(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'XXuserXX'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_38(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'USER'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_39(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_40(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_41(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
        }
        
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_params}
        
        # Prepare request parameters
        request_params = None
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_42(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_43(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_44(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_45(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_46(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_47(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_48(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_49(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_50(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_51(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_52(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_53(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_54(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_55(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_56(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_57(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_58(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_59(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_60(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_61(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_62(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_63(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_64(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_65(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_66(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    def xǁOpenAIProviderǁgenerate_response__mutmut_67(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using OpenAI's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions  
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Filter out unsupported parameters for OpenAI
        supported_params = {
            'temperature', 'max_tokens', 'top_p', 'frequency_penalty', 
            'presence_penalty', 'stop', 'stream', 'logit_bias',
            'max_completion_tokens', 'n', 'response_format', 'seed',
            'service_tier', 'stream_options', 'top_logprobs', 'user'
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
            
    
    xǁOpenAIProviderǁgenerate_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁgenerate_response__mutmut_1': xǁOpenAIProviderǁgenerate_response__mutmut_1, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_2': xǁOpenAIProviderǁgenerate_response__mutmut_2, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_3': xǁOpenAIProviderǁgenerate_response__mutmut_3, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_4': xǁOpenAIProviderǁgenerate_response__mutmut_4, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_5': xǁOpenAIProviderǁgenerate_response__mutmut_5, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_6': xǁOpenAIProviderǁgenerate_response__mutmut_6, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_7': xǁOpenAIProviderǁgenerate_response__mutmut_7, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_8': xǁOpenAIProviderǁgenerate_response__mutmut_8, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_9': xǁOpenAIProviderǁgenerate_response__mutmut_9, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_10': xǁOpenAIProviderǁgenerate_response__mutmut_10, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_11': xǁOpenAIProviderǁgenerate_response__mutmut_11, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_12': xǁOpenAIProviderǁgenerate_response__mutmut_12, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_13': xǁOpenAIProviderǁgenerate_response__mutmut_13, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_14': xǁOpenAIProviderǁgenerate_response__mutmut_14, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_15': xǁOpenAIProviderǁgenerate_response__mutmut_15, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_16': xǁOpenAIProviderǁgenerate_response__mutmut_16, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_17': xǁOpenAIProviderǁgenerate_response__mutmut_17, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_18': xǁOpenAIProviderǁgenerate_response__mutmut_18, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_19': xǁOpenAIProviderǁgenerate_response__mutmut_19, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_20': xǁOpenAIProviderǁgenerate_response__mutmut_20, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_21': xǁOpenAIProviderǁgenerate_response__mutmut_21, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_22': xǁOpenAIProviderǁgenerate_response__mutmut_22, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_23': xǁOpenAIProviderǁgenerate_response__mutmut_23, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_24': xǁOpenAIProviderǁgenerate_response__mutmut_24, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_25': xǁOpenAIProviderǁgenerate_response__mutmut_25, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_26': xǁOpenAIProviderǁgenerate_response__mutmut_26, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_27': xǁOpenAIProviderǁgenerate_response__mutmut_27, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_28': xǁOpenAIProviderǁgenerate_response__mutmut_28, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_29': xǁOpenAIProviderǁgenerate_response__mutmut_29, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_30': xǁOpenAIProviderǁgenerate_response__mutmut_30, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_31': xǁOpenAIProviderǁgenerate_response__mutmut_31, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_32': xǁOpenAIProviderǁgenerate_response__mutmut_32, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_33': xǁOpenAIProviderǁgenerate_response__mutmut_33, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_34': xǁOpenAIProviderǁgenerate_response__mutmut_34, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_35': xǁOpenAIProviderǁgenerate_response__mutmut_35, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_36': xǁOpenAIProviderǁgenerate_response__mutmut_36, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_37': xǁOpenAIProviderǁgenerate_response__mutmut_37, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_38': xǁOpenAIProviderǁgenerate_response__mutmut_38, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_39': xǁOpenAIProviderǁgenerate_response__mutmut_39, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_40': xǁOpenAIProviderǁgenerate_response__mutmut_40, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_41': xǁOpenAIProviderǁgenerate_response__mutmut_41, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_42': xǁOpenAIProviderǁgenerate_response__mutmut_42, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_43': xǁOpenAIProviderǁgenerate_response__mutmut_43, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_44': xǁOpenAIProviderǁgenerate_response__mutmut_44, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_45': xǁOpenAIProviderǁgenerate_response__mutmut_45, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_46': xǁOpenAIProviderǁgenerate_response__mutmut_46, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_47': xǁOpenAIProviderǁgenerate_response__mutmut_47, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_48': xǁOpenAIProviderǁgenerate_response__mutmut_48, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_49': xǁOpenAIProviderǁgenerate_response__mutmut_49, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_50': xǁOpenAIProviderǁgenerate_response__mutmut_50, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_51': xǁOpenAIProviderǁgenerate_response__mutmut_51, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_52': xǁOpenAIProviderǁgenerate_response__mutmut_52, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_53': xǁOpenAIProviderǁgenerate_response__mutmut_53, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_54': xǁOpenAIProviderǁgenerate_response__mutmut_54, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_55': xǁOpenAIProviderǁgenerate_response__mutmut_55, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_56': xǁOpenAIProviderǁgenerate_response__mutmut_56, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_57': xǁOpenAIProviderǁgenerate_response__mutmut_57, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_58': xǁOpenAIProviderǁgenerate_response__mutmut_58, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_59': xǁOpenAIProviderǁgenerate_response__mutmut_59, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_60': xǁOpenAIProviderǁgenerate_response__mutmut_60, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_61': xǁOpenAIProviderǁgenerate_response__mutmut_61, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_62': xǁOpenAIProviderǁgenerate_response__mutmut_62, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_63': xǁOpenAIProviderǁgenerate_response__mutmut_63, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_64': xǁOpenAIProviderǁgenerate_response__mutmut_64, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_65': xǁOpenAIProviderǁgenerate_response__mutmut_65, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_66': xǁOpenAIProviderǁgenerate_response__mutmut_66, 
        'xǁOpenAIProviderǁgenerate_response__mutmut_67': xǁOpenAIProviderǁgenerate_response__mutmut_67
    }
    
    def generate_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁgenerate_response__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁgenerate_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_response.__signature__ = _mutmut_signature(xǁOpenAIProviderǁgenerate_response__mutmut_orig)
    xǁOpenAIProviderǁgenerate_response__mutmut_orig.__name__ = 'xǁOpenAIProviderǁgenerate_response'
    def xǁOpenAIProviderǁ_convert_response__mutmut_orig(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_1(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = None
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_2(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[1].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_3(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = None
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_4(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = None
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_5(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = None
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_6(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = None
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_7(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(None)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_8(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(None) from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_9(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_10(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = None
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_11(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_12(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_13(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_14(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_15(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_16(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_17(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_18(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_19(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_20(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_21(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_22(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_23(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_24(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_25(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_26(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_27(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_28(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_29(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_30(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_31(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_32(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_33(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_34(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_35(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_36(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_37(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_38(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_39(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    def xǁOpenAIProviderǁ_convert_response__mutmut_40(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments safely
                arguments = tc.function.arguments
                if isinstance(arguments, str):
                    try:
                        import json
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Failed to parse tool arguments as JSON: {arguments}") from e
                elif not isinstance(arguments, dict):
                    arguments = {}
                    
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
        
    
    xǁOpenAIProviderǁ_convert_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁ_convert_response__mutmut_1': xǁOpenAIProviderǁ_convert_response__mutmut_1, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_2': xǁOpenAIProviderǁ_convert_response__mutmut_2, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_3': xǁOpenAIProviderǁ_convert_response__mutmut_3, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_4': xǁOpenAIProviderǁ_convert_response__mutmut_4, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_5': xǁOpenAIProviderǁ_convert_response__mutmut_5, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_6': xǁOpenAIProviderǁ_convert_response__mutmut_6, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_7': xǁOpenAIProviderǁ_convert_response__mutmut_7, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_8': xǁOpenAIProviderǁ_convert_response__mutmut_8, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_9': xǁOpenAIProviderǁ_convert_response__mutmut_9, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_10': xǁOpenAIProviderǁ_convert_response__mutmut_10, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_11': xǁOpenAIProviderǁ_convert_response__mutmut_11, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_12': xǁOpenAIProviderǁ_convert_response__mutmut_12, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_13': xǁOpenAIProviderǁ_convert_response__mutmut_13, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_14': xǁOpenAIProviderǁ_convert_response__mutmut_14, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_15': xǁOpenAIProviderǁ_convert_response__mutmut_15, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_16': xǁOpenAIProviderǁ_convert_response__mutmut_16, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_17': xǁOpenAIProviderǁ_convert_response__mutmut_17, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_18': xǁOpenAIProviderǁ_convert_response__mutmut_18, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_19': xǁOpenAIProviderǁ_convert_response__mutmut_19, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_20': xǁOpenAIProviderǁ_convert_response__mutmut_20, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_21': xǁOpenAIProviderǁ_convert_response__mutmut_21, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_22': xǁOpenAIProviderǁ_convert_response__mutmut_22, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_23': xǁOpenAIProviderǁ_convert_response__mutmut_23, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_24': xǁOpenAIProviderǁ_convert_response__mutmut_24, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_25': xǁOpenAIProviderǁ_convert_response__mutmut_25, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_26': xǁOpenAIProviderǁ_convert_response__mutmut_26, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_27': xǁOpenAIProviderǁ_convert_response__mutmut_27, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_28': xǁOpenAIProviderǁ_convert_response__mutmut_28, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_29': xǁOpenAIProviderǁ_convert_response__mutmut_29, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_30': xǁOpenAIProviderǁ_convert_response__mutmut_30, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_31': xǁOpenAIProviderǁ_convert_response__mutmut_31, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_32': xǁOpenAIProviderǁ_convert_response__mutmut_32, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_33': xǁOpenAIProviderǁ_convert_response__mutmut_33, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_34': xǁOpenAIProviderǁ_convert_response__mutmut_34, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_35': xǁOpenAIProviderǁ_convert_response__mutmut_35, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_36': xǁOpenAIProviderǁ_convert_response__mutmut_36, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_37': xǁOpenAIProviderǁ_convert_response__mutmut_37, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_38': xǁOpenAIProviderǁ_convert_response__mutmut_38, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_39': xǁOpenAIProviderǁ_convert_response__mutmut_39, 
        'xǁOpenAIProviderǁ_convert_response__mutmut_40': xǁOpenAIProviderǁ_convert_response__mutmut_40
    }
    
    def _convert_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁ_convert_response__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁ_convert_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _convert_response.__signature__ = _mutmut_signature(xǁOpenAIProviderǁ_convert_response__mutmut_orig)
    xǁOpenAIProviderǁ_convert_response__mutmut_orig.__name__ = 'xǁOpenAIProviderǁ_convert_response'
    def xǁOpenAIProviderǁsupports_tool_calling__mutmut_orig(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.tool_calling if capabilities else False
        
    def xǁOpenAIProviderǁsupports_tool_calling__mutmut_1(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.tool_calling if capabilities else False
        
    def xǁOpenAIProviderǁsupports_tool_calling__mutmut_2(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.tool_calling if capabilities else False
        
    def xǁOpenAIProviderǁsupports_tool_calling__mutmut_3(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.tool_calling if capabilities else True
        
    
    xǁOpenAIProviderǁsupports_tool_calling__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁsupports_tool_calling__mutmut_1': xǁOpenAIProviderǁsupports_tool_calling__mutmut_1, 
        'xǁOpenAIProviderǁsupports_tool_calling__mutmut_2': xǁOpenAIProviderǁsupports_tool_calling__mutmut_2, 
        'xǁOpenAIProviderǁsupports_tool_calling__mutmut_3': xǁOpenAIProviderǁsupports_tool_calling__mutmut_3
    }
    
    def supports_tool_calling(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁsupports_tool_calling__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁsupports_tool_calling__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_tool_calling.__signature__ = _mutmut_signature(xǁOpenAIProviderǁsupports_tool_calling__mutmut_orig)
    xǁOpenAIProviderǁsupports_tool_calling__mutmut_orig.__name__ = 'xǁOpenAIProviderǁsupports_tool_calling'
    def xǁOpenAIProviderǁsupports_parallel_tools__mutmut_orig(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else False
    def xǁOpenAIProviderǁsupports_parallel_tools__mutmut_1(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.supports_parallel_tools if capabilities else False
    def xǁOpenAIProviderǁsupports_parallel_tools__mutmut_2(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.supports_parallel_tools if capabilities else False
    def xǁOpenAIProviderǁsupports_parallel_tools__mutmut_3(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else True
    
    xǁOpenAIProviderǁsupports_parallel_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁsupports_parallel_tools__mutmut_1': xǁOpenAIProviderǁsupports_parallel_tools__mutmut_1, 
        'xǁOpenAIProviderǁsupports_parallel_tools__mutmut_2': xǁOpenAIProviderǁsupports_parallel_tools__mutmut_2, 
        'xǁOpenAIProviderǁsupports_parallel_tools__mutmut_3': xǁOpenAIProviderǁsupports_parallel_tools__mutmut_3
    }
    
    def supports_parallel_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁsupports_parallel_tools__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁsupports_parallel_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_parallel_tools.__signature__ = _mutmut_signature(xǁOpenAIProviderǁsupports_parallel_tools__mutmut_orig)
    xǁOpenAIProviderǁsupports_parallel_tools__mutmut_orig.__name__ = 'xǁOpenAIProviderǁsupports_parallel_tools'
    
    def xǁOpenAIProviderǁsupports_images__mutmut_orig(self) -> bool:
        """Check if the model supports image input."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_image_input if capabilities else False
        
    
    def xǁOpenAIProviderǁsupports_images__mutmut_1(self) -> bool:
        """Check if the model supports image input."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.supports_image_input if capabilities else False
        
    
    def xǁOpenAIProviderǁsupports_images__mutmut_2(self) -> bool:
        """Check if the model supports image input."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.supports_image_input if capabilities else False
        
    
    def xǁOpenAIProviderǁsupports_images__mutmut_3(self) -> bool:
        """Check if the model supports image input."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_image_input if capabilities else True
        
    
    xǁOpenAIProviderǁsupports_images__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁsupports_images__mutmut_1': xǁOpenAIProviderǁsupports_images__mutmut_1, 
        'xǁOpenAIProviderǁsupports_images__mutmut_2': xǁOpenAIProviderǁsupports_images__mutmut_2, 
        'xǁOpenAIProviderǁsupports_images__mutmut_3': xǁOpenAIProviderǁsupports_images__mutmut_3
    }
    
    def supports_images(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁsupports_images__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁsupports_images__mutmut_mutants"), args, kwargs, self)
        return result 
    
    supports_images.__signature__ = _mutmut_signature(xǁOpenAIProviderǁsupports_images__mutmut_orig)
    xǁOpenAIProviderǁsupports_images__mutmut_orig.__name__ = 'xǁOpenAIProviderǁsupports_images'
    def xǁOpenAIProviderǁget_max_tokens__mutmut_orig(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.output_limit if capabilities else None
        
    def xǁOpenAIProviderǁget_max_tokens__mutmut_1(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.output_limit if capabilities else None
        
    def xǁOpenAIProviderǁget_max_tokens__mutmut_2(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.output_limit if capabilities else None
        
    
    xǁOpenAIProviderǁget_max_tokens__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁget_max_tokens__mutmut_1': xǁOpenAIProviderǁget_max_tokens__mutmut_1, 
        'xǁOpenAIProviderǁget_max_tokens__mutmut_2': xǁOpenAIProviderǁget_max_tokens__mutmut_2
    }
    
    def get_max_tokens(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁget_max_tokens__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁget_max_tokens__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_max_tokens.__signature__ = _mutmut_signature(xǁOpenAIProviderǁget_max_tokens__mutmut_orig)
    xǁOpenAIProviderǁget_max_tokens__mutmut_orig.__name__ = 'xǁOpenAIProviderǁget_max_tokens'
    def xǁOpenAIProviderǁget_context_window__mutmut_orig(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.context_limit if capabilities else None
    def xǁOpenAIProviderǁget_context_window__mutmut_1(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = None
        return capabilities.context_limit if capabilities else None
    def xǁOpenAIProviderǁget_context_window__mutmut_2(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(None)
        return capabilities.context_limit if capabilities else None
    
    xǁOpenAIProviderǁget_context_window__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIProviderǁget_context_window__mutmut_1': xǁOpenAIProviderǁget_context_window__mutmut_1, 
        'xǁOpenAIProviderǁget_context_window__mutmut_2': xǁOpenAIProviderǁget_context_window__mutmut_2
    }
    
    def get_context_window(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIProviderǁget_context_window__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIProviderǁget_context_window__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_context_window.__signature__ = _mutmut_signature(xǁOpenAIProviderǁget_context_window__mutmut_orig)
    xǁOpenAIProviderǁget_context_window__mutmut_orig.__name__ = 'xǁOpenAIProviderǁget_context_window'


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek provider using OpenAI-compatible API."""
    
    def xǁDeepSeekProviderǁ__init____mutmut_orig(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_1(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault(None, 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_2(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', None)
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_3(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_4(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', )
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_5(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('XXbase_urlXX', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_6(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('BASE_URL', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_7(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'XXhttps://api.deepseek.comXX')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_8(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'HTTPS://API.DEEPSEEK.COM')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_9(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_10(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = None
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_11(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv(None)
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_12(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('XXDEEPSEEK_API_KEYXX')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_13(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('deepseek_api_key')
            
        super().__init__(model_name, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_14(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(None, api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_15(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, None, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_16(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(api_key, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_17(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, **kwargs)
        
    
    def xǁDeepSeekProviderǁ__init____mutmut_18(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize DeepSeek provider.
        
        Args:
            model_name: Name of the DeepSeek model
            api_key: DeepSeek API key (will use DEEPSEEK_API_KEY env var if not provided)
            **kwargs: Additional configuration
        """
        # Set DeepSeek-specific defaults
        kwargs.setdefault('base_url', 'https://api.deepseek.com')
        
        # Use DeepSeek API key if available
        if not api_key:
            api_key = os.getenv('DEEPSEEK_API_KEY')
            
        super().__init__(model_name, api_key, )
        
    
    xǁDeepSeekProviderǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDeepSeekProviderǁ__init____mutmut_1': xǁDeepSeekProviderǁ__init____mutmut_1, 
        'xǁDeepSeekProviderǁ__init____mutmut_2': xǁDeepSeekProviderǁ__init____mutmut_2, 
        'xǁDeepSeekProviderǁ__init____mutmut_3': xǁDeepSeekProviderǁ__init____mutmut_3, 
        'xǁDeepSeekProviderǁ__init____mutmut_4': xǁDeepSeekProviderǁ__init____mutmut_4, 
        'xǁDeepSeekProviderǁ__init____mutmut_5': xǁDeepSeekProviderǁ__init____mutmut_5, 
        'xǁDeepSeekProviderǁ__init____mutmut_6': xǁDeepSeekProviderǁ__init____mutmut_6, 
        'xǁDeepSeekProviderǁ__init____mutmut_7': xǁDeepSeekProviderǁ__init____mutmut_7, 
        'xǁDeepSeekProviderǁ__init____mutmut_8': xǁDeepSeekProviderǁ__init____mutmut_8, 
        'xǁDeepSeekProviderǁ__init____mutmut_9': xǁDeepSeekProviderǁ__init____mutmut_9, 
        'xǁDeepSeekProviderǁ__init____mutmut_10': xǁDeepSeekProviderǁ__init____mutmut_10, 
        'xǁDeepSeekProviderǁ__init____mutmut_11': xǁDeepSeekProviderǁ__init____mutmut_11, 
        'xǁDeepSeekProviderǁ__init____mutmut_12': xǁDeepSeekProviderǁ__init____mutmut_12, 
        'xǁDeepSeekProviderǁ__init____mutmut_13': xǁDeepSeekProviderǁ__init____mutmut_13, 
        'xǁDeepSeekProviderǁ__init____mutmut_14': xǁDeepSeekProviderǁ__init____mutmut_14, 
        'xǁDeepSeekProviderǁ__init____mutmut_15': xǁDeepSeekProviderǁ__init____mutmut_15, 
        'xǁDeepSeekProviderǁ__init____mutmut_16': xǁDeepSeekProviderǁ__init____mutmut_16, 
        'xǁDeepSeekProviderǁ__init____mutmut_17': xǁDeepSeekProviderǁ__init____mutmut_17, 
        'xǁDeepSeekProviderǁ__init____mutmut_18': xǁDeepSeekProviderǁ__init____mutmut_18
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDeepSeekProviderǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDeepSeekProviderǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDeepSeekProviderǁ__init____mutmut_orig)
    xǁDeepSeekProviderǁ__init____mutmut_orig.__name__ = 'xǁDeepSeekProviderǁ__init__'
    def xǁDeepSeekProviderǁ_get_provider_name__mutmut_orig(self) -> str:
        """Return the provider name."""
        return 'deepseek'
    def xǁDeepSeekProviderǁ_get_provider_name__mutmut_1(self) -> str:
        """Return the provider name."""
        return 'XXdeepseekXX'
    def xǁDeepSeekProviderǁ_get_provider_name__mutmut_2(self) -> str:
        """Return the provider name."""
        return 'DEEPSEEK'
    
    xǁDeepSeekProviderǁ_get_provider_name__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDeepSeekProviderǁ_get_provider_name__mutmut_1': xǁDeepSeekProviderǁ_get_provider_name__mutmut_1, 
        'xǁDeepSeekProviderǁ_get_provider_name__mutmut_2': xǁDeepSeekProviderǁ_get_provider_name__mutmut_2
    }
    
    def _get_provider_name(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDeepSeekProviderǁ_get_provider_name__mutmut_orig"), object.__getattribute__(self, "xǁDeepSeekProviderǁ_get_provider_name__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_provider_name.__signature__ = _mutmut_signature(xǁDeepSeekProviderǁ_get_provider_name__mutmut_orig)
    xǁDeepSeekProviderǁ_get_provider_name__mutmut_orig.__name__ = 'xǁDeepSeekProviderǁ_get_provider_name'