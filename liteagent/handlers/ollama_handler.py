"""
Ollama-specific tool calling handler implementation.
"""

import json
import uuid
from typing import Dict, List, Any

from ..pattern_tool_handler import PatternToolHandler


class OllamaToolCallingHandler(PatternToolHandler):
    """Handler for Ollama tool calling using native API format."""
    
    def __init__(self):
        """Initialize with Ollama-specific settings."""
        super().__init__()
        self.max_tools = 10  # Ollama supports multiple tools
        self.supports_streaming = True
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from Ollama response.
        
        Args:
            response: The model response from Ollama
            
        Returns:
            A list of extracted tool calls
        """
        tool_calls = []
        
        # Handle Ollama native format
        if hasattr(response, 'message') and hasattr(response.message, 'tool_calls'):
            for tc in response.message.tool_calls:
                if hasattr(tc, 'function'):
                    # Parse arguments
                    args = tc.function.arguments
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    elif not isinstance(args, dict):
                        args = {}
                    
                    tool_call_data = {
                        "name": tc.function.name if hasattr(tc.function, 'name') else "unknown",
                        "arguments": args,
                        "id": tc.id if hasattr(tc, 'id') else str(uuid.uuid4())
                    }
                    tool_calls.append(tool_call_data)
                    self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
        
        # Handle LiteLLM wrapped response format
        elif hasattr(response, 'choices') and response.choices:
            message = response.choices[0].message if response.choices else None
            
            if message and hasattr(message, 'tool_calls') and message.tool_calls:
                for tc in message.tool_calls:
                    if hasattr(tc, 'function'):
                        # Parse arguments
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
    
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """
        Format tools for Ollama models.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools for Ollama (OpenAI-compatible format)
        """
        # Validate tool count
        if len(tools) > self.max_tools:
            raise ValueError(f"Ollama supports a maximum of {self.max_tools} tools, but {len(tools)} were provided")
        
        # Ollama uses OpenAI-compatible format for tools
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
        Format tool results for Ollama.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted tool result for Ollama
        """
        # Convert result to string format
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        # Track for testing
        self._track_tool_result(tool_name, result)
        
        # Ollama uses a similar format to OpenAI
        tool_call_id = kwargs.get("tool_call_id") or kwargs.get("tool_id") or str(uuid.uuid4())
        
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        }