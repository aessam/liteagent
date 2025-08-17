"""
No-operation tool calling handler implementation.

This handler is used for models that don't support tool calling or when tool calling
needs to be explicitly disabled.
"""

import json
import uuid
from typing import Dict, List, Any

from ..simple_tool_handler import SimpleToolCallingHandler


class NoopToolCallingHandler(SimpleToolCallingHandler):
    """Compatibility class for no-op tool calling."""
    
    def format_tools_for_model(self, tools: List[Dict]) -> None:
        """
        Override to return None for no-op handler.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            None as this handler doesn't support tool calling
        """
        # This handler doesn't format tools for models since it doesn't support tool calling
        return None
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Override to provide format expected by tests.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted tool result for compatibility with tests
        """
        content = result
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        self._track_tool_result(tool_name, result)
        
        # Format for test expectations
        return {
            "role": "tool",
            "content": content,
            "tool_call_id": kwargs.get("tool_id", f"call_{uuid.uuid4()}")
        } 