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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class MCPAgentObserver(AgentObserver):
    """Observer that captures agent activity for MCP integration."""
    
    def xǁMCPAgentObserverǁ__init____mutmut_orig(self):
        self.last_response = None
        self.last_function_result = None
        self.last_function_call = None
    
    def xǁMCPAgentObserverǁ__init____mutmut_1(self):
        self.last_response = ""
        self.last_function_result = None
        self.last_function_call = None
    
    def xǁMCPAgentObserverǁ__init____mutmut_2(self):
        self.last_response = None
        self.last_function_result = ""
        self.last_function_call = None
    
    def xǁMCPAgentObserverǁ__init____mutmut_3(self):
        self.last_response = None
        self.last_function_result = None
        self.last_function_call = ""
    
    xǁMCPAgentObserverǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMCPAgentObserverǁ__init____mutmut_1': xǁMCPAgentObserverǁ__init____mutmut_1, 
        'xǁMCPAgentObserverǁ__init____mutmut_2': xǁMCPAgentObserverǁ__init____mutmut_2, 
        'xǁMCPAgentObserverǁ__init____mutmut_3': xǁMCPAgentObserverǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMCPAgentObserverǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁMCPAgentObserverǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁMCPAgentObserverǁ__init____mutmut_orig)
    xǁMCPAgentObserverǁ__init____mutmut_orig.__name__ = 'xǁMCPAgentObserverǁ__init__'
    
    def xǁMCPAgentObserverǁon_agent_response__mutmut_orig(self, event):
        self.last_response = event.response
        
    
    def xǁMCPAgentObserverǁon_agent_response__mutmut_1(self, event):
        self.last_response = None
        
    
    xǁMCPAgentObserverǁon_agent_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMCPAgentObserverǁon_agent_response__mutmut_1': xǁMCPAgentObserverǁon_agent_response__mutmut_1
    }
    
    def on_agent_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMCPAgentObserverǁon_agent_response__mutmut_orig"), object.__getattribute__(self, "xǁMCPAgentObserverǁon_agent_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_agent_response.__signature__ = _mutmut_signature(xǁMCPAgentObserverǁon_agent_response__mutmut_orig)
    xǁMCPAgentObserverǁon_agent_response__mutmut_orig.__name__ = 'xǁMCPAgentObserverǁon_agent_response'
    def xǁMCPAgentObserverǁon_function_result__mutmut_orig(self, event):
        self.last_function_result = event.result
        
    def xǁMCPAgentObserverǁon_function_result__mutmut_1(self, event):
        self.last_function_result = None
        
    
    xǁMCPAgentObserverǁon_function_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMCPAgentObserverǁon_function_result__mutmut_1': xǁMCPAgentObserverǁon_function_result__mutmut_1
    }
    
    def on_function_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMCPAgentObserverǁon_function_result__mutmut_orig"), object.__getattribute__(self, "xǁMCPAgentObserverǁon_function_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_function_result.__signature__ = _mutmut_signature(xǁMCPAgentObserverǁon_function_result__mutmut_orig)
    xǁMCPAgentObserverǁon_function_result__mutmut_orig.__name__ = 'xǁMCPAgentObserverǁon_function_result'
    def xǁMCPAgentObserverǁon_function_call__mutmut_orig(self, event):
        self.last_function_call = event
        
    def xǁMCPAgentObserverǁon_function_call__mutmut_1(self, event):
        self.last_function_call = None
        
    
    xǁMCPAgentObserverǁon_function_call__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁMCPAgentObserverǁon_function_call__mutmut_1': xǁMCPAgentObserverǁon_function_call__mutmut_1
    }
    
    def on_function_call(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁMCPAgentObserverǁon_function_call__mutmut_orig"), object.__getattribute__(self, "xǁMCPAgentObserverǁon_function_call__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_function_call.__signature__ = _mutmut_signature(xǁMCPAgentObserverǁon_function_call__mutmut_orig)
    xǁMCPAgentObserverǁon_function_call__mutmut_orig.__name__ = 'xǁMCPAgentObserverǁon_function_call'
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_orig(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_1(self, name: str, agents: List[LiteAgent], transport: str = "XXsseXX", host: str = "127.0.0.1", port: int = 8000):
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_2(self, name: str, agents: List[LiteAgent], transport: str = "SSE", host: str = "127.0.0.1", port: int = 8000):
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_3(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "XX127.0.0.1XX", port: int = 8000):
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_4(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8001):
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_5(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the MCP server with LiteAgent instances.
        
        Args:
            name: Name of the MCP server
            agents: List of LiteAgent instances to expose
            transport: Transport protocol to use ("stdio" or "sse")
            host: Host to bind the server to (only used with "sse" transport)
            port: Port to bind the server to (only used with "sse" transport)
        """
        self.name = None
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_6(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.agents = None
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_7(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.mcp_server = None
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_8(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.mcp_server = FastMCP(None)
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_9(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.observers = None
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_10(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.transport = None
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_11(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.host = None
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_12(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        self.port = None
        
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
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_13(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
            observer = None
            agent.add_observer(observer)
            self.observers[agent.name] = observer
            
            # Register the agent as a tool
            self._register_agent_as_tool(agent)
            
            # Register a resource for this agent's system prompt
            self._register_agent_resources(agent)
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_14(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
            agent.add_observer(None)
            self.observers[agent.name] = observer
            
            # Register the agent as a tool
            self._register_agent_as_tool(agent)
            
            # Register a resource for this agent's system prompt
            self._register_agent_resources(agent)
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_15(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
            self.observers[agent.name] = None
            
            # Register the agent as a tool
            self._register_agent_as_tool(agent)
            
            # Register a resource for this agent's system prompt
            self._register_agent_resources(agent)
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_16(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
            self._register_agent_as_tool(None)
            
            # Register a resource for this agent's system prompt
            self._register_agent_resources(agent)
    
    def xǁLiteAgentMCPServerǁ__init____mutmut_17(self, name: str, agents: List[LiteAgent], transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
            self._register_agent_resources(None)
    
    xǁLiteAgentMCPServerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentMCPServerǁ__init____mutmut_1': xǁLiteAgentMCPServerǁ__init____mutmut_1, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_2': xǁLiteAgentMCPServerǁ__init____mutmut_2, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_3': xǁLiteAgentMCPServerǁ__init____mutmut_3, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_4': xǁLiteAgentMCPServerǁ__init____mutmut_4, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_5': xǁLiteAgentMCPServerǁ__init____mutmut_5, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_6': xǁLiteAgentMCPServerǁ__init____mutmut_6, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_7': xǁLiteAgentMCPServerǁ__init____mutmut_7, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_8': xǁLiteAgentMCPServerǁ__init____mutmut_8, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_9': xǁLiteAgentMCPServerǁ__init____mutmut_9, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_10': xǁLiteAgentMCPServerǁ__init____mutmut_10, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_11': xǁLiteAgentMCPServerǁ__init____mutmut_11, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_12': xǁLiteAgentMCPServerǁ__init____mutmut_12, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_13': xǁLiteAgentMCPServerǁ__init____mutmut_13, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_14': xǁLiteAgentMCPServerǁ__init____mutmut_14, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_15': xǁLiteAgentMCPServerǁ__init____mutmut_15, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_16': xǁLiteAgentMCPServerǁ__init____mutmut_16, 
        'xǁLiteAgentMCPServerǁ__init____mutmut_17': xǁLiteAgentMCPServerǁ__init____mutmut_17
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentMCPServerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentMCPServerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLiteAgentMCPServerǁ__init____mutmut_orig)
    xǁLiteAgentMCPServerǁ__init____mutmut_orig.__name__ = 'xǁLiteAgentMCPServerǁ__init__'
    
    def xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_orig(self, agent: LiteAgent):
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
    
    def xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_1(self, agent: LiteAgent):
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
        agent_tool.__name__ = None
        agent_tool.__doc__ = agent.description
    
    def xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_2(self, agent: LiteAgent):
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
        agent_tool.__doc__ = None
    
    xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_1': xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_1, 
        'xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_2': xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_2
    }
    
    def _register_agent_as_tool(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _register_agent_as_tool.__signature__ = _mutmut_signature(xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_orig)
    xǁLiteAgentMCPServerǁ_register_agent_as_tool__mutmut_orig.__name__ = 'xǁLiteAgentMCPServerǁ_register_agent_as_tool'
    
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
    
    def xǁLiteAgentMCPServerǁrun__mutmut_orig(self):
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
    
    def xǁLiteAgentMCPServerǁrun__mutmut_1(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport != "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="sse")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_2(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "XXsseXX":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="sse")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_3(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "SSE":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="sse")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_4(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = None
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="sse")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_5(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = None
            self.mcp_server.run(transport="sse")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_6(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport=None)
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_7(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="XXsseXX")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_8(self):
        """Run the MCP server in development mode."""
        # Use the configured transport
        if self.transport == "sse":
            # For SSE transport, we need to use the FastMCP run method with the configured host and port
            # Set the host and port in the FastMCP settings
            self.mcp_server.settings.host = self.host
            self.mcp_server.settings.port = self.port
            self.mcp_server.run(transport="SSE")
        else:
            # For stdio transport, we can use the FastMCP run method directly
            self.mcp_server.run(transport=self.transport)
    
    def xǁLiteAgentMCPServerǁrun__mutmut_9(self):
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
            self.mcp_server.run(transport=None)
    
    xǁLiteAgentMCPServerǁrun__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentMCPServerǁrun__mutmut_1': xǁLiteAgentMCPServerǁrun__mutmut_1, 
        'xǁLiteAgentMCPServerǁrun__mutmut_2': xǁLiteAgentMCPServerǁrun__mutmut_2, 
        'xǁLiteAgentMCPServerǁrun__mutmut_3': xǁLiteAgentMCPServerǁrun__mutmut_3, 
        'xǁLiteAgentMCPServerǁrun__mutmut_4': xǁLiteAgentMCPServerǁrun__mutmut_4, 
        'xǁLiteAgentMCPServerǁrun__mutmut_5': xǁLiteAgentMCPServerǁrun__mutmut_5, 
        'xǁLiteAgentMCPServerǁrun__mutmut_6': xǁLiteAgentMCPServerǁrun__mutmut_6, 
        'xǁLiteAgentMCPServerǁrun__mutmut_7': xǁLiteAgentMCPServerǁrun__mutmut_7, 
        'xǁLiteAgentMCPServerǁrun__mutmut_8': xǁLiteAgentMCPServerǁrun__mutmut_8, 
        'xǁLiteAgentMCPServerǁrun__mutmut_9': xǁLiteAgentMCPServerǁrun__mutmut_9
    }
    
    def run(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentMCPServerǁrun__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentMCPServerǁrun__mutmut_mutants"), args, kwargs, self)
        return result 
    
    run.__signature__ = _mutmut_signature(xǁLiteAgentMCPServerǁrun__mutmut_orig)
    xǁLiteAgentMCPServerǁrun__mutmut_orig.__name__ = 'xǁLiteAgentMCPServerǁrun'


def x_run_as_mcp__mutmut_orig(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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


def x_run_as_mcp__mutmut_1(*agents, server_name: str = "XXLiteAgent MCPXX", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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


def x_run_as_mcp__mutmut_2(*agents, server_name: str = "liteagent mcp", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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


def x_run_as_mcp__mutmut_3(*agents, server_name: str = "LITEAGENT MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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


def x_run_as_mcp__mutmut_4(*agents, server_name: str = "LiteAgent MCP", transport: str = "XXsseXX", host: str = "127.0.0.1", port: int = 8000):
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


def x_run_as_mcp__mutmut_5(*agents, server_name: str = "LiteAgent MCP", transport: str = "SSE", host: str = "127.0.0.1", port: int = 8000):
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


def x_run_as_mcp__mutmut_6(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "XX127.0.0.1XX", port: int = 8000):
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


def x_run_as_mcp__mutmut_7(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8001):
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


def x_run_as_mcp__mutmut_8(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    if agents:
        raise ValueError("At least one agent must be provided")
    
    # Create and run the MCP server
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_9(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        raise ValueError(None)
    
    # Create and run the MCP server
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_10(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        raise ValueError("XXAt least one agent must be providedXX")
    
    # Create and run the MCP server
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_11(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        raise ValueError("at least one agent must be provided")
    
    # Create and run the MCP server
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_12(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
        raise ValueError("AT LEAST ONE AGENT MUST BE PROVIDED")
    
    # Create and run the MCP server
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_13(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = None
    server.run() 


def x_run_as_mcp__mutmut_14(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(None, list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_15(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, None, transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_16(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(agents), transport=None, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_17(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=None, port=port)
    server.run() 


def x_run_as_mcp__mutmut_18(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, port=None)
    server.run() 


def x_run_as_mcp__mutmut_19(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(list(agents), transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_20(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, transport=transport, host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_21(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(agents), host=host, port=port)
    server.run() 


def x_run_as_mcp__mutmut_22(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, port=port)
    server.run() 


def x_run_as_mcp__mutmut_23(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(agents), transport=transport, host=host, )
    server.run() 


def x_run_as_mcp__mutmut_24(*agents, server_name: str = "LiteAgent MCP", transport: str = "sse", host: str = "127.0.0.1", port: int = 8000):
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
    server = LiteAgentMCPServer(server_name, list(None), transport=transport, host=host, port=port)
    server.run() 

x_run_as_mcp__mutmut_mutants : ClassVar[MutantDict] = {
'x_run_as_mcp__mutmut_1': x_run_as_mcp__mutmut_1, 
    'x_run_as_mcp__mutmut_2': x_run_as_mcp__mutmut_2, 
    'x_run_as_mcp__mutmut_3': x_run_as_mcp__mutmut_3, 
    'x_run_as_mcp__mutmut_4': x_run_as_mcp__mutmut_4, 
    'x_run_as_mcp__mutmut_5': x_run_as_mcp__mutmut_5, 
    'x_run_as_mcp__mutmut_6': x_run_as_mcp__mutmut_6, 
    'x_run_as_mcp__mutmut_7': x_run_as_mcp__mutmut_7, 
    'x_run_as_mcp__mutmut_8': x_run_as_mcp__mutmut_8, 
    'x_run_as_mcp__mutmut_9': x_run_as_mcp__mutmut_9, 
    'x_run_as_mcp__mutmut_10': x_run_as_mcp__mutmut_10, 
    'x_run_as_mcp__mutmut_11': x_run_as_mcp__mutmut_11, 
    'x_run_as_mcp__mutmut_12': x_run_as_mcp__mutmut_12, 
    'x_run_as_mcp__mutmut_13': x_run_as_mcp__mutmut_13, 
    'x_run_as_mcp__mutmut_14': x_run_as_mcp__mutmut_14, 
    'x_run_as_mcp__mutmut_15': x_run_as_mcp__mutmut_15, 
    'x_run_as_mcp__mutmut_16': x_run_as_mcp__mutmut_16, 
    'x_run_as_mcp__mutmut_17': x_run_as_mcp__mutmut_17, 
    'x_run_as_mcp__mutmut_18': x_run_as_mcp__mutmut_18, 
    'x_run_as_mcp__mutmut_19': x_run_as_mcp__mutmut_19, 
    'x_run_as_mcp__mutmut_20': x_run_as_mcp__mutmut_20, 
    'x_run_as_mcp__mutmut_21': x_run_as_mcp__mutmut_21, 
    'x_run_as_mcp__mutmut_22': x_run_as_mcp__mutmut_22, 
    'x_run_as_mcp__mutmut_23': x_run_as_mcp__mutmut_23, 
    'x_run_as_mcp__mutmut_24': x_run_as_mcp__mutmut_24
}

def run_as_mcp(*args, **kwargs):
    result = _mutmut_trampoline(x_run_as_mcp__mutmut_orig, x_run_as_mcp__mutmut_mutants, args, kwargs)
    return result 

run_as_mcp.__signature__ = _mutmut_signature(x_run_as_mcp__mutmut_orig)
x_run_as_mcp__mutmut_orig.__name__ = 'x_run_as_mcp'