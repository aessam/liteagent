"""
Comprehensive deterministic unit tests for the observer module.

This module tests the observer pattern dependency injection implementation
to achieve 90%+ coverage. Tests are purely deterministic - no API calls.
Focuses on event creation, observer interface, and dependency injection mechanics.
"""

import pytest
import time
import json
from typing import Dict, List, Any
from collections import defaultdict

from liteagent.observer import (
    AgentEvent, AgentInitializedEvent, UserMessageEvent, ModelRequestEvent,
    ModelResponseEvent, FunctionCallEvent, FunctionResultEvent, AgentResponseEvent,
    AgentObserver, ConsoleObserver, TreeTraceObserver
)


class TestAgentEvents:
    """Test all agent event classes for proper functionality."""
    
    def test_agent_event_base(self):
        """Test the base AgentEvent class."""
        agent_id = "test-agent-123"
        agent_name = "test-agent"
        context_id = "ctx-456"
        parent_context_id = "parent-ctx-789"
        timestamp = 1234567890.0
        event_data = {"key": "value", "number": 42}
        
        event = AgentEvent(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            timestamp=timestamp,
            event_data=event_data
        )
        
        # Test properties
        assert event.agent_id == agent_id
        assert event.agent_name == agent_name
        assert event.context_id == context_id
        assert event.parent_context_id == parent_context_id
        assert event.timestamp == timestamp
        assert event.event_type == "AgentEvent"
        assert event.event_data == event_data
        
        # Test to_dict method (event_data is merged into the dict, not as a separate key)
        event_dict = event.to_dict()
        assert event_dict["agent_id"] == agent_id
        assert event_dict["agent_name"] == agent_name
        assert event_dict["context_id"] == context_id
        assert event_dict["parent_context_id"] == parent_context_id
        assert event_dict["timestamp"] == timestamp
        assert event_dict["event_type"] == "AgentEvent"
        # event_data fields are merged into the main dict
        assert event_dict["key"] == "value"
        assert event_dict["number"] == 42
    
    def test_agent_event_defaults(self):
        """Test AgentEvent with default values."""
        before_time = time.time()
        
        event = AgentEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="test-ctx"
        )
        
        after_time = time.time()
        
        # Check defaults
        assert event.parent_context_id is None
        assert before_time <= event.timestamp <= after_time
        assert event.event_data == {}
    
    def test_agent_event_kwargs(self):
        """Test AgentEvent with additional kwargs."""
        event = AgentEvent(
            agent_id="test-id",
            agent_name="test-name", 
            context_id="test-ctx",
            extra_param="extra_value"
        )
        
        # Should not crash and should have basic properties
        assert event.agent_id == "test-id"
        assert event.event_type == "AgentEvent"
    
    def test_agent_initialized_event(self):
        """Test AgentInitializedEvent."""
        model = "gpt-4"
        system_prompt = "You are a helpful assistant"
        tools = ["calculator", "weather"]
        
        event = AgentInitializedEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            model=model,
            system_prompt=system_prompt,
            tools=tools
        )
        
        assert event.event_type == "AgentInitializedEvent"
        assert event.model_name == model
        assert event.system_prompt == system_prompt
        assert event.tools == tools
        
        event_dict = event.to_dict()
        assert event_dict["model_name"] == model
        assert event_dict["system_prompt"] == system_prompt
    
    def test_user_message_event(self):
        """Test UserMessageEvent."""
        message = "Hello, how are you?"
        
        event = UserMessageEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            message=message
        )
        
        assert event.event_type == "UserMessageEvent"
        assert event.message == message
        
        event_dict = event.to_dict()
        assert event_dict["message"] == message
    
    def test_model_request_event(self):
        """Test ModelRequestEvent."""
        messages = [{"role": "user", "content": "Hello"}]
        model = "gpt-4o-mini"
        functions = [{"name": "calculator"}]  # Uses functions, not tools
        
        event = ModelRequestEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            messages=messages,
            model=model,
            functions=functions
        )
        
        assert event.event_type == "ModelRequestEvent"
        assert event.messages == messages
        assert event.model == model
        assert event.functions == functions
        
        event_dict = event.to_dict()
        assert event_dict["messages"] == messages
        assert event_dict["model"] == model
        assert event_dict["functions"] == functions
    
    def test_model_response_event(self):
        """Test ModelResponseEvent."""
        response = "Hello! I'm doing well, thank you."
        model = "gpt-4o-mini"
        
        event = ModelResponseEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            response=response,
            model=model
        )
        
        assert event.event_type == "ModelResponseEvent"
        assert event.response == response
        assert event.model == model
        
        event_dict = event.to_dict()
        # Response is summarized in event_data
        assert event_dict["model"] == model
        assert "response_summary" in event_dict
    
    def test_function_call_event(self):
        """Test FunctionCallEvent."""
        function_name = "get_weather"
        function_args = {"city": "New York", "units": "celsius"}
        
        event = FunctionCallEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            function_name=function_name,
            function_args=function_args
        )
        
        assert event.event_type == "FunctionCallEvent"
        assert event.function_name == function_name
        assert event.function_args == function_args
        
        event_dict = event.to_dict()
        assert event_dict["function_name"] == function_name
        assert event_dict["function_args"] == function_args
    
    def test_function_result_event(self):
        """Test FunctionResultEvent."""
        function_name = "get_weather"
        result = '{"temperature": 72, "condition": "sunny"}'
        
        event = FunctionResultEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            function_name=function_name,
            result=result
        )
        
        assert event.event_type == "FunctionResultEvent"
        assert event.function_name == function_name
        assert event.result == result
        
        event_dict = event.to_dict()
        assert event_dict["function_name"] == function_name
    
    def test_function_result_event_with_error(self):
        """Test FunctionResultEvent with error flag."""
        event = FunctionResultEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            function_name="api_call",
            result="API timeout",
            error="Timeout occurred"
        )
        
        assert event.error == "Timeout occurred"
        assert event.to_dict()["function_name"] == "api_call"
    
    def test_agent_response_event(self):
        """Test AgentResponseEvent."""
        response = "Based on the weather data, it's sunny and 72°F."
        
        event = AgentResponseEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-123",
            response=response
        )
        
        assert event.event_type == "AgentResponseEvent"
        assert event.response == response
        
        event_dict = event.to_dict()
        assert event_dict["response"] == response


