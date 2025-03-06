"""
Validation strategies for different tool calling types.

This module provides a set of validation strategies for different tool calling types,
allowing for consistent validation of tool calls, results, and responses across
different language models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable, TypeVar, Generic, Union
import re
import json
import time

from .tool_calling_types import ToolCallingType

T = TypeVar('T')

class ToolValidationStrategy(ABC, Generic[T]):
    """Base class for tool validation strategies."""
    
    @abstractmethod
    def validate_function_call(self, function_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Validates if a function call is correct.
        
        Args:
            function_name: The name of the function
            arguments: The arguments passed to the function
            
        Returns:
            bool: True if the function call is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def validate_function_result(self, function_name: str, result: Any) -> bool:
        """
        Validates if a function result is correct.
        
        Args:
            function_name: The name of the function
            result: The result of the function call
            
        Returns:
            bool: True if the function result is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def extract_structured_data(self, response: str) -> Dict[str, Any]:
        """
        Extracts structured data from a text response.
        
        Args:
            response: The text response to extract data from
            
        Returns:
            Dict[str, Any]: The extracted structured data
        """
        pass
    
    @abstractmethod
    def parse_response(self, response: str, expected_tool: str) -> Dict[str, Any]:
        """
        Parses a response with focus on a specific tool.
        
        Args:
            response: The text response to parse
            expected_tool: The name of the tool to focus on
            
        Returns:
            Dict[str, Any]: The parsed response data
        """
        pass


