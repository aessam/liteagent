"""
Unit tests for the AgentTool functionality.

This module contains tests for using LiteAgent instances as tools
within other LiteAgent instances (agent-as-tool pattern).
"""

import json
import pytest
from unittest.mock import MagicMock, patch, call

# Import LiteAgent components
from liteagent.agent import LiteAgent
from liteagent.agent_tool import AgentTool
from liteagent.observer import AgentObserver

# Import our testing utilities
from tests.unit.test_mock_llm import MockModelInterface


class TestAgentTool:
    """Test the AgentTool class."""
    
    def test_agent_tool_creation(self, agent_with_mock_model):
        """Test that an AgentTool can be created from a LiteAgent."""
        # Create an AgentTool from the agent
        agent_tool = AgentTool(agent_with_mock_model)
        
        # Check the tool properties
        assert agent_tool.name == "test-agent"
        assert agent_tool.description == "You are a test agent."
        assert agent_tool.agent == agent_with_mock_model
    
    def test_agent_tool_with_custom_name_and_description(self, agent_with_mock_model):
        """Test that an AgentTool can be created with custom name and description."""
        # Create an AgentTool with custom name and description
        agent_tool = AgentTool(
            agent_with_mock_model,
            name="custom-tool-name",
            description="Custom tool description."
        )
        
        # Check the tool properties
        assert agent_tool.name == "custom-tool-name"
        assert agent_tool.description == "Custom tool description."
        assert agent_tool.agent == agent_with_mock_model
    
    def test_agent_tool_execution(self, agent_with_mock_model):
        """Test that an AgentTool can be executed."""
        # Configure the mock model to return a specific response
        agent_with_mock_model.model_interface.responses = [
            {"type": "text", "content": "I'm a sub-agent responding to your query."}
        ]
        
        # Create an AgentTool from the agent
        agent_tool = AgentTool(agent_with_mock_model)
        
        # Execute the tool with a message
        result = agent_tool.execute(message="Hello, sub-agent!", parent_context_id="test-context-id")
        
        # Check the result
        assert result == "I'm a sub-agent responding to your query."
        
        # Verify that the agent received the message
        messages = agent_with_mock_model.memory.get_messages()
        assert len(messages) >= 2  # System prompt + user message
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello, sub-agent!"
    
    def test_agent_tool_with_message_template(self, agent_with_mock_model):
        """Test that an AgentTool can be used with a message template."""
        # Configure the mock model to return a specific response
        agent_with_mock_model.model_interface.responses = [
            {"type": "text", "content": "I'm responding to a query about apples in New York."}
        ]
        
        # Create an AgentTool with a message template
        template = "Find information about {item} in {location}."
        agent_tool = AgentTool(
            agent_with_mock_model,
            message_template=template
        )
        
        # When using a message template, we need to pass the parameters as kwargs
        # and set message to an empty string instead of None to satisfy Pydantic validation
        result = agent_tool.execute(message="", kwargs={"item": "apples", "location": "New York"}, parent_context_id="test-context-id")
        
        # Check the result
        assert result == "I'm responding to a query about apples in New York."
        
        # Verify that the agent received the formatted message
        messages = agent_with_mock_model.memory.get_messages()
        assert len(messages) >= 2  # System prompt + user message
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Find information about apples in New York."
    
    def test_nested_agents(self, agent_with_mock_model, agent_with_tools):
        """Test that agents can be nested (agent using another agent as a tool)."""
        # Configure the sub-agent (agent_with_mock_model) to return a specific response
        agent_with_mock_model.model_interface.responses = [
            {"type": "text", "content": "I'm the sub-agent responding."}
        ]
        
        # Create an AgentTool from the sub-agent
        sub_agent_tool = AgentTool(agent_with_mock_model, name="sub_agent")
        
        # Configure the main agent to use the sub-agent tool
        main_agent = agent_with_tools
        
        # Manually add the sub-agent tool to the main agent's tools
        main_agent.tools["sub_agent"] = sub_agent_tool.to_function_definition()
        main_agent.tool_instances["sub_agent"] = sub_agent_tool
        
        # Configure the main agent to call the sub-agent
        main_agent.model_interface.responses = [
            {
                "type": "function_call",
                "function_name": "sub_agent",
                "function_args": {"message": "Hello from the main agent!", "parent_context_id": main_agent.context_id}
            },
            {"type": "text", "content": "The sub-agent responded successfully."}
        ]
        
        # Chat with the main agent
        response = main_agent.chat("Use the sub-agent")
        
        # Verify the response
        assert response == "The sub-agent responded successfully."
        
        # Verify that the sub-agent received the message
        sub_agent_messages = agent_with_mock_model.memory.get_messages()
        assert len(sub_agent_messages) >= 2  # System prompt + user message
        assert sub_agent_messages[1]["role"] == "user"
        assert sub_agent_messages[1]["content"] == "Hello from the main agent!"
    
    def test_parent_context_propagation(self, agent_with_mock_model):
        """Test that context IDs are properly propagated between agents."""
        # Configure the mock model to return a specific response
        agent_with_mock_model.model_interface.responses = [
            {"type": "text", "content": "Response with context propagation."}
        ]
        
        # Create an AgentTool from the agent
        agent_tool = AgentTool(agent_with_mock_model)
        
        # Store the original parent_context_id
        original_parent_context_id = agent_with_mock_model.parent_context_id
        
        # Execute the tool with a context_id
        test_context_id = "test-context-id"
        agent_tool.execute(message="Hello", parent_context_id=test_context_id, _context_id=test_context_id)
        
        # Check that parent_context_id was updated during execution
        # (We can't verify this directly but can check it was reset)
        assert agent_with_mock_model.parent_context_id == original_parent_context_id
    
    def test_agent_tool_observer_propagation(self, agent_with_mock_model, mock_observer):
        """Test that observers are properly propagated to the agent."""
        # Configure the mock model to return a specific response
        agent_with_mock_model.model_interface.responses = [
            {"type": "text", "content": "Response with observer."}
        ]
        
        # Create an AgentTool from the agent
        agent_tool = AgentTool(agent_with_mock_model)
        
        # Add an observer to the tool
        agent_tool.add_observer(mock_observer)
        
        # Verify that the observer was added to the agent
        assert mock_observer in agent_with_mock_model.observers
        
        # Execute the tool
        agent_tool.execute(message="Hello with observer", parent_context_id="test-context-id")
        
        # Verify that the observer methods were called
        assert mock_observer.on_user_message.called
        assert mock_observer.on_model_request.called
        assert mock_observer.on_model_response.called
        assert mock_observer.on_agent_response.called
        
        # Remove the observer
        agent_tool.remove_observer(mock_observer)
        
        # Verify that the observer was removed from the agent
        assert mock_observer not in agent_with_mock_model.observers


if __name__ == "__main__":
    pytest.main(["-v", "test_agent_tool.py"]) 