"""
Observer for validation in integration tests.

This module provides specialized observer classes for validation of agent
behavior in integration tests.
"""

from typing import Dict, List, Optional, Any, Set
from liteagent.observer import AgentObserver, AgentEvent, FunctionCallEvent, FunctionResultEvent

class ValidationObserver(AgentObserver):
    """
    Observer for validating agent behavior in integration tests.
    
    This observer tracks function calls and can be used to validate that
    specific functions were called or not called during agent interactions.
    """
    
    def __init__(self):
        """Initialize the validation observer."""
        self.function_calls: List[Dict[str, Any]] = []
        self.function_results: List[Dict[str, Any]] = []
        self.called_functions: Set[str] = set()
        self.user_messages: List[str] = []
        self.agent_responses: List[str] = []
        
    def on_event(self, event: AgentEvent):
        """Base handler for all events."""
        # This is required to satisfy the AgentObserver abstract base class
        pass
        
    def on_function_call(self, event: FunctionCallEvent):
        """Record function call event."""
        super().on_function_call(event)
        
        # Add function call info - make sure we're using function_args from the event
        # Print for debugging
        print(f"Processing function call: {event.function_name} with args: {event.function_args}")
        
        self.function_calls.append({
            "name": event.function_name,
            "arguments": event.function_args
        })
        self.called_functions.add(event.function_name)
        
    def on_function_result(self, event: FunctionResultEvent):
        """Record function result event."""
        super().on_function_result(event)
        self.function_results.append({
            "name": event.function_name,
            "result": event.result
        })
    
    def on_user_message(self, event):
        """Record user message."""
        super().on_user_message(event)
        self.user_messages.append(event.message)
        
    def on_agent_response(self, event):
        """Record agent response."""
        super().on_agent_response(event)
        self.agent_responses.append(event.response)
        
    def assert_function_called(self, function_name: str):
        """Assert that a function was called during the interaction."""
        assert function_name in self.called_functions, f"Function {function_name} was not called"
        
    def assert_function_not_called(self, function_name: str):
        """Assert that a function was not called during the interaction."""
        assert function_name not in self.called_functions, f"Function {function_name} was called"
        
    def assert_function_called_with(self, function_name: str, **kwargs):
        """Assert that a function was called with specific arguments."""
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
        
    def reset(self):
        """Reset the observer state."""
        self.function_calls = []
        self.function_results = []
        self.called_functions = set()
        self.user_messages = []
        self.agent_responses = [] 