# LiteAgent

A lightweight agent framework using LiteLLM for LLM interactions.

## Features

- Simple, lightweight agent implementation with clean abstractions
- Uses LiteLLM for model-agnostic LLM interactions
- Support for function/tool calling with compatible models
- Fallback text-based function calling for models without native function calling
- Customizable system prompts
- Ability to create agents with specific tool sets
- Smart detection and prevention of repeated function calls
- Efficient handling of function call loops
- Support for different types of tools:
  - Standalone functions
  - Instance methods
  - Static methods
  - Decorated functions and methods with `@liteagent_tool`
- **New**: Comprehensive observability layer with:
  - Context ID tracking for multi-agent systems
  - Parent-child relationship tracking between agents
  - Event-based logging of all agent operations
  - Customizable observers for different monitoring needs

## Architecture

LiteAgent is designed with clean abstractions to make it easy to understand and extend:

- **Tools**: Abstraction for callable tools with `BaseTool`, `FunctionTool`, `InstanceMethodTool`, and `StaticMethodTool`
- **Models**: Abstraction for different model capabilities with `ModelInterface`, `FunctionCallingModel`, and `TextBasedFunctionCallingModel`
- **Memory**: Conversation history management with `ConversationMemory`
- **Agent**: Core orchestration with `LiteAgent`
- **Observer**: Event-based tracking and monitoring with `AgentObserver` implementations

## Installation

### Via pip (recommended)

```bash
pip install liteagent
```

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/liteagent.git
cd liteagent

# Install in development mode
pip install -e .
```

## Quick Start

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

# Define a tool using the decorator
@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

# Create an agent
agent = LiteAgent(model="gpt-3.5-turbo")

# Chat with the agent
response = agent.chat("What is 3 + 7?")
print(response)
```

## Command-Line Usage

LiteAgent comes with a command-line interface that follows a command-based structure:

### Using the installed liteagent command

After installation, you can use the `liteagent` command directly:

```bash
# Show help and available options
liteagent --help

# Run examples with a specific model
liteagent run --model gpt-4o-mini

# Run only the class methods example
liteagent run --class-methods --model ollama/phi4

# View sample tool definitions
liteagent tools --sample-output
```

### Using Python module syntax

You can run the CLI using Python module syntax:

```bash
# Show help and available options
python -m liteagent --help

# Run examples with a specific model
python -m liteagent run --model gpt-4o-mini

# Run only the class methods example
python -m liteagent run --class-methods --model ollama/phi4

# View sample tool definitions
python -m liteagent tools --sample-output
```

### Available Commands

The CLI now follows a command-based structure with these main commands:

```bash
# Run examples (with various options)
python -m liteagent run --model gpt-4o-mini [options]

# Tool-related operations
python -m liteagent tools --sample-output

# Show version information
python -m liteagent --version
```

### Available Command-Line Arguments

The following command-line arguments are available:

#### Global options (work with any command)
- `--version`: Show version information and exit
- `--debug`: Enable debug mode with verbose logging
- `--debug-litellm`: Enable debug mode for LiteLLM
- `--log-file`: Log output to a file
- `--no-color`: Disable colored log output

#### Run command options
- `--model MODEL`: Model to use (e.g., gpt-4o-mini, ollama/phi4)
- `--class-methods`: Run only the class methods example
- `--custom-agents`: Run only the custom agents example
- `--all`: Run all examples (default behavior)
- `--ollama`: Use Ollama for local inference (automatically prepends 'ollama/' to model name)
- `--enable-observability`: Enable observability features

#### Tools command options
- `--sample-output` or `-so`: Display sample tool definitions as they would be sent to the LLM

For more details on examples and CLI usage, see the [Examples and CLI Documentation](docs/examples_and_cli.md).

## Creating Agents with Custom Tools

You can create multiple agents with different system prompts and tool sets:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

# Define tools
@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@liteagent_tool
def get_weather(city: str) -> str:
    """Returns weather information for a city."""
    return f"The weather in {city} is 22°C and sunny."

# Create a math-only agent
math_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="MathAgent",
    system_prompt="You are a math specialist. You can only perform mathematical calculations.",
    tools=[add_numbers],  # Only provide the add_numbers tool
)

# Create a weather-only agent
weather_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="WeatherAgent",
    system_prompt="You are a weather specialist. You can only provide weather information.",
    tools=[get_weather],  # Only provide the weather tool
)

