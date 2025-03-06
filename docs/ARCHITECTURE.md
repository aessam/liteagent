# LiteAgent Architecture

This document outlines the architecture of the LiteAgent framework, focusing on the tool calling system and validation strategies.

## Tool Calling Architecture

The tool calling system is designed to support multiple LLM providers with different tool calling mechanisms:

### Tool Calling Types

The `ToolCallingType` enum in `liteagent/tool_calling_types.py` defines the different types of tool calling supported:

- `NONE`: No tool calling support
- `OPENAI_FUNCTION_CALLING`: OpenAI-style function calling (includes Groq and compatible models)
- `ANTHROPIC_TOOL_CALLING`: Anthropic-style tool calling
- `JSON_EXTRACTION`: Generic JSON output parsing (for models like Ollama that use text-based approaches)
- `PROMPT_BASED`: Handles models that need specific prompting to return structured outputs

### Model Capabilities Registry

The `MODEL_CAPABILITIES` dictionary in `liteagent/tool_calling_types.py` maps model names to their capabilities, including:

- `tool_calling_type`: The type of tool calling supported by the model
- `supports_multiple_tools`: Whether the model supports multiple tools in a single request
- `max_tools_per_request`: The maximum number of tools that can be included in a single request

These capabilities are also stored in `model_capabilities.json` for easier maintenance, and additional utility functions for managing model capabilities are available in `liteagent/model_capabilities.py`.

### Tool Calling Handlers

The `ToolCallingHandler` class hierarchy in `liteagent/tool_calling.py` provides implementations for different tool calling types:

- `OpenAIToolCallingHandler`: For OpenAI-compatible function calling
- `AnthropicToolCallingHandler`: For Anthropic-style tool calling
- `OllamaToolCallingHandler`: For JSON extraction from Ollama and similar models
- `TextBasedToolCallingHandler`: For prompt-based tool calling
- `NoopToolCallingHandler`: For models that don't support tool calling

## Agent Architecture

The agent architecture is built around the core `LiteAgent` class:

### Core Agent Components

- `LiteAgent`: The main agent class that handles conversation flow, tool calling, and memory management
- `Memory`: Manages conversation history and token tracking
- `AgentTool`: Wraps standalone tools or class methods as tools for agent use

### Multi-Agent Support

The framework supports creating hierarchies of agents that can communicate:

- Parent agents can delegate tasks to child agents
- Context can be propagated from parent to child
- Specialized agents can handle specific tools or tasks
- Agent routing allows distribution of tasks based on capabilities

## Validation Architecture

The validation system is designed to validate agent behavior in tests:

### Validation Strategies

The `ToolValidationStrategy` class hierarchy in `liteagent/validation_strategies.py` provides implementations for different validation strategies:

- `OpenAIValidationStrategy`: For validating OpenAI-compatible function calling
- `AnthropicValidationStrategy`: For validating Anthropic-style tool calling
- `JSONExtractionStrategy`: For validating JSON extraction
- `PromptBasedStrategy`: For validating prompt-based tool calling

### Validation Observer

The `ValidationObserver` class in `tests/integration/validation_observer.py` provides a way to observe and validate agent behavior:

- Records function calls, results, and responses
- Validates function calls and results
- Parses responses based on expected formats
- Supports different validation strategies

### Validation Helper

The `ValidationTestHelper` class in `tests/utils/validation_helper.py` provides helper functions for validation in tests:

- Checks if API keys are available for models
- Generates system prompts for tools
- Registers appropriate parsers for tools
- Provides parsing functions for different tools
- Validates tool usage

## Observer System

The observer system provides event monitoring and validation throughout the agent lifecycle:

### Observer Types

- `Observer`: Base class for all observers
- `TreeTraceObserver`: Creates a tree visualization of agent interactions
- `ValidationObserver`: Validates agent behavior in tests
- `SequenceValidationObserver`: Validates sequences of function calls

