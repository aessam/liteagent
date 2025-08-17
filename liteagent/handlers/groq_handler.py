"""
Groq-specific tool calling handler implementation.
"""

import json
import uuid
from typing import Dict, List, Any

from ..simple_tool_handler import SimpleToolCallingHandler

class GroqToolCallingHandler(SimpleToolCallingHandler):
    """
    Handler for Groq tool calling using OpenAI-compatible format.
    Groq uses the same API format as OpenAI for function calling.
    """
    
    def __init__(self):
        """Initialize with Groq-specific limits."""
        super().__init__()
        self.max_tools = 128  # Groq supports up to 128 tools
        self.supports_parallel_tools = True
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from a Groq response (OpenAI-compatible format).
        
        Args:
            response: The model response
            
        Returns:
            A list of extracted tool calls
        """
        # Handle empty response or empty choices
        if not hasattr(response, 'choices') or not response.choices:
            return []
        
        tool_calls = []
        try:
            message = response.choices[0].message
            
            # Groq uses OpenAI format for tool calls
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tc in message.tool_calls:
                    if hasattr(tc, 'function'):
                        # Parse arguments if they're a JSON string
                        args = tc.function.arguments
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except json.JSONDecodeError:
                                args = {}
                        
                        tool_call_data = {
                            "name": tc.function.name,
                            "arguments": args,
                            "id": tc.id if hasattr(tc, 'id') else str(uuid.uuid4())
                        }
                        tool_calls.append(tool_call_data)
                        self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
                        
        except (IndexError, AttributeError):
            pass
            
        return tool_calls
    
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """
        Format tools for Groq models (OpenAI-compatible format).
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools for Groq (max 128 tools)
        """
        # Validate tool count
        if len(tools) > self.max_tools:
            raise ValueError(f"Groq supports a maximum of {self.max_tools} tools, but {len(tools)} were provided")
        
        # Groq uses OpenAI-compatible format
        formatted_tools = []
        
        for tool in tools:
            formatted_tool = {
                "type": "function",
                "function": {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                }
            }
            formatted_tools.append(formatted_tool)
            
        return formatted_tools
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results for Groq (OpenAI-compatible format).
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted tool result for Groq
        """
        # Convert result to string format
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        # Track for testing
        self._track_tool_result(tool_name, result)
        
        # Format in OpenAI style (Groq is OpenAI-compatible)
        tool_call_id = kwargs.get("tool_call_id") or kwargs.get("tool_id") or str(uuid.uuid4())
        
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        } 