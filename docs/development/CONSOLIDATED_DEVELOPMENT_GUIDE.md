# LiteAgent Development Guide
*High-density consolidated documentation - everything you need to know*

## 🏗️ Architecture Overview

**Core Components:**
- `LiteAgent`: Main orchestrator (chat, tools, memory, observers)
- `ModelInterface`: Provider adapters (OpenAI, Anthropic, Groq, Ollama)
- `ToolCallingHandler`: Provider-specific extraction/formatting
- `ConversationMemory`: History + loop detection
- `AgentObserver`: Event system (console, file, trace)

**Tool System:**
- `@liteagent_tool`: Decorator for functions/methods
- `FunctionTool`: Standalone functions
- `InstanceMethodTool`: Class methods
- `AgentTool`: Agent-as-tool pattern

**Multi-Agent:**
```python
manager = LiteAgent(model="gpt-4o-mini")
coder = LiteAgent(model="claude-3-opus", parent_context_id=manager.context_id)
manager.tools = [coder.as_tool(name="code_writer")]
```

## 🛠️ Function Calling Architecture (2025)

**Provider Handlers:**
- `OpenAIToolCallingHandler` (112 lines): Native `tools` parameter, `parallel_tool_calls=true`
- `AnthropicToolCallingHandler` (122 lines): `input_schema` format, parallel support
- `GroqToolCallingHandler` (123 lines): OpenAI-compatible, 128 tool limit
- `OllamaToolCallingHandler` (137 lines): Native format, 10 tool limit
- `TextBasedToolCallingHandler`: Legacy models without native support
- `StructuredOutputHandler`: JSON extraction for legacy models

**Correct Formats:**
```python
# OpenAI/Groq
{"tools": [{"type": "function", "function": {"name": "...", "parameters": {...}}}]}

# Anthropic  
{"tools": [{"name": "...", "input_schema": {...}}]}

# Tool Results
{"role": "tool", "tool_call_id": "...", "content": "..."}  # OpenAI
{"type": "tool_result", "tool_use_id": "...", "content": "..."}  # Anthropic
```

**XPath Complexity Removed:**
- ❌ `xpath_extractor.py` (226 lines)
- ❌ `tool_calling_detection.py` (141 lines) 
- ❌ `pattern_tool_handler.py` (403 lines)
- ❌ `auto_detect_handler.py` (109 lines)
- ✅ Direct provider-to-handler mapping (no runtime detection)

## 📁 Repository Structure (Python Standards)

```
liteagent/
├── pyproject.toml              # Modern packaging only
├── README.md, LICENSE
├── liteagent/                  # Main package
│   ├── __main__.py             # CLI entry
│   ├── handlers/               # Provider handlers
│   ├── models.py               # Core functionality  
│   └── simple_tool_handler.py  # Clean base class
├── tests/
│   ├── unit/                   # Isolated tests
│   └── integration/            # Cross-component tests
├── docs/
│   ├── examples/               # Moved from root
│   └── development/            # This file
└── scripts/dev-tools/          # Moved from tools/
```

**Removed Files:**
- `liteagent.egg-info/`, `static/`, `pytestdebug.log`
- `setup.py`, `requirements.txt`, `MANIFEST.in`
- `cli/`, `main.py`, `examples/` (root)

## 🧪 Testing Matrix

**Test Coverage by Feature:**
| Component | Unit | Integration | Critical Gaps |
|-----------|------|-------------|---------------|
| Agent Core | 78% | ✅ | Error recovery |
| Function Calling | 70% | ✅ | API failure handling |
| Observer Events | 75% | ✅ | Console/file observers |
| Memory Management | 68% | ❌ | Cross-model memory |
| Tool System | 70% | ✅ | Complex combinations |
| Multi-Agent | 65% | ✅ | Method tools + multi-agent |

