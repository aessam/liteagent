#!/usr/bin/env python
"""
Unit tests for the provider_roles module with a focus on Ollama provider.

This module tests the special handling for Ollama providers, especially
tool calling functionality that requires embedding tool calls in messages.
"""

import pytest
from typing import Dict, List
from pprint import pprint

from liteagent.provider_roles import process_messages_for_provider


def test_ollama_system_prompt_augmentation():
    """Test that Ollama's system prompt is augmented with tool information."""
    # Create a system message with tools
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
            "tools": [
                {
                    "name": "get_weather",
                    "description": "Get the current weather for a city."
                },
                {
                    "name": "add_numbers",
                    "description": "Add two numbers together."
                }
            ]
        },
        {"role": "user", "content": "What's the weather in London?"}
    ]
    
    # Process messages for Ollama
    processed_messages = process_messages_for_provider(messages, "ollama")
    
    # Verify system message is augmented with tool information
    system_msg = processed_messages[0]
    assert system_msg["role"] == "system", "First message should be system message"
    assert "You have access to the following tools:" in system_msg["content"], "System prompt should include tool info"
    assert "get_weather" in system_msg["content"], "System prompt should mention get_weather tool"
    assert "add_numbers" in system_msg["content"], "System prompt should mention add_numbers tool"
    assert "To use a tool" in system_msg["content"], "System prompt should include tool usage instructions"


def test_ollama_tool_calls_embedding():
    """Test that tool calls are properly embedded in user messages for Ollama."""
    # Create a conversation with tool calls and responses
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather in London?"},
        {"role": "assistant", "content": "I'll check the weather for you."},
        {"role": "function", "name": "get_weather", "content": '{"temperature": 18, "condition": "cloudy"}'},
        {"role": "assistant", "content": "The weather in London is 18°C and cloudy."}
    ]
    
    # Process messages for Ollama
    processed_messages = process_messages_for_provider(messages, "ollama")
    
    # Verify function calls are embedded as user messages
    found_tool_msg = False
    for msg in processed_messages:
        if msg["role"] == "user" and "Tool result from get_weather" in msg["content"]:
            found_tool_msg = True
            break
    
    assert found_tool_msg, "Function call should be converted to a user message with the tool result"
    
    # Verify we have the right message alternation
    roles = [msg["role"] for msg in processed_messages]
    print("Resulting role sequence:", roles)
    
    # Check for proper alternation
    for i in range(1, len(roles)-1):
        assert roles[i] != roles[i+1] or roles[i] == "system", \
            f"Found consecutive {roles[i]} roles at positions {i} and {i+1}"


def test_ollama_last_message_constraint():
    """Test that the last message is always a user message for Ollama."""
    # Create a conversation ending with assistant message
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there! How can I help you today?"}
    ]
    
    # Process messages for Ollama
    processed_messages = process_messages_for_provider(messages, "ollama")
    
    # Verify last message is a user message
    assert processed_messages[-1]["role"] == "user", "Last message must be a user message for Ollama"
    assert processed_messages[-1]["content"] == "Continue.", "A default 'Continue.' message should be added"


def test_ollama_with_multiple_tool_calls():
    """Test handling of multiple tool calls in a conversation with Ollama."""
    # Create a conversation with multiple tool calls
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather in London?"},
        {"role": "assistant", "content": "I'll check the weather for you."},
        {"role": "tool", "name": "get_weather", "content": '{"temperature": 18, "condition": "cloudy"}'},
        {"role": "assistant", "content": "The weather in London is 18°C and cloudy. Can I help with anything else?"},
        {"role": "user", "content": "What's 7 * 9?"},
        {"role": "assistant", "content": "Let me calculate that for you."},
        {"role": "tool", "name": "multiply", "content": '{"result": 63}'},
        {"role": "assistant", "content": "7 * 9 = 63"}
    ]
    
    # Process messages for Ollama
    processed_messages = process_messages_for_provider(messages, "ollama")
    
    # Verify both tool calls are embedded as user messages
    tool_results_found = 0
    for msg in processed_messages:
        if msg["role"] == "user" and "Tool result from" in msg["content"]:
            tool_results_found += 1
    
    assert tool_results_found == 2, f"Expected 2 embedded tool results, found {tool_results_found}"
    
    # Verify no consecutive identical roles
    roles = [msg["role"] for msg in processed_messages]
    for i in range(1, len(roles)-1):
        assert roles[i] != roles[i+1] or roles[i] == "system", \
            f"Found consecutive {roles[i]} roles at positions {i} and {i+1}"


if __name__ == "__main__":
    # This allows running the tests directly from the command line
    pytest.main(["-xvs", __file__]) 