"""
Tool calling implementation for different types of language models.

This module provides classes for handling tool calling interactions with different LLM providers.
"""

from abc import ABC, abstractmethod
import json
import re
import uuid
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Union, Callable, Set, Tuple
import logging

from .tools import get_function_definitions
from .agent_tool import FunctionDefinition
from .tool_calling_types import ToolCallingType
from .utils import logger

# Tool call tracking for tests
class ToolCallTracker:
    """Tracker for tool calls to help with testing."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = ToolCallTracker()
        return cls._instance
    
    def __init__(self):
        """Initialize the tracker."""
        self.reset()
    
    def reset(self):
        """Reset the tracker."""
        self.called_tools = set()
        self.tool_args = {}
        self.tool_results = {}
    
    def record_call(self, tool_name: str, arguments: Dict):
        """Record a tool call."""
        self.called_tools.add(tool_name)
        self.tool_args[tool_name] = arguments
    
    def record_result(self, tool_name: str, result: Any):
        """Record a tool result."""
        self.tool_results[tool_name] = result
    
    def was_tool_called(self, tool_name: str) -> bool:
        """Check if a tool was called."""
        return tool_name in self.called_tools
    
    def get_tool_args(self, tool_name: str) -> Dict:
        """Get the arguments for a tool call."""
        return self.tool_args.get(tool_name, {})
    
    def get_tool_result(self, tool_name: str) -> Any:
        """Get the result of a tool call."""
        return self.tool_results.get(tool_name)


class ToolCallingHandler(ABC):
    """Base class for tool calling handlers."""
    
    @abstractmethod
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from a model response.
        
        Args:
            response: The model response
            
        Returns:
            A list of tool call dictionaries
        """
        pass
        
    @abstractmethod
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Format tools for a model.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools in the format expected by the model
        """
        pass
        
    @abstractmethod
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results for a model.
        
        Args:
            tool_name: The name of the tool
            result: The result of the tool call
            
        Returns:
            Formatted tool results in the format expected by the model
        """
        pass
        
    @abstractmethod
    def can_handle_response(self, response: Any) -> bool:
        """
        Determine if this handler can process the given response format.
        
        Args:
            response: The response to check
            
        Returns:
            bool: True if this handler can process the response, False otherwise
        """
        pass

    def _track_tool_call(self, tool_name: str, arguments: Dict):
        """Track a tool call for testing purposes."""
        ToolCallTracker.get_instance().record_call(tool_name, arguments)
    
    def _track_tool_result(self, tool_name: str, result: Any):
        """Track a tool result for testing purposes."""
        ToolCallTracker.get_instance().record_result(tool_name, result)


