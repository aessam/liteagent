"""
OpenAI-specific tool calling handler implementation.
"""

import json
import uuid
from typing import Dict, List, Any, Optional

from ..simple_tool_handler import SimpleToolCallingHandler

class OpenAIToolCallingHandler(SimpleToolCallingHandler):
    """Handler for OpenAI-style function calling using native API format."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from OpenAI API response.
        
        Args:
            response: The model response from OpenAI API
            
        Returns:
            A list of extracted tool calls with name, arguments, and id
        """
        # Handle empty response or empty choices
        if not hasattr(response, 'choices') or not response.choices:
            return []
        
        try:
            message = response.choices[0].message
            
            # Check if there are tool calls in the response
            if hasattr(message, 'tool_calls') and message.tool_calls:
                tool_calls = []
                for tc in message.tool_calls:
                    # Extract function details
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
                        
                return tool_calls
                
        except (IndexError, AttributeError) as e:
            # Log error but don't fail
            pass
        
        return []
    
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """
        Format tools for OpenAI API format.
        
        Args:
            tools: List of tool definitions
            
        Returns:
            Formatted tools in OpenAI format
        """
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
        Format tool results for OpenAI API.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments (must include tool_call_id)
            
        Returns:
            A formatted tool result in OpenAI format
        """
        # Get tool_call_id - required for OpenAI format
        tool_call_id = kwargs.get("tool_call_id") or kwargs.get("tool_id") or str(uuid.uuid4())
        
        # Track for debugging/testing
        self._track_tool_result(tool_name, result)
        
        # Convert result to string format
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        # Return in OpenAI tool result format
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        } 