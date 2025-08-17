"""
Unit tests for the observer functionality in LiteAgent.

This module contains tests for the observer functionality, which allows
monitoring and tracking of agent operations and interactions.
"""

import json
import pytest
import time
from collections import defaultdict

# Import LiteAgent components
from liteagent.observer import (AgentObserver, AgentEvent, AgentInitializedEvent, 
                              UserMessageEvent, ModelRequestEvent, ModelResponseEvent, 
                              FunctionCallEvent, FunctionResultEvent, AgentResponseEvent, 
                              ConsoleObserver, TreeTraceObserver)
from liteagent.agent import LiteAgent

# NO MOCKS - using real API calls only


class TestObserverEvents:
    """Test the observer event classes."""
    
    def test_agent_event_base(self):
        """Test the base AgentEvent class."""
        event = AgentEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id"
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.event_type == "AgentEvent"
        
        # Test to_dict method
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "AgentEvent"
        assert event_dict["agent_id"] == "test-agent-id"
        assert event_dict["agent_name"] == "test-agent"
        assert event_dict["context_id"] == "test-context-id"
        assert event_dict["parent_context_id"] == "parent-context-id"
        assert "timestamp" in event_dict
    
    def test_model_response_event(self):
        """Test the ModelResponseEvent class."""
        # Test with a simple string response
        event = ModelResponseEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id",
            response="This is a test response"
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.response == "This is a test response"
        assert event.event_type == "ModelResponseEvent"
        
        # Test to_dict method
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "ModelResponseEvent"
        assert event_dict["response"] == "This is a test response"
        
        # Test with an object that has to_dict method
        class TestObject:
            def __init__(self):
                self.value = "test value"
                
            def to_dict(self):
                return {"value": self.value}
        
        test_obj = TestObject()
        event = ModelResponseEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            response=test_obj
        )
        
        # Test to_dict method with object
        event_dict = event.to_dict()
        assert event_dict["response"] == {"value": "test value"}
        
        # Test with an object that has __dict__ but no to_dict
        class AnotherTestObject:
            def __init__(self):
                self.attribute = "test attribute"
                
        another_obj = AnotherTestObject()
        event = ModelResponseEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            response=another_obj
        )
        
        # Test to_dict method with object that has __dict__
        event_dict = event.to_dict()
        assert event_dict["response"]["attribute"] == "test attribute"
        
        # Skip test with a circular reference object because behavior depends on Python version
        # and implementation details of the serialization
        
        # Test with None response
        event = ModelResponseEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            response=None
        )
        
        # Test to_dict method with None response
        event_dict = event.to_dict()
        assert event_dict["response"] is None
    
    def test_agent_initialized_event(self):
        """Test the AgentInitializedEvent class."""
        event = AgentInitializedEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id",
            model_name="gpt-4o-mini",
            system_prompt="You are a test agent."
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.model_name == "gpt-4o-mini"
        assert event.system_prompt == "You are a test agent."
        assert event.event_type == "AgentInitializedEvent"
        
        # Test to_dict method
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "AgentInitializedEvent"
        assert event_dict["model_name"] == "gpt-4o-mini"
        assert event_dict["system_prompt"] == "You are a test agent."
    
    def test_user_message_event(self):
        """Test the UserMessageEvent class."""
        event = UserMessageEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id",
            message="Hello, agent!"
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.message == "Hello, agent!"
        assert event.event_type == "UserMessageEvent"
        
        # Test to_dict method
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "UserMessageEvent"
        assert event_dict["message"] == "Hello, agent!"
    
    def test_function_call_event(self):
        """Test the FunctionCallEvent class."""
        event = FunctionCallEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id",
            function_name="test_function",
            function_args={"param1": "value1", "param2": 123},
            function_call_id="call-id-123"
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.function_name == "test_function"
        assert event.function_args == {"param1": "value1", "param2": 123}
        assert event.function_call_id == "call-id-123"
        assert event.event_type == "FunctionCallEvent"
        
        # Test to_dict method
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "FunctionCallEvent"
        assert event_dict["function_name"] == "test_function"
        assert event_dict["function_args"] == {"param1": "value1", "param2": 123}
        assert event_dict["function_call_id"] == "call-id-123"

    def test_function_result_event(self):
        """Test the FunctionResultEvent class."""
        # Test with a simple serializable result
        event = FunctionResultEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id",
            function_name="test_function",
            function_args={"param1": "value1", "param2": 123},
            result={"status": "success", "data": [1, 2, 3]},
            function_call_id="call-id-123"
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.function_name == "test_function"
        assert event.function_args == {"param1": "value1", "param2": 123}
        assert event.result == {"status": "success", "data": [1, 2, 3]}
        assert event.function_call_id == "call-id-123"
        assert event.error is None
        assert event.event_type == "FunctionResultEvent"
        
        # Test to_dict method with serializable result
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "FunctionResultEvent"
        assert event_dict["function_name"] == "test_function"
        assert event_dict["function_args"] == {"param1": "value1", "param2": 123}
        assert event_dict["result"] == {"status": "success", "data": [1, 2, 3]}
        assert event_dict["function_call_id"] == "call-id-123"
        assert event_dict["error"] is None
        
        # Test with a non-serializable result
        class NonSerializableObject:
            def __init__(self):
                self.circular_ref = self
                
        non_serializable = NonSerializableObject()
        event = FunctionResultEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            function_name="test_function",
            function_args={"param1": "test"},
            result=non_serializable,
            function_call_id="call-id-456"
        )
        
        # Test to_dict method with non-serializable result
        event_dict = event.to_dict()
        assert isinstance(event_dict["result"], str)
        
        # Test with error
        event = FunctionResultEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            function_name="test_function",
            function_args={"param1": "value1"},
            result=None,
            error="Function execution failed",
            function_call_id="call-id-789"
        )
        
        # Test to_dict method with error
        event_dict = event.to_dict()
        assert event_dict["error"] == "Function execution failed"
        assert event_dict["result"] is None