class TestObserverInterface:
    """Test the observer interface and dependency injection."""
    
    def test_agent_observer_abstract_interface(self):
        """Test that AgentObserver is properly abstract."""
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            AgentObserver()
    
    def test_console_observer_creation(self):
        """Test ConsoleObserver instantiation and interface."""
        observer = ConsoleObserver()
        
        # Check that it implements the required methods
        assert hasattr(observer, 'on_event')
        assert hasattr(observer, 'on_agent_initialized')
        assert hasattr(observer, 'on_user_message')
        assert hasattr(observer, 'on_model_request')
        assert hasattr(observer, 'on_model_response')
        assert hasattr(observer, 'on_function_call')
        assert hasattr(observer, 'on_function_result')
        assert hasattr(observer, 'on_agent_response')
        
        # Check default behavior
        assert observer.verbose is False
    
    def test_console_observer_with_verbose(self):
        """Test ConsoleObserver with verbose mode."""
        observer = ConsoleObserver(verbose=True)
        
        assert observer.verbose is True
    
    def test_tree_trace_observer_creation(self):
        """Test TreeTraceObserver instantiation."""
        observer = TreeTraceObserver()
        
        # Check data structures are initialized
        assert isinstance(observer.context_map, dict)
        assert isinstance(observer.parent_map, dict)
        assert isinstance(observer.children_map, defaultdict)
        assert isinstance(observer.agent_events, defaultdict)
        
        # Check that it has required methods
        assert hasattr(observer, 'on_agent_initialized')
        assert hasattr(observer, '_format_args')
        assert hasattr(observer, '_print_agent_tree')
        assert hasattr(observer, '_print_agent_events')


