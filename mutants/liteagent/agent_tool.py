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

# Function definition for tool calling
class FunctionDefinition:
    """
    Represents a function definition for tool calling.
    
    This class is used to define functions that can be called by an LLM.
    """
    
    def xǁFunctionDefinitionǁ__init____mutmut_orig(self, name: str, description: str, parameters: Dict[str, Any]):
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
    
    def xǁFunctionDefinitionǁ__init____mutmut_1(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Initialize a function definition.
        
        Args:
            name: The name of the function
            description: A description of what the function does
            parameters: A dictionary defining the parameters
        """
        self.name = None
        self.description = description
        self.parameters = parameters
    
    def xǁFunctionDefinitionǁ__init____mutmut_2(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Initialize a function definition.
        
        Args:
            name: The name of the function
            description: A description of what the function does
            parameters: A dictionary defining the parameters
        """
        self.name = name
        self.description = None
        self.parameters = parameters
    
    def xǁFunctionDefinitionǁ__init____mutmut_3(self, name: str, description: str, parameters: Dict[str, Any]):
        """
        Initialize a function definition.
        
        Args:
            name: The name of the function
            description: A description of what the function does
            parameters: A dictionary defining the parameters
        """
        self.name = name
        self.description = description
        self.parameters = None
    
    xǁFunctionDefinitionǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionDefinitionǁ__init____mutmut_1': xǁFunctionDefinitionǁ__init____mutmut_1, 
        'xǁFunctionDefinitionǁ__init____mutmut_2': xǁFunctionDefinitionǁ__init____mutmut_2, 
        'xǁFunctionDefinitionǁ__init____mutmut_3': xǁFunctionDefinitionǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionDefinitionǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionDefinitionǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionDefinitionǁ__init____mutmut_orig)
    xǁFunctionDefinitionǁ__init____mutmut_orig.__name__ = 'xǁFunctionDefinitionǁ__init__'
    
    def xǁFunctionDefinitionǁto_dict__mutmut_orig(self) -> Dict[str, Any]:
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
    
    def xǁFunctionDefinitionǁto_dict__mutmut_1(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "XXnameXX": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    def xǁFunctionDefinitionǁto_dict__mutmut_2(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "NAME": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    def xǁFunctionDefinitionǁto_dict__mutmut_3(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "name": self.name,
            "XXdescriptionXX": self.description,
            "parameters": self.parameters
        }
    
    def xǁFunctionDefinitionǁto_dict__mutmut_4(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "name": self.name,
            "DESCRIPTION": self.description,
            "parameters": self.parameters
        }
    
    def xǁFunctionDefinitionǁto_dict__mutmut_5(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "name": self.name,
            "description": self.description,
            "XXparametersXX": self.parameters
        }
    
    def xǁFunctionDefinitionǁto_dict__mutmut_6(self) -> Dict[str, Any]:
        """
        Convert the function definition to a dictionary.
        
        Returns:
            A dictionary representation of the function definition
        """
        return {
            "name": self.name,
            "description": self.description,
            "PARAMETERS": self.parameters
        }
    
    xǁFunctionDefinitionǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionDefinitionǁto_dict__mutmut_1': xǁFunctionDefinitionǁto_dict__mutmut_1, 
        'xǁFunctionDefinitionǁto_dict__mutmut_2': xǁFunctionDefinitionǁto_dict__mutmut_2, 
        'xǁFunctionDefinitionǁto_dict__mutmut_3': xǁFunctionDefinitionǁto_dict__mutmut_3, 
        'xǁFunctionDefinitionǁto_dict__mutmut_4': xǁFunctionDefinitionǁto_dict__mutmut_4, 
        'xǁFunctionDefinitionǁto_dict__mutmut_5': xǁFunctionDefinitionǁto_dict__mutmut_5, 
        'xǁFunctionDefinitionǁto_dict__mutmut_6': xǁFunctionDefinitionǁto_dict__mutmut_6
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionDefinitionǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁFunctionDefinitionǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁFunctionDefinitionǁto_dict__mutmut_orig)
    xǁFunctionDefinitionǁto_dict__mutmut_orig.__name__ = 'xǁFunctionDefinitionǁto_dict'

class AgentTool(BaseTool):
    """
    Tool implementation for using a LiteAgent as a tool.
    This allows for nested agent architectures where one agent can delegate tasks to other agents.
    """
    
    def xǁAgentToolǁ__init____mutmut_orig(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
    
    def xǁAgentToolǁ__init____mutmut_1(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        self.agent = None
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
    
    def xǁAgentToolǁ__init____mutmut_2(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        self.message_template = None
        
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
    
    def xǁAgentToolǁ__init____mutmut_3(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        tool_name = None
        
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
    
    def xǁAgentToolǁ__init____mutmut_4(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        tool_name = name and f"{agent.name}"
        
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
    
    def xǁAgentToolǁ__init____mutmut_5(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        tool_description = None
        
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
    
    def xǁAgentToolǁ__init____mutmut_6(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        tool_description = description and agent.system_prompt
        
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
    
    def xǁAgentToolǁ__init____mutmut_7(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                original_parent_context_id = None
                
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
    
    def xǁAgentToolǁ__init____mutmut_8(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    if 'XXparent_context_idXX' in kwargs:
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
    
    def xǁAgentToolǁ__init____mutmut_9(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    if 'PARENT_CONTEXT_ID' in kwargs:
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
    
    def xǁAgentToolǁ__init____mutmut_10(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    if 'parent_context_id' not in kwargs:
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
    
    def xǁAgentToolǁ__init____mutmut_11(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        self.agent.parent_context_id = None
                    
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
    
    def xǁAgentToolǁ__init____mutmut_12(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        self.agent.parent_context_id = kwargs.pop(None)
                    
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
    
    def xǁAgentToolǁ__init____mutmut_13(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        self.agent.parent_context_id = kwargs.pop('XXparent_context_idXX')
                    
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
    
    def xǁAgentToolǁ__init____mutmut_14(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        self.agent.parent_context_id = kwargs.pop('PARENT_CONTEXT_ID')
                    
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
    
    def xǁAgentToolǁ__init____mutmut_15(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    
                    if message is None:
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
    
    def xǁAgentToolǁ__init____mutmut_16(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        return self.agent.chat(None)
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
    
    def xǁAgentToolǁ__init____mutmut_17(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        formatted_message = None
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
    
    def xǁAgentToolǁ__init____mutmut_18(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        return self.agent.chat(None)
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
    
    def xǁAgentToolǁ__init____mutmut_19(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    self.agent.parent_context_id = None
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
    
    def xǁAgentToolǁ__init____mutmut_20(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                original_parent_context_id = None
                
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
    
    def xǁAgentToolǁ__init____mutmut_21(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                        self.agent.parent_context_id = None
                    
                    return self.agent.chat(message)
                finally:
                    # Restore the original parent_context_id
                    self.agent.parent_context_id = original_parent_context_id
        
        # Initialize the BaseTool with the wrapper function
        super().__init__(agent_wrapper, tool_name, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_22(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    
                    return self.agent.chat(None)
                finally:
                    # Restore the original parent_context_id
                    self.agent.parent_context_id = original_parent_context_id
        
        # Initialize the BaseTool with the wrapper function
        super().__init__(agent_wrapper, tool_name, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_23(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
                    self.agent.parent_context_id = None
        
        # Initialize the BaseTool with the wrapper function
        super().__init__(agent_wrapper, tool_name, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_24(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        super().__init__(None, tool_name, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_25(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        super().__init__(agent_wrapper, None, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_26(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        super().__init__(agent_wrapper, tool_name, None)
    
    def xǁAgentToolǁ__init____mutmut_27(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        super().__init__(tool_name, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_28(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        super().__init__(agent_wrapper, tool_description)
    
    def xǁAgentToolǁ__init____mutmut_29(self, agent: 'LiteAgent', name: Optional[str] = None, description: Optional[str] = None, 
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
        super().__init__(agent_wrapper, tool_name, )
    
    xǁAgentToolǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentToolǁ__init____mutmut_1': xǁAgentToolǁ__init____mutmut_1, 
        'xǁAgentToolǁ__init____mutmut_2': xǁAgentToolǁ__init____mutmut_2, 
        'xǁAgentToolǁ__init____mutmut_3': xǁAgentToolǁ__init____mutmut_3, 
        'xǁAgentToolǁ__init____mutmut_4': xǁAgentToolǁ__init____mutmut_4, 
        'xǁAgentToolǁ__init____mutmut_5': xǁAgentToolǁ__init____mutmut_5, 
        'xǁAgentToolǁ__init____mutmut_6': xǁAgentToolǁ__init____mutmut_6, 
        'xǁAgentToolǁ__init____mutmut_7': xǁAgentToolǁ__init____mutmut_7, 
        'xǁAgentToolǁ__init____mutmut_8': xǁAgentToolǁ__init____mutmut_8, 
        'xǁAgentToolǁ__init____mutmut_9': xǁAgentToolǁ__init____mutmut_9, 
        'xǁAgentToolǁ__init____mutmut_10': xǁAgentToolǁ__init____mutmut_10, 
        'xǁAgentToolǁ__init____mutmut_11': xǁAgentToolǁ__init____mutmut_11, 
        'xǁAgentToolǁ__init____mutmut_12': xǁAgentToolǁ__init____mutmut_12, 
        'xǁAgentToolǁ__init____mutmut_13': xǁAgentToolǁ__init____mutmut_13, 
        'xǁAgentToolǁ__init____mutmut_14': xǁAgentToolǁ__init____mutmut_14, 
        'xǁAgentToolǁ__init____mutmut_15': xǁAgentToolǁ__init____mutmut_15, 
        'xǁAgentToolǁ__init____mutmut_16': xǁAgentToolǁ__init____mutmut_16, 
        'xǁAgentToolǁ__init____mutmut_17': xǁAgentToolǁ__init____mutmut_17, 
        'xǁAgentToolǁ__init____mutmut_18': xǁAgentToolǁ__init____mutmut_18, 
        'xǁAgentToolǁ__init____mutmut_19': xǁAgentToolǁ__init____mutmut_19, 
        'xǁAgentToolǁ__init____mutmut_20': xǁAgentToolǁ__init____mutmut_20, 
        'xǁAgentToolǁ__init____mutmut_21': xǁAgentToolǁ__init____mutmut_21, 
        'xǁAgentToolǁ__init____mutmut_22': xǁAgentToolǁ__init____mutmut_22, 
        'xǁAgentToolǁ__init____mutmut_23': xǁAgentToolǁ__init____mutmut_23, 
        'xǁAgentToolǁ__init____mutmut_24': xǁAgentToolǁ__init____mutmut_24, 
        'xǁAgentToolǁ__init____mutmut_25': xǁAgentToolǁ__init____mutmut_25, 
        'xǁAgentToolǁ__init____mutmut_26': xǁAgentToolǁ__init____mutmut_26, 
        'xǁAgentToolǁ__init____mutmut_27': xǁAgentToolǁ__init____mutmut_27, 
        'xǁAgentToolǁ__init____mutmut_28': xǁAgentToolǁ__init____mutmut_28, 
        'xǁAgentToolǁ__init____mutmut_29': xǁAgentToolǁ__init____mutmut_29
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentToolǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAgentToolǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAgentToolǁ__init____mutmut_orig)
    xǁAgentToolǁ__init____mutmut_orig.__name__ = 'xǁAgentToolǁ__init__'
    
    def xǁAgentToolǁexecute__mutmut_orig(self, **kwargs) -> Any:
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
    
    def xǁAgentToolǁexecute__mutmut_1(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = None
        
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
    
    def xǁAgentToolǁexecute__mutmut_2(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Validate arguments using the schema
            validated_args = None
            
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
    
    def xǁAgentToolǁexecute__mutmut_3(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Validate arguments using the schema
            validated_args = self.schema(**kwargs)
            
            # Get the parent context ID from the calling agent's context
            # This is passed implicitly by the LiteAgent when calling tools
            parent_context_id = None
            
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
    
    def xǁAgentToolǁexecute__mutmut_4(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Validate arguments using the schema
            validated_args = self.schema(**kwargs)
            
            # Get the parent context ID from the calling agent's context
            # This is passed implicitly by the LiteAgent when calling tools
            parent_context_id = kwargs.get(None)
            
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
    
    def xǁAgentToolǁexecute__mutmut_5(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Validate arguments using the schema
            validated_args = self.schema(**kwargs)
            
            # Get the parent context ID from the calling agent's context
            # This is passed implicitly by the LiteAgent when calling tools
            parent_context_id = kwargs.get('XX_context_idXX')
            
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
    
    def xǁAgentToolǁexecute__mutmut_6(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Save the original parent_context_id
        original_parent_context_id = self.agent.parent_context_id
        
        try:
            # Validate arguments using the schema
            validated_args = self.schema(**kwargs)
            
            # Get the parent context ID from the calling agent's context
            # This is passed implicitly by the LiteAgent when calling tools
            parent_context_id = kwargs.get('_CONTEXT_ID')
            
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
    
    def xǁAgentToolǁexecute__mutmut_7(self, **kwargs) -> Any:
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
                self.agent.parent_context_id = None
            
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
    
    def xǁAgentToolǁexecute__mutmut_8(self, **kwargs) -> Any:
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
            message = ""
            
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
    
    def xǁAgentToolǁexecute__mutmut_9(self, **kwargs) -> Any:
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
            if 'XXmessageXX' in validated_args.model_dump():
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
    
    def xǁAgentToolǁexecute__mutmut_10(self, **kwargs) -> Any:
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
            if 'MESSAGE' in validated_args.model_dump():
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
    
    def xǁAgentToolǁexecute__mutmut_11(self, **kwargs) -> Any:
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
            if 'message' not in validated_args.model_dump():
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
    
    def xǁAgentToolǁexecute__mutmut_12(self, **kwargs) -> Any:
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
                message = None
            
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
    
    def xǁAgentToolǁexecute__mutmut_13(self, **kwargs) -> Any:
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
                message = validated_args.model_dump()['XXmessageXX']
            
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
    
    def xǁAgentToolǁexecute__mutmut_14(self, **kwargs) -> Any:
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
                message = validated_args.model_dump()['MESSAGE']
            
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
    
    def xǁAgentToolǁexecute__mutmut_15(self, **kwargs) -> Any:
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
                if 'kwargs' in validated_args.model_dump() or isinstance(validated_args.model_dump()['kwargs'], dict):
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
    
    def xǁAgentToolǁexecute__mutmut_16(self, **kwargs) -> Any:
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
                if 'XXkwargsXX' in validated_args.model_dump() and isinstance(validated_args.model_dump()['kwargs'], dict):
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
    
    def xǁAgentToolǁexecute__mutmut_17(self, **kwargs) -> Any:
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
                if 'KWARGS' in validated_args.model_dump() and isinstance(validated_args.model_dump()['kwargs'], dict):
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
    
    def xǁAgentToolǁexecute__mutmut_18(self, **kwargs) -> Any:
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
                if 'kwargs' not in validated_args.model_dump() and isinstance(validated_args.model_dump()['kwargs'], dict):
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
    
    def xǁAgentToolǁexecute__mutmut_19(self, **kwargs) -> Any:
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
                    nested_kwargs = None
                    message = self.message_template.format(**nested_kwargs)
            
            # If we have a message, use it to chat with the agent
            if message is not None:
                return self.agent.chat(message)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def xǁAgentToolǁexecute__mutmut_20(self, **kwargs) -> Any:
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
                    nested_kwargs = validated_args.model_dump()['XXkwargsXX']
                    message = self.message_template.format(**nested_kwargs)
            
            # If we have a message, use it to chat with the agent
            if message is not None:
                return self.agent.chat(message)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def xǁAgentToolǁexecute__mutmut_21(self, **kwargs) -> Any:
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
                    nested_kwargs = validated_args.model_dump()['KWARGS']
                    message = self.message_template.format(**nested_kwargs)
            
            # If we have a message, use it to chat with the agent
            if message is not None:
                return self.agent.chat(message)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def xǁAgentToolǁexecute__mutmut_22(self, **kwargs) -> Any:
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
                    message = None
            
            # If we have a message, use it to chat with the agent
            if message is not None:
                return self.agent.chat(message)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def xǁAgentToolǁexecute__mutmut_23(self, **kwargs) -> Any:
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
            if message is None:
                return self.agent.chat(message)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def xǁAgentToolǁexecute__mutmut_24(self, **kwargs) -> Any:
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
                return self.agent.chat(None)
            
            # Otherwise, call the function with the validated arguments
            return self.func(**validated_args.model_dump())
        finally:
            # Restore the original parent_context_id
            self.agent.parent_context_id = original_parent_context_id
    
    def xǁAgentToolǁexecute__mutmut_25(self, **kwargs) -> Any:
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
            self.agent.parent_context_id = None
    
    xǁAgentToolǁexecute__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentToolǁexecute__mutmut_1': xǁAgentToolǁexecute__mutmut_1, 
        'xǁAgentToolǁexecute__mutmut_2': xǁAgentToolǁexecute__mutmut_2, 
        'xǁAgentToolǁexecute__mutmut_3': xǁAgentToolǁexecute__mutmut_3, 
        'xǁAgentToolǁexecute__mutmut_4': xǁAgentToolǁexecute__mutmut_4, 
        'xǁAgentToolǁexecute__mutmut_5': xǁAgentToolǁexecute__mutmut_5, 
        'xǁAgentToolǁexecute__mutmut_6': xǁAgentToolǁexecute__mutmut_6, 
        'xǁAgentToolǁexecute__mutmut_7': xǁAgentToolǁexecute__mutmut_7, 
        'xǁAgentToolǁexecute__mutmut_8': xǁAgentToolǁexecute__mutmut_8, 
        'xǁAgentToolǁexecute__mutmut_9': xǁAgentToolǁexecute__mutmut_9, 
        'xǁAgentToolǁexecute__mutmut_10': xǁAgentToolǁexecute__mutmut_10, 
        'xǁAgentToolǁexecute__mutmut_11': xǁAgentToolǁexecute__mutmut_11, 
        'xǁAgentToolǁexecute__mutmut_12': xǁAgentToolǁexecute__mutmut_12, 
        'xǁAgentToolǁexecute__mutmut_13': xǁAgentToolǁexecute__mutmut_13, 
        'xǁAgentToolǁexecute__mutmut_14': xǁAgentToolǁexecute__mutmut_14, 
        'xǁAgentToolǁexecute__mutmut_15': xǁAgentToolǁexecute__mutmut_15, 
        'xǁAgentToolǁexecute__mutmut_16': xǁAgentToolǁexecute__mutmut_16, 
        'xǁAgentToolǁexecute__mutmut_17': xǁAgentToolǁexecute__mutmut_17, 
        'xǁAgentToolǁexecute__mutmut_18': xǁAgentToolǁexecute__mutmut_18, 
        'xǁAgentToolǁexecute__mutmut_19': xǁAgentToolǁexecute__mutmut_19, 
        'xǁAgentToolǁexecute__mutmut_20': xǁAgentToolǁexecute__mutmut_20, 
        'xǁAgentToolǁexecute__mutmut_21': xǁAgentToolǁexecute__mutmut_21, 
        'xǁAgentToolǁexecute__mutmut_22': xǁAgentToolǁexecute__mutmut_22, 
        'xǁAgentToolǁexecute__mutmut_23': xǁAgentToolǁexecute__mutmut_23, 
        'xǁAgentToolǁexecute__mutmut_24': xǁAgentToolǁexecute__mutmut_24, 
        'xǁAgentToolǁexecute__mutmut_25': xǁAgentToolǁexecute__mutmut_25
    }
    
    def execute(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentToolǁexecute__mutmut_orig"), object.__getattribute__(self, "xǁAgentToolǁexecute__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute.__signature__ = _mutmut_signature(xǁAgentToolǁexecute__mutmut_orig)
    xǁAgentToolǁexecute__mutmut_orig.__name__ = 'xǁAgentToolǁexecute'
    
    def xǁAgentToolǁadd_observer__mutmut_orig(self, observer: AgentObserver) -> None:
        """
        Add an observer to the underlying agent.
        
        Args:
            observer: The observer to add
        """
        self.agent.add_observer(observer)
    
    def xǁAgentToolǁadd_observer__mutmut_1(self, observer: AgentObserver) -> None:
        """
        Add an observer to the underlying agent.
        
        Args:
            observer: The observer to add
        """
        self.agent.add_observer(None)
    
    xǁAgentToolǁadd_observer__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentToolǁadd_observer__mutmut_1': xǁAgentToolǁadd_observer__mutmut_1
    }
    
    def add_observer(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentToolǁadd_observer__mutmut_orig"), object.__getattribute__(self, "xǁAgentToolǁadd_observer__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_observer.__signature__ = _mutmut_signature(xǁAgentToolǁadd_observer__mutmut_orig)
    xǁAgentToolǁadd_observer__mutmut_orig.__name__ = 'xǁAgentToolǁadd_observer'
    
    def xǁAgentToolǁremove_observer__mutmut_orig(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the underlying agent.
        
        Args:
            observer: The observer to remove
        """
        self.agent.remove_observer(observer) 
    
    def xǁAgentToolǁremove_observer__mutmut_1(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the underlying agent.
        
        Args:
            observer: The observer to remove
        """
        self.agent.remove_observer(None) 
    
    xǁAgentToolǁremove_observer__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAgentToolǁremove_observer__mutmut_1': xǁAgentToolǁremove_observer__mutmut_1
    }
    
    def remove_observer(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAgentToolǁremove_observer__mutmut_orig"), object.__getattribute__(self, "xǁAgentToolǁremove_observer__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_observer.__signature__ = _mutmut_signature(xǁAgentToolǁremove_observer__mutmut_orig)
    xǁAgentToolǁremove_observer__mutmut_orig.__name__ = 'xǁAgentToolǁremove_observer'