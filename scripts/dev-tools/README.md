# LiteAgent Development Tools

This directory contains utility scripts for LiteAgent development and testing.

## Available Tools

### test_tool_call.sh
A comprehensive shell script for testing tool calling functionality across different providers.

**Usage:**
```bash
# Test specific model
./test_tool_call.sh -p openai -m gpt-4o-mini -r

# List available models
./test_tool_call.sh -p anthropic -l

# Test all models for a provider
./test_tool_call.sh -p groq --all
```

**Supported Providers:** OpenAI, Anthropic, Groq, Ollama, DeepSeek, Mistral

**Features:**
- Tests both native tool calling APIs and simulated tool formats
- Automatically handles provider-specific authentication and formatting
- Saves responses to `.tool_test/` directory for analysis
- Supports batch testing across multiple models

### call_collector.py
Python AST analysis tool for building call graphs and analyzing function usage patterns in Python code.

**Usage:**
```bash
python call_collector.py path/to/python/file.py
```

## Environment Setup

Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
```

## Notes

These tools test the native function calling capabilities that LiteAgent now uses directly with each provider's API, rather than the pattern-matching approach used in earlier versions.