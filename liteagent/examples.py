"""
Example usage of LiteAgent.
"""

from .tools import tool
from .agent import LiteAgent
from .utils import check_api_keys

# Example tools
@tool
def get_weather(city: str) -> str:
    """Returns weather information for a city."""
    return f"The weather in {city} is 22°C and sunny."

@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@tool
def search_database(query: str, limit: int = 5) -> list:
    """
    Simulates searching a database for information.
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        
    Returns:
        List of search results
    """
    # Simulate database search
    results = [
        {"id": 1, "title": f"Result for {query} #1", "score": 0.95},
        {"id": 2, "title": f"Another match for {query}", "score": 0.87},
        {"id": 3, "title": f"Information about {query}", "score": 0.82},
        {"id": 4, "title": f"More data on {query}", "score": 0.76},
        {"id": 5, "title": f"Additional info for {query}", "score": 0.70},
        {"id": 6, "title": f"Supplementary data on {query}", "score": 0.65},
    ]
    return results[:limit]

def run_examples(model):
    """
    Run example scenarios with LiteAgent.
    """
    # Check for API keys
    check_api_keys()
    
    print("\nStarting LiteAgent...")
    
    # Create agent instance with drop_params=True to handle different model capabilities
    agent = LiteAgent(model=model, name="LiteAgent", debug=False, drop_params=True)
    
    # Example 1: Weather query
    print("\n=== Example 1: Weather Query ===")
    response = agent.chat("What's the weather in New York?")
    print("Final Response:", response)
    
    # Example 2: Math calculation
    print("\n=== Example 2: Math Calculation ===")
    agent.reset_memory()  # Reset for a new conversation
    response = agent.chat("What is 3 + 7?")
    print("Final Response:", response)
    
    # Example 3: Database search
    print("\n=== Example 3: Database Search ===")
    agent.reset_memory()
    response = agent.chat("Can you search for information about climate change?")
    print("Final Response:", response)
    
    # Example 4: Multi-tool interaction
    print("\n=== Example 4: Multi-tool Interaction ===")
    agent.reset_memory()
    response = agent.chat("What's the weather in Paris and what is 15 + 27?")
    print("Final Response:", response)