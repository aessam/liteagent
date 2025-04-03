# LiteAgent

A lightweight agent framework using LiteLLM for LLM interactions.

## Features

- Simple, lightweight agent implementation with clean abstractions
- Uses LiteLLM for model-agnostic LLM interactions
- Support for multiple function/tool calling formats:
  - OpenAI-style function calling (OpenAI, Groq, and compatible models)
  - Anthropic-style tool calling
  - Ollama JSON output parsing
  - Text-based function calling for models without native support
  - Structured output for models that need specific prompting
- Auto-detection of model capabilities and appropriate tool calling format
- Customizable system prompts
- Ability to create agents with specific tool sets
- Smart detection and prevention of repeated function calls
- Efficient handling of function call loops
- Support for different types of tools:
  - Standalone functions
  - Instance methods
  - Static methods
  - Decorated functions and methods with `@liteagent_tool`
- Hierarchical multi-agent systems with parent-child relationships
- Comprehensive observability layer with:
  - Context ID tracking for multi-agent systems
  - Parent-child relationship tracking between agents
  - Event-based logging of all agent operations
  - Multiple observer types (console, file, trace visualization)
  - Customizable observers for different monitoring needs

## Architecture

LiteAgent is designed with clean abstractions to make it easy to understand and extend:

- **Tools**: Abstraction for callable tools with `BaseTool`, `FunctionTool`, `InstanceMethodTool`, and `StaticMethodTool`
- **Models**: Abstraction for different model capabilities with `ModelInterface`, `FunctionCallingModel`, and `TextBasedFunctionCallingModel`
- **Memory**: Conversation history management with `ConversationMemory`
- **Agent**: Core orchestration with `LiteAgent`
- **Observer**: Event-based tracking and monitoring with `AgentObserver` implementations
- **Handlers**: Specialized handlers for different tool calling formats in the `handlers/` module

### Development Tools

The project includes a set of development and testing tools in the `tools/` directory:

- **Tool Format Detection**: Tools for analyzing and detecting function calling formats from different LLMs
- **Pattern Testing**: Utilities for testing the pattern-based tool extraction functionality
- **Batch Testing**: Scripts for running tests across multiple models and inputs
- **Analysis Tools**: Utilities for analyzing tool call performance and behavior

These tools are primarily for library developers and contributors to help with testing and improving the tool calling capabilities.

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

## Model Context Protocol (MCP) Integration

LiteAgent now includes built-in support for the Model Context Protocol (MCP), allowing your agents to work with any MCP-compatible clients like Claude Desktop.

### What is MCP?

The Model Context Protocol (MCP) is a standardized protocol for connecting AI systems with data sources and tools. It provides a common interface for sharing contextual information, exposing tools, and building composable integrations between language models and applications.

### Using LiteAgent with MCP

You can easily expose one or more LiteAgent instances as MCP servers using the `run_as_mcp` function:

```python
from liteagent import LiteAgent, run_as_mcp, liteagent_tool

# Define tools
@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@liteagent_tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny and 72 degrees."

# Create agents with different capabilities
math_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="Math",
    system_prompt="You are a Math Agent that can perform calculations.",
    tools=[add_numbers]
)

weather_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="Weather",
    system_prompt="You are a Weather Agent that can provide weather information.",
    tools=[get_weather]
)

# Run both agents as MCP servers
run_as_mcp(math_agent, weather_agent, server_name="Multi-Agent Demo")
```

This will start an MCP server that exposes both agents and their tools to any MCP-compatible client.

### MCP Server Configuration

The `run_as_mcp` function accepts several configuration options:

```python
run_as_mcp(
    agent1, 
    agent2, 
    server_name="My MCP Server",
    transport="sse",  # Transport protocol: "stdio" or "sse"
    host="127.0.0.1", # Host to bind the server to (for SSE transport)
    port=8000         # Port to bind the server to (for SSE transport)
)
```

You can also set these options using environment variables:
- `MCP_TRANSPORT`: Transport protocol to use ("stdio" or "sse")
- `MCP_HOST`: Host to bind the server to (default: "127.0.0.1")
- `MCP_PORT`: Port to bind the server to (default: 8000)

### Command-Line Interface

The MCP example provides a user-friendly command-line interface:

