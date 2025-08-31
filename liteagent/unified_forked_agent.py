"""
Unified ForkedAgent implementation combining best features from v1 and v2.

This implementation provides:
- LiteAgent compatibility for backward compatibility (from v1)
- Provider-specific optimization and intelligent rate limiting (from v2)  
- Event system and observability features (from v1)
- Multi-agent coordinator integration (new)
- Comprehensive error handling and recovery
"""

import copy
import uuid
import time
import asyncio
from typing import Any, Dict, List, Optional, Union, Set
from dataclasses import dataclass
from enum import Enum

from .agent import LiteAgent
from .memory import ConversationMemory
from .models import create_model_interface
from .utils import logger
from .observer import generate_context_id, AgentEvent
from .rate_limiter import get_rate_limiter, RateLimitError

# Import new multi-agent components
from .agent_registry import AgentRegistry, AgentCapability, AgentStatus
from .blackboard import Blackboard

# Optional imports for stateful providers
try:
    from .providers.openai_assistants import OpenAIAssistantsProvider
except ImportError:
    OpenAIAssistantsProvider = None

try:
    from .providers.gemini_chat import GeminiChatProvider
except ImportError:
    GeminiChatProvider = None


class SessionType(Enum):
    """Types of session management for different providers."""
    STATELESS = "stateless"  # Traditional request/response
    STATEFUL = "stateful"    # Provider manages state (OpenAI Assistants, Gemini)
    CACHED = "cached"        # Client manages state with caching (Anthropic)


class ForkEvent(AgentEvent):
    """Event emitted when an agent is forked."""
    
    def __init__(self, parent_agent_id: str, child_agent_id: str, 
                 parent_context_id: str, child_context_id: str,
                 prefill_role: Optional[str] = None,
                 allowed_tools: Optional[Set[str]] = None,
                 session_type: Optional[str] = None,
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
                "allowed_tools": sorted([str(tool) for tool in allowed_tools]) if allowed_tools else None,
                "session_type": session_type
            }
        )
        self.event_type = "fork"


@dataclass
class ForkConfig:
    """Configuration for creating a fork."""
    name: str
    role: str
    tools: Optional[List[str]] = None
    tier: Optional[str] = None
    max_retries: int = 3
    system_prompt_suffix: Optional[str] = None
    capabilities: Optional[List[str]] = None


class UnifiedForkedMemory(ConversationMemory):
    """Enhanced memory implementation with copy-on-write semantics and multi-agent support."""
    
    def __init__(self, parent_memory: ConversationMemory, 
                 prefill_messages: Optional[List[Dict[str, str]]] = None,
                 session_type: SessionType = SessionType.CACHED):
        """
        Initialize forked memory from parent memory.
        
        Args:
            parent_memory: The parent agent's memory to fork from
            prefill_messages: Optional prefill messages for role definition
            session_type: Type of session management being used
        """
        # Create a deep copy of parent messages to avoid mutations
        self.messages = copy.deepcopy(parent_memory.messages)
        self.system_prompt = parent_memory.system_prompt
        self.function_calls = {}
        self.last_function_call = None
        self.session_type = session_type
        
        # Mark the fork point for cache optimization
        self._fork_point = len(self.messages)
        self._parent_memory = parent_memory
        
        # Add prefill messages if provided
        if prefill_messages:
            for msg in prefill_messages:
                self.messages.append(msg)
    
    def get_cache_key(self) -> str:
        """Generate a cache key for the forked memory state."""
        import hashlib
        import json
        
        # Hash the messages up to fork point
        fork_content = json.dumps(self.messages[:self._fork_point], sort_keys=True)
        return hashlib.sha256(fork_content.encode()).hexdigest()
    
    def get_fork_point_messages(self) -> List[Dict]:
        """Get messages up to the fork point for caching."""
        return self.messages[:self._fork_point]
    
    def get_post_fork_messages(self) -> List[Dict]:
        """Get messages after the fork point."""
        return self.messages[self._fork_point:]