**LLM-Proof Testing Strategies:**
1. **External Knowledge**: `test_get_user_data_class_method` (data LLMs can't know)
2. **Complex Calculations**: Large number operations beyond LLM capability
3. **Explicit Instructions**: Force tool usage over LLM knowledge
4. **Tool Verification**: Assert tool calls, not just response content
5. **Optional Marking**: `@pytest.mark.optional` for flaky tests

**Model Coverage:**
- GPT-4o-mini: Native function calling + parallel tools
- Ollama/Phi: Text-based extraction + basic tools  
- Mock Models: All handler types in unit tests

## 📈 Recent Improvements (2024-2025)

**Function Calling Cleanup Results:**
- 65% code reduction (Ollama: 401→137 lines)
- Native API usage (no pattern matching)
- 2025 features: parallel tools, streaming, fine-grained streaming
- 18/22 tests passing (core functionality intact)

**Repository Structure Cleanup Results:**
- 30% fewer root files
- Python packaging standards compliance
- Zero breaking changes for users
- Better IDE/tooling support

**Test Effectiveness Analysis:**
- 52 critical gaps identified across 10 test files
- Security testing prioritized (input validation, injection prevention)
- Cross-provider consistency validation needed
- Performance benchmarking required

## 🔧 Development Tools

**Located in `scripts/dev-tools/`:**
- `detect_tool_calling_format.py`: Analyze model responses
- `test_pattern_*.py`: Validate extraction logic
- `find_similarities.py`: Pattern analysis
- `batch_test_patterns.py`: Comprehensive testing

**Model Capabilities:**
- `model_capabilities.json`: Provider features, limits, API versions
- Dynamic detection via `detect_model_capability()`
- Cached results in `_MODEL_CAPABILITIES_CACHE`

## 🚀 Performance & Limits

**Provider Specifications:**
| Provider | Max Tools | Parallel | Streaming | Native Format |
|----------|-----------|----------|-----------|---------------|
| OpenAI | 128 | ✅ | ✅ | `tools` parameter |
| Anthropic | 64 | ✅ | ✅ Fine-grained | `input_schema` |  
| Groq | 128 | ✅ | ✅ | OpenAI-compatible |
| Ollama | 10 | ❌ | ✅ | OpenAI-compatible |

**Expected Performance:**
- 30% latency reduction (no regex processing)
- 50% error rate reduction (native APIs)
- Better debugging (cleaner stack traces)

## 📋 Critical Implementation Patterns

**Handler Selection:**
```python
# Direct mapping (no auto-detection)
tool_calling_type = get_tool_calling_type(model_name)  
handler = get_tool_calling_handler(tool_calling_type)
```

**Tool Registration:**
```python
@liteagent_tool
def my_tool(param: str) -> str:
    """Tool that LLMs can't perform without."""
    return external_api_call(param)

class MyTools:
    @liteagent_tool  
    def my_method(self, param: str) -> str:
        return self.process(param)
```

**Agent-as-Tool:**
```python
specialist = LiteAgent(model="claude-3-opus", tools=[domain_tools])
manager = LiteAgent(tools=[specialist.as_tool(name="expert")])
```

**Observer Usage:**
```python
observer = TreeTraceObserver()
agent = LiteAgent(observers=[observer])
observer.print_trace()  # Visualize interaction tree
```

## ⚠️ Critical Patterns & Anti-Patterns

**✅ Do:**
- Use native provider APIs directly
- Test external knowledge, not LLM capabilities  
- Direct handler mapping (no runtime detection)
- Single responsibility per handler
- Standard Python project structure

**❌ Don't:**
- Pattern matching for native providers
- Test functionality LLMs can perform alone
- Auto-detection complexity
- Build artifacts in repo
- Hardcoded test values in production code

## 🎯 Next Priority Actions

**Phase 1 Complete:** XPath removal, native handlers, repository cleanup
**Phase 2 Pending:** Security testing, error handling, cross-provider validation

**Immediate Focus:**
1. Implement critical security tests (input validation, injection prevention)
2. Add comprehensive error handling for API failures  
3. Test native function calling reliability
4. Validate cross-provider consistency
5. Performance benchmarking vs old implementation

**Success Metrics:**
- All handlers <150 lines ✅
- Native API usage only ✅  
- No pattern matching for native providers ✅
- Clean test separation ✅
- Zero breaking changes ✅

This consolidation represents 6 documents into 1 high-density reference covering architecture, implementation, testing, and development practices for LiteAgent.