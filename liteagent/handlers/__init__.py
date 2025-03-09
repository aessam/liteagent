"""
Tool calling handler implementations for different model providers.

This package contains implementations for extracting and formatting tool calls
for various LLM providers.
"""

from .openai_handler import OpenAIToolCallingHandler
from .anthropic_handler import AnthropicToolCallingHandler
from .groq_handler import GroqToolCallingHandler
from .ollama_handler import OllamaToolCallingHandler
from .text_based_handler import TextBasedToolCallingHandler
from .structured_output_handler import StructuredOutputHandler
from .noop_handler import NoopToolCallingHandler
from .auto_detect_handler import AutoDetectToolCallingHandler
from ..tool_calling_types import ToolCallingType

__all__ = [
    'OpenAIToolCallingHandler',
    'AnthropicToolCallingHandler',
    'GroqToolCallingHandler',
    'OllamaToolCallingHandler',
    'TextBasedToolCallingHandler',
    'StructuredOutputHandler',
    'NoopToolCallingHandler',
    'AutoDetectToolCallingHandler',
    'create_tool_handler',
]

def create_tool_handler(tool_calling_type: ToolCallingType):
    """
    Create the appropriate tool calling handler based on the detected type.
    
    Args:
        tool_calling_type: The detected tool calling type
        
    Returns:
        An appropriate tool calling handler instance
    """
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
        # Default to auto-detect if unsure
        return AutoDetectToolCallingHandler() 