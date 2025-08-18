#!/usr/bin/env python
"""
Test script for the provider_roles module.

This script tests the process_messages_for_provider function with different providers,
especially focusing on Mistral and DeepSeek which have specific role requirements.
"""

import sys
import json
from pprint import pprint

# Add the current directory to the path so we can import liteagent
sys.path.insert(0, '.')

from liteagent.provider_roles import process_messages_for_provider

def test_mistral_roles():
    """Test message processing for Mistral provider."""
    print("\n=== Testing Mistral Provider ===")
    
    # Create a sample conversation with various roles
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, can you help me?"},
        {"role": "assistant", "content": "Yes, I can help you."},
        {"role": "function", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I'll check the weather for you."},
        {"role": "tool", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'}
    ]
    
    # Process messages for Mistral
    processed_messages = process_messages_for_provider(messages, "mistral")
    
    print("Original messages:")
    pprint(messages)
    print("\nProcessed messages for Mistral:")
    pprint(processed_messages)
    
    # Verify that function/tool roles are properly converted
    for msg in processed_messages:
        assert msg["role"] in ["system", "user", "assistant", "tool"], f"Invalid role: {msg['role']}"
        if msg["role"] == "tool":
            assert "name" in msg, "Tool message missing name"

def test_mistral_system_after_assistant():
    """Test Mistral's handling of system messages after assistant messages."""
    print("\n=== Testing Mistral System After Assistant ===")
    
    # Create a conversation with a system message after assistant (which should be invalid for Mistral)
    messages = [
        {"role": "system", "content": "Initial system instruction."},
        {"role": "user", "content": "Hello, can you help me?"},
        {"role": "assistant", "content": "Yes, I can help you."},
        {"role": "system", "content": "New system instruction that should be converted for Mistral."},
        {"role": "user", "content": "Another question."}
    ]
    
    # Process messages for Mistral
    processed_messages = process_messages_for_provider(messages, "mistral")
    
    print("Original messages:")
    pprint(messages)
    print("\nProcessed messages for Mistral:")
    pprint(processed_messages)
    
    # Verify that the first message is a system message
    assert processed_messages[0]["role"] == "system", "First message should be a system message"
    assert processed_messages[0]["content"] == "Initial system instruction.", "First system message content should be preserved"
    
    # Verify that the second system message was converted to a user message
    converted_found = False
    for msg in processed_messages:
        if (msg["role"] == "user" and 
            "System instruction: New system instruction" in msg["content"]):
            converted_found = True
            break
    
    assert converted_found, "Second system message should be converted to a user message"

def test_mistral_consecutive_roles():
    """Test Mistral's handling of consecutive identical roles."""
    print("\n=== Testing Mistral Consecutive Roles ===")
    
    # Create a conversation with consecutive user and assistant messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "First user message."},
        {"role": "user", "content": "Second consecutive user message."},
        {"role": "assistant", "content": "First assistant response."},
        {"role": "assistant", "content": "Second consecutive assistant response."}
    ]
    
    # Process messages for Mistral
    processed_messages = process_messages_for_provider(messages, "mistral")
    
    print("Original messages:")
    pprint(messages)
    print("\nProcessed messages for Mistral:")
    pprint(processed_messages)
    
    # Check if alternating placeholder messages were inserted
    roles = [msg["role"] for msg in processed_messages]
    print("Resulting role sequence:", roles)
    
    # Verify no consecutive identical roles (except possibly system)
    for i in range(1, len(roles)-1):
        if roles[i] == roles[i+1] and roles[i] != "system":
            assert False, f"Found consecutive {roles[i]} roles at positions {i} and {i+1}"

def test_deepseek_roles():
    """Test message processing for DeepSeek provider."""
    print("\n=== Testing DeepSeek Provider ===")
    
    # Create a sample conversation with various roles
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, can you help me?"},
        {"role": "assistant", "content": "Yes, I can help you."},
        {"role": "function", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I'll check the weather for you."},
        {"role": "tool", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'}
    ]
    
    # Process messages for DeepSeek
    processed_messages = process_messages_for_provider(messages, "deepseek")
    
    print("Original messages:")
    pprint(messages)
    print("\nProcessed messages for DeepSeek:")
    pprint(processed_messages)
    
    # Verify that function/tool roles are properly converted
    for msg in processed_messages:
        assert msg["role"] in ["system", "user", "assistant", "tool"], f"Invalid role: {msg['role']}"
        if msg["role"] == "tool":
            assert "name" in msg, "Tool message missing name"

def test_openai_roles():
    """Test message processing for OpenAI provider (should not change)."""
    print("\n=== Testing OpenAI Provider ===")
    
    # Create a sample conversation with various roles
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, can you help me?"},
        {"role": "assistant", "content": "Yes, I can help you."},
        {"role": "function", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I'll check the weather for you."},
        {"role": "tool", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'}
    ]
    
    # Process messages for OpenAI
    processed_messages = process_messages_for_provider(messages, "openai")
    
    print("Original messages:")
    pprint(messages)
    print("\nProcessed messages for OpenAI:")
    pprint(processed_messages)
    
    # For OpenAI, both function and tool roles should be preserved
    function_roles = [msg for msg in processed_messages if msg["role"] in ["function", "tool"]]
    assert len(function_roles) == 2, "Function or tool roles were modified for OpenAI"

def test_anthropic_roles():
    """Test message processing for Anthropic provider."""
    print("\n=== Testing Anthropic Provider ===")
    
    # Create a sample conversation with various roles
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, can you help me?"},
        {"role": "assistant", "content": "Yes, I can help you."},
        {"role": "function", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I'll check the weather for you."},
        {"role": "tool", "name": "get_weather", "content": '{"temperature": 72, "condition": "sunny"}'}
    ]
    
    # Process messages for Anthropic
    processed_messages = process_messages_for_provider(messages, "anthropic")
    
    print("Original messages:")
    pprint(messages)
    print("\nProcessed messages for Anthropic:")
    pprint(processed_messages)
    
    # Verify that function/tool roles are properly converted to the format Anthropic expects
    for msg in processed_messages:
        assert msg["role"] in ["system", "user", "assistant"], f"Invalid role for Anthropic: {msg['role']}"

def main():
    """Run all tests."""
    test_mistral_roles()
    test_mistral_system_after_assistant()
    test_mistral_consecutive_roles()
    test_deepseek_roles()
    test_openai_roles()
    test_anthropic_roles()
    
    print("\n=== All tests completed successfully! ===")

if __name__ == "__main__":
    main() 