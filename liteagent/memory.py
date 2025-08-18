"""
Memory management for LiteAgent.

This module provides classes for managing conversation history and memory
for the agent.
"""

import json
from typing import Dict, List, Optional, Any, Union

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
    
    def add_user_message_with_images(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def _is_url(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(('http://', 'https://'))
    
    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "assistant", "content": content})
    
    def add_function_call(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def add_tool_call(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def add_function_result(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Only Ollama needs user role format for tool results, Anthropic needs proper tool_result
        if provider and provider.lower() == "ollama":
            # For Ollama, use user role to provide tool results as if user is providing information
            message = {
                "role": "user", 
                "content": f"Tool result from {name}({args}): {content}"
            }
        else:
            # Use modern 'tool' role instead of deprecated 'function' role
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def add_tool_result(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def add_system_message(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "system", "content": content})
    
    def get_messages(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def has_function_been_called(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("args") == args:
                return True
                
        return False
    
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
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
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
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    def clear(self) -> None:
        """Clear all conversation history except the system prompt."""
        # This is an alias for reset()
        self.reset() 