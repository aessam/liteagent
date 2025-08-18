"""
Simplified observer pattern implementation for LiteAgent.

This module provides a streamlined observer interface and implementation for tracking
agent operations and tool usage.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TextIO, Set
import uuid
import time
import json
import os
import sys
from collections import defaultdict
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

# ---- Event Classes ----

class AgentEvent:
    """Base class for all agent events."""
    
    def xǁAgentEventǁ__init____mutmut_orig(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_1(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = None
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_2(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = None
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_3(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = None
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_4(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = None
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_5(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = None
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_6(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp and time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_7(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = None
        self.event_data = event_data or {}
    
    def xǁAgentEventǁ__init____mutmut_8(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = None
    
    def xǁAgentEventǁ__init____mutmut_9(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None,
                 event_data: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
            event_data: Additional event-specific data
            **kwargs: Additional keyword arguments for backward compatibility
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
        self.event_data = event_data and {}
    
    xǁAgentEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentEventǁ__init____mutmut_1': xǁAgentEventǁ__init____mutmut_1, 
        'xǁAgentEventǁ__init____mutmut_2': xǁAgentEventǁ__init____mutmut_2, 
        'xǁAgentEventǁ__init____mutmut_3': xǁAgentEventǁ__init____mutmut_3, 
        'xǁAgentEventǁ__init____mutmut_4': xǁAgentEventǁ__init____mutmut_4, 
        'xǁAgentEventǁ__init____mutmut_5': xǁAgentEventǁ__init____mutmut_5, 
        'xǁAgentEventǁ__init____mutmut_6': xǁAgentEventǁ__init____mutmut_6, 
        'xǁAgentEventǁ__init____mutmut_7': xǁAgentEventǁ__init____mutmut_7, 
        'xǁAgentEventǁ__init____mutmut_8': xǁAgentEventǁ__init____mutmut_8, 
        'xǁAgentEventǁ__init____mutmut_9': xǁAgentEventǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentEventǁ__init____mutmut_orig)
    xǁAgentEventǁ__init____mutmut_orig.__name__ = 'xǁAgentEventǁ__init__'
    
    def xǁAgentEventǁto_dict__mutmut_orig(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_1(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = None
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_2(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "XXevent_typeXX": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_3(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "EVENT_TYPE": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_4(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "XXagent_idXX": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_5(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "AGENT_ID": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_6(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "XXagent_nameXX": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_7(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "AGENT_NAME": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_8(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "XXcontext_idXX": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_9(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "CONTEXT_ID": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_10(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "XXtimestampXX": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_11(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "TIMESTAMP": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_12(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = None
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_13(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["XXparent_context_idXX"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_14(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["PARENT_CONTEXT_ID"] = self.parent_context_id
            
        # Add event-specific data
        result.update(self.event_data)
        
        return result
    
    def xǁAgentEventǁto_dict__mutmut_15(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "timestamp": self.timestamp
        }
        
        if self.parent_context_id:
            result["parent_context_id"] = self.parent_context_id
            
        # Add event-specific data
        result.update(None)
        
        return result
    
    xǁAgentEventǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentEventǁto_dict__mutmut_1': xǁAgentEventǁto_dict__mutmut_1, 
        'xǁAgentEventǁto_dict__mutmut_2': xǁAgentEventǁto_dict__mutmut_2, 
        'xǁAgentEventǁto_dict__mutmut_3': xǁAgentEventǁto_dict__mutmut_3, 
        'xǁAgentEventǁto_dict__mutmut_4': xǁAgentEventǁto_dict__mutmut_4, 
        'xǁAgentEventǁto_dict__mutmut_5': xǁAgentEventǁto_dict__mutmut_5, 
        'xǁAgentEventǁto_dict__mutmut_6': xǁAgentEventǁto_dict__mutmut_6, 
        'xǁAgentEventǁto_dict__mutmut_7': xǁAgentEventǁto_dict__mutmut_7, 
        'xǁAgentEventǁto_dict__mutmut_8': xǁAgentEventǁto_dict__mutmut_8, 
        'xǁAgentEventǁto_dict__mutmut_9': xǁAgentEventǁto_dict__mutmut_9, 
        'xǁAgentEventǁto_dict__mutmut_10': xǁAgentEventǁto_dict__mutmut_10, 
        'xǁAgentEventǁto_dict__mutmut_11': xǁAgentEventǁto_dict__mutmut_11, 
        'xǁAgentEventǁto_dict__mutmut_12': xǁAgentEventǁto_dict__mutmut_12, 
        'xǁAgentEventǁto_dict__mutmut_13': xǁAgentEventǁto_dict__mutmut_13, 
        'xǁAgentEventǁto_dict__mutmut_14': xǁAgentEventǁto_dict__mutmut_14, 
        'xǁAgentEventǁto_dict__mutmut_15': xǁAgentEventǁto_dict__mutmut_15
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentEventǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁAgentEventǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁAgentEventǁto_dict__mutmut_orig)
    xǁAgentEventǁto_dict__mutmut_orig.__name__ = 'xǁAgentEventǁto_dict'
    
    def __str__(self) -> str:
        """Convert event to string representation."""
        return f"{self.event_type}(agent={self.agent_name}, context={self.context_id})"


# Specialized event types
class AgentInitializedEvent(AgentEvent):
    """Event fired when an agent is initialized."""
    
    def xǁAgentInitializedEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = None
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name and kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model and model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get(None, 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', None)
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', )
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('XXmodel_nameXX', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('MODEL_NAME', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'XXunknownXX')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'UNKNOWN')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "XXmodelXX": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_23(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "MODEL": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_24(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "XXsystem_promptXX": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_25(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "SYSTEM_PROMPT": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_26(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt and kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_27(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get(None, ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_28(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', None),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_29(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get(''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_30(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_31(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('XXsystem_promptXX', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_32(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('SYSTEM_PROMPT', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_33(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', 'XXXX'),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_34(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "XXtoolsXX": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_35(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "TOOLS": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_36(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools and kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_37(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get(None, [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_38(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', None)
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_39(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get([])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_40(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', )
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_41(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('XXtoolsXX', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_42(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('TOOLS', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_43(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = None  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_44(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = None
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_45(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt and kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_46(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get(None, '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_47(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', None)
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_48(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_49(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', )
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_50(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('XXsystem_promptXX', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_51(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('SYSTEM_PROMPT', '')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_52(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', 'XXXX')
        self.tools = tools or kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_53(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = None
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_54(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools and kwargs.get('tools', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_55(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get(None, [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_56(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', None)
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_57(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get([])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_58(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('tools', )
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_59(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('XXtoolsXX', [])
        
    
    def xǁAgentInitializedEventǁ__init____mutmut_60(self, agent_id: str, agent_name: str, context_id: str, 
                 model: Optional[str] = None, system_prompt: Optional[str] = None, tools: Optional[List[str]] = None,
                 parent_context_id: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        """Initialize an agent initialized event."""
        # Handle backward compatibility
        model = model or model_name or kwargs.get('model_name', 'unknown')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "system_prompt": system_prompt or kwargs.get('system_prompt', ''),
                "tools": tools or kwargs.get('tools', [])
            }
        )
        self.model_name = model  # For backward compatibility
        self.system_prompt = system_prompt or kwargs.get('system_prompt', '')
        self.tools = tools or kwargs.get('TOOLS', [])
        
    
    xǁAgentInitializedEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentInitializedEventǁ__init____mutmut_1': xǁAgentInitializedEventǁ__init____mutmut_1, 
        'xǁAgentInitializedEventǁ__init____mutmut_2': xǁAgentInitializedEventǁ__init____mutmut_2, 
        'xǁAgentInitializedEventǁ__init____mutmut_3': xǁAgentInitializedEventǁ__init____mutmut_3, 
        'xǁAgentInitializedEventǁ__init____mutmut_4': xǁAgentInitializedEventǁ__init____mutmut_4, 
        'xǁAgentInitializedEventǁ__init____mutmut_5': xǁAgentInitializedEventǁ__init____mutmut_5, 
        'xǁAgentInitializedEventǁ__init____mutmut_6': xǁAgentInitializedEventǁ__init____mutmut_6, 
        'xǁAgentInitializedEventǁ__init____mutmut_7': xǁAgentInitializedEventǁ__init____mutmut_7, 
        'xǁAgentInitializedEventǁ__init____mutmut_8': xǁAgentInitializedEventǁ__init____mutmut_8, 
        'xǁAgentInitializedEventǁ__init____mutmut_9': xǁAgentInitializedEventǁ__init____mutmut_9, 
        'xǁAgentInitializedEventǁ__init____mutmut_10': xǁAgentInitializedEventǁ__init____mutmut_10, 
        'xǁAgentInitializedEventǁ__init____mutmut_11': xǁAgentInitializedEventǁ__init____mutmut_11, 
        'xǁAgentInitializedEventǁ__init____mutmut_12': xǁAgentInitializedEventǁ__init____mutmut_12, 
        'xǁAgentInitializedEventǁ__init____mutmut_13': xǁAgentInitializedEventǁ__init____mutmut_13, 
        'xǁAgentInitializedEventǁ__init____mutmut_14': xǁAgentInitializedEventǁ__init____mutmut_14, 
        'xǁAgentInitializedEventǁ__init____mutmut_15': xǁAgentInitializedEventǁ__init____mutmut_15, 
        'xǁAgentInitializedEventǁ__init____mutmut_16': xǁAgentInitializedEventǁ__init____mutmut_16, 
        'xǁAgentInitializedEventǁ__init____mutmut_17': xǁAgentInitializedEventǁ__init____mutmut_17, 
        'xǁAgentInitializedEventǁ__init____mutmut_18': xǁAgentInitializedEventǁ__init____mutmut_18, 
        'xǁAgentInitializedEventǁ__init____mutmut_19': xǁAgentInitializedEventǁ__init____mutmut_19, 
        'xǁAgentInitializedEventǁ__init____mutmut_20': xǁAgentInitializedEventǁ__init____mutmut_20, 
        'xǁAgentInitializedEventǁ__init____mutmut_21': xǁAgentInitializedEventǁ__init____mutmut_21, 
        'xǁAgentInitializedEventǁ__init____mutmut_22': xǁAgentInitializedEventǁ__init____mutmut_22, 
        'xǁAgentInitializedEventǁ__init____mutmut_23': xǁAgentInitializedEventǁ__init____mutmut_23, 
        'xǁAgentInitializedEventǁ__init____mutmut_24': xǁAgentInitializedEventǁ__init____mutmut_24, 
        'xǁAgentInitializedEventǁ__init____mutmut_25': xǁAgentInitializedEventǁ__init____mutmut_25, 
        'xǁAgentInitializedEventǁ__init____mutmut_26': xǁAgentInitializedEventǁ__init____mutmut_26, 
        'xǁAgentInitializedEventǁ__init____mutmut_27': xǁAgentInitializedEventǁ__init____mutmut_27, 
        'xǁAgentInitializedEventǁ__init____mutmut_28': xǁAgentInitializedEventǁ__init____mutmut_28, 
        'xǁAgentInitializedEventǁ__init____mutmut_29': xǁAgentInitializedEventǁ__init____mutmut_29, 
        'xǁAgentInitializedEventǁ__init____mutmut_30': xǁAgentInitializedEventǁ__init____mutmut_30, 
        'xǁAgentInitializedEventǁ__init____mutmut_31': xǁAgentInitializedEventǁ__init____mutmut_31, 
        'xǁAgentInitializedEventǁ__init____mutmut_32': xǁAgentInitializedEventǁ__init____mutmut_32, 
        'xǁAgentInitializedEventǁ__init____mutmut_33': xǁAgentInitializedEventǁ__init____mutmut_33, 
        'xǁAgentInitializedEventǁ__init____mutmut_34': xǁAgentInitializedEventǁ__init____mutmut_34, 
        'xǁAgentInitializedEventǁ__init____mutmut_35': xǁAgentInitializedEventǁ__init____mutmut_35, 
        'xǁAgentInitializedEventǁ__init____mutmut_36': xǁAgentInitializedEventǁ__init____mutmut_36, 
        'xǁAgentInitializedEventǁ__init____mutmut_37': xǁAgentInitializedEventǁ__init____mutmut_37, 
        'xǁAgentInitializedEventǁ__init____mutmut_38': xǁAgentInitializedEventǁ__init____mutmut_38, 
        'xǁAgentInitializedEventǁ__init____mutmut_39': xǁAgentInitializedEventǁ__init____mutmut_39, 
        'xǁAgentInitializedEventǁ__init____mutmut_40': xǁAgentInitializedEventǁ__init____mutmut_40, 
        'xǁAgentInitializedEventǁ__init____mutmut_41': xǁAgentInitializedEventǁ__init____mutmut_41, 
        'xǁAgentInitializedEventǁ__init____mutmut_42': xǁAgentInitializedEventǁ__init____mutmut_42, 
        'xǁAgentInitializedEventǁ__init____mutmut_43': xǁAgentInitializedEventǁ__init____mutmut_43, 
        'xǁAgentInitializedEventǁ__init____mutmut_44': xǁAgentInitializedEventǁ__init____mutmut_44, 
        'xǁAgentInitializedEventǁ__init____mutmut_45': xǁAgentInitializedEventǁ__init____mutmut_45, 
        'xǁAgentInitializedEventǁ__init____mutmut_46': xǁAgentInitializedEventǁ__init____mutmut_46, 
        'xǁAgentInitializedEventǁ__init____mutmut_47': xǁAgentInitializedEventǁ__init____mutmut_47, 
        'xǁAgentInitializedEventǁ__init____mutmut_48': xǁAgentInitializedEventǁ__init____mutmut_48, 
        'xǁAgentInitializedEventǁ__init____mutmut_49': xǁAgentInitializedEventǁ__init____mutmut_49, 
        'xǁAgentInitializedEventǁ__init____mutmut_50': xǁAgentInitializedEventǁ__init____mutmut_50, 
        'xǁAgentInitializedEventǁ__init____mutmut_51': xǁAgentInitializedEventǁ__init____mutmut_51, 
        'xǁAgentInitializedEventǁ__init____mutmut_52': xǁAgentInitializedEventǁ__init____mutmut_52, 
        'xǁAgentInitializedEventǁ__init____mutmut_53': xǁAgentInitializedEventǁ__init____mutmut_53, 
        'xǁAgentInitializedEventǁ__init____mutmut_54': xǁAgentInitializedEventǁ__init____mutmut_54, 
        'xǁAgentInitializedEventǁ__init____mutmut_55': xǁAgentInitializedEventǁ__init____mutmut_55, 
        'xǁAgentInitializedEventǁ__init____mutmut_56': xǁAgentInitializedEventǁ__init____mutmut_56, 
        'xǁAgentInitializedEventǁ__init____mutmut_57': xǁAgentInitializedEventǁ__init____mutmut_57, 
        'xǁAgentInitializedEventǁ__init____mutmut_58': xǁAgentInitializedEventǁ__init____mutmut_58, 
        'xǁAgentInitializedEventǁ__init____mutmut_59': xǁAgentInitializedEventǁ__init____mutmut_59, 
        'xǁAgentInitializedEventǁ__init____mutmut_60': xǁAgentInitializedEventǁ__init____mutmut_60
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentInitializedEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentInitializedEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentInitializedEventǁ__init____mutmut_orig)
    xǁAgentInitializedEventǁ__init____mutmut_orig.__name__ = 'xǁAgentInitializedEventǁ__init__'
    def xǁAgentInitializedEventǁto_dict__mutmut_orig(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["model_name"] = self.model_name
        result["system_prompt"] = self.system_prompt
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_1(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = None
        # For backward compatibility, make sure these keys are included
        result["model_name"] = self.model_name
        result["system_prompt"] = self.system_prompt
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_2(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["model_name"] = None
        result["system_prompt"] = self.system_prompt
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_3(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["XXmodel_nameXX"] = self.model_name
        result["system_prompt"] = self.system_prompt
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_4(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["MODEL_NAME"] = self.model_name
        result["system_prompt"] = self.system_prompt
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_5(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["model_name"] = self.model_name
        result["system_prompt"] = None
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_6(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["model_name"] = self.model_name
        result["XXsystem_promptXX"] = self.system_prompt
        return result
    def xǁAgentInitializedEventǁto_dict__mutmut_7(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["model_name"] = self.model_name
        result["SYSTEM_PROMPT"] = self.system_prompt
        return result
    
    xǁAgentInitializedEventǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentInitializedEventǁto_dict__mutmut_1': xǁAgentInitializedEventǁto_dict__mutmut_1, 
        'xǁAgentInitializedEventǁto_dict__mutmut_2': xǁAgentInitializedEventǁto_dict__mutmut_2, 
        'xǁAgentInitializedEventǁto_dict__mutmut_3': xǁAgentInitializedEventǁto_dict__mutmut_3, 
        'xǁAgentInitializedEventǁto_dict__mutmut_4': xǁAgentInitializedEventǁto_dict__mutmut_4, 
        'xǁAgentInitializedEventǁto_dict__mutmut_5': xǁAgentInitializedEventǁto_dict__mutmut_5, 
        'xǁAgentInitializedEventǁto_dict__mutmut_6': xǁAgentInitializedEventǁto_dict__mutmut_6, 
        'xǁAgentInitializedEventǁto_dict__mutmut_7': xǁAgentInitializedEventǁto_dict__mutmut_7
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentInitializedEventǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁAgentInitializedEventǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁAgentInitializedEventǁto_dict__mutmut_orig)
    xǁAgentInitializedEventǁto_dict__mutmut_orig.__name__ = 'xǁAgentInitializedEventǁto_dict'


class UserMessageEvent(AgentEvent):
    """Event fired when a user sends a message to an agent."""
    
    def xǁUserMessageEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = None
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message and kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get(None, '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', None)
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', )
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('XXmessageXX', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('MESSAGE', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', 'XXXX')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data={"message": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"XXmessageXX": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"MESSAGE": message}
        )
        self.message = message
    
    def xǁUserMessageEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str,
                 message: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a user message event."""
        message = message or kwargs.get('message', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"message": message}
        )
        self.message = None
    
    xǁUserMessageEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserMessageEventǁ__init____mutmut_1': xǁUserMessageEventǁ__init____mutmut_1, 
        'xǁUserMessageEventǁ__init____mutmut_2': xǁUserMessageEventǁ__init____mutmut_2, 
        'xǁUserMessageEventǁ__init____mutmut_3': xǁUserMessageEventǁ__init____mutmut_3, 
        'xǁUserMessageEventǁ__init____mutmut_4': xǁUserMessageEventǁ__init____mutmut_4, 
        'xǁUserMessageEventǁ__init____mutmut_5': xǁUserMessageEventǁ__init____mutmut_5, 
        'xǁUserMessageEventǁ__init____mutmut_6': xǁUserMessageEventǁ__init____mutmut_6, 
        'xǁUserMessageEventǁ__init____mutmut_7': xǁUserMessageEventǁ__init____mutmut_7, 
        'xǁUserMessageEventǁ__init____mutmut_8': xǁUserMessageEventǁ__init____mutmut_8, 
        'xǁUserMessageEventǁ__init____mutmut_9': xǁUserMessageEventǁ__init____mutmut_9, 
        'xǁUserMessageEventǁ__init____mutmut_10': xǁUserMessageEventǁ__init____mutmut_10, 
        'xǁUserMessageEventǁ__init____mutmut_11': xǁUserMessageEventǁ__init____mutmut_11, 
        'xǁUserMessageEventǁ__init____mutmut_12': xǁUserMessageEventǁ__init____mutmut_12, 
        'xǁUserMessageEventǁ__init____mutmut_13': xǁUserMessageEventǁ__init____mutmut_13, 
        'xǁUserMessageEventǁ__init____mutmut_14': xǁUserMessageEventǁ__init____mutmut_14, 
        'xǁUserMessageEventǁ__init____mutmut_15': xǁUserMessageEventǁ__init____mutmut_15, 
        'xǁUserMessageEventǁ__init____mutmut_16': xǁUserMessageEventǁ__init____mutmut_16, 
        'xǁUserMessageEventǁ__init____mutmut_17': xǁUserMessageEventǁ__init____mutmut_17, 
        'xǁUserMessageEventǁ__init____mutmut_18': xǁUserMessageEventǁ__init____mutmut_18, 
        'xǁUserMessageEventǁ__init____mutmut_19': xǁUserMessageEventǁ__init____mutmut_19, 
        'xǁUserMessageEventǁ__init____mutmut_20': xǁUserMessageEventǁ__init____mutmut_20, 
        'xǁUserMessageEventǁ__init____mutmut_21': xǁUserMessageEventǁ__init____mutmut_21, 
        'xǁUserMessageEventǁ__init____mutmut_22': xǁUserMessageEventǁ__init____mutmut_22
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserMessageEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁUserMessageEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁUserMessageEventǁ__init____mutmut_orig)
    xǁUserMessageEventǁ__init____mutmut_orig.__name__ = 'xǁUserMessageEventǁ__init__'


