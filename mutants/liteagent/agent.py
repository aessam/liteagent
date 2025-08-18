"""
New LiteAgent implementation using official provider clients.

This module contains the updated LiteAgent class that uses the new provider system
instead of LiteLLM.
"""

import json
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Union

from .tools import get_function_definitions, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .models import create_model_interface, UnifiedModelInterface
from .memory import ConversationMemory
from .capabilities import get_model_capabilities
from .providers import ProviderResponse, ToolCall
from .utils import logger
from .observer import (AgentObserver, AgentEvent, AgentInitializedEvent, UserMessageEvent, 
                      ModelRequestEvent, ModelResponseEvent, FunctionCallEvent, 
                      FunctionResultEvent, AgentResponseEvent, generate_context_id)
from .tool_calling import ToolCallTracker
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


class LiteAgent:
    """
    A lightweight agent that uses official provider clients for LLM interactions.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. 
Use the provided tools when needed to answer the user's question.
IMPORTANT: After calling a tool and receiving its result, you MUST provide a complete 
text response to the user. DO NOT call the same tool multiple times with the same arguments.
DO NOT call tools repeatedly if you already have the information needed.
If you've already received the information you need from a tool call, use that information
to provide a final text response to the user."""

    def xǁLiteAgentǁ__init____mutmut_orig(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_1(self, model, name, system_prompt=None, tools=None, debug=True, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_2(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = None
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_3(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = None
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_4(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = None
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_5(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt and self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_6(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = None
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_7(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = None
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_8(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = None
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_9(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = None
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_10(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id and generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_11(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = None
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_12(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(None)
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_13(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = None
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_14(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(None)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_15(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(None)
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_16(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = None
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_17(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(None, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_18(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, None, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_19(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=None, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_20(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_21(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_22(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_23(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, )
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_24(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = None
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_25(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=None)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_26(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = None
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_27(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers and []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_28(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = None
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_29(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = None
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_30(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_31(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(None)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_32(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(None)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_33(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = None
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_34(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = None
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_35(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(None, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_36(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, None) else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_37(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr('name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_38(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, ) else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_39(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'XXnameXX') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_40(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'NAME') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_41(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(None) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_42(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools and []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_43(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = None
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_44(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace(None, '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_45(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', None)}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_46(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_47(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', )}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_48(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].upper().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_49(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split(None)[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_50(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('XX.XX')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_51(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[1].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_52(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('XXyou are XX', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_53(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('YOU ARE ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_54(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', 'XXXX')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_55(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description = f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_56(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description -= f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_57(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(None)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_58(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {'XX, XX'.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_59(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(None)
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_60(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=None,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_61(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=None,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_62(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=None,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_63(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=None,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_64(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=None,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_65(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=None,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_66(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=None
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_67(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_68(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_69(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_70(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_71(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_72(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            tools=list(self.tools.keys())
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_73(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_74(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(None)
        ))
        
        self._log(f"Initialized agent {self.name} with model {self.model} using {self.model_interface.provider.provider_name} provider")
        

    def xǁLiteAgentǁ__init____mutmut_75(self, model, name, system_prompt=None, tools=None, debug=False, 
                 api_key=None, provider=None, parent_context_id=None, context_id=None, observers=None, 
                 description=None, **kwargs):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            api_key (str, optional): API key for the provider
            provider (str, optional): Explicit provider name (overrides auto-detection)
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does and its capabilities.
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.api_key = api_key
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Get model capabilities
        self.capabilities = get_model_capabilities(model)
        if self.capabilities:
            self._log(f"Model capabilities: tool_calling={self.capabilities.tool_calling}, "
                     f"parallel_tools={self.capabilities.supports_parallel_tools}")
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, api_key, provider=provider, **kwargs)
        
        # Initialize memory
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
        # Initialize observers
        self.observers = observers or []
        
        # Register tools
        self.tools = {}
        self.tool_instances = {}
        if tools is not None:
            self._register_tools(tools)
        else:
            # Get all registered tools
            from .tools import TOOLS
            self._register_tools(TOOLS)
        
        # Set or generate the agent's description
        if description:
            self.description = description
        else:
            # Generate a description from system prompt and tools
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools or []]
            self.description = f"{self.name} is an AI agent that {self.system_prompt.split('.')[0].lower().replace('you are ', '')}. "
            if tool_names:
                self.description += f"It has access to the following tools: {', '.join(tool_names)}."
        
        # Emit initialization event
        self._emit_event(AgentInitializedEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            model=self.model,
            system_prompt=self.system_prompt,
            tools=list(self.tools.keys())
        ))
        
        self._log(None)
        
    
    xǁLiteAgentǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ__init____mutmut_1': xǁLiteAgentǁ__init____mutmut_1, 
        'xǁLiteAgentǁ__init____mutmut_2': xǁLiteAgentǁ__init____mutmut_2, 
        'xǁLiteAgentǁ__init____mutmut_3': xǁLiteAgentǁ__init____mutmut_3, 
        'xǁLiteAgentǁ__init____mutmut_4': xǁLiteAgentǁ__init____mutmut_4, 
        'xǁLiteAgentǁ__init____mutmut_5': xǁLiteAgentǁ__init____mutmut_5, 
        'xǁLiteAgentǁ__init____mutmut_6': xǁLiteAgentǁ__init____mutmut_6, 
        'xǁLiteAgentǁ__init____mutmut_7': xǁLiteAgentǁ__init____mutmut_7, 
        'xǁLiteAgentǁ__init____mutmut_8': xǁLiteAgentǁ__init____mutmut_8, 
        'xǁLiteAgentǁ__init____mutmut_9': xǁLiteAgentǁ__init____mutmut_9, 
        'xǁLiteAgentǁ__init____mutmut_10': xǁLiteAgentǁ__init____mutmut_10, 
        'xǁLiteAgentǁ__init____mutmut_11': xǁLiteAgentǁ__init____mutmut_11, 
        'xǁLiteAgentǁ__init____mutmut_12': xǁLiteAgentǁ__init____mutmut_12, 
        'xǁLiteAgentǁ__init____mutmut_13': xǁLiteAgentǁ__init____mutmut_13, 
        'xǁLiteAgentǁ__init____mutmut_14': xǁLiteAgentǁ__init____mutmut_14, 
        'xǁLiteAgentǁ__init____mutmut_15': xǁLiteAgentǁ__init____mutmut_15, 
        'xǁLiteAgentǁ__init____mutmut_16': xǁLiteAgentǁ__init____mutmut_16, 
        'xǁLiteAgentǁ__init____mutmut_17': xǁLiteAgentǁ__init____mutmut_17, 
        'xǁLiteAgentǁ__init____mutmut_18': xǁLiteAgentǁ__init____mutmut_18, 
        'xǁLiteAgentǁ__init____mutmut_19': xǁLiteAgentǁ__init____mutmut_19, 
        'xǁLiteAgentǁ__init____mutmut_20': xǁLiteAgentǁ__init____mutmut_20, 
        'xǁLiteAgentǁ__init____mutmut_21': xǁLiteAgentǁ__init____mutmut_21, 
        'xǁLiteAgentǁ__init____mutmut_22': xǁLiteAgentǁ__init____mutmut_22, 
        'xǁLiteAgentǁ__init____mutmut_23': xǁLiteAgentǁ__init____mutmut_23, 
        'xǁLiteAgentǁ__init____mutmut_24': xǁLiteAgentǁ__init____mutmut_24, 
        'xǁLiteAgentǁ__init____mutmut_25': xǁLiteAgentǁ__init____mutmut_25, 
        'xǁLiteAgentǁ__init____mutmut_26': xǁLiteAgentǁ__init____mutmut_26, 
        'xǁLiteAgentǁ__init____mutmut_27': xǁLiteAgentǁ__init____mutmut_27, 
        'xǁLiteAgentǁ__init____mutmut_28': xǁLiteAgentǁ__init____mutmut_28, 
        'xǁLiteAgentǁ__init____mutmut_29': xǁLiteAgentǁ__init____mutmut_29, 
        'xǁLiteAgentǁ__init____mutmut_30': xǁLiteAgentǁ__init____mutmut_30, 
        'xǁLiteAgentǁ__init____mutmut_31': xǁLiteAgentǁ__init____mutmut_31, 
        'xǁLiteAgentǁ__init____mutmut_32': xǁLiteAgentǁ__init____mutmut_32, 
        'xǁLiteAgentǁ__init____mutmut_33': xǁLiteAgentǁ__init____mutmut_33, 
        'xǁLiteAgentǁ__init____mutmut_34': xǁLiteAgentǁ__init____mutmut_34, 
        'xǁLiteAgentǁ__init____mutmut_35': xǁLiteAgentǁ__init____mutmut_35, 
        'xǁLiteAgentǁ__init____mutmut_36': xǁLiteAgentǁ__init____mutmut_36, 
        'xǁLiteAgentǁ__init____mutmut_37': xǁLiteAgentǁ__init____mutmut_37, 
        'xǁLiteAgentǁ__init____mutmut_38': xǁLiteAgentǁ__init____mutmut_38, 
        'xǁLiteAgentǁ__init____mutmut_39': xǁLiteAgentǁ__init____mutmut_39, 
        'xǁLiteAgentǁ__init____mutmut_40': xǁLiteAgentǁ__init____mutmut_40, 
        'xǁLiteAgentǁ__init____mutmut_41': xǁLiteAgentǁ__init____mutmut_41, 
        'xǁLiteAgentǁ__init____mutmut_42': xǁLiteAgentǁ__init____mutmut_42, 
        'xǁLiteAgentǁ__init____mutmut_43': xǁLiteAgentǁ__init____mutmut_43, 
        'xǁLiteAgentǁ__init____mutmut_44': xǁLiteAgentǁ__init____mutmut_44, 
        'xǁLiteAgentǁ__init____mutmut_45': xǁLiteAgentǁ__init____mutmut_45, 
        'xǁLiteAgentǁ__init____mutmut_46': xǁLiteAgentǁ__init____mutmut_46, 
        'xǁLiteAgentǁ__init____mutmut_47': xǁLiteAgentǁ__init____mutmut_47, 
        'xǁLiteAgentǁ__init____mutmut_48': xǁLiteAgentǁ__init____mutmut_48, 
        'xǁLiteAgentǁ__init____mutmut_49': xǁLiteAgentǁ__init____mutmut_49, 
        'xǁLiteAgentǁ__init____mutmut_50': xǁLiteAgentǁ__init____mutmut_50, 
        'xǁLiteAgentǁ__init____mutmut_51': xǁLiteAgentǁ__init____mutmut_51, 
        'xǁLiteAgentǁ__init____mutmut_52': xǁLiteAgentǁ__init____mutmut_52, 
        'xǁLiteAgentǁ__init____mutmut_53': xǁLiteAgentǁ__init____mutmut_53, 
        'xǁLiteAgentǁ__init____mutmut_54': xǁLiteAgentǁ__init____mutmut_54, 
        'xǁLiteAgentǁ__init____mutmut_55': xǁLiteAgentǁ__init____mutmut_55, 
        'xǁLiteAgentǁ__init____mutmut_56': xǁLiteAgentǁ__init____mutmut_56, 
        'xǁLiteAgentǁ__init____mutmut_57': xǁLiteAgentǁ__init____mutmut_57, 
        'xǁLiteAgentǁ__init____mutmut_58': xǁLiteAgentǁ__init____mutmut_58, 
        'xǁLiteAgentǁ__init____mutmut_59': xǁLiteAgentǁ__init____mutmut_59, 
        'xǁLiteAgentǁ__init____mutmut_60': xǁLiteAgentǁ__init____mutmut_60, 
        'xǁLiteAgentǁ__init____mutmut_61': xǁLiteAgentǁ__init____mutmut_61, 
        'xǁLiteAgentǁ__init____mutmut_62': xǁLiteAgentǁ__init____mutmut_62, 
        'xǁLiteAgentǁ__init____mutmut_63': xǁLiteAgentǁ__init____mutmut_63, 
        'xǁLiteAgentǁ__init____mutmut_64': xǁLiteAgentǁ__init____mutmut_64, 
        'xǁLiteAgentǁ__init____mutmut_65': xǁLiteAgentǁ__init____mutmut_65, 
        'xǁLiteAgentǁ__init____mutmut_66': xǁLiteAgentǁ__init____mutmut_66, 
        'xǁLiteAgentǁ__init____mutmut_67': xǁLiteAgentǁ__init____mutmut_67, 
        'xǁLiteAgentǁ__init____mutmut_68': xǁLiteAgentǁ__init____mutmut_68, 
        'xǁLiteAgentǁ__init____mutmut_69': xǁLiteAgentǁ__init____mutmut_69, 
        'xǁLiteAgentǁ__init____mutmut_70': xǁLiteAgentǁ__init____mutmut_70, 
        'xǁLiteAgentǁ__init____mutmut_71': xǁLiteAgentǁ__init____mutmut_71, 
        'xǁLiteAgentǁ__init____mutmut_72': xǁLiteAgentǁ__init____mutmut_72, 
        'xǁLiteAgentǁ__init____mutmut_73': xǁLiteAgentǁ__init____mutmut_73, 
        'xǁLiteAgentǁ__init____mutmut_74': xǁLiteAgentǁ__init____mutmut_74, 
        'xǁLiteAgentǁ__init____mutmut_75': xǁLiteAgentǁ__init____mutmut_75
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLiteAgentǁ__init____mutmut_orig)
    xǁLiteAgentǁ__init____mutmut_orig.__name__ = 'xǁLiteAgentǁ__init__'
    def xǁLiteAgentǁ_register_tools__mutmut_orig(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_1(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = None
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_2(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(None)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_3(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = None
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_4(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = None
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_5(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = None
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_6(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = None
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_7(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = None
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_8(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = None
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_9(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(None):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_10(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = None
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_11(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get(None) == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_12(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("XXnameXX") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_13(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("NAME") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_14(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") != name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_15(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = None
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_16(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = None
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_17(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(None)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_18(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        return
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_19(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool or "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_20(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) or "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_21(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "XXnameXX" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_22(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "NAME" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_23(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" not in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_24(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "XXfunctionXX" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_25(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "FUNCTION" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_26(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" not in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_27(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = None
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_28(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["XXnameXX"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_29(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["NAME"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_30(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = None
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_31(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = None
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_32(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(None)
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_33(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["XXfunctionXX"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_34(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["FUNCTION"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_35(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) or "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_36(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "XXnameXX" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_37(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "NAME" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_38(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" not in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_39(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = None
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_40(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["XXnameXX"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_41(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["NAME"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_42(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = None
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(self.tools.keys())}")
        
    def xǁLiteAgentǁ_register_tools__mutmut_43(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(None)
        
    def xǁLiteAgentǁ_register_tools__mutmut_44(self, tool_functions):
        """
        Register tool functions with the agent.
        
        Args:
            tool_functions: List of tool functions to register
        """
        # Convert tools to function definitions
        function_defs = get_function_definitions(tool_functions)
        
        # Store tools and function definitions
        for tool in tool_functions:
            if isinstance(tool, (FunctionTool, InstanceMethodTool, StaticMethodTool)):
                # For tool objects, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif isinstance(tool, BaseTool):
                # For base tool classes, use their name
                name = tool.name
                self.tools[name] = tool.to_dict()
                self.tool_instances[name] = tool
            elif callable(tool):
                # For functions, use their __name__
                name = tool.__name__
                # Find the corresponding function definition
                for func_def in function_defs:
                    if func_def.get("name") == name:
                        self.tools[name] = func_def
                        # Create a FunctionTool for this function
                        self.tool_instances[name] = FunctionTool(tool)
                        break
            elif isinstance(tool, dict) and "name" in tool and "function" in tool:
                # For dict with name and function
                name = tool["name"]
                self.tools[name] = tool
                # Create a FunctionTool for this function
                self.tool_instances[name] = FunctionTool(tool["function"])
            elif isinstance(tool, dict) and "name" in tool:
                # For OpenAI-style function definitions
                name = tool["name"]
                self.tools[name] = tool
                # We can't create a tool instance for this, so it will fail if called
        
        self._log(f"Registered {len(self.tools)} tools: {list(None)}")
        
    
    xǁLiteAgentǁ_register_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_register_tools__mutmut_1': xǁLiteAgentǁ_register_tools__mutmut_1, 
        'xǁLiteAgentǁ_register_tools__mutmut_2': xǁLiteAgentǁ_register_tools__mutmut_2, 
        'xǁLiteAgentǁ_register_tools__mutmut_3': xǁLiteAgentǁ_register_tools__mutmut_3, 
        'xǁLiteAgentǁ_register_tools__mutmut_4': xǁLiteAgentǁ_register_tools__mutmut_4, 
        'xǁLiteAgentǁ_register_tools__mutmut_5': xǁLiteAgentǁ_register_tools__mutmut_5, 
        'xǁLiteAgentǁ_register_tools__mutmut_6': xǁLiteAgentǁ_register_tools__mutmut_6, 
        'xǁLiteAgentǁ_register_tools__mutmut_7': xǁLiteAgentǁ_register_tools__mutmut_7, 
        'xǁLiteAgentǁ_register_tools__mutmut_8': xǁLiteAgentǁ_register_tools__mutmut_8, 
        'xǁLiteAgentǁ_register_tools__mutmut_9': xǁLiteAgentǁ_register_tools__mutmut_9, 
        'xǁLiteAgentǁ_register_tools__mutmut_10': xǁLiteAgentǁ_register_tools__mutmut_10, 
        'xǁLiteAgentǁ_register_tools__mutmut_11': xǁLiteAgentǁ_register_tools__mutmut_11, 
        'xǁLiteAgentǁ_register_tools__mutmut_12': xǁLiteAgentǁ_register_tools__mutmut_12, 
        'xǁLiteAgentǁ_register_tools__mutmut_13': xǁLiteAgentǁ_register_tools__mutmut_13, 
        'xǁLiteAgentǁ_register_tools__mutmut_14': xǁLiteAgentǁ_register_tools__mutmut_14, 
        'xǁLiteAgentǁ_register_tools__mutmut_15': xǁLiteAgentǁ_register_tools__mutmut_15, 
        'xǁLiteAgentǁ_register_tools__mutmut_16': xǁLiteAgentǁ_register_tools__mutmut_16, 
        'xǁLiteAgentǁ_register_tools__mutmut_17': xǁLiteAgentǁ_register_tools__mutmut_17, 
        'xǁLiteAgentǁ_register_tools__mutmut_18': xǁLiteAgentǁ_register_tools__mutmut_18, 
        'xǁLiteAgentǁ_register_tools__mutmut_19': xǁLiteAgentǁ_register_tools__mutmut_19, 
        'xǁLiteAgentǁ_register_tools__mutmut_20': xǁLiteAgentǁ_register_tools__mutmut_20, 
        'xǁLiteAgentǁ_register_tools__mutmut_21': xǁLiteAgentǁ_register_tools__mutmut_21, 
        'xǁLiteAgentǁ_register_tools__mutmut_22': xǁLiteAgentǁ_register_tools__mutmut_22, 
        'xǁLiteAgentǁ_register_tools__mutmut_23': xǁLiteAgentǁ_register_tools__mutmut_23, 
        'xǁLiteAgentǁ_register_tools__mutmut_24': xǁLiteAgentǁ_register_tools__mutmut_24, 
        'xǁLiteAgentǁ_register_tools__mutmut_25': xǁLiteAgentǁ_register_tools__mutmut_25, 
        'xǁLiteAgentǁ_register_tools__mutmut_26': xǁLiteAgentǁ_register_tools__mutmut_26, 
        'xǁLiteAgentǁ_register_tools__mutmut_27': xǁLiteAgentǁ_register_tools__mutmut_27, 
        'xǁLiteAgentǁ_register_tools__mutmut_28': xǁLiteAgentǁ_register_tools__mutmut_28, 
        'xǁLiteAgentǁ_register_tools__mutmut_29': xǁLiteAgentǁ_register_tools__mutmut_29, 
        'xǁLiteAgentǁ_register_tools__mutmut_30': xǁLiteAgentǁ_register_tools__mutmut_30, 
        'xǁLiteAgentǁ_register_tools__mutmut_31': xǁLiteAgentǁ_register_tools__mutmut_31, 
        'xǁLiteAgentǁ_register_tools__mutmut_32': xǁLiteAgentǁ_register_tools__mutmut_32, 
        'xǁLiteAgentǁ_register_tools__mutmut_33': xǁLiteAgentǁ_register_tools__mutmut_33, 
        'xǁLiteAgentǁ_register_tools__mutmut_34': xǁLiteAgentǁ_register_tools__mutmut_34, 
        'xǁLiteAgentǁ_register_tools__mutmut_35': xǁLiteAgentǁ_register_tools__mutmut_35, 
        'xǁLiteAgentǁ_register_tools__mutmut_36': xǁLiteAgentǁ_register_tools__mutmut_36, 
        'xǁLiteAgentǁ_register_tools__mutmut_37': xǁLiteAgentǁ_register_tools__mutmut_37, 
        'xǁLiteAgentǁ_register_tools__mutmut_38': xǁLiteAgentǁ_register_tools__mutmut_38, 
        'xǁLiteAgentǁ_register_tools__mutmut_39': xǁLiteAgentǁ_register_tools__mutmut_39, 
        'xǁLiteAgentǁ_register_tools__mutmut_40': xǁLiteAgentǁ_register_tools__mutmut_40, 
        'xǁLiteAgentǁ_register_tools__mutmut_41': xǁLiteAgentǁ_register_tools__mutmut_41, 
        'xǁLiteAgentǁ_register_tools__mutmut_42': xǁLiteAgentǁ_register_tools__mutmut_42, 
        'xǁLiteAgentǁ_register_tools__mutmut_43': xǁLiteAgentǁ_register_tools__mutmut_43, 
        'xǁLiteAgentǁ_register_tools__mutmut_44': xǁLiteAgentǁ_register_tools__mutmut_44
    }
    
    def _register_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_register_tools__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_register_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _register_tools.__signature__ = _mutmut_signature(xǁLiteAgentǁ_register_tools__mutmut_orig)
    xǁLiteAgentǁ_register_tools__mutmut_orig.__name__ = 'xǁLiteAgentǁ_register_tools'
    def xǁLiteAgentǁ_emit_event__mutmut_orig(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_1(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(None)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_2(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(None)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_3(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(None)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_4(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(None)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_5(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(None)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_6(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(None)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_7(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(None)
            else:
                # Fallback to generic event handler
                observer.on_event(event)
                
    def xǁLiteAgentǁ_emit_event__mutmut_8(self, event: AgentEvent) -> None:
        """
        Emit an event to all observers.
        
        Args:
            event: The event to emit
        """
        for observer in self.observers:
            # Call the specific event handler method based on event type
            if isinstance(event, UserMessageEvent):
                observer.on_user_message(event)
            elif isinstance(event, ModelRequestEvent):
                observer.on_model_request(event)
            elif isinstance(event, ModelResponseEvent):
                observer.on_model_response(event)
            elif isinstance(event, FunctionCallEvent):
                observer.on_function_call(event)
            elif isinstance(event, FunctionResultEvent):
                observer.on_function_result(event)
            elif isinstance(event, AgentResponseEvent):
                observer.on_agent_response(event)
            elif isinstance(event, AgentInitializedEvent):
                observer.on_agent_initialized(event)
            else:
                # Fallback to generic event handler
                observer.on_event(None)
                
    
    xǁLiteAgentǁ_emit_event__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_emit_event__mutmut_1': xǁLiteAgentǁ_emit_event__mutmut_1, 
        'xǁLiteAgentǁ_emit_event__mutmut_2': xǁLiteAgentǁ_emit_event__mutmut_2, 
        'xǁLiteAgentǁ_emit_event__mutmut_3': xǁLiteAgentǁ_emit_event__mutmut_3, 
        'xǁLiteAgentǁ_emit_event__mutmut_4': xǁLiteAgentǁ_emit_event__mutmut_4, 
        'xǁLiteAgentǁ_emit_event__mutmut_5': xǁLiteAgentǁ_emit_event__mutmut_5, 
        'xǁLiteAgentǁ_emit_event__mutmut_6': xǁLiteAgentǁ_emit_event__mutmut_6, 
        'xǁLiteAgentǁ_emit_event__mutmut_7': xǁLiteAgentǁ_emit_event__mutmut_7, 
        'xǁLiteAgentǁ_emit_event__mutmut_8': xǁLiteAgentǁ_emit_event__mutmut_8
    }
    
    def _emit_event(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_emit_event__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_emit_event__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _emit_event.__signature__ = _mutmut_signature(xǁLiteAgentǁ_emit_event__mutmut_orig)
    xǁLiteAgentǁ_emit_event__mutmut_orig.__name__ = 'xǁLiteAgentǁ_emit_event'
    def xǁLiteAgentǁadd_observer__mutmut_orig(self, observer: AgentObserver) -> None:
        """
        Add an observer to the agent.
        
        Args:
            observer: The observer to add
        """
        self.observers.append(observer)
        
    def xǁLiteAgentǁadd_observer__mutmut_1(self, observer: AgentObserver) -> None:
        """
        Add an observer to the agent.
        
        Args:
            observer: The observer to add
        """
        self.observers.append(None)
        
    
    xǁLiteAgentǁadd_observer__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁadd_observer__mutmut_1': xǁLiteAgentǁadd_observer__mutmut_1
    }
    
    def add_observer(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁadd_observer__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁadd_observer__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_observer.__signature__ = _mutmut_signature(xǁLiteAgentǁadd_observer__mutmut_orig)
    xǁLiteAgentǁadd_observer__mutmut_orig.__name__ = 'xǁLiteAgentǁadd_observer'
    def xǁLiteAgentǁremove_observer__mutmut_orig(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the agent.
        
        Args:
            observer: The observer to remove
        """
        if observer in self.observers:
            self.observers.remove(observer)
    def xǁLiteAgentǁremove_observer__mutmut_1(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the agent.
        
        Args:
            observer: The observer to remove
        """
        if observer not in self.observers:
            self.observers.remove(observer)
    def xǁLiteAgentǁremove_observer__mutmut_2(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the agent.
        
        Args:
            observer: The observer to remove
        """
        if observer in self.observers:
            self.observers.remove(None)
    
    xǁLiteAgentǁremove_observer__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁremove_observer__mutmut_1': xǁLiteAgentǁremove_observer__mutmut_1, 
        'xǁLiteAgentǁremove_observer__mutmut_2': xǁLiteAgentǁremove_observer__mutmut_2
    }
    
    def remove_observer(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁremove_observer__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁremove_observer__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_observer.__signature__ = _mutmut_signature(xǁLiteAgentǁremove_observer__mutmut_orig)
    xǁLiteAgentǁremove_observer__mutmut_orig.__name__ = 'xǁLiteAgentǁremove_observer'
    
    def xǁLiteAgentǁchat__mutmut_orig(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_1(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = True) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_2(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(None)
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_3(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(None)
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_4(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=None,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_5(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=None,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_6(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=None,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_7(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=None
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_8(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_9(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_10(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_11(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_12(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images or self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_13(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(None, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_14(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, None)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_15(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_16(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, )
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_17(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(None)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_18(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = None
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_19(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=None)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_20(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(None)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_21(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(None)
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_22(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=None,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_23(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=None,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_24(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=None,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_25(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=None
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_26(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_27(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_28(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            response=response
        ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_29(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            ))
        
        self._log(f"Agent: {response}")
        return response
    
    def xǁLiteAgentǁchat__mutmut_30(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            images: Optional list of image paths or URLs for multimodal models
            enable_caching: Enable prompt caching for supported models (Anthropic)
            
        Returns:
            str: The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            message=message
        ))
        
        # Add user message to memory (with images if provided)
        if images and self._supports_image_input():
            self.memory.add_user_message_with_images(message, images)
        else:
            self.memory.add_user_message(message)
        
        # Generate response with tool calling
        response = self._generate_response_with_tools(enable_caching=enable_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(None)
        return response
    
    xǁLiteAgentǁchat__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁchat__mutmut_1': xǁLiteAgentǁchat__mutmut_1, 
        'xǁLiteAgentǁchat__mutmut_2': xǁLiteAgentǁchat__mutmut_2, 
        'xǁLiteAgentǁchat__mutmut_3': xǁLiteAgentǁchat__mutmut_3, 
        'xǁLiteAgentǁchat__mutmut_4': xǁLiteAgentǁchat__mutmut_4, 
        'xǁLiteAgentǁchat__mutmut_5': xǁLiteAgentǁchat__mutmut_5, 
        'xǁLiteAgentǁchat__mutmut_6': xǁLiteAgentǁchat__mutmut_6, 
        'xǁLiteAgentǁchat__mutmut_7': xǁLiteAgentǁchat__mutmut_7, 
        'xǁLiteAgentǁchat__mutmut_8': xǁLiteAgentǁchat__mutmut_8, 
        'xǁLiteAgentǁchat__mutmut_9': xǁLiteAgentǁchat__mutmut_9, 
        'xǁLiteAgentǁchat__mutmut_10': xǁLiteAgentǁchat__mutmut_10, 
        'xǁLiteAgentǁchat__mutmut_11': xǁLiteAgentǁchat__mutmut_11, 
        'xǁLiteAgentǁchat__mutmut_12': xǁLiteAgentǁchat__mutmut_12, 
        'xǁLiteAgentǁchat__mutmut_13': xǁLiteAgentǁchat__mutmut_13, 
        'xǁLiteAgentǁchat__mutmut_14': xǁLiteAgentǁchat__mutmut_14, 
        'xǁLiteAgentǁchat__mutmut_15': xǁLiteAgentǁchat__mutmut_15, 
        'xǁLiteAgentǁchat__mutmut_16': xǁLiteAgentǁchat__mutmut_16, 
        'xǁLiteAgentǁchat__mutmut_17': xǁLiteAgentǁchat__mutmut_17, 
        'xǁLiteAgentǁchat__mutmut_18': xǁLiteAgentǁchat__mutmut_18, 
        'xǁLiteAgentǁchat__mutmut_19': xǁLiteAgentǁchat__mutmut_19, 
        'xǁLiteAgentǁchat__mutmut_20': xǁLiteAgentǁchat__mutmut_20, 
        'xǁLiteAgentǁchat__mutmut_21': xǁLiteAgentǁchat__mutmut_21, 
        'xǁLiteAgentǁchat__mutmut_22': xǁLiteAgentǁchat__mutmut_22, 
        'xǁLiteAgentǁchat__mutmut_23': xǁLiteAgentǁchat__mutmut_23, 
        'xǁLiteAgentǁchat__mutmut_24': xǁLiteAgentǁchat__mutmut_24, 
        'xǁLiteAgentǁchat__mutmut_25': xǁLiteAgentǁchat__mutmut_25, 
        'xǁLiteAgentǁchat__mutmut_26': xǁLiteAgentǁchat__mutmut_26, 
        'xǁLiteAgentǁchat__mutmut_27': xǁLiteAgentǁchat__mutmut_27, 
        'xǁLiteAgentǁchat__mutmut_28': xǁLiteAgentǁchat__mutmut_28, 
        'xǁLiteAgentǁchat__mutmut_29': xǁLiteAgentǁchat__mutmut_29, 
        'xǁLiteAgentǁchat__mutmut_30': xǁLiteAgentǁchat__mutmut_30
    }
    
    def chat(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁchat__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁchat__mutmut_mutants"), args, kwargs, self)
        return result 
    
    chat.__signature__ = _mutmut_signature(xǁLiteAgentǁchat__mutmut_orig)
    xǁLiteAgentǁchat__mutmut_orig.__name__ = 'xǁLiteAgentǁchat'
    
    def xǁLiteAgentǁ_supports_image_input__mutmut_orig(self) -> bool:
        """Check if the current model supports image input."""
        capabilities = get_model_capabilities(self.model)
        return capabilities and capabilities.supports_image_input
        
    
    def xǁLiteAgentǁ_supports_image_input__mutmut_1(self) -> bool:
        """Check if the current model supports image input."""
        capabilities = None
        return capabilities and capabilities.supports_image_input
        
    
    def xǁLiteAgentǁ_supports_image_input__mutmut_2(self) -> bool:
        """Check if the current model supports image input."""
        capabilities = get_model_capabilities(None)
        return capabilities and capabilities.supports_image_input
        
    
    def xǁLiteAgentǁ_supports_image_input__mutmut_3(self) -> bool:
        """Check if the current model supports image input."""
        capabilities = get_model_capabilities(self.model)
        return capabilities or capabilities.supports_image_input
        
    
    xǁLiteAgentǁ_supports_image_input__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_supports_image_input__mutmut_1': xǁLiteAgentǁ_supports_image_input__mutmut_1, 
        'xǁLiteAgentǁ_supports_image_input__mutmut_2': xǁLiteAgentǁ_supports_image_input__mutmut_2, 
        'xǁLiteAgentǁ_supports_image_input__mutmut_3': xǁLiteAgentǁ_supports_image_input__mutmut_3
    }
    
    def _supports_image_input(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_supports_image_input__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_supports_image_input__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _supports_image_input.__signature__ = _mutmut_signature(xǁLiteAgentǁ_supports_image_input__mutmut_orig)
    xǁLiteAgentǁ_supports_image_input__mutmut_orig.__name__ = 'xǁLiteAgentǁ_supports_image_input'
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_orig(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_1(self, enable_caching: bool = True) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_2(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = None
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_3(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 11
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_4(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = None
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_5(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 1
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_6(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration <= max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_7(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration = 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_8(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration -= 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_9(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 2
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_10(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = None
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_11(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = ""
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_12(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() or self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_13(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = None
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_14(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(None)
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_15(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=None,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_16(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=None,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_17(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=None,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_18(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=None,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_19(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=None
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_20(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_21(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_22(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_23(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_24(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_25(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = None
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_26(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(None, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_27(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, None, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_28(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=None)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_29(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_30(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_31(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, )
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_32(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(None)
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_33(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=None,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_34(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=None,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_35(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=None,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_36(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=None
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_37(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_38(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_39(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_40(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_41(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = None
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_42(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_43(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = None
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_44(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(None)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_45(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content and "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_46(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "XXI apologize, but I couldn't generate a response.XX"
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_47(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "i apologize, but i couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_48(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I APOLOGIZE, BUT I COULDN'T GENERATE A RESPONSE."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_49(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(None, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_50(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, None)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_51(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_52(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, )
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_53(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(None)
                return f"I encountered an error: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_54(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(None)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_55(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "XXI reached the maximum number of tool iterations. Please try rephrasing your question.XX"
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_56(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "i reached the maximum number of tool iterations. please try rephrasing your question."
        
    def xǁLiteAgentǁ_generate_response_with_tools__mutmut_57(self, enable_caching: bool = False) -> str:
        """
        Generate a response with tool calling support.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages
            messages = self.memory.get_messages()
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Generate response
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Emit model response event
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                self._log(f"Error generating response: {e}")
                return f"I encountered an error: {str(e)}"
        
        return "I REACHED THE MAXIMUM NUMBER OF TOOL ITERATIONS. PLEASE TRY REPHRASING YOUR QUESTION."
        
    
    xǁLiteAgentǁ_generate_response_with_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_generate_response_with_tools__mutmut_1': xǁLiteAgentǁ_generate_response_with_tools__mutmut_1, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_2': xǁLiteAgentǁ_generate_response_with_tools__mutmut_2, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_3': xǁLiteAgentǁ_generate_response_with_tools__mutmut_3, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_4': xǁLiteAgentǁ_generate_response_with_tools__mutmut_4, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_5': xǁLiteAgentǁ_generate_response_with_tools__mutmut_5, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_6': xǁLiteAgentǁ_generate_response_with_tools__mutmut_6, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_7': xǁLiteAgentǁ_generate_response_with_tools__mutmut_7, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_8': xǁLiteAgentǁ_generate_response_with_tools__mutmut_8, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_9': xǁLiteAgentǁ_generate_response_with_tools__mutmut_9, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_10': xǁLiteAgentǁ_generate_response_with_tools__mutmut_10, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_11': xǁLiteAgentǁ_generate_response_with_tools__mutmut_11, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_12': xǁLiteAgentǁ_generate_response_with_tools__mutmut_12, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_13': xǁLiteAgentǁ_generate_response_with_tools__mutmut_13, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_14': xǁLiteAgentǁ_generate_response_with_tools__mutmut_14, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_15': xǁLiteAgentǁ_generate_response_with_tools__mutmut_15, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_16': xǁLiteAgentǁ_generate_response_with_tools__mutmut_16, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_17': xǁLiteAgentǁ_generate_response_with_tools__mutmut_17, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_18': xǁLiteAgentǁ_generate_response_with_tools__mutmut_18, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_19': xǁLiteAgentǁ_generate_response_with_tools__mutmut_19, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_20': xǁLiteAgentǁ_generate_response_with_tools__mutmut_20, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_21': xǁLiteAgentǁ_generate_response_with_tools__mutmut_21, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_22': xǁLiteAgentǁ_generate_response_with_tools__mutmut_22, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_23': xǁLiteAgentǁ_generate_response_with_tools__mutmut_23, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_24': xǁLiteAgentǁ_generate_response_with_tools__mutmut_24, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_25': xǁLiteAgentǁ_generate_response_with_tools__mutmut_25, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_26': xǁLiteAgentǁ_generate_response_with_tools__mutmut_26, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_27': xǁLiteAgentǁ_generate_response_with_tools__mutmut_27, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_28': xǁLiteAgentǁ_generate_response_with_tools__mutmut_28, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_29': xǁLiteAgentǁ_generate_response_with_tools__mutmut_29, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_30': xǁLiteAgentǁ_generate_response_with_tools__mutmut_30, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_31': xǁLiteAgentǁ_generate_response_with_tools__mutmut_31, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_32': xǁLiteAgentǁ_generate_response_with_tools__mutmut_32, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_33': xǁLiteAgentǁ_generate_response_with_tools__mutmut_33, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_34': xǁLiteAgentǁ_generate_response_with_tools__mutmut_34, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_35': xǁLiteAgentǁ_generate_response_with_tools__mutmut_35, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_36': xǁLiteAgentǁ_generate_response_with_tools__mutmut_36, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_37': xǁLiteAgentǁ_generate_response_with_tools__mutmut_37, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_38': xǁLiteAgentǁ_generate_response_with_tools__mutmut_38, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_39': xǁLiteAgentǁ_generate_response_with_tools__mutmut_39, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_40': xǁLiteAgentǁ_generate_response_with_tools__mutmut_40, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_41': xǁLiteAgentǁ_generate_response_with_tools__mutmut_41, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_42': xǁLiteAgentǁ_generate_response_with_tools__mutmut_42, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_43': xǁLiteAgentǁ_generate_response_with_tools__mutmut_43, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_44': xǁLiteAgentǁ_generate_response_with_tools__mutmut_44, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_45': xǁLiteAgentǁ_generate_response_with_tools__mutmut_45, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_46': xǁLiteAgentǁ_generate_response_with_tools__mutmut_46, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_47': xǁLiteAgentǁ_generate_response_with_tools__mutmut_47, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_48': xǁLiteAgentǁ_generate_response_with_tools__mutmut_48, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_49': xǁLiteAgentǁ_generate_response_with_tools__mutmut_49, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_50': xǁLiteAgentǁ_generate_response_with_tools__mutmut_50, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_51': xǁLiteAgentǁ_generate_response_with_tools__mutmut_51, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_52': xǁLiteAgentǁ_generate_response_with_tools__mutmut_52, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_53': xǁLiteAgentǁ_generate_response_with_tools__mutmut_53, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_54': xǁLiteAgentǁ_generate_response_with_tools__mutmut_54, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_55': xǁLiteAgentǁ_generate_response_with_tools__mutmut_55, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_56': xǁLiteAgentǁ_generate_response_with_tools__mutmut_56, 
        'xǁLiteAgentǁ_generate_response_with_tools__mutmut_57': xǁLiteAgentǁ_generate_response_with_tools__mutmut_57
    }
    
    def _generate_response_with_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_generate_response_with_tools__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_generate_response_with_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _generate_response_with_tools.__signature__ = _mutmut_signature(xǁLiteAgentǁ_generate_response_with_tools__mutmut_orig)
    xǁLiteAgentǁ_generate_response_with_tools__mutmut_orig.__name__ = 'xǁLiteAgentǁ_generate_response_with_tools'
    def xǁLiteAgentǁ_prepare_tools__mutmut_orig(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_1(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = None
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_2(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'XXfunctionXX' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_3(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'FUNCTION' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_4(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' not in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_5(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(None)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_6(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append(None)
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_7(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'XXtypeXX': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_8(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'TYPE': 'function',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_9(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'XXfunctionXX',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_10(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'FUNCTION',
                    'function': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_11(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'XXfunctionXX': tool_def
                })
        return tools
        
    def xǁLiteAgentǁ_prepare_tools__mutmut_12(self) -> List[Dict]:
        """
        Prepare tools for the model.
        
        Returns:
            List of tool definitions
        """
        tools = []
        for tool_name, tool_def in self.tools.items():
            if 'function' in tool_def:
                # Already in tools format
                tools.append(tool_def)
            else:
                # Convert to tools format
                tools.append({
                    'type': 'function',
                    'FUNCTION': tool_def
                })
        return tools
        
    
    xǁLiteAgentǁ_prepare_tools__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_prepare_tools__mutmut_1': xǁLiteAgentǁ_prepare_tools__mutmut_1, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_2': xǁLiteAgentǁ_prepare_tools__mutmut_2, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_3': xǁLiteAgentǁ_prepare_tools__mutmut_3, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_4': xǁLiteAgentǁ_prepare_tools__mutmut_4, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_5': xǁLiteAgentǁ_prepare_tools__mutmut_5, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_6': xǁLiteAgentǁ_prepare_tools__mutmut_6, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_7': xǁLiteAgentǁ_prepare_tools__mutmut_7, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_8': xǁLiteAgentǁ_prepare_tools__mutmut_8, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_9': xǁLiteAgentǁ_prepare_tools__mutmut_9, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_10': xǁLiteAgentǁ_prepare_tools__mutmut_10, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_11': xǁLiteAgentǁ_prepare_tools__mutmut_11, 
        'xǁLiteAgentǁ_prepare_tools__mutmut_12': xǁLiteAgentǁ_prepare_tools__mutmut_12
    }
    
    def _prepare_tools(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_prepare_tools__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_prepare_tools__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _prepare_tools.__signature__ = _mutmut_signature(xǁLiteAgentǁ_prepare_tools__mutmut_orig)
    xǁLiteAgentǁ_prepare_tools__mutmut_orig.__name__ = 'xǁLiteAgentǁ_prepare_tools'
    def xǁLiteAgentǁ_process_tool_calls__mutmut_orig(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_1(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(None)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_2(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(None, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_3(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, None):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_4(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_5(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, ):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_6(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(None)
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_7(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = None
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_8(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(None)
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_9(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=None,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_10(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=None,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_11(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=None,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_12(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=None,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_13(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=None
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_14(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_15(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_16(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_17(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_18(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_19(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(None, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_20(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, None, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_21(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, None)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_22(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_23(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_24(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, )
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_25(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(None)
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_26(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = None
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_27(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(None, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_28(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, None)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_29(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_30(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, )
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_31(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(None)
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_32(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(None)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_33(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:201]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_34(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(None)
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_35(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=None,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_36(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=None,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_37(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=None,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_38(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=None,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_39(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=None
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_40(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_41(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_42(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_43(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_44(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_45(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(None, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_46(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, None, tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_47(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), None)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_48(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_49(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_50(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), )
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_51(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(None), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_52(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = None
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_53(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(None)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_54(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(None)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_55(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(None, error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_56(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, None, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_57(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, None, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_58(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=None)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_59(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(error_msg, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_60(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, tool_call.id, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_61(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, is_error=True)
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_62(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, )
                
    def xǁLiteAgentǁ_process_tool_calls__mutmut_63(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
        """
        Process tool calls from the model response.
        
        Args:
            tool_calls: List of tool calls to process
            response: The model response containing the tool calls
        """
        # Add assistant message with tool calls to memory
        if response.content:
            # If there's content along with tool calls, add it
            self.memory.add_assistant_message(response.content)
            
        # Check for tool calling loops before processing any tools
        for tool_call in tool_calls:
            if self.memory.is_function_call_loop(tool_call.name, tool_call.arguments):
                logger.warning(f"Detected repeated function call: {tool_call.name} with args {tool_call.arguments}")
                # Return immediately to break the cycle
                loop_message = f"I notice I'm repeatedly trying to call the same tool. Let me provide a response based on the information I already have rather than continuing to search."
                return loop_message
        
        # Add tool calls to memory
        for tool_call in tool_calls:
            self._emit_event(FunctionCallEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                function_name=tool_call.name,
                function_args=tool_call.arguments
            ))
            
            # Add tool call to memory
            self.memory.add_tool_call(tool_call.name, tool_call.arguments, tool_call.id)
            
            # Execute the tool
            try:
                self._log(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
                result = self._execute_tool(tool_call.name, tool_call.arguments)
                self._log(f"Tool {tool_call.name} result: {str(result)[:200]}...")
                
                # Emit function result event
                self._emit_event(FunctionResultEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    function_name=tool_call.name,
                    result=result
                ))
                
                # Add result to memory
                self.memory.add_tool_result(tool_call.name, str(result), tool_call.id)
                
            except Exception as e:
                error_msg = f"Error executing {tool_call.name}: {str(e)}"
                self._log(error_msg)
                
                # Add error result to memory
                self.memory.add_tool_result(tool_call.name, error_msg, tool_call.id, is_error=False)
                
    
    xǁLiteAgentǁ_process_tool_calls__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_process_tool_calls__mutmut_1': xǁLiteAgentǁ_process_tool_calls__mutmut_1, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_2': xǁLiteAgentǁ_process_tool_calls__mutmut_2, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_3': xǁLiteAgentǁ_process_tool_calls__mutmut_3, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_4': xǁLiteAgentǁ_process_tool_calls__mutmut_4, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_5': xǁLiteAgentǁ_process_tool_calls__mutmut_5, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_6': xǁLiteAgentǁ_process_tool_calls__mutmut_6, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_7': xǁLiteAgentǁ_process_tool_calls__mutmut_7, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_8': xǁLiteAgentǁ_process_tool_calls__mutmut_8, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_9': xǁLiteAgentǁ_process_tool_calls__mutmut_9, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_10': xǁLiteAgentǁ_process_tool_calls__mutmut_10, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_11': xǁLiteAgentǁ_process_tool_calls__mutmut_11, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_12': xǁLiteAgentǁ_process_tool_calls__mutmut_12, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_13': xǁLiteAgentǁ_process_tool_calls__mutmut_13, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_14': xǁLiteAgentǁ_process_tool_calls__mutmut_14, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_15': xǁLiteAgentǁ_process_tool_calls__mutmut_15, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_16': xǁLiteAgentǁ_process_tool_calls__mutmut_16, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_17': xǁLiteAgentǁ_process_tool_calls__mutmut_17, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_18': xǁLiteAgentǁ_process_tool_calls__mutmut_18, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_19': xǁLiteAgentǁ_process_tool_calls__mutmut_19, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_20': xǁLiteAgentǁ_process_tool_calls__mutmut_20, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_21': xǁLiteAgentǁ_process_tool_calls__mutmut_21, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_22': xǁLiteAgentǁ_process_tool_calls__mutmut_22, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_23': xǁLiteAgentǁ_process_tool_calls__mutmut_23, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_24': xǁLiteAgentǁ_process_tool_calls__mutmut_24, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_25': xǁLiteAgentǁ_process_tool_calls__mutmut_25, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_26': xǁLiteAgentǁ_process_tool_calls__mutmut_26, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_27': xǁLiteAgentǁ_process_tool_calls__mutmut_27, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_28': xǁLiteAgentǁ_process_tool_calls__mutmut_28, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_29': xǁLiteAgentǁ_process_tool_calls__mutmut_29, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_30': xǁLiteAgentǁ_process_tool_calls__mutmut_30, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_31': xǁLiteAgentǁ_process_tool_calls__mutmut_31, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_32': xǁLiteAgentǁ_process_tool_calls__mutmut_32, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_33': xǁLiteAgentǁ_process_tool_calls__mutmut_33, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_34': xǁLiteAgentǁ_process_tool_calls__mutmut_34, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_35': xǁLiteAgentǁ_process_tool_calls__mutmut_35, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_36': xǁLiteAgentǁ_process_tool_calls__mutmut_36, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_37': xǁLiteAgentǁ_process_tool_calls__mutmut_37, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_38': xǁLiteAgentǁ_process_tool_calls__mutmut_38, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_39': xǁLiteAgentǁ_process_tool_calls__mutmut_39, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_40': xǁLiteAgentǁ_process_tool_calls__mutmut_40, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_41': xǁLiteAgentǁ_process_tool_calls__mutmut_41, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_42': xǁLiteAgentǁ_process_tool_calls__mutmut_42, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_43': xǁLiteAgentǁ_process_tool_calls__mutmut_43, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_44': xǁLiteAgentǁ_process_tool_calls__mutmut_44, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_45': xǁLiteAgentǁ_process_tool_calls__mutmut_45, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_46': xǁLiteAgentǁ_process_tool_calls__mutmut_46, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_47': xǁLiteAgentǁ_process_tool_calls__mutmut_47, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_48': xǁLiteAgentǁ_process_tool_calls__mutmut_48, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_49': xǁLiteAgentǁ_process_tool_calls__mutmut_49, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_50': xǁLiteAgentǁ_process_tool_calls__mutmut_50, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_51': xǁLiteAgentǁ_process_tool_calls__mutmut_51, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_52': xǁLiteAgentǁ_process_tool_calls__mutmut_52, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_53': xǁLiteAgentǁ_process_tool_calls__mutmut_53, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_54': xǁLiteAgentǁ_process_tool_calls__mutmut_54, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_55': xǁLiteAgentǁ_process_tool_calls__mutmut_55, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_56': xǁLiteAgentǁ_process_tool_calls__mutmut_56, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_57': xǁLiteAgentǁ_process_tool_calls__mutmut_57, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_58': xǁLiteAgentǁ_process_tool_calls__mutmut_58, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_59': xǁLiteAgentǁ_process_tool_calls__mutmut_59, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_60': xǁLiteAgentǁ_process_tool_calls__mutmut_60, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_61': xǁLiteAgentǁ_process_tool_calls__mutmut_61, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_62': xǁLiteAgentǁ_process_tool_calls__mutmut_62, 
        'xǁLiteAgentǁ_process_tool_calls__mutmut_63': xǁLiteAgentǁ_process_tool_calls__mutmut_63
    }
    
    def _process_tool_calls(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_process_tool_calls__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_process_tool_calls__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _process_tool_calls.__signature__ = _mutmut_signature(xǁLiteAgentǁ_process_tool_calls__mutmut_orig)
    xǁLiteAgentǁ_process_tool_calls__mutmut_orig.__name__ = 'xǁLiteAgentǁ_process_tool_calls'
    def xǁLiteAgentǁ_execute_tool__mutmut_orig(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_1(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_2(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(None)
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_3(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = None
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_4(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = None
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_5(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = ""
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_6(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = ""
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_7(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(None, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_8(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, None):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_9(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr('execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_10(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, ):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_11(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'XXexecuteXX'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_12(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'EXECUTE'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_13(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = None
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_14(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(None):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_15(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = None
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_16(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(None)
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_17(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = None
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_18(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() + start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_19(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=None,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_20(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=None,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_21(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_22(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=None
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_23(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_24(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_25(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_26(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_27(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = None
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_28(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() + start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_29(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = None
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_30(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(None)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_31(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=None,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_32(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=None,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_33(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=None,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_34(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=None
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_35(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_36(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                result=None,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_37(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                execution_time=execution_time,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_38(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                error=error_msg
            )
            raise  # Re-raise the original exception
    def xǁLiteAgentǁ_execute_tool__mutmut_39(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool function.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        if tool_name not in self.tool_instances:
            raise ValueError(f"Tool {tool_name} not found")
            
        tool_instance = self.tool_instances[tool_name]
        
        start_time = time.time()
        result = None
        error = None
        
        try:
            if hasattr(tool_instance, 'execute'):
                # For tool objects
                result = tool_instance.execute(**arguments)
            elif callable(tool_instance):
                # For function objects
                result = tool_instance(**arguments)
            else:
                raise ValueError(f"Tool {tool_name} is not executable")
            
            # Record successful tool call
            execution_time = time.time() - start_time
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=result,
                execution_time=execution_time
            )
            
            return result
            
        except Exception as e:
            # Record failed tool call
            execution_time = time.time() - start_time
            error_msg = str(e)
            ToolCallTracker.get_instance().record_call(
                name=tool_name,
                arguments=arguments,
                result=None,
                execution_time=execution_time,
                )
            raise  # Re-raise the original exception
    
    xǁLiteAgentǁ_execute_tool__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_execute_tool__mutmut_1': xǁLiteAgentǁ_execute_tool__mutmut_1, 
        'xǁLiteAgentǁ_execute_tool__mutmut_2': xǁLiteAgentǁ_execute_tool__mutmut_2, 
        'xǁLiteAgentǁ_execute_tool__mutmut_3': xǁLiteAgentǁ_execute_tool__mutmut_3, 
        'xǁLiteAgentǁ_execute_tool__mutmut_4': xǁLiteAgentǁ_execute_tool__mutmut_4, 
        'xǁLiteAgentǁ_execute_tool__mutmut_5': xǁLiteAgentǁ_execute_tool__mutmut_5, 
        'xǁLiteAgentǁ_execute_tool__mutmut_6': xǁLiteAgentǁ_execute_tool__mutmut_6, 
        'xǁLiteAgentǁ_execute_tool__mutmut_7': xǁLiteAgentǁ_execute_tool__mutmut_7, 
        'xǁLiteAgentǁ_execute_tool__mutmut_8': xǁLiteAgentǁ_execute_tool__mutmut_8, 
        'xǁLiteAgentǁ_execute_tool__mutmut_9': xǁLiteAgentǁ_execute_tool__mutmut_9, 
        'xǁLiteAgentǁ_execute_tool__mutmut_10': xǁLiteAgentǁ_execute_tool__mutmut_10, 
        'xǁLiteAgentǁ_execute_tool__mutmut_11': xǁLiteAgentǁ_execute_tool__mutmut_11, 
        'xǁLiteAgentǁ_execute_tool__mutmut_12': xǁLiteAgentǁ_execute_tool__mutmut_12, 
        'xǁLiteAgentǁ_execute_tool__mutmut_13': xǁLiteAgentǁ_execute_tool__mutmut_13, 
        'xǁLiteAgentǁ_execute_tool__mutmut_14': xǁLiteAgentǁ_execute_tool__mutmut_14, 
        'xǁLiteAgentǁ_execute_tool__mutmut_15': xǁLiteAgentǁ_execute_tool__mutmut_15, 
        'xǁLiteAgentǁ_execute_tool__mutmut_16': xǁLiteAgentǁ_execute_tool__mutmut_16, 
        'xǁLiteAgentǁ_execute_tool__mutmut_17': xǁLiteAgentǁ_execute_tool__mutmut_17, 
        'xǁLiteAgentǁ_execute_tool__mutmut_18': xǁLiteAgentǁ_execute_tool__mutmut_18, 
        'xǁLiteAgentǁ_execute_tool__mutmut_19': xǁLiteAgentǁ_execute_tool__mutmut_19, 
        'xǁLiteAgentǁ_execute_tool__mutmut_20': xǁLiteAgentǁ_execute_tool__mutmut_20, 
        'xǁLiteAgentǁ_execute_tool__mutmut_21': xǁLiteAgentǁ_execute_tool__mutmut_21, 
        'xǁLiteAgentǁ_execute_tool__mutmut_22': xǁLiteAgentǁ_execute_tool__mutmut_22, 
        'xǁLiteAgentǁ_execute_tool__mutmut_23': xǁLiteAgentǁ_execute_tool__mutmut_23, 
        'xǁLiteAgentǁ_execute_tool__mutmut_24': xǁLiteAgentǁ_execute_tool__mutmut_24, 
        'xǁLiteAgentǁ_execute_tool__mutmut_25': xǁLiteAgentǁ_execute_tool__mutmut_25, 
        'xǁLiteAgentǁ_execute_tool__mutmut_26': xǁLiteAgentǁ_execute_tool__mutmut_26, 
        'xǁLiteAgentǁ_execute_tool__mutmut_27': xǁLiteAgentǁ_execute_tool__mutmut_27, 
        'xǁLiteAgentǁ_execute_tool__mutmut_28': xǁLiteAgentǁ_execute_tool__mutmut_28, 
        'xǁLiteAgentǁ_execute_tool__mutmut_29': xǁLiteAgentǁ_execute_tool__mutmut_29, 
        'xǁLiteAgentǁ_execute_tool__mutmut_30': xǁLiteAgentǁ_execute_tool__mutmut_30, 
        'xǁLiteAgentǁ_execute_tool__mutmut_31': xǁLiteAgentǁ_execute_tool__mutmut_31, 
        'xǁLiteAgentǁ_execute_tool__mutmut_32': xǁLiteAgentǁ_execute_tool__mutmut_32, 
        'xǁLiteAgentǁ_execute_tool__mutmut_33': xǁLiteAgentǁ_execute_tool__mutmut_33, 
        'xǁLiteAgentǁ_execute_tool__mutmut_34': xǁLiteAgentǁ_execute_tool__mutmut_34, 
        'xǁLiteAgentǁ_execute_tool__mutmut_35': xǁLiteAgentǁ_execute_tool__mutmut_35, 
        'xǁLiteAgentǁ_execute_tool__mutmut_36': xǁLiteAgentǁ_execute_tool__mutmut_36, 
        'xǁLiteAgentǁ_execute_tool__mutmut_37': xǁLiteAgentǁ_execute_tool__mutmut_37, 
        'xǁLiteAgentǁ_execute_tool__mutmut_38': xǁLiteAgentǁ_execute_tool__mutmut_38, 
        'xǁLiteAgentǁ_execute_tool__mutmut_39': xǁLiteAgentǁ_execute_tool__mutmut_39
    }
    
    def _execute_tool(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_execute_tool__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_execute_tool__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _execute_tool.__signature__ = _mutmut_signature(xǁLiteAgentǁ_execute_tool__mutmut_orig)
    xǁLiteAgentǁ_execute_tool__mutmut_orig.__name__ = 'xǁLiteAgentǁ_execute_tool'
    
    def xǁLiteAgentǁ_log__mutmut_orig(self, message: str) -> None:
        """
        Log a message if debug mode is enabled.
        
        Args:
            message: The message to log
        """
        if self.debug:
            logger.info(f"[{self.name}] {message}")
        
    
    def xǁLiteAgentǁ_log__mutmut_1(self, message: str) -> None:
        """
        Log a message if debug mode is enabled.
        
        Args:
            message: The message to log
        """
        if self.debug:
            logger.info(None)
        
    
    xǁLiteAgentǁ_log__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁ_log__mutmut_1': xǁLiteAgentǁ_log__mutmut_1
    }
    
    def _log(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁ_log__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁ_log__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log.__signature__ = _mutmut_signature(xǁLiteAgentǁ_log__mutmut_orig)
    xǁLiteAgentǁ_log__mutmut_orig.__name__ = 'xǁLiteAgentǁ_log'
    def xǁLiteAgentǁreset_memory__mutmut_orig(self) -> None:
        """Reset the agent's conversation memory."""
        self.memory.reset()
        self._log("Memory reset")
        
    def xǁLiteAgentǁreset_memory__mutmut_1(self) -> None:
        """Reset the agent's conversation memory."""
        self.memory.reset()
        self._log(None)
        
    def xǁLiteAgentǁreset_memory__mutmut_2(self) -> None:
        """Reset the agent's conversation memory."""
        self.memory.reset()
        self._log("XXMemory resetXX")
        
    def xǁLiteAgentǁreset_memory__mutmut_3(self) -> None:
        """Reset the agent's conversation memory."""
        self.memory.reset()
        self._log("memory reset")
        
    def xǁLiteAgentǁreset_memory__mutmut_4(self) -> None:
        """Reset the agent's conversation memory."""
        self.memory.reset()
        self._log("MEMORY RESET")
        
    
    xǁLiteAgentǁreset_memory__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁreset_memory__mutmut_1': xǁLiteAgentǁreset_memory__mutmut_1, 
        'xǁLiteAgentǁreset_memory__mutmut_2': xǁLiteAgentǁreset_memory__mutmut_2, 
        'xǁLiteAgentǁreset_memory__mutmut_3': xǁLiteAgentǁreset_memory__mutmut_3, 
        'xǁLiteAgentǁreset_memory__mutmut_4': xǁLiteAgentǁreset_memory__mutmut_4
    }
    
    def reset_memory(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁreset_memory__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁreset_memory__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset_memory.__signature__ = _mutmut_signature(xǁLiteAgentǁreset_memory__mutmut_orig)
    xǁLiteAgentǁreset_memory__mutmut_orig.__name__ = 'xǁLiteAgentǁreset_memory'
    def get_memory(self) -> ConversationMemory:
        """Get the agent's conversation memory."""
        return self.memory
        
    def get_tools(self) -> Dict[str, Dict]:
        """Get the agent's registered tools."""
        return self.tools.copy()
        
    def xǁLiteAgentǁadd_tool__mutmut_orig(self, tool) -> None:
        """
        Add a single tool to the agent.
        
        Args:
            tool: The tool to add
        """
        self._register_tools([tool])
        
    def xǁLiteAgentǁadd_tool__mutmut_1(self, tool) -> None:
        """
        Add a single tool to the agent.
        
        Args:
            tool: The tool to add
        """
        self._register_tools(None)
        
    
    xǁLiteAgentǁadd_tool__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁadd_tool__mutmut_1': xǁLiteAgentǁadd_tool__mutmut_1
    }
    
    def add_tool(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁadd_tool__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁadd_tool__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_tool.__signature__ = _mutmut_signature(xǁLiteAgentǁadd_tool__mutmut_orig)
    xǁLiteAgentǁadd_tool__mutmut_orig.__name__ = 'xǁLiteAgentǁadd_tool'
    def xǁLiteAgentǁremove_tool__mutmut_orig(self, tool_name: str) -> None:
        """
        Remove a tool from the agent.
        
        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
        if tool_name in self.tool_instances:
            del self.tool_instances[tool_name]
        self._log(f"Removed tool: {tool_name}")
    def xǁLiteAgentǁremove_tool__mutmut_1(self, tool_name: str) -> None:
        """
        Remove a tool from the agent.
        
        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name not in self.tools:
            del self.tools[tool_name]
        if tool_name in self.tool_instances:
            del self.tool_instances[tool_name]
        self._log(f"Removed tool: {tool_name}")
    def xǁLiteAgentǁremove_tool__mutmut_2(self, tool_name: str) -> None:
        """
        Remove a tool from the agent.
        
        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
        if tool_name not in self.tool_instances:
            del self.tool_instances[tool_name]
        self._log(f"Removed tool: {tool_name}")
    def xǁLiteAgentǁremove_tool__mutmut_3(self, tool_name: str) -> None:
        """
        Remove a tool from the agent.
        
        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
        if tool_name in self.tool_instances:
            del self.tool_instances[tool_name]
        self._log(None)
    
    xǁLiteAgentǁremove_tool__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLiteAgentǁremove_tool__mutmut_1': xǁLiteAgentǁremove_tool__mutmut_1, 
        'xǁLiteAgentǁremove_tool__mutmut_2': xǁLiteAgentǁremove_tool__mutmut_2, 
        'xǁLiteAgentǁremove_tool__mutmut_3': xǁLiteAgentǁremove_tool__mutmut_3
    }
    
    def remove_tool(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLiteAgentǁremove_tool__mutmut_orig"), object.__getattribute__(self, "xǁLiteAgentǁremove_tool__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_tool.__signature__ = _mutmut_signature(xǁLiteAgentǁremove_tool__mutmut_orig)
    xǁLiteAgentǁremove_tool__mutmut_orig.__name__ = 'xǁLiteAgentǁremove_tool'


# Backward compatibility alias
LiteAgentNew = LiteAgent