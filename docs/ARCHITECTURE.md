# LiteAgent Architecture

This document describes the high-level architecture of the LiteAgent library.

## Core Components

LiteAgent is organized around these key components:

- `LiteAgent`: The main agent class that coordinates interactions between tools and LLMs
- `Models`: Interfaces for different LLM providers
- `Tools`: Registry and implementation of tools (functions) that agents can use
- `Memory`: Conversation history management
- `Observer`: Event notification system for monitoring agent behavior

## Tool Calling

LiteAgent supports multiple different tool calling strategies:

### Tool Calling Types

The `ToolCallingType` enum defines the different types of tool calling:

- `NONE`: No tool calling support
- `OPENAI`: OpenAI-style function calling (includes Groq and compatible models)
- `ANTHROPIC`: Anthropic-style tool calling
- `GROQ`: Groq-specific tool calling
- `OLLAMA`: Generic JSON output parsing for Ollama models
- `TEXT_BASED`: Simple text-based function call patterns
- `STRUCTURED_OUTPUT`: Models that need specific prompting to return structured outputs

### Tool Calling Handlers

Tool calls are handled by specialized handler classes in the `handlers` module:

- `OpenAIToolCallingHandler`: Handles OpenAI-style function calling
- `AnthropicToolCallingHandler`: Handles Anthropic-style tool calling
- `GroqToolCallingHandler`: Handles Groq-specific function calling
- `OllamaToolCallingHandler`: Handles Ollama-style tool calling
- `TextBasedToolCallingHandler`: Handles text-based function calling
- `StructuredOutputHandler`: Handles structured output tool calling
- `NoopToolCallingHandler`: Used when no tool calling is supported
- `AutoDetectToolCallingHandler`: Auto-detects the appropriate handler based on the response

## Agent-Tool Interaction Flow

1. Agent receives a user input
2. Agent prepares LLM request with tools and conversation history
3. LLM response is processed to extract potential tool calls
4. If a tool call is detected:
   - Tool is executed with the provided arguments
   - Result is added to the conversation history
   - Updated conversation is sent back to the LLM
5. Final LLM response is returned to the user

## Multi-Agent Composition

LiteAgent supports creating multiple agents that can interact with each other:

```python
manager = LiteAgent(model="gpt-4", name="manager")
coder = LiteAgent(model="claude-3-opus", name="coder", parent_context_id=manager.context_id)
tester = LiteAgent(model="gpt-3.5-turbo", name="tester", parent_context_id=manager.context_id)

# Manager can use child agents as tools
manager_tools = [
    coder.as_tool(name="code_writer", description="Use this to write code"),
    tester.as_tool(name="code_tester", description="Use this to test code")
]
manager.tools = manager_tools
```

### Agent-as-Tool

The `as_tool` method converts an agent into a tool that can be used by another agent:

```python
weather_agent = LiteAgent(model="gpt-3.5-turbo", name="weather_expert", 
                         tools=[get_weather])
                         
# Convert the agent to a tool
weather_tool = weather_agent.as_tool(
    name="get_detailed_weather",
    description="Get detailed weather information for a location"
)

# Use the agent-as-tool in another agent
main_agent = LiteAgent(model="gpt-4", tools=[weather_tool])
main_agent.chat("What's the weather like in Tokyo?")
```

## Observer Pattern

The observer pattern allows tracking agent behavior and integrating with external systems.

### Observer Types

- `AgentObserver`: Base abstract class for all observers
- `UnifiedObserver`: Base implementation with console, file and trace capabilities
- `ConsoleObserver`: Prints events to the console with configurable verbosity
- `FileObserver`: Logs events to a file in JSONL format
- `TreeTraceObserver`: Builds a tree visualization of agent interactions

### Usage

```python
observer = ConsoleObserver(verbose=True)
agent = LiteAgent(model="gpt-4", observers=[observer])
```

### Event Types

Events include:
- `AgentInitializedEvent`: Agent initialization with model and tools info
- `UserMessageEvent`: User message received
- `ModelRequestEvent`: Request sent to the model
- `ModelResponseEvent`: Response received from the model
- `FunctionCallEvent`: Function call with arguments
- `FunctionResultEvent`: Function result or error
- `AgentResponseEvent`: Final agent response to the user

### Tree Visualization

The `TreeTraceObserver` can visualize the tree of agent interactions:

```python
trace_observer = TreeTraceObserver()
agent = LiteAgent(model="gpt-4", observers=[trace_observer])
agent.chat("Hello")
trace_observer.print_trace()
```

## Memory Management

The `ConversationMemory` class manages conversation history, including:
- System prompts
- User messages
- Assistant messages
- Function calls and results

The memory system also tracks tool usage to detect potential loops and repetitive behaviors.

