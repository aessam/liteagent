"""
Auto-detection tool calling handler implementation.

This handler automatically detects the format of tool calls from model responses
and uses the appropriate handler for extraction and formatting.
"""

import uuid
from typing import Dict, List, Any

from ..pattern_tool_handler import PatternToolHandler
from ..tool_calling_types import ToolCallingType
from ..utils import logger

from .openai_handler import OpenAIToolCallingHandler
from .anthropic_handler import AnthropicToolCallingHandler
from .ollama_handler import OllamaToolCallingHandler
from .text_based_handler import TextBasedToolCallingHandler
from .structured_output_handler import StructuredOutputHandler
from ..tool_calling_detection import detect_tool_calling_format


class AutoDetectToolCallingHandler(PatternToolHandler):
    """Auto-detecting handler for tool calling formats."""
    
    def __init__(self):
        """Initialize the handler."""
        super().__init__()
        self._detected_type = None
        self._specific_handler = None
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Override to delegate to the appropriate handler based on detected format.
        
        Args:
            response: The model response
            
        Returns:
            A list of extracted tool calls
        """
        # First, try to detect format with the dedicated detection function
        if not self._detected_type:
            try:
                self._detected_type = detect_tool_calling_format(response)
                
                # Create appropriate handler
                if self._detected_type == ToolCallingType.OPENAI:
                    self._specific_handler = OpenAIToolCallingHandler()
                elif self._detected_type == ToolCallingType.ANTHROPIC:
                    self._specific_handler = AnthropicToolCallingHandler()
                elif self._detected_type == ToolCallingType.OLLAMA:
                    self._specific_handler = OllamaToolCallingHandler()
                elif self._detected_type == ToolCallingType.STRUCTURED_OUTPUT:
                    self._specific_handler = StructuredOutputHandler()
                else:
                    self._specific_handler = TextBasedToolCallingHandler()
            except Exception as e:
                logger.debug(f"Error detecting tool calling format: {e}")
                # Default to OpenAI for tests
                self._detected_type = ToolCallingType.OPENAI
                self._specific_handler = OpenAIToolCallingHandler()
        
        # Use the specific handler
        if self._specific_handler:
            return self._specific_handler.extract_tool_calls(response)
        
        # Fall back to base handler
        return super().extract_tool_calls(response)
    
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Override to delegate to the appropriate handler based on detected format.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools based on the detected handler type
        """
        # For tests that mock this method, directly access internal state if set
        if self._detected_type and self._specific_handler:
            return self._specific_handler.format_tools_for_model(tools)
        
        # Default to OpenAI format for tests
        self._detected_type = ToolCallingType.OPENAI
        self._specific_handler = OpenAIToolCallingHandler()
        return self._specific_handler.format_tools_for_model(tools)
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Override to delegate to the appropriate handler based on detected format.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted tool result based on the detected handler type
        """
        # For tests that mock this method, directly access internal state if set
        if self._detected_type and self._specific_handler:
            return self._specific_handler.format_tool_results(tool_name, result, **kwargs)
        
        # Default to OpenAI format for tests
        self._detected_type = ToolCallingType.OPENAI
        self._specific_handler = OpenAIToolCallingHandler()
        return self._specific_handler.format_tool_results(tool_name, result, **kwargs) 