"""
Anthropic-specific tool calling handler implementation.
"""

import json
import uuid
from typing import Dict, List, Any

from ..pattern_tool_handler import PatternToolHandler

class AnthropicToolCallingHandler(PatternToolHandler):
    """Handler for Anthropic Claude tool use with native API format."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from Anthropic API response.
        
        Args:
            response: The model response from Anthropic API
            
        Returns:
            A list of extracted tool calls with name, arguments (input), and id
        """
        tool_calls = []
        
        # Handle direct Anthropic API format (content blocks)
        if hasattr(response, 'content') and isinstance(response.content, list):
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'tool_use':
                    tool_call_data = {
                        "name": block.name if hasattr(block, 'name') else "unknown",
                        "arguments": block.input if hasattr(block, 'input') else {},
                        "id": block.id if hasattr(block, 'id') else str(uuid.uuid4())
                    }
                    tool_calls.append(tool_call_data)
                    self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
        
        # Handle LiteLLM wrapped responses (standardized format)
        elif hasattr(response, 'choices') and response.choices:
            message = response.choices[0].message if response.choices else None
            
            if message:
                # LiteLLM may standardize to tool_calls format
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tc in message.tool_calls:
                        if hasattr(tc, 'function'):
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
        Format tools for Anthropic Claude API format.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools for Anthropic with input_schema
        """
        anthropic_tools = []
        
        for tool in tools:
            # Anthropic uses input_schema instead of parameters
            anthropic_tool = {
                "name": tool.get("name", ""),
                "description": tool.get("description", ""),
                "input_schema": tool.get("parameters", {})
            }
            
            # Ensure input_schema has the correct structure
            if "type" not in anthropic_tool["input_schema"]:
                anthropic_tool["input_schema"]["type"] = "object"
            
            anthropic_tools.append(anthropic_tool)
            
        return anthropic_tools
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results for Anthropic Claude API.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments (should include tool_use_id)
            
        Returns:
            A formatted tool result for Anthropic
        """
        # Format content as string
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        # Track for testing
        self._track_tool_result(tool_name, result)
        
        # Get tool_use_id from kwargs - this is critical for Anthropic
        tool_use_id = kwargs.get("tool_use_id") or kwargs.get("tool_id") or kwargs.get("id")
        if not tool_use_id:
            tool_use_id = f"toolu_{uuid.uuid4().hex[:12]}"
        
        # Anthropic tool result format
        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": content
        } 