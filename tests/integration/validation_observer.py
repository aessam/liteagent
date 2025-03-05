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
from liteagent.tool_calling_types import ToolCallingType
from liteagent.validation_strategies import ToolValidationStrategy, get_validation_strategy
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
    
    def __init__(self, tool_calling_type: Optional[ToolCallingType] = None):
        """
        Initialize the validation observer.
        
        Args:
            tool_calling_type: The tool calling type to use for validation.
                If None, no validation strategy will be used until set_validation_strategy is called.
        """
        self.function_calls: List[Dict[str, Any]] = []
        self.function_results: List[Dict[str, Any]] = []
        self.called_functions: Set[str] = set()
        self.function_call_counts: Counter = Counter()
        self.user_messages: List[str] = []
        self.agent_responses: List[str] = []
        
        # Set validation strategy based on tool calling type
        self.strategy: Optional[ToolValidationStrategy] = None
        if tool_calling_type is not None:
            self.set_validation_strategy(tool_calling_type)
        
    def set_validation_strategy(self, tool_calling_type: ToolCallingType):
        """
        Set the validation strategy based on tool calling type.
        
        Args:
            tool_calling_type: The tool calling type to use for validation
        """
        self.strategy = get_validation_strategy(tool_calling_type)
        
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
    
    def register_response_parser(self, function_name: str, parser: ResponseParser):
        """
        Register a custom parser for a specific function's response.
        
        Args:
            function_name: The name of the function to register the parser for
            parser: A function that takes a response string and returns a structured dict
        """
        if self.strategy is None:
            raise ValueError("Cannot register response parser without a validation strategy")
        self.strategy.register_response_parser(function_name, parser)
    
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
        
    def assert_function_not_called(self, function_name: str):
        """
        Assert that a function was not called during the interaction.
        
        Args:
            function_name: The name of the function
        """
        assert function_name not in self.called_functions, f"Function {function_name} was called"
    
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
        if self.strategy is None:
            raise ValueError("Cannot parse response without a validation strategy")
            
        if expected_tool:
            return self.strategy.parse_response(response, expected_tool)
        
        # Default parsing
        return self.strategy.extract_structured_data(response)
    
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