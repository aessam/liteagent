"""
LiteAgent - Core agent implementation.

This module contains the main LiteAgent class that handles conversation,
function calling, and response processing.
"""

import json
import time
import litellm
from typing import Any, Callable, Dict, List, Optional, Union

from .tools import get_tools, get_function_definitions, BaseTool, FunctionTool, InstanceMethodTool, StaticMethodTool
from .models import create_model_interface, ModelInterface
from .memory import ConversationMemory
from .utils import logger, log_completion_request, log_completion_response

class LiteAgent:
    """
    A lightweight agent that uses LiteLLM for LLM interactions and tool usage.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. 
Use the provided functions when needed to answer the user's question. 
After calling a function and receiving its result, you MUST provide a complete 
text response to the user. Do not call functions repeatedly if you already 
have the information needed."""

    def __init__(self, model, name, system_prompt=None, tools=None, debug=False, drop_params=True):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use. If None, uses all globally registered tools.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            drop_params (bool, optional): Whether to drop unsupported parameters. Defaults to True.
        """
        self.model_name = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.drop_params = drop_params
        
        # Set global litellm setting for dropping unsupported parameters
        litellm.drop_params = self.drop_params
        
        # Initialize model interface
        self.model_interface = create_model_interface(self.model_name, self.drop_params)
        
        # Initialize memory
        self.memory = ConversationMemory(self.system_prompt)
        
        # Initialize tools
        self.tools = {}
        self.tool_instances = {}  # Store tool instances for reference
        if tools is not None:
            # Register the provided tools
            self._register_tools(tools)
        else:
            # Use all globally registered tools
            self.tools = get_tools()

    def _register_tools(self, tool_functions):
        """
        Register the provided tool functions for this agent instance.
        
        Args:
            tool_functions (list): List of functions, methods, or BaseTool objects to register as tools
        """
        import inspect
        
        for tool_or_func in tool_functions:
            # Check if the item is already a BaseTool instance
            if isinstance(tool_or_func, BaseTool):
                tool = tool_or_func
                self.tool_instances[tool.name] = tool
            else:
                # Create the appropriate tool instance based on the function type
                func = tool_or_func
                if inspect.ismethod(func):
                    # For bound methods
                    if func.__self__ is not None:
                        tool = InstanceMethodTool(func, func.__self__)
                        # Store the instance for reference
                        self.tool_instances[tool.name] = tool
                    else:
                        # For static/class methods
                        tool = StaticMethodTool(func)
                        self.tool_instances[tool.name] = tool
                else:
                    # For regular functions
                    tool = FunctionTool(func)
                    self.tool_instances[tool.name] = tool
            
            # Store in tools dictionary
            self.tools[tool.name] = {
                "schema": tool.schema,
                "function": tool.func
            }

    def reset_memory(self):
        """Reset conversation history to only include the system prompt."""
        self.memory.reset()

    def _log(self, message, level="debug"):
        """Log a message at the specified level if debug mode is enabled."""
        if self.debug:
            log_method = getattr(logger, level.lower(), logger.debug)
            log_method(message)

    def chat(self, user_input):
        """
        Process a single user query, potentially calling tools if needed.
        
        Args:
            user_input (str): User's query
            
        Returns:
            str: Agent's response
        """
        # Add user input to memory
        self.memory.add_user_message(user_input)
        
        max_iterations = 5  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}")

            # Get response from LLM
            try:
                response = self._get_llm_response()
            except Exception as e:
                logger.error(f"Error calling LLM API: {str(e)}")
                return f"Error calling LLM API: {str(e)}"

            # Process the response
            result = self._process_response(response, iteration)
            
            # If we got a final result, return it
            if result is not None:
                return result
                
            # Check if we're in a function calling loop
            last_call = self.memory.last_function_call
            if last_call and self.memory.is_function_call_loop(last_call["name"], last_call["args"]):
                logger.warning(f"Function call loop detected for {last_call['name']}. Breaking loop.")
                
                # Get the last function result
                last_result = self.memory.get_last_function_result(last_call["name"]) or "unknown"
                
                # Force a final response
                self.memory.add_system_message(
                    f"You have called {last_call['name']} multiple times. The result is: {last_result}. "
                    "Please provide a FINAL answer to the user without calling any more functions."
                )
                
                try:
                    final_response = self._get_llm_response()
                    content = self.model_interface.extract_content(final_response)
                    if content:
                        self.memory.add_assistant_message(content)
                        return content
                except Exception as e:
                    logger.error(f"Error getting final response: {str(e)}")
                
                # If we couldn't get a good final response, create one from the function result
                final_answer = f"Based on the information I have, {last_result}"
                self.memory.add_assistant_message(final_answer)
                return final_answer

        # Fallback if no non-empty answer is produced
        return "No complete response generated after maximum iterations."

    def _get_llm_response(self):
        """
        Get a response from the LLM.
        
        Returns:
            The response from the LLM
        """
        # Get function definitions from the agent's own tools
        function_definitions = []
        if self.model_interface.supports_function_calling():
            for tool_name, tool_instance in self.tool_instances.items():
                function_definitions.append(tool_instance.to_function_definition())
        
        # Get response from model interface
        return self.model_interface.generate_response(
            messages=self.memory.get_messages(),
            functions=function_definitions
        )

    def _process_response(self, response, iteration):
        """
        Process the response from the LLM.
        
        Args:
            response: Response from the LLM
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        # Extract function call if present
        function_call = self.model_interface.extract_function_call(response)
        
        if function_call:
            # Handle function call
            function_name = function_call["name"]
            function_args = function_call["arguments"]
            
            return self._handle_function_call(function_name, function_args, iteration)
        
        # Handle text content
        content = self.model_interface.extract_content(response)
        if content:
            logger.info(f"Model response: {content}")
            self.memory.add_assistant_message(content)
            return content
            
        return None

    def _handle_function_call(self, function_name, function_args, iteration):
        """
        Handle a function call from the LLM.
        
        Args:
            function_name (str): Name of the function to call
            function_args (dict): Arguments to pass to the function
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        logger.info(f"Function call detected: {function_name} with args: {function_args}")
        
        if function_name not in self.tools:
            error_msg = f"Tool {function_name} is not registered with this agent."
            logger.warning(error_msg)
            self.memory.add_assistant_message(error_msg)
            return error_msg
            
        # Check if this is a repeated call (same function with same normalized arguments)
        if self.memory.is_function_call_loop(function_name, function_args):
            logger.warning("Detected repeated function call! Breaking loop.")
            # Get the last function result from memory
            last_result = self.memory.get_last_function_result(function_name) or "unknown"
            
            # Create a more helpful response that encourages the model to give a final answer
            response = f"I already have the information from {function_name}. The result was: {last_result}. Let me provide a complete answer to your question."
            self.memory.add_assistant_message(response)
            
            # For models without native function calling, add an explicit instruction
            if not self.model_interface.supports_function_calling():
                self.memory.add_system_message(
                    "You have all the information needed. Please provide a final, complete answer to the user's question without calling any more functions."
                )
            
            return response
        
        try:
            # Execute the function using the tool instance
            if function_name in self.tool_instances:
                # Use the execute method of the tool instance
                function_response = self.tool_instances[function_name].execute(**function_args)
            else:
                # This should not happen if tools are registered correctly
                error_msg = f"Tool {function_name} is registered but no tool instance found."
                logger.error(error_msg)
                self.memory.add_system_message(error_msg)
                return error_msg
            
            # Add function result to memory
            self.memory.add_function_result(function_name, function_response, function_args)
            
            # Add a conversational prompt to guide the model to give a more natural final answer
            if iteration >= 1:  # Add guidance after the first iteration
                # Add a system message to encourage a final response
                guidance = f"You now have the result from {function_name}: {function_response}. Please provide a complete, final answer to the user's question using this information. Do not call the same function again."
                
                self.memory.add_system_message(guidance)
            
            logger.info(f"Function executed: {function_name}, result: {function_response}")
            return None  # Continue the loop
            
        except Exception as e:
            error_msg = f"Error executing {function_name}: {str(e)}"
            logger.error(f"Function error: {error_msg}")
            self.memory.add_function_result(function_name, error_msg)
            return None