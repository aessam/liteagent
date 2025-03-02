"""
LiteAgent - A lightweight agent framework using LiteLLM for LLM interactions.
"""

from .tools import tool, register_tool, liteagent_tool, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .agent import LiteAgent
from .models import create_model_interface, ModelInterface, FunctionCallingModel, TextBasedFunctionCallingModel
from .memory import ConversationMemory
from .utils import setup_logging, check_api_keys

__version__ = "0.1.0"