class OpenAIToolCallingHandler(ToolCallingHandler):
    """Handler for OpenAI-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an OpenAI-style response."""
        tool_calls = []
        
        # Handle None response
        if response is None:
            logger.debug("Received None response in OpenAIToolCallingHandler")
            return tool_calls
            
        # Log response structure for debugging
        logger.debug(f"Extracting tool calls from response: {type(response)}")
        if hasattr(response, 'choices'):
            logger.debug(f"Response has {len(response.choices)} choices")
        
        # Modern OpenAI format
        if hasattr(response, 'choices') and response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            
            # Log choice structure for debugging
            logger.debug(f"Processing choice: {choice}")
            
            # Check for message and tool_calls attributes
            has_message = hasattr(choice, 'message')
            has_tool_calls = has_message and hasattr(choice.message, 'tool_calls')
            tool_calls_not_none = has_tool_calls and choice.message.tool_calls is not None
            
            logger.debug(f"Has message: {has_message}, Has tool_calls: {has_tool_calls}, Tool calls not None: {tool_calls_not_none}")
            
            if tool_calls_not_none:
                for tool_call in choice.message.tool_calls:
                    if hasattr(tool_call, 'function'):
                        function_call = tool_call.function
                        tool_call_data = {
                            "name": function_call.name,
                            "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                            "id": tool_call.id if hasattr(tool_call, 'id') else str(uuid.uuid4())
                        }
                        tool_calls.append(tool_call_data)
                        # Track this tool call
                        self._track_tool_call(function_call.name, tool_call_data["arguments"])
                        
            # Legacy format - function_call at the message level
            elif has_message and hasattr(choice.message, 'function_call') and choice.message.function_call is not None:
                function_call = choice.message.function_call
                if hasattr(function_call, 'name') and hasattr(function_call, 'arguments'):
                    try:
                        args = json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse function arguments: {function_call.arguments}")
                        args = {}
                        
                    tool_call_data = {
                        "name": function_call.name,
                        "arguments": args,
                        "id": str(uuid.uuid4())
                    }
                    tool_calls.append(tool_call_data)
                    # Track this tool call
                    self._track_tool_call(function_call.name, args)
                    
        # If we found tool calls, return them
        if tool_calls:
            logger.debug(f"Extracted {len(tool_calls)} tool calls")
            return tool_calls
            
        # No tool calls found, check for an 'error' field indicating an API error
        if hasattr(response, 'error') and response.error is not None:
            logger.warning(f"API error detected: {response.error}")
            
        # Fall back to text-based extraction if no tool calls were found
        content = self._extract_content(response)
        if content:
            # Try to find function calls in the text content using JSON pattern matching
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            import re
            matches = re.findall(json_pattern, content)
            
            for json_str in sorted(matches, key=len, reverse=True):
                try:
                    json_obj = json.loads(json_str)
                    # Check if this looks like a function call
                    if "name" in json_obj and ("arguments" in json_obj or "params" in json_obj):
                        args = json_obj.get("arguments", json_obj.get("params", {}))
                        tool_call_data = {
                            "name": json_obj["name"],
                            "arguments": args,
                            "id": str(uuid.uuid4())
                        }
                        tool_calls.append(tool_call_data)
                        # Track this tool call
                        self._track_tool_call(json_obj["name"], args)
                        break
                except json.JSONDecodeError:
                    continue
                    
        # Return whatever we found, which might be an empty list
        return tool_calls
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for OpenAI models."""
        # OpenAI requires a "type" field for each tool and a "function" property
        formatted_tools = []
        for tool in tools:
            # Create a copy of the tool to avoid modifying the original
            tool_copy = tool.copy()
            
            # Add the "type" field if it doesn't exist
            if "type" not in tool_copy:
                tool_copy["type"] = "function"
            
            # Ensure the tool has a "function" property
            if "function" not in tool_copy:
                # If the tool has name, description, and parameters, move them to a function object
                function_data = {}
                if "name" in tool_copy:
                    function_data["name"] = tool_copy["name"]
                if "description" in tool_copy:
                    function_data["description"] = tool_copy["description"]
                if "parameters" in tool_copy:
                    function_data["parameters"] = tool_copy["parameters"]
                
                # Add the function object to the tool
                tool_copy["function"] = function_data
                
                # Remove the fields that were moved to the function object
                # but keep them if they're needed at the top level
                if "parameters" in tool_copy and "function" in tool_copy:
                    tool_copy.pop("parameters", None)
            
            formatted_tools.append(tool_copy)
        return formatted_tools
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for OpenAI models."""
        # Track the result
        self._track_tool_result(tool_name, result)
        
        tool_call_id = kwargs.get("tool_call_id")
        if not tool_call_id:
            # Generate a UUID if no tool call ID provided
            tool_call_id = str(uuid.uuid4())
            
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": json.dumps(result) if not isinstance(result, str) else result
        }

    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        if not (hasattr(response, 'choices') and len(response.choices) > 0 and 
                hasattr(response.choices[0], 'message')):
            return False
            
        # Check if the response has a message with tool_calls in OpenAI format
        message = response.choices[0].message
        return hasattr(message, 'tool_calls') and isinstance(message.tool_calls, list)

    def _extract_content(self, response: Any) -> str:
        """Extract text content from the response."""
        if hasattr(response, 'choices') and len(response.choices) > 0:
            if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                content = response.choices[0].message.content
                return str(content).strip() if content else ""
        
        if hasattr(response, 'content') and isinstance(response.content, list):
            # Concatenate all text content
            text_content = []
            for content_item in response.content:
                if hasattr(content_item, "type") and content_item.type == "text":
                    text_content.append(content_item.text)
            return "\n".join(text_content)
        
        return ""


