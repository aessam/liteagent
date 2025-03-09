"""
Model interfaces for LiteAgent.

This module provides abstractions for different LLM models with varying capabilities,
particularly around function/tool calling.
"""

import json
import time
import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import litellm
from litellm.exceptions import RateLimitError, APIError, APIConnectionError, Timeout, ServiceUnavailableError

from .tool_calling_types import ToolCallingType, get_tool_calling_type, get_provider_from_model
from .tool_calling import get_tool_calling_handler, get_provider_specific_handler
from .utils import logger, log_completion_request, log_completion_response
from .provider_roles import process_messages_for_provider


class ModelInterface(ABC):
    """Abstract base class for model interfaces."""
    
    def __init__(self, model_name: str, drop_params: bool = True):
        """
        Initialize the model interface.
        
        Args:
            model_name: Name of the model to use
            drop_params: Whether to drop unsupported parameters
        """
        self.model_name = model_name
        self.drop_params = drop_params
        self.provider = get_provider_from_model(model_name)
        self.tool_calling_type = get_tool_calling_type(model_name)
        self.tool_handler = get_provider_specific_handler(self.provider, self.tool_calling_type)
        self.temperature = None  # Default to None, which will use the model's default temperature
        
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Any:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message dictionaries
            functions: Optional list of function definitions
            
        Returns:
            The model's response
        """
        # Prepare kwargs for the API call
        kwargs = {
            "model": self.model_name,
            "messages": messages,
        }
        
        # Add functions if provided and supported
        if functions:
            # Format functions based on tool calling type
            formatted_tools = self.tool_handler.format_tools_for_model(functions)
            
            # Add functions to kwargs based on tool calling type
            if self.tool_calling_type == ToolCallingType.OPENAI:
                # OpenAI-style function calling
                kwargs["tools"] = formatted_tools
                kwargs["tool_choice"] = "auto"
            elif self.tool_calling_type == ToolCallingType.ANTHROPIC:
                # Anthropic-style tool calling
                kwargs["tools"] = formatted_tools
            elif self.tool_calling_type in [ToolCallingType.OLLAMA, ToolCallingType.TEXT_BASED, ToolCallingType.STRUCTURED_OUTPUT]:
                # For these types, we need to modify the system prompt
                tool_description = formatted_tools
                if messages and messages[0]["role"] == "system":
                    # Create a copy of messages to avoid modifying the original
                    messages = messages.copy()
                    # Update the system prompt with tool descriptions
                    messages[0] = {
                        "role": "system",
                        "content": f"{messages[0]['content']}\n\n{tool_description}"
                    }
                    kwargs["messages"] = messages
            
            logger.info(f"Calling LiteLLM with model: {self.model_name}")
            logger.info(f"Message count: {len(messages)}")
            logger.info(f"Tool calling type: {self.tool_calling_type.name}")
            logger.info(f"Tools available: {[f.get('name', 'unknown') for f in functions]}")
        else:
            logger.info(f"Calling LiteLLM with model: {self.model_name} (without functions)")
            logger.info(f"Message count: {len(messages)}")
        
        # Log the request
        log_completion_request(self.model_name, messages, functions)
        
        # Track request time
        start_time = time.time()
        response = self._call_api(kwargs)
        elapsed_time = time.time() - start_time
        
        # Log the response
        log_completion_response(response, elapsed_time)
        
        # Debug log for Ollama responses
        if self.tool_calling_type == ToolCallingType.OLLAMA:
            logger.debug(f"Ollama response type: {type(response)}")
            logger.debug(f"Ollama response attributes: {dir(response) if hasattr(response, '__dict__') else 'No attributes'}")
            logger.debug(f"Ollama response dict: {response.__dict__ if hasattr(response, '__dict__') else 'Not a class instance'}")
            
            # Check for message attribute
            if hasattr(response, 'message'):
                logger.debug(f"Ollama message: {response.message}")
        
        return response
    
    @abstractmethod
    def _call_api(self, kwargs: Dict) -> Any:
        """
        Make the actual API call to the model provider.
        
        Args:
            kwargs: Dictionary of arguments for the API call
            
        Returns:
            The model's response
        """
        pass
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the model's response.
        
        Args:
            response: The model's response
            
        Returns:
            List of dictionaries with tool call details
        """
        return self.tool_handler.extract_tool_calls(response)
    
    def extract_content(self, response: Any) -> str:
        """
        Extract the content from a response.
        
        Args:
            response: The response from the model
            
        Returns:
            str: The text content
        """
        # Extract content based on the model type
        if self.tool_calling_type == ToolCallingType.OPENAI:
            if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
                return ""
                
            message_obj = response.choices[0].message
            content = message_obj.content if hasattr(message_obj, 'content') else ""
            return str(content).strip() if content else ""
            
        elif self.tool_calling_type == ToolCallingType.ANTHROPIC:
            if not response:
                return ""
                
            # Handle different response formats
            if hasattr(response, 'content') and isinstance(response.content, list):
                # Extract text from content blocks
                text_blocks = []
                for block in response.content:
                    if block.get('type') == 'text':
                        text_blocks.append(block.get('text', ''))
                return ' '.join(text_blocks)
            
            # Handle Anthropic responses via LiteLLM
            if hasattr(response, 'choices') and len(response.choices) > 0:
                message_obj = response.choices[0].message
                content = message_obj.content if hasattr(message_obj, 'content') else ""
                
                # If content is None but there are tool calls, return a default message
                if content is None and hasattr(message_obj, 'tool_calls') and message_obj.tool_calls:
                    tool_names = [tool.function.name for tool in message_obj.tool_calls if hasattr(tool, 'function')]
                    if tool_names:
                        return f"I'm using the {', '.join(tool_names)} tool(s) to help answer your question."
                    return "I'm using tools to help answer your question."
                
                return str(content).strip() if content else ""
            
        elif self.tool_calling_type == ToolCallingType.OLLAMA:
            if not response:
                return ""
                
            # Try to extract content from Ollama response
            if hasattr(response, 'message'):
                content = response.message.content if hasattr(response.message, 'content') else ""
                return str(content).strip() if content else ""
            
            # Handle LiteLLM response format
            if hasattr(response, 'choices') and len(response.choices) > 0:
                message_obj = response.choices[0].message
                content = message_obj.content if hasattr(message_obj, 'content') else ""
                return str(content).strip() if content else ""
            
        else:
            # For other types, use a generic approach
            if hasattr(response, 'choices') and len(response.choices) > 0:
                message_obj = response.choices[0].message
                content = message_obj.content if hasattr(message_obj, 'content') else ""
                return str(content).strip() if content else ""
            
        # Default fallback
        return ""
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool execution results for the model.
        
        Args:
            tool_name: Name of the tool that was called
            result: Result from the tool execution
            **kwargs: Additional arguments like tool_call_id
            
        Returns:
            Dictionary formatted as a message to send back to the model
        """
        return self.tool_handler.format_tool_results(tool_name, result, **kwargs)


class LiteLLMInterface(ModelInterface):
    """Model interface that uses LiteLLM for API calls."""
    
    def __init__(self, model_name: str, drop_params: bool = True):
        """Initialize with retry settings."""
        super().__init__(model_name, drop_params)
        self.max_retries = 3
        self.initial_retry_delay = 2.0  # in seconds
    
    def _call_api(self, kwargs: Dict) -> Any:
        """Make the API call using LiteLLM with retries for rate limits."""
        # Process messages for provider compatibility
        if "messages" in kwargs:
            kwargs["messages"] = process_messages_for_provider(kwargs["messages"], self.provider)
            
        retries = 0
        while True:
            try:
                return litellm.completion(**kwargs)
            except (RateLimitError, ServiceUnavailableError) as e:
                retries += 1
                if retries > self.max_retries:
                    logger.error(f"Exceeded maximum retries ({self.max_retries}) for {self.model_name}")
                    raise
                
                # Calculate backoff with jitter
                delay = self.initial_retry_delay * (2 ** (retries - 1))
                jitter = random.uniform(0, 0.1 * delay)  # 10% jitter
                delay += jitter
                
                logger.warning(f"Rate limit hit for {self.model_name} ({self.provider}). Retrying in {delay:.2f}s (attempt {retries}/{self.max_retries})")
                time.sleep(delay)
            except (Timeout, APIConnectionError) as e:
                retries += 1
                if retries > self.max_retries:
                    logger.error(f"Connection/timeout errors exceeded maximum retries ({self.max_retries})")
                    raise
                
                # Different backoff strategy for network issues
                delay = self.initial_retry_delay * 1.5 * (retries)
                jitter = random.uniform(0, 0.1 * delay)
                delay += jitter
                
                logger.warning(f"Connection error with {self.model_name}: {str(e)}. Retrying in {delay:.2f}s")
                time.sleep(delay)
            except Exception as e:
                # All other exceptions are not retried
                logger.error(f"Error calling {self.model_name}: {type(e).__name__}: {str(e)}")
                raise


def create_model_interface(model_name: str, drop_params: bool = True) -> ModelInterface:
    """
    Factory function to create the appropriate model interface based on the model name.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters
        
    Returns:
        ModelInterface: The appropriate model interface
    """
    # For now, we only have one implementation that uses LiteLLM
    return LiteLLMInterface(model_name, drop_params) 