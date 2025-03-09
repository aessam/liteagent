import pytest
import os
from unittest.mock import patch
from liteagent.models import LiteLLMInterface
from liteagent.provider_roles import process_messages_for_provider


# Skip if MISTRAL_API_KEY is not available
requires_mistral = pytest.mark.skipif(
    os.environ.get("MISTRAL_API_KEY") is None,
    reason="MISTRAL_API_KEY environment variable not set"
)


@requires_mistral
def test_mistral_system_message_handling():
    """Test that Mistral correctly handles system messages when multiple are present."""
    
    # Setup messages with multiple system messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there! How can I help you today?"},
        {"role": "system", "content": "Remember to be concise"},
        {"role": "user", "content": "What's the capital of France?"}
    ]
    
    # Process messages for Mistral
    processed_messages = process_messages_for_provider(messages, "mistral")
    
    # Verify the first system message is preserved
    assert processed_messages[0]["role"] == "system"
    assert "You are a helpful assistant" in processed_messages[0]["content"]
    
    # Verify the second system message is converted to user
    # Find the position of the converted system message
    converted_found = False
    for msg in processed_messages:
        if msg["role"] == "user" and "System instruction: Remember to be concise" in msg["content"]:
            converted_found = True
            break
    
    assert converted_found, "Second system message not properly converted to user message"
    
    # Mock the API call to avoid actual API usage for this test
    with patch.object(LiteLLMInterface, '_call_api', return_value={"choices": [{"message": {"content": "Paris is the capital of France."}}]}):
        model = LiteLLMInterface(model_name="mistral-small-latest")
        response = model.generate_response(messages=messages)
        
        # Just verify we get any response without errors
        assert "Paris" in response["choices"][0]["message"]["content"]


@requires_mistral
def test_mistral_sequence_constraints():
    """Test that Mistral correctly enforces sequence constraints."""
    
    # Setup messages with consecutive assistant messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "assistant", "content": "How can I help you today?"},
        {"role": "user", "content": "What's the capital of France?"}
    ]
    
    # Process messages for Mistral
    processed_messages = process_messages_for_provider(messages, "mistral")
    
    # Check that consecutive assistant roles are handled properly
    # We now expect a "Please continue." user message to be inserted between
    # consecutive assistant messages
    assistant_count = 0
    placeholder_user_found = False
    
    for i, msg in enumerate(processed_messages):
        if msg["role"] == "assistant":
            assistant_count += 1
        # Check if we have a placeholder user message between assistant messages
        if (msg["role"] == "user" and 
            msg["content"] == "Please continue." and
            i > 0 and i < len(processed_messages) - 1 and
            processed_messages[i-1]["role"] == "assistant" and
            processed_messages[i+1]["role"] == "assistant"):
            placeholder_user_found = True
    
    # We should still have two assistant messages but with a user message in between
    assert assistant_count == 2, f"Expected 2 assistant messages, got {assistant_count}"
    assert placeholder_user_found, "Placeholder user message not found between consecutive assistant messages"
    
    # Mock the API call to avoid actual API usage
    with patch.object(LiteLLMInterface, '_call_api', return_value={"choices": [{"message": {"content": "Paris is the capital of France."}}]}):
        model = LiteLLMInterface(model_name="mistral-small-latest")
        response = model.generate_response(messages=messages)
        
        # Just verify we get a response without errors
        assert response["choices"][0]["message"]["content"] 