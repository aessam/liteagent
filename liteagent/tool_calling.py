"""
Tool calling support for LiteAgent.

This module provides abstractions for different tool calling approaches across
various LLM providers, making it easier to handle the differences in their APIs.
"""

import json
import uuid
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

from .utils import logger


class ToolCallingType(Enum):
    """Enum representing different tool calling approaches used by LLM providers."""
    OPENAI = auto()           # OpenAI style with tool_calls array
    ANTHROPIC = auto()        # Anthropic style with content array and tool_use
    OLLAMA = auto()           # Ollama style arguments
    STRUCTURED_OUTPUT = auto() # Models that can reliably output JSON/structured data when prompted
    TEXT_BASED = auto()       # Fallback text-based extraction for less predictable outputs
    NONE = auto()             # No function calling support


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
        if not hasattr(response, "choices") or not response.choices:
            return []
            
        message = response.choices[0].message
        if not hasattr(message, "tool_calls") or not message.tool_calls:
            return []
            
        tool_calls = []
        for tool_call in message.tool_calls:
            if tool_call.type == "function":
                function_call = tool_call.function
                try:
                    arguments = json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments
                except json.JSONDecodeError:
                    arguments = {}
                    
                tool_calls.append({
                    "name": function_call.name,
                    "arguments": arguments,
                    "id": tool_call.id
                })
                
        return tool_calls
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """Format tools for OpenAI models."""
        # OpenAI format is our base format, so we just return the tools as is
        return tools
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format tool results for OpenAI models."""
        tool_call_id = kwargs.get("tool_call_id")
        if not tool_call_id:
            logger.warning("No tool_call_id provided for OpenAI tool result formatting")
            
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": json.dumps(result) if not isinstance(result, str) else result
        }


class AnthropicToolCallingHandler(ToolCallingHandler):
    """Handler for Anthropic-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an Anthropic-style response."""
        if not hasattr(response, "content") or not isinstance(response.content, list):
            return []
            
        tool_calls = []
        for content_item in response.content:
            if hasattr(content_item, "type") and content_item.type == "tool_use":
                tool_calls.append({
                    "name": content_item.name,
                    "arguments": content_item.input,
                    "id": content_item.id
                })
                
        return tool_calls
        
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
        tool_id = kwargs.get("tool_id")
        if not tool_id:
            logger.warning("No tool_id provided for Anthropic tool result formatting")
            
        return {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": json.dumps(result) if not isinstance(result, str) else result
                }
            ]
        }


class OllamaToolCallingHandler(ToolCallingHandler):
    """Handler for Ollama-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from an Ollama-style response."""
        if not hasattr(response, "message") or not hasattr(response.message, "tool_calls"):
            return []
            
        tool_calls = []
        for tool_call in response.message.tool_calls:
            if hasattr(tool_call, "function"):
                function_call = tool_call.function
                tool_calls.append({
                    "name": function_call.name,
                    "arguments": function_call.arguments,
                    "id": str(uuid.uuid4())  # Ollama doesn't provide IDs, so we generate one
                })
                
        return tool_calls
        
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


def get_tool_calling_handler(tool_calling_type: ToolCallingType) -> ToolCallingHandler:
    """
    Get the appropriate tool calling handler for the given type.
    
    Args:
        tool_calling_type: The tool calling type
        
    Returns:
        ToolCallingHandler: The appropriate handler instance
    """
    handlers = {
        ToolCallingType.OPENAI: OpenAIToolCallingHandler(),
        ToolCallingType.ANTHROPIC: AnthropicToolCallingHandler(),
        ToolCallingType.OLLAMA: OllamaToolCallingHandler(),
        ToolCallingType.STRUCTURED_OUTPUT: StructuredOutputHandler(),
        ToolCallingType.TEXT_BASED: TextBasedToolCallingHandler(),
        ToolCallingType.NONE: NoopToolCallingHandler()
    }
    
    return handlers.get(tool_calling_type, TextBasedToolCallingHandler()) 