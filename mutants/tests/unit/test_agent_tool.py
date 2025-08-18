"""
Unit tests for the AgentTool functionality using REAL API calls.

This module contains tests for using LiteAgent instances as tools
within other LiteAgent instances (agent-as-tool pattern).
NO MOCKS - uses actual API keys and real provider calls.
"""

import pytest
from liteagent.agent import LiteAgent
from liteagent.agent_tool import AgentTool
from liteagent.observer import AgentObserver


class TestAgentTool:
    """Test the AgentTool class using real API calls."""
    
    def test_agent_tool_creation(self, openai_agent):
        """Test that an AgentTool can be created from a real LiteAgent."""
        # Create an AgentTool from the real agent
        agent_tool = AgentTool(openai_agent)
        
        # Check the tool properties
        assert agent_tool.name == "test-openai-agent"
        assert agent_tool.description == "You are a helpful test assistant. Use tools when needed."
        assert agent_tool.agent == openai_agent
    
    def test_agent_tool_with_custom_name_and_description(self, anthropic_agent):
        """Test that an AgentTool can be created with custom name and description."""
        # Create an AgentTool with custom name and description
        agent_tool = AgentTool(
            anthropic_agent,
            name="custom-tool-name",
            description="Custom tool description."
        )
        
        # Check the tool properties
        assert agent_tool.name == "custom-tool-name"
        assert agent_tool.description == "Custom tool description."
        assert agent_tool.agent == anthropic_agent
    
    def test_agent_tool_execution(self, api_keys):
        """Test that an AgentTool can be executed with real API calls."""
        if not api_keys['openai']:
            pytest.skip("OPENAI_API_KEY not available")
            
        # Create a specialized sub-agent
        sub_agent = LiteAgent(
            model="gpt-4o-mini",
            name="math-helper",
            api_key=api_keys['openai'],
            system_prompt="You are a math helper. Answer math questions briefly and clearly."
        )
        
        # Create an AgentTool from the sub-agent
        agent_tool = AgentTool(sub_agent)
        
        # Execute the tool with a message
        result = agent_tool.execute(message="What is 5 + 3?", parent_context_id="test-context-id")
        
        # Check that we get a reasonable response
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain the answer 8 or "eight"
        assert "8" in result or "eight" in result.lower()
        
        # Verify that the agent received the message
        messages = sub_agent.memory.get_messages()
        assert len(messages) >= 2  # System prompt + user message
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What is 5 + 3?"
    
    def test_agent_tool_with_message_template(self, api_keys):
        """Test that an AgentTool can be used with a message template."""
        if not api_keys['anthropic']:
            pytest.skip("ANTHROPIC_API_KEY not available")
            
        # Create a specialized sub-agent for weather queries
        weather_agent = LiteAgent(
            model="claude-3-5-haiku-20241022",
            name="weather-helper",
            api_key=api_keys['anthropic'],
            system_prompt="You are a weather assistant. Provide brief weather information."
        )
        
        # Create an AgentTool with a message template
        template = "What's the weather like for {item} in {location}?"
        agent_tool = AgentTool(
            weather_agent,
            message_template=template
        )
        
        # Execute with template parameters
        result = agent_tool.execute(
            message="", 
            kwargs={"item": "outdoor activities", "location": "San Francisco"}, 
            parent_context_id="test-context-id"
        )
        
        # Check that we get a reasonable response
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Verify that the agent received the formatted message
        messages = weather_agent.memory.get_messages()
        assert len(messages) >= 2  # System prompt + user message
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What's the weather like for outdoor activities in San Francisco?"
    
    def test_nested_agents(self, api_keys, test_tool):
        """Test that agents can be nested (agent using another agent as a tool)."""
        if not api_keys['openai']:
            pytest.skip("OPENAI_API_KEY not available")
            
        # Create a specialized sub-agent for calculations
        calc_agent = LiteAgent(
            model="gpt-4o-mini",
            name="calculator",
            api_key=api_keys['openai'],
            system_prompt="You are a calculator. Provide only the numerical answer to math problems."
        )
        
        # Create an AgentTool from the sub-agent
        calc_tool = AgentTool(calc_agent, name="calculator_agent")
        
        # Create a main agent that can use the calculator agent
        main_agent = LiteAgent(
            model="gpt-4o-mini",
            name="main-agent",
            api_key=api_keys['openai'],
            tools=[test_tool, calc_tool],
            system_prompt="You are a helpful assistant. Use the calculator_agent tool for math problems."
        )
        
        # Chat with the main agent asking it to use the sub-agent
        response = main_agent.chat("Use the calculator_agent to find what 15 * 7 equals")
        
        # Verify we get a response
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Check that the sub-agent was used (should contain 105 or reference to calculation)
        # Note: This is a real API test so we can't guarantee exact behavior, 
        # but we can check that something reasonable happened
        assert len(calc_agent.memory.get_messages()) > 1  # Sub-agent should have been called
    
    def test_parent_context_propagation(self, api_keys):
        """Test that context IDs are properly handled between agents."""
        if not api_keys['openai']:
            pytest.skip("OPENAI_API_KEY not available")
            
        # Create a sub-agent
        sub_agent = LiteAgent(
            model="gpt-4o-mini",
            name="sub-agent",
            api_key=api_keys['openai'],
            system_prompt="You are a helpful sub-agent."
        )
        
        # Create an AgentTool from the agent
        agent_tool = AgentTool(sub_agent)
        
        # Store the original context state
        original_context = sub_agent.context_id
        
        # Execute the tool with a context_id
        test_context_id = "test-context-id"
        result = agent_tool.execute(
            message="Hello", 
            parent_context_id=test_context_id, 
            _context_id=test_context_id
        )
        
        # Check that we got a result
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Context should still be valid
        assert sub_agent.context_id is not None


if __name__ == "__main__":
    pytest.main(["-v", "test_agent_tool.py"])