"""
AgentTool - Implementation for using LiteAgent instances as tools.

This module provides the AgentTool class that allows using LiteAgent instances
as tools within other LiteAgent instances, enabling nested agent architectures.
"""

import json
from typing import Any, Dict, Optional, List

from .tools import BaseTool
from .agent import LiteAgent
from .observer import AgentObserver

class AgentTool(BaseTool):
    """
    Tool implementation for using a LiteAgent as a tool.
    This allows for nested agent architectures where one agent can delegate tasks to other agents.
    """
    
    def __init__(self, agent: LiteAgent, name: Optional[str] = None, description: Optional[str] = None, 
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
        """
        Execute the agent tool with the given arguments.
        
        Args:
            **kwargs: Arguments to pass to the agent
            
        Returns:
            The agent's response
        """
        # Validate arguments using the schema
        validated_args = self.schema(**kwargs)
        
        # Store the current parent_context_id to restore it later
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Get the parent context ID from the calling agent's context
            # This is passed implicitly by the LiteAgent when calling tools
            parent_context_id = kwargs.get('_context_id')
            
            # Set the parent context ID for the child agent
            if parent_context_id:
                self.agent.parent_context_id = parent_context_id
            
            # Check if there's a direct 'message' parameter
            if 'message' in validated_args.dict():
                message = validated_args.dict()['message']
                if message:
                    return self.agent.chat(message)
            
            # Handle the case where the model passes a dictionary of arguments
            if 'kwargs' in validated_args.dict() and isinstance(validated_args.dict()['kwargs'], dict):
                # Extract the nested kwargs
                nested_kwargs = validated_args.dict()['kwargs']
                
                # Check if there's a 'message' key in the nested kwargs
                if 'message' in nested_kwargs:
                    # Use the message directly
                    return self.agent.chat(nested_kwargs['message'])
                else:
                    # Format the nested kwargs into a message using the template
                    if self.message_template:
                        try:
                            formatted_message = self.message_template.format(**nested_kwargs)
                            return self.agent.chat(formatted_message)
                        except KeyError:
                            # If formatting fails, just use the first value as the message
                            if nested_kwargs:
                                first_key = next(iter(nested_kwargs))
                                return self.agent.chat(str(nested_kwargs[first_key]))
                            else:
                                return "Error: No message provided to the agent."
                    else:
                        # If no template, just use the first value as the message
                        if nested_kwargs:
                            first_key = next(iter(nested_kwargs))
                            return self.agent.chat(str(nested_kwargs[first_key]))
                        else:
                            return "Error: No message provided to the agent."
            else:
                # Call the agent with the validated arguments
                return self.func(**validated_args.dict())
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