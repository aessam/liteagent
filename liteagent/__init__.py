"""
LiteAgent is a lightweight, extensible framework for building AI agents.
"""

from .tools import liteagent_tool, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .agent import LiteAgent
from .observer import AgentObserver, ConsoleObserver
from .models import create_model_interface, ModelInterface
from .memory import ConversationMemory
from .utils import setup_logging, check_api_keys
from .tool_calling_types import ToolCallingType
from .mcp_adapter import run_as_mcp, LiteAgentMCPServer, MCPAgentObserver

__version__ = "0.1.0"