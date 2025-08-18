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


class OllamaProvider(ProviderInterface):
    """Ollama provider using the official Ollama client library."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
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
        
    def _get_provider_name(self) -> str:
        """Return the provider name."""
        return 'ollama'
        
    def _setup_client(self) -> None:
        """Setup the Ollama client."""
        self.client = Client(host=self.host)
        
    def generate_response(
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
            
    def _supports_native_tools(self) -> bool:
        """Check if the model supports native tool calling."""
        # Modern Ollama supports tool calling for most models
        return True
        
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
        
    def _embed_tools_in_prompt(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
    
    def _preprocess_messages_for_ollama(self, messages: List[Dict]) -> List[Dict]:
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
        
    def _extract_tool_calls_from_text(self, text: str) -> List[ToolCall]:
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
        
    def _convert_response(self, response: Dict[str, Any], tools: Optional[List[Dict]] = None) -> ProviderResponse:
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
        
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        # Ollama models can always support tool calling via prompt embedding
        # even if they don't have native tool support or aren't in the capabilities database
        return True
        
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