class GroqToolCallingHandler(OpenAIToolCallingHandler):
    """Handler for Groq-style tool calling, which is similar to OpenAI but with some differences."""
    
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for Groq models."""
        # Groq requires a "type" field for each tool and a "function" property
        formatted_tools = []
        for tool in tools:
            # Create a copy of the tool to avoid modifying the original
            tool_copy = tool.copy()
            
            # Add the "type" field if it doesn't exist
            if "type" not in tool_copy:
                tool_copy["type"] = "function"
            
            # Ensure the tool has a "function" property
            if "function" not in tool_copy:
                # If the tool has name, description, and parameters, move them to a function object
                function_data = {}
                if "name" in tool_copy:
                    function_data["name"] = tool_copy["name"]
                if "description" in tool_copy:
                    function_data["description"] = tool_copy["description"]
                if "parameters" in tool_copy:
                    function_data["parameters"] = tool_copy["parameters"]
                
                # Add the function object to the tool
                tool_copy["function"] = function_data
                
                # Remove the fields that were moved to the function object
                # but keep them if they're needed at the top level
                if "parameters" in tool_copy and "function" in tool_copy:
                    tool_copy.pop("parameters", None)
            
            formatted_tools.append(tool_copy)
        return formatted_tools
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for Groq models."""
        tool_call_id = kwargs.get("tool_id")
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": json.dumps(result) if not isinstance(result, str) else result
        }

    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # Groq uses the same format as OpenAI
        return super().can_handle_response(response)


class AnthropicToolCallingHandler(ToolCallingHandler):
    """Handler for Anthropic-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an Anthropic-style response."""
        tool_calls = []
        
        # Debug log the response structure
        logger.debug(f"Anthropic response type: {type(response)}")
        logger.debug(f"Anthropic response attributes: {dir(response) if hasattr(response, '__dict__') else 'No attributes'}")
        
        # Check for content array in the response (standard Anthropic format)
        if hasattr(response, "content") and isinstance(response.content, list):
            for content_item in response.content:
                if hasattr(content_item, "type") and content_item.type == "tool_use":
                    tool_calls.append({
                        "name": content_item.name,
                        "arguments": content_item.input,
                        "id": content_item.id
                    })
        
        # Check for ModelResponse structure from LiteLLM
        elif hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, 'message'):
                message = choice.message
                
                # Check for tool_calls in the message (OpenAI-like format that LiteLLM might use)
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tool_call in message.tool_calls:
                        if hasattr(tool_call, 'function'):
                            function_call = tool_call.function
                            tool_calls.append({
                                "name": function_call.name,
                                "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                                "id": tool_call.id
                            })
                
                # Check for content array in the message (LiteLLM might wrap Anthropic's response)
                elif hasattr(message, 'content') and isinstance(message.content, list):
                    for content_item in message.content:
                        if hasattr(content_item, "type") and content_item.type == "tool_use":
                            tool_calls.append({
                                "name": content_item.name,
                                "arguments": content_item.input,
                                "id": content_item.id
                            })
        
        # If we found tool calls, return them
        if tool_calls:
            logger.debug(f"Extracted tool calls from Anthropic response: {tool_calls}")
            return tool_calls
            
        # If no tool calls were found, try to extract from text using text-based approach
        content = self._extract_content(response)
        if content and "[FUNCTION_CALL]" in content and "[/FUNCTION_CALL]" in content:
            # Extract function call from text
            start_idx = content.find("[FUNCTION_CALL]")
            end_idx = content.find("[/FUNCTION_CALL]")
            
            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                func_text = content[start_idx + 15:end_idx].strip()
                
                # Parse function name and arguments
                if "(" in func_text and ")" in func_text:
                    func_name = func_text[:func_text.find("(")].strip()
                    args_text = func_text[func_text.find("(")+1:func_text.rfind(")")].strip()
                    
                    # Parse arguments
                    func_args = {}
                    if args_text:
                        try:
                            # Try to parse as JSON first
                            func_args = json.loads("{" + args_text + "}")
                        except json.JSONDecodeError:
                            # Fall back to parsing key-value pairs
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
                    
                    return [{
                        "name": func_name,
                        "arguments": func_args,
                        "id": str(uuid.uuid4())
                    }]
        
        # No tool calls found
        logger.debug("No tool calls found in Anthropic response")
        return []
    
    def _extract_content(self, response: Any) -> str:
        """Extract text content from the response."""
        if hasattr(response, 'choices') and len(response.choices) > 0:
            if hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                content = response.choices[0].message.content
                return str(content).strip() if content else ""
        
        if hasattr(response, 'content') and isinstance(response.content, list):
            # Concatenate all text content
            text_content = []
            for content_item in response.content:
                if hasattr(content_item, "type") and content_item.type == "text":
                    text_content.append(content_item.text)
            return "\n".join(text_content)
        
        return ""
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for Anthropic models."""
        anthropic_tools = []
        for tool in tools:
            anthropic_tools.append({
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("parameters", {})
            })
        return anthropic_tools
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for Anthropic models."""
        # For Anthropic, we'll use a regular user message with text content
        # to avoid the error when there was no tool_use in the previous message
        return {
            "role": "user",
            "content": f"The result of calling {tool_name} is: {json.dumps(result) if not isinstance(result, str) else result}"
        }

    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # Check for Anthropic's content structure with tool_use type
        if not hasattr(response, 'content'):
            return False
            
        content = response.content
        if not isinstance(content, list):
            return False
            
        # Look for any tool_use items in the content list
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'tool_use':
                return True
                
        return False


