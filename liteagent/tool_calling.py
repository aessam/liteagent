"""
Tool calling implementation for different types of language models.

This module provides classes for handling tool calling interactions with different LLM providers.
"""

import json
import re
import uuid
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Union, Callable, Set, Tuple
import logging
import copy

from .tools import get_function_definitions
from .agent_tool import FunctionDefinition
from .tool_calling_types import ToolCallingType
from .utils import logger

# Import our base class and pattern-based handler
from .pattern_tool_handler import ToolCallingHandlerBase, PatternToolHandler

# Tool call tracking for tests
class ToolCallTracker:
    """Tracker for tool calls to help with testing."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = ToolCallTracker()
        return cls._instance
    
    def __init__(self):
        """Initialize the tracker."""
        self.reset()
    
    def reset(self):
        """Reset the tracker."""
        self.called_tools = set()
        self.tool_args = {}
        self.tool_results = {}
    
    def record_call(self, tool_name: str, arguments: Dict):
        """Record a tool call."""
        self.called_tools.add(tool_name)
        self.tool_args[tool_name] = arguments
    
    def record_result(self, tool_name: str, result: Any):
        """Record a tool result."""
        self.tool_results[tool_name] = result
    
    def was_tool_called(self, tool_name: str) -> bool:
        """Check if a tool was called."""
        return tool_name in self.called_tools
    
    def get_tool_args(self, tool_name: str) -> Dict:
        """Get the arguments used for a tool call."""
        return self.tool_args.get(tool_name, {})
    
    def get_tool_result(self, tool_name: str) -> Any:
        """Get the result of a tool call."""
        return self.tool_results.get(tool_name)

# Import specific handlers
from .handlers.openai_handler import OpenAIToolCallingHandler
from .handlers.anthropic_handler import AnthropicToolCallingHandler
from .handlers.groq_handler import GroqToolCallingHandler
from .handlers.ollama_handler import OllamaToolCallingHandler
from .handlers.text_based_handler import TextBasedToolCallingHandler
from .handlers.structured_output_handler import StructuredOutputHandler
from .handlers.noop_handler import NoopToolCallingHandler
from .handlers.auto_detect_handler import AutoDetectToolCallingHandler

def get_tool_calling_handler(tool_calling_type: Optional[ToolCallingType] = None) -> ToolCallingHandlerBase:
    """
    Get a tool calling handler for a given model.
    
    Args:
        tool_calling_type: The tool calling type to use (overrides automatic detection)
        
    Returns:
        A tool calling handler
    """
    # Default to auto-detection if none specified
    if tool_calling_type is None:
        # We used to have a model registry here, but now we try to auto-detect the format from responses
        return AutoDetectToolCallingHandler()
        
    # If a specific tool calling type is specified, use it
    if tool_calling_type == ToolCallingType.OPENAI:
        return OpenAIToolCallingHandler()
    elif tool_calling_type == ToolCallingType.ANTHROPIC:
        return AnthropicToolCallingHandler()
    elif tool_calling_type == ToolCallingType.GROQ:
        return GroqToolCallingHandler()
    elif tool_calling_type == ToolCallingType.OLLAMA:
        return OllamaToolCallingHandler()
    elif tool_calling_type == ToolCallingType.TEXT_BASED:
        return TextBasedToolCallingHandler()
    elif tool_calling_type == ToolCallingType.STRUCTURED_OUTPUT:
        return StructuredOutputHandler()
    elif tool_calling_type == ToolCallingType.NONE:
        return NoopToolCallingHandler()
    else:
        logger.warning(f"Unknown tool calling type: {tool_calling_type}. Using auto-detection instead.")
        return AutoDetectToolCallingHandler()

def get_provider_specific_handler(provider: str, tool_calling_type: ToolCallingType) -> ToolCallingHandlerBase:
    """
    Get a provider-specific tool calling handler.
    
    Args:
        provider: The provider name
        tool_calling_type: The tool calling type
        
    Returns:
        A tool calling handler
    """
    if provider.lower() == "openai":
        return OpenAIToolCallingHandler()
    elif provider.lower() == "anthropic":
        return AnthropicToolCallingHandler()
    elif provider.lower() == "groq":
        return GroqToolCallingHandler()
    elif provider.lower() == "ollama":
        return OllamaToolCallingHandler()
    else:
        # Return the handler for the specified tool calling type
        return get_tool_calling_handler(tool_calling_type) 