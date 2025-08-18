"""
Enhanced observer for validation in integration tests.

This module provides specialized observer classes for validation of agent
behavior in integration tests, with support for different tool calling types.
"""

from typing import Dict, List, Optional, Any, Set, Callable, TypeVar, Union
from collections import Counter, defaultdict
import json
import re
import time

from liteagent.observer import AgentObserver, AgentEvent, FunctionCallEvent, FunctionResultEvent
from liteagent.capabilities import ModelCapabilities
# Removed auto_detect_handler import - using direct provider handlers now
from typing_extensions import Protocol

T = TypeVar('T')

class ResponseParser(Protocol):
    """Protocol for response parsers."""
    def __call__(self, response: str) -> Dict[str, Any]: ...

class ValidationObserver(AgentObserver):
    """
    Enhanced observer for validating agent behavior in integration tests.
    
    This observer tracks function calls and can be used to validate that
    specific functions were called or not called during agent interactions.
    It also provides advanced validation capabilities for function calls,
    arguments, and results, with support for different tool calling types.
    """
    
    def __init__(self, model_capabilities: Optional[ModelCapabilities] = None):
        """
        Initialize the validation observer.
        
        Args:
            model_capabilities: The model capabilities to use for validation.
                If None, no validation strategy will be used until set_validation_strategy is called.
        """
        self.function_calls: List[Dict[str, Any]] = []
        self.function_results: List[Dict[str, Any]] = []
        self.called_functions: Set[str] = set()
        self.function_call_counts: Counter = Counter()
        self.user_messages: List[str] = []
        self.agent_responses: List[str] = []
        
        # Store model capabilities for validation
        self._model_capabilities: Optional[ModelCapabilities] = model_capabilities
        self._response_parsers = {}
        
    def set_validation_strategy(self, model_capabilities: ModelCapabilities):
        """
        Set the model capabilities for validation.
        
        Args:
            model_capabilities: The model capabilities to use for validation
        """
        # Store the model capabilities
        self._model_capabilities = model_capabilities
        
    @property
    def validation_strategy(self) -> Optional[ModelCapabilities]:
        """
        Get the current model capabilities.
        
        Returns:
            The model capabilities, or None if not set
        """
        return self._model_capabilities
        
    def on_event(self, event: AgentEvent):
        """Base handler for all events."""
        # This is required to satisfy the AgentObserver abstract base class
        pass
        
    def on_function_call(self, event: FunctionCallEvent):
        """Record function call event."""
        super().on_function_call(event)
        
        # Add function call info
        self.function_calls.append({
            "name": event.function_name,
            "arguments": event.function_args,
            "timestamp": time.time()
        })
        self.called_functions.add(event.function_name)
        self.function_call_counts[event.function_name] += 1
        
    def on_function_result(self, event: FunctionResultEvent):
        """Record function result event."""
        super().on_function_result(event)
        self.function_results.append({
            "name": event.function_name,
            "result": event.result,
            "timestamp": time.time()
        })
    
    def on_user_message(self, event):
        """Record user message."""
        super().on_user_message(event)
        self.user_messages.append(event.message)
        
    def on_agent_response(self, event):
        """Record agent response."""
        super().on_agent_response(event)
        self.agent_responses.append(event.response)
    
    def register_response_parser(self, pattern_or_name, parser):
        """
        Register a custom parser for a specific function's response.
        
        Args:
            pattern_or_name: The name of the function or a regex pattern to match
            parser: A function that takes a response string and returns a structured dict
        """
        self._response_parsers[pattern_or_name] = parser
    
    def was_tool_called(self, tool_name: str) -> bool:
        """
        Check if a tool was called during the interaction.
        
        Args:
            tool_name: The name of the tool
            
        Returns:
            True if the tool was called, False otherwise
        """
        return tool_name in self.called_functions
    
    def get_function_call_count(self, function_name: str) -> int:
        """
        Get the number of times a function was called.
        
        Args:
            function_name: The name of the function
            
        Returns:
            The number of times the function was called
        """
        return self.function_call_counts.get(function_name, 0)
        
    def assert_function_called(self, function_name: str):
        """
        Assert that a function was called during the interaction.
        
        Args:
            function_name: The name of the function
        """
        assert function_name in self.called_functions, f"Function {function_name} was not called"
    
    def assert_tool_called(self, tool_name: str):
        """
        Assert that a tool was called during the interaction.
        Alias for assert_function_called with clearer naming.
        
        Args:
            tool_name: The name of the tool
        """
        self.assert_function_called(tool_name)
        
    def assert_function_not_called(self, function_name: str):
        """
        Assert that a function was not called during the interaction.
        
        Args:
            function_name: The name of the function
        """
        assert function_name not in self.called_functions, f"Function {function_name} was called"
    
    def assert_tool_not_called(self, tool_name: str):
        """
        Assert that a tool was not called during the interaction.
        Alias for assert_function_not_called with clearer naming.
        
        Args:
            tool_name: The name of the tool
        """
        self.assert_function_not_called(tool_name)
    
    def assert_function_call_count(self, function_name: str, expected_count: int):
        """
        Assert that a function was called a specific number of times.
        
        Args:
            function_name: The name of the function
            expected_count: The expected number of calls
        """
        actual_count = self.get_function_call_count(function_name)
        assert actual_count == expected_count, f"Expected {expected_count} calls to {function_name}, got {actual_count}"
        
    def assert_function_called_with(self, function_name: str, **kwargs):
        """
        Assert that a function was called with specific arguments.
        
        Args:
            function_name: The name of the function
            **kwargs: The expected arguments
        """
        for call in self.function_calls:
            if call["name"] == function_name:
                # Check if all the specified kwargs are in the arguments
                # and have the expected values
                args_match = all(
                    key in call["arguments"] and call["arguments"][key] == value
                    for key, value in kwargs.items()
                )
                if args_match:
                    return
                    
        # If we get here, no matching call was found
        raise AssertionError(
            f"Function {function_name} was not called with the expected arguments: {kwargs}"
        )
    
    def get_last_function_result(self, function_name: str) -> Optional[Any]:
        """
        Get the result of the most recent call to a function.
        
        Args:
            function_name: The name of the function
            
        Returns:
            The result of the most recent call, or None if the function was not called
        """
        for result in reversed(self.function_results):
            if result["name"] == function_name:
                return result["result"]
        return None
        
    def get_function_call_args(self, function_name: str) -> List[Dict[str, Any]]:
        """
        Get the arguments for all calls to a specific function.
        
        Args:
            function_name: The name of the function
            
        Returns:
            A list of argument dictionaries, one for each call to the function
        """
        args_list = []
        for call in self.function_calls:
            if call["name"] == function_name:
                args_list.append(call["arguments"])
        return args_list
        
    def assert_function_result_structure(self, function_name: str, 
                                        expected_structure: Dict[str, Any],
                                        strict: bool = False):
        """
        Assert that a function result matches an expected structure.
        
        Args:
            function_name: The name of the function
            expected_structure: A dictionary representing the expected structure
            strict: If True, all keys in the result must be in expected_structure
        """
        result = self.get_last_function_result(function_name)
        assert result is not None, f"No result found for function {function_name}"
        
        if not isinstance(result, dict):
            raise AssertionError(f"Result for {function_name} is not a dict: {result}")
        
        # Check expected keys exist with correct values
        for key, expected_value in expected_structure.items():
            assert key in result, f"Expected key '{key}' not found in result: {result}"
            
            if expected_value is not None:
                if callable(expected_value):
                    # If expected_value is a callable, use it to validate the actual value
                    assert expected_value(result[key]), f"Value for key '{key}' failed validation: {result[key]}"
                else:
                    # Otherwise check for equality
                    assert result[key] == expected_value, f"Expected {key}={expected_value}, got {key}={result[key]}"
        
        # In strict mode, ensure no extra keys
        if strict:
            for key in result:
                assert key in expected_structure, f"Unexpected key '{key}' found in result: {result}"
    
    def assert_function_result_list_length(self, function_name: str, expected_length: int):
        """
        Assert that a function result list has a specific length.
        
        Args:
            function_name: The name of the function
            expected_length: The expected length of the result list
        """
        result = self.get_last_function_result(function_name)
        assert result is not None, f"No result found for function {function_name}"
        assert isinstance(result, list), f"Result for {function_name} is not a list: {result}"
        assert len(result) == expected_length, f"Expected list of length {expected_length}, got {len(result)}"
    
    def parse_response(self, response: str, expected_tool: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse a response string into a structured object based on expected format.
        
        This method is useful for validating responses against expected structures
        rather than using string matching.
        
        Args:
            response: The response string to parse
            expected_tool: Optional function name to use a specific parser
            
        Returns:
            A dictionary with the parsed response data
        """
        result = {}
        
        # Try tool-specific parser first
        if expected_tool and expected_tool in self._response_parsers:
            parser = self._response_parsers[expected_tool]
            if callable(parser):
                return parser(response)
                
        # Try regex-based parsers
        for pattern, parser in self._response_parsers.items():
            if isinstance(pattern, str) and not pattern in self.called_functions:
                # This is a regex pattern, not a function name
                match = re.search(pattern, response)
                if match and callable(parser):
                    return parser(match)
        
        # Fall back to extracting structured data
        return self._extract_structured_data(response)
        
    def _extract_structured_data(self, response: str) -> Dict[str, Any]:
        """Extract structured data from a text response."""
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
    
    def assert_response_contains_structure(self, response: str, 
                                         expected_structure: Dict[str, Any],
                                         function_name: Optional[str] = None):
        """
        Assert that a response contains an expected structure.
        
        Args:
            response: The response string
            expected_structure: A dictionary representing the expected structure
            function_name: Optional function name to use a specific parser
        """
        parsed = self.parse_response(response, function_name)
        
        for key, expected_value in expected_structure.items():
            assert key in parsed, f"Expected key '{key}' not found in parsed response: {parsed}"
            
            if expected_value is not None:
                if callable(expected_value):
                    # If expected_value is a callable, use it to validate the actual value
                    assert expected_value(parsed[key]), f"Value for key '{key}' failed validation: {parsed[key]}"
                else:
                    # Otherwise check for equality
                    assert parsed[key] == expected_value, f"Expected {key}={expected_value}, got {key}={parsed[key]}"
    
    def reset(self):
        """Reset the observer state."""
        self.function_calls = []
        self.function_results = []
        self.called_functions = set()
        self.function_call_counts = Counter()
        self.user_messages = []
        self.agent_responses = []
        # Note: We don't reset the strategy or response parsers


class SequenceValidationObserver(ValidationObserver):
    """Observer that validates the sequence of function calls."""
    
    def assert_function_call_sequence(self, sequence: List[str]):
        """
        Assert that functions were called in a specific sequence.
        
        Args:
            sequence: The expected sequence of function names
        """
        # Extract the sequence of function names from the calls
        actual_sequence = [call["name"] for call in self.function_calls]
        
        # Check if the expected sequence is a subsequence of the actual sequence
        i, j = 0, 0
        while i < len(actual_sequence) and j < len(sequence):
            if actual_sequence[i] == sequence[j]:
                j += 1
            i += 1
            
        assert j == len(sequence), f"Expected sequence {sequence} not found in actual sequence {actual_sequence}" 