class OllamaToolCallingHandler(ToolCallingHandler):
    """Handler for Ollama-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an Ollama-style response."""
        logger.debug(f"OllamaToolCallingHandler.extract_tool_calls called with response type: {type(response)}")
        
        tool_calls = []
        
        # First try to extract native tool calls from ModelResponse structure
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            logger.debug(f"Examining choice with type: {type(choice)}")
            if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls'):
                logger.debug(f"Found tool_calls in message: {choice.message.tool_calls}")
                # Safety check to ensure tool_calls is not None before iterating
                if choice.message.tool_calls is not None:
                    for tool_call in choice.message.tool_calls:
                        if hasattr(tool_call, 'function'):
                            function_call = tool_call.function
                            # Handle the special case where name is "arguments" (Ollama format)
                            if function_call.name == "arguments":
                                logger.debug(f"Found Ollama-style function with arguments: {function_call.arguments}")
                                # In this case, the arguments field contains the actual function call data
                                # Try to parse it as JSON or key-value pairs
                                arguments = function_call.arguments
                                if isinstance(arguments, str):
                                    # Try to parse as JSON first
                                    try:
                                        # Extract location from the arguments string
                                        # The format could be like: "location":"San Francisco, CA"
                                        parsed_args = {}
                                        parts = arguments.split(":")
                                        if len(parts) >= 2:
                                            key = parts[0].strip('"')
                                            value = ":".join(parts[1:]).strip('"')
                                            parsed_args[key] = value
                                        logger.debug(f"Parsed Ollama arguments to: {parsed_args}")
                                        return [{
                                            "name": "get_weather",  # Assuming the function name based on context
                                            "arguments": parsed_args,
                                            "id": str(uuid.uuid4())
                                        }]
                                    except:
                                        # If parsing fails, use as is
                                        logger.warning(f"Failed to parse Ollama arguments: {arguments}")
                                        return [{
                                            "name": "get_weather",  # Assuming the function name based on context
                                            "arguments": {"args": arguments},
                                            "id": str(uuid.uuid4())
                                        }]
                            else:
                                # Standard format with name and arguments
                                logger.debug(f"Found standard function call: {function_call.name}")
                                tool_call_data = {
                                    "name": function_call.name,
                                    "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                                    "id": tool_call.id if hasattr(tool_call, 'id') else str(uuid.uuid4())
                                }
                                tool_calls.append(tool_call_data)
                                # Track this tool call
                                self._track_tool_call(function_call.name, tool_call_data["arguments"])
                else:
                    logger.debug("tool_calls attribute is None, skipping tool calls extraction")
        
        if tool_calls:
            logger.debug(f"Returning tool calls: {tool_calls}")
            return tool_calls
        
        # Then try the original Ollama format
        if hasattr(response, "message") and hasattr(response.message, "tool_calls"):
            logger.debug(f"Found tool_calls in response.message: {response.message.tool_calls}")
            # Safety check to ensure tool_calls is not None before iterating
            if response.message.tool_calls is not None:
                tool_calls = []
                for tool_call in response.message.tool_calls:
                    if hasattr(tool_call, "function"):
                        function_call = tool_call.function
                        # Handle the special case where name is "arguments" (Ollama format)
                        if function_call.name == "arguments":
                            logger.debug(f"Found Ollama-style function with arguments: {function_call.arguments}")
                            # In this case, the arguments field contains the actual function call data
                            arguments = function_call.arguments
                            if isinstance(arguments, str):
                                # Try to parse as key-value pairs
                                try:
                                    # Extract location from the arguments string
                                    # The format could be like: "location":"San Francisco, CA"
                                    parsed_args = {}
                                    parts = arguments.split(":")
                                    if len(parts) >= 2:
                                        key = parts[0].strip('"')
                                        value = ":".join(parts[1:]).strip('"')
                                        parsed_args[key] = value
                                    logger.debug(f"Parsed Ollama arguments to: {parsed_args}")
                                    return [{
                                        "name": "get_weather",  # Assuming the function name based on context
                                        "arguments": parsed_args,
                                        "id": str(uuid.uuid4())
                                    }]
                                except:
                                    # If parsing fails, use as is
                                    logger.warning(f"Failed to parse Ollama arguments: {arguments}")
                                    return [{
                                        "name": "get_weather",  # Assuming the function name based on context
                                        "arguments": {"args": arguments},
                                        "id": str(uuid.uuid4())
                                    }]
                        else:
                            # Standard format with name and arguments
                            logger.debug(f"Found standard function call: {function_call.name}")
                            tool_calls.append({
                                "name": function_call.name,
                                "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                                "id": str(uuid.uuid4())  # Ollama doesn't provide IDs, so we generate one
                            })
            
                if tool_calls:
                    logger.debug(f"Returning tool calls: {tool_calls}")
                    return tool_calls
            else:
                logger.debug("tool_calls attribute in response.message is None, skipping tool calls extraction")
        
        # If no native tool calls found, try text-based extraction as a fallback
        # Extract content from the response
        content = ""
        if hasattr(response, "message") and hasattr(response.message, "content"):
            content = response.message.content
        elif hasattr(response, 'choices') and len(response.choices) > 0 and hasattr(response.choices[0], 'message'):
            content = response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else ""
        
        # Log the content for debugging
        logger.debug(f"Extracted content for text-based extraction: {content[:100]}...")
        
        if not content:
            logger.warning("No content found in response")
            return []
        
        # Try to extract JSON using our advanced method
        json_data = self.extract_json_from_text(content)
        if json_data and "function" in json_data:
            logger.debug(f"Found function call in JSON: {json_data['function']}")
            function_info = json_data["function"]
            tool_call = {
                "name": function_info["name"],
                "arguments": function_info.get("arguments", {}),
                "id": str(uuid.uuid4())
            }
            
            # Track this tool call for testing
            self._track_tool_call(tool_call["name"], tool_call["arguments"])
            
            return [tool_call]
        
        # Check for our special function call syntax
        if "[FUNCTION_CALL]" in content and "[/FUNCTION_CALL]" in content:
            logger.debug("Found [FUNCTION_CALL] markers in content")
            # Extract function call from text
            start_idx = content.find("[FUNCTION_CALL]")
            end_idx = content.find("[/FUNCTION_CALL]")
            
            if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
                # No valid function call found
                logger.warning("Invalid function call markers in content")
                return []
                
            func_text = content[start_idx + 15:end_idx].strip()
            logger.debug(f"Extracted function text: {func_text}")
            
            # Parse function name and arguments
            if "(" not in func_text or ")" not in func_text:
                # Invalid function call format
                logger.warning("Invalid function call format (missing parentheses)")
                return []
                
            func_name = func_text[:func_text.find("(")].strip()
            args_text = func_text[func_text.find("(")+1:func_text.rfind(")")].strip()
            logger.debug(f"Parsed function name: {func_name}, args: {args_text}")
            
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
            
            logger.debug(f"Parsed arguments: {func_args}")
            tool_call = {
                "name": func_name,
                "arguments": func_args,
                "id": str(uuid.uuid4())
            }
            
            # Track this tool call for testing
            self._track_tool_call(func_name, func_args)
            
            return [tool_call]
        
        logger.warning("No tool calls found in the response")
        return []
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for Ollama models."""
        ollama_tools = []
        for tool in tools:
            ollama_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                }
            })
        
        # Also add text-based instructions to the system prompt
        tool_descriptions = []
        for func in tools:
            name = func.get("name", "unknown")
            description = func.get("description", f"Function to {name}")
            params = func.get("parameters", {}).get("properties", {})
            
            param_desc = ", ".join([f"{p} ({t.get('type', 'any')})" 
                                  for p, t in params.items()])
            
            tool_descriptions.append(f"Function: {name}({param_desc})\nDescription: {description}\n")
        
        # Add the text-based instructions to the first tool's description
        if ollama_tools:
            current_desc = ollama_tools[0]["function"]["description"]
            text_instructions = ("\n\nIf you need to use a function, you can also output exactly "
                               "[FUNCTION_CALL] function_name(param1=value1, param2=value2) [/FUNCTION_CALL].\n\n" + 
                               "\n".join(tool_descriptions))
            
            ollama_tools[0]["function"]["description"] = current_desc + text_instructions
            
        return ollama_tools
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for Ollama models."""
        return {
            "role": "user",
            "content": f"The result of calling {tool_name} is: {json.dumps(result) if not isinstance(result, str) else result}"
        }

    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # Check for Ollama's tool_calls structure
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls'):
                return True
                
        # Also check original Ollama format
        if hasattr(response, "message") and hasattr(response.message, "tool_calls"):
            return True
            
        return False

    def extract_json_from_text(self, content: str) -> Optional[Dict]:
        """
        Extract a JSON object from text content. This is useful for finding function calls
        embedded in model responses from models that don't have native function calling.
        
        Args:
            content: The text content to search for JSON
            
        Returns:
            Optional[Dict]: The extracted JSON object, or None if no valid JSON is found
        """
        # First try to find a complete JSON object enclosed in curly braces
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        import re
        matches = re.findall(json_pattern, content)
        
        logger.debug(f"Found {len(matches)} potential JSON objects in content")
        
        # Try all potential JSON matches, starting with the most comprehensive ones
        for json_str in sorted(matches, key=len, reverse=True):
            try:
                json_obj = json.loads(json_str)
                logger.debug(f"Successfully parsed JSON object: {json_str[:100]}...")
                
                # Check if this looks like a function call
                if "function" in json_obj and isinstance(json_obj["function"], dict):
                    logger.debug(f"Found function call in JSON: {json_obj['function']}")
                    return json_obj
                    
                # Also check for direct function call format
                if "name" in json_obj and ("arguments" in json_obj or "params" in json_obj):
                    logger.debug(f"Found direct function call format: {json_obj}")
                    function_data = {
                        "function": {
                            "name": json_obj["name"],
                            "arguments": json_obj.get("arguments", json_obj.get("params", {}))
                        }
                    }
                    return function_data
            except json.JSONDecodeError:
                continue
        
        logger.debug("No valid JSON objects found that match function call patterns")
        return None


