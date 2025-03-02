"""
Observer pattern implementation for LiteAgent observability.

This module provides the observer interface and implementations for tracking
agent operations, function calls, and inter-agent communication.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import uuid
import time
import json
from collections import defaultdict


class AgentEvent:
    """Base class for all agent events."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 timestamp: Optional[float] = None):
        """
        Initialize a new agent event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            timestamp: Event timestamp (defaults to current time)
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.context_id = context_id
        self.parent_context_id = parent_context_id
        self.timestamp = timestamp or time.time()
        self.event_type = self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        return {
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "context_id": self.context_id,
            "parent_context_id": self.parent_context_id,
            "timestamp": self.timestamp
        }


class AgentInitializedEvent(AgentEvent):
    """Event emitted when an agent is initialized."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 model_name: str = None,
                 system_prompt: str = None,
                 **kwargs):
        """
        Initialize an agent initialized event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            model_name: Name of the model used by the agent
            system_prompt: System prompt used by the agent
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.model_name = model_name
        self.system_prompt = system_prompt
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        result.update({
            "model_name": self.model_name,
            "system_prompt": self.system_prompt
        })
        return result


class UserMessageEvent(AgentEvent):
    """Event emitted when a user message is received."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 message: str = None,
                 **kwargs):
        """
        Initialize a user message event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            message: User message content
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.message = message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        result.update({
            "message": self.message
        })
        return result


class ModelRequestEvent(AgentEvent):
    """Event emitted before a request is sent to the model."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 messages: List[Dict] = None,
                 functions: List[Dict] = None,
                 **kwargs):
        """
        Initialize a model request event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            messages: Messages being sent to the model
            functions: Function definitions being sent to the model
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.messages = messages
        self.functions = functions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        result.update({
            "messages": self.messages,
            "functions": self.functions
        })
        return result


class ModelResponseEvent(AgentEvent):
    """Event emitted after a response is received from the model."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 response: Any = None,
                 **kwargs):
        """
        Initialize a model response event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            response: Model response
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.response = response
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        
        # Handle non-serializable response objects
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
            result["response"] = None
            
        return result


class FunctionCallEvent(AgentEvent):
    """Event emitted before a function/tool is called."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 function_name: str = None,
                 function_args: Dict = None,
                 function_call_id: str = None,
                 **kwargs):
        """
        Initialize a function call event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            function_name: Name of the function being called
            function_args: Arguments being passed to the function
            function_call_id: Unique ID to link this call with its result
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.function_name = function_name
        self.function_args = function_args
        self.function_call_id = function_call_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        result.update({
            "function_name": self.function_name,
            "function_args": self.function_args,
            "function_call_id": self.function_call_id
        })
        return result


class FunctionResultEvent(AgentEvent):
    """Event emitted after a function/tool returns a result."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 function_name: str = None,
                 function_args: Dict = None,
                 result: Any = None,
                 error: str = None,
                 function_call_id: str = None,
                 **kwargs):
        """
        Initialize a function result event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            function_name: Name of the function that was called
            function_args: Arguments that were passed to the function
            result: Result returned by the function
            error: Error message if the function call failed
            function_call_id: Unique ID linking this result to its function call
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.function_name = function_name
        self.function_args = function_args
        self.result = result
        self.error = error
        self.function_call_id = function_call_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result_dict = super().to_dict()
        
        # Ensure result is serializable
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
            
        result_dict.update({
            "function_name": self.function_name,
            "function_args": self.function_args,
            "result": serialized_result,
            "error": self.error,
            "function_call_id": self.function_call_id
        })
        return result_dict


class AgentResponseEvent(AgentEvent):
    """Event emitted when an agent generates a final response."""
    
    def __init__(self, 
                 agent_id: str, 
                 agent_name: str, 
                 context_id: str, 
                 parent_context_id: Optional[str] = None,
                 response: str = None,
                 **kwargs):
        """
        Initialize an agent response event.
        
        Args:
            agent_id: Unique identifier of the agent
            agent_name: Name of the agent
            context_id: Context ID of the current execution
            parent_context_id: Optional parent context ID if this agent was created by another agent
            response: Agent's response content
        """
        super().__init__(agent_id, agent_name, context_id, parent_context_id)
        self.response = response
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        result = super().to_dict()
        result.update({
            "response": self.response
        })
        return result


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
        """
        Handle an agent initialized event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)
    
    def on_user_message(self, event: UserMessageEvent) -> None:
        """
        Handle a user message event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)
    
    def on_model_request(self, event: ModelRequestEvent) -> None:
        """
        Handle a model request event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)
    
    def on_model_response(self, event: ModelResponseEvent) -> None:
        """
        Handle a model response event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)
    
    def on_function_call(self, event: FunctionCallEvent) -> None:
        """
        Handle a function call event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)
    
    def on_function_result(self, event: FunctionResultEvent) -> None:
        """
        Handle a function result event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)
    
    def on_agent_response(self, event: AgentResponseEvent) -> None:
        """
        Handle an agent response event.
        
        Args:
            event: The event to handle
        """
        self.on_event(event)


class ConsoleObserver(AgentObserver):
    """
    Observer that logs events to the console.
    
    This is a simple implementation for debugging purposes.
    """
    
    def on_event(self, event: AgentEvent) -> None:
        """Log event to console."""
        event_dict = event.to_dict()
        print(f"[{event.event_type}] Agent: {event.agent_name} ({event.agent_id})")
        print(f"  Context: {event.context_id}")
        if event.parent_context_id:
            print(f"  Parent Context: {event.parent_context_id}")
        
        # Print event-specific details
        if isinstance(event, AgentInitializedEvent):
            print(f"  Model: {event.model_name}")
        elif isinstance(event, UserMessageEvent):
            print(f"  User Message: {event.message}")
        elif isinstance(event, FunctionCallEvent):
            print(f"  Function Call: {event.function_name}")
            print(f"  Arguments: {event.function_args}")
        elif isinstance(event, FunctionResultEvent):
            print(f"  Function Result: {event.function_name}")
            print(f"  Result: {event.result}")
            if event.error:
                print(f"  Error: {event.error}")
        elif isinstance(event, AgentResponseEvent):
            print(f"  Response: {event.response}")
        
        print("\n")


class FileObserver(AgentObserver):
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
        self.filename = filename
    
    def on_event(self, event: AgentEvent) -> None:
        """Log event to file."""
        try:
            event_dict = event.to_dict()
            with open(self.filename, 'a') as f:
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            print(f"Error logging event to file: {str(e)}")


class TreeTraceObserver(AgentObserver):
    """
    Observer that builds and displays a hierarchical tree visualization of agent interactions.
    
    This provides a clear view of parent-child relationships and event sequences.
    """
    
    def __init__(self):
        """Initialize the tree trace observer."""
        self.events = []
        self.agents = {}  # agent_id -> agent info
        self.context_map = {}  # context_id -> agent_id
        self.parent_map = {}  # context_id -> parent_context_id
        self.children_map = defaultdict(list)  # parent_context_id -> [child_context_ids]
        self.agent_events = defaultdict(list)  # agent_id -> [events]
        self.function_calls = {}  # function_call_id -> call event
        self.function_results = {}  # function_call_id -> result event
        
    def on_event(self, event: AgentEvent) -> None:
        """Record all events."""
        self.events.append(event)
        
        # Track agents
        if event.agent_id not in self.agents:
            self.agents[event.agent_id] = {
                "name": event.agent_name,
                "context_id": event.context_id,
                "parent_context_id": event.parent_context_id
            }
            
            # Update parent-child relationships
            if event.parent_context_id:
                self.parent_map[event.context_id] = event.parent_context_id
                self.children_map[event.parent_context_id].append(event.context_id)
            
        # Map contexts to agents
        if event.context_id not in self.context_map:
            self.context_map[event.context_id] = event.agent_id
            
        # Store events by agent
        self.agent_events[event.agent_id].append(event)
        
        # Track function calls and results
        if isinstance(event, FunctionCallEvent) and hasattr(event, 'function_call_id') and event.function_call_id:
            self.function_calls[event.function_call_id] = event
            
        if isinstance(event, FunctionResultEvent) and hasattr(event, 'function_call_id') and event.function_call_id:
            self.function_results[event.function_call_id] = event
    
    def print_trace(self) -> None:
        """Print a hierarchical tree visualization of agent interactions."""
        print("\n=== Agent Interaction Tree ===")
        
        # Find root contexts (those without parents)
        root_contexts = []
        for context_id in self.context_map.keys():
            if context_id not in self.parent_map:
                root_contexts.append(context_id)
        
        # Print each tree starting from root contexts
        for root_context in root_contexts:
            self._print_agent_tree(root_context, "", True)
    
    def _print_agent_tree(self, context_id: str, prefix: str, is_last: bool) -> None:
        """
        Recursively print the agent tree.
        
        Args:
            context_id: The context ID to print
            prefix: Prefix string for indentation
            is_last: Whether this is the last child in its parent
        """
        agent_id = self.context_map.get(context_id)
        if not agent_id:
            return
            
        agent = self.agents.get(agent_id, {})
        agent_name = agent.get("name", "Unknown")
        
        # Print the agent node
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}Agent: {agent_name} (context: {context_id[:8]}...)")
        
        # Print events for this agent
        events_prefix = prefix + ("    " if is_last else "│   ")
        self._print_agent_events(agent_id, events_prefix)
        
        # Print child agents
        children = self.children_map.get(context_id, [])
        for i, child_context in enumerate(children):
            child_prefix = prefix + ("    " if is_last else "│   ")
            is_last_child = (i == len(children) - 1)
            self._print_agent_tree(child_context, child_prefix, is_last_child)
    
    def _print_agent_events(self, agent_id: str, prefix: str) -> None:
        """
        Print events for an agent.
        
        Args:
            agent_id: The agent ID to print events for
            prefix: Prefix string for indentation
        """
        events = sorted(self.agent_events.get(agent_id, []), key=lambda e: e.timestamp)
        
        for event in events:
            event_type = event.event_type
            
            # Format the event line based on event type
            if event_type == "AgentInitializedEvent":
                print(f"{prefix}├── Initialized (model: {event.model_name})")
            
            elif event_type == "UserMessageEvent":
                message = event.message[:40] + "..." if len(event.message) > 40 else event.message
                print(f"{prefix}├── User message: {message}")
            
            elif event_type == "FunctionCallEvent":
                args_str = self._format_args(event.function_args)
                call_id = getattr(event, 'function_call_id', None)
                if call_id:
                    call_id_short = call_id[:8]
                    print(f"{prefix}├── Function call: {event.function_name}({args_str}) [id:{call_id_short}]")
                else:
                    print(f"{prefix}├── Function call: {event.function_name}({args_str})")
            
            elif event_type == "FunctionResultEvent":
                result_str = str(event.result)[:40] + "..." if len(str(event.result)) > 40 else str(event.result)
                call_id = getattr(event, 'function_call_id', None)
                if call_id:
                    call_id_short = call_id[:8]
                    if event.error:
                        print(f"{prefix}├── Function error: {event.error[:40]}... [id:{call_id_short}]")
                    else:
                        print(f"{prefix}├── Function result: {result_str} [id:{call_id_short}]")
                else:
                    if event.error:
                        print(f"{prefix}├── Function error: {event.error[:40]}...")
                    else:
                        print(f"{prefix}├── Function result: {result_str}")
            
            elif event_type == "AgentResponseEvent":
                response = event.response[:40] + "..." if len(event.response) > 40 else event.response
                print(f"{prefix}└── Response: {response}")
    
    def _format_args(self, args: Dict) -> str:
        """Format function arguments for display."""
        if not args:
            return ""
        
        parts = []
        for key, value in args.items():
            parts.append(f"{key}={value}")
        
        return ", ".join(parts)


def generate_context_id() -> str:
    """
    Generate a unique context ID.
    
    Returns:
        A unique context ID
    """
    return str(uuid.uuid4()) 