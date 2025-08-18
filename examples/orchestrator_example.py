#!/usr/bin/env python3
"""
Orchestrator Agent Example

This example demonstrates a multi-agent system where:
- Main Agent (Orchestrator): Talks to the user and coordinates other agents
- Web Search Agent: Handles web searches using DuckDuckGo
- File Agent: Handles file operations (read, grep, find)

Usage:
    python examples/orchestrator_example.py -p openai -m gpt-5
    python examples/orchestrator_example.py -p anthropic -m claude-3-5-sonnet-20241022
    python examples/orchestrator_example.py -p groq -m qwen/qwen3-32b
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# Add the project root to the path so we can import liteagent
sys.path.insert(0, str(Path(__file__).parent.parent))

from liteagent import LiteAgent, liteagent_tool

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional, continue without it
    pass


# =============================================================================
# LEVEL 2: SPECIALIZED SUB-AGENTS
# =============================================================================

class WebSearchAgent:
    """Level 2: Specialized agent for web searches."""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.agent = LiteAgent(
            model=model,
            name="web-search-agent",
            api_key=api_key,
            provider=provider,
            debug=True,
            tools=[self._search_duckduckgo],
            system_prompt="""You are a specialized web search agent. Your only job is to search the web using DuckDuckGo and return well-formatted results.

When you receive a search query:
1. Use the search_duckduckgo tool ONCE with the provided query
2. Format the results clearly and concisely  
3. Return the most relevant information immediately
4. DO NOT perform additional searches - provide your final response after the first search

CRITICAL: After calling a tool and receiving its result, you MUST provide a complete text response to the user. DO NOT call the same tool multiple times with the same arguments. DO NOT call tools repeatedly if you already have the information needed. If you've already received the information you need from a tool call, use that information to provide a final text response to the user.

You must STOP after one successful search and provide a final response."""
        )
    
    @liteagent_tool
    def _search_duckduckgo(self, query: str) -> str:
        """Search the web using DuckDuckGo."""
        try:
            from ddgs import DDGS
            
            print(f"🔍 [Web Search Agent] Searching for: '{query}'")
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                
            if not results:
                return f"No search results found for: {query}"
                
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                href = result.get('href', 'No URL')
                formatted_results.append(f"{i}. **{title}**\n   {body}\n   URL: {href}\n")
                
            search_summary = "\n".join(formatted_results)
            print(f"✅ [Web Search Agent] Found {len(results)} results")
            
            return f"Web search results for '{query}':\n\n{search_summary}"
            
        except ImportError:
            return "Error: ddgs library not installed. Install with: pip install ddgs"
        except Exception as e:
            return f"Error during web search: {str(e)}"
    
    def search(self, query: str) -> str:
        """Public interface for web searches."""
        return self.agent.chat(f"Search for: {query}")


class FileAgent:
    """Level 2: Specialized agent for file operations."""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.agent = LiteAgent(
            model=model,
            name="file-agent",
            api_key=api_key,
            provider=provider,
            debug=True,
            tools=[self._read_file, self._grep_files, self._find_files, self._list_directory],
            system_prompt="""You are a specialized file operations agent. Your job is to help with file-related tasks.

Available operations:
- read_file: Read contents of specific files
- grep_files: Search for patterns in files
- find_files: Find files by name pattern  
- list_directory: List directory contents

When you receive a file operation request:
1. Use the appropriate tool(s) 
2. Provide clear, well-formatted results
3. Be helpful and thorough

CRITICAL: After calling a tool and receiving its result, you MUST provide a complete text response to the user. DO NOT call the same tool multiple times with the same arguments. DO NOT call tools repeatedly if you already have the information needed. If you've already received the information you need from a tool call, use that information to provide a final text response to the user.