class TextBasedToolCallingHandler(ToolCallingHandler):
    """Handler for text-based tool calling (for models without native tool calling)."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from a text-based response."""
        # Extract content from the response
        content = self._extract_content(response)
        if not content:
            return []
            
        # Check for our special function call syntax
        if "[FUNCTION_CALL]" in content and "[/FUNCTION_CALL]" in content:
            # Extract function call from text
            start_idx = content.find("[FUNCTION_CALL]")
            end_idx = content.find("[/FUNCTION_CALL]")
            
            if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
                # No valid function call found
                return []
                
            func_text = content[start_idx + 15:end_idx].strip()
            
            # Parse function name and arguments
            if "(" not in func_text or ")" not in func_text:
                # Invalid function call format
                return []
                
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
            
            return [{
                "name": func_name,
                "arguments": func_args,
                "id": str(uuid.uuid4())
            }]
        
        return []
        
    def format_tools_for_model(self, tools: List[Dict]) -> str:
        """Format tools as a text description for the system prompt."""
        if not tools:
            return ""
            
        tool_descriptions = []
        for func in tools:
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
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for text-based models."""
        return {
            "role": "user",
            "content": f"The result of calling {tool_name} is: {json.dumps(result) if not isinstance(result, str) else result}"
        }
        
    def _extract_content(self, response: Any) -> str:
        """Extract text content from the response."""
        if hasattr(response, 'choices') and len(response.choices) > 0:
            content = response.choices[0].message.content
        elif isinstance(response, dict) and "choices" in response:
            content = response["choices"][0]["message"].get("content", "")
        else:
            content = ""
            
        return str(content).strip() if content else ""

    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # Extract content and check for [FUNCTION_CALL] markers
        content = self._extract_content(response)
        return "[FUNCTION_CALL]" in content and "[/FUNCTION_CALL]" in content


class StructuredOutputHandler(ToolCallingHandler):
    """Handler for models that can output structured JSON but don't have native tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from a structured output response."""
        # Extract the content
        content = self._extract_content(response)
        if not content:
            return []
            
        # Try to parse content as JSON
        try:
            data = json.loads(content)
            # Look for a function call structure
            if isinstance(data, dict) and "function" in data and "name" in data["function"]:
                return [{
                    "name": data["function"]["name"],
                    "arguments": data["function"]["arguments"],
                    "id": data.get("id", str(uuid.uuid4()))
                }]
        except (json.JSONDecodeError, AttributeError, TypeError):
            pass
            
        return []
        
    def format_tools_for_model(self, tools: List[Dict]) -> str:
        """Format tools as a schema description in the system prompt."""
        tool_descriptions = []
        for tool in tools:
            params = tool.get("parameters", {}).get("properties", {})
            param_desc = "\n".join([f"  - {name}: {details.get('type', 'any')} - {details.get('description', '')}" 
                                   for name, details in params.items()])
            
            tool_descriptions.append(f"""
Function: {tool['name']}
Description: {tool.get('description', '')}
Parameters:
{param_desc}
            """)
        
        prompt = """
You have access to the following functions. To use a function, you must respond with a JSON object in the following format:
{
  "function": {
    "name": "function_name",
    "arguments": {
      "param1": "value1",
      "param2": "value2"
    }
  }
}

Available functions:
"""
        return prompt + "\n".join(tool_descriptions)
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for structured output models."""
        return {
            "role": "user",
            "content": f"The result of calling {tool_name} is: {json.dumps(result) if not isinstance(result, str) else result}"
        }
        
    def _extract_content(self, response: Any) -> str:
        """Extract text content from the response."""
        if hasattr(response, 'choices') and len(response.choices) > 0:
            content = response.choices[0].message.content
        elif isinstance(response, dict) and "choices" in response:
            content = response["choices"][0]["message"].get("content", "")
        else:
            content = ""
            
        return str(content).strip() if content else ""

    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # Try to extract and parse content as JSON with expected structure
        content = self._extract_content(response)
        if not content:
            return False
            
        try:
            data = json.loads(content)
            # Check for expected structure
            return (isinstance(data, dict) and 
                    "function" in data and 
                    isinstance(data["function"], dict) and
                    "name" in data["function"])
        except (json.JSONDecodeError, AttributeError, TypeError):
            return False


class NoopToolCallingHandler(ToolCallingHandler):
    """Handler for models without tool calling capabilities."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls (always returns empty list)."""
        return []
    
    def format_tools_for_model(self, tools: List[Dict]) -> None:
        """Format tools (returns None)."""
        return None
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results (returns as user message)."""
        return {
            "role": "user",
            "content": f"Result from {tool_name}: {result}"
        }
    
    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # This handler doesn't actually handle any tool calls
        return False


class AutoDetectToolCallingHandler(ToolCallingHandler):
    """
    Tool calling handler that automatically detects and adapts to different formats.
    
    This is useful for models with unknown capabilities or when testing new models.
    It will try to detect the format of tool calls in responses and handle them appropriately.
    """
    
    def __init__(self):
        """Initialize the auto-detect handler."""
        self._specific_handler = None
        self._detected_type = None
        # Initialize all possible handlers for detection
        self._handlers = {
            ToolCallingType.OPENAI_FUNCTION_CALLING: OpenAIToolCallingHandler(),
            ToolCallingType.ANTHROPIC_TOOL_CALLING: AnthropicToolCallingHandler(),
            ToolCallingType.JSON_EXTRACTION: OllamaToolCallingHandler(),
            ToolCallingType.PROMPT_BASED: StructuredOutputHandler(),
            "text_based": TextBasedToolCallingHandler()
        }
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the response by auto-detecting the format.
        
        Args:
            response: The model's response
            
        Returns:
            List of extracted tool calls
        """
        # Use the detect_tool_calling_format function from tool_calling_detection module
        from .tool_calling_detection import detect_tool_calling_format
        detected_type = detect_tool_calling_format(response)
        
        # Get the appropriate handler for the detected type
        handler = self._handlers.get(detected_type)
        if handler is None:
            logger.warning(f"No handler found for detected type {detected_type}. Using text-based handler.")
            handler = self._handlers["text_based"]
        
        # Try using the detected handler
        try:
            return handler.extract_tool_calls(response)
        except Exception as e:
            logger.warning(f"Error using detected handler: {e}. Falling back to generic extraction.")
            # Fall back to the generic extraction method
            from .tool_calling_detection import extract_tool_calls_from_response
            return extract_tool_calls_from_response(response)
    
    def _detect_handler(self, response: Any) -> ToolCallingHandler:
        """
        Detect the appropriate handler for the response format.
        
        Args:
            response: The model's response
            
        Returns:
            The appropriate handler for the response format
        """
        # Try each handler in priority order to see if it can handle the response
        for handler_type, handler in self._handlers.items():
            if handler.can_handle_response(response):
                logger.debug(f"Detected handler type: {handler_type}")
                return handler
        
        # If no handler matched, use the basic text-based handler as fallback
        logger.debug("No specific handler matched, using fallback TextBasedToolCallingHandler")
        return self._handlers["text_based"]
    
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Format tools for the model, using the best guess at the format.
        
        Args:
            tools: List of tool definitions
            
        Returns:
            Formatted tools
        """
        # Default to OpenAI format if we don't know yet
        if self._specific_handler is None:
            self._specific_handler = OpenAIToolCallingHandler()
        
        return self._specific_handler.format_tools_for_model(tools)
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results for the model, using the detected format.
        
        Args:
            tool_name: Name of the tool that was called
            result: Result from the tool execution
            
        Returns:
            Formatted tool results
        """
        # Default to OpenAI format if we don't know yet
        if self._specific_handler is None:
            self._specific_handler = OpenAIToolCallingHandler()
        
        return self._specific_handler.format_tool_results(tool_name, result, **kwargs)
    
    def can_handle_response(self, response: Any) -> bool:
        """Determine if this handler can process the given response format."""
        # Auto-detect handler can always handle responses by routing to the appropriate handler
        return True


