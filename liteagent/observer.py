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

# ---- Event Classes ----

class AgentEvent:
    """Base class for all agent events."""
    
    def __init__(self, 
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
    
    def to_dict(self) -> Dict[str, Any]:
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
    
    def __str__(self) -> str:
        """Convert event to string representation."""
        return f"{self.event_type}(agent={self.agent_name}, context={self.context_id})"


# Specialized event types
class AgentInitializedEvent(AgentEvent):
    """Event fired when an agent is initialized."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str, 
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
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        # For backward compatibility, make sure these keys are included
        result["model_name"] = self.model_name
        result["system_prompt"] = self.system_prompt
        return result


class UserMessageEvent(AgentEvent):
    """Event fired when a user sends a message to an agent."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str,
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


class ModelRequestEvent(AgentEvent):
    """Event fired when a request is sent to a model."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str,
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


class ModelResponseEvent(AgentEvent):
    """Event fired when a response is received from a model."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str,
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
        
    # Override to_dict for backward compatibility
    def to_dict(self) -> Dict[str, Any]:
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


class FunctionCallEvent(AgentEvent):
    """Event fired when a function is called."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str,
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


class FunctionResultEvent(AgentEvent):
    """Event fired when a function call returns a result."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str,
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
        
    # Override to_dict for backward compatibility
    def to_dict(self) -> Dict[str, Any]:
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


class AgentResponseEvent(AgentEvent):
    """Event fired when an agent generates a response."""
    
    def __init__(self, agent_id: str, agent_name: str, context_id: str,
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
    
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        """Handle an agent initialized event."""
        self.on_event(event)
    
    def on_user_message(self, event: UserMessageEvent) -> None:
        """Handle a user message event."""
        self.on_event(event)
    
    def on_model_request(self, event: ModelRequestEvent) -> None:
        """Handle a model request event."""
        self.on_event(event)
    
    def on_model_response(self, event: ModelResponseEvent) -> None:
        """Handle a model response event."""
        self.on_event(event)
    
    def on_function_call(self, event: FunctionCallEvent) -> None:
        """Handle a function call event."""
        self.on_event(event)
    
    def on_function_result(self, event: FunctionResultEvent) -> None:
        """Handle a function result event."""
        self.on_event(event)
    
    def on_agent_response(self, event: AgentResponseEvent) -> None:
        """Handle an agent response event."""
        self.on_event(event)


# ---- Unified Observer Implementation ----

class UnifiedObserver(AgentObserver):
    """
    Configurable observer that combines console, file, and tree trace functionality.
    
    This observer can be configured to log events to the console, a file, or both,
    and can also build a hierarchical trace of agent interactions.
    """
    
    def __init__(self, 
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
    
    def on_event(self, event: AgentEvent) -> None:
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
    
    def _log_to_console(self, event: AgentEvent) -> None:
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
    
    def _log_to_file(self, event: AgentEvent) -> None:
        """Log an event to a file in JSON format."""
        try:
            event_dict = event.to_dict()
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")
    
    def _store_event_for_trace(self, event: AgentEvent) -> None:
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
    
    def print_trace(self, output: TextIO = sys.stdout) -> None:
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
    
    def _print_context_trace(self, context_id: str, indent: int, output: TextIO) -> None:
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
    
    # Add alias for backward compatibility
    def _print_agent_tree(self, context_id: str, prefix: str, is_last: bool, output: TextIO = sys.stdout) -> None:
        """
        Alias for _print_context_trace for backward compatibility.
        
        Args:
            context_id: Context ID to print trace for
            prefix: Ignored, kept for backward compatibility
            is_last: Ignored, kept for backward compatibility
            output: Output stream to write to
        """
        self._print_context_trace(context_id, 0, output)
    
    def _print_agent_events(self, agent_id: str, prefix: str = "") -> None:
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
    
    def _get_event_summary(self, event: AgentEvent) -> str:
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

    def _format_args(self, args: Dict) -> str:
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


# Simple observer implementations for backward compatibility
class ConsoleObserver(UnifiedObserver):
    """
    Observer that logs events to the console.
    
    This is a simple implementation for debugging purposes.
    """
    
    def __init__(self, verbose: bool = False):
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


class FileObserver(UnifiedObserver):
    """
    Observer that logs events to a file in JSON format.
    
    This allows for later analysis and visualization.
    """
    
    def __init__(self, filename: str = 'agent_events.jsonl'):
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


class TreeTraceObserver(UnifiedObserver):
    """
    Observer that builds and displays a hierarchical tree visualization of agent interactions.
    
    This provides a clear view of parent-child relationships and event sequences.
    """
    
    def __init__(self, console_output: bool = False):
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


def generate_context_id() -> str:
    """
    Generate a unique context ID.
    
    Returns:
        A unique context ID
    """
    return str(uuid.uuid4()) 