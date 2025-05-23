"""
LiteCodeAgent - Agent for solving problems by writing and executing code.

This module implements a specialized agent that extends LiteAgent to solve
problems by generating and executing code in a secure container environment.
"""

import os
import re
import json
import uuid
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union

from .agent import LiteAgent
from .container_executor import ContainerExecutor, ContainerFactory
from .utils import logger
from .observer import AgentEvent, FunctionResultEvent


class LiteCodeAgent(LiteAgent):
    """
    An agent that solves problems by generating and executing code in a secure container.
    
    This agent extends LiteAgent to safely run code in isolated containers
    using Docker or Podman.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant specialized in solving problems by writing code.
When faced with a task, think step by step about how to solve it using code.
Write clean, well-documented code to solve the problem.

IMPORTANT NOTES:
1. Your code will run in an isolated container environment and NEVER on the host machine
2. You only have access to a limited set of Python standard libraries
3. Your code should be self-contained and complete
4. Always include detailed comments to explain your approach
5. If your code needs to manipulate files, they should be within the container workspace
6. Clearly print or return your final results

When the user asks a question, respond with Python code that solves their problem."""

    def __init__(self, model, name="CodeAgent", system_prompt=None, tools=None, debug=False, 
                 drop_params=True, parent_context_id=None, context_id=None, observers=None,
                 description=None, container_type="podman", container_config=None):
        """
        Initialize the LiteCodeAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            tools (list, optional): List of tool functions to use
            debug (bool, optional): Whether to print debug information. Defaults to False.
            drop_params (bool, optional): Whether to drop unsupported parameters. Defaults to True.
            parent_context_id (str, optional): Parent context ID if this agent was created by another agent.
            context_id (str, optional): Context ID for this agent. If None, a new ID will be generated.
            observers (list, optional): List of observers to notify of agent events.
            description (str, optional): A clear description of what this agent does.
            container_type (str, optional): Type of container to use ("docker" or "podman"). Defaults to "podman".
            container_config (dict, optional): Configuration for the container executor.
        """
        # Initialize the base LiteAgent
        super().__init__(
            model=model,
            name=name,
            system_prompt=system_prompt or self.DEFAULT_SYSTEM_PROMPT,
            tools=tools,
            debug=debug,
            drop_params=drop_params,
            parent_context_id=parent_context_id,
            context_id=context_id,
            observers=observers,
            description=description
        )
        
        # Container configuration
        self.container_type = container_type
        self.container_config = container_config or {}
        self.temp_dir = None
        
        # Initialize the workspace directory if not provided
        if 'source_directory' not in self.container_config:
            self.temp_dir = tempfile.mkdtemp(prefix="codeagent_workspace_")
            self.container_config['source_directory'] = self.temp_dir
        
        # Register code execution tool
        from .tools import FunctionTool
        
        # Create a tool for executing code
        execute_code_tool = FunctionTool(
            self._execute_code,
            name="execute_code",
            description="Execute Python code in a secure container environment",
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        )
        
        # Register the tool
        self._register_tools([execute_code_tool])
        
    def _execute_code(self, code: str, _context_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute code in a secure container environment.
        
        Args:
            code (str): Python code to execute
            _context_id (str, optional): Context ID for tracking tool calls
            
        Returns:
            Dict with execution results
        """
        self._log(f"Executing code in {self.container_type} container")
        
        # Extract code block if wrapped in markdown code block
        extracted_code = self._extract_code_block(code)
        
        # Create a container executor
        container_executor = ContainerFactory.create_container(
            container_type=self.container_type,
            **self.container_config
        )
        
        try:
            # Execute the code
            with container_executor as executor:
                result, logs, success = executor.execute_code(extracted_code)
                
                # Format the response
                response = {
                    "result": result,
                    "logs": logs,
                    "success": success
                }
                
                return response
                
        except Exception as e:
            error_message = f"Error executing code: {str(e)}"
            self._log(error_message, level="error")
            return {
                "result": {"error": str(e)},
                "logs": error_message,
                "success": False
            }
            
    def _extract_code_block(self, text: str) -> str:
        """
        Extract code from markdown code blocks or return the original text.
        
        Args:
            text (str): Text that may contain code blocks
            
        Returns:
            str: Extracted code or original text
        """
        # Pattern to match code blocks with or without language specifier
        pattern = r'```(?:python)?\s*([\s\S]*?)\s*```'
        matches = re.findall(pattern, text)
        
        if matches:
            # Return the content of the first code block
            return matches[0].strip()
        
        # No code block found, return the original text
        return text.strip()
        
    def chat(self, message: str) -> str:
        """
        Chat with the agent and get a response that includes code execution if needed.
        
        Args:
            message: The user's message
            
        Returns:
            str: The agent's response
        """
        return super().chat(message)
        
    def cleanup(self):
        """Clean up temporary resources."""
        # Remove the temporary directory if we created one
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
            
    def __enter__(self):
        """Context manager entry point"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.cleanup()