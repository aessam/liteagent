# LiteAgent Test Suite

This directory contains the test suite for the LiteAgent library. The tests are organized as follows:

## Directory Structure

- `unit/`: Unit tests for individual components
  - `test_mock_llm.py`: Tests for the mock LLM implementation
  - `test_agent.py`: Tests for the core LiteAgent class
  - `test_agent_tool.py`: Tests for the AgentTool functionality
  - `test_observer.py`: Tests for the observer functionality
  - `test_models.py`: Tests for the model interfaces

## Running Tests

To run the tests, use pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_agent.py

# Run with coverage
pytest --cov=liteagent
```

## Testing Philosophy

The tests are designed to be fast, reliable, and independent. The key testing principles include:

1. **Dependency Injection**: Using mock LLMs instead of real API calls
2. **Comprehensive Coverage**: Testing all key functions and permutations
3. **Clear Assertions**: Making test failures easy to understand

## Mock LLM Implementation

The `MockModelInterface` class in `test_mock_llm.py` provides a mock implementation of the `ModelInterface` abstract class, allowing tests to run without making real API calls. This mock can be configured to:

- Return predefined text responses
- Simulate function/tool calling
- Track calls for assertion purposes
- Simulate different model capabilities

## Testing Scenarios

The test suite covers various scenarios:

- LLM configurations (with/without function calling)
- Different types of functions/tools
- Agent-as-tool patterns
- Observability features
- Error handling
- Function call loop prevention 