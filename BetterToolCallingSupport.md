# Improving Tool Calling Support in LiteAgent

This document outlines our approach to improving tool calling support in the LiteAgent framework, making it more robust and maintainable.

## Current Challenges

- Complex, brittle code for detecting function calling capabilities
- Hardcoded model detection and handling
- Difficult to maintain and extend as new models are released
- Multiple code paths for different models
- Text-based function calling with regex patterns is error-prone

## Response Format Analysis

After analyzing sample responses from different providers, we identified these key patterns:

### OpenAI Format

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_zUWYWcHrFG0TZlYhm8bbDC0u",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\":\"San Francisco, CA\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### Anthropic Format

```json
{
  "role": "assistant",
  "content": [
    {"type": "text", "text": "..."},
    {
      "type": "tool_use",
      "id": "toolu_01Nx9gRcpkgP64tVVwTCiDts",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    }
  ],
  "stop_reason": "tool_use"
}
```

### Groq Format (OpenAI-compatible)

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "tool_calls": [
          {
            "id": "call_bqc2",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"location\":\"San Francisco\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### Ollama Format

```json
{
  "message": {
    "role": "assistant",
    "content": "",
    "tool_calls": [
      {
        "function": {
          "name": "get_weather",
          "arguments": {"location": "San Francisco"}
        }
      }
    ]
  }
}
```

## Proposed Solution

### 1. Tool Calling Types

Define clear types for different function calling approaches:

```python
class ToolCallingType(Enum):
    OPENAI = auto()           # OpenAI style with tool_calls array
    ANTHROPIC = auto()        # Anthropic style with content array and tool_use
    OLLAMA = auto()           # Ollama style arguments
    STRUCTURED_OUTPUT = auto() # Models that can reliably output JSON/structured data when prompted
    TEXT_BASED = auto()       # Fallback text-based extraction for less predictable outputs
    NONE = auto()             # No function calling support
```

### 2. Configuration-Driven Approach

Use a JSON configuration file to map models and providers to their tool calling types:

```json
{
  "providers": {
    "openai": {
      "tool_calling_type": "OPENAI",
      "models": {
        "default": "OPENAI",
        "gpt-3.5-turbo": "OPENAI",
        "gpt-4": "OPENAI"
      }
    },
    "anthropic": {
      "tool_calling_type": "ANTHROPIC",
      "models": {
        "default": "ANTHROPIC",
        "claude-3-opus": "ANTHROPIC",
        "claude-3-sonnet": "ANTHROPIC",
        "claude-3-haiku": "ANTHROPIC"
      }
    },
    "groq": {
      "tool_calling_type": "OPENAI",
      "models": {
        "default": "OPENAI"
      }
    },
    "ollama": {
      "tool_calling_type": "OLLAMA",
      "models": {
        "default": "OLLAMA"
      }
    },
    "mistral": {
      "tool_calling_type": "STRUCTURED_OUTPUT",
      "models": {
        "default": "STRUCTURED_OUTPUT"
      }
    },
    "huggingface": {
      "tool_calling_type": "TEXT_BASED",
      "models": {
        "default": "TEXT_BASED"
      }
    }
  }
}
```

### 3. Tool Calling Handler Interface

Create a handler interface for each tool calling type:

```python
class ToolCallingHandler(ABC):
    @abstractmethod
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from the model's response"""
        pass
        
    @abstractmethod
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """Format tools in the way the model expects"""
        pass
        
    @abstractmethod
    def format_tool_results(self, tool_name: str, result: Any) -> Dict:
        """Format tool execution results for the model"""
        pass
```

### 4. Implementations of Handlers

#### OpenAI Tool Calling Handler

```python
class OpenAIToolCallingHandler(ToolCallingHandler):
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        if not hasattr(response, "choices") or not response.choices:
            return []
            
        message = response.choices[0].message
        if not hasattr(message, "tool_calls") or not message.tool_calls:
            return []
            
        tool_calls = []
        for tool_call in message.tool_calls:
            if tool_call.type == "function":
                function_call = tool_call.function
                try:
                    arguments = json.loads(function_call.arguments)
                except json.JSONDecodeError:
                    arguments = {}
                    
                tool_calls.append({
                    "name": function_call.name,
                    "arguments": arguments,
                    "id": tool_call.id
                })
                
        return tool_calls
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        # Convert tools to OpenAI format if needed
        return tools
        
    def format_tool_results(self, tool_name: str, result: Any, tool_call_id: str = None) -> Dict:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": json.dumps(result) if not isinstance(result, str) else result
        }
```

#### Anthropic Tool Calling Handler

```python
class AnthropicToolCallingHandler(ToolCallingHandler):
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        if not hasattr(response, "content") or not isinstance(response.content, list):
            return []
            
        tool_calls = []
        for content_item in response.content:
            if hasattr(content_item, "type") and content_item.type == "tool_use":
                tool_calls.append({
                    "name": content_item.name,
                    "arguments": content_item.input,
                    "id": content_item.id
                })
                
        return tool_calls
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        # Convert tools to Anthropic format
        anthropic_tools = []
        for tool in tools:
            anthropic_tools.append({
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("parameters", {})
            })
        return anthropic_tools
        
    def format_tool_results(self, tool_name: str, result: Any, tool_id: str = None) -> Dict:
        return {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": json.dumps(result) if not isinstance(result, str) else result
                }
            ]
        }
```

#### Structured Output Handler

```python
class StructuredOutputHandler(ToolCallingHandler):
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        # Extract the content
        content = self._extract_content(response)
        if not content:
            return []
            
        # Try to parse content as JSON
        try:
            data = json.loads(content)
            # Look for a function call structure
            if "function" in data and "name" in data["function"]:
                return [{
                    "name": data["function"]["name"],
                    "arguments": data["function"]["arguments"],
                    "id": data.get("id", str(uuid.uuid4()))
                }]
        except (json.JSONDecodeError, AttributeError, TypeError):
            pass
            
        return []
        
    def format_tools_for_model(self, tools: List[Dict]) -> str:
        # Format tools as a schema description in the system prompt
        tool_descriptions = []
        for tool in tools:
            params = tool.get("parameters", {}).get("properties", {})
            param_desc = "\n".join([f"  - {name}: {details.get('type', 'any')} - {details.get('description', '')}" 
                                   for name, details in params.items()])
            
            tool_descriptions.append(f"""
Function: {tool['name']}
Description: {tool.get('description', '')}
Parameters:
{param_desc}
            """)
        
        return "\n".join(tool_descriptions)
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        # For structured output, we just format as user message with the result
        return {
            "role": "user",
            "content": f"The result of calling {tool_name} is: {json.dumps(result)}"
        }
        
    def _extract_content(self, response: Any) -> str:
        # Extract content from various response formats
        # (Implementation details)
        return ""
```

### 5. Factory Method

```python
def get_tool_calling_handler(model_name: str) -> ToolCallingHandler:
    """Get the appropriate tool calling handler for the model"""
    # Use the config to determine the handler type
    tool_calling_type = get_tool_calling_type_from_config(model_name)
    
    if tool_calling_type == ToolCallingType.OPENAI:
        return OpenAIToolCallingHandler()
    elif tool_calling_type == ToolCallingType.ANTHROPIC:
        return AnthropicToolCallingHandler()
    elif tool_calling_type == ToolCallingType.OLLAMA:
        return OllamaToolCallingHandler()
    elif tool_calling_type == ToolCallingType.STRUCTURED_OUTPUT:
        return StructuredOutputHandler()
    elif tool_calling_type == ToolCallingType.TEXT_BASED:
        return TextBasedToolCallingHandler()
    else:
        return NoopToolCallingHandler()
```

### 6. Simplified ModelInterface

```python
class ModelInterface(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tool_handler = get_tool_calling_handler(model_name)
    
    def generate_response(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Any:
        """Generate a response from the model"""
        # Format tools appropriately for this model
        formatted_tools = self.tool_handler.format_tools_for_model(tools) if tools else None
        
        # Make the API call
        response = self._call_api(messages, formatted_tools)
        return response
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from the response"""
        return self.tool_handler.extract_tool_calls(response)
        
    @abstractmethod
    def _call_api(self, messages: List[Dict], tools: Any = None) -> Any:
        """Make the actual API call to the model provider"""
        pass
```

## Implementation Roadmap

1. Create the `ToolCallingType` enum and handler interface
2. Implement the model configuration JSON file
3. Create handler implementations for each tool calling type
4. Update the `ModelInterface` class to use handlers
5. Write tests for each handler using sample responses
6. Update the agent to use the new tool calling system

## Benefits of This Approach

- **Separation of Concerns**: Each handler focuses on one type of tool calling
- **Extensibility**: Easy to add support for new models by updating the configuration
- **Maintainability**: Clearer code with less complexity
- **Testability**: Each handler can be tested independently
- **Configuration-Driven**: No code changes needed for most new models

## Test-Driven Approach

For each handler, we'll write tests using the sample responses to ensure correct extraction and formatting. Example test structure:

```python
def test_openai_handler_extraction():
    # Load sample response
    with open("tool_calling_data/response_openai_gpt-4o.json", "r") as f:
        sample = json.load(f)
    
    # Create handler and extract tool calls
    handler = OpenAIToolCallingHandler()
    tool_calls = handler.extract_tool_calls(sample)
    
    # Verify extraction
    assert len(tool_calls) == 1
    assert tool_calls[0]["name"] == "get_weather"
    assert tool_calls[0]["arguments"]["location"] == "San Francisco, CA"
``` 