"""
ForkedAgent implementation for cost-optimized multi-agent systems.

This module provides the ForkedAgent class that leverages provider caching
to create multiple specialized agents from a shared context without re-sending
the full context for each agent.
"""

import copy
import uuid
from typing import Any, Dict, List, Optional, Union, Set
from .agent import LiteAgent
from .memory import ConversationMemory
from .models import create_model_interface
from .utils import logger
from .observer import generate_context_id, AgentEvent


class ForkEvent(AgentEvent):
    """Event emitted when an agent is forked."""
    
    def __init__(self, parent_agent_id: str, child_agent_id: str, 
                 parent_context_id: str, child_context_id: str,
                 prefill_role: Optional[str] = None,
                 allowed_tools: Optional[Set[str]] = None,
                 **kwargs):
        """Initialize a fork event."""
        super().__init__(
            agent_id=parent_agent_id,
            agent_name=f"fork_{parent_agent_id}",
            context_id=parent_context_id,
            parent_context_id=None,
            event_data={
                "child_agent_id": child_agent_id,
                "child_context_id": child_context_id,
                "prefill_role": prefill_role,
                "allowed_tools": list(allowed_tools) if allowed_tools else None
            }
        )
        self.event_type = "fork"  # Override the default class name


class ForkedMemory(ConversationMemory):
    """Memory implementation with copy-on-write semantics for forked agents."""
    
    def __init__(self, parent_memory: ConversationMemory, 
                 prefill_messages: Optional[List[Dict[str, str]]] = None):
        """
        Initialize forked memory from parent memory.
        
        Args:
            parent_memory: The parent agent's memory to fork from
            prefill_messages: Optional prefill messages for role definition
        """
        # Create a deep copy of parent messages to avoid mutations
        self.messages = copy.deepcopy(parent_memory.messages)
        self.system_prompt = parent_memory.system_prompt
        self.function_calls = {}
        self.last_function_call = None
        
        # Mark the fork point for cache optimization
        self._fork_point = len(self.messages)
        self._parent_memory = parent_memory
        
        # Add prefill messages if provided
        if prefill_messages:
            for msg in prefill_messages:
                self.messages.append(msg)
                
    def get_messages_for_api(self, include_cached: bool = True) -> List[Dict]:
        """
        Get messages formatted for API calls with cache optimization.
        
        Args:
            include_cached: Whether to include messages before fork point
            
        Returns:
            List of messages formatted for API
        """
        if include_cached:
            return self.messages
        else:
            # Return only messages after fork point for incremental updates
            return self.messages[self._fork_point:]
            
    def get_cache_key(self) -> str:
        """Generate a cache key for the forked memory state."""
        # Use parent's cache key up to fork point
        import hashlib
        import json
        
        # Hash the messages up to fork point
        fork_content = json.dumps(self.messages[:self._fork_point], sort_keys=True)
        return hashlib.sha256(fork_content.encode()).hexdigest()


