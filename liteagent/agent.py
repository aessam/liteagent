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

    def __init__(self, model, name, system_prompt=None, tools=None, debug=False, 
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
        # Combine custom prompt with default termination logic
        if system_prompt:
            self.system_prompt = f"{system_prompt}\n\n{self.DEFAULT_SYSTEM_PROMPT}"
        else:
            self.system_prompt = self.DEFAULT_SYSTEM_PROMPT
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
        self.observers.append(observer)
        
    def remove_observer(self, observer: AgentObserver) -> None:
        """
        Remove an observer from the agent.
        
        Args:
            observer: The observer to remove
        """
        if observer in self.observers:
            self.observers.remove(observer)
    
    def chat(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
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
    
    def _supports_image_input(self) -> bool:
        """Check if the current model supports image input."""
        capabilities = get_model_capabilities(self.model)
        return capabilities and capabilities.supports_image_input
        
    def _generate_response_with_tools(self, enable_caching: bool = False) -> str:
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
        
    def _prepare_tools(self) -> List[Dict]:
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
        
    def _process_tool_calls(self, tool_calls: List[ToolCall], response: ProviderResponse) -> None:
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
                
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
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
        
        if hasattr(tool_instance, 'execute'):
            # For tool objects
            return tool_instance.execute(**arguments)
        elif callable(tool_instance):
            # For function objects
            return tool_instance(**arguments)
        else:
            raise ValueError(f"Tool {tool_name} is not executable")
    
    def _log(self, message: str) -> None:
        """
        Log a message if debug mode is enabled.
        
        Args:
            message: The message to log
        """
        if self.debug:
            logger.info(f"[{self.name}] {message}")
        
    def reset_memory(self) -> None:
        """Reset the agent's conversation memory."""
        self.memory.reset()
        self._log("Memory reset")
        
    def get_memory(self) -> ConversationMemory:
        """Get the agent's conversation memory."""
        return self.memory
        
    def get_tools(self) -> Dict[str, Dict]:
        """Get the agent's registered tools."""
        return self.tools.copy()
        
    def add_tool(self, tool) -> None:
        """
        Add a single tool to the agent.
        
        Args:
            tool: The tool to add
        """
        self._register_tools([tool])
        
    def remove_tool(self, tool_name: str) -> None:
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


# Backward compatibility alias
LiteAgentNew = LiteAgent