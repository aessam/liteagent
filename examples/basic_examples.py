"""
Basic examples demonstrating various features of LiteAgent.
"""

from liteagent import LiteAgent
from liteagent.utils import check_api_keys
from examples.tools import get_weather, add_numbers, search_database
from examples.tools import ToolsForAgents, SimplifiedToolsForAgents, calculate_area

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