class TestEventHandling:
    """Test event handling and observer pattern mechanics."""
    
    def test_console_observer_event_handling(self):
        """Test that ConsoleObserver handles events properly."""
        observer = ConsoleObserver()
        
        # Test agent initialized event
        init_event = AgentInitializedEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            model="gpt-4"
        )
        
        # Should not raise exceptions
        observer.on_agent_initialized(init_event)
        observer.on_event(init_event)
        
        # Test user message event
        user_event = UserMessageEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            message="Hello"
        )
        
        observer.on_user_message(user_event)
        observer.on_event(user_event)
        
        # Test model request event
        model_req_event = ModelRequestEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            messages=[{"role": "user", "content": "Hello"}],
            model="gpt-4",
            functions=[]
        )
        
        observer.on_model_request(model_req_event)
        observer.on_event(model_req_event)
        
        # Test model response event
        model_resp_event = ModelResponseEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            response="Hi there!",
            model="gpt-4"
        )
        
        observer.on_model_response(model_resp_event)
        observer.on_event(model_resp_event)
        
        # Test function call event
        func_call_event = FunctionCallEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            function_name="test_func",
            function_args={"arg": "value"}
        )
        
        observer.on_function_call(func_call_event)
        observer.on_event(func_call_event)
        
        # Test function result event
        func_result_event = FunctionResultEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            function_name="test_func",
            result="result",
            error=None
        )
        
        observer.on_function_result(func_result_event)
        observer.on_event(func_result_event)
        
        # Test agent response event
        agent_resp_event = AgentResponseEvent(
            agent_id="test-id",
            agent_name="test-name",
            context_id="ctx-123",
            response="Final response"
        )
        
        observer.on_agent_response(agent_resp_event)
        observer.on_event(agent_resp_event)
    
    def test_tree_trace_observer_event_tracking(self):
        """Test TreeTraceObserver tracks events properly."""
        observer = TreeTraceObserver()
        
        # Test agent initialized event
        init_event = AgentInitializedEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-456",
            parent_context_id="parent-ctx-789",
            model="gpt-4"
        )
        
        observer.on_agent_initialized(init_event)
        
        # Check that context and relationships are tracked
        assert init_event.context_id in observer.context_map
        assert observer.context_map[init_event.context_id] == init_event.agent_id
        
        if init_event.parent_context_id:
            assert init_event.context_id in observer.parent_map
            assert observer.parent_map[init_event.context_id] == init_event.parent_context_id
            assert init_event.context_id in observer.children_map[init_event.parent_context_id]
        
        # Check that events are stored
        assert init_event.agent_id in observer.agent_events
        assert len(observer.agent_events[init_event.agent_id]) == 1
        assert observer.agent_events[init_event.agent_id][0] == init_event
        
        # Test adding another event for the same agent
        user_event = UserMessageEvent(
            agent_id="agent-123",
            agent_name="test-agent",
            context_id="ctx-456",
            message="Hello"
        )
        
        observer.on_event(user_event)
        
        # Should have 2 events now
        assert len(observer.agent_events["agent-123"]) == 2
        assert observer.agent_events["agent-123"][1] == user_event
    
    def test_tree_trace_observer_parent_child_relationships(self):
        """Test TreeTraceObserver tracks parent-child relationships."""
        observer = TreeTraceObserver()
        
        # Parent agent
        parent_event = AgentInitializedEvent(
            agent_id="parent-agent",
            agent_name="parent",
            context_id="parent-ctx"
        )
        
        observer.on_agent_initialized(parent_event)
        
        # Child agent
        child_event = AgentInitializedEvent(
            agent_id="child-agent",
            agent_name="child",
            context_id="child-ctx",
            parent_context_id="parent-ctx"
        )
        
        observer.on_agent_initialized(child_event)
        
        # Check relationships
        assert child_event.context_id in observer.parent_map
        assert observer.parent_map[child_event.context_id] == parent_event.context_id
        assert child_event.context_id in observer.children_map[parent_event.context_id]
        
        # Grandchild agent
        grandchild_event = AgentInitializedEvent(
            agent_id="grandchild-agent",
            agent_name="grandchild",
            context_id="grandchild-ctx",
            parent_context_id="child-ctx"
        )
        
        observer.on_agent_initialized(grandchild_event)
        
        # Check nested relationships
        assert grandchild_event.context_id in observer.parent_map
        assert observer.parent_map[grandchild_event.context_id] == child_event.context_id
        assert grandchild_event.context_id in observer.children_map[child_event.context_id]


class TestUtilityMethods:
    """Test utility methods in observers."""
    
    def test_tree_trace_observer_format_args(self):
        """Test the _format_args method."""
        observer = TreeTraceObserver()
        
        # Test simple args
        simple_args = {"param1": "value1", "param2": 123}
        formatted = observer._format_args(simple_args)
        assert "param1='value1'" in formatted
        assert "param2=123" in formatted
        
        # Test nested args
        nested_args = {
            "simple": "value",
            "nested": {"key": "nested_value"},
            "list": [1, 2, 3]
        }
        formatted = observer._format_args(nested_args)
        assert "simple='value'" in formatted
        assert "nested=" in formatted
        assert "list=" in formatted
        
        # Test empty args
        empty_formatted = observer._format_args({})
        assert empty_formatted == ""
        
        # Test None
        none_formatted = observer._format_args(None)
        assert none_formatted == ""
    
    def test_tree_trace_observer_visualization_methods_exist(self):
        """Test that visualization methods exist and are callable."""
        observer = TreeTraceObserver()
        
        # Add some test data
        observer.context_map["test-ctx"] = "test-agent"
        observer.agents["test-agent"] = {
            "name": "test",
            "contexts": set(["test-ctx"])
        }
        observer.agent_events["test-agent"] = [
            AgentInitializedEvent(
                agent_id="test-agent",
                agent_name="test",
                context_id="test-ctx"
            )
        ]
        
        # Test methods exist and are callable (they print to stdout)
        try:
            # _print_agent_tree is an alias that calls _print_context_trace with indent 0
            observer._print_agent_tree("test-ctx", "", True)
            observer._print_agent_events("test-agent", "")
            # If we get here, methods ran without errors
            methods_work = True
        except Exception as e:
            # Debug the exception
            print(f"Error in visualization methods: {e}")
            methods_work = False
        
        assert methods_work


