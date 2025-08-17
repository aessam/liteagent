"""
Anthropic provider implementation for LiteAgent.

This provider uses the official Anthropic Python client library.
"""

import os
import time
from typing import Any, Dict, List, Optional

try:
    from anthropic import Anthropic
    from anthropic.types import Message, ContentBlock, TextBlock, ToolUseBlock
except ImportError:
    raise ImportError("Anthropic library not installed. Install with: pip install anthropic")

from .base import ProviderInterface, ProviderResponse, ToolCall
from ..utils import logger


class AnthropicProvider(ProviderInterface):
    """Anthropic provider using the official Anthropic client library."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Anthropic provider.
        
        Args:
            model_name: Name of the Anthropic model (e.g., 'claude-3-5-sonnet-20241022')
            api_key: Anthropic API key (will use ANTHROPIC_API_KEY env var if not provided)
            **kwargs: Additional configuration
                - max_retries: Maximum number of retries
                - timeout: Request timeout in seconds
        """
        self.max_retries = kwargs.get('max_retries', 3)
        self.timeout = kwargs.get('timeout', 60)
        
        super().__init__(model_name, api_key, **kwargs)
        
    def _get_provider_name(self) -> str:
        """Return the provider name."""
        return 'anthropic'
        
    def _setup_client(self) -> None:
        """Setup the Anthropic client."""
        self.client = Anthropic(
            api_key=self.api_key or os.getenv('ANTHROPIC_API_KEY'),
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
        Generate a response using Anthropic's messages API.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional parameters like temperature, max_tokens, etc.
            
        Returns:
            ProviderResponse: Standardized response object
        """
        start_time = time.time()
        self._log_request(messages, tools)
        
        # Convert messages to Anthropic format
        anthropic_messages = self._convert_messages(messages)
        
        # Extract system message if present
        system_message = None
        if anthropic_messages and anthropic_messages[0].get('role') == 'system':
            system_message = anthropic_messages.pop(0)['content']
            
        # Prepare request parameters
        request_params = {
            'model': self.model_name,
            'messages': anthropic_messages,
            'max_tokens': kwargs.get('max_tokens', 4096),  # Required for Anthropic
        }
        
        if system_message:
            request_params['system'] = system_message
            
        # Add other optional parameters
        if 'temperature' in kwargs:
            request_params['temperature'] = kwargs['temperature']
            
        # Add tools if provided and model supports them
        if tools and self.supports_tool_calling():
            request_params['tools'] = self._convert_tools(tools)
        
        # Add caching support if enabled and model supports it
        if kwargs.get('enable_caching', False) and self.supports_caching():
            # Mark system message for caching if it's long enough
            if system_message and len(system_message) > 1000:
                request_params['system'] = [
                    {
                        "type": "text",
                        "text": system_message,
                        "cache_control": {"type": "ephemeral"}
                    }
                ]
            
            # Mark long messages for caching
            for message in request_params['messages']:
                if isinstance(message.get('content'), str) and len(message['content']) > 1000:
                    message['content'] = [
                        {
                            "type": "text", 
                            "text": message['content'],
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                elif isinstance(message.get('content'), list):
                    # For multimodal content, mark text parts for caching if long enough
                    for content_item in message['content']:
                        if (content_item.get('type') == 'text' and 
                            len(content_item.get('text', '')) > 1000):
                            content_item['cache_control'] = {"type": "ephemeral"}
            
        try:
            # Make the API call
            response: Message = self.client.messages.create(**request_params)
            
            # Convert to standardized format
            provider_response = self._convert_response(response)
            
            elapsed_time = time.time() - start_time
            self._log_response(provider_response, elapsed_time)
            
            return provider_response
            
        except Exception as e:
            self._handle_error(e, "during message creation")
            
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert messages to Anthropic format."""
        anthropic_messages = []
        
        for msg in messages:
            role = msg['role']
            content = msg['content']
            
            # Skip function/tool role messages - they get embedded differently in Anthropic
            if role in ['function', 'tool']:
                continue
                
            # Convert assistant messages with tool calls
            if role == 'assistant' and 'tool_calls' in msg:
                # Create content blocks for text and tool uses
                content_blocks = []
                
                if content:
                    content_blocks.append({'type': 'text', 'text': content})
                    
                for tool_call in msg['tool_calls']:
                    # Ensure arguments are a dictionary for Anthropic API
                    arguments = tool_call['function']['arguments']
                    if isinstance(arguments, str):
                        try:
                            import json
                            arguments = json.loads(arguments)
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse tool arguments: {arguments}")
                            arguments = {}
                    elif not isinstance(arguments, dict):
                        arguments = {}
                        
                    content_blocks.append({
                        'type': 'tool_use',
                        'id': tool_call['id'],
                        'name': tool_call['function']['name'],
                        'input': arguments
                    })
                    
                anthropic_messages.append({
                    'role': 'assistant',
                    'content': content_blocks
                })
            else:
                # Handle multimodal content (text + images)
                if isinstance(content, list):
                    # Already in multimodal format - convert for Anthropic
                    anthropic_content = []
                    for item in content:
                        if item['type'] == 'text':
                            anthropic_content.append({
                                'type': 'text',
                                'text': item['text']
                            })
                        elif item['type'] == 'image_url':
                            # Convert OpenAI image format to Anthropic format
                            image_url = item['image_url']['url']
                            if image_url.startswith('data:'):
                                # Base64 encoded image
                                # Extract media type and data
                                parts = image_url.split(',', 1)
                                if len(parts) == 2:
                                    header = parts[0]  # data:image/jpeg;base64
                                    data = parts[1]
                                    # Extract media type
                                    media_type = header.split(';')[0].replace('data:', '')
                                    anthropic_content.append({
                                        'type': 'image',
                                        'source': {
                                            'type': 'base64',
                                            'media_type': media_type,
                                            'data': data
                                        }
                                    })
                            else:
                                # External URL - Anthropic doesn't support external URLs directly
                                # Add a text description instead
                                anthropic_content.append({
                                    'type': 'text',
                                    'text': f'[Image URL provided: {image_url}]'
                                })
                    
                    anthropic_messages.append({
                        'role': role,
                        'content': anthropic_content
                    })
                else:
                    # Simple text content
                    anthropic_messages.append({
                        'role': role,
                        'content': content
                    })
                
        return anthropic_messages
        
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tool definitions to Anthropic format."""
        anthropic_tools = []
        
        for tool in tools:
            if 'function' in tool:
                func = tool['function']
                anthropic_tools.append({
                    'name': func['name'],
                    'description': func.get('description', ''),
                    'input_schema': func.get('parameters', {})
                })
            else:
                # Already in Anthropic format
                anthropic_tools.append(tool)
                
        return anthropic_tools
        
    def _convert_response(self, response: Message) -> ProviderResponse:
        """Convert Anthropic response to standardized format."""
        content_text = ""
        tool_calls = []
        
        # Process content blocks
        for block in response.content:
            if isinstance(block, TextBlock):
                content_text += block.text
            elif isinstance(block, ToolUseBlock):
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=block.input
                ))
                
        # Extract usage info
        usage = None
        if response.usage:
            usage = {
                'prompt_tokens': response.usage.input_tokens,
                'completion_tokens': response.usage.output_tokens,
                'total_tokens': response.usage.input_tokens + response.usage.output_tokens,
            }
            
        return ProviderResponse(
            content=content_text if content_text else None,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=response.stop_reason
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
    
    def supports_images(self) -> bool:
        """Check if the model supports image input."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_image_input if capabilities else False
    
    def supports_caching(self) -> bool:
        """Check if the model supports caching."""
        from ..capabilities import get_model_capabilities
        capabilities = get_model_capabilities(self.model_name)
        return capabilities.supports_caching if capabilities else False
        
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