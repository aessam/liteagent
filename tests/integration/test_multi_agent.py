"""
Integration tests for multi-agent functionality.

These tests run different agents with specialized roles, similar to the
examples.py agent specialization examples but with enhanced testing.
"""

import pytest
import os
import time
from typing import List, Dict, Optional

from liteagent.agent import LiteAgent
from liteagent.tools import tool, liteagent_tool
from liteagent.examples import (
    get_weather, add_numbers, search_database, calculate_area
)

from tests.integration.test_observer import ValidationObserver


# Skip tests if API key is not set
skip_if_no_api_key = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OpenAI API key not found in environment variables"
)


# Custom tool for the specialized agents
@tool
def summarize_text(text: str, max_words: Optional[int] = None) -> str:
    """
    Simulates summarizing a text.
    
    Args:
        text: The text to summarize
        max_words: Maximum number of words in the summary (optional)
        
    Returns:
        A summary of the text
    """
    words = text.split()
    if max_words and len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return f"Summary of '{text[:30]}...' - {len(words)} words"


@pytest.mark.integration
@pytest.mark.slow
@skip_if_no_api_key
class TestMultiAgent:
    """Integration tests for LiteAgent with multiple specialized agents."""
    
    # Using gpt-4o-mini as it has good function calling but is more cost-effective
    MODEL_NAME = "gpt-4o-mini"
    
    def test_specialized_agents(self, validation_observer):
        """Test specialized agents with different tools and system prompts."""
        # Create a Math Agent
        math_agent = LiteAgent(
            model=self.MODEL_NAME,
            name="Math Agent",
            system_prompt="You are a Math Agent. You can only perform mathematical operations. If asked about anything else, politely explain that you can only help with math.",
            tools=[add_numbers, calculate_area],
            observers=[validation_observer]
        )
        
        # Create a Weather Agent
        weather_agent = LiteAgent(
            model=self.MODEL_NAME,
            name="Weather Agent",
            system_prompt="You are a Weather Agent. You can only provide weather information. If asked about anything else, politely explain that you can only help with weather.",
            tools=[get_weather],
            observers=[validation_observer]
        )
        
        # Create a Research Agent
        research_agent = LiteAgent(
            model=self.MODEL_NAME,
            name="Research Agent",
            system_prompt="You are a Research Agent. You can search for information and summarize text. If asked about math or weather, suggest using the appropriate specialized agent.",
            tools=[search_database, summarize_text],
            observers=[validation_observer]
        )
        
        # Test Math Agent with math question
        response = math_agent.chat("Calculate the area of a rectangle with width 7 and height 3.")
        validation_observer.assert_function_called("calculate_area")
        validation_observer.assert_function_called_with("calculate_area", width=7, height=3)
        assert "21" in response
        
        validation_observer.reset()
        
        # Test Math Agent with non-math question
        response = math_agent.chat("What's the weather in Tokyo?")
        validation_observer.assert_function_not_called("get_weather")
        validation_observer.assert_function_not_called("calculate_area")
        assert "math" in response.lower()  # Should mention only doing math
        
        validation_observer.reset()
        
        # Test Weather Agent with weather question
        response = weather_agent.chat("What's the weather in London?")
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_called_with("get_weather", city="London")
        assert "London" in response
        
        validation_observer.reset()
        
        # Test Weather Agent with non-weather question
        response = weather_agent.chat("What is 5 + 7?")
        validation_observer.assert_function_not_called("add_numbers")
        validation_observer.assert_function_not_called("get_weather")
        assert "weather" in response.lower()  # Should mention only doing weather
        
        validation_observer.reset()
        
        # Test Research Agent with research question
        response = research_agent.chat("Search for information about renewable energy and summarize the results.")
        assert validation_observer.called_functions.intersection({"search_database", "summarize_text"})
        assert "renewable energy" in str(validation_observer.function_calls).lower()
        
        validation_observer.reset()
    
    def test_agent_routing(self, validation_observer):
        """Test routing between multiple agents."""
        # Create new function specifically for agent routing
        @tool
        def route_to_agent(query: str) -> Dict[str, str]:
            """
            Routes a query to the appropriate agent based on content.
            
            Args:
                query: The user query to route
                
            Returns:
                Dict with 'agent' field specifying which agent should handle the query
            """
            if "weather" in query.lower():
                return {"agent": "weather", "explanation": "Query is about weather"}
            elif any(term in query.lower() for term in ["math", "calculate", "add", "multiply", "area"]):
                return {"agent": "math", "explanation": "Query is about mathematical calculations"}
            else:
                return {"agent": "research", "explanation": "Query requires research"}
        
        # Create the Router Agent with stronger system prompt
        router_agent = LiteAgent(
            model=self.MODEL_NAME,
            name="Router Agent",
            system_prompt=(
                "You are a Router Agent. Your job is to determine which specialized agent "
                "should handle a user query. ALWAYS USE the route_to_agent tool to determine this. "
                "NEVER respond without calling route_to_agent first. "
                "When routing math questions, always include the word 'math' in your response. "
                "For weather questions, include 'weather'. For research questions, include 'research'."
            ),
            tools=[route_to_agent],
            observers=[validation_observer]
        )
        
        # Test with weather query
        response = router_agent.chat("What's the weather like in Paris?")
        print(f"\nCalled functions for weather query: {validation_observer.called_functions}")
        print(f"Response: {response}")
        assert "route_to_agent" in validation_observer.called_functions
        assert "weather" in response.lower()
        
        validation_observer.reset()
        
        # Test with explicit math query to ensure routing to math agent
        response = router_agent.chat("This is a math question: calculate the area of a circle with radius 5")
        print(f"\nCalled functions for math query: {validation_observer.called_functions}")
        print(f"Response: {response}")
        assert "route_to_agent" in validation_observer.called_functions
        assert "math" in response.lower(), f"Response should contain 'math', but got: {response}"
        
        validation_observer.reset()
        
        # Test with research query
        response = router_agent.chat("Tell me about the history of artificial intelligence")
        print(f"\nCalled functions for research query: {validation_observer.called_functions}")
        print(f"Response: {response}")
        assert "route_to_agent" in validation_observer.called_functions
        assert "research" in response.lower() 