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
        
    @abstractmethod
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Dict:
        """
        Generate a response from the model.
        
        Args:
            messages: List of conversation messages
            functions: Optional list of function definitions
            
        Returns:
            Dict containing the model's response
        """
        pass
    
    @abstractmethod
    def supports_function_calling(self) -> bool:
        """
        Check if this model supports native function calling.
        
        Returns:
            bool: Whether the model supports function calling
        """
        pass
    
    @abstractmethod
    def extract_function_call(self, response: Any) -> Optional[Dict]:
        """
        Extract function call information from the model's response.
        
        Args:
            response: The model's response
            
        Returns:
            Dict with function call details or None if no function call
        """
        pass
    
    @abstractmethod
    def extract_content(self, response: Any) -> str:
        """
        Extract text content from the model's response.
        
        Args:
            response: The model's response
            
        Returns:
            str: The text content
        """
        pass


class FunctionCallingModel(ModelInterface):
    """Model interface for models that support native function calling."""
    
    # Models known not to support function calling
    FUNCTION_CALL_UNSUPPORTED = [
        "text-davinci", "text-ada", "text-babbage", "text-curie", 
        "ollama/", "phi", "llama", "mistral"
    ]
    
    def supports_function_calling(self) -> bool:
        """Check if the model supports native function calling."""
        model_lower = self.model_name.lower()
        
        # Check against list of models known not to support function calling
        for unsupported in self.FUNCTION_CALL_UNSUPPORTED:
            if unsupported.lower() in model_lower:
                logger.info(f"Model '{self.model_name}' is detected as not supporting function calling")
                return False
                
        # Default to assuming support for other models
        return True
    
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Any:
        """Generate a response from the model with optional function calling."""
        kwargs = {"model": self.model_name, "messages": messages}
        
        if self.supports_function_calling() and functions:
            # Add function definitions for supported models
            kwargs["functions"] = functions
            kwargs["function_call"] = "auto"
            
            logger.info(f"Calling LiteLLM with model: {self.model_name}")
            logger.info(f"Message count: {len(messages)}")
            logger.info(f"Tools available: {[f['name'] for f in functions]}")
        else:
            logger.info(f"Calling LiteLLM with model: {self.model_name} (without function calling)")
            logger.info(f"Message count: {len(messages)}")
        
        # Log the request
        log_completion_request(self.model_name, messages, kwargs.get("functions"))
        
        # Track request time
        start_time = time.time()
        response = litellm.completion(**kwargs)
        elapsed_time = time.time() - start_time
        
        # Log the response
        log_completion_response(response, elapsed_time)
        
        return response
    
    def extract_function_call(self, response: Any) -> Optional[Dict]:
        """Extract function call information from the response."""
        if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
            return None
            
        message_obj = response.choices[0].message
        
        # Check for function call
        if hasattr(message_obj, 'function_call') and message_obj.function_call:
            function_call = message_obj.function_call
            function_name = function_call.name
            
            try:
                # Arguments might be a string that needs to be parsed as JSON
                function_args = json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments
            except json.JSONDecodeError:
                function_args = {}
                
            return {
                "name": function_name,
                "arguments": function_args
            }
        
        return None
    
    def extract_content(self, response: Any) -> str:
        """Extract text content from the response."""
        if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
            return ""
            
        message_obj = response.choices[0].message
        
        # Handle content response
        content = message_obj.content if hasattr(message_obj, 'content') else ""
        return str(content).strip() if content else ""


