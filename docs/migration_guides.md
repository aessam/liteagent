# Migration Guides

This document provides guidance on how to migrate from deprecated features to their replacements.

## Table of Contents

- [Migrating from `ToolsForAgents` to Alternative Implementations](#migrating-from-toolsforagents)
- [Migrating to Refactored Tool Calling Handlers](#migrating-to-refactored-tool-calling-handlers)
- [Understanding Tool Calling Type Enum Changes](#understanding-tool-calling-type-enum-changes)

## Migrating from `ToolsForAgents`

The `ToolsForAgents` class in the main library has been deprecated and will be removed in a future version. It has been moved to the test utilities.

### Original Usage

```python
from liteagent.tools import ToolsForAgents

tools_instance = ToolsForAgents(api_key="your-api-key")
weather = tools_instance.get_weather("New York")
```

### Recommended Approaches

#### Option 1: Use `FunctionTool` and class methods

```python
from liteagent.tools import FunctionTool

# Create a class with your tool methods
class WeatherTools:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def get_weather(self, city):
        # Implement weather lookup
        return {"temperature": 72, "condition": "sunny"}
        
# Create an instance and register its methods as tools
weather_tools = WeatherTools(api_key="your-api-key")
get_weather_tool = FunctionTool(weather_tools.get_weather)

# Use in an agent
agent = LiteAgent(
    model="gpt-4",
    tools=[get_weather_tool],
    # ... other parameters
)
```

#### Option 2: Use `BaseTool` for more control

```python
from liteagent.tools import BaseTool

class WeatherTool(BaseTool):
    def __init__(self, api_key):
        self.api_key = api_key
        
    @property
    def name(self):
        return "get_weather"
        
    @property
    def description(self):
        return "Get weather information for a city"
        
    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for"
                }
            },
            "required": ["city"]
        }
        
    def __call__(self, city):
        # Implement weather lookup
        return {"temperature": 72, "condition": "sunny"}
        
# Create and use the tool
weather_tool = WeatherTool(api_key="your-api-key")

# Use in an agent
agent = LiteAgent(
    model="gpt-4",
    tools=[weather_tool],
    # ... other parameters
)
```

## Migrating to Refactored Tool Calling Handlers

The tool calling handling has been refactored to use separate handler classes for different model providers in the `liteagent.handlers` module.

### Original Usage

```python
from liteagent.tool_calling import get_tool_calling_handler, ToolCallingType

handler = get_tool_calling_handler("gpt-4", ToolCallingType.OPENAI_FUNCTION_CALLING)
```

### New Usage

```python
from liteagent.tool_calling import get_tool_calling_handler
from liteagent.tool_calling_types import ToolCallingType

# The function signature remains the same for backward compatibility
handler = get_tool_calling_handler("gpt-4", ToolCallingType.OPENAI)
```

### Direct Handler Usage

If you need more control, you can use the handlers directly:

```python
from liteagent.handlers import OpenAIToolCallingHandler, AnthropicToolCallingHandler

# For OpenAI models
openai_handler = OpenAIToolCallingHandler()

# For Anthropic models
anthropic_handler = AnthropicToolCallingHandler()
```

## Understanding Tool Calling Type Enum Changes

The `ToolCallingType` enum has been updated with more specific types and aliases for backward compatibility.

### Original Enum Values

- `ToolCallingType.NONE`
- `ToolCallingType.OPENAI_FUNCTION_CALLING`
- `ToolCallingType.ANTHROPIC_TOOL_CALLING`
- `ToolCallingType.OLLAMA_TOOL_CALLING`
- `ToolCallingType.PROMPT_BASED`

### New Enum Values

- `ToolCallingType.NONE`
- `ToolCallingType.OPENAI` (alias: `ToolCallingType.OPENAI_FUNCTION_CALLING`)
- `ToolCallingType.ANTHROPIC` (alias: `ToolCallingType.ANTHROPIC_TOOL_CALLING`)
- `ToolCallingType.GROQ` (new)
- `ToolCallingType.OLLAMA` (alias: `ToolCallingType.OLLAMA_TOOL_CALLING`)
- `ToolCallingType.TEXT_BASED` (new)
- `ToolCallingType.STRUCTURED_OUTPUT` (alias: `ToolCallingType.PROMPT_BASED`)

The aliases ensure backward compatibility, so existing code using the old enum values will continue to work.

### Migration Example

```python
from liteagent.tool_calling_types import ToolCallingType

# Old code
handler_type = ToolCallingType.OPENAI_FUNCTION_CALLING

# New code (recommended)
handler_type = ToolCallingType.OPENAI
```

## Deprecation Timeline

| Feature | Deprecated In | Will Be Removed In | Notes |
|---------|---------------|-------------------|-------|
| `ToolsForAgents` class | 0.4.0 | 0.6.0 | Use `FunctionTool` or `BaseTool` instead |
| `ToolCallingType.OPENAI_FUNCTION_CALLING` | 0.5.0 | 0.7.0 | Use `ToolCallingType.OPENAI` instead |
| `ToolCallingType.ANTHROPIC_TOOL_CALLING` | 0.5.0 | 0.7.0 | Use `ToolCallingType.ANTHROPIC` instead |
| `ToolCallingType.OLLAMA_TOOL_CALLING` | 0.5.0 | 0.7.0 | Use `ToolCallingType.OLLAMA` instead |
| `ToolCallingType.PROMPT_BASED` | 0.5.0 | 0.7.0 | Use `ToolCallingType.STRUCTURED_OUTPUT` instead | 