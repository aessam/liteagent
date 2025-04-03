# Task Document: Implementing Ephemeral Agent in LiteAgent

## Overview
The Ephemeral Agent is a specialized type of agent that can dynamically create and execute other agents based on specific needs. Unlike traditional agents that have a fixed set of tools, the Ephemeral Agent will have access to a single meta-tool called "CreateAndExecuteAgent" that allows it to dynamically create purpose-built agents with specific system prompts and tools to handle user queries.

## Core Functionality
The Ephemeral Agent will:
1. Accept a user query
2. Analyze the query to determine the appropriate agent configuration needed
3. Dynamically create and execute a specialized agent with the right system prompt and tools
4. Return the result to the user
5. Discard the specialized agent after use (hence "ephemeral")

## Implementation Plan

### 1. Create the CreateAndExecuteAgent Tool

```python
# File: liteagent/ephemeral_tool.py

"""
Tool for dynamically creating and executing ephemeral agents.
"""

import random
import uuid
from typing import List, Dict, Any, Optional

from .tools import BaseTool
from liteagent import LiteAgent

class CreateAndExecuteAgentTool(BaseTool):
    """Tool that creates and executes a specialized agent on demand."""
    
    def __init__(self, available_tools_registry=None, parent_context_id=None):
        """
        Initialize the CreateAndExecuteAgent tool.
        
        Args:
            available_tools_registry: Dictionary mapping tool names to tool implementations
                                     that can be provided to created agents
            parent_context_id: The context ID of the parent agent, for tracking purposes
        """
        self.available_tools_registry = available_tools_registry or {}
        self.parent_context_id = parent_context_id
        
        # Define the tool function
        def create_and_execute_agent(
            system_prompt: str, 
            tool_names: List[str], 
            query: str,
            model: str = "gpt-4o-mini"
        ) -> str:
            """
            Create a new agent with specified system prompt and tools, then execute the query.
            
            Args:
                system_prompt: The system prompt to use for the agent
                tool_names: List of tool names to make available to the agent
                query: The query to execute with the agent
                model: Optional model name to use (defaults to gpt-4)
                
            Returns:
                The agent's response to the query
            """
            # Validate that all requested tools are available
            unavailable_tools = [name for name in tool_names if name not in self.available_tools_registry]
            if unavailable_tools:
                return f"Error: The following tools are not available: {', '.join(unavailable_tools)}"
                    
            # Get the tools for the agent
            tools = [self.available_tools_registry[name] for name in tool_names]
            
            # Create the agent with specified system prompt and tools
            agent_name = f"ephemeral-{uuid.uuid4().hex[:8]}"
            agent = LiteAgent(
                model=model,
                name=agent_name, 
                system_prompt=system_prompt,
                tools=tools,
                parent_context_id=self.parent_context_id
            )
            
            try:
                # Execute the query
                response = agent.chat(query)
                return response
            finally:
                # No need to explicitly clean up the agent as it will be garbage collected
                pass
        
        # Initialize the BaseTool with our function
        super().__init__(
            create_and_execute_agent, 
            name="CreateAndExecuteAgent",
            description="Creates a specialized agent with specified system prompt and tools, "
                        "then executes a query with it. This allows for creating purpose-built agents "
                        "that are optimized for specific tasks."
        )
```

### 2. Create the EphemeralAgent Class

