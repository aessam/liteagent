"""
Memory management for LiteAgent.

This module provides classes for managing conversation history and memory
for the agent.
"""

from typing import Dict, List, Optional, Any

class ConversationMemory:
    """Class to manage conversation history."""
    
    def __init__(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def add_user_message(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "assistant", "content": content})
    
    def add_function_result(self, name: str, content: str, args: Dict = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
        """
        message = {
            "role": "function",
            "name": name,
            "content": str(content)
        }
        
        if args:
            # Store args for better repetition detection
            message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        key = f"{name}:{str(args)}"
        self.function_calls[key] = self.function_calls.get(key, 0) + 1
    
    def add_system_message(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "system", "content": content})
    
    def get_messages(self) -> List[Dict]:
        """
        Get all messages in the conversation.
        
        Returns:
            List of message dictionaries
        """
        return self.messages
    
    def reset(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def update_system_prompt(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def is_function_call_loop(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        key = f"{function_name}:{str(normalized_args)}"
        
        # Check if we've called this function with similar args too many times
        call_count = self.function_calls.get(key, 0)
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def get_last_function_result(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            if message.get("role") == "function" and message.get("name") == function_name:
                return message.get("content")
        return None 