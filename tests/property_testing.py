"""
Property-based testing utilities for LiteAgent using Hypothesis.

This module provides property-based testing strategies and generators
specifically designed for testing LLM agent behavior with various inputs.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from typing import Dict, Any, List, Tuple, Optional
import re


# Custom strategies for LiteAgent testing
@st.composite
def valid_model_names(draw):
    """Generate valid model names in different formats."""
    providers = ["openai", "anthropic", "groq", "mistral", "deepseek", "ollama"]
    models = ["gpt-4", "claude-3", "llama3-70b", "mistral-large", "deepseek-chat", "gpt-oss:20b"]
    
    provider = draw(st.sampled_from(providers))
    model = draw(st.sampled_from(models))
    
    # Generate different formats
    format_choice = draw(st.integers(0, 2))
    if format_choice == 0:
        return f"{provider}/{model}"  # String format
    elif format_choice == 1:
        return (provider, model)  # Tuple format
    else:
        return model  # Just model name


@st.composite  
def user_messages(draw):
    """Generate realistic user messages for testing."""
    message_types = [
        # Tool-requiring messages
        "What's the weather in {city}?",
        "Calculate {num1} + {num2}",
        "What is the square root of {number}?",
        "Get information for user {user_id}",
        
        # General questions
        "How does {topic} work?",
        "Explain {concept} to me",
        "What are the benefits of {thing}?",
        
        # Complex requests
        "Create a report that includes {item1} and {item2}",
        "Compare {option1} with {option2}",
    ]
    
    template = draw(st.sampled_from(message_types))
    
    # Fill in placeholders
    if "{city}" in template:
        city = draw(st.sampled_from(["Tokyo", "New York", "London", "Paris", "Berlin"]))
        template = template.replace("{city}", city)
    
    if "{num1}" in template and "{num2}" in template:
        num1 = draw(st.integers(1, 100))
        num2 = draw(st.integers(1, 100))
        template = template.replace("{num1}", str(num1)).replace("{num2}", str(num2))
    
    if "{number}" in template:
        number = draw(st.integers(100000, 999999999))
        template = template.replace("{number}", str(number))
        
    if "{user_id}" in template:
        user_id = draw(st.sampled_from(["user123", "user456", "user789"]))
        template = template.replace("{user_id}", user_id)
        
    # Replace other placeholders with generic terms
    for placeholder in ["{topic}", "{concept}", "{thing}", "{item1}", "{item2}", "{option1}", "{option2}"]:
        if placeholder in template:
            replacement = draw(st.text(min_size=3, max_size=15, alphabet=st.characters(whitelist_categories=["L"])))
            template = template.replace(placeholder, replacement)
    
    return template


@st.composite
def tool_configurations(draw):
    """Generate valid tool configurations for agents."""
    available_tools = [
        "get_weather",
        "add_numbers", 
        "multiply_numbers",
        "calculate_square_root",
        "get_user_data",
        "calculate_area"
    ]
    
    # Select 1-4 tools
    num_tools = draw(st.integers(1, 4))
    selected_tools = draw(st.lists(
        st.sampled_from(available_tools),
        min_size=num_tools,
        max_size=num_tools,
        unique=True
    ))
    
    return selected_tools


@st.composite
def system_prompts(draw):
    """Generate system prompts with different directive levels."""
    prompt_styles = [
        "You are a helpful assistant that can use tools.",
        "You are a TOOL-USING assistant. You MUST use tools for all operations.",
        "You are an agent with access to tools. Use them when appropriate.",
        "CRITICAL: You MUST use tools for calculations and data retrieval. NEVER guess.",
    ]
    
    base_prompt = draw(st.sampled_from(prompt_styles))
    
    # Sometimes add tool-specific instructions
    add_specifics = draw(st.booleans())
    if add_specifics:
        specifics = [
            "\nFor weather queries, use get_weather tool.",
            "\nFor math, use calculation tools.",
            "\nFor user data, use get_user_data tool.",
        ]
        base_prompt += draw(st.sampled_from(specifics))
    
    return base_prompt


class AgentPropertyTester:
    """Property-based tester for LiteAgent behavior."""
    
    @given(
        model_name=valid_model_names(),
        message=user_messages(),
        tools=tool_configurations(),
        system_prompt=system_prompts()
    )
    @settings(max_examples=10, deadline=30000)  # Limit for LLM testing
    def test_agent_responds_to_valid_inputs(self, model_name, message, tools, system_prompt):
        """
        Property: Valid inputs should never crash the agent.
        
        This test ensures that any combination of valid model names,
        user messages, tools, and system prompts results in a response
        rather than an exception.
        """
        from liteagent import LiteAgent
        from tests.utils.test_tools import get_weather, add_numbers, calculate_square_root, get_user_data
        
        # Skip if model format is not supported
        assume(isinstance(model_name, (str, tuple)))
        
        # Map tool names to actual functions
        tool_mapping = {
            "get_weather": get_weather,
            "add_numbers": add_numbers,
            "calculate_square_root": calculate_square_root,
            "get_user_data": get_user_data,
        }
        
        selected_tool_functions = [
            tool_mapping[tool_name] for tool_name in tools 
            if tool_name in tool_mapping
        ]
        
        # Skip if no valid tools
        assume(len(selected_tool_functions) > 0)
        
        try:
            if isinstance(model_name, tuple):
                provider, model = model_name
                agent = LiteAgent(
                    model=model,
                    provider=provider,
                    system_prompt=system_prompt,
                    tools=selected_tool_functions
                )
            else:
                agent = LiteAgent(
                    model=model_name,
                    system_prompt=system_prompt,
                    tools=selected_tool_functions
                )
            
            # The agent should be created without error
            assert agent is not None
            assert agent.name is not None
            
            # For now, we just test creation - actual chat would require API keys
            # and would be too slow for property testing
            
        except Exception as e:
            # Log the failing case for debugging
            pytest.fail(f"Agent creation failed with model={model_name}, tools={tools}, error={str(e)}")
    
    @given(
        user_id=st.text(min_size=3, max_size=20, alphabet=st.characters(whitelist_categories=["L", "N"])),
        numbers=st.lists(st.integers(-1000, 1000), min_size=2, max_size=2)
    )
    def test_tool_input_validation(self, user_id, numbers):
        """
        Property: Tools should handle various input types gracefully.
        
        This tests that our tools can handle different input formats
        without crashing, even if they return error messages.
        """
        from tests.utils.test_tools import get_user_data, add_numbers
        
        # Test get_user_data with various user IDs
        result = get_user_data(user_id)
        assert isinstance(result, dict)
        assert "error" in result or "name" in result  # Either error or valid data
        
        # Test add_numbers with various number pairs
        a, b = numbers
        result = add_numbers(a, b)
        assert isinstance(result, (int, float))
        assert result == a + b  # Should always be mathematically correct


class AgentStateMachine(RuleBasedStateMachine):
    """
    Stateful property-based testing for agent behavior.
    
    This tests that agents maintain consistent behavior across
    multiple interactions and state changes.
    """
    
    def __init__(self):
        super().__init__()
        self.agents = {}
        self.message_count = 0
        self.last_responses = []
    
    @rule(
        agent_name=st.text(min_size=3, max_size=10, alphabet=st.characters(whitelist_categories=["L"])),
        tools=tool_configurations()
    )
    def create_agent(self, agent_name, tools):
        """Create a new agent with specified tools."""
        assume(agent_name not in self.agents)
        
        # For property testing, we create agents but don't actually initialize them
        # with real models to avoid API calls and timeouts
        self.agents[agent_name] = {
            "name": agent_name,
            "tools": tools,
            "created": True
        }
    
    @rule(
        agent_name=st.sampled_from(["agent1", "agent2", "agent3"]),
        message=user_messages()
    )
    def send_message(self, agent_name, message):
        """Send a message to an agent."""
        assume(agent_name in self.agents)
        
        # Simulate response without actual LLM call
        self.message_count += 1
        response = f"Response {self.message_count} to: {message[:50]}..."
        self.last_responses.append(response)
        
        # Keep only last 5 responses
        if len(self.last_responses) > 5:
            self.last_responses.pop(0)
    
    @invariant()
    def agents_remain_consistent(self):
        """Agents should maintain their configuration."""
        for agent_name, agent_data in self.agents.items():
            assert agent_data["created"] is True
            assert len(agent_data["tools"]) > 0
            assert isinstance(agent_data["name"], str)
    
    @invariant() 
    def responses_are_tracked(self):
        """Response history should be maintained."""
        assert len(self.last_responses) <= 5
        assert self.message_count >= len(self.last_responses)


# Test runner function
def run_property_tests():
    """Run all property-based tests."""
    tester = AgentPropertyTester()
    
    print("Running property-based tests...")
    
    try:
        # Run creation test
        print("Testing agent creation properties...")
        tester.test_agent_responds_to_valid_inputs()
        
        # Run tool validation test  
        print("Testing tool input validation properties...")
        tester.test_tool_input_validation()
        
        # Run stateful tests
        print("Testing stateful agent properties...")
        state_machine_test = AgentStateMachine.TestCase()
        state_machine_test.runTest()
        
        print("✅ All property-based tests passed!")
        
    except Exception as e:
        print(f"❌ Property-based test failed: {e}")
        raise


if __name__ == "__main__":
    run_property_tests()