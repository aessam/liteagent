# Migration Guides

This document provides guidance on how to migrate from deprecated features to their replacements.

## Table of Contents

- [Migrating from `ToolsForAgents` to Alternative Implementations](#migrating-from-toolsforagents)
- [Migrating to Refactored Tool Calling Handlers](#migrating-to-refactored-tool-calling-handlers)
- [Understanding Tool Calling Type Enum Changes](#understanding-tool-calling-type-enum-changes)
- [Using the New Observer System](#using-the-new-observer-system)
- [Converting to Multi-Agent Architecture](#converting-to-multi-agent-architecture)

## Migrating from `ToolsForAgents`

The `ToolsForAgents` class in the main library has been deprecated and will be removed in a future version. It has been moved to the test utilities.

### Original Usage

```python
from liteagent.tools import ToolsForAgents

tools_instance = ToolsForAgents(api_key="your-api-key")
weather = tools_instance.get_weather("New York")
```

### Recommended Approaches

#### Option 1: Use `FunctionTool` and class methods

```python
from liteagent.tools import FunctionTool

# Create a class with your tool methods
class WeatherTools:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def get_weather(self, city):
        # Implement weather lookup
        return {"temperature": 72, "condition": "sunny"}
        
# Create an instance and register its methods as tools
weather_tools = WeatherTools(api_key="your-api-key")
get_weather_tool = FunctionTool(weather_tools.get_weather)

# Use in an agent
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[get_weather_tool],
    # ... other parameters
)
```

#### Option 2: Use the `liteagent_tool` decorator (Recommended)

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

class WeatherTools:
    def __init__(self, api_key):
        self.api_key = api_key
        
    @liteagent_tool
    def get_weather(self, city: str) -> dict:
        """Get weather information for a city."""
        # Implementation using self.api_key
        return {"temperature": 72, "condition": "sunny"}
        
    @liteagent_tool
    def get_forecast(self, city: str, days: int = 3) -> list:
        """Get forecast for multiple days."""
        # Implementation
        return [{"day": 1, "temperature": 72}, {"day": 2, "temperature": 74}]

# Create an instance
tools = WeatherTools(api_key="your-api-key")

# Create an agent with the decorated methods
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[tools.get_weather, tools.get_forecast],
    # ... other parameters
)
```

## Migrating to Refactored Tool Calling Handlers

The tool calling handler system has been restructured to better support different types of tool calling formats.

### Original Usage

```python
from liteagent import LiteAgent
from liteagent.tool_calling_types import ToolCallingType

# Manually specifying the tool calling type
agent = LiteAgent(
    model="my-model",
    tool_calling_type=ToolCallingType.OPENAI
)
```

### New Usage

```python
from liteagent import LiteAgent

# The tool calling type is automatically detected based on the model
agent = LiteAgent(
    model="gpt-4o-mini"  # Will automatically use OpenAI-style
)

# For Anthropic models
agent = LiteAgent(
    model="claude-3-haiku"  # Will automatically use Anthropic-style
)

# For Ollama models
agent = LiteAgent(
    model="ollama/phi3"  # Will automatically use Ollama-style
)
```

## Understanding Tool Calling Type Enum Changes

The `ToolCallingType` enum has been expanded to support more models and calling styles.

### Original Enum

```python
class ToolCallingType(Enum):
    NONE = "none"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    STRUCTURED_OUTPUT = "structured_output"
```

### New Enum

```python
class ToolCallingType(Enum):
    NONE = "none"
    OPENAI = "openai"  # OpenAI-compatible models
    ANTHROPIC = "anthropic"  # Anthropic models
    GROQ = "groq"  # Groq-specific function calling
    OLLAMA = "ollama"  # Ollama JSON output parsing
    TEXT_BASED = "text_based"  # Simple text-based extraction
    STRUCTURED_OUTPUT = "structured_output"  # Prompt-based structured outputs
```

## Using the New Observer System

The observer system has been enhanced with more features and easier usage.

### Original Usage

```python
from liteagent import LiteAgent
from liteagent.observer import AgentObserver

class CustomObserver(AgentObserver):
    def on_event(self, event):
        # Process the event
        print(f"Event: {event.event_type}")

# Create and use the observer
observer = CustomObserver()
agent = LiteAgent(model="gpt-4o-mini", observers=[observer])
```

### New Usage with Built-in Observers

```python
from liteagent import LiteAgent
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver

# Create observers
console_observer = ConsoleObserver(verbose=True)  # Detailed console logging
file_observer = FileObserver(filename="agent_logs.jsonl")  # File logging
trace_observer = TreeTraceObserver()  # Visual trace builder

# Use multiple observers
agent = LiteAgent(
    model="gpt-4o-mini",
    observers=[console_observer, file_observer, trace_observer]
)

# Chat with the agent
response = agent.chat("Hello")

# Print the trace visualization
trace_observer.print_trace()
```

## Converting to Multi-Agent Architecture

If you have a single agent handling multiple types of tasks, you can migrate to a multi-agent architecture for better performance and specialization.

### Original Single-Agent Approach

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

@liteagent_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 75°F"

@liteagent_tool
def search_database(query: str) -> list:
    """Search database for information."""
    return [{"title": "Result", "text": f"Info about {query}"}]

# Single agent handling everything
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[get_weather, search_database]
)

response = agent.chat("What's the weather in Tokyo and find info about climate change")
```

### New Multi-Agent Architecture

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool
from liteagent.observer import TreeTraceObserver

# Create a trace observer
trace_observer = TreeTraceObserver()

@liteagent_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 75°F"

@liteagent_tool
def search_database(query: str) -> list:
    """Search database for information."""
    return [{"title": "Result", "text": f"Info about {query}"}]

# Create specialized agents
weather_agent = LiteAgent(
    model="gpt-3.5-turbo",  # Simpler model for simpler task
    name="WeatherAgent",
    system_prompt="You are a weather specialist.",
    tools=[get_weather],
    observers=[trace_observer]
)

search_agent = LiteAgent(
    model="claude-3-sonnet",  # More powerful model for complex task
    name="SearchAgent",
    system_prompt="You are a research specialist.",
    tools=[search_database],
    observers=[trace_observer]
)

# Create a coordinator agent
coordinator = LiteAgent(
    model="gpt-4o-mini",
    name="Coordinator",
    system_prompt="You are a coordinator that delegates tasks to specialized agents.",
    tools=[
        weather_agent.as_tool(name="weather_expert"),
        search_agent.as_tool(name="search_expert")
    ],
    observers=[trace_observer]
)

# Use the coordinator for complex queries
response = coordinator.chat("What's the weather in Tokyo and find info about climate change")

# Visualize the interactions
trace_observer.print_trace()
``` 