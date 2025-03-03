"""
Integration tests showcasing the ValidationObserver for test validation.

These tests demonstrate how the ValidationObserver can be used to validate
complex tool usage patterns and agent behaviors in integration tests.
"""

import pytest
import os
import time
from typing import List, Dict, Any

from liteagent.agent import LiteAgent
from liteagent.tools import tool
from liteagent.observer import (
    AgentObserver, AgentInitializedEvent, UserMessageEvent, 
    ModelRequestEvent, ModelResponseEvent, 
    FunctionCallEvent, FunctionResultEvent, AgentResponseEvent
)

from tests.integration.test_observer import ValidationObserver

# Skip tests if API key is not set
skip_if_no_api_key = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OpenAI API key not found in environment variables"
)


# Custom tools for testing validation
@tool
def fetch_user_data(user_id: str) -> Dict[str, Any]:
    """
    Simulates fetching user data from a database.
    
    Args:
        user_id: The ID of the user to fetch
        
    Returns:
        Dictionary with user data
    """
    # Simulate different users for testing
    users = {
        "user1": {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "age": 32,
            "subscription": "premium"
        },
        "user2": {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "age": 45,
            "subscription": "basic"
        },
        "admin": {
            "name": "Admin User",
            "email": "admin@example.com",
            "age": 40,
            "subscription": "admin",
            "permissions": ["read", "write", "delete"]
        }
    }
    
    if user_id in users:
        return users[user_id]
    return {"error": f"User {user_id} not found"}


@tool
def update_user_data(user_id: str, field: str, value: Any) -> Dict[str, Any]:
    """
    Simulates updating user data in a database.
    
    Args:
        user_id: The ID of the user to update
        field: The field to update
        value: The new value
        
    Returns:
        Dictionary with status and updated user data
    """
    # For testing purposes, we'll just return success without actually updating
    return {
        "status": "success",
        "user_id": user_id,
        "updated_field": field,
        "new_value": value,
        "timestamp": time.time()
    }


@tool
def log_system_event(event_type: str, description: str, severity: str = "info") -> Dict[str, Any]:
    """
    Simulates logging a system event.
    
    Args:
        event_type: Type of event (e.g., 'user_login', 'data_update')
        description: Description of the event
        severity: Severity level ('info', 'warning', 'error', 'critical')
        
    Returns:
        Dictionary with event log details
    """
    return {
        "event_id": f"evt_{int(time.time())}",
        "event_type": event_type,
        "description": description,
        "severity": severity,
        "timestamp": time.time()
    }


class SequenceValidationObserver(ValidationObserver):
    """
    Enhanced validation observer that can validate sequences of function calls.
    """
    
    def assert_function_call_sequence(self, sequence: List[str]):
        """
        Assert that functions were called in the specified sequence.
        
        Args:
            sequence: List of function names in the expected order
        """
        # Extract just the function names in the order they were called
        actual_sequence = [call["name"] for call in self.function_calls]
        
        # Check if the expected sequence is a subsequence of the actual sequence
        if len(sequence) > len(actual_sequence):
            raise AssertionError(
                f"Expected sequence {sequence} is longer than actual sequence {actual_sequence}"
            )
            
        # Find the subsequence
        i, j = 0, 0
        while i < len(actual_sequence) and j < len(sequence):
            if actual_sequence[i] == sequence[j]:
                j += 1
            i += 1
            
        if j != len(sequence):
            raise AssertionError(
                f"Expected sequence {sequence} was not found in actual sequence {actual_sequence}"
            )


@pytest.fixture
def sequence_validation_observer():
    """Create a sequence validation observer for tests."""
    return SequenceValidationObserver()


