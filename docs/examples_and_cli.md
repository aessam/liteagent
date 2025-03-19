# LiteAgent Examples and CLI

This document explains the example tools and command-line interface (CLI) provided with LiteAgent.

## Examples

The `examples/` directory contains example implementations and tools that can be used with LiteAgent.

### Example Tools

The `examples/tools.py` file contains example tool implementations:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool
from examples.tools import get_weather, add_numbers, search_database, calculate_area
from examples.tools import ToolsForAgents, SimplifiedToolsForAgents

# Using standalone tools
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[get_weather, add_numbers, search_database, calculate_area]
)

# Using class method tools
tools_instance = ToolsForAgents(api_key="your-api-key")
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[
        tools_instance.add_numbers,
        tools_instance.multiply_numbers,
        tools_instance.get_weather,
        tools_instance.get_user_data
    ]
)

# Using simplified tools with decorators
simplified_tools = SimplifiedToolsForAgents(api_key="your-api-key")
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[
        simplified_tools.add_numbers,
        simplified_tools.multiply_numbers,
        simplified_tools.get_weather,
        simplified_tools.get_user_data
    ]
)
```

### Tool Definition Approaches

LiteAgent supports multiple ways to define tools:

1. **Using the `liteagent_tool` decorator on standalone functions**:

```python
from liteagent.tools import liteagent_tool

@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b
```

2. **Using the decorator with custom parameters**:

```python
@liteagent_tool(
    name="find_user",
    description="Find a user by ID or email"
)
def get_user(user_identifier: str) -> dict:
    """Find user by ID or email."""
    # Implementation here
    pass
```

3. **Using the decorator with class methods**:

```python
class ToolsWithDecorators:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @liteagent_tool
    def get_profile(self, user_id: str) -> dict:
        """Get user profile information."""
        # Implementation here
        pass
        
    @liteagent_tool(
        name="analyze_text_sentiment",
        description="Analyze the sentiment of a text passage"
    )
    def analyze_sentiment(self, text: str) -> dict:
        """Analyze the sentiment of a text passage."""
        # Implementation here
        pass
```

4. **Using explicit tool wrappers**:

```python
from liteagent.tools import FunctionTool, InstanceMethodTool

# Function tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

multiply_tool = FunctionTool(multiply)

# Instance method tool
class Calculator:
    def add(self, a: int, b: int) -> int:
        """Adds two numbers."""
        return a + b

calc = Calculator()
add_tool = InstanceMethodTool(calc.add, calc)
```

### Multi-Agent Examples

The examples include demonstrations of multi-agent systems:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool
from liteagent.observer import TreeTraceObserver

# Create some tools
@liteagent_tool
def get_weather(city: str) -> str:
    """Gets the weather for a city."""
    return f"The weather in {city} is sunny with a high of 75°F"

@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

# Create a trace observer to visualize the agent interactions
trace_observer = TreeTraceObserver()

# Create specialized agents
weather_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="WeatherExpert",
    system_prompt="You are a weather expert. Provide detailed weather information.",
    tools=[get_weather],
    observers=[trace_observer]
)

math_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="MathExpert",
    system_prompt="You are a math expert. Solve math problems accurately.",
    tools=[add_numbers],
    observers=[trace_observer]
)

# Create a coordinator agent that uses the experts
coordinator = LiteAgent(
    model="gpt-4o-mini",
    name="Coordinator",
    system_prompt="You are a helpful assistant that delegates tasks to appropriate experts.",
    tools=[
        weather_agent.as_tool(name="weather_expert", 
                              description="Ask the weather expert about weather-related questions"),
        math_agent.as_tool(name="math_expert", 
                           description="Ask the math expert about math problems")
    ],
    observers=[trace_observer]
)

# Ask the coordinator a complex question
response = coordinator.chat("What's the weather in New York and what is 123 + 456?")

# Print the trace to visualize the agent interactions
trace_observer.print_trace()
```

### Example Runners

The `examples/basic_examples.py` file contains functions to run demonstration examples:

```python
from examples.basic_examples import (
    run_examples,                  # Run all examples
    run_class_methods_example,     # Run class methods example
    run_custom_agents_example,     # Run custom agents example
    run_simplified_tools_example   # Run simplified tools example
)

# Run all examples with a specific model
run_examples(model="gpt-4o-mini")

# Run only the class methods example
run_class_methods_example(model="ollama/llama3.3")
```

## Command-Line Interface (CLI)

LiteAgent provides a command-line interface for running examples, viewing tool definitions, and testing the framework.

### Running the CLI

You can run the CLI in several ways:

```bash
# Using the Python module syntax
python -m liteagent [command] [options]

# Using the installed liteagent command
liteagent [command] [options]
```

### Available Commands

The CLI uses a command-based structure:

```bash
# Run examples
liteagent run [options]

# Tool operations
liteagent tools [options]

# Show version
liteagent --version
```

### Global Options

The following global options work with any command:

```bash
# Show help
liteagent --help

# Show version info
liteagent --version

# Enable debug mode
liteagent [command] --debug

# Enable LiteLLM debug
liteagent [command] --debug-litellm

# Log to file
liteagent [command] --log-file=agent.log

# Disable colored output
liteagent [command] --no-color
```

### Run Command

The `run` command executes examples:

```bash
# Run all examples with a specific model
liteagent run --model gpt-4o-mini

# Run only the class methods example
liteagent run --class-methods --model ollama/phi4

# Run only the custom agents example
liteagent run --custom-agents --model claude-3-haiku

# Use Ollama for local inference
liteagent run --ollama --model phi3
# This is equivalent to: liteagent run --model ollama/phi3

# Enable observability features
liteagent run --enable-observability --model gpt-4o-mini
```

### Tools Command

The `tools` command provides information about tool definitions:

```bash
# Display sample tool definitions as they would be sent to the LLM
liteagent tools --sample-output
```

### Examples with Specific Features

```bash
# Run examples with observability enabled
liteagent run --enable-observability --model gpt-4o-mini

# Run examples with a local model
liteagent run --ollama --model phi3

# Run examples with a specific model and debug logging
liteagent run --model claude-3-haiku --debug

# Run examples with output saved to a log file
liteagent run --model gpt-4o-mini --log-file=agent_runs.log
```

## Adding Your Own Examples

You can add your own examples by:

1. Creating tool functions in your code
2. Registering them with the `liteagent_tool` decorator
3. Creating an agent with your tools
4. Chatting with the agent

Example:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool
from liteagent.observer import ConsoleObserver

# Define your own tools
@liteagent_tool
def search_database(query: str) -> list:
    """Search the database for information."""
    # This is a mock implementation
    return [{"id": 1, "name": "Example Result", "data": f"Data for: {query}"}]

@liteagent_tool
def send_notification(user_id: str, message: str) -> bool:
    """Send a notification to a user."""
    # This is a mock implementation
    print(f"Sending notification to user {user_id}: {message}")
    return True

# Create an observer
observer = ConsoleObserver(verbose=True)

# Create an agent with your tools
agent = LiteAgent(
    model="gpt-4o-mini",
    name="DatabaseAgent",
    system_prompt="You are an assistant that can search databases and send notifications.",
    tools=[search_database, send_notification],
    observers=[observer]
)

# Chat with your agent
response = agent.chat("Search the database for information about AI and notify user 123 about the results.")
print(f"Final response: {response}")
``` 