class ModelRequestEvent(AgentEvent):
    """Event fired when a request is sent to a model."""
    
    def xǁModelRequestEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = None
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages and kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get(None, [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', None)
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get([])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', )
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('XXmessagesXX', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('MESSAGES', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = None
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "XXmessagesXX": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "MESSAGES": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "XXmodelXX": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "MODEL": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model and kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get(None, 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', None)
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', )
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('XXmodelXX', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('MODEL', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'XXunknownXX')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'UNKNOWN')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_23(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions and 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_24(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'XXfunctionsXX' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_25(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'FUNCTIONS' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_26(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' not in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_27(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = None
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_28(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["XXfunctionsXX"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_29(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["FUNCTIONS"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_30(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions and kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_31(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get(None, [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_32(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', None)
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_33(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get([])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_34(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', )
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_35(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('XXfunctionsXX', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_36(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('FUNCTIONS', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_37(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_38(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_39(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_40(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_41(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_42(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_43(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_44(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_45(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_46(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_47(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = None
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_48(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = None
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_49(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model and kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_50(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get(None, 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_51(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', None)
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_52(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_53(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', )
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_54(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('XXmodelXX', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_55(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('MODEL', 'unknown')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_56(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'XXunknownXX')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_57(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'UNKNOWN')
        self.functions = functions or kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_58(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = None  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_59(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions and kwargs.get('functions', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_60(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get(None, [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_61(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', None)  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_62(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get([])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_63(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('functions', )  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_64(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('XXfunctionsXX', [])  # For backward compatibility
    
    def xǁModelRequestEventǁ__init____mutmut_65(self, agent_id: str, agent_name: str, context_id: str,
                 messages: Optional[List[Dict[str, Any]]] = None, model: Optional[str] = None,
                 parent_context_id: Optional[str] = None, functions: Optional[List[Dict]] = None, **kwargs):
        """Initialize a model request event."""
        messages = messages or kwargs.get('messages', [])
        
        event_data = {
            "messages": messages,
            "model": model or kwargs.get('model', 'unknown')
        }
        
        # For backward compatibility, also include functions if provided
        if functions or 'functions' in kwargs:
            event_data["functions"] = functions or kwargs.get('functions', [])
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.messages = messages
        self.model = model or kwargs.get('model', 'unknown')
        self.functions = functions or kwargs.get('FUNCTIONS', [])  # For backward compatibility
    
    xǁModelRequestEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁModelRequestEventǁ__init____mutmut_1': xǁModelRequestEventǁ__init____mutmut_1, 
        'xǁModelRequestEventǁ__init____mutmut_2': xǁModelRequestEventǁ__init____mutmut_2, 
        'xǁModelRequestEventǁ__init____mutmut_3': xǁModelRequestEventǁ__init____mutmut_3, 
        'xǁModelRequestEventǁ__init____mutmut_4': xǁModelRequestEventǁ__init____mutmut_4, 
        'xǁModelRequestEventǁ__init____mutmut_5': xǁModelRequestEventǁ__init____mutmut_5, 
        'xǁModelRequestEventǁ__init____mutmut_6': xǁModelRequestEventǁ__init____mutmut_6, 
        'xǁModelRequestEventǁ__init____mutmut_7': xǁModelRequestEventǁ__init____mutmut_7, 
        'xǁModelRequestEventǁ__init____mutmut_8': xǁModelRequestEventǁ__init____mutmut_8, 
        'xǁModelRequestEventǁ__init____mutmut_9': xǁModelRequestEventǁ__init____mutmut_9, 
        'xǁModelRequestEventǁ__init____mutmut_10': xǁModelRequestEventǁ__init____mutmut_10, 
        'xǁModelRequestEventǁ__init____mutmut_11': xǁModelRequestEventǁ__init____mutmut_11, 
        'xǁModelRequestEventǁ__init____mutmut_12': xǁModelRequestEventǁ__init____mutmut_12, 
        'xǁModelRequestEventǁ__init____mutmut_13': xǁModelRequestEventǁ__init____mutmut_13, 
        'xǁModelRequestEventǁ__init____mutmut_14': xǁModelRequestEventǁ__init____mutmut_14, 
        'xǁModelRequestEventǁ__init____mutmut_15': xǁModelRequestEventǁ__init____mutmut_15, 
        'xǁModelRequestEventǁ__init____mutmut_16': xǁModelRequestEventǁ__init____mutmut_16, 
        'xǁModelRequestEventǁ__init____mutmut_17': xǁModelRequestEventǁ__init____mutmut_17, 
        'xǁModelRequestEventǁ__init____mutmut_18': xǁModelRequestEventǁ__init____mutmut_18, 
        'xǁModelRequestEventǁ__init____mutmut_19': xǁModelRequestEventǁ__init____mutmut_19, 
        'xǁModelRequestEventǁ__init____mutmut_20': xǁModelRequestEventǁ__init____mutmut_20, 
        'xǁModelRequestEventǁ__init____mutmut_21': xǁModelRequestEventǁ__init____mutmut_21, 
        'xǁModelRequestEventǁ__init____mutmut_22': xǁModelRequestEventǁ__init____mutmut_22, 
        'xǁModelRequestEventǁ__init____mutmut_23': xǁModelRequestEventǁ__init____mutmut_23, 
        'xǁModelRequestEventǁ__init____mutmut_24': xǁModelRequestEventǁ__init____mutmut_24, 
        'xǁModelRequestEventǁ__init____mutmut_25': xǁModelRequestEventǁ__init____mutmut_25, 
        'xǁModelRequestEventǁ__init____mutmut_26': xǁModelRequestEventǁ__init____mutmut_26, 
        'xǁModelRequestEventǁ__init____mutmut_27': xǁModelRequestEventǁ__init____mutmut_27, 
        'xǁModelRequestEventǁ__init____mutmut_28': xǁModelRequestEventǁ__init____mutmut_28, 
        'xǁModelRequestEventǁ__init____mutmut_29': xǁModelRequestEventǁ__init____mutmut_29, 
        'xǁModelRequestEventǁ__init____mutmut_30': xǁModelRequestEventǁ__init____mutmut_30, 
        'xǁModelRequestEventǁ__init____mutmut_31': xǁModelRequestEventǁ__init____mutmut_31, 
        'xǁModelRequestEventǁ__init____mutmut_32': xǁModelRequestEventǁ__init____mutmut_32, 
        'xǁModelRequestEventǁ__init____mutmut_33': xǁModelRequestEventǁ__init____mutmut_33, 
        'xǁModelRequestEventǁ__init____mutmut_34': xǁModelRequestEventǁ__init____mutmut_34, 
        'xǁModelRequestEventǁ__init____mutmut_35': xǁModelRequestEventǁ__init____mutmut_35, 
        'xǁModelRequestEventǁ__init____mutmut_36': xǁModelRequestEventǁ__init____mutmut_36, 
        'xǁModelRequestEventǁ__init____mutmut_37': xǁModelRequestEventǁ__init____mutmut_37, 
        'xǁModelRequestEventǁ__init____mutmut_38': xǁModelRequestEventǁ__init____mutmut_38, 
        'xǁModelRequestEventǁ__init____mutmut_39': xǁModelRequestEventǁ__init____mutmut_39, 
        'xǁModelRequestEventǁ__init____mutmut_40': xǁModelRequestEventǁ__init____mutmut_40, 
        'xǁModelRequestEventǁ__init____mutmut_41': xǁModelRequestEventǁ__init____mutmut_41, 
        'xǁModelRequestEventǁ__init____mutmut_42': xǁModelRequestEventǁ__init____mutmut_42, 
        'xǁModelRequestEventǁ__init____mutmut_43': xǁModelRequestEventǁ__init____mutmut_43, 
        'xǁModelRequestEventǁ__init____mutmut_44': xǁModelRequestEventǁ__init____mutmut_44, 
        'xǁModelRequestEventǁ__init____mutmut_45': xǁModelRequestEventǁ__init____mutmut_45, 
        'xǁModelRequestEventǁ__init____mutmut_46': xǁModelRequestEventǁ__init____mutmut_46, 
        'xǁModelRequestEventǁ__init____mutmut_47': xǁModelRequestEventǁ__init____mutmut_47, 
        'xǁModelRequestEventǁ__init____mutmut_48': xǁModelRequestEventǁ__init____mutmut_48, 
        'xǁModelRequestEventǁ__init____mutmut_49': xǁModelRequestEventǁ__init____mutmut_49, 
        'xǁModelRequestEventǁ__init____mutmut_50': xǁModelRequestEventǁ__init____mutmut_50, 
        'xǁModelRequestEventǁ__init____mutmut_51': xǁModelRequestEventǁ__init____mutmut_51, 
        'xǁModelRequestEventǁ__init____mutmut_52': xǁModelRequestEventǁ__init____mutmut_52, 
        'xǁModelRequestEventǁ__init____mutmut_53': xǁModelRequestEventǁ__init____mutmut_53, 
        'xǁModelRequestEventǁ__init____mutmut_54': xǁModelRequestEventǁ__init____mutmut_54, 
        'xǁModelRequestEventǁ__init____mutmut_55': xǁModelRequestEventǁ__init____mutmut_55, 
        'xǁModelRequestEventǁ__init____mutmut_56': xǁModelRequestEventǁ__init____mutmut_56, 
        'xǁModelRequestEventǁ__init____mutmut_57': xǁModelRequestEventǁ__init____mutmut_57, 
        'xǁModelRequestEventǁ__init____mutmut_58': xǁModelRequestEventǁ__init____mutmut_58, 
        'xǁModelRequestEventǁ__init____mutmut_59': xǁModelRequestEventǁ__init____mutmut_59, 
        'xǁModelRequestEventǁ__init____mutmut_60': xǁModelRequestEventǁ__init____mutmut_60, 
        'xǁModelRequestEventǁ__init____mutmut_61': xǁModelRequestEventǁ__init____mutmut_61, 
        'xǁModelRequestEventǁ__init____mutmut_62': xǁModelRequestEventǁ__init____mutmut_62, 
        'xǁModelRequestEventǁ__init____mutmut_63': xǁModelRequestEventǁ__init____mutmut_63, 
        'xǁModelRequestEventǁ__init____mutmut_64': xǁModelRequestEventǁ__init____mutmut_64, 
        'xǁModelRequestEventǁ__init____mutmut_65': xǁModelRequestEventǁ__init____mutmut_65
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁModelRequestEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁModelRequestEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁModelRequestEventǁ__init____mutmut_orig)
    xǁModelRequestEventǁ__init____mutmut_orig.__name__ = 'xǁModelRequestEventǁ__init__'


class ModelResponseEvent(AgentEvent):
    """Event fired when a response is received from a model."""
    
    def xǁModelResponseEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = None
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response and kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get(None)
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('XXresponseXX')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('RESPONSE')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = None
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model and kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get(None, 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', None)
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', )
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('XXmodelXX', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('MODEL', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'XXunknownXX')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'UNKNOWN')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_23(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_24(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_25(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_26(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "XXmodelXX": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_27(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "MODEL": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_28(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "XXresponse_summaryXX": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_29(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "RESPONSE_SUMMARY": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_30(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] - "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_31(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(None)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_32(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:101] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_33(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "XX...XX" if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_34(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response or len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_35(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) >= 100 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_36(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 101 else str(response or "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_37(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(None)
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_38(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response and "")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_39(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "XXXX")
            }
        )
        self.response = response
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_40(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = None
        self.model = model
        
    
    def xǁModelResponseEventǁ__init____mutmut_41(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[Any] = None, model: Optional[str] = None, 
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a model response event."""
        # For backward compatibility
        response = response or kwargs.get('response')
        model = model or kwargs.get('model', 'unknown')
        
        # Don't include full response in event_data to avoid serialization issues
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "model": model,
                "response_summary": str(response)[:100] + "..." if response and len(str(response)) > 100 else str(response or "")
            }
        )
        self.response = response
        self.model = None
        
    
    xǁModelResponseEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁModelResponseEventǁ__init____mutmut_1': xǁModelResponseEventǁ__init____mutmut_1, 
        'xǁModelResponseEventǁ__init____mutmut_2': xǁModelResponseEventǁ__init____mutmut_2, 
        'xǁModelResponseEventǁ__init____mutmut_3': xǁModelResponseEventǁ__init____mutmut_3, 
        'xǁModelResponseEventǁ__init____mutmut_4': xǁModelResponseEventǁ__init____mutmut_4, 
        'xǁModelResponseEventǁ__init____mutmut_5': xǁModelResponseEventǁ__init____mutmut_5, 
        'xǁModelResponseEventǁ__init____mutmut_6': xǁModelResponseEventǁ__init____mutmut_6, 
        'xǁModelResponseEventǁ__init____mutmut_7': xǁModelResponseEventǁ__init____mutmut_7, 
        'xǁModelResponseEventǁ__init____mutmut_8': xǁModelResponseEventǁ__init____mutmut_8, 
        'xǁModelResponseEventǁ__init____mutmut_9': xǁModelResponseEventǁ__init____mutmut_9, 
        'xǁModelResponseEventǁ__init____mutmut_10': xǁModelResponseEventǁ__init____mutmut_10, 
        'xǁModelResponseEventǁ__init____mutmut_11': xǁModelResponseEventǁ__init____mutmut_11, 
        'xǁModelResponseEventǁ__init____mutmut_12': xǁModelResponseEventǁ__init____mutmut_12, 
        'xǁModelResponseEventǁ__init____mutmut_13': xǁModelResponseEventǁ__init____mutmut_13, 
        'xǁModelResponseEventǁ__init____mutmut_14': xǁModelResponseEventǁ__init____mutmut_14, 
        'xǁModelResponseEventǁ__init____mutmut_15': xǁModelResponseEventǁ__init____mutmut_15, 
        'xǁModelResponseEventǁ__init____mutmut_16': xǁModelResponseEventǁ__init____mutmut_16, 
        'xǁModelResponseEventǁ__init____mutmut_17': xǁModelResponseEventǁ__init____mutmut_17, 
        'xǁModelResponseEventǁ__init____mutmut_18': xǁModelResponseEventǁ__init____mutmut_18, 
        'xǁModelResponseEventǁ__init____mutmut_19': xǁModelResponseEventǁ__init____mutmut_19, 
        'xǁModelResponseEventǁ__init____mutmut_20': xǁModelResponseEventǁ__init____mutmut_20, 
        'xǁModelResponseEventǁ__init____mutmut_21': xǁModelResponseEventǁ__init____mutmut_21, 
        'xǁModelResponseEventǁ__init____mutmut_22': xǁModelResponseEventǁ__init____mutmut_22, 
        'xǁModelResponseEventǁ__init____mutmut_23': xǁModelResponseEventǁ__init____mutmut_23, 
        'xǁModelResponseEventǁ__init____mutmut_24': xǁModelResponseEventǁ__init____mutmut_24, 
        'xǁModelResponseEventǁ__init____mutmut_25': xǁModelResponseEventǁ__init____mutmut_25, 
        'xǁModelResponseEventǁ__init____mutmut_26': xǁModelResponseEventǁ__init____mutmut_26, 
        'xǁModelResponseEventǁ__init____mutmut_27': xǁModelResponseEventǁ__init____mutmut_27, 
        'xǁModelResponseEventǁ__init____mutmut_28': xǁModelResponseEventǁ__init____mutmut_28, 
        'xǁModelResponseEventǁ__init____mutmut_29': xǁModelResponseEventǁ__init____mutmut_29, 
        'xǁModelResponseEventǁ__init____mutmut_30': xǁModelResponseEventǁ__init____mutmut_30, 
        'xǁModelResponseEventǁ__init____mutmut_31': xǁModelResponseEventǁ__init____mutmut_31, 
        'xǁModelResponseEventǁ__init____mutmut_32': xǁModelResponseEventǁ__init____mutmut_32, 
        'xǁModelResponseEventǁ__init____mutmut_33': xǁModelResponseEventǁ__init____mutmut_33, 
        'xǁModelResponseEventǁ__init____mutmut_34': xǁModelResponseEventǁ__init____mutmut_34, 
        'xǁModelResponseEventǁ__init____mutmut_35': xǁModelResponseEventǁ__init____mutmut_35, 
        'xǁModelResponseEventǁ__init____mutmut_36': xǁModelResponseEventǁ__init____mutmut_36, 
        'xǁModelResponseEventǁ__init____mutmut_37': xǁModelResponseEventǁ__init____mutmut_37, 
        'xǁModelResponseEventǁ__init____mutmut_38': xǁModelResponseEventǁ__init____mutmut_38, 
        'xǁModelResponseEventǁ__init____mutmut_39': xǁModelResponseEventǁ__init____mutmut_39, 
        'xǁModelResponseEventǁ__init____mutmut_40': xǁModelResponseEventǁ__init____mutmut_40, 
        'xǁModelResponseEventǁ__init____mutmut_41': xǁModelResponseEventǁ__init____mutmut_41
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁModelResponseEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁModelResponseEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁModelResponseEventǁ__init____mutmut_orig)
    xǁModelResponseEventǁ__init____mutmut_orig.__name__ = 'xǁModelResponseEventǁ__init__'
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_orig(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_1(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = None
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_2(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_3(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(None, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_4(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, None):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_5(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr('to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_6(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, ):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_7(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'XXto_dictXX'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_8(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'TO_DICT'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_9(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = None
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_10(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(None, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_11(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, None):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_12(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr('__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_13(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, ):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_14(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, 'XX__dict__XX'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_15(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__DICT__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_16(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = None
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_17(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = None
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_18(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(None)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_19(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = None
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_20(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(None)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_21(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = None
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_22(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["XXresponseXX"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_23(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["RESPONSE"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_24(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["response"] = ""
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_25(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["XXresponseXX"] = None
            
        return result
    # Override to_dict for backward compatibility
    def xǁModelResponseEventǁto_dict__mutmut_26(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects for backward compatibility
        if self.response is not None:
            try:
                # Try to convert to dict if the response has a to_dict method
                if hasattr(self.response, 'to_dict'):
                    response_dict = self.response.to_dict()
                # Try to convert to dict if the response is a dictionary-like object
                elif hasattr(self.response, '__dict__'):
                    response_dict = self.response.__dict__
                # Otherwise, convert to string
                else:
                    response_dict = str(self.response)
            except Exception:
                # Fallback to string representation if conversion fails
                response_dict = str(self.response)
                
            result["response"] = response_dict
        else:
            # Make sure response is always in the dict, even if None
            result["RESPONSE"] = None
            
        return result
    
    xǁModelResponseEventǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁModelResponseEventǁto_dict__mutmut_1': xǁModelResponseEventǁto_dict__mutmut_1, 
        'xǁModelResponseEventǁto_dict__mutmut_2': xǁModelResponseEventǁto_dict__mutmut_2, 
        'xǁModelResponseEventǁto_dict__mutmut_3': xǁModelResponseEventǁto_dict__mutmut_3, 
        'xǁModelResponseEventǁto_dict__mutmut_4': xǁModelResponseEventǁto_dict__mutmut_4, 
        'xǁModelResponseEventǁto_dict__mutmut_5': xǁModelResponseEventǁto_dict__mutmut_5, 
        'xǁModelResponseEventǁto_dict__mutmut_6': xǁModelResponseEventǁto_dict__mutmut_6, 
        'xǁModelResponseEventǁto_dict__mutmut_7': xǁModelResponseEventǁto_dict__mutmut_7, 
        'xǁModelResponseEventǁto_dict__mutmut_8': xǁModelResponseEventǁto_dict__mutmut_8, 
        'xǁModelResponseEventǁto_dict__mutmut_9': xǁModelResponseEventǁto_dict__mutmut_9, 
        'xǁModelResponseEventǁto_dict__mutmut_10': xǁModelResponseEventǁto_dict__mutmut_10, 
        'xǁModelResponseEventǁto_dict__mutmut_11': xǁModelResponseEventǁto_dict__mutmut_11, 
        'xǁModelResponseEventǁto_dict__mutmut_12': xǁModelResponseEventǁto_dict__mutmut_12, 
        'xǁModelResponseEventǁto_dict__mutmut_13': xǁModelResponseEventǁto_dict__mutmut_13, 
        'xǁModelResponseEventǁto_dict__mutmut_14': xǁModelResponseEventǁto_dict__mutmut_14, 
        'xǁModelResponseEventǁto_dict__mutmut_15': xǁModelResponseEventǁto_dict__mutmut_15, 
        'xǁModelResponseEventǁto_dict__mutmut_16': xǁModelResponseEventǁto_dict__mutmut_16, 
        'xǁModelResponseEventǁto_dict__mutmut_17': xǁModelResponseEventǁto_dict__mutmut_17, 
        'xǁModelResponseEventǁto_dict__mutmut_18': xǁModelResponseEventǁto_dict__mutmut_18, 
        'xǁModelResponseEventǁto_dict__mutmut_19': xǁModelResponseEventǁto_dict__mutmut_19, 
        'xǁModelResponseEventǁto_dict__mutmut_20': xǁModelResponseEventǁto_dict__mutmut_20, 
        'xǁModelResponseEventǁto_dict__mutmut_21': xǁModelResponseEventǁto_dict__mutmut_21, 
        'xǁModelResponseEventǁto_dict__mutmut_22': xǁModelResponseEventǁto_dict__mutmut_22, 
        'xǁModelResponseEventǁto_dict__mutmut_23': xǁModelResponseEventǁto_dict__mutmut_23, 
        'xǁModelResponseEventǁto_dict__mutmut_24': xǁModelResponseEventǁto_dict__mutmut_24, 
        'xǁModelResponseEventǁto_dict__mutmut_25': xǁModelResponseEventǁto_dict__mutmut_25, 
        'xǁModelResponseEventǁto_dict__mutmut_26': xǁModelResponseEventǁto_dict__mutmut_26
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁModelResponseEventǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁModelResponseEventǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁModelResponseEventǁto_dict__mutmut_orig)
    xǁModelResponseEventǁto_dict__mutmut_orig.__name__ = 'xǁModelResponseEventǁto_dict'


class FunctionCallEvent(AgentEvent):
    """Event fired when a function is called."""
    
    def xǁFunctionCallEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = None
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name and kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get(None, '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', None)
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', )
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('XXfunction_nameXX', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('FUNCTION_NAME', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', 'XXXX')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = None
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args and kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get(None, {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', None)
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get({})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', )
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('XXfunction_argsXX', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('FUNCTION_ARGS', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = None
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id and kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get(None, str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', None)
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get(str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_23(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', )
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_24(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('XXfunction_call_idXX', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_25(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('FUNCTION_CALL_ID', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_26(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(None))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_27(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_28(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_29(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_30(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_31(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_32(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_33(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_34(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_35(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_36(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_37(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "XXfunction_nameXX": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_38(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "FUNCTION_NAME": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_39(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "XXfunction_argsXX": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_40(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "FUNCTION_ARGS": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_41(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "XXfunction_call_idXX": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_42(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "FUNCTION_CALL_ID": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_43(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = None
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_44(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = None
        self.function_call_id = function_call_id
    
    def xǁFunctionCallEventǁ__init____mutmut_45(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None, 
                 function_call_id: Optional[str] = None,
                 parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function call event."""
        function_name = function_name or kwargs.get('function_name', '')
        function_args = function_args or kwargs.get('function_args', {})
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={
                "function_name": function_name,
                "function_args": function_args,
                "function_call_id": function_call_id
            }
        )
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = None
    
    xǁFunctionCallEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionCallEventǁ__init____mutmut_1': xǁFunctionCallEventǁ__init____mutmut_1, 
        'xǁFunctionCallEventǁ__init____mutmut_2': xǁFunctionCallEventǁ__init____mutmut_2, 
        'xǁFunctionCallEventǁ__init____mutmut_3': xǁFunctionCallEventǁ__init____mutmut_3, 
        'xǁFunctionCallEventǁ__init____mutmut_4': xǁFunctionCallEventǁ__init____mutmut_4, 
        'xǁFunctionCallEventǁ__init____mutmut_5': xǁFunctionCallEventǁ__init____mutmut_5, 
        'xǁFunctionCallEventǁ__init____mutmut_6': xǁFunctionCallEventǁ__init____mutmut_6, 
        'xǁFunctionCallEventǁ__init____mutmut_7': xǁFunctionCallEventǁ__init____mutmut_7, 
        'xǁFunctionCallEventǁ__init____mutmut_8': xǁFunctionCallEventǁ__init____mutmut_8, 
        'xǁFunctionCallEventǁ__init____mutmut_9': xǁFunctionCallEventǁ__init____mutmut_9, 
        'xǁFunctionCallEventǁ__init____mutmut_10': xǁFunctionCallEventǁ__init____mutmut_10, 
        'xǁFunctionCallEventǁ__init____mutmut_11': xǁFunctionCallEventǁ__init____mutmut_11, 
        'xǁFunctionCallEventǁ__init____mutmut_12': xǁFunctionCallEventǁ__init____mutmut_12, 
        'xǁFunctionCallEventǁ__init____mutmut_13': xǁFunctionCallEventǁ__init____mutmut_13, 
        'xǁFunctionCallEventǁ__init____mutmut_14': xǁFunctionCallEventǁ__init____mutmut_14, 
        'xǁFunctionCallEventǁ__init____mutmut_15': xǁFunctionCallEventǁ__init____mutmut_15, 
        'xǁFunctionCallEventǁ__init____mutmut_16': xǁFunctionCallEventǁ__init____mutmut_16, 
        'xǁFunctionCallEventǁ__init____mutmut_17': xǁFunctionCallEventǁ__init____mutmut_17, 
        'xǁFunctionCallEventǁ__init____mutmut_18': xǁFunctionCallEventǁ__init____mutmut_18, 
        'xǁFunctionCallEventǁ__init____mutmut_19': xǁFunctionCallEventǁ__init____mutmut_19, 
        'xǁFunctionCallEventǁ__init____mutmut_20': xǁFunctionCallEventǁ__init____mutmut_20, 
        'xǁFunctionCallEventǁ__init____mutmut_21': xǁFunctionCallEventǁ__init____mutmut_21, 
        'xǁFunctionCallEventǁ__init____mutmut_22': xǁFunctionCallEventǁ__init____mutmut_22, 
        'xǁFunctionCallEventǁ__init____mutmut_23': xǁFunctionCallEventǁ__init____mutmut_23, 
        'xǁFunctionCallEventǁ__init____mutmut_24': xǁFunctionCallEventǁ__init____mutmut_24, 
        'xǁFunctionCallEventǁ__init____mutmut_25': xǁFunctionCallEventǁ__init____mutmut_25, 
        'xǁFunctionCallEventǁ__init____mutmut_26': xǁFunctionCallEventǁ__init____mutmut_26, 
        'xǁFunctionCallEventǁ__init____mutmut_27': xǁFunctionCallEventǁ__init____mutmut_27, 
        'xǁFunctionCallEventǁ__init____mutmut_28': xǁFunctionCallEventǁ__init____mutmut_28, 
        'xǁFunctionCallEventǁ__init____mutmut_29': xǁFunctionCallEventǁ__init____mutmut_29, 
        'xǁFunctionCallEventǁ__init____mutmut_30': xǁFunctionCallEventǁ__init____mutmut_30, 
        'xǁFunctionCallEventǁ__init____mutmut_31': xǁFunctionCallEventǁ__init____mutmut_31, 
        'xǁFunctionCallEventǁ__init____mutmut_32': xǁFunctionCallEventǁ__init____mutmut_32, 
        'xǁFunctionCallEventǁ__init____mutmut_33': xǁFunctionCallEventǁ__init____mutmut_33, 
        'xǁFunctionCallEventǁ__init____mutmut_34': xǁFunctionCallEventǁ__init____mutmut_34, 
        'xǁFunctionCallEventǁ__init____mutmut_35': xǁFunctionCallEventǁ__init____mutmut_35, 
        'xǁFunctionCallEventǁ__init____mutmut_36': xǁFunctionCallEventǁ__init____mutmut_36, 
        'xǁFunctionCallEventǁ__init____mutmut_37': xǁFunctionCallEventǁ__init____mutmut_37, 
        'xǁFunctionCallEventǁ__init____mutmut_38': xǁFunctionCallEventǁ__init____mutmut_38, 
        'xǁFunctionCallEventǁ__init____mutmut_39': xǁFunctionCallEventǁ__init____mutmut_39, 
        'xǁFunctionCallEventǁ__init____mutmut_40': xǁFunctionCallEventǁ__init____mutmut_40, 
        'xǁFunctionCallEventǁ__init____mutmut_41': xǁFunctionCallEventǁ__init____mutmut_41, 
        'xǁFunctionCallEventǁ__init____mutmut_42': xǁFunctionCallEventǁ__init____mutmut_42, 
        'xǁFunctionCallEventǁ__init____mutmut_43': xǁFunctionCallEventǁ__init____mutmut_43, 
        'xǁFunctionCallEventǁ__init____mutmut_44': xǁFunctionCallEventǁ__init____mutmut_44, 
        'xǁFunctionCallEventǁ__init____mutmut_45': xǁFunctionCallEventǁ__init____mutmut_45
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionCallEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionCallEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionCallEventǁ__init____mutmut_orig)
    xǁFunctionCallEventǁ__init____mutmut_orig.__name__ = 'xǁFunctionCallEventǁ__init__'


class FunctionResultEvent(AgentEvent):
    """Event fired when a function call returns a result."""
    
    def xǁFunctionResultEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = None
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name and kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get(None, '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', None)
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', )
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('XXfunction_nameXX', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('FUNCTION_NAME', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', 'XXXX')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = None
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result and kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get(None)
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('XXresultXX')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('RESULT')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = None
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id and kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get(None, str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', None)
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get(str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', )
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('XXfunction_call_idXX', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('FUNCTION_CALL_ID', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_23(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(None))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_24(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = None
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_25(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error and kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_26(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get(None)
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_27(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('XXerrorXX')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_28(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('ERROR')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_29(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = None
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_30(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "XXfunction_nameXX": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_31(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "FUNCTION_NAME": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_32(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "XXfunction_call_idXX": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_33(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "FUNCTION_CALL_ID": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_34(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "XXresult_summaryXX": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_35(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "RESULT_SUMMARY": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_36(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] - "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_37(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(None)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_38(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:101] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_39(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "XX...XX" if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_40(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None or len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_41(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_42(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) >= 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_43(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 101 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_44(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(None)
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_45(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result and "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_46(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "XXXX")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_47(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args and kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_48(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get(None):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_49(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('XXfunction_argsXX'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_50(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('FUNCTION_ARGS'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_51(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = None
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_52(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["XXfunction_argsXX"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_53(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["FUNCTION_ARGS"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_54(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args and kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_55(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get(None, {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_56(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', None)
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_57(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get({})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_58(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', )
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_59(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('XXfunction_argsXX', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_60(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('FUNCTION_ARGS', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_61(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = None
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_62(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["XXerrorXX"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_63(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["ERROR"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_64(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_65(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_66(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_67(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_68(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_69(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_70(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_71(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_72(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_73(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_74(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = None
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_75(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = None
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_76(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = None
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_77(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = None
        self.function_args = function_args or kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_78(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = None  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_79(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args and kwargs.get('function_args', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_80(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get(None, {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_81(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', None)  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_82(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get({})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_83(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('function_args', )  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_84(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('XXfunction_argsXX', {})  # For backward compatibility
        
    
    def xǁFunctionResultEventǁ__init____mutmut_85(self, agent_id: str, agent_name: str, context_id: str,
                 function_name: Optional[str] = None, result: Optional[Any] = None, 
                 function_call_id: Optional[str] = None, function_args: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize a function result event."""
        function_name = function_name or kwargs.get('function_name', '')
        result = result or kwargs.get('result')
        function_call_id = function_call_id or kwargs.get('function_call_id', str(uuid.uuid4()))
        error = error or kwargs.get('error')
        
        # Don't include full result in event_data to avoid serialization issues
        event_data = {
            "function_name": function_name,
            "function_call_id": function_call_id,
            "result_summary": str(result)[:100] + "..." if result is not None and len(str(result)) > 100 else str(result or "")
        }
        
        # For backward compatibility
        if function_args or kwargs.get('function_args'):
            event_data["function_args"] = function_args or kwargs.get('function_args', {})
        
        if error:
            event_data["error"] = error
            
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=event_data
        )
        self.function_name = function_name
        self.result = result
        self.function_call_id = function_call_id
        self.error = error
        self.function_args = function_args or kwargs.get('FUNCTION_ARGS', {})  # For backward compatibility
        
    
    xǁFunctionResultEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionResultEventǁ__init____mutmut_1': xǁFunctionResultEventǁ__init____mutmut_1, 
        'xǁFunctionResultEventǁ__init____mutmut_2': xǁFunctionResultEventǁ__init____mutmut_2, 
        'xǁFunctionResultEventǁ__init____mutmut_3': xǁFunctionResultEventǁ__init____mutmut_3, 
        'xǁFunctionResultEventǁ__init____mutmut_4': xǁFunctionResultEventǁ__init____mutmut_4, 
        'xǁFunctionResultEventǁ__init____mutmut_5': xǁFunctionResultEventǁ__init____mutmut_5, 
        'xǁFunctionResultEventǁ__init____mutmut_6': xǁFunctionResultEventǁ__init____mutmut_6, 
        'xǁFunctionResultEventǁ__init____mutmut_7': xǁFunctionResultEventǁ__init____mutmut_7, 
        'xǁFunctionResultEventǁ__init____mutmut_8': xǁFunctionResultEventǁ__init____mutmut_8, 
        'xǁFunctionResultEventǁ__init____mutmut_9': xǁFunctionResultEventǁ__init____mutmut_9, 
        'xǁFunctionResultEventǁ__init____mutmut_10': xǁFunctionResultEventǁ__init____mutmut_10, 
        'xǁFunctionResultEventǁ__init____mutmut_11': xǁFunctionResultEventǁ__init____mutmut_11, 
        'xǁFunctionResultEventǁ__init____mutmut_12': xǁFunctionResultEventǁ__init____mutmut_12, 
        'xǁFunctionResultEventǁ__init____mutmut_13': xǁFunctionResultEventǁ__init____mutmut_13, 
        'xǁFunctionResultEventǁ__init____mutmut_14': xǁFunctionResultEventǁ__init____mutmut_14, 
        'xǁFunctionResultEventǁ__init____mutmut_15': xǁFunctionResultEventǁ__init____mutmut_15, 
        'xǁFunctionResultEventǁ__init____mutmut_16': xǁFunctionResultEventǁ__init____mutmut_16, 
        'xǁFunctionResultEventǁ__init____mutmut_17': xǁFunctionResultEventǁ__init____mutmut_17, 
        'xǁFunctionResultEventǁ__init____mutmut_18': xǁFunctionResultEventǁ__init____mutmut_18, 
        'xǁFunctionResultEventǁ__init____mutmut_19': xǁFunctionResultEventǁ__init____mutmut_19, 
        'xǁFunctionResultEventǁ__init____mutmut_20': xǁFunctionResultEventǁ__init____mutmut_20, 
        'xǁFunctionResultEventǁ__init____mutmut_21': xǁFunctionResultEventǁ__init____mutmut_21, 
        'xǁFunctionResultEventǁ__init____mutmut_22': xǁFunctionResultEventǁ__init____mutmut_22, 
        'xǁFunctionResultEventǁ__init____mutmut_23': xǁFunctionResultEventǁ__init____mutmut_23, 
        'xǁFunctionResultEventǁ__init____mutmut_24': xǁFunctionResultEventǁ__init____mutmut_24, 
        'xǁFunctionResultEventǁ__init____mutmut_25': xǁFunctionResultEventǁ__init____mutmut_25, 
        'xǁFunctionResultEventǁ__init____mutmut_26': xǁFunctionResultEventǁ__init____mutmut_26, 
        'xǁFunctionResultEventǁ__init____mutmut_27': xǁFunctionResultEventǁ__init____mutmut_27, 
        'xǁFunctionResultEventǁ__init____mutmut_28': xǁFunctionResultEventǁ__init____mutmut_28, 
        'xǁFunctionResultEventǁ__init____mutmut_29': xǁFunctionResultEventǁ__init____mutmut_29, 
        'xǁFunctionResultEventǁ__init____mutmut_30': xǁFunctionResultEventǁ__init____mutmut_30, 
        'xǁFunctionResultEventǁ__init____mutmut_31': xǁFunctionResultEventǁ__init____mutmut_31, 
        'xǁFunctionResultEventǁ__init____mutmut_32': xǁFunctionResultEventǁ__init____mutmut_32, 
        'xǁFunctionResultEventǁ__init____mutmut_33': xǁFunctionResultEventǁ__init____mutmut_33, 
        'xǁFunctionResultEventǁ__init____mutmut_34': xǁFunctionResultEventǁ__init____mutmut_34, 
        'xǁFunctionResultEventǁ__init____mutmut_35': xǁFunctionResultEventǁ__init____mutmut_35, 
        'xǁFunctionResultEventǁ__init____mutmut_36': xǁFunctionResultEventǁ__init____mutmut_36, 
        'xǁFunctionResultEventǁ__init____mutmut_37': xǁFunctionResultEventǁ__init____mutmut_37, 
        'xǁFunctionResultEventǁ__init____mutmut_38': xǁFunctionResultEventǁ__init____mutmut_38, 
        'xǁFunctionResultEventǁ__init____mutmut_39': xǁFunctionResultEventǁ__init____mutmut_39, 
        'xǁFunctionResultEventǁ__init____mutmut_40': xǁFunctionResultEventǁ__init____mutmut_40, 
        'xǁFunctionResultEventǁ__init____mutmut_41': xǁFunctionResultEventǁ__init____mutmut_41, 
        'xǁFunctionResultEventǁ__init____mutmut_42': xǁFunctionResultEventǁ__init____mutmut_42, 
        'xǁFunctionResultEventǁ__init____mutmut_43': xǁFunctionResultEventǁ__init____mutmut_43, 
        'xǁFunctionResultEventǁ__init____mutmut_44': xǁFunctionResultEventǁ__init____mutmut_44, 
        'xǁFunctionResultEventǁ__init____mutmut_45': xǁFunctionResultEventǁ__init____mutmut_45, 
        'xǁFunctionResultEventǁ__init____mutmut_46': xǁFunctionResultEventǁ__init____mutmut_46, 
        'xǁFunctionResultEventǁ__init____mutmut_47': xǁFunctionResultEventǁ__init____mutmut_47, 
        'xǁFunctionResultEventǁ__init____mutmut_48': xǁFunctionResultEventǁ__init____mutmut_48, 
        'xǁFunctionResultEventǁ__init____mutmut_49': xǁFunctionResultEventǁ__init____mutmut_49, 
        'xǁFunctionResultEventǁ__init____mutmut_50': xǁFunctionResultEventǁ__init____mutmut_50, 
        'xǁFunctionResultEventǁ__init____mutmut_51': xǁFunctionResultEventǁ__init____mutmut_51, 
        'xǁFunctionResultEventǁ__init____mutmut_52': xǁFunctionResultEventǁ__init____mutmut_52, 
        'xǁFunctionResultEventǁ__init____mutmut_53': xǁFunctionResultEventǁ__init____mutmut_53, 
        'xǁFunctionResultEventǁ__init____mutmut_54': xǁFunctionResultEventǁ__init____mutmut_54, 
        'xǁFunctionResultEventǁ__init____mutmut_55': xǁFunctionResultEventǁ__init____mutmut_55, 
        'xǁFunctionResultEventǁ__init____mutmut_56': xǁFunctionResultEventǁ__init____mutmut_56, 
        'xǁFunctionResultEventǁ__init____mutmut_57': xǁFunctionResultEventǁ__init____mutmut_57, 
        'xǁFunctionResultEventǁ__init____mutmut_58': xǁFunctionResultEventǁ__init____mutmut_58, 
        'xǁFunctionResultEventǁ__init____mutmut_59': xǁFunctionResultEventǁ__init____mutmut_59, 
        'xǁFunctionResultEventǁ__init____mutmut_60': xǁFunctionResultEventǁ__init____mutmut_60, 
        'xǁFunctionResultEventǁ__init____mutmut_61': xǁFunctionResultEventǁ__init____mutmut_61, 
        'xǁFunctionResultEventǁ__init____mutmut_62': xǁFunctionResultEventǁ__init____mutmut_62, 
        'xǁFunctionResultEventǁ__init____mutmut_63': xǁFunctionResultEventǁ__init____mutmut_63, 
        'xǁFunctionResultEventǁ__init____mutmut_64': xǁFunctionResultEventǁ__init____mutmut_64, 
        'xǁFunctionResultEventǁ__init____mutmut_65': xǁFunctionResultEventǁ__init____mutmut_65, 
        'xǁFunctionResultEventǁ__init____mutmut_66': xǁFunctionResultEventǁ__init____mutmut_66, 
        'xǁFunctionResultEventǁ__init____mutmut_67': xǁFunctionResultEventǁ__init____mutmut_67, 
        'xǁFunctionResultEventǁ__init____mutmut_68': xǁFunctionResultEventǁ__init____mutmut_68, 
        'xǁFunctionResultEventǁ__init____mutmut_69': xǁFunctionResultEventǁ__init____mutmut_69, 
        'xǁFunctionResultEventǁ__init____mutmut_70': xǁFunctionResultEventǁ__init____mutmut_70, 
        'xǁFunctionResultEventǁ__init____mutmut_71': xǁFunctionResultEventǁ__init____mutmut_71, 
        'xǁFunctionResultEventǁ__init____mutmut_72': xǁFunctionResultEventǁ__init____mutmut_72, 
        'xǁFunctionResultEventǁ__init____mutmut_73': xǁFunctionResultEventǁ__init____mutmut_73, 
        'xǁFunctionResultEventǁ__init____mutmut_74': xǁFunctionResultEventǁ__init____mutmut_74, 
        'xǁFunctionResultEventǁ__init____mutmut_75': xǁFunctionResultEventǁ__init____mutmut_75, 
        'xǁFunctionResultEventǁ__init____mutmut_76': xǁFunctionResultEventǁ__init____mutmut_76, 
        'xǁFunctionResultEventǁ__init____mutmut_77': xǁFunctionResultEventǁ__init____mutmut_77, 
        'xǁFunctionResultEventǁ__init____mutmut_78': xǁFunctionResultEventǁ__init____mutmut_78, 
        'xǁFunctionResultEventǁ__init____mutmut_79': xǁFunctionResultEventǁ__init____mutmut_79, 
        'xǁFunctionResultEventǁ__init____mutmut_80': xǁFunctionResultEventǁ__init____mutmut_80, 
        'xǁFunctionResultEventǁ__init____mutmut_81': xǁFunctionResultEventǁ__init____mutmut_81, 
        'xǁFunctionResultEventǁ__init____mutmut_82': xǁFunctionResultEventǁ__init____mutmut_82, 
        'xǁFunctionResultEventǁ__init____mutmut_83': xǁFunctionResultEventǁ__init____mutmut_83, 
        'xǁFunctionResultEventǁ__init____mutmut_84': xǁFunctionResultEventǁ__init____mutmut_84, 
        'xǁFunctionResultEventǁ__init____mutmut_85': xǁFunctionResultEventǁ__init____mutmut_85
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionResultEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionResultEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionResultEventǁ__init____mutmut_orig)
    xǁFunctionResultEventǁ__init____mutmut_orig.__name__ = 'xǁFunctionResultEventǁ__init__'
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_orig(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_1(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = None
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_2(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_3(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(None)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_4(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = None
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_5(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = None
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_6(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(None)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_7(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = ""
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_8(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update(None)
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_9(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "XXfunction_argsXX": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_10(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "FUNCTION_ARGS": self.function_args,
            "result": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_11(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "XXresultXX": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_12(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "RESULT": serialized_result,
            "error": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_13(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "XXerrorXX": self.error  # Always include error, even if None
        })
            
        return result_dict
    # Override to_dict for backward compatibility
    def xǁFunctionResultEventǁto_dict__mutmut_14(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable for backward compatibility
        if self.result is not None:
            try:
                # Test if it's directly serializable
                json.dumps(self.result)
                serialized_result = self.result
            except (TypeError, OverflowError):
                # If not, convert to string
                serialized_result = str(self.result)
        else:
            serialized_result = None
        
        # Add fields expected by older code    
        result_dict.update({
            "function_args": self.function_args,
            "result": serialized_result,
            "ERROR": self.error  # Always include error, even if None
        })
            
        return result_dict
    
    xǁFunctionResultEventǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionResultEventǁto_dict__mutmut_1': xǁFunctionResultEventǁto_dict__mutmut_1, 
        'xǁFunctionResultEventǁto_dict__mutmut_2': xǁFunctionResultEventǁto_dict__mutmut_2, 
        'xǁFunctionResultEventǁto_dict__mutmut_3': xǁFunctionResultEventǁto_dict__mutmut_3, 
        'xǁFunctionResultEventǁto_dict__mutmut_4': xǁFunctionResultEventǁto_dict__mutmut_4, 
        'xǁFunctionResultEventǁto_dict__mutmut_5': xǁFunctionResultEventǁto_dict__mutmut_5, 
        'xǁFunctionResultEventǁto_dict__mutmut_6': xǁFunctionResultEventǁto_dict__mutmut_6, 
        'xǁFunctionResultEventǁto_dict__mutmut_7': xǁFunctionResultEventǁto_dict__mutmut_7, 
        'xǁFunctionResultEventǁto_dict__mutmut_8': xǁFunctionResultEventǁto_dict__mutmut_8, 
        'xǁFunctionResultEventǁto_dict__mutmut_9': xǁFunctionResultEventǁto_dict__mutmut_9, 
        'xǁFunctionResultEventǁto_dict__mutmut_10': xǁFunctionResultEventǁto_dict__mutmut_10, 
        'xǁFunctionResultEventǁto_dict__mutmut_11': xǁFunctionResultEventǁto_dict__mutmut_11, 
        'xǁFunctionResultEventǁto_dict__mutmut_12': xǁFunctionResultEventǁto_dict__mutmut_12, 
        'xǁFunctionResultEventǁto_dict__mutmut_13': xǁFunctionResultEventǁto_dict__mutmut_13, 
        'xǁFunctionResultEventǁto_dict__mutmut_14': xǁFunctionResultEventǁto_dict__mutmut_14
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionResultEventǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁFunctionResultEventǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁFunctionResultEventǁto_dict__mutmut_orig)
    xǁFunctionResultEventǁto_dict__mutmut_orig.__name__ = 'xǁFunctionResultEventǁto_dict'


class AgentResponseEvent(AgentEvent):
    """Event fired when an agent generates a response."""
    
    def xǁAgentResponseEventǁ__init____mutmut_orig(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_1(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = None
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_2(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response and kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_3(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get(None, '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_4(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', None)
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_5(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_6(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', )
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_7(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('XXresponseXX', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_8(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('RESPONSE', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_9(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', 'XXXX')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_10(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=None,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_11(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=None,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_12(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=None,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_13(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=None,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_14(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data=None
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_15(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_16(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_17(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_18(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            event_data={"response": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_19(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_20(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"XXresponseXX": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_21(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"RESPONSE": response}
        )
        self.response = response
    
    def xǁAgentResponseEventǁ__init____mutmut_22(self, agent_id: str, agent_name: str, context_id: str,
                 response: Optional[str] = None, parent_context_id: Optional[str] = None, **kwargs):
        """Initialize an agent response event."""
        response = response or kwargs.get('response', '')
        
        super().__init__(
            agent_id=agent_id,
            agent_name=agent_name,
            context_id=context_id,
            parent_context_id=parent_context_id,
            event_data={"response": response}
        )
        self.response = None
    
    xǁAgentResponseEventǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentResponseEventǁ__init____mutmut_1': xǁAgentResponseEventǁ__init____mutmut_1, 
        'xǁAgentResponseEventǁ__init____mutmut_2': xǁAgentResponseEventǁ__init____mutmut_2, 
        'xǁAgentResponseEventǁ__init____mutmut_3': xǁAgentResponseEventǁ__init____mutmut_3, 
        'xǁAgentResponseEventǁ__init____mutmut_4': xǁAgentResponseEventǁ__init____mutmut_4, 
        'xǁAgentResponseEventǁ__init____mutmut_5': xǁAgentResponseEventǁ__init____mutmut_5, 
        'xǁAgentResponseEventǁ__init____mutmut_6': xǁAgentResponseEventǁ__init____mutmut_6, 
        'xǁAgentResponseEventǁ__init____mutmut_7': xǁAgentResponseEventǁ__init____mutmut_7, 
        'xǁAgentResponseEventǁ__init____mutmut_8': xǁAgentResponseEventǁ__init____mutmut_8, 
        'xǁAgentResponseEventǁ__init____mutmut_9': xǁAgentResponseEventǁ__init____mutmut_9, 
        'xǁAgentResponseEventǁ__init____mutmut_10': xǁAgentResponseEventǁ__init____mutmut_10, 
        'xǁAgentResponseEventǁ__init____mutmut_11': xǁAgentResponseEventǁ__init____mutmut_11, 
        'xǁAgentResponseEventǁ__init____mutmut_12': xǁAgentResponseEventǁ__init____mutmut_12, 
        'xǁAgentResponseEventǁ__init____mutmut_13': xǁAgentResponseEventǁ__init____mutmut_13, 
        'xǁAgentResponseEventǁ__init____mutmut_14': xǁAgentResponseEventǁ__init____mutmut_14, 
        'xǁAgentResponseEventǁ__init____mutmut_15': xǁAgentResponseEventǁ__init____mutmut_15, 
        'xǁAgentResponseEventǁ__init____mutmut_16': xǁAgentResponseEventǁ__init____mutmut_16, 
        'xǁAgentResponseEventǁ__init____mutmut_17': xǁAgentResponseEventǁ__init____mutmut_17, 
        'xǁAgentResponseEventǁ__init____mutmut_18': xǁAgentResponseEventǁ__init____mutmut_18, 
        'xǁAgentResponseEventǁ__init____mutmut_19': xǁAgentResponseEventǁ__init____mutmut_19, 
        'xǁAgentResponseEventǁ__init____mutmut_20': xǁAgentResponseEventǁ__init____mutmut_20, 
        'xǁAgentResponseEventǁ__init____mutmut_21': xǁAgentResponseEventǁ__init____mutmut_21, 
        'xǁAgentResponseEventǁ__init____mutmut_22': xǁAgentResponseEventǁ__init____mutmut_22
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentResponseEventǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentResponseEventǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentResponseEventǁ__init____mutmut_orig)
    xǁAgentResponseEventǁ__init____mutmut_orig.__name__ = 'xǁAgentResponseEventǁ__init__'


# ---- Observer Interface ----

class AgentObserver(ABC):
    """
    Observer interface for LiteAgent events.
    
    Implement this interface to receive events from LiteAgent instances.
    """
    
    @abstractmethod
    def on_event(self, event: AgentEvent) -> None:
        """
        Handle an agent event.
        
        Args:
            event: The event to handle
        """
        pass
    
    def xǁAgentObserverǁon_agent_initialized__mutmut_orig(self, event: AgentInitializedEvent) -> None:
        """Handle an agent initialized event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_agent_initialized__mutmut_1(self, event: AgentInitializedEvent) -> None:
        """Handle an agent initialized event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_agent_initialized__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_agent_initialized__mutmut_1': xǁAgentObserverǁon_agent_initialized__mutmut_1
    }
    
    def on_agent_initialized(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_agent_initialized__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_agent_initialized__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_agent_initialized.__signature__ = _mutmut_signature(xǁAgentObserverǁon_agent_initialized__mutmut_orig)
    xǁAgentObserverǁon_agent_initialized__mutmut_orig.__name__ = 'xǁAgentObserverǁon_agent_initialized'
    
    def xǁAgentObserverǁon_user_message__mutmut_orig(self, event: UserMessageEvent) -> None:
        """Handle a user message event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_user_message__mutmut_1(self, event: UserMessageEvent) -> None:
        """Handle a user message event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_user_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_user_message__mutmut_1': xǁAgentObserverǁon_user_message__mutmut_1
    }
    
    def on_user_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_user_message__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_user_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_user_message.__signature__ = _mutmut_signature(xǁAgentObserverǁon_user_message__mutmut_orig)
    xǁAgentObserverǁon_user_message__mutmut_orig.__name__ = 'xǁAgentObserverǁon_user_message'
    
    def xǁAgentObserverǁon_model_request__mutmut_orig(self, event: ModelRequestEvent) -> None:
        """Handle a model request event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_model_request__mutmut_1(self, event: ModelRequestEvent) -> None:
        """Handle a model request event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_model_request__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_model_request__mutmut_1': xǁAgentObserverǁon_model_request__mutmut_1
    }
    
    def on_model_request(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_model_request__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_model_request__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_model_request.__signature__ = _mutmut_signature(xǁAgentObserverǁon_model_request__mutmut_orig)
    xǁAgentObserverǁon_model_request__mutmut_orig.__name__ = 'xǁAgentObserverǁon_model_request'
    
    def xǁAgentObserverǁon_model_response__mutmut_orig(self, event: ModelResponseEvent) -> None:
        """Handle a model response event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_model_response__mutmut_1(self, event: ModelResponseEvent) -> None:
        """Handle a model response event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_model_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_model_response__mutmut_1': xǁAgentObserverǁon_model_response__mutmut_1
    }
    
    def on_model_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_model_response__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_model_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_model_response.__signature__ = _mutmut_signature(xǁAgentObserverǁon_model_response__mutmut_orig)
    xǁAgentObserverǁon_model_response__mutmut_orig.__name__ = 'xǁAgentObserverǁon_model_response'
    
    def xǁAgentObserverǁon_function_call__mutmut_orig(self, event: FunctionCallEvent) -> None:
        """Handle a function call event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_function_call__mutmut_1(self, event: FunctionCallEvent) -> None:
        """Handle a function call event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_function_call__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_function_call__mutmut_1': xǁAgentObserverǁon_function_call__mutmut_1
    }
    
    def on_function_call(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_function_call__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_function_call__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_function_call.__signature__ = _mutmut_signature(xǁAgentObserverǁon_function_call__mutmut_orig)
    xǁAgentObserverǁon_function_call__mutmut_orig.__name__ = 'xǁAgentObserverǁon_function_call'
    
    def xǁAgentObserverǁon_function_result__mutmut_orig(self, event: FunctionResultEvent) -> None:
        """Handle a function result event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_function_result__mutmut_1(self, event: FunctionResultEvent) -> None:
        """Handle a function result event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_function_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_function_result__mutmut_1': xǁAgentObserverǁon_function_result__mutmut_1
    }
    
    def on_function_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_function_result__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_function_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_function_result.__signature__ = _mutmut_signature(xǁAgentObserverǁon_function_result__mutmut_orig)
    xǁAgentObserverǁon_function_result__mutmut_orig.__name__ = 'xǁAgentObserverǁon_function_result'
    
    def xǁAgentObserverǁon_agent_response__mutmut_orig(self, event: AgentResponseEvent) -> None:
        """Handle an agent response event."""
        self.on_event(event)
    
    def xǁAgentObserverǁon_agent_response__mutmut_1(self, event: AgentResponseEvent) -> None:
        """Handle an agent response event."""
        self.on_event(None)
    
    xǁAgentObserverǁon_agent_response__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentObserverǁon_agent_response__mutmut_1': xǁAgentObserverǁon_agent_response__mutmut_1
    }
    
    def on_agent_response(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentObserverǁon_agent_response__mutmut_orig"), object.__getattribute__(self, "xǁAgentObserverǁon_agent_response__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_agent_response.__signature__ = _mutmut_signature(xǁAgentObserverǁon_agent_response__mutmut_orig)
    xǁAgentObserverǁon_agent_response__mutmut_orig.__name__ = 'xǁAgentObserverǁon_agent_response'


# ---- Unified Observer Implementation ----

class UnifiedObserver(AgentObserver):
    """
    Configurable observer that combines console, file, and tree trace functionality.
    
    This observer can be configured to log events to the console, a file, or both,
    and can also build a hierarchical trace of agent interactions.
    """
    
    def xǁUnifiedObserverǁ__init____mutmut_orig(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_1(self, 
                 console_output: bool = False,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_2(self, 
                 console_output: bool = True,
                 file_output: bool = True, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_3(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "XXagent_events.jsonlXX",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_4(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "AGENT_EVENTS.JSONL",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_5(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = True,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_6(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = True):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_7(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = None
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_8(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = None
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_9(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = None
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_10(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = None
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_11(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = None
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_12(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = None
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_13(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = None  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_14(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = None  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_15(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = None  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_16(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = None  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_17(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(None)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_18(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = None  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_19(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(None)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_20(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = None  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_21(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(None)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_22(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = None  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
    
    def xǁUnifiedObserverǁ__init____mutmut_23(self, 
                 console_output: bool = True,
                 file_output: bool = False, 
                 file_path: str = "agent_events.jsonl",
                 build_trace: bool = False,
                 verbose: bool = False):
        """
        Initialize a unified observer.
        
        Args:
            console_output: Whether to log events to the console
            file_output: Whether to log events to a file
            file_path: Path to the file to log events to
            build_trace: Whether to build a hierarchical trace of agent interactions
            verbose: Whether to include verbose details in console output
        """
        self.console_output = console_output
        self.file_output = file_output
        self.file_path = file_path
        self.build_trace = build_trace
        self.verbose = verbose
        
        # For tree trace
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.context_events = defaultdict(list)  # context_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = None  # function_call_id -> result event
    
    xǁUnifiedObserverǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ__init____mutmut_1': xǁUnifiedObserverǁ__init____mutmut_1, 
        'xǁUnifiedObserverǁ__init____mutmut_2': xǁUnifiedObserverǁ__init____mutmut_2, 
        'xǁUnifiedObserverǁ__init____mutmut_3': xǁUnifiedObserverǁ__init____mutmut_3, 
        'xǁUnifiedObserverǁ__init____mutmut_4': xǁUnifiedObserverǁ__init____mutmut_4, 
        'xǁUnifiedObserverǁ__init____mutmut_5': xǁUnifiedObserverǁ__init____mutmut_5, 
        'xǁUnifiedObserverǁ__init____mutmut_6': xǁUnifiedObserverǁ__init____mutmut_6, 
        'xǁUnifiedObserverǁ__init____mutmut_7': xǁUnifiedObserverǁ__init____mutmut_7, 
        'xǁUnifiedObserverǁ__init____mutmut_8': xǁUnifiedObserverǁ__init____mutmut_8, 
        'xǁUnifiedObserverǁ__init____mutmut_9': xǁUnifiedObserverǁ__init____mutmut_9, 
        'xǁUnifiedObserverǁ__init____mutmut_10': xǁUnifiedObserverǁ__init____mutmut_10, 
        'xǁUnifiedObserverǁ__init____mutmut_11': xǁUnifiedObserverǁ__init____mutmut_11, 
        'xǁUnifiedObserverǁ__init____mutmut_12': xǁUnifiedObserverǁ__init____mutmut_12, 
        'xǁUnifiedObserverǁ__init____mutmut_13': xǁUnifiedObserverǁ__init____mutmut_13, 
        'xǁUnifiedObserverǁ__init____mutmut_14': xǁUnifiedObserverǁ__init____mutmut_14, 
        'xǁUnifiedObserverǁ__init____mutmut_15': xǁUnifiedObserverǁ__init____mutmut_15, 
        'xǁUnifiedObserverǁ__init____mutmut_16': xǁUnifiedObserverǁ__init____mutmut_16, 
        'xǁUnifiedObserverǁ__init____mutmut_17': xǁUnifiedObserverǁ__init____mutmut_17, 
        'xǁUnifiedObserverǁ__init____mutmut_18': xǁUnifiedObserverǁ__init____mutmut_18, 
        'xǁUnifiedObserverǁ__init____mutmut_19': xǁUnifiedObserverǁ__init____mutmut_19, 
        'xǁUnifiedObserverǁ__init____mutmut_20': xǁUnifiedObserverǁ__init____mutmut_20, 
        'xǁUnifiedObserverǁ__init____mutmut_21': xǁUnifiedObserverǁ__init____mutmut_21, 
        'xǁUnifiedObserverǁ__init____mutmut_22': xǁUnifiedObserverǁ__init____mutmut_22, 
        'xǁUnifiedObserverǁ__init____mutmut_23': xǁUnifiedObserverǁ__init____mutmut_23
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ__init____mutmut_orig)
    xǁUnifiedObserverǁ__init____mutmut_orig.__name__ = 'xǁUnifiedObserverǁ__init__'
    
    def xǁUnifiedObserverǁon_event__mutmut_orig(self, event: AgentEvent) -> None:
        """Handle an agent event by delegating to the appropriate outputs."""
        # Store event for trace
        if self.build_trace:
            self._store_event_for_trace(event)
        
        # Log to console
        if self.console_output:
            self._log_to_console(event)
        
        # Log to file
        if self.file_output:
            self._log_to_file(event)
    
    def xǁUnifiedObserverǁon_event__mutmut_1(self, event: AgentEvent) -> None:
        """Handle an agent event by delegating to the appropriate outputs."""
        # Store event for trace
        if self.build_trace:
            self._store_event_for_trace(None)
        
        # Log to console
        if self.console_output:
            self._log_to_console(event)
        
        # Log to file
        if self.file_output:
            self._log_to_file(event)
    
    def xǁUnifiedObserverǁon_event__mutmut_2(self, event: AgentEvent) -> None:
        """Handle an agent event by delegating to the appropriate outputs."""
        # Store event for trace
        if self.build_trace:
            self._store_event_for_trace(event)
        
        # Log to console
        if self.console_output:
            self._log_to_console(None)
        
        # Log to file
        if self.file_output:
            self._log_to_file(event)
    
    def xǁUnifiedObserverǁon_event__mutmut_3(self, event: AgentEvent) -> None:
        """Handle an agent event by delegating to the appropriate outputs."""
        # Store event for trace
        if self.build_trace:
            self._store_event_for_trace(event)
        
        # Log to console
        if self.console_output:
            self._log_to_console(event)
        
        # Log to file
        if self.file_output:
            self._log_to_file(None)
    
    xǁUnifiedObserverǁon_event__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁon_event__mutmut_1': xǁUnifiedObserverǁon_event__mutmut_1, 
        'xǁUnifiedObserverǁon_event__mutmut_2': xǁUnifiedObserverǁon_event__mutmut_2, 
        'xǁUnifiedObserverǁon_event__mutmut_3': xǁUnifiedObserverǁon_event__mutmut_3
    }
    
    def on_event(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁon_event__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁon_event__mutmut_mutants"), args, kwargs, self)
        return result 
    
    on_event.__signature__ = _mutmut_signature(xǁUnifiedObserverǁon_event__mutmut_orig)
    xǁUnifiedObserverǁon_event__mutmut_orig.__name__ = 'xǁUnifiedObserverǁon_event'
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_orig(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_1(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(None)
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_2(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) or self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_3(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(None)
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_4(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(None)
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_5(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(None) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_6(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {'XX, XX'.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_7(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'XXNoneXX'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_8(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'none'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_9(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'NONE'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_10(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(None)
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_11(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(None)
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_12(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(None)
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_13(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(None)
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_14(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(None)
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_15(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(None)
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_16(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(None)
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_17(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose or event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_18(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(None)
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_19(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(None)
            
        print("")
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_20(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print(None)
    
    def xǁUnifiedObserverǁ_log_to_console__mutmut_21(self, event: AgentEvent) -> None:
        """Log an event to the console."""
        print(f"[{event.event_type}] Agent: {event.agent_name}")
        
        # Print event-specific details based on event type
        if isinstance(event, AgentInitializedEvent) and self.verbose:
            print(f"  Model: {event.model_name}")
            print(f"  Tools: {', '.join(event.tools) if event.tools else 'None'}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            if self.verbose:
                print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        if self.verbose and event.parent_context_id:
            print(f"  Context: {event.context_id}")
            print(f"  Parent Context: {event.parent_context_id}")
            
        print("XXXX")
    
    xǁUnifiedObserverǁ_log_to_console__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_log_to_console__mutmut_1': xǁUnifiedObserverǁ_log_to_console__mutmut_1, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_2': xǁUnifiedObserverǁ_log_to_console__mutmut_2, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_3': xǁUnifiedObserverǁ_log_to_console__mutmut_3, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_4': xǁUnifiedObserverǁ_log_to_console__mutmut_4, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_5': xǁUnifiedObserverǁ_log_to_console__mutmut_5, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_6': xǁUnifiedObserverǁ_log_to_console__mutmut_6, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_7': xǁUnifiedObserverǁ_log_to_console__mutmut_7, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_8': xǁUnifiedObserverǁ_log_to_console__mutmut_8, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_9': xǁUnifiedObserverǁ_log_to_console__mutmut_9, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_10': xǁUnifiedObserverǁ_log_to_console__mutmut_10, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_11': xǁUnifiedObserverǁ_log_to_console__mutmut_11, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_12': xǁUnifiedObserverǁ_log_to_console__mutmut_12, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_13': xǁUnifiedObserverǁ_log_to_console__mutmut_13, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_14': xǁUnifiedObserverǁ_log_to_console__mutmut_14, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_15': xǁUnifiedObserverǁ_log_to_console__mutmut_15, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_16': xǁUnifiedObserverǁ_log_to_console__mutmut_16, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_17': xǁUnifiedObserverǁ_log_to_console__mutmut_17, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_18': xǁUnifiedObserverǁ_log_to_console__mutmut_18, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_19': xǁUnifiedObserverǁ_log_to_console__mutmut_19, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_20': xǁUnifiedObserverǁ_log_to_console__mutmut_20, 
        'xǁUnifiedObserverǁ_log_to_console__mutmut_21': xǁUnifiedObserverǁ_log_to_console__mutmut_21
    }
    
    def _log_to_console(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_log_to_console__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_log_to_console__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log_to_console.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_log_to_console__mutmut_orig)
    xǁUnifiedObserverǁ_log_to_console__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_log_to_console'
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_orig(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_1(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = None
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_2(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(None, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_3(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, None) as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_4(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open('a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_5(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, ) as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_6(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'XXaXX') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_7(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'A') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_8(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(None)
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_9(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) - '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_10(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(None) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_11(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) + 'XX\nXX')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_12(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(None)
    
    def xǁUnifiedObserverǁ_log_to_file__mutmut_13(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(None)}")
    
    xǁUnifiedObserverǁ_log_to_file__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_log_to_file__mutmut_1': xǁUnifiedObserverǁ_log_to_file__mutmut_1, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_2': xǁUnifiedObserverǁ_log_to_file__mutmut_2, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_3': xǁUnifiedObserverǁ_log_to_file__mutmut_3, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_4': xǁUnifiedObserverǁ_log_to_file__mutmut_4, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_5': xǁUnifiedObserverǁ_log_to_file__mutmut_5, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_6': xǁUnifiedObserverǁ_log_to_file__mutmut_6, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_7': xǁUnifiedObserverǁ_log_to_file__mutmut_7, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_8': xǁUnifiedObserverǁ_log_to_file__mutmut_8, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_9': xǁUnifiedObserverǁ_log_to_file__mutmut_9, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_10': xǁUnifiedObserverǁ_log_to_file__mutmut_10, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_11': xǁUnifiedObserverǁ_log_to_file__mutmut_11, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_12': xǁUnifiedObserverǁ_log_to_file__mutmut_12, 
        'xǁUnifiedObserverǁ_log_to_file__mutmut_13': xǁUnifiedObserverǁ_log_to_file__mutmut_13
    }
    
    def _log_to_file(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_log_to_file__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_log_to_file__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log_to_file.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_log_to_file__mutmut_orig)
    xǁUnifiedObserverǁ_log_to_file__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_log_to_file'
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_orig(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_1(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(None)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_2(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_3(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = None
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_4(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "XXnameXX": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_5(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "NAME": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_6(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "XXcontextsXX": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_7(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "CONTEXTS": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_8(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set(None)
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_9(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(None)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_10(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["XXcontextsXX"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_11(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["CONTEXTS"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_12(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = None
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_13(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = None
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_14(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(None)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_15(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(None)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_16(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(None)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_17(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = None
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = event
    
    def xǁUnifiedObserverǁ_store_event_for_trace__mutmut_18(self, event: AgentEvent) -> None:
        """Store an event for trace building."""
        self.events.append(event)
        
        # Track agent info
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "contexts": set([event.context_id])
            }
        else:
            self.agents[event.agent_id]["contexts"].add(event.context_id)
        
        # Track context relationships
        self.context_map[event.context_id] = event.agent_id
        
        if event.parent_context_id:
            self.parent_map[event.context_id] = event.parent_context_id
            self.children_map[event.parent_context_id].append(event.context_id)
        
        # Track events by agent and context
        self.agent_events[event.agent_id].append(event)
        self.context_events[event.context_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent):
            self.function_calls[event.function_call_id] = event
        elif isinstance(event, FunctionResultEvent):
            self.function_results[event.function_call_id] = None
    
    xǁUnifiedObserverǁ_store_event_for_trace__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_1': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_1, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_2': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_2, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_3': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_3, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_4': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_4, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_5': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_5, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_6': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_6, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_7': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_7, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_8': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_8, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_9': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_9, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_10': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_10, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_11': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_11, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_12': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_12, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_13': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_13, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_14': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_14, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_15': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_15, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_16': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_16, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_17': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_17, 
        'xǁUnifiedObserverǁ_store_event_for_trace__mutmut_18': xǁUnifiedObserverǁ_store_event_for_trace__mutmut_18
    }
    
    def _store_event_for_trace(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_store_event_for_trace__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_store_event_for_trace__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _store_event_for_trace.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_store_event_for_trace__mutmut_orig)
    xǁUnifiedObserverǁ_store_event_for_trace__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_store_event_for_trace'
    
    def xǁUnifiedObserverǁprint_trace__mutmut_orig(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_1(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace and not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_2(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_3(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_4(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print(None, file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_5(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=None)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_6(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print(file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_7(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", )
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_8(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("XXNo trace available or trace building is disabledXX", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_9(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("no trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_10(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("NO TRACE AVAILABLE OR TRACE BUILDING IS DISABLED", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_11(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = None
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_12(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) + set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_13(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(None) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_14(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(None)
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_15(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print(None, file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_16(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=None)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_17(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print(file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_18(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", )
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_19(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("XX\n=== Agent Interaction Trace ===\nXX", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_20(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== agent interaction trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_21(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== AGENT INTERACTION TRACE ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_22(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(None, 0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_23(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, None, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_24(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, None)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_25(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(0, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_26(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, output)
    
    def xǁUnifiedObserverǁprint_trace__mutmut_27(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 0, )
    
    def xǁUnifiedObserverǁprint_trace__mutmut_28(self, output: TextIO = sys.stdout) -> None:
        """
        Print the hierarchical trace of agent interactions.
        
        Args:
            output: Output stream to write to (default: sys.stdout)
        """
        if not self.build_trace or not self.events:
            print("No trace available or trace building is disabled", file=output)
            return
        
        # Find root contexts (those without parents)
        root_contexts = set(self.context_map.keys()) - set(self.parent_map.keys())
        
        print("\n=== Agent Interaction Trace ===\n", file=output)
        
        # Print the trace for each root context
        for context_id in root_contexts:
            self._print_context_trace(context_id, 1, output)
    
    xǁUnifiedObserverǁprint_trace__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁprint_trace__mutmut_1': xǁUnifiedObserverǁprint_trace__mutmut_1, 
        'xǁUnifiedObserverǁprint_trace__mutmut_2': xǁUnifiedObserverǁprint_trace__mutmut_2, 
        'xǁUnifiedObserverǁprint_trace__mutmut_3': xǁUnifiedObserverǁprint_trace__mutmut_3, 
        'xǁUnifiedObserverǁprint_trace__mutmut_4': xǁUnifiedObserverǁprint_trace__mutmut_4, 
        'xǁUnifiedObserverǁprint_trace__mutmut_5': xǁUnifiedObserverǁprint_trace__mutmut_5, 
        'xǁUnifiedObserverǁprint_trace__mutmut_6': xǁUnifiedObserverǁprint_trace__mutmut_6, 
        'xǁUnifiedObserverǁprint_trace__mutmut_7': xǁUnifiedObserverǁprint_trace__mutmut_7, 
        'xǁUnifiedObserverǁprint_trace__mutmut_8': xǁUnifiedObserverǁprint_trace__mutmut_8, 
        'xǁUnifiedObserverǁprint_trace__mutmut_9': xǁUnifiedObserverǁprint_trace__mutmut_9, 
        'xǁUnifiedObserverǁprint_trace__mutmut_10': xǁUnifiedObserverǁprint_trace__mutmut_10, 
        'xǁUnifiedObserverǁprint_trace__mutmut_11': xǁUnifiedObserverǁprint_trace__mutmut_11, 
        'xǁUnifiedObserverǁprint_trace__mutmut_12': xǁUnifiedObserverǁprint_trace__mutmut_12, 
        'xǁUnifiedObserverǁprint_trace__mutmut_13': xǁUnifiedObserverǁprint_trace__mutmut_13, 
        'xǁUnifiedObserverǁprint_trace__mutmut_14': xǁUnifiedObserverǁprint_trace__mutmut_14, 
        'xǁUnifiedObserverǁprint_trace__mutmut_15': xǁUnifiedObserverǁprint_trace__mutmut_15, 
        'xǁUnifiedObserverǁprint_trace__mutmut_16': xǁUnifiedObserverǁprint_trace__mutmut_16, 
        'xǁUnifiedObserverǁprint_trace__mutmut_17': xǁUnifiedObserverǁprint_trace__mutmut_17, 
        'xǁUnifiedObserverǁprint_trace__mutmut_18': xǁUnifiedObserverǁprint_trace__mutmut_18, 
        'xǁUnifiedObserverǁprint_trace__mutmut_19': xǁUnifiedObserverǁprint_trace__mutmut_19, 
        'xǁUnifiedObserverǁprint_trace__mutmut_20': xǁUnifiedObserverǁprint_trace__mutmut_20, 
        'xǁUnifiedObserverǁprint_trace__mutmut_21': xǁUnifiedObserverǁprint_trace__mutmut_21, 
        'xǁUnifiedObserverǁprint_trace__mutmut_22': xǁUnifiedObserverǁprint_trace__mutmut_22, 
        'xǁUnifiedObserverǁprint_trace__mutmut_23': xǁUnifiedObserverǁprint_trace__mutmut_23, 
        'xǁUnifiedObserverǁprint_trace__mutmut_24': xǁUnifiedObserverǁprint_trace__mutmut_24, 
        'xǁUnifiedObserverǁprint_trace__mutmut_25': xǁUnifiedObserverǁprint_trace__mutmut_25, 
        'xǁUnifiedObserverǁprint_trace__mutmut_26': xǁUnifiedObserverǁprint_trace__mutmut_26, 
        'xǁUnifiedObserverǁprint_trace__mutmut_27': xǁUnifiedObserverǁprint_trace__mutmut_27, 
        'xǁUnifiedObserverǁprint_trace__mutmut_28': xǁUnifiedObserverǁprint_trace__mutmut_28
    }
    
    def print_trace(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁprint_trace__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁprint_trace__mutmut_mutants"), args, kwargs, self)
        return result 
    
    print_trace.__signature__ = _mutmut_signature(xǁUnifiedObserverǁprint_trace__mutmut_orig)
    xǁUnifiedObserverǁprint_trace__mutmut_orig.__name__ = 'xǁUnifiedObserverǁprint_trace'
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_orig(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_1(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = None
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_2(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(None)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_3(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_4(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = None
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_5(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["XXnameXX"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_6(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["NAME"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_7(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = None
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_8(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " / indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_9(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "XX  XX" * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_10(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(None, file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_11(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=None)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_12(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_13(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", )
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_14(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = None
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_15(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(None)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_16(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(None, file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_17(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=None)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_18(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_19(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", )
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_20(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(None, []):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_21(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, None):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_22(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get([]):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_23(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, ):
            self._print_context_trace(child_context_id, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_24(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(None, indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_25(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, None, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_26(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, None)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_27(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(indent + 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_28(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_29(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 1, )
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_30(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent - 1, output)
    
    def xǁUnifiedObserverǁ_print_context_trace__mutmut_31(self, context_id: str, indent: int, output: TextIO) -> None:
        """
        Print the trace for a specific context.
        
        Args:
            context_id: Context ID to print trace for
            indent: Current indentation level
            output: Output stream to write to
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
        
        agent_name = self.agents[agent_id]["name"]
        indent_str = "  " * indent
        
        print(f"{indent_str}Context: {context_id} (Agent: {agent_name})", file=output)
        
        # Print events for this context
        for event in self.context_events[context_id]:
            event_summary = self._get_event_summary(event)
            print(f"{indent_str}  {event.event_type}: {event_summary}", file=output)
        
        # Print child contexts
        for child_context_id in self.children_map.get(context_id, []):
            self._print_context_trace(child_context_id, indent + 2, output)
    
    xǁUnifiedObserverǁ_print_context_trace__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_print_context_trace__mutmut_1': xǁUnifiedObserverǁ_print_context_trace__mutmut_1, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_2': xǁUnifiedObserverǁ_print_context_trace__mutmut_2, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_3': xǁUnifiedObserverǁ_print_context_trace__mutmut_3, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_4': xǁUnifiedObserverǁ_print_context_trace__mutmut_4, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_5': xǁUnifiedObserverǁ_print_context_trace__mutmut_5, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_6': xǁUnifiedObserverǁ_print_context_trace__mutmut_6, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_7': xǁUnifiedObserverǁ_print_context_trace__mutmut_7, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_8': xǁUnifiedObserverǁ_print_context_trace__mutmut_8, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_9': xǁUnifiedObserverǁ_print_context_trace__mutmut_9, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_10': xǁUnifiedObserverǁ_print_context_trace__mutmut_10, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_11': xǁUnifiedObserverǁ_print_context_trace__mutmut_11, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_12': xǁUnifiedObserverǁ_print_context_trace__mutmut_12, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_13': xǁUnifiedObserverǁ_print_context_trace__mutmut_13, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_14': xǁUnifiedObserverǁ_print_context_trace__mutmut_14, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_15': xǁUnifiedObserverǁ_print_context_trace__mutmut_15, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_16': xǁUnifiedObserverǁ_print_context_trace__mutmut_16, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_17': xǁUnifiedObserverǁ_print_context_trace__mutmut_17, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_18': xǁUnifiedObserverǁ_print_context_trace__mutmut_18, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_19': xǁUnifiedObserverǁ_print_context_trace__mutmut_19, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_20': xǁUnifiedObserverǁ_print_context_trace__mutmut_20, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_21': xǁUnifiedObserverǁ_print_context_trace__mutmut_21, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_22': xǁUnifiedObserverǁ_print_context_trace__mutmut_22, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_23': xǁUnifiedObserverǁ_print_context_trace__mutmut_23, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_24': xǁUnifiedObserverǁ_print_context_trace__mutmut_24, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_25': xǁUnifiedObserverǁ_print_context_trace__mutmut_25, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_26': xǁUnifiedObserverǁ_print_context_trace__mutmut_26, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_27': xǁUnifiedObserverǁ_print_context_trace__mutmut_27, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_28': xǁUnifiedObserverǁ_print_context_trace__mutmut_28, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_29': xǁUnifiedObserverǁ_print_context_trace__mutmut_29, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_30': xǁUnifiedObserverǁ_print_context_trace__mutmut_30, 
        'xǁUnifiedObserverǁ_print_context_trace__mutmut_31': xǁUnifiedObserverǁ_print_context_trace__mutmut_31
    }
    
    def _print_context_trace(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_print_context_trace__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_print_context_trace__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _print_context_trace.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_print_context_trace__mutmut_orig)
    xǁUnifiedObserverǁ_print_context_trace__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_print_context_trace'
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_orig(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, 0, output)
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_1(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(None, 0, output)
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_2(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, None, output)
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_3(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, 0, None)
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_4(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(0, output)
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_5(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, output)
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_6(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, 0, )
    
    # Add alias for backward compatibility
    def xǁUnifiedObserverǁ_print_agent_tree__mutmut_7(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, 1, output)
    
    xǁUnifiedObserverǁ_print_agent_tree__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_print_agent_tree__mutmut_1': xǁUnifiedObserverǁ_print_agent_tree__mutmut_1, 
        'xǁUnifiedObserverǁ_print_agent_tree__mutmut_2': xǁUnifiedObserverǁ_print_agent_tree__mutmut_2, 
        'xǁUnifiedObserverǁ_print_agent_tree__mutmut_3': xǁUnifiedObserverǁ_print_agent_tree__mutmut_3, 
        'xǁUnifiedObserverǁ_print_agent_tree__mutmut_4': xǁUnifiedObserverǁ_print_agent_tree__mutmut_4, 
        'xǁUnifiedObserverǁ_print_agent_tree__mutmut_5': xǁUnifiedObserverǁ_print_agent_tree__mutmut_5, 
        'xǁUnifiedObserverǁ_print_agent_tree__mutmut_6': xǁUnifiedObserverǁ_print_agent_tree__mutmut_6, 
        'xǁUnifiedObserverǁ_print_agent_tree__mutmut_7': xǁUnifiedObserverǁ_print_agent_tree__mutmut_7
    }
    
    def _print_agent_tree(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_print_agent_tree__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_print_agent_tree__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _print_agent_tree.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_print_agent_tree__mutmut_orig)
    xǁUnifiedObserverǁ_print_agent_tree__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_print_agent_tree'
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_orig(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents or agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(event)
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_1(self, agent_id: str, prefix: str = "XXXX") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents or agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(event)
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_2(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents and agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(event)
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_3(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id in self.agents or agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(event)
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_4(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents or agent_id in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(event)
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_5(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents or agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = None
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_6(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents or agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(None)
            print(f"  {event.event_type}: {event_summary}")
    
    def xǁUnifiedObserverǁ_print_agent_events__mutmut_7(self, agent_id: str, prefix: str = "") -> None:
        """
        Alias method for backward compatibility that prints events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation (ignored, for compatibility)
        """
        if agent_id not in self.agents or agent_id not in self.agent_events:
            return
            
        # Print events for this agent
        for event in self.agent_events[agent_id]:
            event_summary = self._get_event_summary(event)
            print(None)
    
    xǁUnifiedObserverǁ_print_agent_events__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_print_agent_events__mutmut_1': xǁUnifiedObserverǁ_print_agent_events__mutmut_1, 
        'xǁUnifiedObserverǁ_print_agent_events__mutmut_2': xǁUnifiedObserverǁ_print_agent_events__mutmut_2, 
        'xǁUnifiedObserverǁ_print_agent_events__mutmut_3': xǁUnifiedObserverǁ_print_agent_events__mutmut_3, 
        'xǁUnifiedObserverǁ_print_agent_events__mutmut_4': xǁUnifiedObserverǁ_print_agent_events__mutmut_4, 
        'xǁUnifiedObserverǁ_print_agent_events__mutmut_5': xǁUnifiedObserverǁ_print_agent_events__mutmut_5, 
        'xǁUnifiedObserverǁ_print_agent_events__mutmut_6': xǁUnifiedObserverǁ_print_agent_events__mutmut_6, 
        'xǁUnifiedObserverǁ_print_agent_events__mutmut_7': xǁUnifiedObserverǁ_print_agent_events__mutmut_7
    }
    
    def _print_agent_events(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_print_agent_events__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_print_agent_events__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _print_agent_events.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_print_agent_events__mutmut_orig)
    xǁUnifiedObserverǁ_print_agent_events__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_print_agent_events'
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_orig(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_1(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:51]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_2(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) >= 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_3(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 51 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_4(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = None
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_5(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(None)
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_6(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = "XX, XX".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_7(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(None)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_8(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = None
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_9(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(None)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_10(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:51]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_11(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) >= 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_12(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 51 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(event)
    
    def xǁUnifiedObserverǁ_get_event_summary__mutmut_13(self, event: AgentEvent) -> str:
        """Get a summary string for an event."""
        if isinstance(event, UserMessageEvent):
            return f"User: {event.message}"
        elif isinstance(event, AgentResponseEvent):
            return f"Agent: {event.response[:50]}..." if len(event.response) > 50 else event.response
        elif isinstance(event, FunctionCallEvent):
            args_str = ", ".join(f"{k}={repr(v)}" for k, v in event.function_args.items())
            return f"{event.function_name}({args_str})"
        elif isinstance(event, FunctionResultEvent):
            result_str = str(event.result)
            return f"{event.function_name} -> {result_str[:50]}..." if len(result_str) > 50 else result_str
        elif isinstance(event, AgentInitializedEvent):
            return f"Model: {event.model_name}, Tools: {len(event.tools)}"
        else:
            return str(None)
    
    xǁUnifiedObserverǁ_get_event_summary__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_get_event_summary__mutmut_1': xǁUnifiedObserverǁ_get_event_summary__mutmut_1, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_2': xǁUnifiedObserverǁ_get_event_summary__mutmut_2, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_3': xǁUnifiedObserverǁ_get_event_summary__mutmut_3, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_4': xǁUnifiedObserverǁ_get_event_summary__mutmut_4, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_5': xǁUnifiedObserverǁ_get_event_summary__mutmut_5, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_6': xǁUnifiedObserverǁ_get_event_summary__mutmut_6, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_7': xǁUnifiedObserverǁ_get_event_summary__mutmut_7, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_8': xǁUnifiedObserverǁ_get_event_summary__mutmut_8, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_9': xǁUnifiedObserverǁ_get_event_summary__mutmut_9, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_10': xǁUnifiedObserverǁ_get_event_summary__mutmut_10, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_11': xǁUnifiedObserverǁ_get_event_summary__mutmut_11, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_12': xǁUnifiedObserverǁ_get_event_summary__mutmut_12, 
        'xǁUnifiedObserverǁ_get_event_summary__mutmut_13': xǁUnifiedObserverǁ_get_event_summary__mutmut_13
    }
    
    def _get_event_summary(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_get_event_summary__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_get_event_summary__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_event_summary.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_get_event_summary__mutmut_orig)
    xǁUnifiedObserverǁ_get_event_summary__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_get_event_summary'

    def xǁUnifiedObserverǁ_format_args__mutmut_orig(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={repr(value)}")
        
        return ", ".join(parts)

    def xǁUnifiedObserverǁ_format_args__mutmut_1(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={repr(value)}")
        
        return ", ".join(parts)

    def xǁUnifiedObserverǁ_format_args__mutmut_2(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return "XXXX"
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={repr(value)}")
        
        return ", ".join(parts)

    def xǁUnifiedObserverǁ_format_args__mutmut_3(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return ""
        
        parts = None
        for key, value in args.items():
            parts.append(f"{key}={repr(value)}")
        
        return ", ".join(parts)

    def xǁUnifiedObserverǁ_format_args__mutmut_4(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(None)
        
        return ", ".join(parts)

    def xǁUnifiedObserverǁ_format_args__mutmut_5(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={repr(None)}")
        
        return ", ".join(parts)

    def xǁUnifiedObserverǁ_format_args__mutmut_6(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={repr(value)}")
        
        return ", ".join(None)

    def xǁUnifiedObserverǁ_format_args__mutmut_7(self, args: Dict) -> str:
        """
        Format function arguments as a string.
        
        Args:
            args: Dictionary of function arguments
            
        Returns:
            Formatted string representation of arguments
        """
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={repr(value)}")
        
        return "XX, XX".join(parts)
    
    xǁUnifiedObserverǁ_format_args__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnifiedObserverǁ_format_args__mutmut_1': xǁUnifiedObserverǁ_format_args__mutmut_1, 
        'xǁUnifiedObserverǁ_format_args__mutmut_2': xǁUnifiedObserverǁ_format_args__mutmut_2, 
        'xǁUnifiedObserverǁ_format_args__mutmut_3': xǁUnifiedObserverǁ_format_args__mutmut_3, 
        'xǁUnifiedObserverǁ_format_args__mutmut_4': xǁUnifiedObserverǁ_format_args__mutmut_4, 
        'xǁUnifiedObserverǁ_format_args__mutmut_5': xǁUnifiedObserverǁ_format_args__mutmut_5, 
        'xǁUnifiedObserverǁ_format_args__mutmut_6': xǁUnifiedObserverǁ_format_args__mutmut_6, 
        'xǁUnifiedObserverǁ_format_args__mutmut_7': xǁUnifiedObserverǁ_format_args__mutmut_7
    }
    
    def _format_args(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnifiedObserverǁ_format_args__mutmut_orig"), object.__getattribute__(self, "xǁUnifiedObserverǁ_format_args__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _format_args.__signature__ = _mutmut_signature(xǁUnifiedObserverǁ_format_args__mutmut_orig)
    xǁUnifiedObserverǁ_format_args__mutmut_orig.__name__ = 'xǁUnifiedObserverǁ_format_args'


# Simple observer implementations for backward compatibility
class ConsoleObserver(UnifiedObserver):
    """
    Observer that logs events to the console.
    
    This is a simple implementation for debugging purposes.
    """
    
    def xǁConsoleObserverǁ__init____mutmut_orig(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_1(self, verbose: bool = True):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_2(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=None,
            file_output=False,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_3(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=None,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_4(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            build_trace=None,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_5(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            build_trace=False,
            verbose=None
        )
    
    def xǁConsoleObserverǁ__init____mutmut_6(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            file_output=False,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_7(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_8(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_9(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            build_trace=False,
            )
    
    def xǁConsoleObserverǁ__init____mutmut_10(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=False,
            file_output=False,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_11(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=True,
            build_trace=False,
            verbose=verbose
        )
    
    def xǁConsoleObserverǁ__init____mutmut_12(self, verbose: bool = False):
        """
        Initialize a console observer.
        
        Args:
            verbose: Whether to include verbose details in console output
        """
        super().__init__(
            console_output=True,
            file_output=False,
            build_trace=True,
            verbose=verbose
        )
    
    xǁConsoleObserverǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleObserverǁ__init____mutmut_1': xǁConsoleObserverǁ__init____mutmut_1, 
        'xǁConsoleObserverǁ__init____mutmut_2': xǁConsoleObserverǁ__init____mutmut_2, 
        'xǁConsoleObserverǁ__init____mutmut_3': xǁConsoleObserverǁ__init____mutmut_3, 
        'xǁConsoleObserverǁ__init____mutmut_4': xǁConsoleObserverǁ__init____mutmut_4, 
        'xǁConsoleObserverǁ__init____mutmut_5': xǁConsoleObserverǁ__init____mutmut_5, 
        'xǁConsoleObserverǁ__init____mutmut_6': xǁConsoleObserverǁ__init____mutmut_6, 
        'xǁConsoleObserverǁ__init____mutmut_7': xǁConsoleObserverǁ__init____mutmut_7, 
        'xǁConsoleObserverǁ__init____mutmut_8': xǁConsoleObserverǁ__init____mutmut_8, 
        'xǁConsoleObserverǁ__init____mutmut_9': xǁConsoleObserverǁ__init____mutmut_9, 
        'xǁConsoleObserverǁ__init____mutmut_10': xǁConsoleObserverǁ__init____mutmut_10, 
        'xǁConsoleObserverǁ__init____mutmut_11': xǁConsoleObserverǁ__init____mutmut_11, 
        'xǁConsoleObserverǁ__init____mutmut_12': xǁConsoleObserverǁ__init____mutmut_12
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleObserverǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁConsoleObserverǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁConsoleObserverǁ__init____mutmut_orig)
    xǁConsoleObserverǁ__init____mutmut_orig.__name__ = 'xǁConsoleObserverǁ__init__'


class FileObserver(UnifiedObserver):
    """
    Observer that logs events to a file in JSON format.
    
    This allows for later analysis and visualization.
    """
    
    def xǁFileObserverǁ__init____mutmut_orig(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_1(self, filename: str = 'XXagent_events.jsonlXX'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_2(self, filename: str = 'AGENT_EVENTS.JSONL'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_3(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=None,
            file_output=True,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_4(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=None,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_5(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=None,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_6(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=filename,
            build_trace=None
        )
    
    def xǁFileObserverǁ__init____mutmut_7(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            file_output=True,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_8(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_9(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_10(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=filename,
            )
    
    def xǁFileObserverǁ__init____mutmut_11(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=True,
            file_output=True,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_12(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=False,
            file_path=filename,
            build_trace=False
        )
    
    def xǁFileObserverǁ__init____mutmut_13(self, filename: str = 'agent_events.jsonl'):
        """
        Initialize a file observer.
        
        Args:
            filename: Name of the file to log events to
        """
        super().__init__(
            console_output=False,
            file_output=True,
            file_path=filename,
            build_trace=True
        )
    
    xǁFileObserverǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFileObserverǁ__init____mutmut_1': xǁFileObserverǁ__init____mutmut_1, 
        'xǁFileObserverǁ__init____mutmut_2': xǁFileObserverǁ__init____mutmut_2, 
        'xǁFileObserverǁ__init____mutmut_3': xǁFileObserverǁ__init____mutmut_3, 
        'xǁFileObserverǁ__init____mutmut_4': xǁFileObserverǁ__init____mutmut_4, 
        'xǁFileObserverǁ__init____mutmut_5': xǁFileObserverǁ__init____mutmut_5, 
        'xǁFileObserverǁ__init____mutmut_6': xǁFileObserverǁ__init____mutmut_6, 
        'xǁFileObserverǁ__init____mutmut_7': xǁFileObserverǁ__init____mutmut_7, 
        'xǁFileObserverǁ__init____mutmut_8': xǁFileObserverǁ__init____mutmut_8, 
        'xǁFileObserverǁ__init____mutmut_9': xǁFileObserverǁ__init____mutmut_9, 
        'xǁFileObserverǁ__init____mutmut_10': xǁFileObserverǁ__init____mutmut_10, 
        'xǁFileObserverǁ__init____mutmut_11': xǁFileObserverǁ__init____mutmut_11, 
        'xǁFileObserverǁ__init____mutmut_12': xǁFileObserverǁ__init____mutmut_12, 
        'xǁFileObserverǁ__init____mutmut_13': xǁFileObserverǁ__init____mutmut_13
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFileObserverǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFileObserverǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFileObserverǁ__init____mutmut_orig)
    xǁFileObserverǁ__init____mutmut_orig.__name__ = 'xǁFileObserverǁ__init__'


class TreeTraceObserver(UnifiedObserver):
    """
    Observer that builds and displays a hierarchical tree visualization of agent interactions.
    
    This provides a clear view of parent-child relationships and event sequences.
    """
    
    def xǁTreeTraceObserverǁ__init____mutmut_orig(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=False,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_1(self, console_output: bool = True):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=False,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_2(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=None,
            file_output=False,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_3(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=None,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_4(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=False,
            build_trace=None
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_5(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            file_output=False,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_6(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_7(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=False,
            )
    
    def xǁTreeTraceObserverǁ__init____mutmut_8(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=True,
            build_trace=True
        )
    
    def xǁTreeTraceObserverǁ__init____mutmut_9(self, console_output: bool = False):
        """
        Initialize a tree trace observer.
        
        Args:
            console_output: Whether to also log events to the console
        """
        super().__init__(
            console_output=console_output,
            file_output=False,
            build_trace=False
        )
    
    xǁTreeTraceObserverǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTreeTraceObserverǁ__init____mutmut_1': xǁTreeTraceObserverǁ__init____mutmut_1, 
        'xǁTreeTraceObserverǁ__init____mutmut_2': xǁTreeTraceObserverǁ__init____mutmut_2, 
        'xǁTreeTraceObserverǁ__init____mutmut_3': xǁTreeTraceObserverǁ__init____mutmut_3, 
        'xǁTreeTraceObserverǁ__init____mutmut_4': xǁTreeTraceObserverǁ__init____mutmut_4, 
        'xǁTreeTraceObserverǁ__init____mutmut_5': xǁTreeTraceObserverǁ__init____mutmut_5, 
        'xǁTreeTraceObserverǁ__init____mutmut_6': xǁTreeTraceObserverǁ__init____mutmut_6, 
        'xǁTreeTraceObserverǁ__init____mutmut_7': xǁTreeTraceObserverǁ__init____mutmut_7, 
        'xǁTreeTraceObserverǁ__init____mutmut_8': xǁTreeTraceObserverǁ__init____mutmut_8, 
        'xǁTreeTraceObserverǁ__init____mutmut_9': xǁTreeTraceObserverǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTreeTraceObserverǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTreeTraceObserverǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTreeTraceObserverǁ__init____mutmut_orig)
    xǁTreeTraceObserverǁ__init____mutmut_orig.__name__ = 'xǁTreeTraceObserverǁ__init__'


def x_generate_context_id__mutmut_orig() -> str:
    """
    Generate a unique context ID.
    
    Returns:
        A unique context ID
    """
    return str(uuid.uuid4()) 


def x_generate_context_id__mutmut_1() -> str:
    """
    Generate a unique context ID.
    
    Returns:
        A unique context ID
    """
    return str(None) 

x_generate_context_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_generate_context_id__mutmut_1': x_generate_context_id__mutmut_1
}

def generate_context_id(*args, **kwargs):
    result = _mutmut_trampoline(x_generate_context_id__mutmut_orig, x_generate_context_id__mutmut_mutants, args, kwargs)
    return result 

generate_context_id.__signature__ = _mutmut_signature(x_generate_context_id__mutmut_orig)
x_generate_context_id__mutmut_orig.__name__ = 'x_generate_context_id'