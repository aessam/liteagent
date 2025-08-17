"""
Simplified tool calling handler base classes.

This module provides clean base classes for tool calling handlers without
the complexity of XPath-based pattern matching.
"""

import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .utils import logger


class ToolCallingHandlerBase(ABC):
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
        Format a tool result for a model.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted result in the format expected by the model
        """
        pass
        
    def can_handle_response(self, response: Any) -> bool:
        """
        Determine if this handler can process the given response format.
        
        Args:
            response: The response to check
            
        Returns:
            True if this handler can process the response, False otherwise
        """
        # Default implementation - most handlers can handle their intended responses
        return True

    def _track_tool_call(self, tool_name: str, arguments: Dict):
        """Track a tool call for testing purposes."""
        from .tool_calling import ToolCallTracker
        tracker = ToolCallTracker.get_instance()
        tracker.record_call(tool_name, arguments)
        
    def _track_tool_result(self, tool_name: str, result: Any):
        """Track a tool result for testing purposes."""
        from .tool_calling import ToolCallTracker
        tracker = ToolCallTracker.get_instance()
        tracker.record_result(tool_name, result)


class SimpleToolCallingHandler(ToolCallingHandlerBase):
    """
    Simple base implementation for tool calling handlers.
    
    This provides common functionality without XPath complexity.
    """
    
    def __init__(self):
        """Initialize the handler."""
        pass
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Default implementation returns empty list.
        Override in subclasses for specific provider logic.
        """
        return []
    
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Default implementation returns tools as-is.
        Override in subclasses for provider-specific formatting.
        """
        return tools
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Default implementation in OpenAI format.
        Override in subclasses for provider-specific formatting.
        """
        tool_call_id = kwargs.get("tool_call_id", str(uuid.uuid4()))
        
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": str(result) if result is not None else ""
        }