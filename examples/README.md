# LiteAgent Examples

This directory contains practical examples demonstrating LiteAgent capabilities.

## Examples

### 🤖 Orchestrator Example (`orchestrator_example.py`)

A multi-agent system with specialized sub-agents:

- **Orchestrator Agent**: Main agent that talks to you and coordinates other agents
- **Web Search Agent**: Handles web searches using DuckDuckGo
- **File Agent**: Handles file operations (read, grep, find, list)

#### Features

- **Smart Coordination**: Orchestrator decides which agents to use based on your requests
- **Step-by-Step Logging**: See exactly what's happening behind the scenes
- **Multiple Providers**: Works with OpenAI, Anthropic, Groq, Mistral, DeepSeek
- **Real Tools**: Actual web search and file operations

#### Installation

```bash
# Install optional dependencies (includes .env support)
pip install -r examples/requirements-examples.txt
```

#### Usage

```bash
# Using OpenAI GPT-5
python examples/orchestrator_example.py -p openai -m gpt-5

# Using Anthropic Claude
python examples/orchestrator_example.py -p anthropic -m claude-3-5-sonnet-20241022

# Using Groq
python examples/orchestrator_example.py -p groq -m qwen/qwen3-32b

# Using Mistral
python examples/orchestrator_example.py -p mistral -m open-mixtral-8x22b
```

#### Example Interactions

**Web Search + File Analysis:**
```
🧑 You: Find information about Python async programming and check if we have any async code in our project

🤖 Orchestrator: I'll help you with both parts:
1. First, I'll search the web for current information about Python async programming
2. Then, I'll search your project files for async-related code

Let me start with the web search...

🔍 [Web Search] Searching for: 'Python async programming best practices 2024'
✅ [Web Search] Found 5 results

🔍 [File Agent] Searching for pattern 'async' in ./*.py
✅ [File Agent] Found 15 matches in 3 files

Based on my search, here's what I found...
```

**File Operations:**
```
🧑 You: List all Python files in the project and show me the main.py file

🤖 Orchestrator: I'll help you explore your project structure:
1. First, I'll find all Python files in your project
2. Then, I'll read the main.py file for you

📁 [File Agent] Finding files matching '*.py' in .
✅ [File Agent] Found 23 files matching pattern

📖 [File Agent] Reading file: main.py
✅ [File Agent] Read 45 lines from main.py

Here's what I found in your project...
```

#### API Keys

**Option 1: .env file (Recommended)**
Create a `.env` file in the project root:
```bash
# .env file
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
GROQ_API_KEY=your-groq-key-here
MISTRAL_API_KEY=your-mistral-key-here
DEEPSEEK_API_KEY=your-deepseek-key-here
```

**Option 2: Environment variables**
```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GROQ_API_KEY="your-key-here"
export MISTRAL_API_KEY="your-key-here"
```

**Option 3: Command line**
```bash
python examples/orchestrator_example.py -p openai -m gpt-5 --api-key your-key-here
```

## Architecture

The orchestrator example demonstrates:

1. **Specialized Agents**: Each agent has specific tools and responsibilities
2. **Tool Coordination**: Main agent decides which tools to use based on context
3. **Clear Logging**: All operations are logged with clear indicators
4. **Error Handling**: Graceful handling of missing dependencies or API errors
5. **Multi-Provider Support**: Same interface works across all supported providers

## Contributing

To add new examples:

1. Create a new Python file in this directory
2. Follow the pattern of using `liteagent_tool` decorators
3. Include clear documentation and usage examples
4. Add any optional dependencies to `requirements-examples.txt`