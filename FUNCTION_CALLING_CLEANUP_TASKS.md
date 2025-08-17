# Function Calling Implementation Cleanup Tasks

## Overview
The current implementation over-relies on pattern matching and structured output handling instead of utilizing native function calling APIs provided by each LLM provider. This document outlines the comprehensive cleanup and correction tasks needed to properly implement function calling for each provider.

## Current Issues

### 1. Routing Problem
- Most function calls are being routed through `structured_output_handler.py` instead of using native APIs
- The `pattern_tool_handler.py` is being used as a fallback even for providers with native support
- Excessive regex pattern matching and text parsing instead of using proper API formats

### 2. Provider Implementation Issues
- Handlers contain excessive mock object handling and test-specific code
- Mixed approaches trying to handle both native and text-based formats
- Incorrect parameter formats being passed to provider APIs
- Not utilizing 2025 API updates and features

## Provider-Specific Tasks

### OpenAI Handler (`liteagent/handlers/openai_handler.py`)

#### Current Issues:
- Contains mock object handling logic mixed with production code
- Falls back to pattern-based extraction unnecessarily
- Not properly utilizing OpenAI's native tool calling format

#### Required Changes:
```python
# CORRECT FORMAT:
{
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "function_name",
                "description": "Function description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string", "description": "Parameter description"}
                    },
                    "required": ["param1"]
                }
            }
        }
    ],
    "tool_choice": "auto",  # or "none", "required", or specific function
    "parallel_tool_calls": true  # Enable parallel execution
}

# Tool result format:
{
    "role": "tool",
    "tool_call_id": "call_xyz123",
    "content": "result_content"
}
```

#### Tasks:
- [ ] Remove mock object handling from production code
- [ ] Implement proper tool extraction from `response.choices[0].message.tool_calls`
- [ ] Remove pattern-based fallback logic
- [ ] Ensure proper `tool_choice` parameter support
- [ ] Add support for `parallel_tool_calls` parameter
- [ ] Validate tool result formatting with correct `tool_call_id`

### Anthropic Handler (`liteagent/handlers/anthropic_handler.py`)

#### Current Issues:
- Converting parameters to wrong format
- Not utilizing Anthropic's native tool format properly
- Missing support for 2025 features like parallel tool calling

#### Required Changes:
```python
# CORRECT FORMAT:
{
    "tools": [
        {
            "name": "function_name",
            "description": "Function description",
            "input_schema": {
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "Parameter description"}
                },
                "required": ["param1"]
            }
        }
    ]
}

# Tool use block in response:
{
    "type": "tool_use",
    "id": "toolu_xyz123",
    "name": "function_name",
    "input": {"param1": "value"}
}

# Tool result format:
{
    "type": "tool_result",
    "tool_use_id": "toolu_xyz123",
    "content": "result_content"
}
```

#### Tasks:
- [ ] Remove OpenAI format conversion logic
- [ ] Implement proper `input_schema` formatting
- [ ] Add support for parallel tool calling (2025 feature)
- [ ] Implement fine-grained streaming support for Sonnet 4 and Opus 4
- [ ] Fix tool result formatting with `tool_use_id`
- [ ] Remove unnecessary compatibility layers

### Groq Handler (`liteagent/handlers/groq_handler.py`)

#### Current Issues:
- Correctly uses OpenAI format but missing some features
- Not handling the 128 tool limit properly
- Missing parallel tool calling support

#### Required Changes:
```python
# CORRECT FORMAT (OpenAI-compatible):
{
    "tools": [...],  # OpenAI format
    "tool_choice": "auto",
    "parallel_tool_calls": true,
    "max_tools": 128  # Groq-specific limit
}
```

#### Tasks:
- [ ] Add validation for 128 tool maximum
- [ ] Implement `parallel_tool_calls` parameter support
- [ ] Add proper error handling for tool limits
- [ ] Ensure full OpenAI compatibility
- [ ] Add support for Llama-3-Groq-Tool-Use models

### Ollama Handler (`liteagent/handlers/ollama_handler.py`)

#### Current Issues:
- Excessive regex pattern matching (250+ lines of parsing code)
- Not using native Ollama tool format
- Hardcoded test values mixed with production code
- System prompt injection instead of proper tool parameter

#### Required Changes:
```python
# CORRECT FORMAT:
{
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "function_name",
                "description": "Function description",
                "parameters": {
                    "type": "object",
                    "properties": {...},
                    "required": [...]
                }
            }
        }
    ]
}

# Response format:
{
    "message": {
        "tool_calls": [
            {
                "function": {
                    "name": "function_name",
                    "arguments": {"param1": "value"}
                }
            }
        ]
    }
}
```

#### Tasks:
- [ ] Remove all regex pattern matching code
- [ ] Implement native Ollama tool format usage
- [ ] Remove hardcoded test values
- [ ] Add streaming tool response support
- [ ] Simplify to under 100 lines of code
- [ ] Remove text-based function call detection