def get_tool_calling_handler(model_name: str, tool_calling_type: Optional[ToolCallingType] = None) -> ToolCallingHandler:
    """
    Get the appropriate tool calling handler for a model.
    
    Args:
        model_name: The name of the model
        tool_calling_type: Optional, explicitly specified tool calling type (overrides model default)
        
    Returns:
        ToolCallingHandler: The appropriate tool calling handler
    """
    # If a specific tool_calling_type is provided, always respect it
    if tool_calling_type is not None:
        # Create a handler directly based on the specified tool calling type
        if tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
            return OpenAIToolCallingHandler()
        elif tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
            return AnthropicToolCallingHandler()
        elif tool_calling_type == ToolCallingType.JSON_EXTRACTION:
            return OllamaToolCallingHandler()
        elif tool_calling_type == ToolCallingType.PROMPT_BASED:
            return StructuredOutputHandler()
        elif tool_calling_type == ToolCallingType.NONE:
            return NoopToolCallingHandler()
    
    # Only if no tool_calling_type is specified, detect by provider
    # Get provider from model name
    from .tool_calling_config import get_provider_from_model
    provider = get_provider_from_model(model_name)
    
    # Use specified tool calling type or get it from model capabilities
    actual_tool_calling_type = tool_calling_type
    if actual_tool_calling_type is None:
        from .tool_calling_types import get_tool_calling_type
        actual_tool_calling_type = get_tool_calling_type(model_name)
    
    # Get provider-specific handler
    return get_provider_specific_handler(provider, actual_tool_calling_type)


