"""
Mistral provider implementation for LiteAgent.

This provider uses the official Mistral Python client library.
"""

import os
import time
from typing import Any, Dict, List, Optional

try:
    from mistralai import Mistral
    from mistralai.models import ChatCompletionResponse
except ImportError:
    raise ImportError("Mistral library not installed. Install with: pip install mistralai")

from .base import ProviderInterface, ProviderResponse, ToolCall
from ..utils import logger


class MistralProvider(ProviderInterface):
    """Mistral provider using the official Mistral client library."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Mistral provider.
        
        Args:
            model_name: Name of the Mistral model (e.g., 'mistral-large-latest')
            api_key: Mistral API key (will use MISTRAL_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    def _get_provider_name(self) -> str:
        """Return the provider name."""
        return 'mistral'
        
    def _setup_client(self) -> None:
        """Setup the Mistral client."""
        self.client = Mistral(
            api_key=self.api_key or os.getenv('MISTRAL_API_KEY'),
            # Note: Mistral client doesn't support max_retries or timeout_ms in constructor
        )
        
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response using Mistral's chat completions API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Process messages for Mistral constraints (ordering, system message handling)
        from ..provider_roles import process_messages_for_provider
        processed_messages = process_messages_for_provider(messages, "mistral")
        
        # Convert messages to Mistral format (handle function -> tool role conversion)
        mistral_messages = self._convert_messages(processed_messages)
        
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': mistral_messages,
        }
        
        # Add optional parameters
        if 'temperature' in kwargs:
            request_params['temperature'] = kwargs['temperature']
        if 'max_tokens' in kwargs:
            request_params['max_tokens'] = kwargs['max_tokens']
        if 'top_p' in kwargs:
            request_params['top_p'] = kwargs['top_p']
            
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
            request_params['tool_choice'] = 'auto'
            
        # Make the API call
        response: ChatCompletionResponse = self.client.chat.complete(**request_params)
        
        # Convert to standardized format
        provider_response = self._convert_response(response)
        
        elapsed_time = time.time() - start_time
        self._log_response(provider_response, elapsed_time)
        
        return provider_response
            
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert messages to Mistral format (function -> tool role)."""
        mistral_messages = []
        
        for msg in messages:
            role = msg['role']
            content = msg['content']
            
            # Convert function role to tool role for Mistral
            if role == 'function':
                mistral_messages.append({
                    'role': 'tool',
                    'content': content,
                    'tool_call_id': msg.get('tool_call_id', msg.get('name', ''))
                })
            else:
                mistral_messages.append(msg)
                
        return mistral_messages
        
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Mistral format."""
        mistral_tools = []
        
        for tool in tools:
            if 'function' in tool:
                # Convert OpenAI-style to Mistral-style
                mistral_tools.append({
                    'type': 'function',
                    'function': tool['function']
                })
            else:
                # Already in correct format
                mistral_tools.append(tool)
                
        return mistral_tools
        
    def _convert_response(self, response: ChatCompletionResponse) -> ProviderResponse:
        """Convert Mistral response to standardized format."""
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