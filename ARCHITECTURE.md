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

### Tool Calling Handlers

The `ToolCallingHandler` class hierarchy in `liteagent/tool_calling.py` provides implementations for different tool calling types:

- `OpenAIToolCallingHandler`: For OpenAI-compatible function calling
- `AnthropicToolCallingHandler`: For Anthropic-style tool calling
- `OllamaToolCallingHandler`: For JSON extraction from Ollama and similar models
- `TextBasedToolCallingHandler`: For prompt-based tool calling
- `NoopToolCallingHandler`: For models that don't support tool calling

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

## Testing Architecture

The testing system is organized by capability rather than by model:

### Capability-Based Tests

Tests are organized in the `tests/integration/capabilities` directory:

- `test_standalone_tools.py`: Tests for standalone function tools
- `test_class_method_tools.py`: Tests for class method tools
- `test_multi_step.py`: Tests for multi-step reasoning with multiple tools
- `test_json_extraction.py`: Tests for extracting structured JSON data
- `test_prompt_based.py`: Tests for models that use prompt-based tool calling

### Test Fixtures

The `conftest.py` file in `tests/integration/capabilities` provides fixtures for tests:

- `validation_observer`: A fixture that provides a `ValidationObserver` instance

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