class UnifiedForkedAgent(LiteAgent):
    """
    Unified ForkedAgent combining best features from v1 and v2.
    
    Features:
    - Full LiteAgent compatibility
    - Provider-specific optimization (stateful/cached/stateless)
    - Intelligent rate limiting with token bucket algorithm
    - Event system for observability
    - Multi-agent coordinator integration
    - Comprehensive error handling and recovery
    """
    
    def __init__(self, *args, 
                 enable_caching: bool = True,
                 enable_rate_limiting: bool = True,
                 tier: Optional[str] = None,
                 multi_agent_coordinator: Optional[Any] = None,
                 **kwargs):
        """
        Initialize a UnifiedForkedAgent.
        
        Args:
            *args: Positional arguments for LiteAgent
            enable_caching: Whether to enable provider caching
            enable_rate_limiting: Whether to enable intelligent rate limiting
            tier: Rate limiting tier (auto-detected if None)
            multi_agent_coordinator: Optional multi-agent coordinator for registration
            **kwargs: Keyword arguments for LiteAgent
        """
        super().__init__(*args, **kwargs)
        
        # Core configuration
        self.enable_caching = enable_caching
        self.enable_rate_limiting = enable_rate_limiting
        self.tier = tier
        self.multi_agent_coordinator = multi_agent_coordinator
        
        # Fork management
        self._fork_count = 0
        self._child_agents = []
        self._is_fork = False
        self._allowed_tools = None
        self.forks: Dict[str, 'UnifiedForkedAgent'] = {}
        self.parent_agent: Optional['UnifiedForkedAgent'] = None
        
        # Session management
        self.session_type = self._determine_session_type()
        self.session_id: Optional[str] = None
        self.thread_id: Optional[str] = None
        self.assistant_id: Optional[str] = None
        
        # Rate limiting
        self.rate_limiter = get_rate_limiter() if enable_rate_limiting else None
        if self.rate_limiter:
            self._validate_rate_limits()
        
        # Multi-agent integration
        self._agent_registry_id: Optional[str] = None
        self._blackboard_subscriptions: List[str] = []
        
        logger.info(f"[{self.name}] Initialized UnifiedForkedAgent with {self.session_type.value} session")
    
    def _determine_session_type(self) -> SessionType:
        """Determine the best session type for this provider/model."""
        provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
        
        if provider_name == 'openai':
            return SessionType.STATEFUL  # Use Assistants API where possible
        elif provider_name == 'google':
            return SessionType.STATEFUL  # Use Chat Sessions
        elif provider_name == 'anthropic':
            return SessionType.CACHED    # Use prompt caching
        else:
            return SessionType.STATELESS # Fallback
    
    def _validate_rate_limits(self):
        """Validate that rate limits are configured for this model."""
        if not self.rate_limiter:
            return
            
        try:
            provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
            limits = self.rate_limiter.get_rate_limit(
                provider=provider_name,
                model=self.model,
                tier=self.tier
            )
            logger.info(f"[{self.name}] Rate limits: {limits.rpm} RPM, {limits.tpm} TPM")
        except RateLimitError as e:
            logger.warning(f"[{self.name}] {e}")
    
    def register_with_coordinator(self, capabilities: List[Union[str, AgentCapability]]) -> str:
        """
        Register this agent with the multi-agent coordinator.
        
        Args:
            capabilities: List of capabilities this agent provides
            
        Returns:
            str: Agent registration ID
        """
        if not self.multi_agent_coordinator:
            raise ValueError("No multi-agent coordinator configured")
        
        # Convert string capabilities to AgentCapability objects if needed
        capability_objects = []
        for cap in capabilities:
            if isinstance(cap, str):
                capability_objects.append(AgentCapability(
                    name=cap,
                    description=f"Capability: {cap}",
                    metadata={"agent_type": "forked_agent"}
                ))
            else:
                capability_objects.append(cap)
        
        # Register with coordinator
        self._agent_registry_id = asyncio.run(
            self.multi_agent_coordinator.register_agent(
                agent=self,
                capabilities=capability_objects,
                name=self.name,
                metadata={
                    "session_type": self.session_type.value,
                    "is_fork": self._is_fork,
                    "parent_agent": self.parent_agent.name if self.parent_agent else None
                }
            )
        )
        
        logger.info(f"[{self.name}] Registered with coordinator: {self._agent_registry_id}")
        return self._agent_registry_id
    
    def subscribe_to_blackboard(self, pattern: str, 
                              callback: Optional[callable] = None,
                              categories: Optional[List[str]] = None) -> str:
        """
        Subscribe to blackboard updates.
        
        Args:
            pattern: Regex pattern to match knowledge keys
            callback: Optional callback function (uses default if None)
            categories: Optional categories to filter by
            
        Returns:
            str: Subscription ID
        """
        if not self.multi_agent_coordinator:
            raise ValueError("No multi-agent coordinator configured")
        
        # Use default callback if none provided
        if callback is None:
            callback = self._default_blackboard_callback
        
        subscription_id = asyncio.run(
            self.multi_agent_coordinator.subscribe_to_knowledge_updates(
                pattern=pattern,
                callback=callback,
                agent_id=self._agent_registry_id or self.agent_id,
                categories=categories
            )
        )
        
        self._blackboard_subscriptions.append(subscription_id)
        logger.info(f"[{self.name}] Subscribed to blackboard pattern: {pattern}")
        return subscription_id
    
    def _default_blackboard_callback(self, knowledge_item):
        """Default callback for blackboard updates."""
        logger.info(f"[{self.name}] Blackboard update: {knowledge_item.key} = {knowledge_item.data}")
    
    def prepare_for_forking(self) -> bool:
        """
        Prepare the agent for efficient forking.
        
        Returns:
            bool: True if preparation successful
        """
        if self._is_fork:
            logger.warning(f"[{self.name}] Cannot prepare fork for forking")
            return False
            
        if self.session_type == SessionType.STATEFUL:
            return self._prepare_stateful_session()
        elif self.session_type == SessionType.CACHED:
            return self._prepare_cached_session()
        else:
            # Stateless doesn't need special preparation
            return True
    
    def _prepare_stateful_session(self) -> bool:
        """Prepare stateful session (OpenAI Assistants, Gemini Chat)."""
        try:
            provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
            
            if (provider_name == 'openai' and 
                OpenAIAssistantsProvider is not None and 
                hasattr(self.model_interface, 'provider') and
                isinstance(self.model_interface.provider, OpenAIAssistantsProvider)):
                
                # Create assistant and initial thread
                self.assistant_id = self.model_interface.provider.create_assistant(
                    instructions=self.system_prompt,
                    name=f"{self.name}_assistant"
                )
                
                # Create initial thread with preparation message
                self.thread_id = self.model_interface.provider.create_thread([
                    {"role": "user", "content": "I will define specific roles for analysis tasks. Please acknowledge."}
                ])
                
                logger.info(f"[{self.name}] OpenAI Assistant prepared: {self.assistant_id}")
                return True
                
            elif (provider_name == 'google' and 
                  GeminiChatProvider is not None and 
                  hasattr(self.model_interface, 'provider') and
                  isinstance(self.model_interface.provider, GeminiChatProvider)):
                
                # Start chat session with preparation
                self.session_id = self.model_interface.provider.start_chat_session([
                    {"role": "user", "content": "I will assign you specific analysis roles. Please confirm readiness."}
                ])
                
                logger.info(f"[{self.name}] Gemini Chat session prepared: {self.session_id}")
                return True
                
        except Exception as e:
            logger.error(f"[{self.name}] Failed to prepare stateful session: {e}")
            return False
            
        return False
    
    def _prepare_cached_session(self) -> bool:
        """Prepare cached session (Anthropic with prompt caching)."""
        try:
            # Add preparation message to memory
            self.memory.add_user_message(
                "I will define your role and purpose in the next message. Please acknowledge that you are ready."
            )
            
            # Generate cached response
            response = self._generate_response_with_rate_limiting(
                messages=self.memory.get_messages(),
                enable_caching=True
            )
            
            self.memory.add_assistant_message(response)
            
            logger.info(f"[{self.name}] Cached session prepared")
            return True
            
        except Exception as e:
            logger.error(f"[{self.name}] Failed to prepare cached session: {e}")
            return False
    
    def fork(self, 
             config: Union[ForkConfig, Dict[str, Any]],
             prepare_for_caching: bool = True) -> 'UnifiedForkedAgent':
        """
        Create a forked child agent with specialized role and tools.
        
        Args:
            config: Fork configuration (ForkConfig object or dict)
            prepare_for_caching: Whether to prepare parent for caching first
            
        Returns:
            UnifiedForkedAgent: The forked child agent
        """
        # Convert dict to ForkConfig if needed
        if isinstance(config, dict):
            config = ForkConfig(**config)
        
        # Ensure parent is prepared for forking
        if prepare_for_caching and not self.prepare_for_forking():
            raise RuntimeError(f"Agent {self.name} could not be prepared for forking")
        
        self._fork_count += 1
        
        # Create fork based on session type
        if self.session_type == SessionType.STATEFUL:
            fork = self._create_stateful_fork(config)
        elif self.session_type == SessionType.CACHED:
            fork = self._create_cached_fork(config)
        else:
            fork = self._create_stateless_fork(config)
        
        # Set fork-specific attributes
        fork._is_fork = True
        fork._allowed_tools = set(str(tool) for tool in config.tools) if config.tools else None
        fork.parent_agent = self
        
        # Track child agent
        self._child_agents.append(fork)
        self.forks[config.name] = fork
        
        # Register with multi-agent coordinator if available
        if config.capabilities and self.multi_agent_coordinator:
            fork.multi_agent_coordinator = self.multi_agent_coordinator
            fork.register_with_coordinator(config.capabilities)
        
        # Emit fork event
        if self.observers:
            fork_event = ForkEvent(
                parent_agent_id=self.agent_id,
                child_agent_id=fork.agent_id,
                parent_context_id=self.context_id,
                child_context_id=fork.context_id,
                prefill_role=config.role,
                allowed_tools=fork._allowed_tools,
                session_type=self.session_type.value
            )
            for observer in self.observers:
                observer.on_event(fork_event)
        
        logger.info(f"[{self.name}] Created fork '{config.name}' with session type {self.session_type.value}")
        return fork
    
    def _create_stateful_fork(self, config: ForkConfig) -> 'UnifiedForkedAgent':
        """Create fork with stateful session."""
        fork = self._create_base_fork(config)
        
        provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
        
        if provider_name == 'openai' and self.thread_id:
            # Fork the thread
            role_message = f"You are now a specialized {config.role}. Focus your analysis on this domain."
            if hasattr(self.model_interface.provider, 'fork_thread'):
                fork.thread_id = self.model_interface.provider.fork_thread(self.thread_id, role_message)
                fork.assistant_id = self.assistant_id
            
        elif provider_name == 'google' and self.session_id:
            # Fork the chat session
            if hasattr(self.model_interface.provider, 'fork_chat_session'):
                base_history = self.model_interface.provider.get_chat_history()
                role_message = f"You are now a specialized {config.role}. Focus your analysis on this domain."
                fork.session_id = self.model_interface.provider.fork_chat_session(base_history, role_message)
        
        return fork
    
    def _create_cached_fork(self, config: ForkConfig) -> 'UnifiedForkedAgent':
        """Create fork with cached context."""
        fork = self._create_base_fork(config)
        
        # Create forked memory from the cached parent state
        prefill_messages = self._generate_role_definition_message(config.role)
        fork.memory = UnifiedForkedMemory(
            self.memory, 
            prefill_messages, 
            SessionType.CACHED
        )
        
        return fork
    
    def _create_stateless_fork(self, config: ForkConfig) -> 'UnifiedForkedAgent':
        """Create fork with stateless provider."""
        fork = self._create_base_fork(config)
        
        # Copy full conversation state and add role message
        fork.memory = UnifiedForkedMemory(self.memory, session_type=SessionType.STATELESS)
        fork.memory.add_user_message(
            f"You are now a specialized {config.role}. Focus your analysis and responses on this specific domain."
        )
        
        return fork
    
    def _create_base_fork(self, config: ForkConfig) -> 'UnifiedForkedAgent':
        """Create the base fork instance."""
        # Prepare system prompt for fork
        fork_system_prompt = self.system_prompt
        if config.system_prompt_suffix:
            fork_system_prompt = f"{self.system_prompt}\n\n{config.system_prompt_suffix}"
        
        # Filter tools if subset specified
        if config.tools:
            # Ensure tool names are strings
            tool_names = [str(name) for name in config.tools]
            fork_tool_instances = [self.tool_instances[name] for name in tool_names 
                                 if name in self.tool_instances]
        else:
            fork_tool_instances = list(self.tool_instances.values())
        
        # Create the forked agent
        fork = UnifiedForkedAgent(
            model=self.model,
            name=config.name,
            system_prompt=fork_system_prompt,
            tools=fork_tool_instances,
            debug=self.debug,
            api_key=self.api_key,
            provider=getattr(self.model_interface, 'provider_name', 'unknown'),
            parent_context_id=self.context_id,
            context_id=generate_context_id(),
            observers=self.observers.copy(),
            enable_caching=self.enable_caching,
            enable_rate_limiting=self.enable_rate_limiting,
            tier=config.tier or self.tier,
            multi_agent_coordinator=self.multi_agent_coordinator
        )
        
        return fork
    
    def _generate_role_definition_message(self, role: str) -> List[Dict[str, str]]:
        """Generate role definition message for the fork."""
        return [
            {
                "role": "user",
                "content": f"You are now a specialized {role}. Focus your analysis and responses on this specific domain. Use your available tools to provide expert insights in this area."
            }
        ]
    
    def _generate_response_with_rate_limiting(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Generate response with intelligent rate limiting."""
        # Estimate tokens for rate limiting
        estimated_tokens = sum(len(msg.get('content', '')) for msg in messages) // 4
        
        # Wait if needed
        if self.rate_limiter:
            provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
            wait_time = self.rate_limiter.wait_if_needed(
                provider=provider_name,
                model=self.model,
                tier=self.tier,
                estimated_tokens=estimated_tokens
            )
            
            if wait_time > 0:
                logger.info(f"[{self.name}] Waited {wait_time:.1f}s for rate limits")
        
        # Generate response using parent's method
        try:
            response = self._generate_response_with_tools(**kwargs)
            
            # Update rate limiter with actual usage if available
            if self.rate_limiter and hasattr(response, 'usage') and response.usage:
                actual_tokens = response.usage.get('total_tokens', estimated_tokens)
                provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
                self.rate_limiter.consume_tokens(
                    provider=provider_name,
                    model=self.model,
                    tier=self.tier,
                    actual_tokens=actual_tokens
                )
            
            return response
            
        except Exception as e:
            logger.error(f"[{self.name}] Error generating response: {e}")
            raise
    
    def batch_analyze(self, tasks: List[Dict[str, Any]], max_parallel: int = 3) -> Dict[str, Any]:
        """
        Run multiple analysis tasks with intelligent batching.
        
        Args:
            tasks: List of task configurations
            max_parallel: Maximum parallel executions
            
        Returns:
            Dict: Results keyed by task name
        """
        results = {}
        
        # Create forks for tasks
        forks = []
        for task in tasks:
            config = ForkConfig(
                name=task['name'],
                role=task['role'],
                tools=task.get('tools'),
                tier=task.get('tier', self.tier),
                capabilities=task.get('capabilities')
            )
            fork = self.fork(config)
            forks.append((fork, task))
        
        # Execute in batches
        for i in range(0, len(forks), max_parallel):
            batch = forks[i:i + max_parallel]
            batch_results = self._execute_batch(batch)
            results.update(batch_results)
            
            # Delay between batches if rate limiting enabled
            if self.rate_limiter and i + max_parallel < len(forks):
                delay = self._calculate_batch_delay()
                if delay > 0:
                    logger.info(f"[{self.name}] Batch delay: {delay:.1f}s")
                    time.sleep(delay)
        
        return results
    
    def _execute_batch(self, batch: List[tuple]) -> Dict[str, Any]:
        """Execute a batch of tasks."""
        results = {}
        
        for fork, task in batch:
            try:
                message = task.get('message', f"Please perform your {task['role']} analysis.")
                response = fork.chat(message)
                results[task['name']] = {
                    'success': True,
                    'response': response,
                    'fork_name': fork.name
                }
            except Exception as e:
                logger.error(f"[{fork.name}] Task failed: {e}")
                results[task['name']] = {
                    'success': False,
                    'error': str(e),
                    'fork_name': fork.name
                }
        
        return results
    
    def _calculate_batch_delay(self) -> float:
        """Calculate delay needed between batches."""
        if not self.rate_limiter:
            return 0
            
        try:
            provider_name = getattr(self.model_interface, 'provider_name', 'unknown')
            limits = self.rate_limiter.get_rate_limit(
                provider=provider_name,
                model=self.model,
                tier=self.tier
            )
            
            # Conservative delay based on RPM limits
            min_delay = 60.0 / limits.rpm
            return min_delay * 2  # 2x safety factor
            
        except Exception:
            return 5.0  # Default 5 second delay
    
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
            "session_type": self.session_type.value,
            "allowed_tools": list(self._allowed_tools) if self._allowed_tools else None,
            "multi_agent_registered": self._agent_registry_id is not None,
            "children": []
        }
        
        for child in self._child_agents:
            if isinstance(child, UnifiedForkedAgent):
                tree["children"].append(child.get_fork_tree())
            else:
                tree["children"].append({
                    "agent_id": child.agent_id,
                    "name": child.name
                })
                
        return tree
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive agent statistics."""
        stats = {
            'agent_id': self.agent_id,
            'name': self.name,
            'model': self.model,
            'session_type': self.session_type.value,
            'is_fork': self._is_fork,
            'num_forks': len(self.forks),
            'fork_names': list(self.forks.keys()),
            'multi_agent_registry_id': self._agent_registry_id,
            'blackboard_subscriptions': len(self._blackboard_subscriptions)
        }
        
        if self.session_type == SessionType.STATEFUL:
            stats.update({
                'session_id': self.session_id,
                'thread_id': self.thread_id,
                'assistant_id': self.assistant_id
            })
        
        if self.rate_limiter:
            stats['rate_limiter_stats'] = self.rate_limiter.get_usage_stats()
        
        return stats
    
    def cleanup(self):
        """Clean up resources and unregister from coordinator."""
        # Clean up forks
        for fork in self.forks.values():
            fork.cleanup()
        
        # Unsubscribe from blackboard
        if self.multi_agent_coordinator:
            for subscription_id in self._blackboard_subscriptions:
                asyncio.run(
                    self.multi_agent_coordinator.unsubscribe_from_knowledge_updates(subscription_id)
                )
        
        # Unregister from coordinator
        if self._agent_registry_id and self.multi_agent_coordinator:
            asyncio.run(
                self.multi_agent_coordinator.unregister_agent(self._agent_registry_id)
            )
        
        # Clean up provider resources
        if hasattr(self.model_interface, 'cleanup'):
            self.model_interface.cleanup()
        
        logger.info(f"[{self.name}] Cleaned up resources")


# Alias for backward compatibility
ForkedAgent = UnifiedForkedAgent