```bash
# Show help
python examples/mcp_example.py --help

# Run with default settings (SSE transport on 127.0.0.1:8000)
python examples/mcp_example.py

# Use stdio transport
python examples/mcp_example.py --transport stdio

# Specify host and port
python examples/mcp_example.py --host 0.0.0.0 --port 8080

# Specify model
python examples/mcp_example.py --model gpt-4o-mini

# Skip agent testing
python examples/mcp_example.py --skip-tests

# Enable debug mode
python examples/mcp_example.py --debug
```

The command-line interface is organized into logical groups:
- **MCP Server Configuration**: Options for configuring the MCP server
- **Model Configuration**: Options for specifying the model to use
- **Testing Options**: Options for controlling the testing phase
- **Debug Options**: Options for enabling debug mode

### Benefits of MCP Integration

- **Interoperability**: Your agents can work with any MCP-compatible client like Claude Desktop
- **Tool Sharing**: Expose agent-specific tools that can be discovered by clients
- **Resource Access**: Share system prompts and other agent information as MCP resources
- **Prompt Templates**: Expose agent functionality as interactive prompt templates

### Available MCP Features

When you run your agents with `run_as_mcp`, the following MCP features are exposed:

- **Tools**: All tools registered with your agents are exposed as MCP tools
- **Resources**: Agent system prompts and tool descriptions are exposed as MCP resources
- **Prompts**: Each agent can be interacted with through MCP prompts

For a complete example of using LiteAgent with MCP, see the [MCP example](examples/mcp_example.py).

## Using the Observer System

LiteAgent provides a comprehensive observer system for monitoring agent behavior:

```python
from liteagent import LiteAgent
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver
from liteagent.tools import liteagent_tool

# Define a tool
@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

# Create observers
console_observer = ConsoleObserver(verbose=True)  # Logs detailed events to console
file_observer = FileObserver(filename="agent_logs.jsonl")  # Logs events to a file
trace_observer = TreeTraceObserver()  # Builds a trace tree for visualization

# Create an agent with observers
agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="ObservableAgent",
    tools=[add_numbers],
    observers=[console_observer, file_observer, trace_observer]
)

# Chat with the agent
agent.chat("What is 5 + 7?")

# Print a visualization of the agent's actions
trace_observer.print_trace()
```

## Creating Multi-Agent Systems

LiteAgent supports creating hierarchical multi-agent systems where agents can call other agents:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

# Define some tools
@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@liteagent_tool
def get_weather(city: str) -> str:
    """Gets weather for a city."""
    return f"The weather in {city} is 22°C and sunny."

# Create a manager agent
manager = LiteAgent(
    model="gpt-4o-mini",
    name="Manager",
    system_prompt="You are a helpful assistant that coordinates tasks between specialized agents."
)

# Create specialized agents as child agents of the manager
math_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="MathAgent",
    system_prompt="You are a math specialist.",
    tools=[add_numbers],
    parent_context_id=manager.context_id  # Link to parent agent
)

weather_agent = LiteAgent(
    model="claude-3-haiku",
    name="WeatherAgent",
    system_prompt="You are a weather specialist.",
    tools=[get_weather],
    parent_context_id=manager.context_id  # Link to parent agent
)

# Convert child agents to tools for the manager
manager.tools = [
    math_agent.as_tool(name="math_agent", description="Use this for mathematical calculations."),
    weather_agent.as_tool(name="weather_agent", description="Use this for weather information.")
]

# Now the manager can delegate to specialized agents
response = manager.chat("I need to know the sum of 42 and 17, and also the weather in Tokyo.")
print(response)
```

## Auto-Detection of Model Capabilities

LiteAgent automatically detects the capabilities of different models and adapts accordingly:

```python
from liteagent import LiteAgent
from liteagent.tools import liteagent_tool

@liteagent_tool
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# Works with OpenAI models
openai_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="OpenAIAgent",
    tools=[calculate]
)

# Works with Anthropic models
anthropic_agent = LiteAgent(
    model="claude-3-haiku",
    name="AnthropicAgent",
    tools=[calculate]
)

# Works with Ollama models
ollama_agent = LiteAgent(
    model="ollama/phi3",
    name="OllamaAgent",
    tools=[calculate]
)

# Each agent automatically uses the appropriate tool calling format
```

## License

MIT 