### Tool Call Tracking

The `ToolCallTracker` tracks function call patterns to:

1. Detect and prevent repeated function calls
2. Normalize function arguments for comparison
3. Identify potential loops and circular reasoning
4. Prevent excessive or unnecessary tool usage

## Model Interface System

The model interface system adapts to different LLM providers:

### Model Types

- `ModelInterface`: Base class for all model interfaces
- `FunctionCallingModel`: For models with native function calling
- `TextBasedFunctionCallingModel`: For models that need text-based function calling

### Auto-Detection

The library automatically detects the appropriate model interface and tool calling handler based on the model name using:

- `detect_model_capability`: Function that checks model capabilities
- `create_model_interface`: Factory function that creates the appropriate interface
- `create_tool_handler`: Factory function that creates the appropriate handler

## Tool Implementation

The tool system supports different tool types:

### Tool Types

- `BaseTool`: Base class for all tool implementations
- `FunctionTool`: Wraps standalone functions
- `InstanceMethodTool`: Wraps instance methods
- `StaticMethodTool`: Wraps static methods
- `AgentTool`: Wraps an agent as a tool for another agent

### Tool Registration

Tools can be registered and accessed in several ways:

```python
# Using the decorator
@liteagent_tool(name="custom_name", description="Custom description")
def my_tool(param: str) -> str:
    """Tool docstring"""
    return f"Processed {param}"

# Direct tool creation
tool = FunctionTool(my_function)

# Class method tools
class MyTools:
    @liteagent_tool
    def my_method(self, param: str) -> str:
        """Method docstring"""
        return f"Processed {param}"
```

## Project Organization

LiteAgent is organized with a clean separation of concerns:

- **Core Library**: The `liteagent/` directory contains the core framework code.
- **Examples**: The `examples/` directory contains example tools and usage patterns.
- **CLI**: The `cli/` directory contains the command-line interface.
- **Tests**: The `tests/` directory contains unit and integration tests.

This organization makes it easy to focus on the core functionality in the liteagent package while keeping examples and CLI functionality separate.

## Development Tools

The `tools/` directory contains utility scripts that are primarily used during development and testing of the LiteAgent library. These tools help with analyzing model responses, validating tool calling implementations, and testing pattern extraction capabilities.

### Tool Calling Format Detection

- **detect_tool_calling_format.py**: A command-line tool that analyzes JSON response files from LLMs to determine what style of tool calling they use (OpenAI, Anthropic, Ollama, etc.). This is useful for understanding how different models structure their tool calling responses.

  Usage: `python tools/detect_tool_calling_format.py response.json`

### Pattern Testing Utilities

- **test_pattern_handler.py**: Tests the pattern-based tool calling handler with sample responses to verify correct extraction of tool calls and formatting of results.
- **test_pattern_backend.py**: Tests the backend implementation of pattern-based tool calling.
- **batch_test_patterns.py**: Runs batch tests across multiple pattern files and response formats to verify consistency.

### Analysis Tools

- **find_similarities.py**: Analyzes tool call patterns to find similarities between different model outputs.
- **find_node.py**: Helps locate specific nodes in complex nested JSON structures from model responses.
- **call_collector.py**: Collects and analyzes tool calls across multiple model runs for pattern recognition.

These tools are particularly helpful when:
- Implementing support for new LLM providers
- Debugging issues with tool call extraction
- Comparing tool calling formats across different models
- Validating pattern extraction algorithms
- Analyzing model response structures

## Model Capabilities Registry

The `MODEL_CAPABILITIES` dictionary in `liteagent/tool_calling_types.py` maps model names to their capabilities, including:

- `tool_calling_type`: The type of tool calling supported by the model
- `supports_multiple_tools`: Whether the model supports multiple tools in a single request
- `max_tools_per_request`: The maximum number of tools that can be included in a single request

These capabilities are also stored in `model_capabilities.json` for easier maintenance, and additional utility functions for managing model capabilities are available in `liteagent/model_capabilities.py`.

## XPath Extractor

The XPath extractor provides a powerful way to extract structured data from unstructured text outputs:

- Used for text-based tool calling extraction
- Provides CSS-like selection syntax for text patterns
- Handles nested structure extraction
- Used primarily by the `TextBasedToolCallingHandler`

## Pattern-Based Tool Handling

For models without native tool calling support, LiteAgent uses pattern-based tool extraction:

1. Enhances the system prompt with structured output instructions
2. Uses regex patterns to detect tool calls in text output
3. Extracts function names and arguments
4. Normalizes arguments for the tool
5. Executes the tool and provides results

This approach allows using a wider range of models, including:
- Smaller open-source models
- Models without native function calling APIs
- Self-hosted models
- New or experimental models 