"""
Tool calling utilities and tracking.

This module provides utilities for tracking and managing tool calls.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import time


@dataclass
class ToolCallRecord:
    """Record of a tool call execution."""
    name: str
    arguments: Dict[str, Any]
    result: Any
    timestamp: float
    execution_time: Optional[float] = None
    error: Optional[str] = None


class ToolCallTracker:
    """Tracks tool calls for debugging and analysis."""
    
    _instance = None
    
    def __init__(self):
        """Initialize the tool call tracker."""
        self.calls: List[ToolCallRecord] = []
        self._call_counts: Dict[str, int] = {}
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of ToolCallTracker."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def record_call(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def get_call_count(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(tool_name, 0)
    
    def was_tool_called(self, tool_name: str) -> bool:
        """Check if a tool was called at least once."""
        return self.get_call_count(tool_name) > 0
    
    def get_calls_for_tool(self, tool_name: str) -> List[ToolCallRecord]:
        """Get all calls for a specific tool."""
        return [call for call in self.calls if call.name == tool_name]
    
    def clear(self) -> None:
        """Clear all recorded calls."""
        self.calls.clear()
        self._call_counts.clear()
    
    def reset(self) -> None:
        """Reset the tracker (alias for clear)."""
        self.clear()
    
    @property
    def total_calls(self) -> int:
        """Get the total number of calls recorded."""
        return len(self.calls)
    
    @property
    def unique_tools_called(self) -> List[str]:
        """Get list of unique tool names that were called."""
        return list(self._call_counts.keys())