Always explain what you're doing and provide useful summaries, then STOP."""
        )
    
    @liteagent_tool  
    def _read_file(self, file_path: str, max_lines: int = 100) -> str:
        """Read the contents of a file."""
        try:
            print(f"📖 [File Agent] Reading file: {file_path}")
            
            path = Path(file_path)
            if not path.exists():
                return f"Error: File '{file_path}' does not exist"
                
            if not path.is_file():
                return f"Error: '{file_path}' is not a file"
                
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            if len(lines) > max_lines:
                content = ''.join(lines[:max_lines])
                content += f"\n\n... (truncated after {max_lines} lines, total: {len(lines)} lines)"
            else:
                content = ''.join(lines)
                
            print(f"✅ [File Agent] Read {len(lines)} lines from {file_path}")
            return f"Contents of '{file_path}':\n\n{content}"
            
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"

    @liteagent_tool
    def _grep_files(self, pattern: str, directory: str = ".", file_extension: str = "*.py") -> str:
        """Search for a pattern in files."""
        try:
            import re
            import glob
            
            print(f"🔍 [File Agent] Searching for pattern '{pattern}' in {directory}/{file_extension}")
            
            search_path = Path(directory)
            if not search_path.exists():
                return f"Error: Directory '{directory}' does not exist"
                
            pattern_path = search_path / file_extension
            files = glob.glob(str(pattern_path), recursive=True)
            
            if not files:
                return f"No files matching '{file_extension}' found in '{directory}'"
                
            results = []
            total_matches = 0
            
            for file_path in files[:20]:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    file_matches = []
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            file_matches.append(f"  Line {line_num}: {line.strip()}")
                            total_matches += 1
                            
                    if file_matches:
                        results.append(f"{file_path}:")
                        results.extend(file_matches[:10])
                        if len(file_matches) > 10:
                            results.append(f"  ... ({len(file_matches) - 10} more matches)")
                        results.append("")
                        
                except Exception as e:
                    results.append(f"{file_path}: Error reading file - {str(e)}")
                    
            if not results:
                return f"No matches found for pattern '{pattern}' in {len(files)} files"
                
            print(f"✅ [File Agent] Found {total_matches} matches in {len([r for r in results if ':' in r and not r.startswith(' ')])} files")
            
            return f"Search results for pattern '{pattern}':\n\n" + "\n".join(results)
            
        except Exception as e:
            return f"Error during file search: {str(e)}"

    @liteagent_tool
    def _find_files(self, filename_pattern: str, directory: str = ".") -> str:
        """Find files by name pattern."""
        try:
            import glob
            
            print(f"📁 [File Agent] Finding files matching '{filename_pattern}' in {directory}")
            
            search_path = Path(directory)
            if not search_path.exists():
                return f"Error: Directory '{directory}' does not exist"
                
            pattern_path = search_path / "**" / filename_pattern
            files = glob.glob(str(pattern_path), recursive=True)
            
            if not files:
                return f"No files matching '{filename_pattern}' found in '{directory}'"
                
            files.sort()
            if len(files) > 50:
                file_list = files[:50]
                result = "\n".join(file_list)
                result += f"\n\n... (showing first 50 of {len(files)} total matches)"
            else:
                result = "\n".join(files)
                
            print(f"✅ [File Agent] Found {len(files)} files matching pattern")
            
            return f"Files matching '{filename_pattern}':\n\n{result}"
            
        except Exception as e:
            return f"Error during file search: {str(e)}"

    @liteagent_tool
    def _list_directory(self, directory: str = ".") -> str:
        """List contents of a directory."""
        try:
            print(f"📂 [File Agent] Listing directory: {directory}")
            
            path = Path(directory)
            if not path.exists():
                return f"Error: Directory '{directory}' does not exist"
                
            if not path.is_dir():
                return f"Error: '{directory}' is not a directory"
                
            items = []
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    items.append(f"📁 {item.name}/")
                else:
                    size = item.stat().st_size
                    if size > 1024 * 1024:
                        size_str = f"{size / (1024 * 1024):.1f}MB"
                    elif size > 1024:
                        size_str = f"{size / 1024:.1f}KB"
                    else:
                        size_str = f"{size}B"
                    items.append(f"📄 {item.name} ({size_str})")
                    
            print(f"✅ [File Agent] Listed {len(items)} items")
            
            return f"Contents of '{directory}':\n\n" + "\n".join(items)
            
        except Exception as e:
            return f"Error listing directory '{directory}': {str(e)}"
    
    def handle_request(self, request: str) -> str:
        """Public interface for file operations."""
        return self.agent.chat(request)


# =============================================================================
# LEVEL 1: ORCHESTRATOR AGENT DELEGATION TOOLS
# =============================================================================

# Global variables to hold the Level 2 agents
web_search_agent = None
file_agent = None

@liteagent_tool
def search_web(query: str) -> str:
    """
    Delegate web search to the specialized Web Search Agent.
    
    Args:
        query: Search query to look for on the web
        
    Returns:
        Search results from the Web Search Agent
    """
    global web_search_agent
    if web_search_agent is None:
        return "Error: Web Search Agent not initialized"
    
    print(f"🤖 [Orchestrator] Delegating web search to Web Search Agent...")
    return web_search_agent.search(query)


@liteagent_tool  
def call_file_agent(request: str) -> str:
    """
    Delegate file operations to the specialized File Agent.
    
    Args:
        request: File operation request (e.g., "read main.py", "find all .py files", "search for 'async' in the project")
        
    Returns:
        Result from the File Agent
    """
    global file_agent
    if file_agent is None:
        return "Error: File Agent not initialized"
    
    print(f"🤖 [Orchestrator] Delegating file operation to File Agent...")
    return file_agent.handle_request(request)



