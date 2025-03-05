"""
Tool definitions and utilities for LiteAgent.

This module provides classes and functions for defining and working with tools
that can be called by the LiteAgent.
"""

from pydantic import create_model, BaseModel
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union, ForwardRef

# Import tools and observers without circular references
from .tools import BaseTool
from .observer import AgentObserver

# Use a forward reference for LiteAgent to avoid circular imports
LiteAgent = ForwardRef('LiteAgent')

# Function definition for tool calling
class FunctionDefinition:
    """
    Represents a function definition for tool calling.
    
    This class is used to define functions that can be called by an LLM.
    """
    
    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Initialize a function definition.
        
        Args:
            name: The name of the function
            description: A description of what the function does
            parameters: A dictionary defining the parameters
        """
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

class AgentTool(BaseTool):
    """
    Tool implementation for using a LiteAgent as a tool.
    This allows for nested agent architectures where one agent can delegate tasks to other agents.
    """
    
    def __init__(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
                 message_template: Optional[str] = None):
        """
        Initialize an AgentTool.
        
        Args:
            agent: The LiteAgent instance to use as a tool
            name: Optional custom name for the tool (defaults to agent's name)
            description: Optional custom description (defaults to agent's system prompt)
            message_template: Optional template for formatting parameters into a message
                             If not provided, a simple message parameter will be used
        """
        self.agent = agent
        self.message_template = message_template
        
        # Use the agent's name if no custom name is provided
        tool_name = name or f"{agent.name}"
        
        # Use the agent's system prompt as the description if none is provided
        tool_description = description or agent.system_prompt
        
        # Create a wrapper function that handles the agent interaction
        if message_template:
            # For complex parameter structures with a template
            def agent_wrapper(message: str = None, **kwargs) -> str:
                """
                Format parameters into a message using the template and send to the agent.
                
                Args:
                    message: Optional direct message to send to the agent
                    **kwargs: Parameters to format into the message template
                    
                Returns:
                    The agent's response
                """
                # Store the current parent_context_id to restore it later
                original_parent_context_id = self.agent.parent_context_id
                
                try:
                    # Set the parent context ID from the calling agent if available
                    if 'parent_context_id' in kwargs:
                        self.agent.parent_context_id = kwargs.pop('parent_context_id')
                    
                    if message is not None:
                        # If a direct message is provided, use it
                        return self.agent.chat(message)
                    else:
                        # Otherwise, format the kwargs into a message using the template
                        formatted_message = self.message_template.format(**kwargs)
                        return self.agent.chat(formatted_message)
                finally:
                    # Restore the original parent_context_id
                    self.agent.parent_context_id = original_parent_context_id
        else:
            # For simple message parameter
            def agent_wrapper(message: str, parent_context_id: str = None) -> str:
                """
                Send a message to the agent and return its response.
                
                Args:
                    message: The message to send to the agent
                    parent_context_id: Optional parent context ID
                    
                Returns:
                    The agent's response
                """
                # Store the current parent_context_id to restore it later
                original_parent_context_id = self.agent.parent_context_id
                
                try:
                    # Set the parent context ID from the calling agent if available
                    if parent_context_id:
                        self.agent.parent_context_id = parent_context_id
                    
                    return self.agent.chat(message)
                finally:
                    # Restore the original parent_context_id
                    self.agent.parent_context_id = original_parent_context_id
        
        # Initialize the BaseTool with the wrapper function
        super().__init__(agent_wrapper, tool_name, tool_description)
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Validate arguments using the schema
            validated_args = self.schema(**kwargs)
            
            # Get the parent context ID from the calling agent's context
            # This is passed implicitly by the LiteAgent when calling tools
            parent_context_id = kwargs.get('_context_id')
            
            # Set the parent context ID for the child agent
            if parent_context_id:
                self.agent.parent_context_id = parent_context_id
            
            # Initialize message variable
            message = None
            
            # Check if we have a message parameter
            if 'message' in validated_args.model_dump():
                message = validated_args.model_dump()['message']
            
            # If we have a message template, format it with the arguments
            if self.message_template:
                # Check if we have a kwargs parameter for nested formatting
                if 'kwargs' in validated_args.model_dump() and isinstance(validated_args.model_dump()['kwargs'], dict):
                    # Extract the kwargs for nested formatting
                    nested_kwargs = validated_args.model_dump()['kwargs']
                    message = self.message_template.format(**nested_kwargs)
            
            # If we have a message, use it to chat with the agent
            if message is not None:
                return self.agent.chat(message)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def add_observer(self, observer: AgentObserver) -> None:
        """
        Add an observer to the underlying agent.
        
        Args:
            observer: The observer to add
        """
        self.agent.add_observer(observer)
    
    def remove_observer(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the underlying agent.
        
        Args:
            observer: The observer to remove
        """
        self.agent.remove_observer(observer) 