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

### Using Class Method Tools

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

class WeatherService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    @liteagent_tool
    def get_weather(self, city: str, date: str = "today") -> str:
        """Get the weather for a city."""
        # In a real app, you would use the API key to call a weather service
        if self.api_key:
            return f"Using API key {self.api_key[:5]}... to get weather for {city}: Sunny, 75°F"
        return f"The weather in {city} on {date} is sunny and 75°F"
        
    @liteagent_tool
    def get_forecast(self, city: str, days: int = 3) -> list:
        """Get a multi-day forecast for a city."""
        forecast = []
        for i in range(days):
            forecast.append(f"Day {i+1}: Sunny, {75 + i}°F")
        return forecast

# Create an instance of the weather service
weather_service = WeatherService(api_key="your-api-key-here")

# Create an agent with class method tools
agent = LiteAgent(
    model="gpt-4o-mini",
    name="WeatherAgent",
    system_prompt="You are a helpful weather assistant.",
    tools=[weather_service.get_weather, weather_service.get_forecast]
)

# Chat with the agent
response = agent.chat("What's the weather in Tokyo and what's the 5-day forecast?")
print(response)
```

### Using Observability

LiteAgent provides powerful observability features to monitor agent behavior:

```python
from liteagent import LiteAgent
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver
from liteagent.tools import liteagent_tool

@liteagent_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny and 75°F"

# Create observers
console_observer = ConsoleObserver(verbose=True)  # Prints detailed events to console
file_observer = FileObserver(filename="agent_logs.jsonl")  # Logs to a file
tree_observer = TreeTraceObserver()  # Builds a trace for visualization

# Create an agent with observers
agent = LiteAgent(
    model="gpt-4o-mini",
    name="ObservableAgent",
    system_prompt="You are a helpful weather assistant.",
    tools=[get_weather],
    observers=[console_observer, file_observer, tree_observer]
)

# Chat with the agent
response = agent.chat("What's the weather in Tokyo?")
print(f"Final response: {response}")

# Print a visualization of the agent's interactions
tree_observer.print_trace()
```

### Multi-Agent Systems

LiteAgent supports creating hierarchical multi-agent systems:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool
from liteagent.observer import TreeTraceObserver

# Create a trace observer to visualize agent interactions
trace_observer = TreeTraceObserver()

# Define tools for specialized agents
@liteagent_tool
def search_database(query: str) -> list:
    """Search the database for information."""
    return [{"title": "AI Advances", "excerpt": f"Information about {query}..."}]

@liteagent_tool
def calculate_stats(numbers: list) -> dict:
    """Calculate statistics for a list of numbers."""
    return {
        "mean": sum(numbers) / len(numbers),
        "max": max(numbers),
        "min": min(numbers),
        "count": len(numbers)
    }

# Create specialized agents
search_agent = LiteAgent(
    model="gpt-4o-mini",
    name="SearchAgent",
    system_prompt="You are a search expert. Provide relevant information from databases.",
    tools=[search_database],
    observers=[trace_observer]
)

stats_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="StatsAgent",
    system_prompt="You are a statistics expert. Calculate statistics accurately.",
    tools=[calculate_stats],
    observers=[trace_observer]
)

# Create a coordinator agent that uses the specialized agents as tools
coordinator = LiteAgent(
    model="claude-3-haiku",
    name="Coordinator",
    system_prompt="You are a coordinator that delegates tasks to specialized agents.",
    tools=[
        search_agent.as_tool(name="search_expert", 
                             description="Use this to search for information in databases"),
        stats_agent.as_tool(name="stats_expert", 
                            description="Use this to calculate statistics on numerical data")
    ],
    observers=[trace_observer]
)

# Ask the coordinator a question that requires both specialized agents
response = coordinator.chat("Find information about renewable energy and calculate the average of [45, 67, 89, 12, 34]")
print(f"Final response: {response}")

# Visualize the agent interactions
trace_observer.print_trace()
```

### Model Compatibility

LiteAgent automatically adapts to different model capabilities:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

@liteagent_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny and 75°F"

# Works with OpenAI models (native function calling)
openai_agent = LiteAgent(
    model="gpt-3.5-turbo",
    tools=[get_weather]
)

# Works with Anthropic models (tool use format)
anthropic_agent = LiteAgent(
    model="claude-3-haiku",
    tools=[get_weather]
)

# Works with Ollama models (JSON extraction)
ollama_agent = LiteAgent(
    model="ollama/llama3.3",
    tools=[get_weather]
)

# Each agent automatically uses the appropriate tool calling format
# for its underlying model, with no code changes needed
```

### Command-Line Usage

LiteAgent includes a command-line interface for easy testing:

```bash
# Show help
liteagent --help

# Run examples with a specific model
liteagent run --model gpt-4o-mini

# Run examples with a local model via Ollama
liteagent run --ollama --model phi3

# Enable observability in examples
liteagent run --enable-observability --model gpt-3.5-turbo

# View sample tool definitions
liteagent tools --sample-output
```

## Advanced Usage

For more advanced usage, including custom tool handling, multi-agent systems, and detailed observability, see the [API Reference](api_reference.md) and [Architecture Documentation](ARCHITECTURE.md). 