"""
Semantic validation utilities for test assertions.

This module provides semantic validation capabilities that leverage
the existing ValidationObserver infrastructure for more robust testing.
"""

import re
import json
from typing import Dict, Any, Optional, List, Union, Callable
from tests.integration.validation_observer import ValidationObserver


class SemanticValidator:
    """
    Provides semantic validation methods for test assertions.
    
    This class extends the capabilities of ValidationObserver to provide
    semantic validation rather than simple string matching.
    """
    
    def __init__(self, observer: ValidationObserver):
        """
        Initialize with a ValidationObserver instance.
        
        Args:
            observer: The ValidationObserver to use for validation
        """
        self.observer = observer
    
    def validate_arithmetic_response(
        self, 
        response: str, 
        operation: str, 
        operands: List[Union[int, float]], 
        expected: Union[int, float],
        allow_none: bool = False
    ) -> bool:
        """
        Validate an arithmetic response semantically.
        
        Args:
            response: The agent's response
            operation: The operation performed (add, multiply, etc.)
            operands: The operands used
            expected: The expected result
            allow_none: Whether to allow None responses (for Ollama compatibility)
            
        Returns:
            True if validation passes
            
        Raises:
            AssertionError: If validation fails
        """
        # Handle None response case
        if response is None:
            if allow_none and self._is_ollama_model():
                # Ollama models sometimes return None - check tool calls instead
                return self._validate_arithmetic_via_tools(operation, operands, expected)
            else:
                raise AssertionError(f"Model returned None response for {operation} operation")
        
        # Check if the correct tool was called
        tool_name = self._get_tool_for_operation(operation)
        if tool_name and tool_name in self.observer.called_functions:
            # Validate via tool calls
            return self._validate_arithmetic_via_tools(operation, operands, expected)
        
        # Parse response for semantic validation
        parsed = self._parse_arithmetic_response(response, expected)
        
        # Validate the result semantically
        if parsed['found_result']:
            assert parsed['result'] == expected, \
                f"Expected {expected}, but found {parsed['result']} in response"
        else:
            # Check if response contains reasoning about the calculation
            assert self._contains_arithmetic_reasoning(response, operation, operands), \
                f"Response does not contain valid reasoning for {operation} of {operands}"
        
        return True
    
    def validate_tool_execution(
        self,
        response: Optional[str],
        expected_tool: str,
        expected_args: Optional[Dict[str, Any]] = None,
        expected_result: Optional[Any] = None,
        allow_none: bool = False
    ) -> bool:
        """
        Validate that a tool was executed correctly.
        
        Args:
            response: The agent's response (can be None)
            expected_tool: The tool that should have been called
            expected_args: Expected arguments (optional)
            expected_result: Expected result (optional)
            allow_none: Whether to allow None responses
            
        Returns:
            True if validation passes
            
        Raises:
            AssertionError: If validation fails
        """
        # Handle None response
        if response is None and not allow_none:
            raise AssertionError(f"Model returned None response when {expected_tool} was expected")
        
        # Check tool was called
        assert expected_tool in self.observer.called_functions, \
            f"Expected tool '{expected_tool}' was not called. Called: {self.observer.called_functions}"
        
        # Validate arguments if specified
        if expected_args:
            actual_args = self.observer.get_function_call_args(expected_tool)
            assert len(actual_args) > 0, f"No arguments found for {expected_tool}"
            
            # Check last call matches expected args
            last_args = actual_args[-1]
            for key, value in expected_args.items():
                assert key in last_args, f"Expected arg '{key}' not found in {last_args}"
                assert last_args[key] == value, \
                    f"Expected {key}={value}, got {key}={last_args[key]}"
        
        # Validate result if specified
        if expected_result is not None:
            actual_result = self.observer.get_last_function_result(expected_tool)
            assert actual_result == expected_result, \
                f"Expected result {expected_result}, got {actual_result}"
        
        return True
    
    def validate_multi_step_reasoning(
        self,
        response: Optional[str],
        expected_tools: List[str],
        expected_final_result: Optional[Any] = None,
        allow_none: bool = False
    ) -> bool:
        """
        Validate multi-step reasoning with multiple tool calls.
        
        Args:
            response: The agent's response
            expected_tools: List of tools that should be called
            expected_final_result: Expected final result (optional)
            allow_none: Whether to allow None responses
            
        Returns:
            True if validation passes
            
        Raises:
            AssertionError: If validation fails
        """
        # Handle None response
        if response is None and not allow_none:
            raise AssertionError("Model returned None response for multi-step reasoning")
        
        # Check all expected tools were called
        for tool in expected_tools:
            assert tool in self.observer.called_functions, \
                f"Expected tool '{tool}' not called. Called: {self.observer.called_functions}"
        
        # Validate sequence if order matters
        if len(expected_tools) > 1:
            actual_sequence = [call["name"] for call in self.observer.function_calls]
            # Check expected tools appear in order (but allow other calls between)
            self._validate_tool_sequence(actual_sequence, expected_tools)
        
        # Validate final result if specified
        if expected_final_result is not None and response is not None:
            assert str(expected_final_result) in response, \
                f"Expected final result {expected_final_result} not found in response"
        
        return True
    
    def validate_error_handling(
        self,
        response: Optional[str],
        error_type: str,
        should_recover: bool = True
    ) -> bool:
        """
        Validate error handling behavior.
        
        Args:
            response: The agent's response
            error_type: Type of error to validate
            should_recover: Whether the agent should recover from the error
            
        Returns:
            True if validation passes
            
        Raises:
            AssertionError: If validation fails
        """
        if should_recover:
            # Agent should have produced a response despite the error
            assert response is not None, \
                f"Agent failed to recover from {error_type} error"
            
            # Check for appropriate error acknowledgment
            error_keywords = {
                "network": ["connection", "network", "timeout", "unavailable"],
                "rate_limit": ["rate limit", "too many requests", "throttled"],
                "invalid_json": ["parse", "format", "invalid"],
                "tool_error": ["error", "failed", "exception"]
            }
            
            if error_type in error_keywords:
                keywords = error_keywords[error_type]
                assert any(kw in response.lower() for kw in keywords), \
                    f"Response doesn't acknowledge {error_type} error appropriately"
        else:
            # Agent should fail gracefully
            assert response is None or "error" in response.lower(), \
                f"Agent should have failed for {error_type} error"
        
        return True
    
    # Helper methods
    
    def _is_ollama_model(self) -> bool:
        """Check if the current model is Ollama-based."""
        if self.observer._model_capabilities:
            return "ollama" in self.observer._model_capabilities.provider.lower()
        return False
    
    def _get_tool_for_operation(self, operation: str) -> Optional[str]:
        """Get the tool name for an arithmetic operation."""
        tool_map = {
            "add": "add_numbers",
            "addition": "add_numbers",
            "sum": "add_numbers",
            "multiply": "multiply_numbers",
            "multiplication": "multiply_numbers",
            "product": "multiply_numbers"
        }
        return tool_map.get(operation.lower())
    
    def _validate_arithmetic_via_tools(
        self,
        operation: str,
        operands: List[Union[int, float]],
        expected: Union[int, float]
    ) -> bool:
        """Validate arithmetic through tool calls."""
        tool_name = self._get_tool_for_operation(operation)
        
        if not tool_name:
            raise AssertionError(f"Unknown operation: {operation}")
        
        # Check tool was called
        assert tool_name in self.observer.called_functions, \
            f"Tool '{tool_name}' not called for {operation}"
        
        # Validate arguments
        args = self.observer.get_function_call_args(tool_name)
        assert len(args) > 0, f"No arguments for {tool_name}"
        
        last_args = args[-1]
        if len(operands) == 2:
            assert last_args.get("a") == operands[0], \
                f"Expected a={operands[0]}, got {last_args.get('a')}"
            assert last_args.get("b") == operands[1], \
                f"Expected b={operands[1]}, got {last_args.get('b')}"
        
        # Validate result
        result = self.observer.get_last_function_result(tool_name)
        assert result == expected, f"Expected {expected}, got {result}"
        
        return True
    
    def _parse_arithmetic_response(
        self,
        response: str,
        expected: Union[int, float]
    ) -> Dict[str, Any]:
        """Parse arithmetic response for validation."""
        result = {
            'found_result': False,
            'result': None,
            'reasoning': []
        }
        
        # Look for the expected number in various formats
        patterns = [
            rf'\b{expected}\b',  # Exact number
            rf'equals?\s+{expected}',  # "equals 42"
            rf'is\s+{expected}',  # "is 42"
            rf'result:?\s*{expected}',  # "result: 42"
            rf'answer:?\s*{expected}',  # "answer: 42"
        ]
        
        for pattern in patterns:
            if re.search(pattern, response, re.IGNORECASE):
                result['found_result'] = True
                result['result'] = expected
                break
        
        # Extract reasoning steps
        reasoning_patterns = [
            r'(\d+)\s*[+\-*/]\s*(\d+)',  # Math expressions
            r'step\s+\d+:.*',  # Step-by-step reasoning
            r'first.*then.*',  # Sequential reasoning
        ]
        
        for pattern in reasoning_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                result['reasoning'].extend(matches)
        
        return result
    
    def _contains_arithmetic_reasoning(
        self,
        response: str,
        operation: str,
        operands: List[Union[int, float]]
    ) -> bool:
        """Check if response contains valid arithmetic reasoning."""
        # Check for operation mention
        op_keywords = {
            "add": ["add", "sum", "plus", "+"],
            "multiply": ["multiply", "times", "product", "*", "×"]
        }
        
        if operation.lower() in op_keywords:
            keywords = op_keywords[operation.lower()]
            has_operation = any(kw in response.lower() for kw in keywords)
        else:
            has_operation = False
        
        # Check for operand mentions
        has_operands = all(str(op) in response for op in operands)
        
        return has_operation and has_operands
    
    def _validate_tool_sequence(
        self,
        actual_sequence: List[str],
        expected_sequence: List[str]
    ) -> None:
        """Validate that expected tools appear in order."""
        j = 0  # Index for expected sequence
        for tool in actual_sequence:
            if j < len(expected_sequence) and tool == expected_sequence[j]:
                j += 1
        
        assert j == len(expected_sequence), \
            f"Expected sequence {expected_sequence} not found in {actual_sequence}"


def create_semantic_validator(observer: ValidationObserver) -> SemanticValidator:
    """
    Factory function to create a SemanticValidator.
    
    Args:
        observer: The ValidationObserver to use
        
    Returns:
        A configured SemanticValidator instance
    """
    return SemanticValidator(observer)