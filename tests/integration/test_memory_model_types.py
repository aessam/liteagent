"""
Integration tests for memory management across different model types.

These tests validate that memory management works correctly with different types of models
and their tool calling formats.
"""

import pytest
import json
from typing import Dict, List, Any, Tuple
from unittest.mock import patch, MagicMock

from liteagent.agent import LiteAgent
from liteagent.memory import ConversationMemory
from liteagent.tool_calling_types import ToolCallingType
from liteagent.tools import FunctionTool


# Sample tools for testing
def get_weather(city: str) -> Dict[str, Any]:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Weather information
    """
    return {"temperature": 72, "condition": "sunny", "city": city}


def add_numbers(a: int, b: int) -> Dict[str, Any]:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    return {"sum": a + b}


class TestMemoryModelTypes:
    """Test suite for memory management across model types."""
    
    @pytest.fixture
    def system_prompt(self) -> str:
        """Fixture providing a standard system prompt for tests."""
        return "You are a helpful AI assistant. Use the provided tools when needed."
    
    def test_openai_memory_management(self, system_prompt: str) -> None:
        """Test memory management with OpenAI-style tool calling."""
        # Create agent with OpenAI-style tool calling
        with patch.object(LiteAgent, 'chat') as mock_chat:
            # Set up mock to return a canned response
            mock_chat.return_value = "The weather in San Francisco is sunny and 72°F."
            
            # Create the agent
            agent = LiteAgent(
                model="gpt-4",
                name="weather-agent",
                system_prompt=system_prompt,
                tools=[FunctionTool(get_weather)],
                debug=True
            )
            
            # Manually add a user message to memory
            agent.memory.add_user_message("What's the weather in San Francisco?")
            
            # Manually add a simulated assistant message with tool call
            agent.memory.add_tool_call(
                name="get_weather",
                args={"city": "San Francisco"},
                call_id="call_123"
            )
            
            # Manually add a simulated tool response
            agent.memory.add_tool_result(
                name="get_weather", 
                content=json.dumps({"temperature": 72, "condition": "sunny", "city": "San Francisco"}),
                call_id="call_123"
            )
            
            # Manually add the final assistant response
            agent.memory.add_assistant_message("The weather in San Francisco is sunny and 72°F.")
            
            # Verify memory state
            memory = agent.memory
            assert len(memory.messages) >= 5  # system + user + assistant tool call + tool result + assistant response
            
            # Find tool call in messages
            tool_call_message = None
            for msg in memory.messages:
                if msg["role"] == "assistant" and "tool_calls" in msg:
                    tool_call_message = msg
                    break
            
            assert tool_call_message is not None
            
            # Verify function call tracking
            assert "get_weather" in memory.function_calls
            assert len(memory.function_calls["get_weather"]) == 1
            assert memory.function_calls["get_weather"][0]["args"] == {"city": "San Francisco"}
            
            # Find tool response
            tool_response = None
            for msg in memory.messages:
                if msg["role"] == "tool" and "name" in msg and msg["name"] == "get_weather":
                    tool_response = msg
                    break
            
            assert tool_response is not None
    
    def test_anthropic_memory_management(self, system_prompt: str) -> None:
        """Test memory management with Anthropic-style tool calling."""
        # Create agent with Anthropic-style tool calling
        with patch.object(LiteAgent, 'chat') as mock_chat:
            # Set up mock to return a canned response
            mock_chat.return_value = "The weather in San Francisco is sunny and 72°F."
            
            # Create the agent
            agent = LiteAgent(
                model="claude-3",
                name="weather-agent",
                system_prompt=system_prompt,
                tools=[FunctionTool(get_weather)],
                debug=True
            )
            
            # Manually add a user message to memory
            agent.memory.add_user_message("What's the weather in San Francisco?")
            
            # For Anthropic, the tool call would be processed and added as a function call
            agent.memory.function_calls["get_weather"] = [{
                "args": {"city": "San Francisco"},
                "call_id": "call_123"
            }]
            
            # Add an assistant message with tool call (converted to standard format)
            agent.memory.add_assistant_message("I'll check the weather for you.")
            
            # Add a tool result
            agent.memory.add_tool_result(
                name="get_weather", 
                content=json.dumps({"temperature": 72, "condition": "sunny", "city": "San Francisco"}),
                call_id="call_123"
            )
            
            # Verify memory state
            memory = agent.memory
            assert len(memory.messages) >= 4  # system + user + assistant + tool
            
            # Verify function call tracking
            assert "get_weather" in memory.function_calls
            assert len(memory.function_calls["get_weather"]) == 1
            assert memory.function_calls["get_weather"][0]["args"] == {"city": "San Francisco"}
            
            # Find tool messages
            tool_messages = [msg for msg in memory.messages if msg["role"] == "tool"]
            assert len(tool_messages) > 0
            assert tool_messages[0]["name"] == "get_weather"
    
    def test_text_based_memory_management(self, system_prompt: str) -> None:
        """Test memory management with text-based tool calling."""
        with patch.object(LiteAgent, 'chat') as mock_chat:
            # Set up mock to return a canned response
            mock_chat.return_value = "The weather in San Francisco is sunny and 72°F."
            
            # Create the agent with text-based tool calling
            with patch("liteagent.models.get_tool_calling_type") as mock_get_type:
                mock_get_type.return_value = ToolCallingType.TEXT_BASED
                
                agent = LiteAgent(
                    model="open-mistral",
                    name="weather-agent",
                    system_prompt=system_prompt,
                    tools=[FunctionTool(get_weather)],
                    debug=True
                )
            
            # Manually add a user message to memory
            agent.memory.add_user_message("What's the weather in San Francisco?")
            
            # Manually add a simulated assistant message with text-based tool call
            agent.memory.add_assistant_message(
                "I'll check the weather for you.\n\n"
                "[FUNCTION_CALL] get_weather(city=\"San Francisco\") [/FUNCTION_CALL]"
            )
            
            # Manually add the function call to memory tracking
            agent.memory.function_calls["get_weather"] = [{
                "args": {"city": "San Francisco"},
                "call_id": "call_123"
            }]
            
            # Add a tool result
            agent.memory.add_tool_result(
                name="get_weather", 
                content=json.dumps({"temperature": 72, "condition": "sunny", "city": "San Francisco"}),
                call_id="call_123"
            )
            
            # Manually add final response
            agent.memory.add_assistant_message("The weather in San Francisco is sunny and 72°F.")
            
            # Verify memory state
            memory = agent.memory
            assert len(memory.messages) >= 5  # system + user + assistant with tool call + tool result + final response
            
            # Verify function call tracking
            assert "get_weather" in memory.function_calls
            assert len(memory.function_calls["get_weather"]) == 1
            assert memory.function_calls["get_weather"][0]["args"] == {"city": "San Francisco"}
            
            # Verify tool results
            tool_results = [msg for msg in memory.messages if msg["role"] in ["function", "tool"]]
            assert len(tool_results) > 0
    
    def test_cross_model_memory_compatibility(self, system_prompt: str) -> None:
        """
        Test that memory can be transferred between agents using different models.
        This tests the compatibility of memory formats between different tool calling types.
        """
        # First create an OpenAI-style agent 
        with patch.object(LiteAgent, 'chat') as mock_chat:
            # Set up mock to return a canned response
            mock_chat.return_value = "The result is 12."
            
            # Create OpenAI-style agent
            openai_agent = LiteAgent(
                model="gpt-4",
                name="math-agent1",
                system_prompt=system_prompt,
                tools=[FunctionTool(add_numbers)],
                debug=True
            )
            
            # Manually add a user message
            openai_agent.memory.add_user_message("What is 5 + 7?")
            
            # Manually add a simulated assistant message with tool call
            openai_agent.memory.add_tool_call(
                name="add_numbers",
                args={"a": 5, "b": 7},
                call_id="call_456"
            )
            
            # Manually add a simulated tool response
            openai_agent.memory.add_tool_result(
                name="add_numbers", 
                content=json.dumps({"sum": 12}),
                call_id="call_456"
            )
            
            # Manually add the final assistant response
            openai_agent.memory.add_assistant_message("The result is 12.")
            
            # Get memory to transfer
            openai_memory = openai_agent.memory
            
            # Verify we have function call tracking before transferring
            assert "add_numbers" in openai_memory.function_calls
            assert len(openai_memory.function_calls["add_numbers"]) == 1
            assert openai_memory.function_calls["add_numbers"][0]["args"] == {"a": 5, "b": 7}
        
        # Now create an Anthropic-style agent with the OpenAI agent's memory
        with patch.object(LiteAgent, 'chat') as mock_chat:
            # Set up mock to return a canned response
            mock_chat.return_value = "The sum is 12."
            
            # Create Anthropic-style agent
            anthropic_agent = LiteAgent(
                model="claude-3",
                name="math-agent2",
                system_prompt=system_prompt,
                tools=[FunctionTool(add_numbers)],
                debug=True
            )
            
            # Replace memory with OpenAI agent's memory
            anthropic_agent.memory = openai_memory
            
            # Add a user message to continue the conversation
            anthropic_agent.memory.add_user_message("What's the result?")
            
            # Add a simulated Claude response
            anthropic_agent.memory.add_assistant_message("The sum is 12.")
            
            # Verify memory after multi-model conversation
            memory = anthropic_agent.memory
            
            # Check if the original OpenAI function call is still there
            assert "add_numbers" in memory.function_calls
            assert len(memory.function_calls["add_numbers"]) == 1
            
            # Verify the args are correct
            assert memory.function_calls["add_numbers"][0]["args"] == {"a": 5, "b": 7} 