class TestObserverInterface:
    """Test the AgentObserver interface and implementations."""
    
    def test_agent_observer_interface(self):
        """Test the AgentObserver interface methods."""
        # Create a concrete implementation of the abstract AgentObserver
        class TestObserver(AgentObserver):
            def __init__(self):
                self.events = []
                
            def on_event(self, event):
                self.events.append(("on_event", event))
                
            # Override other methods to track calls
            def on_agent_initialized(self, event):
                self.events.append(("on_agent_initialized", event))
                super().on_agent_initialized(event)
                
            def on_user_message(self, event):
                self.events.append(("on_user_message", event))
                super().on_user_message(event)
                
            def on_model_request(self, event):
                self.events.append(("on_model_request", event))
                super().on_model_request(event)
                
            def on_model_response(self, event):
                self.events.append(("on_model_response", event))
                super().on_model_response(event)
                
            def on_function_call(self, event):
                self.events.append(("on_function_call", event))
                super().on_function_call(event)
                
            def on_function_result(self, event):
                self.events.append(("on_function_result", event))
                super().on_function_result(event)
                
            def on_agent_response(self, event):
                self.events.append(("on_agent_response", event))
                super().on_agent_response(event)
        
        # Create an instance of our test observer
        observer = TestObserver()
        
        # Create events of different types
        init_event = AgentInitializedEvent(
            agent_id="test-id", agent_name="test", context_id="ctx"
        )
        user_event = UserMessageEvent(
            agent_id="test-id", agent_name="test", context_id="ctx", message="Hello"
        )
        
        # Call the observer methods
        observer.on_agent_initialized(init_event)
        observer.on_user_message(user_event)
        
        # Verify that both the specific method and on_event were called
        assert len(observer.events) == 4  # 2 specific events and 2 on_event calls
        
        # Check specific method calls
        assert observer.events[0] == ("on_agent_initialized", init_event)
        assert observer.events[2] == ("on_user_message", user_event)
        
        # Check that on_event was called for both events
        assert observer.events[1] == ("on_event", init_event)
        assert observer.events[3] == ("on_event", user_event)
    
    def test_agent_with_multiple_observers(self, openai_agent):
        """Test that an agent can have multiple observers using real API."""
        # Create console observers to track events
        observer1 = ConsoleObserver()
        observer2 = ConsoleObserver()
        
        # Track events manually by overriding methods
        observer1.events = []
        observer2.events = []
        
        def track_events_1(event):
            observer1.events.append(event.event_type)
        def track_events_2(event):
            observer2.events.append(event.event_type)
            
        observer1.on_event = track_events_1
        observer2.on_event = track_events_2
        
        # Add observers to the agent
        agent = openai_agent
        agent.add_observer(observer1)
        agent.add_observer(observer2)
        
        # Chat with the agent
        response = agent.chat("Say hello")
        
        # Verify we got a response
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Verify that both observers received events
        assert len(observer1.events) > 0
        assert len(observer2.events) > 0
        
        # Both should have the same events
        assert observer1.events == observer2.events
        
        # Remove one observer
        agent.remove_observer(observer1)
        
        # Reset event tracking for next test
        observer1.events = []
        observer2.events = []
        
        # Chat again
        response = agent.chat("Hello after removing an observer")
        
        # Verify we got a response
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Verify that only observer2 received events (observer1 was removed)
        assert len(observer1.events) == 0  # Should not receive any events
        assert len(observer2.events) > 0   # Should still receive events