class TestObserverDependencyInjection:
    """Test the dependency injection aspects of observers."""
    
    def test_observer_interface_compliance(self):
        """Test that observers implement the required interface."""
        # Create observers
        console_observer = ConsoleObserver()
        tree_observer = TreeTraceObserver()
        
        # Test required methods exist
        required_methods = [
            'on_event', 'on_agent_initialized', 'on_user_message',
            'on_model_request', 'on_model_response', 'on_function_call',
            'on_function_result', 'on_agent_response'
        ]
        
        for method_name in required_methods:
            assert hasattr(console_observer, method_name)
            assert callable(getattr(console_observer, method_name))
            assert hasattr(tree_observer, method_name)
            assert callable(getattr(tree_observer, method_name))
    
    def test_observer_isolation(self):
        """Test that observers maintain independent state."""
        observer1 = TreeTraceObserver()
        observer2 = TreeTraceObserver()
        
        # Add event to observer1
        event1 = AgentInitializedEvent(
            agent_id="agent-1",
            agent_name="test1",
            context_id="ctx-1"
        )
        observer1.on_agent_initialized(event1)
        
        # Add different event to observer2
        event2 = AgentInitializedEvent(
            agent_id="agent-2",
            agent_name="test2", 
            context_id="ctx-2"
        )
        observer2.on_agent_initialized(event2)
        
        # Check that observers have independent state
        assert "ctx-1" in observer1.context_map
        assert "ctx-1" not in observer2.context_map
        assert "ctx-2" in observer2.context_map
        assert "ctx-2" not in observer1.context_map
        
        assert "agent-1" in observer1.agent_events
        assert "agent-1" not in observer2.agent_events
        assert "agent-2" in observer2.agent_events
        assert "agent-2" not in observer1.agent_events
    
    def test_multiple_observers_same_event(self):
        """Test that multiple observers can handle the same event."""
        console_observer = ConsoleObserver()
        tree_observer = TreeTraceObserver()
        
        # Create an event
        event = UserMessageEvent(
            agent_id="test-agent",
            agent_name="test",
            context_id="test-ctx",
            message="Test message"
        )
        
        # Both observers should handle the event without interference
        console_observer.on_user_message(event)
        tree_observer.on_user_message(event)
        
        # TreeTraceObserver should have stored the event
        assert "test-agent" in tree_observer.agent_events
        assert len(tree_observer.agent_events["test-agent"]) == 1
        assert tree_observer.agent_events["test-agent"][0] == event
        
        # ConsoleObserver doesn't store events, just logs them
        # No exception should have been raised


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_event_with_none_values(self):
        """Test events with None values."""
        event = ModelResponseEvent(
            agent_id="test-agent",
            agent_name="test",
            context_id="test-ctx",
            response=None,
            model=None
        )
        
        assert event.response is None
        # model gets default value
        assert event.model == "unknown"
        
        event_dict = event.to_dict()
        assert event_dict["model"] == "unknown"
    
    def test_event_with_empty_collections(self):
        """Test events with empty collections."""
        event = ModelRequestEvent(
            agent_id="test-agent",
            agent_name="test",
            context_id="test-ctx",
            messages=[],
            model="",
            functions=[]
        )
        
        assert event.messages == []
        # Empty model gets default value
        assert event.model == "unknown"  
        assert event.functions == []
    
    def test_observer_with_invalid_events(self):
        """Test that observers handle unusual event data gracefully."""
        observer = TreeTraceObserver()
        
        # Event with missing optional fields
        minimal_event = AgentEvent(
            agent_id="test-agent",
            agent_name="test",
            context_id="test-ctx"
        )
        
        # Should not raise exceptions
        observer.on_event(minimal_event)
        
        # Check that event was stored
        assert "test-agent" in observer.agent_events
        assert len(observer.agent_events["test-agent"]) == 1


if __name__ == "__main__":
    pytest.main(["-v", __file__])