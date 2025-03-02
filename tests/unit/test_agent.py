"""
Unit tests for LiteAgent using mock LLM implementations.

This module contains tests for the core functionality of LiteAgent 
using a mock LLM to avoid real API calls during testing.
"""

import json
import pytest
from unittest.mock import MagicMock, patch, call

# Import our testing utilities
from tests.unit.test_mock_llm import MockModelInterface

# Import LiteAgent components
from liteagent.agent import LiteAgent
from liteagent.observer import (AgentInitializedEvent, UserMessageEvent, 
                              ModelRequestEvent, ModelResponseEvent, 
                              FunctionCallEvent, FunctionResultEvent, 
                              AgentResponseEvent)


class TestAgentWithMockLLM:
    """Test the LiteAgent class with a mock LLM."""
    
    def test_agent_initialization(self, agent_with_mock_model):
        """Test that the agent initializes correctly with a mock model."""
        agent = agent_with_mock_model
        
        assert agent.name == "test-agent"
        assert agent.model_name == "mock-model"
        assert agent.system_prompt == "You are a test agent."
        assert isinstance(agent.model_interface, MockModelInterface)
    
    def test_agent_simple_chat(self, agent_with_mock_model):
        """Test that the agent can handle a simple chat interaction."""
        agent = agent_with_mock_model
        
        # Set up the mock to return a predefined response
        agent.model_interface.responses = [
            {"type": "text", "content": "This is a test response."}
        ]
        
        # Chat with the agent
        response = agent.chat("Hello, agent!")
        
        # Verify the response
        assert response == "This is a test response."
        assert len(agent.model_interface.generate_response_calls) == 1
        
        # Check that the message was properly added to memory
        messages = agent.memory.get_messages()
        assert len(messages) == 3  # System prompt + user message + assistant response
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a test agent."
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello, agent!"
        assert messages[2]["role"] == "assistant"
        assert messages[2]["content"] == "This is a test response."
    
    def test_agent_with_function_call(self, agent_with_tools):
        """Test that the agent properly handles function calling."""
        agent = agent_with_tools
        
        # Set up the mock to return a function call followed by a text response
        agent.model_interface.responses = [
            {
                "type": "function_call",
                "function_name": "example_function",
                "function_args": {"param1": "test value", "param2": 42}
            },
            {"type": "text", "content": "I've called the function for you."}
        ]
        
        # Chat with the agent
        response = agent.chat("Call a function please")
        
        # Verify the response
        assert response == "I've called the function for you."
        
        # Check that the function was called with the right parameters
        messages = agent.memory.get_messages()
        
        # Find the function result message
        function_results = [msg for msg in messages if msg["role"] == "function" and msg["name"] == "example_function"]
        
        # Verify function result exists
        assert len(function_results) == 1
        
        # Verify function result details
        function_result = function_results[0]
        assert function_result["role"] == "function"
        assert function_result["name"] == "example_function"
        assert "Function called with param1=test value, param2=42" in function_result["content"]
        
        # Verify that the model_interface was called with the right function
        assert len(agent.model_interface.generate_response_calls) >= 2
        first_call = agent.model_interface.generate_response_calls[0]
        assert "functions" in first_call
        assert first_call["functions"] is not None
        
        # Verify that the final response was added to memory
        assert messages[-1]["role"] == "assistant"
        assert messages[-1]["content"] == "I've called the function for you."
    
    def test_agent_with_observer(self, agent_with_mock_model, mock_observer):
        """Test that the agent properly emits events to observers."""
        agent = agent_with_mock_model
        agent.add_observer(mock_observer)
        
        # Set up the mock to return a text response
        agent.model_interface.responses = [
            {"type": "text", "content": "This is a test response."}
        ]
        
        # Chat with the agent
        response = agent.chat("Hello, agent!")
        
        # Verify that the observer methods were called
        assert mock_observer.on_user_message.called
        assert mock_observer.on_model_request.called
        assert mock_observer.on_model_response.called
        assert mock_observer.on_agent_response.called
        
        # Verify the arguments of the calls
        user_message_call = mock_observer.on_user_message.call_args[0][0]
        assert isinstance(user_message_call, UserMessageEvent)
        assert user_message_call.message == "Hello, agent!"
        
        agent_response_call = mock_observer.on_agent_response.call_args[0][0]
        assert isinstance(agent_response_call, AgentResponseEvent)
        assert agent_response_call.response == "This is a test response."
    
    def test_agent_with_conversation(self, agent_with_conversation_model):
        """Test that the agent can handle a multi-turn conversation with function calling."""
        agent = agent_with_conversation_model
        
        # Chat with the agent to start the conversation
        response1 = agent.chat("I need some data.")
        
        # First response should be text
        assert response1 == "I'll help you with that."
        
        # The model's next response should trigger a function call (get_data)
        # Since we don't have a "get_data" function registered, it should fail
        # and then move to the next response
        response2 = agent.chat("Please get the data now.")
        
        # Final response should be text
        assert response2 == "Based on the data, here's your answer..."
    
    def test_agent_reset_memory(self, agent_with_mock_model):
        """Test that the agent can reset its memory."""
        agent = agent_with_mock_model
        
        # Set up the mock to return a predefined response
        agent.model_interface.responses = [
            {"type": "text", "content": "This is a test response."}
        ]
        
        # Chat with the agent
        agent.chat("Hello, agent!")
        
        # Verify memory has conversation
        messages = agent.memory.get_messages()
        assert len(messages) == 3  # System prompt + user message + assistant response
        
        # Reset memory
        agent.reset_memory()
        
        # Verify only system prompt remains
        messages = agent.memory.get_messages()
        assert len(messages) == 1
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a test agent."
    
    def test_consecutive_function_calls(self, agent_with_tools):
        """Test the agent's handling of consecutive function calls."""
        agent = agent_with_tools
        
        # Set up the mock to return multiple function calls
        agent.model_interface.responses = [
            {
                "type": "function_call",
                "function_name": "example_function",
                "function_args": {"param1": "first call", "param2": 1}
            },
            {
                "type": "function_call",
                "function_name": "example_function",
                "function_args": {"param1": "second call", "param2": 2}
            },
            {
                "type": "function_call",
                "function_name": "example_function",
                "function_args": {"param1": "third call", "param2": 3}
            },
            {"type": "text", "content": "I've called the functions."}
        ]
        
        # Chat with the agent
        response = agent.chat("Call some functions")
        
        # Verify the final response
        assert response == "I've called the functions."
        
        # Check that all functions were called
        messages = agent.memory.get_messages()
        
        # Count function results
        function_results = [msg for msg in messages if msg["role"] == "function" and msg["name"] == "example_function"]
        assert len(function_results) == 3
        
        # Verify function results
        results_content = [result["content"] for result in function_results]
        assert "Function called with param1=first call, param2=1" in results_content
        assert "Function called with param1=second call, param2=2" in results_content
        assert "Function called with param1=third call, param2=3" in results_content
    
    def test_repeated_function_call_prevention(self, agent_with_tools):
        """Test that the agent prevents repeated function calls with the same arguments."""
        agent = agent_with_tools
        
        # Set up the mock to return repeated function calls
        agent.model_interface.responses = [
            {
                "type": "function_call",
                "function_name": "example_function",
                "function_args": {"param1": "repeated", "param2": 1}
            },
            {
                "type": "function_call",
                "function_name": "example_function",
                "function_args": {"param1": "repeated", "param2": 1}  # Same args as before
            },
            {"type": "text", "content": "Final response after prevention."}
        ]
        
        # Chat with the agent
        response = agent.chat("Call a function repeatedly")
        
        # The agent should prevent the repeated call and force a text response
        assert response == "Final response after prevention."
        
        # Check the messages to see that a system message was added to prevent repetition
        messages = agent.memory.get_messages()
        system_messages = [msg for msg in messages if msg["role"] == "system" and "called the same function multiple times" in msg["content"]]
        assert len(system_messages) > 0
        
        # Function should only have been called once despite two attempts
        function_results = [msg for msg in messages if msg["role"] == "function" and msg["name"] == "example_function"]
        assert len(function_results) == 1


if __name__ == "__main__":
    pytest.main(["-v", "test_agent.py"]) 