# =============================================================================
# ORCHESTRATOR SYSTEM
# =============================================================================

def create_orchestrator_agent(provider: str, model: str, api_key: str) -> LiteAgent:
    """Create the main orchestrator agent that coordinates other agents."""
    global web_search_agent, file_agent
    
    # Initialize Level 2 specialized agents
    web_search_agent = WebSearchAgent(provider, model, api_key)
    file_agent = FileAgent(provider, model, api_key)
    
    print(f"✅ [Orchestrator] Initialized Web Search Agent and File Agent")
    
    system_prompt = """You are an intelligent orchestrator agent that helps users by coordinating specialized agents.

You have access to two specialized agents through these tools:

WEB SEARCH AGENT (use search_web):
- Use this when the user needs information from the internet
- Good for: current events, research, looking up facts, finding documentation
- Always search with specific, well-crafted queries

FILE AGENT (use call_file_agent):
- Use this when the user needs to work with files or explore directories
- Can read files, search for patterns, find files by name, list directories
- Pass clear requests like "read main.py", "find all .py files", "search for 'async' pattern"

IMPORTANT BEHAVIOR:
1. ALWAYS explain what you're doing before calling tools
2. Call the appropriate specialized agent based on user needs
3. You can use multiple tools in sequence if needed
4. Summarize findings and provide helpful responses
5. If the user asks about both web content and files, use both agents

STEP-BY-STEP APPROACH:
1. Understand what the user wants
2. Explain your plan (which agents you'll use and why)
3. Execute the plan using the appropriate tools
4. Summarize the results and provide a helpful response

Example interaction:
User: "Find information about Python async programming and also check if we have any async code in our project"

Response: "I'll help you with both parts:
1. First, I'll search the web for information about Python async programming
2. Then, I'll search our project files for async-related code

Let me start with the web search..."

Always be helpful, clear, and explain your actions."""

    return LiteAgent(
        model=model,
        name="orchestrator",
        api_key=api_key,
        provider=provider,
        debug=True,
        tools=[search_web, call_file_agent],
        system_prompt=system_prompt
    )


def print_banner():
    """Print a nice banner for the orchestrator."""
    print("=" * 70)
    print("🤖 LITEAGENT ORCHESTRATOR - Multi-Agent System")
    print("=" * 70)
    print("Available agents:")
    print("  🌐 Web Search Agent - Uses DuckDuckGo for web searches")
    print("  📁 File Agent - Handles file operations (read, grep, find)")
    print("  🎯 Orchestrator - Coordinates agents and talks to you")
    print("=" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Orchestrator System - 2-Level Architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python examples/orchestrator_example.py -p openai -m gpt-5
  python examples/orchestrator_example.py -p anthropic -m claude-3-5-sonnet-20241022
  python examples/orchestrator_example.py -p groq -m qwen/qwen3-32b
  python examples/orchestrator_example.py -p mistral -m open-mixtral-8x22b
  python examples/orchestrator_example.py -p ollama -m gpt-oss:20b
        """
    )
    
    parser.add_argument("-p", "--provider", required=True, 
                       choices=["openai", "anthropic", "groq", "mistral", "deepseek", "ollama"],
                       help="AI provider to use")
    parser.add_argument("-m", "--model", required=True,
                       help="Model name to use")
    parser.add_argument("--api-key", help="API key (or set environment variable)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key
    
    # Ollama is local and doesn't need an API key
    if args.provider == "ollama":
        api_key = "local"  # Placeholder for local provider
    elif not api_key:
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY", 
            "groq": "GROQ_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY"
        }
        
        env_var = env_vars.get(args.provider)
        if env_var:
            api_key = os.getenv(env_var)
            
        if not api_key:
            print(f"❌ Error: API key required.")
            print(f"   Option 1: Set {env_var} environment variable")
            print(f"   Option 2: Create a .env file with {env_var}=your-key-here")
            print(f"   Option 3: Use --api-key your-key-here")
            return 1
    
    print_banner()
    print(f"🚀 Initializing orchestrator with {args.provider}/{args.model}...")
    
    try:
        # Create the orchestrator agent
        orchestrator = create_orchestrator_agent(args.provider, args.model, api_key)
        print(f"✅ Orchestrator ready!")
        print(f"💡 The orchestrator will coordinate web search and file operations for you.")
        print()
        
        # Interactive loop
        print("Type 'quit', 'exit', or Ctrl+C to stop")
        print("-" * 70)
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                    
                if not user_input:
                    continue
                    
                print(f"\n🤖 Orchestrator: ", end="", flush=True)
                
                # Get response from orchestrator
                response = orchestrator.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.")
                
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())