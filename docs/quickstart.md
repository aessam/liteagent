# LiteAgent Quickstart Guide

This guide will help you get started with LiteAgent, a lightweight agent framework that works with different LLM providers.

## Installation

```bash
pip install liteagent
```

## Project Structure

LiteAgent is organized with a clean separation of concerns:

- **Core Library**: The `liteagent/` directory contains the core framework code.
- **Examples**: The `examples/` directory contains example tools and usage patterns.
- **CLI**: The `cli/` directory contains the command-line interface.
- **Tests**: The `tests/` directory contains unit and integration tests.

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

There are multiple ways to define tools for your agent:

#### Using the Decorator Approach (Recommended)

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

# Define tools using the decorator
@liteagent_tool
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

@liteagent_tool
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

#### Using Explicit Tool Classes

```python
from liteagent import LiteAgent
from liteagent.tools import FunctionTool

# Define functions
def get_weather(city: str, date: str = "today") -> str:
    """Get the weather for a city."""
    return f"The weather in {city} on {date} is sunny and 75°F"

def add_numbers(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

# Create tool objects
weather_tool = FunctionTool(get_weather)
add_tool = FunctionTool(add_numbers)

# Create an agent with tool objects
agent = LiteAgent(
    model="gpt-4o-mini",
    name="ToolAgent",
    system_prompt="You are a helpful assistant that can check weather and do math.",
    tools=[weather_tool, add_tool]
)

# Chat with the agent
response = agent.chat("What's the weather in Tokyo and what is 25 plus 17?")
print(response)
```

### Using Observability

```python
from liteagent import LiteAgent
from liteagent.observer import ConsoleObserver, TreeTraceObserver
from liteagent.tools import liteagent_tool

@liteagent_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny and 75°F"

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
from liteagent.tools import liteagent_tool

@liteagent_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny and 75°F"

@liteagent_tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

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

### Using Class Methods as Tools

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

class WeatherService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    @liteagent_tool
    def get_current_weather(self, city: str) -> str:
        """Get current weather for a city."""
        # In a real app, you would use the API key to call a weather API
        return f"The weather in {city} is sunny and 75°F"
        
    @liteagent_tool
    def get_forecast(self, city: str, days: int = 3) -> list:
        """Get weather forecast for a city."""
        # Mock implementation
        return [f"Day {i+1}: Sunny, {70+i}°F" for i in range(days)]
        
    @liteagent_tool(
        name="historical_weather",
        description="Get historical weather data for a location"
    )
    def get_historical(self, city: str, date: str) -> dict:
        """Get historical weather for a specific date."""
        return {
            "city": city,
            "date": date,
            "temperature": "72°F",
            "conditions": "Partly cloudy"
        }

# Create service instance
weather_service = WeatherService(api_key="demo-api-key")

# Create an agent with decorated class methods as tools
agent = LiteAgent(
    model="gpt-4o-mini",
    name="WeatherAgent",
    system_prompt="You are a helpful weather assistant.",
    tools=[
        weather_service.get_current_weather,
        weather_service.get_forecast,
        weather_service.get_historical
    ]
)

# Chat with the agent
response = agent.chat("What's the weather in Paris?")
print(response)
```

## Command-Line Usage

LiteAgent provides a command-based CLI for running examples and viewing tool definitions:

```bash
# Show help
python -m liteagent --help

# Run examples with a specific model
python -m liteagent run --model gpt-4o-mini

# View sample tool definitions
python -m liteagent tools --sample-output

# Run only the class methods example
python -m liteagent run --class-methods --model gpt-4o-mini
```

## Using Example Tools

LiteAgent comes with example tools that you can use directly:

```python
from liteagent import LiteAgent
from examples.tools import get_weather, add_numbers, search_database

# Create an agent with the example tools
agent = LiteAgent(
    model="gpt-4o-mini",
    name="ExampleToolsAgent",
    system_prompt="You are a helpful assistant that can use various tools.",
    tools=[get_weather, add_numbers, search_database]
)

# Chat with the agent
response = agent.chat("What's the weather in Paris and what is 15 + 27?")
print(response)
```

## Next Steps

- Explore the [API Reference](api_reference.md) for detailed information about LiteAgent classes and methods
- Check out the [Examples](examples/) directory for more advanced use cases
- See [Examples and CLI](examples_and_cli.md) for details on example tools and the command-line interface
- Learn about [Model Support](model_support.md) to understand which LLM providers and models are supported 