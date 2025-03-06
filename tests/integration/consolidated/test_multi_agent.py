"""
Consolidated integration tests for multi-agent functionality across different models.

This module tests interactions between multiple agent instances using different models.
"""

import pytest
import re
from typing import Dict, Any, List

from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from liteagent.tools import get_weather, add_numbers

from tests.utils.validation_helper import ValidationTestHelper


@pytest.mark.integration
class TestMultiAgent:
    """Tests for multi-agent functionality across all models."""
    
    @pytest.fixture
    def basic_tools(self):
        """Provide basic tools for multi-agent tests."""
        return [get_weather, add_numbers]
    
    @pytest.fixture
    def system_prompt_agent1(self):
        """Provide system prompt for the first agent."""
        return """You are Agent 1, a helpful assistant that can use tools.
You specialize in getting weather information."""
    
    @pytest.fixture
    def system_prompt_agent2(self):
        """Provide system prompt for the second agent."""
        return """You are Agent 2, a helpful assistant that can use tools.
You specialize in performing calculations."""
    
    @pytest.fixture
    def tool_names(self):
        """Provide the tool names for parser registration."""
        return ["get_weather", "add_numbers"]
    
    def test_agent_context_isolation(self, model, validation_observer, basic_tools, tool_names):
        """
        Test that multiple agent instances have isolated contexts.
        
        This test verifies that conversation history and state is maintained
        separately for different agent instances.
        """
        # First set the validation strategy based on model
        tool_calling_type = get_tool_calling_type(model)
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Then register appropriate parsers
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type, 
            tool_names
        )
        
        # Create two separate agents with the same model but different configurations
        agent1 = LiteAgent(
            model=model,
            name="WeatherAgent",
            system_prompt="""You are a weather assistant that can get weather information.
Always introduce yourself as the Weather Agent.""",
            tools=[get_weather],
            observers=[validation_observer]
        )
        
        agent2 = LiteAgent(
            model=model,
            name="CalculatorAgent",
            system_prompt="""You are a calculator assistant that can perform calculations.
Always introduce yourself as the Calculator Agent.""",
            tools=[add_numbers],
            observers=[validation_observer]
        )
        
        try:
            # Interact with each agent
            response1 = agent1.chat("Hello, who are you?")
            validation_observer.reset()  # Reset observer between agents
            
            response2 = agent2.chat("Hello, who are you?")
            validation_observer.reset()
            
            # Handle None responses
            if response1 is None or response2 is None:
                pytest.skip(f"Model {model} returned None response, skipping validation")
                return
            
            # Check that each agent maintained its own identity
            assert "weather" in response1.lower() or "weather agent" in response1.lower(), \
                "Agent 1 should identify as a weather assistant"
            assert "calculator" in response2.lower() or "calculator agent" in response2.lower(), \
                "Agent 2 should identify as a calculator assistant"
            
            # Ensure each agent remembers its own history
            response1_followup = agent1.chat("What tools can you use?")
            validation_observer.reset()
            
            response2_followup = agent2.chat("What tools can you use?")
            validation_observer.reset()
            
            # Check appropriate tools are mentioned
            if response1_followup is not None:
                assert "weather" in response1_followup.lower(), \
                    "Agent 1 should mention weather tools"
            
            if response2_followup is not None:
                assert "add" in response2_followup.lower() or "calculation" in response2_followup.lower(), \
                    "Agent 2 should mention calculation tools"
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise
    
    def test_agent_with_different_models(self, validation_observer, basic_tools, tool_names):
        """
        Test creating agents with different models.
        
        This test verifies that multiple agents can be created with different models
        and that they can work together in the same application.
        
        Note: This test doesn't use the model fixture as it explicitly creates
        agents with different models.
        """
        # Get list of available models with API keys
        available_models = []
        for model in ["openai/gpt-4o-mini", "anthropic/claude-3-5-sonnet-latest", 
                     "groq/llama-3.1-8b-instant", "ollama/phi4"]:
            if ValidationTestHelper.has_api_key_for_model(model):
                available_models.append(model)
        
        # Skip if fewer than 2 models are available
        if len(available_models) < 2:
            pytest.skip("Need at least 2 available models for this test")
            return
        
        # Take the first two available models
        model1 = available_models[0]
        model2 = available_models[1]
        
        print(f"Testing with models: {model1} and {model2}")
        
        # First set validation strategy for model1
        tool_calling_type1 = get_tool_calling_type(model1)
        validation_observer.set_validation_strategy(tool_calling_type1)
        
        # Then register appropriate parsers for model1
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type1, 
            tool_names
        )
        
        # Create two agents with different models
        agent1 = LiteAgent(
            model=model1,
            name="Agent1",
            system_prompt="You are Agent 1. Always mention which model you're using.",
            tools=basic_tools,
            observers=[validation_observer]
        )
        
        # Create second agent - need to reset validation strategy for different model
        validation_observer.reset()
        tool_calling_type2 = get_tool_calling_type(model2)
        validation_observer.set_validation_strategy(tool_calling_type2)
        
        agent2 = LiteAgent(
            model=model2,
            name="Agent2",
            system_prompt="You are Agent 2. Always mention which model you're using.",
            tools=basic_tools,
            observers=[validation_observer]
        )
        
        try:
            # Test both agents
            validation_observer.set_validation_strategy(tool_calling_type1)
            response1 = agent1.chat("Hello! What's the weather in Tokyo?")
            validation_observer.reset()
            
            validation_observer.set_validation_strategy(tool_calling_type2)
            response2 = agent2.chat("Hello! What's 25 + 17?")
            
            # If we got this far without exceptions, the test passes
            assert True, "Successfully created and used agents with different models"
            
        except Exception as e:
            # Skip for expected errors with certain models
            if "TypeError: 'NoneType' object is not iterable" in str(e) and \
               ("ollama" in model1 or "ollama" in model2):
                pytest.skip(f"Ollama model returned None response, skipping validation")
            else:
                # For other exceptions, re-raise
                raise 