"""
LiteAgent - A lightweight agent framework using LiteLLM for LLM interactions.
"""

from .tools import tool, register_tool, liteagent_tool, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .agent import LiteAgent
from .models import create_model_interface, ModelInterface
from .memory import ConversationMemory
from .utils import setup_logging, check_api_keys
from .observer import (AgentObserver, AgentEvent, AgentInitializedEvent, UserMessageEvent, 
                      ModelRequestEvent, ModelResponseEvent, FunctionCallEvent, 
                      FunctionResultEvent, AgentResponseEvent, ConsoleObserver, 
                      FileObserver, TreeTraceObserver, generate_context_id)
from .agent_tool import AgentTool
from .tool_calling import ToolCallingType, ToolCallingHandler
from .tool_calling_config import get_tool_calling_type

__version__ = "0.1.0"