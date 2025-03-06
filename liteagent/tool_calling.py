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

from .tools import get_function_definitions
from .agent_tool import FunctionDefinition
from .tool_calling_types import ToolCallingType
from .utils import logger


class ToolCallingHandler(ABC):
    """Abstract base class for tool calling handlers."""
    
    @abstractmethod
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the model's response.
        
        Args:
            response: The model's response object
            
        Returns:
            List of dictionaries containing tool call information with:
            - name: The name of the tool/function to call
            - arguments: Dictionary of arguments for the tool
            - id: Optional ID for the tool call (for response routing)
        """
        pass
        
    @abstractmethod
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Format tools in the way the model expects.
        
        Args:
            tools: List of tool definitions in OpenAI-like format
            
        Returns:
            Tools formatted for the specific model API
        """
        pass
        
    @abstractmethod
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
        pass


class OpenAIToolCallingHandler(ToolCallingHandler):
    """Handler for OpenAI-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an OpenAI-style response."""
        tool_calls = []
        
        # Handle case where response is a ModelResponse object
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, 'message'):
                message = choice.message
                
                # Check for tool_calls array (OpenAI format)
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tool_call in message.tool_calls:
                        if hasattr(tool_call, 'function'):
                            function_call = tool_call.function
                            tool_calls.append({
                                "name": function_call.name,
                                "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                                "id": tool_call.id
                            })
                
                # Check for function_call (older OpenAI format)
                elif hasattr(message, 'function_call') and message.function_call:
                    function_call = message.function_call
                    tool_calls.append({
                        "name": function_call.name,
                        "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                        "id": str(uuid.uuid4())  # Generate an ID since one isn't provided
                    })
        
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
        # Check for both tool_id and tool_call_id for backward compatibility
        tool_call_id = kwargs.get("tool_call_id") or kwargs.get("tool_id")
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": json.dumps(result) if not isinstance(result, str) else result
        }


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


class OllamaToolCallingHandler(ToolCallingHandler):
    """Handler for Ollama-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an Ollama-style response."""
        # First try to extract native tool calls from ModelResponse structure
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls') and choice.message.tool_calls is not None:
                tool_calls = []
                for tool_call in choice.message.tool_calls:
                    if hasattr(tool_call, 'function'):
                        function_call = tool_call.function
                        tool_calls.append({
                            "name": function_call.name,
                            "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                            "id": tool_call.id if hasattr(tool_call, 'id') else str(uuid.uuid4())
                        })
                
                if tool_calls:
                    return tool_calls
        
        # Then try the original Ollama format
        if hasattr(response, "message") and hasattr(response.message, "tool_calls") and response.message.tool_calls is not None:
            tool_calls = []
            for tool_call in response.message.tool_calls:
                if hasattr(tool_call, "function"):
                    function_call = tool_call.function
                    tool_calls.append({
                        "name": function_call.name,
                        "arguments": json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments,
                        "id": str(uuid.uuid4())  # Ollama doesn't provide IDs, so we generate one
                    })
            
            if tool_calls:
                return tool_calls
        
        # If no native tool calls found, try text-based extraction as a fallback
        # Extract content from the response
        content = ""
        if hasattr(response, "message") and hasattr(response.message, "content"):
            content = response.message.content
        elif hasattr(response, 'choices') and len(response.choices) > 0 and hasattr(response.choices[0], 'message'):
            content = response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else ""
        
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


class NoopToolCallingHandler(ToolCallingHandler):
    """Handler for models that don't support tool calling at all."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """No tool calls can be extracted."""
        return []
        
    def format_tools_for_model(self, tools: List[Dict]) -> None:
        """No tools can be formatted."""
        return None
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results as a simple user message."""
        return {
            "role": "user",
            "content": f"The result of calling {tool_name} is: {json.dumps(result) if not isinstance(result, str) else result}"
        }


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
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from the response by auto-detecting the format.
        
        Args:
            response: The model's response
            
        Returns:
            List of extracted tool calls
        """
        from .tool_calling_detection import detect_tool_calling_format, extract_tool_calls_from_response
        
        # Detect the format if not already detected or if we need to re-detect
        if self._detected_type is None or self._specific_handler is None:
            self._detected_type = detect_tool_calling_format(response)
            self._specific_handler = self._get_handler_for_type(self._detected_type)
        
        # Try using the specific handler
        try:
            return self._specific_handler.extract_tool_calls(response)
        except Exception as e:
            logger.warning(f"Error using specific handler: {e}. Falling back to generic extraction.")
            # Fall back to the generic extraction method
            return extract_tool_calls_from_response(response)
    
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Format tools for the model based on detected type.
        
        Args:
            tools: List of tool definitions
            
        Returns:
            Formatted tools
        """
        # If we haven't detected a type yet, default to JSON extraction
        if self._detected_type is None:
            self._detected_type = ToolCallingType.JSON_EXTRACTION
            self._specific_handler = self._get_handler_for_type(self._detected_type)
        
        return self._specific_handler.format_tools_for_model(tools)
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results based on detected type.
        
        Args:
            tool_name: Name of the tool
            result: Result from tool execution
            **kwargs: Additional parameters
            
        Returns:
            Formatted tool results
        """
        # If we haven't detected a type yet, default to JSON extraction
        if self._detected_type is None:
            self._detected_type = ToolCallingType.JSON_EXTRACTION
            self._specific_handler = self._get_handler_for_type(self._detected_type)
        
        return self._specific_handler.format_tool_results(tool_name, result, **kwargs)
    
    def _get_handler_for_type(self, tool_calling_type: ToolCallingType) -> ToolCallingHandler:
        """
        Get a specific handler for the detected type.
        
        Args:
            tool_calling_type: The detected tool calling type
            
        Returns:
            A specific tool calling handler
        """
        if tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
            return OpenAIToolCallingHandler()
        elif tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
            return AnthropicToolCallingHandler()
        elif tool_calling_type == ToolCallingType.JSON_EXTRACTION:
            return OllamaToolCallingHandler()
        elif tool_calling_type == ToolCallingType.PROMPT_BASED:
            return TextBasedToolCallingHandler()
        elif tool_calling_type == ToolCallingType.NONE:
            return NoopToolCallingHandler()
        else:
            return TextBasedToolCallingHandler()


def get_tool_calling_handler(model_name: str, tool_calling_type: Optional[ToolCallingType] = None) -> ToolCallingHandler:
    """
    Get the appropriate tool calling handler for a model.
    
    Args:
        model_name: The name of the model
        tool_calling_type: Optional, explicitly specified tool calling type (overrides model default)
        
    Returns:
        ToolCallingHandler: The appropriate tool calling handler
    """
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
    
    # Use auto-detection for unknown providers
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
        return TextBasedToolCallingHandler()
    elif tool_calling_type == ToolCallingType.NONE:
        return NoopToolCallingHandler()
    else:
        # Default to auto-detection for PROMPT_BASED or unknown types
        return AutoDetectToolCallingHandler() 