@pytest.mark.integration
@pytest.mark.slow
@skip_if_no_api_key
class TestValidationPatterns:
    """Tests demonstrating validation patterns using the ValidationObserver."""
    
    MODEL_NAME = "gpt-4o-mini"
    
    def test_specific_tool_parameter_validation(self, validation_observer):
        """Test validating specific parameters passed to tools."""
        # Create agent with user data tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="UserDataAgent",
            system_prompt=(
                "You are a user management assistant. You can fetch and update user data "
                "and log system events. Be sure to log any updates you make."
            ),
            tools=[fetch_user_data, update_user_data, log_system_event],
            observers=[validation_observer]
        )
        
        # Test fetching user data for a specific user
        response = agent.chat("Get the data for user1")
        
        # Validate function calls
        validation_observer.assert_function_called("fetch_user_data")
        validation_observer.assert_function_called_with("fetch_user_data", user_id="user1")
        
        # Validate that the right data was returned in the response
        assert "Alice" in response
        assert "premium" in response.lower()
        
        validation_observer.reset()
        
        # Test updating user data with specific parameters
        response = agent.chat("Update user2's subscription to premium")
        
        # Validate function calls
        validation_observer.assert_function_called("fetch_user_data")
        validation_observer.assert_function_called("update_user_data")
        validation_observer.assert_function_called_with(
            "update_user_data", user_id="user2", field="subscription", value="premium"
        )
        
        # Check if the agent also logged the event (good practice)
        if "log_system_event" in validation_observer.called_functions:
            # If it logged the event, validate the parameters
            for call in validation_observer.function_calls:
                if call["name"] == "log_system_event":
                    assert "update" in call["arguments"]["event_type"].lower()
                    assert "user2" in call["arguments"]["description"].lower()
    
    def test_call_sequence_validation(self, sequence_validation_observer):
        """Test validating sequences of function calls."""
        # Create agent with user data tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="SequenceAgent",
            system_prompt=(
                "You are a user management assistant. Always follow this process: "
                "1. First fetch the user data to check current values "
                "2. Then update the user data if needed "
                "3. Finally log the system event"
            ),
            tools=[fetch_user_data, update_user_data, log_system_event],
            observers=[sequence_validation_observer]
        )
        
        # Test updating user data should follow the specified sequence
        response = agent.chat("Update user1's age to 33")
        
        # Validate the sequence of function calls
        sequence_validation_observer.assert_function_call_sequence([
            "fetch_user_data",
            "update_user_data",
            "log_system_event"
        ])
        
        # Also validate specific parameters
        sequence_validation_observer.assert_function_called_with(
            "update_user_data", user_id="user1", field="age", value=33
        )
    
    def test_conditional_validation(self, validation_observer):
        """Test conditional validation based on model responses."""
        # Create agent with user data tools
        agent = LiteAgent(
            model=self.MODEL_NAME,
            name="ConditionalAgent",
            system_prompt=(
                "You are a user management assistant. You should verify user permissions "
                "before performing admin operations. Only users with 'admin' subscription "
                "should be allowed to perform admin operations."
            ),
            tools=[fetch_user_data, update_user_data, log_system_event],
            observers=[validation_observer]
        )
        
        # Test with regular user trying to do admin operation
        response = agent.chat("As user1, I want to update user2's email")
        
        # Check that the agent fetched both users' data
        validation_observer.assert_function_called("fetch_user_data")
        
        # Check the response for permission denial
        assert any(word in response.lower() for word in ["cannot", "permission", "not allowed", "admin"])
        
        # Now test with admin user
        validation_observer.reset()
        response = agent.chat("As admin, I want to update user2's email to new_bob@example.com")
        
        # Check that appropriate functions were called
        validation_observer.assert_function_called("fetch_user_data")
        
        # We expect either:
        # 1. The model properly checks permissions and allows the update
        # 2. The model checks permissions but still doesn't allow it (being extra cautious)
        # Either way, we want to make sure it checked the admin's permissions
        
        # Check for admin user fetch
        admin_fetch = False
        for call in validation_observer.function_calls:
            if call["name"] == "fetch_user_data" and call["arguments"].get("user_id") == "admin":
                admin_fetch = True
                break
        
        assert admin_fetch, "The agent did not fetch the admin user's data to check permissions" 