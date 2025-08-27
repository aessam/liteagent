"""
LiteAgent is a lightweight, extensible framework for building AI agents.
"""

from .tools import liteagent_tool, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .agent import LiteAgent
from .observer import AgentObserver, ConsoleObserver
from .models import create_model_interface, UnifiedModelInterface
from .memory import ConversationMemory
from .utils import setup_logging, check_api_keys
from .capabilities import get_model_capabilities, ModelCapabilities
from .mcp_adapter import run_as_mcp, LiteAgentMCPServer, MCPAgentObserver
from .cost_tracking import CostTracker, TokenUsage, get_cost_tracker

# Unified ForkedAgent (replaces old implementations)
from .unified_forked_agent import UnifiedForkedAgent, ForkedAgent, ForkConfig, SessionType

# Multi-Agent Collaboration Components
from .blackboard import Blackboard, KnowledgeItem
from .agent_registry import AgentRegistry, AgentCapability, AgentStatus
from .async_executor import AsyncCoordinator, AgentTask, TaskResult
from .multi_agent_coordinator import MultiAgentCoordinator, MultiAgentRequest, MultiAgentResponse

# Legacy imports (deprecated - use UnifiedForkedAgent instead)
import warnings
try:
    from .forked_agent import ForkedAgent as _LegacyForkedAgent
    warnings.warn(
        "forked_agent.ForkedAgent is deprecated. Use UnifiedForkedAgent instead.",
        DeprecationWarning,
        stacklevel=2
    )
except ImportError:
    pass

try:
    from .forked_agent_v2 import ForkedAgentV2 as _LegacyForkedAgentV2
    warnings.warn(
        "forked_agent_v2.ForkedAgentV2 is deprecated. Use UnifiedForkedAgent instead.",
        DeprecationWarning,
        stacklevel=2
    )
except ImportError:
    pass

__version__ = "0.1.0"