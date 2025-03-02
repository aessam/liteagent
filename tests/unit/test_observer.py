"""
Unit tests for the observer functionality in LiteAgent.

This module contains tests for the observer functionality, which allows
monitoring and tracking of agent operations and interactions.
"""

import json
import pytest
import time
from unittest.mock import MagicMock, patch, call
from collections import defaultdict

# Import LiteAgent components
from liteagent.observer import (AgentObserver, AgentEvent, AgentInitializedEvent, 
                              UserMessageEvent, ModelRequestEvent, ModelResponseEvent, 
                              FunctionCallEvent, FunctionResultEvent, AgentResponseEvent, 
                              ConsoleObserver, TreeTraceObserver)

# Import our testing utilities
from tests.unit.test_mock_llm import MockModelInterface


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
    
    def test_agent_initialized_event(self):
        """Test the AgentInitializedEvent class."""
        event = AgentInitializedEvent(
            agent_id="test-agent-id",
            agent_name="test-agent",
            context_id="test-context-id",
            parent_context_id="parent-context-id",
            model_name="gpt-4",
            system_prompt="You are a test agent."
        )
        
        # Test properties
        assert event.agent_id == "test-agent-id"
        assert event.agent_name == "test-agent"
        assert event.context_id == "test-context-id"
        assert event.parent_context_id == "parent-context-id"
        assert event.model_name == "gpt-4"
        assert event.system_prompt == "You are a test agent."
        assert event.event_type == "AgentInitializedEvent"
        
        # Test to_dict method
        event_dict = event.to_dict()
        assert event_dict["event_type"] == "AgentInitializedEvent"
        assert event_dict["model_name"] == "gpt-4"
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
    
    def test_agent_with_multiple_observers(self, agent_with_mock_model):
        """Test that an agent can have multiple observers."""
        # Create mock observers
        observer1 = MagicMock(spec=AgentObserver)
        observer2 = MagicMock(spec=AgentObserver)
        
        # Add observers to the agent
        agent = agent_with_mock_model
        agent.add_observer(observer1)
        agent.add_observer(observer2)
        
        # Configure the mock to return a text response
        agent.model_interface.responses = [
            {"type": "text", "content": "Response with multiple observers."}
        ]
        
        # Chat with the agent
        agent.chat("Hello with multiple observers")
        
        # Verify that both observers received events
        assert observer1.on_user_message.called
        assert observer1.on_model_request.called
        assert observer1.on_model_response.called
        assert observer1.on_agent_response.called
        
        assert observer2.on_user_message.called
        assert observer2.on_model_request.called
        assert observer2.on_model_response.called
        assert observer2.on_agent_response.called
        
        # Remove one observer
        agent.remove_observer(observer1)
        
        # Reset mock call counts
        observer1.reset_mock()
        observer2.reset_mock()
        
        # Chat again
        agent.chat("Hello after removing an observer")
        
        # Verify that only observer2 received events
        assert not observer1.on_user_message.called
        assert observer2.on_user_message.called


class TestTreeTraceObserver:
    """Test the TreeTraceObserver functionality."""
    
    def test_tree_trace_observer_tracking(self, agent_with_mock_model):
        """Test that TreeTraceObserver properly tracks agent events."""
        # Create a TreeTraceObserver
        tree_observer = TreeTraceObserver()
        
        # Add the observer to the agent
        agent = agent_with_mock_model
        agent.add_observer(tree_observer)
        
        # Configure the mock to return a text response
        agent.model_interface.responses = [
            {"type": "text", "content": "Hello from the agent!"}
        ]
        
        # Chat with the agent
        agent.chat("Hello, agent!")
        
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


if __name__ == "__main__":
    pytest.main(["-v", "test_observer.py"]) 