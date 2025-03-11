# LiteAgent Development Tools

This directory contains utility scripts and tools to help with the development, testing, and analysis of the LiteAgent library, particularly focused on tool calling functionality.

## Tool Calling Format Detection

### detect_tool_calling_format.py

A command-line tool to analyze JSON response files from LLMs and determine what style of tool calling they use (OpenAI, Anthropic, Ollama, etc.).

```bash
# Example usage
python detect_tool_calling_format.py path/to/response.json
```

## Pattern Testing Utilities

### test_pattern_handler.py

Tests the pattern-based tool calling handler with sample responses to verify correct extraction of tool calls and formatting of results.

```bash
# Example usage
python test_pattern_handler.py path/to/sample_response.json
```

### test_pattern_backend.py

Tests the backend implementation of pattern-based tool calling with various input formats.

```bash
# Example usage
python test_pattern_backend.py path/to/test_pattern.json
```

### batch_test_patterns.py

Runs batch tests across multiple pattern files and response formats to verify consistency.

```bash
# Example usage
python batch_test_patterns.py --dir path/to/pattern/directory
```

## Analysis Tools

### find_similarities.py

Analyzes tool call patterns to find similarities between different model outputs, which is useful for identifying common patterns across providers.

```bash
# Example usage
python find_similarities.py path/to/responses/dir
```

### find_node.py

Helps locate specific nodes in complex nested JSON structures from model responses.

```bash
# Example usage
python find_node.py path/to/response.json "path.to.node"
```

### call_collector.py

Collects and analyzes tool calls across multiple model runs for pattern recognition and comparison.

```bash
# Example usage
python call_collector.py --model gpt-4 --output calls.json
```

## Testing Scripts

### test_tool_call.sh

A shell script for quickly testing tool calling functionality with different models and inputs.

```bash
# Example usage
bash test_tool_call.sh gpt-4 "Tell me the weather in Paris"
```

## Using These Tools During Development

These tools are particularly helpful in the following scenarios:

1. **Adding Support for New Models**: When implementing support for a new LLM provider, use these tools to analyze their response formats and test your implementation.

2. **Debugging Tool Calling Issues**: When tool calling isn't working correctly, use these tools to analyze the response structure and identify problems.

3. **Performance Analysis**: Analyze how different models handle tool calling and identify potential optimizations.

4. **Pattern Recognition**: Identify common patterns in tool calling across different models to improve the pattern extraction algorithms.

5. **Testing**: Use the batch testing tools to ensure that changes don't break existing functionality.

## Contributing New Tools

If you develop new tools that might be useful for the development of LiteAgent, please consider adding them to this directory and documenting them in this README. 