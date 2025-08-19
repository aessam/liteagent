"""
LiteAgent is a lightweight, extensible framework for building AI agents.
"""

from .tools import liteagent_tool, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .agent import LiteAgent
from .forked_agent import ForkedAgent
from .observer import AgentObserver, ConsoleObserver
from .models import create_model_interface, UnifiedModelInterface
from .memory import ConversationMemory
from .utils import setup_logging, check_api_keys
from .capabilities import get_model_capabilities, ModelCapabilities
from .mcp_adapter import run_as_mcp, LiteAgentMCPServer, MCPAgentObserver

__version__ = "0.1.0"