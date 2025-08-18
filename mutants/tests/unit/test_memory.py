"""
Unit tests for the memory management components.

These tests validate the functionality of the ConversationMemory class and related
components that manage conversation history.
"""

import pytest
from typing import Dict, List

from liteagent.memory import ConversationMemory


class TestConversationMemory:
    """Test suite for the ConversationMemory class."""
    
    @pytest.fixture
    def system_prompt(self) -> str:
        """Fixture providing a standard system prompt for tests."""
        return "You are a helpful AI assistant. Use the provided tools when needed."
    
    @pytest.fixture
    def memory(self, system_prompt: str) -> ConversationMemory:
        """Fixture providing a standard ConversationMemory instance."""
        return ConversationMemory(system_prompt=system_prompt)
    
    def test_initialization(self, memory: ConversationMemory, system_prompt: str) -> None:
        """Test that memory is initialized correctly with a system prompt."""
        assert memory.system_prompt == system_prompt
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "system"
        assert memory.messages[0]["content"] == system_prompt
        assert memory.function_calls == {}
        assert memory.last_function_call is None
    
    def test_add_user_message(self, memory: ConversationMemory) -> None:
        """Test adding a user message to memory."""
        user_message = "What's the weather like today?"
        memory.add_user_message(user_message)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "user"
        assert memory.messages[1]["content"] == user_message
    
    def test_add_assistant_message(self, memory: ConversationMemory) -> None:
        """Test adding an assistant message to memory."""
        assistant_message = "I'll help you find the weather."
        memory.add_assistant_message(assistant_message)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "assistant"
        assert memory.messages[1]["content"] == assistant_message
    
    def test_add_function_result(self, memory: ConversationMemory) -> None:
        """Test adding a function result to memory."""
        # Add a function result with basic params
        memory.add_function_result("get_weather", '{"temp": 72, "condition": "sunny"}')
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "tool"  # Modern format uses 'tool' instead of 'function'
        assert memory.messages[1]["name"] == "get_weather"
        assert memory.messages[1]["content"] == '{"temp": 72, "condition": "sunny"}'
        
        # Test with additional parameters
        args = {"city": "New York"}
        call_id = "func_123"
        memory.add_function_result(
            "get_weather", 
            '{"temp": 65, "condition": "cloudy"}',
            args=args,
            call_id=call_id
        )
        
        assert len(memory.messages) == 3
        assert memory.messages[2]["role"] == "tool"  # Modern format uses 'tool' instead of 'function'
        assert memory.messages[2]["name"] == "get_weather"
        assert memory.messages[2]["content"] == '{"temp": 65, "condition": "cloudy"}'
        assert memory.last_function_call == {
            "name": "get_weather",
            "args": args,
            "call_id": call_id,
            "result": '{"temp": 65, "condition": "cloudy"}'
        }
    
    def test_add_function_call(self, memory: ConversationMemory) -> None:
        """Test adding a function call to memory."""
        # Add a function call with required parameters
        name = "get_weather"
        args = {"city": "San Francisco"}
        
        memory.add_function_call(name, args)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "assistant"
        assert memory.messages[1]["content"] is None
        assert "function_call" in memory.messages[1]
        assert memory.messages[1]["function_call"]["name"] == name
        assert memory.messages[1]["function_call"]["arguments"] == '{"city": "San Francisco"}'
        
        # Verify function call is tracked
        assert name in memory.function_calls
        assert len(memory.function_calls[name]) == 1
        assert memory.function_calls[name][0]["args"] == args
    
    def test_add_tool_call(self, memory: ConversationMemory) -> None:
        """Test adding a tool call to memory."""
        # Add a tool call
        name = "get_weather"
        args = {"city": "San Francisco"}
        call_id = "tool_123"
        
        memory.add_tool_call(name, args, call_id=call_id)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "assistant"
        assert memory.messages[1]["content"] is None
        assert "tool_calls" in memory.messages[1]
        assert len(memory.messages[1]["tool_calls"]) == 1
        assert memory.messages[1]["tool_calls"][0]["type"] == "function"
        assert memory.messages[1]["tool_calls"][0]["function"]["name"] == name
        assert memory.messages[1]["tool_calls"][0]["function"]["arguments"] == '{"city": "San Francisco"}'
        assert memory.messages[1]["tool_calls"][0]["id"] == call_id
        
        # Verify function call is tracked
        assert name in memory.function_calls
        assert len(memory.function_calls[name]) == 1
        assert memory.function_calls[name][0]["args"] == args
        assert memory.function_calls[name][0]["call_id"] == call_id
    
    def test_add_tool_result(self, memory: ConversationMemory) -> None:
        """Test adding a tool result to memory."""
        # Add a tool result
        name = "get_weather"
        call_id = "tool_123"
        content = '{"temp": 72, "condition": "sunny"}'
        
        memory.add_tool_result(name, content, call_id=call_id)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "tool"
        assert memory.messages[1]["content"] == content
        assert memory.messages[1]["tool_call_id"] == call_id
        
        # Test with error
        memory.add_tool_result("get_weather", "API Error", call_id="tool_456", is_error=True)
        
        assert len(memory.messages) == 3
        assert memory.messages[2]["role"] == "tool"
        assert memory.messages[2]["content"] == "API Error"
        assert memory.messages[2]["tool_call_id"] == "tool_456"
    
    def test_get_messages(self, memory: ConversationMemory) -> None:
        """Test retrieving messages from memory."""
        # Add some messages
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi there!")
        memory.add_user_message("How are you?")
        
        # Get all messages
        messages = memory.get_messages()
        assert len(messages) == 4  # system + 3 messages
        
        # Get only the last 2 messages
        last_messages = memory.get_messages(count=2)
        assert len(last_messages) == 2
        assert last_messages[0]["role"] == "assistant"
        assert last_messages[0]["content"] == "Hi there!"
        assert last_messages[1]["role"] == "user"
        assert last_messages[1]["content"] == "How are you?"
    
    def test_has_function_been_called(self, memory: ConversationMemory) -> None:
        """Test checking if a function has been called with specific arguments."""
        # Add a function call
        memory.add_function_call("get_weather", {"city": "Boston"})
        
        # Check if function was called with same arguments
        assert memory.has_function_been_called("get_weather", {"city": "Boston"}) is True
        
        # Check with different arguments
        assert memory.has_function_been_called("get_weather", {"city": "Seattle"}) is False
        
        # Check with non-existent function
        assert memory.has_function_been_called("calculate_age", {"year": 1990}) is False
    
    def test_clear(self, memory: ConversationMemory, system_prompt: str) -> None:
        """Test clearing the memory."""
        # Add some messages
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi there!")
        memory.add_function_call("get_weather", {"city": "Boston"})
        
        # Clear memory
        memory.clear()
        
        # Verify state after clearing
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "system"
        assert memory.messages[0]["content"] == system_prompt
        assert memory.function_calls == {}
        assert memory.last_function_call is None 