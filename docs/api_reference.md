# LiteAgent API Reference

This document provides detailed information about the classes and functions in the LiteAgent framework.

## Project Organization

LiteAgent is organized with a clean separation of concerns:

- **Core Library**: The `liteagent/` directory contains the core framework code.
- **Examples**: The `examples/` directory contains example tools and usage patterns.
- **CLI**: The `cli/` directory contains the command-line interface.
- **Tests**: The `tests/` directory contains unit and integration tests.

## Core Components

### LiteAgent

```python
LiteAgent(
    model: str, 
    name: str = "agent",
    system_prompt: str = None, 
    tools: List = None,
    observers: List[AgentObserver] = None,
    parent_context_id: str = None,
    context_id: str = None,
    debug: bool = False,
    drop_params: bool = True
)
```

The main agent class that orchestrates interactions between the user, model, and tools.

**Parameters:**
- `model`: The model to use for the agent (e.g., "gpt-4o-mini", "claude-3-sonnet")
- `name`: The name of the agent
- `system_prompt`: The system prompt to use for the agent
- `tools`: List of tools the agent can use
- `observers`: List of observers to attach to the agent
- `parent_context_id`: Context ID of the parent agent, if this is a child agent
- `context_id`: Explicit context ID for the agent (generated automatically if not provided)
- `debug`: Whether to enable debug logging
- `drop_params`: Whether to drop parameters not supported by the model

**Methods:**
- `chat(message: str) -> str`: Send a message to the agent and get a response
- `as_tool(name: str = None, description: str = None) -> AgentTool`: Convert the agent into a tool that can be used by another agent
- `reset_memory()`: Clear the agent's memory
- `add_observer(observer: AgentObserver)`: Add an observer to the agent
- `remove_observer(observer: AgentObserver)`: Remove an observer from the agent

### Tools

#### Decorators

```python
from liteagent.tools import liteagent_tool

@liteagent_tool(name=None, description=None)
def my_tool(param1: str, param2: int) -> str:
    """Tool docstring"""
    # implementation
```

Decorator to register a function as a tool. Optional parameters:
- `name`: Custom name for the tool (defaults to function name)
- `description`: Custom description (defaults to function docstring)

#### BaseTool

```python
BaseTool(
    func: Callable,
    name: str = None,
    description: str = None
)
```

Base class for all tools.

**Parameters:**
- `func`: The function to call when the tool is used
- `name`: The name of the tool (defaults to function name)
- `description`: Description of what the tool does (defaults to function docstring)

**Methods:**
- `execute(**kwargs)`: Execute the tool with the given parameters
- `to_function_definition()`: Convert the tool to an OpenAI-compatible function definition
- `to_dict()`: Convert the tool to a dictionary representation

#### Tool Types

- `FunctionTool`: Tool created from a standalone function
- `InstanceMethodTool`: Tool created from an instance method
- `StaticMethodTool`: Tool created from a static method
- `AgentTool`: Tool created from an agent

### Observer System

The Observer system provides comprehensive tracking and monitoring of agent operations through events.

#### AgentEvent Types

All events inherit from the base `AgentEvent` class and include common fields:
- `agent_id`: Unique ID of the agent
- `agent_name`: Name of the agent
- `context_id`: Context ID for tracking agent interactions
- `parent_context_id`: Optional parent context ID
- `timestamp`: When the event occurred

Available event types:
- `AgentInitializedEvent`: When an agent is initialized, includes model and tools info
- `UserMessageEvent`: When a user message is received
- `ModelRequestEvent`: When a request is sent to the model
- `ModelResponseEvent`: When a response is received from the model
- `FunctionCallEvent`: When a function is called, includes arguments
- `FunctionResultEvent`: When a function returns a result
- `AgentResponseEvent`: When the agent generates a response to the user

#### AgentObserver

```python
AgentObserver()
```

Base class for all observers.

**Methods:**
- `on_event(event: AgentEvent)`: Called when any event occurs
- `on_agent_initialized(event: AgentInitializedEvent)`: Called when an agent is initialized
- `on_user_message(event: UserMessageEvent)`: Called when a user message is received
- `on_model_request(event: ModelRequestEvent)`: Called when a request is sent to the model
- `on_model_response(event: ModelResponseEvent)`: Called when a response is received from the model
- `on_function_call(event: FunctionCallEvent)`: Called when a function is called
- `on_function_result(event: FunctionResultEvent)`: Called when a function returns a result
- `on_agent_response(event: AgentResponseEvent)`: Called when the agent generates a response

#### Built-in Observer Types

- `ConsoleObserver`: Logs events to the console with configurable verbosity
- `FileObserver`: Logs events to a file in JSONL format
- `TreeTraceObserver`: Builds a tree visualization of agent interactions

#### UnifiedObserver

```python
UnifiedObserver(
    console_output: bool = True,
    file_output: bool = False,
    file_path: str = "agent_events.jsonl",
    build_trace: bool = False,
    verbose: bool = False
)
```

Combines multiple observer capabilities (console, file, tracing) in one observer.

**Parameters:**
- `console_output`: Whether to log events to the console
- `file_output`: Whether to log events to a file
- `file_path`: Path to the file for event logging
- `build_trace`: Whether to build a tree trace of events
- `verbose`: Whether to include full event details in logs

**Methods:**
- `print_trace(output=sys.stdout)`: Print the event trace tree

### Model Interface

```python
ModelInterface(model_name: str)
```

Base class for model interfaces.

**Parameters:**
- `model_name`: The name of the model to use

**Methods:**
- `generate_response(messages: List[Dict], tools: List = None) -> Dict`: Generate a response from the model

#### Model Interface Types

- `FunctionCallingModel`: For models that support native function calling
- `TextBasedFunctionCallingModel`: For models that use text-based function calling

### Tool Calling Types

The `ToolCallingType` enum defines the different types of tool calling supported:

- `NONE`: No tool calling support
- `OPENAI`: OpenAI-style function calling (compatible with Groq and similar models)
- `ANTHROPIC`: Anthropic-style tool calling
- `GROQ`: Groq-specific tool calling
- `OLLAMA`: Ollama-style tool calling through structured JSON output
- `TEXT_BASED`: Simple text-based function call patterns
- `STRUCTURED_OUTPUT`: Models that need specific prompting to return structured outputs

### Memory

```python
ConversationMemory()
```

Manages conversation history.

**Methods:**
- `add_user_message(message: str)`: Add a user message to memory
- `add_assistant_message(message: str)`: Add an assistant message to memory
- `add_function_call(function_name: str, arguments: Dict)`: Add a function call to memory
- `add_function_result(function_name: str, result: Any)`: Add a function result to memory
- `get_messages() -> List[Dict]`: Get all messages in memory
- `reset()`: Clear all messages from memory

## Utility Functions

```python
setup_logging(level: str = "INFO")
```

Set up logging for the LiteAgent framework.

```python
check_api_keys(models: List[str] = None) -> Dict[str, bool]
```

Check if the required API keys are available for the given models.

```python
generate_context_id() -> str
```

Generate a unique context ID for tracking agent interactions.

```python
detect_model_capability(model_name: str, model_interface: ModelInterface = None) -> ToolCallingType
```

Detect the tool calling capabilities of a model. 