def get_provider_specific_handler(provider: str, tool_calling_type: ToolCallingType) -> ToolCallingHandler:
    """
    Get a provider-specific tool calling handler.
    
    Args:
        provider: The provider name
        tool_calling_type: The tool calling type
        
    Returns:
        A tool calling handler for the provider
    """
    # Provider-specific handlers
    provider = provider.lower()
    
    # Use auto-detection for unknown providers ONLY if no specific type is requested
    if provider == "unknown":
        return AutoDetectToolCallingHandler()
    
    # Handle providers with custom implementations
    if provider == "groq" and tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
        return GroqToolCallingHandler()
    elif provider == "anthropic" and tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
        return AnthropicToolCallingHandler()
    elif provider == "ollama" and tool_calling_type == ToolCallingType.JSON_EXTRACTION:
        return OllamaToolCallingHandler()
    
    # Default handlers based on tool calling type
    if tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
        return OpenAIToolCallingHandler()
    elif tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
        return AnthropicToolCallingHandler()
    elif tool_calling_type == ToolCallingType.JSON_EXTRACTION:
        return OllamaToolCallingHandler()
    elif tool_calling_type == ToolCallingType.PROMPT_BASED:
        return StructuredOutputHandler()
    elif tool_calling_type == ToolCallingType.NONE:
        return NoopToolCallingHandler()
    else:
        # Default to auto-detection for unknown types
        return AutoDetectToolCallingHandler() 