# Use the agents
math_response = math_agent.chat("What is 42 + 17?")
weather_response = weather_agent.chat("What's the weather in Tokyo?")
```

## Using Class Methods as Tools

LiteAgent supports using class methods as tools, which is useful for organizing related functionality:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

class ToolsForAgents:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    @liteagent_tool
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return a + b
        
    @liteagent_tool
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return a * b
        
    @liteagent_tool
    def get_weather(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        if self.api_key:
            # Use API key to get real weather
            return f"Weather in {city} retrieved with API key {self.api_key[:5]}..."
        else:
            return f"The weather in {city} is 22°C and sunny."

# Create an instance of the tools class
tools_instance = ToolsForAgents(api_key="your-api-key-here")

# Create an agent with decorated class methods as tools
agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="MathWeatherAgent",
    tools=[
        tools_instance.add_numbers,
        tools_instance.get_weather
    ]
)

# Use the agent
response = agent.chat("What's the weather in Paris and what is 15 + 27?")
print(response)
```

## Advanced Usage

### Custom Tool Registration

You can use the `liteagent_tool` decorator to customize tool names and descriptions:

```python
from liteagent.tools import liteagent_tool

@liteagent_tool(name="calculate_sum", description="Calculate the sum of two numbers")
def add_numbers(a: int, b: int) -> int:
    return a + b
```

### Direct Tool Creation

You can create tools directly using the tool classes:

```python
from liteagent.tools import FunctionTool, InstanceMethodTool

# Create a function tool
def multiply(a: int, b: int) -> int:
    return a * b
    
multiply_tool = FunctionTool(multiply, name="multiply_numbers")

# Create an instance method tool
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
        
calc = Calculator()
add_tool = InstanceMethodTool(calc.add, calc, name="addition")
```

## Advanced Features

### Loop Detection and Prevention

LiteAgent automatically detects and prevents repeated function calls and function call loops, which can be common issues with LLM-based agents. This helps to:

- Reduce token usage and API costs
- Prevent infinite loops
- Improve response times
- Ensure the agent provides a final answer to the user

The agent uses several strategies to detect and handle loops:

1. Normalizing function arguments to detect similar calls
2. Tracking function call history
3. Counting repeated calls to the same function
4. Adding explicit instructions to guide the model toward a final response

### Models Without Native Function Calling

For models that don't support native function calling (like some local models), LiteAgent provides a text-based function calling mechanism. The agent:

1. Includes function descriptions in the system prompt
2. Parses function calls from the model's text output
3. Executes the functions and returns results
4. Handles repeated function calls efficiently

## Observability

LiteAgent includes a comprehensive observability layer that allows you to track and monitor all agent operations, including tracing inter-agent relationships and function calls.

### Context IDs

Each agent has a unique context ID, and can optionally have a parent context ID. This allows you to trace the flow of execution in multi-agent systems.

```python
# Create a parent context ID
parent_context_id = generate_context_id()

# Create a main agent with this context
main_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="MainAgent",
    context_id=parent_context_id
)

# Create a child agent that references the parent
child_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="ChildAgent",
    parent_context_id=parent_context_id
)
```

### Observer Pattern

LiteAgent uses the observer pattern to notify interested parties about agent events:

```python
# Create observers
console_observer = ConsoleObserver()
file_observer = FileObserver("agent_events.jsonl")

# Create an agent with observers
agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="MyAgent",
    observers=[console_observer, file_observer]
)

# Add more observers later
agent.add_observer(my_custom_observer)
```

### Events

The following events are tracked:

- `AgentInitializedEvent`: When an agent is created
- `UserMessageEvent`: When a user message is received
- `ModelRequestEvent`: Before a request is sent to the model
- `ModelResponseEvent`: After a response is received from the model
- `FunctionCallEvent`: Before a function/tool is called
- `FunctionResultEvent`: After a function/tool returns a result
- `AgentResponseEvent`: When an agent generates a final response

### Custom Observers

You can create custom observers by implementing the `AgentObserver` interface:

```python
class MyCustomObserver(AgentObserver):
    def on_event(self, event: AgentEvent) -> None:
        # Handle the event
        print(f"Received event: {event.event_type}")
        
    # Optionally override specific event handlers
    def on_function_call(self, event: FunctionCallEvent) -> None:
        print(f"Function call: {event.function_name}")
```

### Example

See `example_observability.py` for a complete example of using the observability features.

## License

MIT 