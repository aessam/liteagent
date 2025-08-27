"""
OpenAI Assistants API provider for stateful conversations.

This provider implements TRUE context sharing by using OpenAI's Assistants API
with persistent threads, eliminating the need to resend context repeatedly.
"""

import os
import time
from typing import Any, Dict, List, Optional, Union
import json

try:
    from openai import OpenAI
    from openai.types.beta import Assistant, Thread
    from openai.types.beta.threads import Message, Run
    from openai.types.beta.threads.runs import ToolCall
except ImportError:
    raise ImportError("OpenAI library not installed. Install with: pip install openai")

from .base import ProviderInterface, ProviderResponse, ToolCall as LiteToolCall
from ..utils import logger


class OpenAIAssistantsProvider(ProviderInterface):
    """
    OpenAI Assistants API provider with stateful thread management.
    
    Key advantages:
    - Threads persist context across requests
    - No need to resend full conversation history
    - Automatic context window management
    - Built-in tool calling support
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI Assistants provider.
        
        Args:
            model_name: OpenAI model name (e.g., 'gpt-4o', 'gpt-4o-mini')
            api_key: OpenAI API key
            **kwargs: Additional configuration
        """
        self.assistant_id: Optional[str] = kwargs.get('assistant_id')
        self.thread_id: Optional[str] = kwargs.get('thread_id')
        self.assistant: Optional[Assistant] = None
        self.thread: Optional[Thread] = None
        self.instructions = kwargs.get('instructions', '')
        self.tools = kwargs.get('tools', [])
        
        super().__init__(model_name, api_key, **kwargs)
        
    def _get_provider_name(self) -> str:
        """Return provider name."""
        return 'openai_assistants'
        
    def _setup_client(self) -> None:
        """Setup OpenAI client."""
        self.client = OpenAI(
            api_key=self.api_key or os.getenv('OPENAI_API_KEY'),
            timeout=self.config.get('timeout', 60),
            max_retries=self.config.get('max_retries', 3)
        )
        
    def create_assistant(self, instructions: str, tools: Optional[List[Dict[str, Any]]] = None, 
                        name: Optional[str] = None) -> str:
        """
        Create a new assistant.
        
        Args:
            instructions: System instructions for the assistant
            tools: List of tools to enable
            name: Optional name for the assistant
            
        Returns:
            str: Assistant ID
        """
        assistant_tools = []
        
        # Convert tools to OpenAI format
        if tools:
            for tool in tools:
                if tool.get('type') == 'function':
                    assistant_tools.append({
                        'type': 'function',
                        'function': tool.get('function', {})
                    })
                elif tool.get('type') in ['code_interpreter', 'file_search']:
                    assistant_tools.append({'type': tool['type']})
        
        try:
            self.assistant = self.client.beta.assistants.create(
                name=name or f"LiteAgent-{int(time.time())}",
                instructions=instructions,
                model=self.model_name,
                tools=assistant_tools
            )
            
            self.assistant_id = self.assistant.id
            self.instructions = instructions
            self.tools = tools or []
            
            logger.info(f"[{self.provider_name}] Created assistant: {self.assistant_id}")
            return self.assistant_id
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Failed to create assistant: {e}")
            raise
            
    def create_thread(self, initial_messages: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Create a new conversation thread.
        
        Args:
            initial_messages: Optional initial messages for the thread
            
        Returns:
            str: Thread ID
        """
        try:
            thread_messages = []
            if initial_messages:
                for msg in initial_messages:
                    if msg.get('role') != 'system':  # System messages go in assistant instructions
                        thread_messages.append({
                            'role': msg['role'],
                            'content': msg['content']
                        })
            
            if thread_messages:
                self.thread = self.client.beta.threads.create(messages=thread_messages)
            else:
                self.thread = self.client.beta.threads.create()
                
            self.thread_id = self.thread.id
            logger.info(f"[{self.provider_name}] Created thread: {self.thread_id}")
            return self.thread_id
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Failed to create thread: {e}")
            raise
            
    def fork_thread(self, base_thread_id: str, role_message: str) -> str:
        """
        Create a new thread that inherits context from base thread.
        
        This simulates forking by creating a new thread and copying messages
        from the base thread, then adding the role-specific message.
        
        Args:
            base_thread_id: Thread ID to fork from
            role_message: Role-specific message for the fork
            
        Returns:
            str: New thread ID
        """
        try:
            # Get messages from base thread
            base_messages = self.client.beta.threads.messages.list(
                thread_id=base_thread_id,
                order="asc"
            )
            
            # Convert to thread creation format
            thread_messages = []
            for msg in base_messages.data:
                # Skip assistant messages and system messages
                if msg.role == 'user':
                    content = ""
                    for content_block in msg.content:
                        if hasattr(content_block, 'text'):
                            content += content_block.text.value
                        elif hasattr(content_block, 'value'):
                            content += content_block.value
                            
                    thread_messages.append({
                        'role': 'user',
                        'content': content
                    })
            
            # Add role-specific message
            thread_messages.append({
                'role': 'user', 
                'content': role_message
            })
            
            # Create new thread with inherited context
            self.thread = self.client.beta.threads.create(messages=thread_messages)
            self.thread_id = self.thread.id
            
            logger.info(f"[{self.provider_name}] Forked thread {base_thread_id} -> {self.thread_id}")
            return self.thread_id
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Failed to fork thread: {e}")
            raise
    
    def add_message(self, content: str, role: str = 'user') -> str:
        """
        Add a message to the current thread.
        
        Args:
            content: Message content
            role: Message role ('user' or 'assistant')
            
        Returns:
            str: Message ID
        """
        if not self.thread_id:
            raise ValueError("No active thread. Create a thread first.")
            
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role=role,
                content=content
            )
            
            logger.debug(f"[{self.provider_name}] Added {role} message to thread {self.thread_id}")
            return message.id
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Failed to add message: {e}")
            raise
    
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate response using Assistants API.
        
        For stateful mode: Only adds new messages to existing thread.
        For stateless mode: Creates temporary assistant and thread.
        
        Args:
            messages: Messages (only new ones if using existing thread)
            tools: Tools to enable
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse: Standardized response
        """
        start_time = time.time()
        
        try:
            # If no assistant/thread, create them
            if not self.assistant_id:
                # Extract system message for instructions
                system_message = ""
                user_messages = []
                
                for msg in messages:
                    if msg.get('role') == 'system':
                        system_message = msg.get('content', '')
                    else:
                        user_messages.append(msg)
                
                self.create_assistant(
                    instructions=system_message or self.instructions,
                    tools=tools,
                    name=kwargs.get('assistant_name')
                )
                
            if not self.thread_id:
                # Create thread with initial messages (excluding system)
                initial_messages = [msg for msg in messages if msg.get('role') != 'system']
                self.create_thread(initial_messages)
            else:
                # Add only new messages to existing thread
                for msg in messages:
                    if msg.get('role') in ['user', 'assistant']:
                        self.add_message(msg['content'], msg['role'])
            
            # Create and run
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
                temperature=kwargs.get('temperature'),
                max_tokens=kwargs.get('max_tokens')
            )
            
            # Wait for completion
            response_content, tool_calls, usage = self._wait_for_run_completion(run.id)
            
            elapsed_time = time.time() - start_time
            logger.info(f"[{self.provider_name}] Response generated in {elapsed_time:.2f}s")
            
            return ProviderResponse(
                content=response_content,
                tool_calls=tool_calls,
                usage=usage,
                model=self.model_name,
                provider=self.provider_name,
                raw_response={'run_id': run.id, 'thread_id': self.thread_id},
                finish_reason='stop'
            )
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Error generating response: {e}")
            raise
    
    def _wait_for_run_completion(self, run_id: str) -> tuple[str, List[LiteToolCall], Dict[str, Any]]:
        """
        Wait for run to complete and extract response.
        
        Args:
            run_id: Run ID to monitor
            
        Returns:
            Tuple of (content, tool_calls, usage)
        """
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_id
            )
            
            if run.status == 'completed':
                break
            elif run.status in ['failed', 'cancelled', 'expired']:
                raise RuntimeError(f"Run {run.status}: {run.last_error}")
            elif run.status == 'requires_action':
                # Handle tool calls if needed
                self._handle_required_actions(run_id, run.required_action)
            else:
                time.sleep(1)  # Wait and check again
        
        # Get the response messages
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id,
            order="desc",
            limit=1
        )
        
        response_content = ""
        tool_calls = []
        
        if messages.data:
            latest_message = messages.data[0]
            for content_block in latest_message.content:
                if hasattr(content_block, 'text'):
                    response_content += content_block.text.value
                elif hasattr(content_block, 'value'):
                    response_content += content_block.value
        
        # Extract usage info from run
        usage = {
            'prompt_tokens': getattr(run.usage, 'prompt_tokens', 0) if run.usage else 0,
            'completion_tokens': getattr(run.usage, 'completion_tokens', 0) if run.usage else 0,
            'total_tokens': getattr(run.usage, 'total_tokens', 0) if run.usage else 0
        }
        
        return response_content, tool_calls, usage
    
    def _handle_required_actions(self, run_id: str, required_action) -> None:
        """Handle required actions (tool calls)."""
        # This would handle tool calls if needed
        # For now, we'll pass - implement based on your tool calling needs
        pass
    
    def get_thread_messages(self) -> List[Dict[str, Any]]:
        """Get all messages from current thread."""
        if not self.thread_id:
            return []
            
        try:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread_id,
                order="asc"
            )
            
            result = []
            for msg in messages.data:
                content = ""
                for content_block in msg.content:
                    if hasattr(content_block, 'text'):
                        content += content_block.text.value
                    elif hasattr(content_block, 'value'):
                        content += content_block.value
                
                result.append({
                    'role': msg.role,
                    'content': content,
                    'created_at': msg.created_at
                })
                
            return result
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Failed to get thread messages: {e}")
            return []
    
    def supports_stateful_sessions(self) -> bool:
        """Return True as this provider supports stateful sessions."""
        return True
    
    def supports_caching(self) -> bool:
        """Return True as threads provide implicit context caching."""
        return True
    
    def supports_tool_calling(self) -> bool:
        """Return True as Assistants API supports tools."""
        return True
    
    def cleanup(self) -> None:
        """Clean up resources (optional - threads persist)."""
        # Optionally delete assistant/thread if they were created temporarily
        if hasattr(self, '_temp_assistant') and self._temp_assistant:
            try:
                self.client.beta.assistants.delete(self.assistant_id)
                logger.info(f"[{self.provider_name}] Cleaned up temporary assistant")
            except Exception as e:
                logger.warning(f"[{self.provider_name}] Failed to cleanup assistant: {e}")
                
        if hasattr(self, '_temp_thread') and self._temp_thread:
            try:
                self.client.beta.threads.delete(self.thread_id)
                logger.info(f"[{self.provider_name}] Cleaned up temporary thread")
            except Exception as e:
                logger.warning(f"[{self.provider_name}] Failed to cleanup thread: {e}")