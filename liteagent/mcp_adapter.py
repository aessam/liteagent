"""
MCP Adapter for LiteAgent.

This module provides functionality to expose LiteAgent instances as MCP servers,
allowing them to be used with any MCP-compatible client like Claude Desktop.
"""

import asyncio
import inspect
import json
from typing import Dict, List, Optional, Union, Any, Callable

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, PromptMessage, GetPromptResult, Prompt, PromptArgument
import mcp.types as mcp_types

from .agent import LiteAgent
from .tools import BaseTool
from .observer import AgentObserver


class MCPAgentObserver(AgentObserver):
    """Observer that captures agent activity for MCP integration."""
    
    def __init__(self):
        self.last_response = None
        self.last_function_result = None
        self.last_function_call = None
    
    def on_agent_response(self, event):
        self.last_response = event.response
        
    def on_function_result(self, event):
        self.last_function_result = event.result
        
    def on_function_call(self, event):
        self.last_function_call = event
        
    def on_event(self, event):
        """Handle any agent event."""
        # This is a catch-all method for any events we don't specifically handle
        pass


class LiteAgentMCPServer:
    """
    MCP Server wrapper for LiteAgent instances.
    
    This class wraps one or more LiteAgent instances and exposes them as an MCP server,
    allowing clients like Claude Desktop to interact with them.
    """
    
    def __init__(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the MCP server with LiteAgent instances.
        
        Args:
            name: Name of the MCP server
            agents: List of LiteAgent instances to expose
            transport: Transport protocol to use ("stdio" or "sse")
            host: Host to bind the server to (only used with "sse" transport)
            port: Port to bind the server to (only used with "sse" transport)
        """
        self.name = name
        self.agents = agents
        self.mcp_server = FastMCP(name)
        self.observers = {}
        self.transport = transport
        self.host = host
        self.port = port
        
        # Register each agent with the MCP server
        for agent in agents:
            # Create an observer for this agent
            observer = MCPAgentObserver()
            agent.add_observer(observer)
            self.observers[agent.name] = observer
            
            # Register the agent as a tool
            self._register_agent_as_tool(agent)
            
            # Register a resource for this agent's system prompt
            self._register_agent_resources(agent)
    
    def _register_agent_as_tool(self, agent: LiteAgent):
        """Register an agent as a tool with the MCP server."""
        
        @self.mcp_server.tool(name=agent.name, description=agent.description)
        def agent_tool(message: str) -> str:
            """Send a message to the agent."""
            try:
                # Send the message to the agent
                response = agent.chat(message)
                return response
            except Exception as e:
                # Return a structured error response
                return {"error": str(e), "status": "error"}
        
        # Update the tool name and docstring
        agent_tool.__name__ = agent.name
        agent_tool.__doc__ = agent.description
    
    def _register_agent_resources(self, agent: LiteAgent):
        """Register resources for the agent with the MCP server."""
        
        # Register the agent's description as a resource
        @self.mcp_server.resource(f"description://{agent.name}")
        def description_resource() -> str:
            """Get the agent's description."""
            return agent.description
        
        # Register the agent's system prompt as a resource
        @self.mcp_server.resource(f"system-prompt://{agent.name}")
        def system_prompt_resource() -> str:
            """Get the agent's system prompt."""
            return agent.system_prompt
        
        # Register the agent's tools as a resource
        @self.mcp_server.resource(f"tools://{agent.name}")
        def tools_resource() -> str:
            """Get information about the agent's tools."""
            return "\n\n".join([
                f"## {name}\n{tool.get('description', '')}\n"
                for name, tool in agent.tools.items()
            ])
    
    def run(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="sse")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)


def run_as_mcp(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
    """
    Run one or more LiteAgent instances as an MCP server.
    
    Args:
        *agents: One or more LiteAgent instances to expose as MCP servers
        server_name: Name of the MCP server
        transport: Transport protocol to use ("stdio" or "sse")
        host: Host to bind the server to (only used with "sse" transport)
        port: Port to bind the server to (only used with "sse" transport)
        
    Example:
        ```python
        agent1 = LiteAgent(model="gpt-3.5-turbo", name="Calculator")
        agent2 = LiteAgent(model="gpt-3.5-turbo", name="Weather")
        liteagent.run_as_mcp(agent1, agent2, transport="sse", port=8080)
        ```
    """
    if not agents:
        raise ValueError("At least one agent must be provided")
    
    # Create and run the MCP server
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=port)
    server.run() 