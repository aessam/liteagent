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
python -m liteagent --help

# Using the run command with a specific model
python -m liteagent run --model gpt-4o-mini

# Using the tools command to view sample tool definitions
python -m liteagent tools --sample-output
```

### Command Structure

The CLI now follows a command-based structure with these main commands:

```
liteagent                         # Base command
  |-- run                         # Run examples
  |     |-- --model MODEL         # Specify model to use
  |     |-- --class-methods       # Run only class methods example
  |     |-- --custom-agents       # Run only custom agents example
  |     |-- --all                 # Run all examples (default)
  |     |-- --ollama              # Use Ollama for local inference
  |     |-- --enable-observability # Enable observability features
  |
  |-- tools                       # Tool operations
  |     |-- --sample-output, -so  # Display sample tool definitions
  |
  |-- --version                   # Show version information
  |-- --debug                     # Enable debug mode
  |-- --debug-litellm            # Debug mode for LiteLLM
  |-- --log-file                  # Log to file
  |-- --no-color                  # Disable colored output
  |-- --help                      # Show help message
```

### Available CLI Commands

```bash
# Show help and available options
python -m liteagent --help

# Run examples with a specific model
python -m liteagent run --model gpt-4o-mini

# Run only the class methods example
python -m liteagent run --class-methods --model ollama/phi4

# Run only the custom agents example
python -m liteagent run --custom-agents --model ollama/llama3.3

# Run all examples (default behavior)
python -m liteagent run --all --model gpt-4o-mini

# Use local Ollama models
python -m liteagent run --ollama --model llama3.3

# Enable debug mode
python -m liteagent run --debug --model gpt-3.5-turbo

# Enable observability features
python -m liteagent run --enable-observability --model gpt-4o-mini

# View sample tool definitions
python -m liteagent tools --sample-output
```

### CLI Architecture

The CLI is organized into components:

1. **Command Module**: The `cli/commands.py` file contains the core CLI functionality:
   - Argument parsing with subcommands
   - Command execution
   - Model handling

2. **Entry Points**:
   - `liteagent/__main__.py`: Module-level entry point for `python -m liteagent`

### Sample Tool Output

The `tools --sample-output` command displays examples of tool definitions that would be sent to the LLM. This is useful for understanding how tools are formatted when sent to language models.

The output includes:
- Regular functions wrapped with `FunctionTool`
- Functions decorated with `@liteagent_tool`
- Class methods wrapped with `InstanceMethodTool`
- Class methods decorated with `@liteagent_tool`

Each tool definition shows:
- Name
- Description
- Parameters (with types and descriptions)
- Required fields

Example usage:

```bash
python -m liteagent tools --sample-output
# or
python -m liteagent tools -so
``` 