### Observable Events

- `AgentInitializedEvent`: When an agent is initialized
- `UserMessageEvent`: When a user message is received
- `ModelRequestEvent`: When a request is sent to the model
- `ModelResponseEvent`: When a response is received from the model
- `FunctionCallEvent`: When a function is called
- `FunctionResultEvent`: When a function returns a result
- `AgentResponseEvent`: When the agent generates a response

## Testing Architecture

The testing system is organized by capability and supports multiple model types:

### Integration Tests

Tests are organized in two main directories:

1. `tests/integration/capabilities/`: Original capability-based tests specific to model types
   - Tests focused on individual model capabilities and behaviors

2. `tests/integration/consolidated/`: Refactored tests that work across model types
   - `test_standalone_tools.py`: Tests for standalone function tools across model types
   - `test_class_method_tools.py`: Tests for class method tools across model types
   - `test_multi_step_reasoning.py`: Tests for multi-step reasoning with multiple tools
   - `test_multi_agent.py`: Tests for multi-agent communication and routing
   - `test_validation.py`: Tests for validation patterns and assertions

Additional integration tests include:
- `test_model_comparison.py`: Direct comparison of different model capabilities

### Feature Coverage Matrix

A comprehensive test-to-feature mapping matrix is maintained in `tests/TEST_FEATURE_MATRIX.md` and shows:

- Feature intersections and their test coverage
- Model type support for different tool capabilities
- Critical feature combinations and coverage gaps
- Unit and integration test coverage for each component

### Model Support Testing

The framework tests different models with varying capabilities:

- **OpenAI-compatible models**: Tested with native function calling
- **Anthropic models**: Tested with Anthropic's tool calling format
- **Text-based models**: Tested with JSON extraction approaches
- **Mock models**: Used for unit testing without API calls

## Usage

To use the LiteAgent framework:

1. Create an agent with tools:

```python
from liteagent import LiteAgent
from liteagent.tools import get_weather, add_numbers

agent = LiteAgent(
    model="gpt-4o-mini",
    name="WeatherAgent",
    system_prompt="You are a helpful assistant that can check the weather and perform calculations.",
    tools=[get_weather, add_numbers]
)

response = agent.chat("What's the weather like in Tokyo and what is 25 plus 17?")
```

2. Use the validation observer for testing:

```python
from liteagent import LiteAgent
from liteagent.tools import get_weather
from tests.integration.validation_observer import ValidationObserver

# Create a validation observer
observer = ValidationObserver()

# Create an agent with the observer
agent = LiteAgent(
    model="gpt-4o-mini",
    tools=[get_weather],
    observers=[observer]
)

# Chat with the agent
response = agent.chat("What's the weather like in Tokyo?")

# Validate function calls
observer.assert_function_called("get_weather")
observer.assert_function_called_with("get_weather", city="Tokyo")

# Get function results
weather_result = observer.get_last_function_result("get_weather")
print(weather_result)
```

3. Create a multi-agent system:

```python
from liteagent import LiteAgent
from liteagent.tools import get_weather, add_numbers

# Create specialized agents
weather_agent = LiteAgent(
    model="gpt-4o-mini",
    name="WeatherAgent",
    system_prompt="You are a weather expert.",
    tools=[get_weather]
)

calculator_agent = LiteAgent(
    model="gpt-3.5-turbo",
    name="CalculatorAgent",
    system_prompt="You are a math expert.",
    tools=[add_numbers]
)

# Create a routing agent
router_agent = LiteAgent(
    model="gpt-4o-mini",
    name="RouterAgent",
    system_prompt="You are a router that delegates tasks to specialized agents.",
    tools=[
        weather_agent.as_tool(description="Get weather information"),
        calculator_agent.as_tool(description="Perform calculations")
    ]
)

# Chat with the router agent
response = router_agent.chat("What's the weather in Tokyo and what is 25 + 17?")
``` 