```python
# File: liteagent/ephemeral_agent.py

"""
Ephemeral Agent implementation for LiteAgent.

This module provides the EphemeralAgent class, which can dynamically create
and execute specialized agents for specific tasks.
"""

from typing import Dict, Any, List, Optional

from .agent import LiteAgent
from .ephemeral_tool import CreateAndExecuteAgentTool

class EphemeralAgent(LiteAgent):
    """
    An agent that can dynamically create and execute purpose-built agents with specific tools.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are an Ephemeral Agent capable of creating specialized agents to handle specific tasks.
    
When given a user query, your job is to:
1. Analyze the query to determine what kind of specialized agent would be best equipped to handle it
2. Create an appropriate system prompt for that specialized agent
3. Select the most relevant tools for that agent from the available tools
4. Execute the query using the specialized agent via the CreateAndExecuteAgent tool

The CreateAndExecuteAgent tool takes:
- system_prompt: A clear, concise system prompt that defines the specialized agent's purpose and behavior
- tool_names: A list of relevant tool names to provide to the agent (only include tools needed for the task)
- query: The user's original query or a refined version that better suits the specialized agent
- model: (Optional) The name of the model to use for the specialized agent

Think carefully about what system prompt and tools would be most helpful for addressing the user's query.
Only select tools that are directly relevant to completing the task at hand.
"""
    
    def __init__(self, model, name="EphemeralAgent", system_prompt=None, tools_registry=None, debug=False, **kwargs):
        """
        Initialize the EphemeralAgent.
        
        Args:
            model: The LLM model to use
            name: Name of the agent (defaults to "EphemeralAgent")
            system_prompt: Custom system prompt (defaults to DEFAULT_SYSTEM_PROMPT)
            tools_registry: Dictionary mapping tool names to tool implementations
                           that can be provided to created agents
            debug: Whether to enable debug logging
            **kwargs: Additional arguments to pass to LiteAgent
        """
        self.debug = debug
        
        # Initialize the tools registry
        if tools_registry is None:
            from .tools import TOOLS
            # Create a registry of all available tools by name
            tools_registry = {}
            for tool in TOOLS:
                if hasattr(tool, 'name'):
                    tools_registry[tool.name] = tool
                elif callable(tool):
                    tools_registry[tool.__name__] = tool
                elif isinstance(tool, dict) and "name" in tool:
                    tools_registry[tool["name"]] = tool
        
        self.tools_registry = tools_registry
        
        # Create the CreateAndExecuteAgent tool with access to all tools
        create_agent_tool = CreateAndExecuteAgentTool(
            available_tools_registry=tools_registry,
            parent_context_id=kwargs.get('context_id')
        )
        
        # Initialize the LiteAgent with just the CreateAndExecuteAgent tool
        super().__init__(
            model=model,
            name=name,
            system_prompt=system_prompt or self.DEFAULT_SYSTEM_PROMPT,
            tools=[create_agent_tool],
            debug=debug,
            **kwargs
        )
    
    def list_available_tools(self) -> Dict[str, str]:
        """
        Return a dictionary of all available tools with their descriptions.
        
        Returns:
            Dict mapping tool names to descriptions
        """
        result = {}
        for name, tool in self.tools_registry.items():
            description = ""
            if hasattr(tool, 'description'):
                description = tool.description
            elif hasattr(tool, '__doc__') and tool.__doc__:
                description = tool.__doc__.strip()
            elif isinstance(tool, dict) and "description" in tool:
                description = tool["description"]
            else:
                description = f"Tool: {name}"
            
            result[name] = description
        
        return result
    
    def add_tool_to_registry(self, tool, name=None):
        """
        Add a new tool to the registry of available tools.
        
        Args:
            tool: The tool to add
            name: Optional custom name for the tool
        """
        if name:
            self.tools_registry[name] = tool
        elif hasattr(tool, 'name'):
            self.tools_registry[tool.name] = tool
        elif callable(tool):
            self.tools_registry[tool.__name__] = tool
        elif isinstance(tool, dict) and "name" in tool:
            self.tools_registry[tool["name"]] = tool
        else:
            raise ValueError("Cannot determine tool name. Please provide a name.")
```

### 3. Register the EphemeralAgent in package __init__.py

```python
# Add to liteagent/__init__.py
from .ephemeral_agent import EphemeralAgent
```

### 4. Create Example File for the Ephemeral Agent

