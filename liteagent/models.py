"""
Model interfaces for LiteAgent.

This module provides abstractions for different LLM models with varying capabilities,
particularly around function/tool calling.
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import litellm

from .tool_calling import ToolCallingType, get_tool_calling_handler
from .tool_calling_config import get_tool_calling_type
from .utils import logger, log_completion_request, log_completion_response


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
        self.tool_calling_type = get_tool_calling_type(model_name)
        self.tool_handler = get_tool_calling_handler(self.tool_calling_type)
        
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Any:
        """
        Generate a response from the model.
        
        Args:
            messages: List of conversation messages
            functions: Optional list of function definitions
            
        Returns:
            Dict containing the model's response
        """
        kwargs = {"model": self.model_name, "messages": messages}
        
        if functions:
            # Format tools appropriately for this model
            formatted_tools = self.tool_handler.format_tools_for_model(functions)
            
            # Handle different tool calling types
            if self.tool_calling_type == ToolCallingType.OPENAI:
                kwargs["functions"] = formatted_tools
                kwargs["function_call"] = "auto"
            elif self.tool_calling_type == ToolCallingType.ANTHROPIC:
                kwargs["tools"] = formatted_tools
            elif self.tool_calling_type == ToolCallingType.OLLAMA:
                kwargs["tools"] = formatted_tools
            elif self.tool_calling_type in [ToolCallingType.STRUCTURED_OUTPUT, ToolCallingType.TEXT_BASED]:
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
                logger.debug(f"Ollama message type: {type(response.message)}")
                logger.debug(f"Ollama message attributes: {dir(response.message) if hasattr(response.message, '__dict__') else 'No attributes'}")
                logger.debug(f"Ollama message dict: {response.message.__dict__ if hasattr(response.message, '__dict__') else 'Not a class instance'}")
        
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
        Extract text content from the model's response.
        
        Args:
            response: The model's response
            
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
            if not response or not hasattr(response, 'content') or not isinstance(response.content, list):
                return ""
                
            # Concatenate all text content
            text_content = []
            for content_item in response.content:
                if hasattr(content_item, "type") and content_item.type == "text":
                    text_content.append(content_item.text)
                    
            return "\n".join(text_content)
            
        elif self.tool_calling_type == ToolCallingType.OLLAMA:
            # Ollama responses can have different structures
            # First check for ModelResponse structure (from litellm)
            if hasattr(response, 'choices') and len(response.choices) > 0:
                choice = response.choices[0]
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    content = choice.message.content
                    if content is not None:
                        return str(content).strip()
            
            # Then check for original Ollama structure
            if hasattr(response, 'message') and hasattr(response.message, 'content'):
                return str(response.message.content).strip()
            elif hasattr(response, 'response'):
                return str(response.response).strip()
            elif hasattr(response, 'content'):
                return str(response.content).strip()
            elif isinstance(response, dict):
                if 'message' in response and 'content' in response['message']:
                    return str(response['message']['content']).strip()
                elif 'response' in response:
                    return str(response['response']).strip()
                elif 'content' in response:
                    return str(response['content']).strip()
            
            # If we can't find content, log the response structure for debugging
            logger.warning(f"Unable to extract content from Ollama response: {response}")
            return ""
            
        else:
            # For other types, use a generic approach
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
            elif isinstance(response, dict) and "choices" in response:
                content = response["choices"][0]["message"].get("content", "")
            elif hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, dict) and "content" in response:
                content = response["content"]
            else:
                content = ""
                
            return str(content).strip() if content else ""
    
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
    
    def _call_api(self, kwargs: Dict) -> Any:
        """Make the API call using LiteLLM."""
        return litellm.completion(**kwargs)


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