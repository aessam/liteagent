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


class OpenAIProvider(ProviderInterface):
    """OpenAI provider using the official OpenAI client library."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
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
        
    def _get_provider_name(self) -> str:
        """Return the provider name."""
        if self.base_url and 'deepseek' in self.base_url.lower():
            return 'deepseek'
        elif self.base_url:
            return 'openai-compatible'
        return 'openai'
        
    def _setup_client(self) -> None:
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
        
    def generate_response(
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
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': messages,
            **kwargs  # Include any additional parameters
        }
        
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            request_params['tools'] = tools
            request_params['tool_choice'] = 'auto'
            
            # Enable parallel tool calls for supported models
            if self.supports_parallel_tools():
                request_params['parallel_tool_calls'] = True
                
        try:
            # Make the API call
            response: ChatCompletion = self.client.chat.completions.create(**request_params)
            
            # Convert to standardized format
            provider_response = self._convert_response(response)
            
            elapsed_time = time.time() - start_time
            self._log_response(provider_response, elapsed_time)
            
            return provider_response
            
        except Exception as e:
            self._handle_error(e, "during chat completion")
            
    def _convert_response(self, response: ChatCompletion) -> ProviderResponse:
        """Convert OpenAI response to standardized format."""
        message = response.choices[0].message
        
        # Extract content
        content = message.content
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=tc.function.arguments if isinstance(tc.function.arguments, dict) 
                             else eval(tc.function.arguments)  # Parse JSON string if needed
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
        
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        # Most modern OpenAI models support tool calling
        unsupported_models = [
            'text-davinci-003', 'text-davinci-002', 'text-curie-001', 
            'text-babbage-001', 'text-ada-001', 'davinci', 'curie', 'babbage', 'ada'
        ]
        return self.model_name not in unsupported_models
        
    def supports_parallel_tools(self) -> bool:
        """Check if the model supports parallel tool execution."""
        # Most recent OpenAI models support parallel tools
        parallel_supported_models = [
            'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'
        ]
        return any(supported in self.model_name for supported in parallel_supported_models)
        
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        # Common OpenAI model limits
        model_limits = {
            'gpt-4o': 4096,
            'gpt-4o-mini': 16384,
            'gpt-4-turbo': 4096,
            'gpt-4': 8192,
            'gpt-3.5-turbo': 4096,
        }
        
        for model_prefix, limit in model_limits.items():
            if self.model_name.startswith(model_prefix):
                return limit
                
        return None
        
    def get_context_window(self) -> Optional[int]:
        """Get the context window size for this model."""
        # Common OpenAI context windows
        context_windows = {
            'gpt-4o': 128000,
            'gpt-4o-mini': 128000,
            'gpt-4-turbo': 128000,
            'gpt-4': 8192,
            'gpt-3.5-turbo': 16385,
        }
        
        for model_prefix, window in context_windows.items():
            if self.model_name.startswith(model_prefix):
                return window
                
        return None


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek provider using OpenAI-compatible API."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
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
        
    def _get_provider_name(self) -> str:
        """Return the provider name."""
        return 'deepseek'