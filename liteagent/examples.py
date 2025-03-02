"""
Example usage of LiteAgent.
"""

from .tools import tool, register_tool, FunctionTool, InstanceMethodTool
from .agent import LiteAgent
from .utils import check_api_keys

# Example standalone tools
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

# Example class with methods that can be used as tools
class ToolsForAgents:
    """
    Example class with methods that can be used as tools.
    This demonstrates how to use class methods as tools.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.counter = 0
        
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        self.counter += 1
        return a + b
        
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        self.counter += 1
        return a * b
        
    def get_weather(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        self.counter += 1
        if self.api_key:
            # In a real implementation, this would use the API key
            return f"Weather in {city} retrieved with API key {self.api_key[:5]}..."
        else:
            return f"The weather in {city} is 22°C and sunny."
            
    def get_call_count(self) -> int:
        """Returns the number of times the tools have been called."""
        return self.counter

def run_custom_agents_example(model):
    """
    Example demonstrating how to create multiple agents with different tools and system prompts.
    """
    # Check for API keys
    check_api_keys()
    
    print("\n=== Example: Multiple Custom Agents ===")
    
    # Create an instance of the tools class
    tools_instance = ToolsForAgents()
    
    # Create tool instances for the class methods
    add_numbers_tool = InstanceMethodTool(tools_instance.add_numbers, tools_instance)
    get_weather_tool = InstanceMethodTool(tools_instance.get_weather, tools_instance)
    
    # Create a math-only agent
    math_agent = LiteAgent(
        model=model,
        name="MathAgent",
        system_prompt="You are a math specialist. You can only perform mathematical calculations.",
        tools=[add_numbers_tool],  # Pass the tool object, not just the function
        debug=False
    )
    
    # Create a weather-only agent
    weather_agent = LiteAgent(
        model=model,
        name="WeatherAgent",
        system_prompt="You are a weather specialist. You can only provide weather information.",
        tools=[get_weather_tool],  # Pass the tool object, not just the function
        debug=False
    )
    
    # Create a search-only agent
    search_agent = LiteAgent(
        model=model,
        name="SearchAgent",
        system_prompt="You are a search specialist. You can search for information in a database.",
        tools=[search_database],  # This is a regular function, so it works as is
        debug=False
    )
    
    # Test each agent with appropriate queries
    print("\n--- Math Agent Test ---")
    response = math_agent.chat("What is 42 + 17?")
    print("Math Agent Response:", response)
    
    print("\n--- Weather Agent Test ---")
    response = weather_agent.chat("What's the weather in Tokyo?")
    print("Weather Agent Response:", response)
    
    print("\n--- Search Agent Test ---")
    response = search_agent.chat("Find information about renewable energy")
    print("Search Agent Response:", response)
    
    # Test with inappropriate queries (agent should not have access to other tools)
    print("\n--- Math Agent with Weather Query ---")
    response = math_agent.chat("What's the weather in London?")
    print("Math Agent Response:", response)
    
    print("\n--- Weather Agent with Math Query ---")
    response = weather_agent.chat("What is 15 + 27?")
    print("Weather Agent Response:", response)

def run_class_methods_example(model):
    """
    Example demonstrating how to use class methods as tools.
    This shows how to maintain state between tool calls.
    """
    # Check for API keys
    check_api_keys()
    
    print("\n=== Example: Class Methods as Tools ===")
    
    # Create an instance of the tools class
    tools_instance = ToolsForAgents(api_key="fake-api-key-12345")
    
    # Create tool instances for the class methods
    add_numbers_tool = InstanceMethodTool(tools_instance.add_numbers, tools_instance)
    multiply_numbers_tool = InstanceMethodTool(tools_instance.multiply_numbers, tools_instance)
    get_weather_tool = InstanceMethodTool(tools_instance.get_weather, tools_instance)
    get_call_count_tool = InstanceMethodTool(tools_instance.get_call_count, tools_instance)
    
    # Create an agent with all the tools
    class_methods_agent = LiteAgent(
        model=model,
        name="ClassMethodsAgent",
        system_prompt="You are a helpful assistant that can perform math operations and get weather information.",
        tools=[add_numbers_tool, multiply_numbers_tool, get_weather_tool, get_call_count_tool],
        debug=True
    )
    
    # Print the available tools
    print("Available tools:", [name for name in class_methods_agent.tools.keys()])
    
    # Test with a query that uses multiple tools
    print("\n--- Class Methods Agent Test ---")
    response = class_methods_agent.chat("What's the weather in Berlin? Also, can you add 23 and 45? Finally, can you multiply 7 and 9?")
    print("Class Methods Agent Response:", response)
    
    # Show that the instance state is maintained
    print(f"Tool call count: {tools_instance.get_call_count()}")

def run_examples(model):
    """
    Run example scenarios with LiteAgent.
    """
    # Check for API keys
    check_api_keys()
    
    print("\nStarting LiteAgent...")
    
    # Create tool instances for the standalone functions
    add_numbers_tool = FunctionTool(add_numbers)
    get_weather_tool = FunctionTool(get_weather)
    search_database_tool = FunctionTool(search_database)
    
    # Create agent instance with drop_params=True to handle different model capabilities
    agent = LiteAgent(
        model=model, 
        name="LiteAgent", 
        debug=False, 
        drop_params=True,
        tools=[add_numbers_tool, get_weather_tool, search_database_tool]
    )
    
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
    
    # Run the custom agents example
    run_custom_agents_example(model)
    
    # Run the class methods example
    run_class_methods_example(model)