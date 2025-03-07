# LiteAgent Examples and CLI

This document explains the example tools and command-line interface (CLI) provided with LiteAgent.

## Examples

The `examples/` directory contains example implementations and tools that can be used with LiteAgent.

### Example Tools

The `examples/tools.py` file contains example tool implementations:

```python
from liteagent import LiteAgent
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

LiteAgent provides a command-line interface for running examples and testing the framework.

### Running the CLI

You can run the CLI in several ways:

```bash
# Using the Python module syntax
python -m liteagent --model gpt-4o-mini

# Directly from the cli directory
python cli/main.py --model gpt-4o-mini

# From the main.py in the project root
python main.py --model gpt-4o-mini
```

### Available CLI Commands

```bash
# Show help and available options
python -m liteagent --help

# Run with a specific model
python -m liteagent --model gpt-4o-mini

# Run only the class methods example
python -m liteagent --class-methods --model ollama/phi4

# Run only the custom agents example
python -m liteagent --custom-agents --model ollama/llama3.3

# Run all examples (default behavior)
python -m liteagent --all --model gpt-4o-mini

# Use local Ollama models
python -m liteagent --ollama --model llama3.3

# Enable debug mode
python -m liteagent --debug --model gpt-3.5-turbo

# Enable observability features
python -m liteagent --enable-observability --model gpt-4o-mini
```

### CLI Architecture

The CLI is organized into two main components:

1. **Command Module**: The `cli/commands.py` file contains the core CLI functionality:
   - Argument parsing
   - Command execution
   - Model handling

2. **Entry Points**:
   - `cli/main.py`: Direct entry point for running the CLI
   - `liteagent/__main__.py`: Module-level entry point for `python -m liteagent`
   - `main.py`: Project root entry point

This separation makes it easy to maintain the CLI functionality independently of the core library code. 