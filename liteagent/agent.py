"""
LiteAgent - Core agent implementation.

This module contains the main LiteAgent class that handles conversation,
function calling, and response processing.
"""

import json
import time
import litellm
import uuid
from typing import Any, Callable, Dict, List, Optional, Union

from .tools import get_tools, get_function_definitions, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .models import create_model_interface, ModelInterface
from .memory import ConversationMemory
from .utils import logger, log_completion_request, log_completion_response
from .observer import (AgentObserver, AgentEvent, AgentInitializedEvent, UserMessageEvent, 
                      ModelRequestEvent, ModelResponseEvent, FunctionCallEvent, 
                      FunctionResultEvent, AgentResponseEvent, generate_context_id)

class LiteAgent:
    """
    A lightweight agent that uses LiteLLM for LLM interactions and tool usage.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. 
Use the provided functions when needed to answer the user's question.
IMPORTANT: After calling a function and receiving its result, you MUST provide a complete 
text response to the user. DO NOT call the same function multiple times with the same arguments.
DO NOT call functions repeatedly if you already have the information needed.
If you've already received the information you need from a function call, use that information
to provide a final text response to the user."""

    def __init__(self, model, name, system_prompt=None, tools=None, debug=False, drop_params=True, 
                 parent_context_id=None, context_id=None, observers=None):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            drop_params (bool, optional): Whether to drop unsupported parameters. Defaults to True.
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.drop_params = drop_params
        self.parent_context_id = parent_context_id
        self.context_id = context_id or generate_context_id()
        self.agent_id = str(uuid.uuid4())
        
        # Initialize the model interface
        self.model_interface = create_model_interface(model, drop_params)
        
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
            all_tools = get_tools()
            self._register_tools(all_tools)
            
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
        
        self._log(f"Initialized agent {self.name} with model {self.model}")
        
    def _register_tools(self, tool_functions):
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
        
    def _emit_event(self, event: AgentEvent) -> None:
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
                
    def add_observer(self, observer: AgentObserver) -> None:
        """
        Add an observer to the agent.
        
        Args:
            observer: The observer to add
        """
        if observer not in self.observers:
            self.observers.append(observer)
            
    def remove_observer(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the agent.
        
        Args:
            observer: The observer to remove
        """
        if observer in self.observers:
            self.observers.remove(observer)
            
    def chat(self, message: str) -> str:
        """
        Chat with the agent.
        
        Args:
            message: The user's message
            
        Returns:
            str: The agent's response
        """
        # Add user message to memory
        self.memory.add_user_message(message)
        
        # Emit user message event
        self._emit_event(UserMessageEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            message=message
        ))
        
        # Get messages from memory
        messages = self.memory.get_messages()
        
        # Get function definitions
        functions = list(self.tools.values()) if self.tools else None
        
        function_called = False
        max_consecutive_function_calls = 10
        consecutive_function_calls = 0
        
        # Track function calls to detect loops
        function_call_counts = {}
        
        while consecutive_function_calls < max_consecutive_function_calls:
            # Emit model request event
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                parent_context_id=self.parent_context_id,
                messages=messages,
                functions=functions
            ))
            
            # Generate a response
            response = self.model_interface.generate_response(messages, functions)
            
            # Emit model response event
            self._emit_event(ModelResponseEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                parent_context_id=self.parent_context_id,
                response=response
            ))
            
            # Check if the model wants to call a function
            tool_calls = self.model_interface.extract_tool_calls(response)
            
            if tool_calls:
                function_called = True
                consecutive_function_calls += 1
                
                # Process each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.get('name')
                    function_args = tool_call.get('arguments', {})
                    function_id = tool_call.get('id', str(uuid.uuid4()))
                    
                    # Try to parse function arguments as JSON if it's a string
                    if isinstance(function_args, str):
                        try:
                            function_args = json.loads(function_args)
                        except json.JSONDecodeError:
                            # Handle error case
                            error_message = f"Error parsing arguments for function {function_name}: {function_args}"
                            logger.error(error_message)
                            # Add function call error to memory
                            self.memory.add_function_result(function_name, error_message, function_args)
                            continue
                    
                    # Check for repeated function calls with same arguments
                    call_key = f"{function_name}:{json.dumps(function_args, sort_keys=True)}"
                    function_call_counts[call_key] = function_call_counts.get(call_key, 0) + 1
                    
                    # If the same function with same args has been called too many times, break the loop
                    if function_call_counts[call_key] >= 2:
                        logger.warning(f"Detected repeated function call: {function_name} with args {function_args}")
                        # Force the agent to generate a text response instead
                        self.memory.add_system_message(
                            "IMPORTANT: You have called the same function multiple times with the same arguments. "
                            "You MUST now provide a final text response based on the information you already have. "
                            "DO NOT make any more function calls. Summarize what you know and respond directly to the user."
                        )
                        
                        # Get updated messages
                        messages = self.memory.get_messages()
                        
                        # Make one more model call to get a text response
                        self._emit_event(ModelRequestEvent(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            context_id=self.context_id,
                            parent_context_id=self.parent_context_id,
                            messages=messages,
                            functions=None  # Don't provide functions to force a text response
                        ))
                        
                        # Generate a response without function calling
                        final_response = self.model_interface.generate_response(messages, None)
                        
                        # Emit model response event
                        self._emit_event(ModelResponseEvent(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            context_id=self.context_id,
                            parent_context_id=self.parent_context_id,
                            response=final_response
                        ))
                        
                        # Extract the text content
                        content = self.model_interface.extract_content(final_response)
                        
                        # Add assistant message to memory
                        self.memory.add_assistant_message(content)
                        
                        # Emit agent response event
                        self._emit_event(AgentResponseEvent(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            context_id=self.context_id,
                            parent_context_id=self.parent_context_id,
                            response=content
                        ))
                        
                        # Return the final response
                        return content
                    
                    # Emit function call event
                    self._emit_event(FunctionCallEvent(
                        agent_id=self.agent_id,
                        agent_name=self.name,
                        context_id=self.context_id,
                        parent_context_id=self.parent_context_id,
                        function_name=function_name,
                        function_args=function_args,
                        function_call_id=function_id
                    ))
                    
                    # Execute the function
                    if function_name in self.tool_instances:
                        try:
                            tool = self.tool_instances[function_name]
                            # Pass the context_id to the tool so it can set the parent-child relationship
                            function_args['_context_id'] = self.context_id
                            function_result = tool.execute(**function_args)
                            
                            # Add result to memory with the function call ID
                            self.memory.add_function_result(
                                name=function_name, 
                                content=function_result, 
                                args=function_args,
                                call_id=function_id,
                                provider=self.model_interface.provider
                            )
                            
                            # Emit function result event
                            self._emit_event(FunctionResultEvent(
                                agent_id=self.agent_id,
                                agent_name=self.name,
                                context_id=self.context_id,
                                parent_context_id=self.parent_context_id,
                                function_name=function_name,
                                function_args=function_args,
                                result=function_result,
                                function_call_id=function_id
                            ))
                        except Exception as e:
                            error_message = f"Error executing function {function_name}: {str(e)}"
                            logger.error(error_message)
                            
                            # Add function call error to memory with the function call ID
                            self.memory.add_function_result(
                                name=function_name, 
                                content=error_message, 
                                args=function_args,
                                call_id=function_id,
                                is_error=True,
                                provider=self.model_interface.provider
                            )
                            
                            # Emit function result event with error
                            self._emit_event(FunctionResultEvent(
                                agent_id=self.agent_id,
                                agent_name=self.name,
                                context_id=self.context_id,
                                parent_context_id=self.parent_context_id,
                                function_name=function_name,
                                function_args=function_args,
                                error=str(e),
                                function_call_id=function_id
                            ))
                    else:
                        error_message = f"Function {function_name} not found"
                        logger.error(error_message)
                        
                        # Add function call error to memory with the function call ID
                        self.memory.add_function_result(
                            name=function_name, 
                            content=error_message, 
                            args=function_args,
                            call_id=function_id,
                            is_error=True,
                            provider=self.model_interface.provider
                        )
                        
                        # Emit function result event with error
                        self._emit_event(FunctionResultEvent(
                            agent_id=self.agent_id,
                            agent_name=self.name,
                            context_id=self.context_id,
                            parent_context_id=self.parent_context_id,
                            function_name=function_name,
                            function_args=function_args,
                            error=error_message,
                            function_call_id=function_id
                        ))
                
                # Get updated messages after processing all tool calls
                messages = self.memory.get_messages()
            else:
                # Extract the text content
                content = self.model_interface.extract_content(response)
                
                # Add assistant message to memory
                self.memory.add_assistant_message(content)
                
                # Emit agent response event
                self._emit_event(AgentResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    parent_context_id=self.parent_context_id,
                    response=content
                ))
                
                return content
        
        # If we've reached the maximum number of consecutive function calls,
        # force the agent to generate a text response
        self.memory.add_system_message(
            "IMPORTANT: You have made too many consecutive function calls. "
            "You MUST now provide a final text response based on the information you have. "
            "DO NOT make any more function calls. Summarize what you know and respond directly to the user."
        )
        
        # Get updated messages
        messages = self.memory.get_messages()
        
        # Make one more model call to get a text response
        self._emit_event(ModelRequestEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            messages=messages,
            functions=None  # Don't provide functions to force a text response
        ))
        
        # Generate a response without function calling
        final_response = self.model_interface.generate_response(messages, None)
        
        # Emit model response event
        self._emit_event(ModelResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            response=final_response
        ))
        
        # Extract the text content
        content = self.model_interface.extract_content(final_response)
        
        # Add assistant message to memory
        self.memory.add_assistant_message(content)
        
        # Emit agent response event
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            parent_context_id=self.parent_context_id,
            response=content
        ))
        
        # Return the final response
        return content
    
    def reset_memory(self):
        """Reset the agent's memory."""
        self.memory = ConversationMemory(system_prompt=self.system_prompt)
        
    def _log(self, message, level="debug"):
        """Log a message if debug is enabled."""
        if self.debug:
            if level == "debug":
                logger.debug(message)
            elif level == "info":
                logger.info(message)
            elif level == "warning":
                logger.warning(message)
            elif level == "error":
                logger.error(message)