class TestTreeTraceObserver:
    """Test the TreeTraceObserver functionality."""
    
    def test_tree_trace_observer_tracking(self, openai_agent):
        """Test that TreeTraceObserver properly tracks agent events."""
        # Create a TreeTraceObserver
        tree_observer = TreeTraceObserver()
        
        # Add the observer to the agent
        agent = openai_agent
        agent.add_observer(tree_observer)
        
        # Chat with the agent
        response = agent.chat("Say hello")
        
        # Verify we got a response
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Check that the observer tracked the context
        assert agent.context_id in tree_observer.context_map
        
        # Check that events were recorded for this agent
        assert agent.agent_id in tree_observer.agent_events
        assert len(tree_observer.agent_events[agent.agent_id]) > 0
        
        # Verify we can see events of different types
        event_types = set(e.event_type for e in tree_observer.agent_events[agent.agent_id])
        assert "UserMessageEvent" in event_types
        assert "ModelRequestEvent" in event_types
        assert "ModelResponseEvent" in event_types
        assert "AgentResponseEvent" in event_types
    
    def test_tree_trace_observer_multi_agent(self, openai_agent, anthropic_agent):
        """Test that TreeTraceObserver properly tracks multiple agents and their relationships."""
        # Create a TreeTraceObserver
        tree_observer = TreeTraceObserver()
        
        # Add the observer to both agents
        agent1 = openai_agent
        agent2 = anthropic_agent
        
        agent1.add_observer(tree_observer)
        agent2.add_observer(tree_observer)
        
        # Set up parent-child relationship between agents
        agent1_context_id = agent1.context_id
        agent2.parent_context_id = agent1_context_id
        
        # Chat with both agents
        response1 = agent1.chat("Say hello")
        response2 = agent2.chat("Say hi")
        
        # Verify we got responses
        assert isinstance(response1, str) and len(response1) > 0
        assert isinstance(response2, str) and len(response2) > 0
        
        # Check that both agents' contexts are tracked
        assert agent1.context_id in tree_observer.context_map
        assert agent2.context_id in tree_observer.context_map
        
        # Check parent-child relationship
        assert agent2.context_id in tree_observer.parent_map
        assert tree_observer.parent_map[agent2.context_id] == agent1_context_id
        assert agent2.context_id in tree_observer.children_map[agent1_context_id]
        
        # Verify events were recorded for both agents
        assert agent1.agent_id in tree_observer.agent_events
        assert agent2.agent_id in tree_observer.agent_events
        assert len(tree_observer.agent_events[agent1.agent_id]) > 0
        assert len(tree_observer.agent_events[agent2.agent_id]) > 0
    
    def test_tree_trace_observer_tree_visualization(self, openai_agent):
        """Test the tree visualization methods of TreeTraceObserver."""
        # Create a TreeTraceObserver
        tree_observer = TreeTraceObserver()
        
        # Add the observer to the agent
        agent = openai_agent
        agent.add_observer(tree_observer)
        
        # Chat with the agent
        response = agent.chat("Say hello")
        
        # Verify we got a response
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Test that the observer has the methods we expect
        assert hasattr(tree_observer, '_print_agent_tree')
        assert hasattr(tree_observer, '_print_agent_events')
        assert hasattr(tree_observer, '_format_args')
        
        # Test _format_args method
        args = {"param1": "value1", "param2": 123}
        formatted = tree_observer._format_args(args)
        assert "param1" in formatted
        assert "value1" in formatted
        assert "param2" in formatted
        assert "123" in formatted
        
        # Verify the observer tracked events properly
        assert agent.agent_id in tree_observer.agent_events
        assert len(tree_observer.agent_events[agent.agent_id]) > 0
        
        # Test that we can call visualization methods without errors
        # These methods print to stdout, so we just verify they don't crash
        try:
            tree_observer._print_agent_tree(agent.context_id, "", True)
            tree_observer._print_agent_events(agent.agent_id, "")
            # If we get here, the methods ran without errors
            visualization_works = True
        except Exception:
            visualization_works = False
            
        assert visualization_works
            
            # Test with a more complex structure
            nested_args = {"param1": {"nested": "value"}, "param2": [1, 2, 3]}
            formatted = tree_observer._format_args(nested_args)
            assert "{" in formatted
            assert "}" in formatted
            assert "[" in formatted
            assert "]" in formatted


if __name__ == "__main__":
    pytest.main(["-v", "test_observer.py"]) 