### Structured Output Handler (`liteagent/handlers/structured_output_handler.py`)

#### Current Issues:
- Being used for providers that have native support
- Contains hardcoded test cases
- Complex JSON extraction logic

#### Required Changes:
- Should ONLY be used for models without native function calling
- Simplify JSON extraction
- Remove test-specific code

#### Tasks:
- [ ] Remove hardcoded test cases (lines 119-129)
- [ ] Simplify JSON extraction patterns
- [ ] Add clear documentation on when to use this handler
- [ ] Reduce complexity of regex patterns
- [ ] Only use for legacy models without native support

## Core System Tasks

### 1. Update `models.py`

#### Tasks:
- [ ] Pass tools directly to LiteLLM without modification
- [ ] Remove system prompt injection for tool descriptions (lines 70-81)
- [ ] Let LiteLLM handle provider-specific formatting
- [ ] Add proper tool parameter validation
- [ ] Implement provider-specific parameter passing

### 2. Update `tool_calling.py`

#### Tasks:
- [ ] Simplify handler selection logic
- [ ] Remove fallback to pattern matching for native providers
- [ ] Add proper provider detection
- [ ] Implement handler caching
- [ ] Add validation for tool formats

### 3. Update `pattern_tool_handler.py`

#### Tasks:
- [ ] Should only be base class, not used directly
- [ ] Remove XPath extraction complexity
- [ ] Simplify to common functionality only
- [ ] Move provider-specific logic to respective handlers
- [ ] Reduce code duplication

### 4. Update `model_capabilities.json`

#### Tasks:
- [ ] Add 2025 feature flags (parallel tools, streaming, etc.)
- [ ] Update max tool limits per provider
- [ ] Add model-specific overrides for new models
- [ ] Document capability detection logic
- [ ] Add version compatibility information

### 5. Create Provider Integration Tests

#### Tasks:
- [ ] Create `tests/integration/providers/` directory
- [ ] Add test suite for each provider:
  - [ ] `test_openai_function_calling.py`
  - [ ] `test_anthropic_tool_use.py`
  - [ ] `test_groq_tools.py`
  - [ ] `test_ollama_tools.py`
- [ ] Test actual API responses (not mocks)
- [ ] Validate format compliance
- [ ] Test parallel tool calling where supported
- [ ] Test error handling and edge cases

## Implementation Order

### Phase 1: Core Cleanup (Priority: High)
1. Update `models.py` to pass tools directly to LiteLLM
2. Simplify `pattern_tool_handler.py` to base functionality only
3. Update `model_capabilities.json` with accurate information

### Phase 2: Provider Updates (Priority: High)
1. Fix OpenAI handler - remove mocks, use native format
2. Fix Anthropic handler - proper input_schema, parallel tools
3. Fix Groq handler - add missing features
4. Simplify Ollama handler - remove regex, use native format

### Phase 3: Testing & Validation (Priority: Medium)
1. Create provider-specific integration tests
2. Remove test code from production handlers
3. Validate all providers with real API calls
4. Document provider-specific requirements

### Phase 4: Optimization (Priority: Low)
1. Add handler caching
2. Implement streaming where supported
3. Add performance monitoring
4. Optimize for parallel tool execution

## Success Criteria

1. **Code Reduction**: Each handler should be under 150 lines of code
2. **Native API Usage**: All providers use their native function calling format
3. **No Pattern Matching**: Providers with native support don't use regex
4. **Clean Separation**: Test code separated from production code
5. **Proper Documentation**: Each handler documents its format clearly
6. **Integration Tests**: Each provider has comprehensive test coverage
7. **Performance**: Function calling latency reduced by 30%
8. **Reliability**: Error rate reduced by 50%

## Testing Checklist

For each provider, verify:
- [ ] Tools are formatted correctly for the provider's API
- [ ] Tool calls are extracted without pattern matching
- [ ] Tool results are formatted properly
- [ ] Parallel tool calling works (where supported)
- [ ] Error handling is robust
- [ ] No test code in production handlers
- [ ] Integration tests pass with real API calls

## Documentation Updates Needed

1. Update `docs/api_reference.md` with correct formats
2. Create provider-specific guides in `docs/providers/`
3. Update quickstart guide with function calling examples
4. Document migration path from current implementation
5. Add troubleshooting guide for common issues

## Estimated Timeline

- Phase 1: 2-3 days
- Phase 2: 4-5 days  
- Phase 3: 3-4 days
- Phase 4: 2-3 days

**Total: 11-15 days**

## Notes

- This cleanup will significantly improve reliability and performance
- Reduces code complexity and maintenance burden
- Enables proper utilization of 2025 API features
- Makes the codebase more maintainable and testable
- Aligns with provider best practices and recommendations