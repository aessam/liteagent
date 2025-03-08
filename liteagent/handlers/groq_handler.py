"""
Groq-specific tool calling handler implementation.
"""

import json
import uuid
from typing import Dict, List, Any

from ..pattern_tool_handler import PatternToolHandler

class GroqToolCallingHandler(PatternToolHandler):
    """
    Handler for Groq-style tool calling.
    Groq's API is similar to OpenAI's, so we can inherit most functionality from the pattern handler.
    """
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from a Groq response.
        
        Args:
            response: The model response
            
        Returns:
            A list of extracted tool calls
        """
        # Handle empty response or empty choices
        if not hasattr(response, 'choices') or not response.choices:
            return []
            
        # Handle OpenAI-like format which Groq uses
        try:
            if (hasattr(response.choices[0], 'message') and
                hasattr(response.choices[0].message, 'tool_calls') and
                isinstance(response.choices[0].message.tool_calls, list) and
                len(response.choices[0].message.tool_calls) > 0):
                
                # This is OpenAI-like format
                tool_calls = []
                for tc in response.choices[0].message.tool_calls:
                    if hasattr(tc, 'function'):
                        tool_call_data = {
                            "name": tc.function.name,
                            "arguments": json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments,
                            "id": tc.id if hasattr(tc, 'id') else str(uuid.uuid4())
                        }
                        tool_calls.append(tool_call_data)
                        self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
                return tool_calls
        except (IndexError, AttributeError, json.JSONDecodeError):
            # Handle any exceptions during the extraction
            return []
        
        # Fall back to pattern-based handling for other responses
        return super().extract_tool_calls(response)
    
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """
        Format tools for Groq models (OpenAI-compatible format).
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools for Groq
        """
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
        # Format result as in OpenAI format
        content = result
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        # Track for testing
        self._track_tool_result(tool_name, result)
        
        # Format in OpenAI style
        tool_id = kwargs.get("tool_call_id", kwargs.get("tool_id", f"call_{uuid.uuid4()}"))
        
        return {
            "role": "tool",
            "tool_call_id": tool_id,
            "name": tool_name,
            "content": content
        } 