class OpenAIValidationStrategy(ToolValidationStrategy):
    """Validation strategy for OpenAI-compatible function calling."""
    
    def __init__(self):
        """Initialize the OpenAI validation strategy."""
        self.response_parsers = {}
    
    def register_response_parser(self, function_name: str, parser: Callable[[str], Dict[str, Any]]):
        """
        Register a custom parser for a specific function's response.
        
        Args:
            function_name: The name of the function to register the parser for
            parser: A function that takes a response string and returns a structured dict
        """
        self.response_parsers[function_name] = parser
    
    def validate_function_call(self, function_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Validates if a function call is correct.
        
        Args:
            function_name: The name of the function
            arguments: The arguments passed to the function
            
        Returns:
            bool: True if the function call is valid, False otherwise
        """
        # OpenAI models typically provide well-structured function calls
        # Basic validation: function name should be a string and arguments should be a dict
        return isinstance(function_name, str) and isinstance(arguments, dict)
    
    def validate_function_result(self, function_name: str, result: Any) -> bool:
        """
        Validates if a function result is correct.
        
        Args:
            function_name: The name of the function
            result: The result of the function call
            
        Returns:
            bool: True if the function result is valid, False otherwise
        """
        # Basic validation: result should not be None
        return result is not None
    
    def extract_structured_data(self, response: str) -> Dict[str, Any]:
        """
        Extracts structured data from a text response.
        
        Args:
            response: The text response to extract data from
            
        Returns:
            Dict[str, Any]: The extracted structured data
        """
        result = {}
        
        # Try to extract JSON if present
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Extract key-value pairs like "Key: value" or "Key = value"
        for line in response.split('\n'):
            kv_match = re.search(r'([^:=]+)[:=]\s*(.*)', line)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                result[key] = value
                
        return result
    
    def parse_response(self, response: str, expected_tool: str) -> Dict[str, Any]:
        """
        Parses a response with focus on a specific tool.
        
        Args:
            response: The text response to parse
            expected_tool: The name of the tool to focus on
            
        Returns:
            Dict[str, Any]: The parsed response data
        """
        if expected_tool in self.response_parsers:
            return self.response_parsers[expected_tool](response)
        
        # Default parsing
        return self.extract_structured_data(response)


class AnthropicValidationStrategy(ToolValidationStrategy):
    """Validation strategy for Anthropic tool calling."""
    
    def __init__(self):
        """Initialize the Anthropic validation strategy."""
        self.response_parsers = {}
    
    def register_response_parser(self, function_name: str, parser: Callable[[str], Dict[str, Any]]):
        """
        Register a custom parser for a specific function's response.
        
        Args:
            function_name: The name of the function to register the parser for
            parser: A function that takes a response string and returns a structured dict
        """
        self.response_parsers[function_name] = parser
    
    def validate_function_call(self, function_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Validates if a function call is correct.
        
        Args:
            function_name: The name of the function
            arguments: The arguments passed to the function
            
        Returns:
            bool: True if the function call is valid, False otherwise
        """
        # Anthropic models typically provide well-structured function calls
        # Basic validation: function name should be a string and arguments should be a dict
        return isinstance(function_name, str) and isinstance(arguments, dict)
    
    def validate_function_result(self, function_name: str, result: Any) -> bool:
        """
        Validates if a function result is correct.
        
        Args:
            function_name: The name of the function
            result: The result of the function call
            
        Returns:
            bool: True if the function result is valid, False otherwise
        """
        # Basic validation: result should not be None
        return result is not None
    
    def extract_structured_data(self, response: str) -> Dict[str, Any]:
        """
        Extracts structured data from a text response.
        
        Args:
            response: The text response to extract data from
            
        Returns:
            Dict[str, Any]: The extracted structured data
        """
        result = {}
        
        # Try to extract JSON if present
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Extract key-value pairs like "Key: value" or "Key = value"
        for line in response.split('\n'):
            kv_match = re.search(r'([^:=]+)[:=]\s*(.*)', line)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                result[key] = value
                
        return result
    
    def parse_response(self, response: str, expected_tool: str) -> Dict[str, Any]:
        """
        Parses a response with focus on a specific tool.
        
        Args:
            response: The text response to parse
            expected_tool: The name of the tool to focus on
            
        Returns:
            Dict[str, Any]: The parsed response data
        """
        if expected_tool in self.response_parsers:
            return self.response_parsers[expected_tool](response)
        
        # Default parsing
        return self.extract_structured_data(response)


class JSONExtractionStrategy(ToolValidationStrategy):
    """Validation strategy for models that use text-based JSON extraction."""
    
    def __init__(self):
        """Initialize the JSON extraction strategy."""
        self.response_parsers = {}
    
    def register_response_parser(self, function_name: str, parser: Callable[[str], Dict[str, Any]]):
        """
        Register a custom parser for a specific function's response.
        
        Args:
            function_name: The name of the function to register the parser for
            parser: A function that takes a response string and returns a structured dict
        """
        self.response_parsers[function_name] = parser
    
    def validate_function_call(self, function_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Validates if a function call is correct.
        
        Args:
            function_name: The name of the function
            arguments: The arguments passed to the function
            
        Returns:
            bool: True if the function call is valid, False otherwise
        """
        # Basic validation: function name should be a string and arguments should be a dict
        return isinstance(function_name, str) and isinstance(arguments, dict)
    
    def validate_function_result(self, function_name: str, result: Any) -> bool:
        """
        Validates if a function result is correct.
        
        Args:
            function_name: The name of the function
            result: The result of the function call
            
        Returns:
            bool: True if the function result is valid, False otherwise
        """
        # Basic validation: result should not be None
        return result is not None
    
    def extract_structured_data(self, response: str) -> Dict[str, Any]:
        """
        Extracts structured data from a text response.
        
        Args:
            response: The text response to extract data from
            
        Returns:
            Dict[str, Any]: The extracted structured data
        """
        # Try to extract JSON from the response
        json_patterns = [
            r'```json\s*(.*?)\s*```',  # Code block with json
            r'```\s*(.*?)\s*```',       # Any code block
            r'{[\s\S]*?}',              # Any JSON-like object
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            for match in matches:
                try:
                    data = json.loads(match)
                    if isinstance(data, dict):
                        return data
                except json.JSONDecodeError:
                    continue
        
        # Fallback to key-value extraction
        result = {}
        for line in response.split('\n'):
            kv_match = re.search(r'([^:=]+)[:=]\s*(.*)', line)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                result[key] = value
                
        return result
    
    def parse_response(self, response: str, expected_tool: str) -> Dict[str, Any]:
        """
        Parses a response with focus on a specific tool.
        
        Args:
            response: The text response to parse
            expected_tool: The name of the tool to focus on
            
        Returns:
            Dict[str, Any]: The parsed response data
        """
        if expected_tool in self.response_parsers:
            return self.response_parsers[expected_tool](response)
        
        # Default parsing
        return self.extract_structured_data(response)


class PromptBasedStrategy(ToolValidationStrategy):
    """Validation strategy for models that need specific prompting."""
    
    def __init__(self):
        """Initialize the prompt-based strategy."""
        self.response_parsers = {}
    
    def register_response_parser(self, function_name: str, parser: Callable[[str], Dict[str, Any]]):
        """
        Register a custom parser for a specific function's response.
        
        Args:
            function_name: The name of the function to register the parser for
            parser: A function that takes a response string and returns a structured dict
        """
        self.response_parsers[function_name] = parser
    
    def validate_function_call(self, function_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Validates if a function call is correct.
        
        Args:
            function_name: The name of the function
            arguments: The arguments passed to the function
            
        Returns:
            bool: True if the function call is valid, False otherwise
        """
        # Basic validation: function name should be a string and arguments should be a dict
        return isinstance(function_name, str) and isinstance(arguments, dict)
    
    def validate_function_result(self, function_name: str, result: Any) -> bool:
        """
        Validates if a function result is correct.
        
        Args:
            function_name: The name of the function
            result: The result of the function call
            
        Returns:
            bool: True if the function result is valid, False otherwise
        """
        # Basic validation: result should not be None
        return result is not None
    
    def extract_structured_data(self, response: str) -> Dict[str, Any]:
        """
        Extracts structured data from a text response.
        
        Args:
            response: The text response to extract data from
            
        Returns:
            Dict[str, Any]: The extracted structured data
        """
        result = {}
        
        # Try to extract JSON if present
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Extract key-value pairs like "Key: value" or "Key = value"
        for line in response.split('\n'):
            kv_match = re.search(r'([^:=]+)[:=]\s*(.*)', line)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                result[key] = value
                
        return result
    
    def parse_response(self, response: str, expected_tool: str) -> Dict[str, Any]:
        """
        Parses a response with focus on a specific tool.
        
        Args:
            response: The text response to parse
            expected_tool: The name of the tool to focus on
            
        Returns:
            Dict[str, Any]: The parsed response data
        """
        if expected_tool in self.response_parsers:
            return self.response_parsers[expected_tool](response)
        
        # Default parsing
        return self.extract_structured_data(response)


def get_validation_strategy(tool_calling_type: ToolCallingType) -> ToolValidationStrategy:
    """
    Get the appropriate validation strategy for a tool calling type.
    
    Args:
        tool_calling_type: The tool calling type
        
    Returns:
        ToolValidationStrategy: The validation strategy for the tool calling type
    """
    if tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
        return OpenAIValidationStrategy()
    elif tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
        return AnthropicValidationStrategy()
    elif tool_calling_type == ToolCallingType.OLLAMA_TOOL_CALLING:
        return JSONExtractionStrategy()
    elif tool_calling_type == ToolCallingType.PROMPT_BASED:
        return PromptBasedStrategy()
    else:
        raise ValueError(f"No validation strategy available for tool calling type {tool_calling_type}") 