"""
Comprehensive deterministic unit tests for the memory management components.

These tests validate ALL functionality of the ConversationMemory class
to achieve 90%+ coverage. NO API calls - pure deterministic testing.
"""

import pytest
import json
from typing import Dict, List, Any

from liteagent.memory import ConversationMemory


class TestConversationMemoryComprehensive:
    """Comprehensive test suite for ConversationMemory class."""
    
    @pytest.fixture
    def system_prompt(self) -> str:
        """Fixture providing a standard system prompt for tests."""
        return "You are a helpful AI assistant. Use the provided tools when needed."
    
    @pytest.fixture
    def memory(self, system_prompt: str) -> ConversationMemory:
        """Fixture providing a standard ConversationMemory instance."""
        return ConversationMemory(system_prompt=system_prompt)
    
    def test_initialization(self, system_prompt: str):
        """Test memory initialization with system prompt."""
        memory = ConversationMemory(system_prompt)
        
        assert memory.system_prompt == system_prompt
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "system"
        assert memory.messages[0]["content"] == system_prompt
        assert memory.function_calls == {}
        assert memory.last_function_call is None
    
    def test_add_user_message(self, memory: ConversationMemory):
        """Test adding user messages."""
        # Test single message
        user_message = "What's the weather like today?"
        memory.add_user_message(user_message)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "user"
        assert memory.messages[1]["content"] == user_message
        
        # Test multiple messages
        second_message = "How about tomorrow?"
        memory.add_user_message(second_message)
        
        assert len(memory.messages) == 3
        assert memory.messages[2]["role"] == "user"
        assert memory.messages[2]["content"] == second_message
    
    def test_add_assistant_message(self, memory: ConversationMemory):
        """Test adding assistant messages."""
        # Test single message
        assistant_message = "I'll help you find the weather information."
        memory.add_assistant_message(assistant_message)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "assistant"
        assert memory.messages[1]["content"] == assistant_message
        
        # Test multiple messages
        second_message = "Let me check the forecast for you."
        memory.add_assistant_message(second_message)
        
        assert len(memory.messages) == 3
        assert memory.messages[2]["role"] == "assistant"
        assert memory.messages[2]["content"] == second_message
    
    def test_add_system_message(self, memory: ConversationMemory):
        """Test adding system messages."""
        system_message = "Additional system instructions."
        memory.add_system_message(system_message)
        
        assert len(memory.messages) == 2
        assert memory.messages[1]["role"] == "system"
        assert memory.messages[1]["content"] == system_message
    
    def test_add_function_call(self, memory: ConversationMemory):
        """Test adding function calls in OpenAI format."""
        # Test without call_id
        function_name = "get_weather"
        args = {"city": "New York", "units": "celsius"}
        memory.add_function_call(function_name, args)
        
        assert len(memory.messages) == 2
        message = memory.messages[1]
        assert message["role"] == "assistant"
        assert message["content"] is None
        assert message["function_call"]["name"] == function_name
        assert json.loads(message["function_call"]["arguments"]) == args
        
        # Check tracking
        assert function_name in memory.function_calls
        assert len(memory.function_calls[function_name]) == 1
        assert memory.function_calls[function_name][0]["args"] == args
        
        # Test with call_id
        call_id = "func_123"
        memory.add_function_call(function_name, args, call_id)
        
        assert len(memory.messages) == 3
        assert len(memory.function_calls[function_name]) == 2
        assert memory.function_calls[function_name][1]["call_id"] == call_id
    
    def test_add_function_call_string_args(self, memory: ConversationMemory):
        """Test function call with string arguments."""
        function_name = "search"
        args = "weather in Tokyo"  # String instead of dict
        memory.add_function_call(function_name, args)
        
        message = memory.messages[1]
        assert message["function_call"]["arguments"] == args
    
    def test_add_tool_call(self, memory: ConversationMemory):
        """Test adding tool calls in modern OpenAI format."""
        tool_name = "calculate"
        args = {"a": 5, "b": 3, "operation": "add"}
        call_id = "call_456"
        
        memory.add_tool_call(tool_name, args, call_id)
        
        assert len(memory.messages) == 2
        message = memory.messages[1]
        assert message["role"] == "assistant"
        assert message["content"] is None
        assert len(message["tool_calls"]) == 1
        
        tool_call = message["tool_calls"][0]
        assert tool_call["id"] == call_id
        assert tool_call["type"] == "function"
        assert tool_call["function"]["name"] == tool_name
        assert json.loads(tool_call["function"]["arguments"]) == args
        
        # Check tracking
        assert tool_name in memory.function_calls
        assert len(memory.function_calls[tool_name]) == 1
        assert memory.function_calls[tool_name][0]["args"] == args
        assert memory.function_calls[tool_name][0]["call_id"] == call_id
    
    def test_add_function_result_default(self, memory: ConversationMemory):
        """Test adding function results in default (modern tool) format."""
        function_name = "get_weather"
        content = '{"temp": 72, "condition": "sunny"}'
        args = {"city": "New York"}
        call_id = "func_123"
        
        memory.add_function_result(function_name, content, args, call_id)
        
        assert len(memory.messages) == 2
        message = memory.messages[1]
        assert message["role"] == "tool"
        assert message["name"] == function_name
        assert message["content"] == content
        assert message["tool_call_id"] == call_id
        assert message["args"] == args
        
        # Check last function call tracking
        assert memory.last_function_call["name"] == function_name
        assert memory.last_function_call["result"] == content
        assert memory.last_function_call["args"] == args
        assert memory.last_function_call["call_id"] == call_id
    
    def test_add_function_result_anthropic(self, memory: ConversationMemory):
        """Test adding function results for Anthropic provider."""
        function_name = "get_weather"
        content = '{"temp": 65, "condition": "cloudy"}'
        args = {"city": "London"}
        
        memory.add_function_result(function_name, content, args, provider="anthropic")
        
        assert len(memory.messages) == 2
        message = memory.messages[1]
        assert message["role"] == "assistant"
        expected_content = f"I called the {function_name} function with {args} and got this result: {content}"
        assert message["content"] == expected_content
    
    def test_add_function_result_with_error(self, memory: ConversationMemory):
        """Test adding function results with error flag."""
        function_name = "api_call"
        content = "API timeout error"
        
        memory.add_function_result(function_name, content, is_error=True)
        
        message = memory.messages[1]
        assert message["role"] == "tool"
        assert message["is_error"] is True
    
    def test_add_function_result_minimal(self, memory: ConversationMemory):
        """Test adding function result with minimal parameters."""
        function_name = "simple_func"
        content = "result"
        
        memory.add_function_result(function_name, content)
        
        message = memory.messages[1]
        assert message["role"] == "tool"
        assert message["name"] == function_name
        assert message["content"] == content
        assert "tool_call_id" not in message
        assert "args" not in message
    
    def test_add_tool_result(self, memory: ConversationMemory):
        """Test adding tool results in modern format."""
        tool_name = "calculator"
        content = "8"
        call_id = "call_789"
        
        memory.add_tool_result(tool_name, content, call_id)
        
        assert len(memory.messages) == 2
        message = memory.messages[1]
        assert message["role"] == "tool"
        assert message["content"] == content
        assert message["tool_call_id"] == call_id
        assert message["name"] == tool_name
    
    def test_add_tool_result_with_error(self, memory: ConversationMemory):
        """Test adding tool result with error flag."""
        content = "Division by zero"
        call_id = "call_error"
        
        memory.add_tool_result("calculator", content, call_id, is_error=True)
        
        message = memory.messages[1]
        assert message["is_error"] is True
    
    def test_add_tool_result_no_name(self, memory: ConversationMemory):
        """Test adding tool result without name (some models don't require it)."""
        content = "result"
        call_id = "call_123"
        
        memory.add_tool_result("", content, call_id)
        
        message = memory.messages[1]
        assert "name" not in message
        assert message["tool_call_id"] == call_id
    
    def test_get_messages_all(self, memory: ConversationMemory):
        """Test getting all messages."""
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi there")
        memory.add_function_result("test", "result", {"arg": "value"})
        
        messages = memory.get_messages()
        assert len(messages) == 4  # system + user + assistant + tool
        
        # Check that internal fields are filtered out
        tool_message = messages[3]
        assert "args" not in tool_message
        assert "is_error" not in tool_message
        assert "function_call_id" not in tool_message
    
    def test_get_messages_limited(self, memory: ConversationMemory):
        """Test getting limited number of messages."""
        memory.add_user_message("Message 1")
        memory.add_user_message("Message 2")
        memory.add_user_message("Message 3")
        
        # Get last 2 messages
        messages = memory.get_messages(count=2)
        assert len(messages) == 2
        assert messages[0]["content"] == "Message 2"
        assert messages[1]["content"] == "Message 3"
    
    def test_has_function_been_called(self, memory: ConversationMemory):
        """Test checking if function has been called with specific args."""
        function_name = "get_weather"
        args1 = {"city": "New York"}
        args2 = {"city": "London"}
        
        # Initially not called
        assert not memory.has_function_been_called(function_name, args1)
        
        # Add a function call
        memory.add_function_call(function_name, args1)
        
        # Now it should be found
        assert memory.has_function_been_called(function_name, args1)
        assert not memory.has_function_been_called(function_name, args2)
        
        # Test with function that was never called
        assert not memory.has_function_been_called("unknown_func", {})
    
    def test_reset(self, memory: ConversationMemory, system_prompt: str):
        """Test resetting memory to initial state."""
        # Add various messages
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi")
        memory.add_function_call("test", {"arg": "value"})
        memory.last_function_call = {"name": "test"}
        
        assert len(memory.messages) > 1
        assert len(memory.function_calls) > 0
        assert memory.last_function_call is not None
        
        # Reset
        memory.reset()
        
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "system"
        assert memory.messages[0]["content"] == system_prompt
        assert memory.function_calls == {}
        assert memory.last_function_call is None
    
    def test_clear_alias(self, memory: ConversationMemory):
        """Test that clear() is an alias for reset()."""
        memory.add_user_message("Test")
        assert len(memory.messages) > 1
        
        memory.clear()
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "system"
    
    def test_update_system_prompt_existing(self, memory: ConversationMemory):
        """Test updating system prompt when one exists."""
        new_prompt = "You are a specialized assistant for weather information."
        
        memory.update_system_prompt(new_prompt)
        
        assert memory.system_prompt == new_prompt
        assert memory.messages[0]["role"] == "system"
        assert memory.messages[0]["content"] == new_prompt
    
    def test_update_system_prompt_no_existing(self):
        """Test updating system prompt when none exists."""
        # Create memory without system message
        memory = ConversationMemory("")
        memory.messages = []  # Clear system message
        
        new_prompt = "New system prompt"
        memory.update_system_prompt(new_prompt)
        
        assert memory.system_prompt == new_prompt
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "system"
        assert memory.messages[0]["content"] == new_prompt
    
    def test_is_function_call_loop_detection(self, memory: ConversationMemory):
        """Test function call loop detection."""
        function_name = "get_weather"
        args = {"city": "New York"}
        
        # First call - not a loop
        assert not memory.is_function_call_loop(function_name, args)
        memory.add_function_call(function_name, args)
        
        # Second call - not a loop yet
        assert not memory.is_function_call_loop(function_name, args)
        memory.add_function_call(function_name, args)
        
        # Third call - now it's a loop
        assert memory.is_function_call_loop(function_name, args)
        
        # Different args - not a loop
        different_args = {"city": "London"}
        assert not memory.is_function_call_loop(function_name, different_args)
    
    def test_is_function_call_loop_normalization(self, memory: ConversationMemory):
        """Test argument normalization in loop detection."""
        function_name = "search"
        
        # Args with quotes
        args1 = {"query": '"weather"'}
        args2 = {"query": "'weather'"}
        args3 = {"query": "weather"}
        
        memory.add_function_call(function_name, args1)
        memory.add_function_call(function_name, args2)
        
        # These should be considered the same due to normalization
        assert memory.is_function_call_loop(function_name, args3)
    
    def test_get_last_function_result(self, memory: ConversationMemory):
        """Test getting last result from specific function."""
        # No results initially
        assert memory.get_last_function_result("weather") is None
        
        # Add some function results
        memory.add_function_result("weather", "sunny", provider="openai")
        memory.add_function_result("calculator", "42")
        memory.add_function_result("weather", "rainy")
        
        # Should get the last weather result
        assert memory.get_last_function_result("weather") == "rainy"
        assert memory.get_last_function_result("calculator") == "42"
        assert memory.get_last_function_result("unknown") is None
    
    def test_get_last_function_result_legacy_format(self, memory: ConversationMemory):
        """Test getting result from legacy 'function' role messages."""
        # Manually add a legacy function message
        memory.messages.append({
            "role": "function", 
            "name": "legacy_func",
            "content": "legacy result"
        })
        
        assert memory.get_last_function_result("legacy_func") == "legacy result"
    
    def test_message_ordering(self, memory: ConversationMemory):
        """Test that messages maintain proper order."""
        memory.add_user_message("First user message")
        memory.add_assistant_message("First assistant message")
        memory.add_user_message("Second user message")
        memory.add_function_call("test", {"arg": "value"})
        memory.add_function_result("test", "result")
        memory.add_assistant_message("Second assistant message")
        
        messages = memory.get_messages()
        roles = [msg["role"] for msg in messages]
        expected_roles = ["system", "user", "assistant", "user", "assistant", "tool", "assistant"]
        assert roles == expected_roles
    
    def test_function_calls_tracking_multiple_functions(self, memory: ConversationMemory):
        """Test tracking multiple different functions."""
        # Add calls to different functions
        memory.add_function_call("weather", {"city": "NY"})
        memory.add_function_call("calculator", {"a": 1, "b": 2})
        memory.add_function_call("weather", {"city": "LA"})
        
        assert len(memory.function_calls) == 2
        assert len(memory.function_calls["weather"]) == 2
        assert len(memory.function_calls["calculator"]) == 1
        
        # Check specific calls
        weather_calls = memory.function_calls["weather"]
        assert weather_calls[0]["args"] == {"city": "NY"}
        assert weather_calls[1]["args"] == {"city": "LA"}
    
    def test_last_function_call_tracking(self, memory: ConversationMemory):
        """Test that last_function_call is properly tracked."""
        # Initially None
        assert memory.last_function_call is None
        
        # After function result
        memory.add_function_result("test", "result", {"arg": "value"}, "call_123")
        
        assert memory.last_function_call["name"] == "test"
        assert memory.last_function_call["result"] == "result"
        assert memory.last_function_call["args"] == {"arg": "value"}
        assert memory.last_function_call["call_id"] == "call_123"
        
        # After loop detection
        memory.is_function_call_loop("another", {"x": 1})
        
        assert memory.last_function_call["name"] == "another"
        assert memory.last_function_call["args"] == {"x": 1}
        assert "result" not in memory.last_function_call  # Only name and args from loop detection
    
    def test_edge_cases_empty_content(self, memory: ConversationMemory):
        """Test edge cases with empty or None content."""
        # Empty string content
        memory.add_user_message("")
        memory.add_assistant_message("")
        memory.add_function_result("test", "")
        
        assert memory.messages[1]["content"] == ""
        assert memory.messages[2]["content"] == ""
        assert memory.messages[3]["content"] == ""
        
        # None content (converted to string)
        memory.add_function_result("test2", None)
        assert memory.messages[4]["content"] == "None"
    
    def test_edge_cases_empty_args(self, memory: ConversationMemory):
        """Test edge cases with empty arguments."""
        memory.add_function_call("test", {})
        
        message = memory.messages[1]
        assert json.loads(message["function_call"]["arguments"]) == {}
        
        # Check loop detection with empty args using fresh function name
        func_name = "loop_test"
        empty_args = {}
        
        # First call - not a loop
        assert not memory.is_function_call_loop(func_name, empty_args)
        memory.add_function_call(func_name, empty_args)
        
        # Second call - not a loop yet  
        assert not memory.is_function_call_loop(func_name, empty_args)
        memory.add_function_call(func_name, empty_args)
        
        # Third call - now it's a loop
        assert memory.is_function_call_loop(func_name, empty_args)


if __name__ == "__main__":
    pytest.main(["-v", __file__])