class ForkedAgent(LiteAgent):
    """
    Agent implementation with forking capability for cost-optimized multi-agent systems.
    
    This agent can create forked children that share its cached context while
    having specialized roles and tool subsets.
    """
    
    def __init__(self, *args, enable_caching: bool = True, **kwargs):
        """
        Initialize a ForkedAgent.
        
        Args:
            *args: Positional arguments for LiteAgent
            enable_caching: Whether to enable provider caching (default: True)
            **kwargs: Keyword arguments for LiteAgent
        """
        super().__init__(*args, **kwargs)
        self.enable_caching = enable_caching
        self._fork_count = 0
        self._child_agents = []
        self._is_fork = False
        self._allowed_tools = None
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "bytes_saved": 0
        }
        
    def fork(self, 
             name: Optional[str] = None,
             prefill_role: Optional[str] = None,
             prefill_messages: Optional[List[Dict[str, str]]] = None,
             allowed_tools: Optional[List[str]] = None,
             system_prompt_suffix: Optional[str] = None) -> 'ForkedAgent':
        """
        Create a forked child agent with specialized role and tools.
        
        Args:
            name: Name for the forked agent (default: parent_name_fork_N)
            prefill_role: Simple role description for auto-prefilling
            prefill_messages: Custom prefill messages for role definition
            allowed_tools: Subset of tools available to the fork
            system_prompt_suffix: Additional system prompt for the fork
            
        Returns:
            ForkedAgent: The forked child agent
            
        Example:
            parent = ForkedAgent(model="claude-3-5-sonnet", context=large_context)
            auditor = parent.fork(
                name="security_auditor",
                prefill_role="security expert focusing on vulnerabilities",
                allowed_tools=["scan_code", "check_dependencies"]
            )
        """
        self._fork_count += 1
        
        # Generate fork name if not provided
        if not name:
            name = f"{self.name}_fork_{self._fork_count}"
            
        # Generate prefill messages from role if needed
        if prefill_role and not prefill_messages:
            prefill_messages = self._generate_prefill_messages(prefill_role)
            
        # Create forked memory
        forked_memory = ForkedMemory(self.memory, prefill_messages)
        
        # Prepare system prompt for fork
        fork_system_prompt = self.system_prompt
        if system_prompt_suffix:
            fork_system_prompt = f"{self.system_prompt}\n\n{system_prompt_suffix}"
            
        # Filter tools if subset specified
        if allowed_tools:
            fork_tools = {name: tool for name, tool in self.tools.items() 
                         if name in allowed_tools}
        else:
            fork_tools = self.tools.copy()
            
        # Create the forked agent
        fork = ForkedAgent(
            model=self.model,
            name=name,
            system_prompt=fork_system_prompt,
            tools=list(fork_tools.values()),
            debug=self.debug,
            api_key=self.api_key,
            provider=self.model_interface.provider.__class__.__name__.replace('Provider', '').lower(),
            parent_context_id=self.context_id,
            context_id=generate_context_id(),
            observers=self.observers.copy(),
            enable_caching=self.enable_caching
        )
        
        # Set fork-specific attributes
        fork._is_fork = True
        fork._allowed_tools = set(allowed_tools) if allowed_tools else None
        fork.memory = forked_memory
        
        # Track child agent
        self._child_agents.append(fork)
        
        # Emit fork event
        if self.observers:
            fork_event = ForkEvent(
                parent_agent_id=self.agent_id,
                child_agent_id=fork.agent_id,
                parent_context_id=self.context_id,
                child_context_id=fork.context_id,
                prefill_role=prefill_role,
                allowed_tools=fork._allowed_tools
            )
            for observer in self.observers:
                observer.on_event(fork_event)
                
        self._log(f"Created fork '{name}' with context_id {fork.context_id}")
        
        return fork
        
    def _generate_prefill_messages(self, role: str) -> List[Dict[str, str]]:
        """
        Generate prefill messages for role definition.
        
        Args:
            role: Role description
            
        Returns:
            List of prefill messages
        """
        return [
            {
                "role": "user",
                "content": f"You are now a specialized agent with the following role: {role}. "
                          f"Please confirm your understanding and explain how you will approach tasks."
            },
            {
                "role": "assistant", 
                "content": f"I understand. As a {role}, I will focus on the specific aspects "
                          f"relevant to this specialization. I'll use my available tools and "
                          f"knowledge to provide focused, expert analysis in this domain. "
                          f"Let me know what you'd like me to analyze or help with."
            }
        ]
        
    def _create_message_with_cache(self, messages: List[Dict]) -> List[Dict]:
        """
        Prepare messages with cache control for API calls.
        
        Args:
            messages: Messages to send
            
        Returns:
            Messages with cache control added
        """
        if not self.enable_caching:
            return messages
            
        # Check if provider supports caching
        if not hasattr(self.model_interface, 'supports_caching') or \
           not self.model_interface.supports_caching():
            return messages
            
        # Add cache control to long messages
        cached_messages = []
        for msg in messages:
            if isinstance(msg.get('content'), str) and len(msg['content']) > 1000:
                # For Anthropic, add cache control
                cached_msg = msg.copy()
                if self.model_interface.provider.__class__.__name__ == 'AnthropicProvider':
                    cached_msg['content'] = [
                        {
                            "type": "text",
                            "text": msg['content'],
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                cached_messages.append(cached_msg)
            else:
                cached_messages.append(msg)
                
        return cached_messages
        
    def chat(self, message: str, images: Optional[List[str]] = None, enable_caching: bool = False) -> str:
        """
        Chat with the agent using cache optimization for forks.
        
        Args:
            message: The message to process
            images: Optional list of image paths/URLs
            enable_caching: Whether to enable caching (overrides instance setting)
            
        Returns:
            The agent's response
        """
        # If this is a fork, we can optimize the API call
        if self._is_fork and isinstance(self.memory, ForkedMemory):
            # The parent's context should already be cached
            self._cache_stats["hits"] += 1
            self._log(f"Fork using cached context (cache key: {self.memory.get_cache_key()[:8]}...)")
            
        # Use instance caching setting or override
        use_caching = enable_caching or self.enable_caching
        
        # Add cache control to the request if supported
        original_messages = self.memory.messages.copy()
        if use_caching:
            self.memory.messages = self._create_message_with_cache(self.memory.messages)
            
        try:
            response = super().chat(message, images=images, enable_caching=use_caching)
        finally:
            # Restore original messages
            self.memory.messages = original_messages
            
        return response
        
    def run(self, message: str) -> str:
        """
        Legacy run method for backward compatibility.
        
        Args:
            message: The message to process
            
        Returns:
            The agent's response
        """
        return self.chat(message)
        
    def get_fork_tree(self) -> Dict[str, Any]:
        """
        Get the fork tree structure starting from this agent.
        
        Returns:
            Dictionary representing the fork tree
        """
        tree = {
            "agent_id": self.agent_id,
            "name": self.name,
            "is_fork": self._is_fork,
            "fork_count": self._fork_count,
            "allowed_tools": list(self._allowed_tools) if self._allowed_tools else None,
            "cache_stats": self._cache_stats.copy(),
            "children": []
        }
        
        for child in self._child_agents:
            if isinstance(child, ForkedAgent):
                tree["children"].append(child.get_fork_tree())
            else:
                tree["children"].append({
                    "agent_id": child.agent_id,
                    "name": child.name
                })
                
        return tree
        
    def get_cache_savings(self) -> Dict[str, Any]:
        """
        Calculate the cost savings from using forked agents.
        
        Returns:
            Dictionary with savings metrics
        """
        # Estimate tokens in cached content
        if isinstance(self.memory, ForkedMemory):
            cached_messages = self.memory.messages[:self.memory._fork_point]
            # Rough estimate: 1 token ≈ 4 characters
            cached_chars = sum(len(msg.get('content', '')) for msg in cached_messages 
                             if isinstance(msg.get('content'), str))
            cached_tokens = cached_chars // 4
        else:
            cached_tokens = 0
            
        # Calculate savings for all forks
        total_forks = len(self._child_agents)
        tokens_saved = cached_tokens * total_forks
        
        # Estimate cost savings (using Anthropic Claude 3.5 Sonnet pricing as example)
        # Input: $3 per million tokens
        cost_per_token = 3.0 / 1_000_000
        cost_saved = tokens_saved * cost_per_token
        
        return {
            "cached_tokens": cached_tokens,
            "total_forks": total_forks,
            "tokens_saved": tokens_saved,
            "estimated_cost_saved": f"${cost_saved:.4f}",
            "cache_hit_rate": self._calculate_cache_hit_rate()
        }
        
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate the cache hit rate for this agent and its forks."""
        total_hits = self._cache_stats["hits"]
        total_misses = self._cache_stats["misses"]
        
        # Include child agents' stats
        for child in self._child_agents:
            if isinstance(child, ForkedAgent):
                total_hits += child._cache_stats["hits"]
                total_misses += child._cache_stats["misses"]
                
        total_requests = total_hits + total_misses
        if total_requests == 0:
            return 0.0
            
        return total_hits / total_requests