class TextBasedFunctionCallingModel(ModelInterface):
    """Model interface for models that don't support native function calling but can use text-based function calls."""
    
    def supports_function_calling(self) -> bool:
        """These models don't support native function calling."""
        return False
    
    def get_tool_description_in_prompt(self, functions: List[Dict]) -> str:
        """
        Create a text description of available tools to include in the prompt.
        
        Args:
            functions: List of function definitions
            
        Returns:
            str: A text description of available tools
        """
        if not functions:
            return ""
            
        tool_descriptions = []
        for func in functions:
            name = func.get("name", "unknown")
            description = func.get("description", f"Function to {name}")
            params = func.get("parameters", {}).get("properties", {})
            
            param_desc = ", ".join([f"{p} ({t.get('type', 'any')})" 
                                  for p, t in params.items()])
            
            tool_descriptions.append(f"Function: {name}({param_desc})\nDescription: {description}\n")
            
        if tool_descriptions:
            return ("You have access to the following functions. To use them, output exactly "
                   "[FUNCTION_CALL] function_name(param1=value1, param2=value2) [/FUNCTION_CALL].\n\n" + 
                   "\n".join(tool_descriptions))
        return ""
    
    def generate_response(self, messages: List[Dict], functions: Optional[List[Dict]] = None) -> Any:
        """Generate a response from the model with text-based function calling."""
        # If we have functions, add their descriptions to the system prompt
        if functions and messages and messages[0]["role"] == "system":
            tool_descriptions = self.get_tool_description_in_prompt(functions)
            if tool_descriptions:
                # Create a copy of messages to avoid modifying the original
                messages = messages.copy()
                # Update the system prompt with tool descriptions
                messages[0] = {
                    "role": "system",
                    "content": f"{messages[0]['content']}\n\n{tool_descriptions}"
                }
        
        kwargs = {"model": self.model_name, "messages": messages}
        
        logger.info(f"Calling LiteLLM with model: {self.model_name} (text-based function calling)")
        logger.info(f"Message count: {len(messages)}")
        
        # Log the request
        log_completion_request(self.model_name, messages, None)
        
        # Track request time
        start_time = time.time()
        response = litellm.completion(**kwargs)
        elapsed_time = time.time() - start_time
        
        # Log the response
        log_completion_response(response, elapsed_time)
        
        return response
    
    def extract_function_call(self, response: Any) -> Optional[Dict]:
        """Extract function call information from text-based response."""
        content = self.extract_content(response)
        if not content:
            return None
            
        # Check for our special function call syntax
        if "[FUNCTION_CALL]" in content and "[/FUNCTION_CALL]" in content:
            # Extract function call from text
            start_idx = content.find("[FUNCTION_CALL]")
            end_idx = content.find("[/FUNCTION_CALL]")
            
            if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
                # No valid function call found
                return None
                
            func_text = content[start_idx + 15:end_idx].strip()
            
            # Parse function name and arguments
            if "(" not in func_text or ")" not in func_text:
                # Invalid function call format
                return None
                
            func_name = func_text[:func_text.find("(")].strip()
            args_text = func_text[func_text.find("(")+1:func_text.rfind(")")].strip()
            
            # Parse arguments
            func_args = {}
            if args_text:
                for arg_pair in args_text.split(","):
                    if "=" in arg_pair:
                        key, value = arg_pair.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Try to convert value to appropriate type
                        try:
                            # Remove quotes from string values
                            if (value.startswith('"') and value.endswith('"')) or \
                               (value.startswith("'") and value.endswith("'")):
                                value = value[1:-1]
                            # Try as number
                            elif value.isdigit():
                                value = int(value)
                            elif value.replace(".", "", 1).isdigit():
                                value = float(value)
                            # Try as boolean
                            elif value.lower() in ["true", "false"]:
                                value = value.lower() == "true"
                            # Keep as string if none of the above
                        except:
                            pass
                            
                        func_args[key] = value
            
            return {
                "name": func_name,
                "arguments": func_args,
                "raw_text": content  # Include the raw text for context
            }
        
        return None
    
    def extract_content(self, response: Any) -> str:
        """Extract text content from the response."""
        if hasattr(response, 'choices') and len(response.choices) > 0:
            content = response.choices[0].message.content
        elif isinstance(response, dict) and "choices" in response:
            content = response["choices"][0]["message"].get("content", "")
        else:
            content = ""
            
        return str(content).strip() if content else ""


def create_model_interface(model_name: str, drop_params: bool = True) -> ModelInterface:
    """
    Factory function to create the appropriate model interface based on the model name.
    
    Args:
        model_name: Name of the model
        drop_params: Whether to drop unsupported parameters
        
    Returns:
        ModelInterface: The appropriate model interface
    """
    # Check if model supports function calling
    model_lower = model_name.lower()
    
    # Check against list of models known not to support function calling
    for unsupported in FunctionCallingModel.FUNCTION_CALL_UNSUPPORTED:
        if unsupported.lower() in model_lower:
            return TextBasedFunctionCallingModel(model_name, drop_params)
    
    # Default to function calling model
    return FunctionCallingModel(model_name, drop_params) 