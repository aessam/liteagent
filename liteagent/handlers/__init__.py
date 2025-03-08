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

__all__ = [
    'OpenAIToolCallingHandler',
    'AnthropicToolCallingHandler',
    'GroqToolCallingHandler',
    'OllamaToolCallingHandler',
    'TextBasedToolCallingHandler',
    'StructuredOutputHandler',
    'NoopToolCallingHandler',
    'AutoDetectToolCallingHandler',
] 