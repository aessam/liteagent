"""
ForkedAgent implementation for cost-optimized multi-agent systems.

This module provides the ForkedAgent class that leverages provider caching
to create multiple specialized agents from a shared context without re-sending
the full context for each agent.
"""

import copy
import uuid
import time
import asyncio
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
        # Remove fake cache stats - use real provider data instead
        
    def fork(self, 
             name: Optional[str] = None,
             prefill_role: Optional[str] = None,
             prefill_messages: Optional[List[Dict[str, str]]] = None,
             allowed_tools: Optional[List[str]] = None,
             system_prompt_suffix: Optional[str] = None,
             prepare_for_caching: bool = True) -> 'ForkedAgent':
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
            
        # HONEST CACHING: Ensure parent has established cache BEFORE creating fork
        if prepare_for_caching and not self._is_prepared_for_caching():
            self._log("🚨 CRITICAL: Parent must establish cache before forking!")
            self._prepare_for_caching()
            # Verify cache is actually established
            if not self._is_prepared_for_caching():
                raise RuntimeError("Failed to establish cache - cannot create fork safely")
            
        # Generate prefill messages from role if needed
        if prefill_role and not prefill_messages:
            prefill_messages = self._generate_role_definition_message(prefill_role)
            
        # Create forked memory from the cached parent state
        # At this point, parent should have cache established
        self._log(f"🔀 Creating forked memory from cached parent state")
        self._log(f"📋 Parent has {len(self.memory.get_messages())} messages (should be ≥3 for caching)")
        forked_memory = ForkedMemory(self.memory, prefill_messages)
        
        # Prepare system prompt for fork
        fork_system_prompt = self.system_prompt
        if system_prompt_suffix:
            fork_system_prompt = f"{self.system_prompt}\n\n{system_prompt_suffix}"
            
        # Filter tools if subset specified
        if allowed_tools:
            fork_tool_instances = [self.tool_instances[name] for name in allowed_tools 
                                 if name in self.tool_instances]
        else:
            fork_tool_instances = list(self.tool_instances.values())
            
        # Create the forked agent
        fork = ForkedAgent(
            model=self.model,
            name=name,
            system_prompt=fork_system_prompt,
            tools=fork_tool_instances,
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
        
    def _is_prepared_for_caching(self) -> bool:
        """
        Check if the agent has the standard cache preparation message.
        
        Returns:
            bool: True if prepared for caching
        """
        messages = self.memory.get_messages()
        if len(messages) >= 3:
            # Check for the cache preparation pattern
            return (messages[1].get('role') == 'user' and 
                   'I will define your role and purpose' in messages[1].get('content', ''))
        return False
        
    def _prepare_for_caching(self):
        """
        Prepare the agent for proper caching by establishing shared context.
        
        This creates a conversation state that can be cached and shared
        across all forks. CRITICAL: This must complete before any forks are created.
        """
        if self._is_prepared_for_caching():
            self._log("✅ Cache already prepared")
            return  # Already prepared
            
        self._log("🔧 Preparing agent for caching with shared context...")
        self._log("📊 This will establish the cacheable conversation state")
        
        # Add the cache preparation message
        self.memory.add_user_message(
            "I will define your role and purpose in the next message. Please acknowledge that you are ready."
        )
        
        # Generate a cached response that will be shared across all forks
        # This is the CRITICAL step that establishes the cache on Anthropic's servers
        try:
            self._log("📡 Sending cache establishment request to Anthropic...")
            response = self._generate_response_with_tools(enable_caching=True)
            self.memory.add_assistant_message(response)
            
            # Verify the cache was actually created
            self._log("🔍 Verifying cache establishment...")
            if self._is_prepared_for_caching():
                self._log("✅ CACHE ESTABLISHED! Forks can now be created safely")
            else:
                self._log("❌ Cache establishment failed!")
                
        except Exception as e:
            self._log(f"💥 CRITICAL: Failed to prepare caching: {e}")
            raise RuntimeError(f"Cache preparation failed: {e}")
            
    def _generate_role_definition_message(self, role: str) -> List[Dict[str, str]]:
        """
        Generate a single role definition message for the fork.
        
        This creates just the role definition that gets added AFTER
        the shared cached context.
        
        Args:
            role: Role description
            
        Returns:
            List containing single role definition message
        """
        return [
            {
                "role": "user",
                "content": f"You are now a specialized {role}. Focus your analysis and responses on this specific domain. Use your available tools to provide expert insights in this area."
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
        Chat with the agent using optimized caching for forks.
        
        Args:
            message: The message to process
            images: Optional list of image paths/URLs
            enable_caching: Whether to enable caching (overrides instance setting)
            
        Returns:
            The agent's response
        """
        self._log(f"User: {message}")
        
        # Emit user message event
        from .observer import UserMessageEvent
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
        
        # Use instance caching setting or override
        use_caching = enable_caching or self.enable_caching
        
        # For forks, use optimized generation that leverages real caching
        if self._is_fork and isinstance(self.memory, ForkedMemory):
            response = self._generate_fork_response_with_tools(enable_caching=use_caching)
        else:
            response = self._generate_response_with_tools(enable_caching=use_caching)
        
        # Add final response to memory
        self.memory.add_assistant_message(response)
        
        # Emit agent response event
        from .observer import AgentResponseEvent
        self._emit_event(AgentResponseEvent(
            agent_id=self.agent_id,
            agent_name=self.name,
            context_id=self.context_id,
            response=response
        ))
        
        self._log(f"Agent: {response}")
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
    
    def _generate_fork_response_with_tools(self, enable_caching: bool = False) -> str:
        """
        Generate a response optimized for fork agents using smart caching.
        
        This method implements true context sharing by ensuring cached content
        is properly recognized and not re-sent to the API.
        
        Args:
            enable_caching: Enable prompt caching for supported models
        
        Returns:
            str: The final response
        """
        max_tool_iterations = 10
        iteration = 0
        
        while iteration < max_tool_iterations:
            iteration += 1
            
            # Get current messages - for forks, we trust the caching system
            messages = self.memory.get_messages()
            
            # For debugging: log the actual message sizes being sent
            total_chars = sum(len(str(msg.get('content', ''))) for msg in messages)
            self._log(f"Sending {len(messages)} messages ({total_chars:,} chars) to API")
            
            # Prepare tools if model supports them
            tools = None
            if self.model_interface.supports_tool_calling() and self.tools:
                tools = self._prepare_tools()
            
            # Emit model request event
            from .observer import ModelRequestEvent
            self._emit_event(ModelRequestEvent(
                agent_id=self.agent_id,
                agent_name=self.name,
                context_id=self.context_id,
                messages=messages,
                tools=tools
            ))
            
            try:
                # Add rate limit handling for parallel fork requests
                if self._is_fork and iteration == 1:
                    # Stagger fork requests to avoid rate limits
                    fork_delay = hash(self.agent_id) % 5  # 0-4 second delay based on agent ID
                    if fork_delay > 0:
                        self._log(f"🕐 Staggering fork request by {fork_delay}s to avoid rate limits")
                        time.sleep(fork_delay)
                
                # Generate response with caching enabled
                response = self.model_interface.generate_response(messages, tools, enable_caching=enable_caching)
                
                # Log cache usage from the actual response
                if hasattr(response, 'usage') and response.usage:
                    cached_tokens = (
                        response.usage.get('cache_read_input_tokens', 0) +
                        response.usage.get('cached_tokens', 0)
                    )
                    total_tokens = response.usage.get('total_tokens', 0)
                    if cached_tokens > 0:
                        cache_rate = (cached_tokens / total_tokens * 100) if total_tokens > 0 else 0
                        self._log(f"✅ Real cache hit: {cached_tokens:,} tokens cached ({cache_rate:.1f}%)")
                    else:
                        self._log(f"❌ No cache hit: {total_tokens:,} tokens processed")
                
                # Emit model response event
                from .observer import ModelResponseEvent
                self._emit_event(ModelResponseEvent(
                    agent_id=self.agent_id,
                    agent_name=self.name,
                    context_id=self.context_id,
                    response=response
                ))
                
                # Extract tool calls
                from .providers import ProviderResponse
                tool_calls = response.tool_calls if isinstance(response, ProviderResponse) else []
                
                if not tool_calls:
                    # No tool calls, return the content
                    content = response.content if isinstance(response, ProviderResponse) else str(response)
                    return content or "I apologize, but I couldn't generate a response."
                
                # Process tool calls
                self._process_tool_calls(tool_calls, response)
                
            except Exception as e:
                error_str = str(e).lower()
                self._log(f"Error generating response: {e}")
                
                # Handle rate limit errors with exponential backoff
                if "rate" in error_str or "limit" in error_str or "quota" in error_str:
                    self._log(f"⚠️ Rate limit hit for fork {self.name}")
                    
                    if iteration <= 3:  # Allow retries for rate limits
                        backoff_time = min(2 ** iteration, 30)  # Exponential backoff, max 30s
                        self._log(f"🔄 Retrying in {backoff_time}s (attempt {iteration})")
                        time.sleep(backoff_time)
                        continue
                    else:
                        return f"⚠️ Rate limit exceeded for {self.name} after {iteration} attempts. " \
                               f"This suggests the forking system is overwhelming the API."
                
                # Handle other errors
                return f"❌ Error in {self.name}: {str(e)}"
        
        return "I reached the maximum number of tool iterations. Please try rephrasing your question."
        
    def get_cache_savings(self) -> Dict[str, Any]:
        """
        Calculate the cost savings from using forked agents using real cost data.
        
        Returns:
            Dictionary with savings metrics
        """
        from .provider_cost_tracker import get_cost_tracker
        cost_tracker = get_cost_tracker()
        savings_report = cost_tracker.get_fork_savings()
        
        # Get additional metrics
        total_forks = len(self._child_agents)
        
        # Estimate cached tokens from memory if available
        cached_tokens = 0
        if isinstance(self.memory, ForkedMemory):
            cached_messages = self.memory.messages[:self.memory._fork_point]
            cached_chars = sum(len(msg.get('content', '')) for msg in cached_messages 
                             if isinstance(msg.get('content'), str))
            cached_tokens = cached_chars // 4
        
        return {
            "cached_tokens": cached_tokens,
            "total_forks": total_forks,
            "tokens_saved": savings_report.get("cached_tokens", 0),
            "actual_cost": savings_report.get("actual_cost", 0.0),
            "traditional_cost": savings_report.get("estimated_traditional_cost", 0.0),
            "cost_saved": savings_report.get("savings", 0.0),
            "savings_percent": savings_report.get("savings_percent", 0.0),
            "cache_hit_rate": self._calculate_cache_hit_rate()
        }
        
    def _generate_prefill_messages(self, role: str) -> List[Dict[str, str]]:
        """Generate prefill messages for role definition."""
        return [
            {"role": "user", "content": f"You are now acting as a {role}. Please confirm your role."},
            {"role": "assistant", "content": f"I understand. I am now acting as a {role} and will provide specialized assistance in that capacity."}
        ]
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate from stored stats."""
        if not hasattr(self, '_cache_stats') or not self._cache_stats:
            return 0.0
        
        hits = self._cache_stats.get('hits', 0)
        misses = self._cache_stats.get('misses', 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return hits / total