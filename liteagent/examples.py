"""
Example usage of LiteAgent.
"""

from .tools import liteagent_tool, FunctionTool, InstanceMethodTool
from .agent import LiteAgent
from .utils import check_api_keys

# Example standalone tools
@liteagent_tool
def get_weather(city: str) -> str:
    """Returns weather information for a city."""
    return f"The weather in {city} is 22°C and sunny."

@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@liteagent_tool
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

# Example class using the new liteagent_tool decorator
class SimplifiedToolsForAgents:
    """
    Example class with methods that use the liteagent_tool decorator.
    This demonstrates how to use the simplified tool registration.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.counter = 0
        
    @liteagent_tool
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        self.counter += 1
        return a + b
        
    @liteagent_tool
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        self.counter += 1
        return a * b
        
    @liteagent_tool
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

# Example standalone function using the new liteagent_tool decorator
@liteagent_tool
def calculate_area(width: float, height: float) -> float:
    """Calculates the area of a rectangle."""
    return width * height

def run_custom_agents_example(model, observers=None):
    """
    Run examples with custom agents.
    
    Args:
        model (str): The model to use
        observers (list, optional): List of observers to attach to the agents
    """
    # Check for API keys
    check_api_keys()
    
    # Create a Math Agent
    math_agent = LiteAgent(
        model=model,
        name="Math Agent",
        system_prompt="You are a Math Agent. You can only perform mathematical operations. If asked about anything else, politely explain that you can only help with math.",
        tools=[add_numbers],
        observers=observers
    )
    
    # Create a Weather Agent
    weather_agent = LiteAgent(
        model=model,
        name="Weather Agent",
        system_prompt="You are a Weather Agent. You can only provide weather information. If asked about anything else, politely explain that you can only help with weather.",
        tools=[get_weather],
        observers=observers
    )
    
    # Create a Search Agent
    search_agent = LiteAgent(
        model=model,
        name="Search Agent",
        system_prompt="You are a Search Agent. You can search for information in a database.",
        tools=[search_database],
        observers=observers
    )
    
    # Test the Math Agent
    print("\n=== Math Agent ===")
    response = math_agent.chat("What is 42 + 17?")
    print(f"Response: {response}")
    
    # Test the Weather Agent
    print("\n=== Weather Agent ===")
    response = weather_agent.chat("What's the weather in Tokyo?")
    print(f"Response: {response}")
    
    # Test the Search Agent
    print("\n=== Search Agent ===")
    response = search_agent.chat("Find information about renewable energy")
    print(f"Response: {response}")
    
    # Test that agents only respond to their domain
    print("\n=== Math Agent (asked about weather) ===")
    response = math_agent.chat("What's the weather in Berlin?")
    print(f"Response: {response}")
    
    print("\n=== Weather Agent (asked about math) ===")
    response = weather_agent.chat("What is 15 + 27?")
    print(f"Response: {response}")

def run_class_methods_example(model, observers=None):
    """
    Run examples with class methods as tools.
    
    Args:
        model (str): The model to use
        observers (list, optional): List of observers to attach to the agents
    """
    # Check for API keys
    check_api_keys()
    
    # Create an instance of the tools class
    tools_instance = ToolsForAgents(api_key="fake-api-key")
    
    # Create an agent with class methods as tools
    agent = LiteAgent(
        model=model,
        name="Class Methods Agent",
        system_prompt="You are a helpful assistant that can perform mathematical operations and get weather information.",
        tools=[
            tools_instance.add_numbers,
            tools_instance.multiply_numbers,
            calculate_area,
            tools_instance.get_weather
        ],
        observers=observers
    )
    
    # Test the agent with class methods
    print("\n=== Class Methods Agent ===")
    response = agent.chat("Can you tell me the latest weather in Berlin?")
    print(f"Response: {response}")
    
    response = agent.chat("What is 23 + 45?")
    print(f"Response: {response}")
    
    response = agent.chat("What is 7 * 9?")
    print(f"Response: {response}")
    
    response = agent.chat("Calculate the area of a rectangle with width 5 and height 10")
    print(f"Response: {response}")

def run_simplified_tools_example(model, observers=None):
    """
    Example demonstrating how to use the simplified liteagent_tool decorator.
    
    Args:
        model (str): The model to use
        observers (list, optional): List of observers to attach to the agents
    """
    # Check for API keys
    check_api_keys()
    
    print("\n=== Example: Simplified Tool Registration ===")
    
    # Create an instance of the simplified tools class
    tools_instance = SimplifiedToolsForAgents(api_key="fake-api-key-12345")
    
    # Create an agent with the simplified tools
    # Note: We don't need to manually create tool instances, just pass the functions
    simplified_agent = LiteAgent(
        model=model,
        name="SimplifiedAgent",
        system_prompt="You are a helpful assistant that can perform math operations and get weather information.",
        tools=[
            tools_instance.add_numbers,
            tools_instance.multiply_numbers, 
            tools_instance.get_weather,
            calculate_area
        ],
        debug=True,
        observers=observers
    )
    
    # Print the available tools
    print("Available tools:", [name for name in simplified_agent.tools.keys()])
    
    # Test with a query that uses multiple tools
    print("\n--- Simplified Agent Test ---")
    response = simplified_agent.chat("What's the weather in Berlin? Also, can you add 23 and 45? Finally, can you multiply 7 and 9? And calculate the area of a rectangle with width 5 and height 10.")
    print("Simplified Agent Response:", response)
    
    # Show that the instance state is maintained
    print(f"Tool call count: {tools_instance.get_call_count()}")

def run_examples(model, observers=None):
    """
    Run all examples.
    
    Args:
        model (str): The model to use
        observers (list, optional): List of observers to attach to the agents
    """
    # Check for API keys
    check_api_keys()
    
    # Create an agent with all tools
    agent = LiteAgent(
        model=model,
        name="LiteAgent",
        system_prompt="You are a helpful assistant that can perform various tasks.",
        tools=[get_weather, add_numbers, search_database],
        observers=observers
    )
    
    # Print available tools
    print("\n=== Available Tools ===")
    for name, tool in agent.tools.items():
        print(f"- {name}: {tool['description'] if isinstance(tool, dict) else tool.description}")
    
    # Test the agent with a simple query
    print("\n=== Weather Query ===")
    response = agent.chat("What's the weather in New York?")
    print(f"Response: {response}")
    
    # Test the agent with a math query
    print("\n=== Math Query ===")
    response = agent.chat("What is 3 + 7?")
    print(f"Response: {response}")
    
    # Test the agent with a search query
    print("\n=== Search Query ===")
    response = agent.chat("Search for information about climate change")
    print(f"Response: {response}")
    
    # Test the agent with a complex query that requires multiple tools
    print("\n=== Multi-tool Query ===")
    response = agent.chat("What's the weather in Paris and what is 15 + 27?")
    print(f"Response: {response}")
    
    # Run the custom agents example
    run_custom_agents_example(model, observers)
    
    # Run the class methods example
    run_class_methods_example(model, observers)
    
    # Run the simplified tools example
    run_simplified_tools_example(model, observers)