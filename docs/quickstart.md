# LiteAgent Quickstart Guide

This guide will help you get started with LiteAgent, a lightweight agent framework that works with different LLM providers.

## Installation

```bash
pip install liteagent
```

## Basic Usage

### Creating a Simple Agent

```python
from liteagent import LiteAgent

# Create a basic agent
agent = LiteAgent(
    model="gpt-4o-mini",  # Or any supported model
    name="MyAgent",
    system_prompt="You are a helpful assistant that answers questions concisely."
)

# Chat with the agent
response = agent.chat("What is the capital of France?")
print(response)
```

### Using Tools with an Agent

```python
from liteagent import LiteAgent, tool

# Define tools (functions) for the agent to use
@tool
def get_weather(city: str, date: str = "today") -> str:
    """
    Get the weather for a city.
    
    Args:
        city: The city to get the weather for
        date: The date to get the weather for, defaults to today
    
    Returns:
        A string describing the weather
    """
    # In a real application, you would call a weather API here
    return f"The weather in {city} on {date} is sunny and 75°F"

@tool
def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers.
    
    Args:
        a: First number to add
        b: Second number to add
    
    Returns:
        The sum of a and b
    """
    return a + b

# Create an agent with tools
agent = LiteAgent(
    model="gpt-4o-mini",
    name="ToolAgent",
    system_prompt="You are a helpful assistant that can check weather and do math.",
    tools=[get_weather, add_numbers]
)

# Chat with the agent
response = agent.chat("What's the weather in Tokyo and what is 25 plus 17?")
print(response)
```

### Using Observability

```python
from liteagent import LiteAgent, ConsoleObserver, TreeTraceObserver
from liteagent.tools import get_weather

# Create observers
console_observer = ConsoleObserver()
tree_trace_observer = TreeTraceObserver()

# Create an agent with observers
agent = LiteAgent(
    model="gpt-4o-mini",
    name="ObservableAgent",
    system_prompt="You are a helpful weather assistant.",
    tools=[get_weather],
    observers=[console_observer, tree_trace_observer]
)

# Chat with the agent
response = agent.chat("What's the weather in Tokyo?")
print(response)

# Get the trace tree
trace = tree_trace_observer.get_tree_visualization()
print(trace)
```

### Creating Multi-Agent Systems

```python
from liteagent import LiteAgent
from liteagent.tools import get_weather, add_numbers

# Create specialized agents
weather_agent = LiteAgent(
    model="gpt-4o-mini",
    name="WeatherAgent",
    system_prompt="You are a weather expert.",
    tools=[get_weather]
)

calculator_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="CalculatorAgent",
    system_prompt="You are a math expert.",
    tools=[add_numbers]
)

# Create a routing agent
router_agent = LiteAgent(
    model="gpt-4o-mini",
    name="RouterAgent",
    system_prompt="You are a router that delegates tasks to specialized agents.",
    tools=[
        weather_agent.as_tool(description="Get weather information"),
        calculator_agent.as_tool(description="Perform calculations")
    ]
)

# Chat with the router agent
response = router_agent.chat("What's the weather in Tokyo and what is 25 + 17?")
print(response)
```

## Next Steps

- Explore the [API Reference](api_reference.md) for detailed information about LiteAgent classes and methods
- Check out the [Examples](examples.md) for more advanced use cases
- Learn about [Model Support](model_support.md) to understand which LLM providers and models are supported 