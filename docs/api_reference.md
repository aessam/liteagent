# LiteAgent API Reference

This document provides detailed information about the classes and functions in the LiteAgent framework.

## Core Components

### LiteAgent

```python
LiteAgent(
    model: str, 
    name: str = "agent",
    system_prompt: str = None, 
    tools: List = None,
    observers: List[AgentObserver] = None,
    parent_context_id: str = None
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

**Methods:**
- `chat(message: str) -> str`: Send a message to the agent and get a response
- `as_tool(name: str = None, description: str = None) -> AgentTool`: Convert the agent into a tool that can be used by another agent
- `reset_memory()`: Clear the agent's memory

### Tools

#### Decorators

```python
@tool
def my_tool(param1: str, param2: int) -> str:
    """Tool docstring"""
    # implementation
```

Decorator to register a function as a tool.

#### BaseTool

```python
BaseTool(
    name: str,
    description: str = None,
    parameters: Dict = None,
    function: Callable = None
)
```

Base class for all tools.

**Parameters:**
- `name`: The name of the tool
- `description`: Description of what the tool does
- `parameters`: Dictionary describing the parameters the tool accepts
- `function`: The function to call when the tool is used

**Methods:**
- `execute(**kwargs)`: Execute the tool with the given parameters

#### Tool Types

- `FunctionTool`: Tool created from a standalone function
- `InstanceMethodTool`: Tool created from an instance method
- `StaticMethodTool`: Tool created from a static method
- `AgentTool`: Tool created from an agent

### Observer System

#### AgentObserver

```python
AgentObserver()
```

Base class for all observers.

**Methods:**
- `on_event(event: AgentEvent)`: Called when an event occurs

#### Observer Types

- `ConsoleObserver`: Prints events to the console
- `FileObserver`: Logs events to a file
- `TreeTraceObserver`: Builds a tree visualization of agent interactions

#### Event Types

- `AgentInitializedEvent`: When an agent is initialized
- `UserMessageEvent`: When a user message is received
- `ModelRequestEvent`: When a request is sent to the model
- `ModelResponseEvent`: When a response is received from the model
- `FunctionCallEvent`: When a function is called
- `FunctionResultEvent`: When a function returns a result
- `AgentResponseEvent`: When the agent generates a response

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

## Constants

### ToolCallingType

Enum defining the types of tool calling supported:

- `NONE`: No tool calling support
- `OPENAI_FUNCTION_CALLING`: OpenAI-style function calling
- `ANTHROPIC_TOOL_CALLING`: Anthropic-style tool calling
- `OLLAMA_TOOL_CALLING`: Generic JSON output parsing
- `PROMPT_BASED`: Prompt-based tool calling 