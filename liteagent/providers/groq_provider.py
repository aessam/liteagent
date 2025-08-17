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


class GroqProvider(ProviderInterface):
    """Groq provider using the official Groq client library."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
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
        
    def _get_provider_name(self) -> str:
        """Return the provider name."""
        return 'groq'
        
    def _setup_client(self) -> None:
        """Setup the Groq client."""
        self.client = Groq(
            api_key=self.api_key or os.getenv('GROQ_API_KEY'),
            max_retries=self.max_retries,
            timeout=self.timeout,
        )
        
    def generate_response(
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
                logger.warning(f"[{self.provider_name}] Too many tools ({len(tools)}), limiting to 128")
                tools = tools[:128]
                
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
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse tool arguments: {arguments}")
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
        
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.tool_calling if capabilities else False
        
    def supports_parallel_tools(self) -> bool:
        """Check if the model supports parallel tool execution."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_parallel_tools if capabilities else False
        
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.output_limit if capabilities else None
        
    def get_context_window(self) -> Optional[int]:
        """Get the context window size for this model."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.context_limit if capabilities else None