```python
# File: examples/ephemeral_agent_example.py

"""
Example demonstrating the use of the EphemeralAgent.
"""

from liteagent import EphemeralAgent
from liteagent.utils import check_api_keys
from examples.tools import get_weather, add_numbers, multiply_numbers, search_database, ToolsForAgents

def run_ephemeral_agent_example(model, observers=None):
    """
    Run example with the Ephemeral Agent.
    
    Args:
        model (str): The model to use
        observers (list, optional): List of observers to attach to the agent
    """
    # Check for API keys
    check_api_keys()
    
    # Create tools for the tools registry
    tools_instance = ToolsForAgents(api_key="fake-api-key")
    
    # Create an ephemeral agent with access to all tools
    agent = EphemeralAgent(
        model=model,
        name="Ephemeral Agent",
        tools_registry={
            "add_numbers": add_numbers,
            "multiply_numbers": multiply_numbers,
            "get_weather": get_weather,
            "search_database": search_database,
        },
        observers=observers
    )
    
    # Test the agent with various queries
    print("\n=== Ephemeral Agent ===")
    
    # This should create a math-focused agent
    response = agent.chat("What is 42 + 17 and then multiply the result by 3?")
    print(f"Math Query Response: {response}")
    
    # This should create a weather-focused agent
    response = agent.chat("What's the weather like in Tokyo today?")
    print(f"Weather Query Response: {response}")
    
    # This should create a search-focused agent
    response = agent.chat("Can you search the database for information about AI ethics?")
    print(f"Search Query Response: {response}")
    
    # This should create a multi-purpose agent
    response = agent.chat("I need to know the weather in Berlin and also calculate 25 * 4")
    print(f"Multi-purpose Query Response: {response}")


if __name__ == "__main__":
    # Use Claude, GPT-4, or other capable model that supports function calling
    model = "gpt-4o-mini"
    run_ephemeral_agent_example(model)
```

## Implementation Considerations

1. **Tool Registry Management**: The Ephemeral Agent needs to maintain a comprehensive registry of all available tools. This should be easily extensible by users.

2. **Context Propagation**: We need to properly propagate context IDs from the parent agent to child agents for proper tracking and debugging.

3. **System Prompt Design**: The system prompt for the Ephemeral Agent is critical - it needs to guide the agent to:
   - Create targeted, concise system prompts for specialized agents
   - Select only the most relevant tools for each task
   - Format the query appropriately for the specialized agent

4. **Error Handling**: The implementation needs robust error handling for cases where:
   - Requested tools don't exist
   - The specialized agent fails to provide a proper response
   - The CreateAndExecuteAgent tool is used incorrectly

5. **Resource Management**: Since each request potentially creates a new agent, we need to ensure proper garbage collection to avoid memory leaks.

## Testing Plan

1. **Functional Testing**:
   - Test the agent's ability to select appropriate tools for different query types
   - Test with complex queries that might require multiple tools
   - Test error handling when requesting non-existent tools

2. **Edge Cases**:
   - Test with ambiguous queries that could be handled by multiple specialized agents
   - Test with queries that require no tools
   - Test with malformed or nonsensical queries

3. **Performance Testing**:
   - Benchmark the overhead of creating ephemeral agents compared to using a single agent with all tools
   - Test memory usage patterns with repeated agent creation

4. **Integration Testing**:
   - Test the EphemeralAgent within larger systems
   - Test with custom observers to ensure proper event propagation

## Future Enhancements

1. **Agent Caching**: Implement a caching mechanism to reuse similar agent configurations for improved performance.

2. **Tool Versioning**: Add support for tool versioning to allow specifying which version of a tool to use.

3. **Tool Recommendation**: Implement a system to automatically recommend the most appropriate tools based on query analysis.

4. **Recursive Agent Creation**: Allow created agents to themselves create other ephemeral agents for subtasks.

5. **Memory Sharing**: Implement mechanisms for sharing memory between the parent agent and ephemeral agents.

6. **Agent Templates**: Create pre-defined templates for common agent types (math agent, weather agent, etc.) to improve response time. 