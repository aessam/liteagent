"""
ForkedAgent v2 with intelligent provider routing and rate limiting.

This version automatically selects the best API approach per provider:
- OpenAI: Uses Assistants API for true stateful sessions
- Google: Uses Gemini Chat Sessions for state management  
- Anthropic: Uses Messages API with prompt caching
- All providers: Intelligent rate limiting with token bucket algorithm
"""

import time
import asyncio
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import uuid

from .providers.base import ProviderInterface, ProviderResponse
from .providers.factory import create_provider

# Optional imports for stateful providers
try:
    from .providers.openai_assistants import OpenAIAssistantsProvider
except ImportError:
    OpenAIAssistantsProvider = None

try:
    from .providers.gemini_chat import GeminiChatProvider
except ImportError:
    GeminiChatProvider = None
from .rate_limiter import get_rate_limiter, RateLimitError
from .memory import ConversationMemory
from .utils import logger


class SessionType(Enum):
    """Types of session management."""
    STATELESS = "stateless"  # Traditional request/response
    STATEFUL = "stateful"    # Provider manages state
    CACHED = "cached"        # Client manages state with caching


@dataclass
class ForkConfig:
    """Configuration for creating a fork."""
    name: str
    role: str
    tools: Optional[List[str]] = None
    tier: Optional[str] = None
    max_retries: int = 3


class ForkedAgentV2:
    """
    Next-generation ForkedAgent with intelligent provider routing.
    
    Features:
    - Provider-specific optimization (stateful vs stateless)
    - Intelligent rate limiting with token bucket algorithm
    - True context sharing where supported
    - Graceful degradation and error handling
    - Cost-effective testing with mock providers
    """
    
    def __init__(
        self,
        model: str,
        provider: str,
        system_prompt: str,
        name: Optional[str] = None,
        tier: Optional[str] = None,
        enable_rate_limiting: bool = True,
        **kwargs
    ):
        """
        Initialize ForkedAgent v2.
        
        Args:
            model: Model name (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022')
            provider: Provider name ('openai', 'anthropic', 'google', etc.)
            system_prompt: System prompt/instructions
            name: Agent name for tracking
            tier: Rate limiting tier (auto-detected if None)
            enable_rate_limiting: Enable intelligent rate limiting
            **kwargs: Additional provider-specific options
        """
        self.agent_id = str(uuid.uuid4())
        self.name = name or f"agent_{self.agent_id[:8]}"
        self.model = model
        self.provider_name = provider
        self.system_prompt = system_prompt
        self.tier = tier
        self.enable_rate_limiting = enable_rate_limiting
        self.kwargs = kwargs
        
        # State management
        self.session_type = self._determine_session_type()
        self.provider: Optional[ProviderInterface] = None
        self.memory = ConversationMemory(system_prompt)
        self.forks: Dict[str, 'ForkedAgentV2'] = {}
        self.parent_agent: Optional['ForkedAgentV2'] = None
        self.is_fork = False
        
        # Session tracking for stateful providers
        self.session_id: Optional[str] = None
        self.thread_id: Optional[str] = None
        self.assistant_id: Optional[str] = None
        
        # Rate limiting
        self.rate_limiter = get_rate_limiter() if enable_rate_limiting else None
        self._validate_rate_limits()
        
        # Initialize provider
        self._setup_provider()
        
        logger.info(f"[{self.name}] Initialized with {self.session_type.value} session type")
    
    def _determine_session_type(self) -> SessionType:
        """Determine the best session type for this provider/model."""
        if self.provider_name == 'openai':
            return SessionType.STATEFUL  # Use Assistants API
        elif self.provider_name == 'google':
            return SessionType.STATEFUL  # Use Chat Sessions
        elif self.provider_name == 'anthropic':
            return SessionType.CACHED    # Use prompt caching
        else:
            return SessionType.STATELESS # Fallback
    
    def _validate_rate_limits(self):
        """Validate that rate limits are configured for this model."""
        if not self.rate_limiter:
            return
            
        try:
            limits = self.rate_limiter.get_rate_limit(
                provider=self.provider_name,
                model=self.model,
                tier=self.tier
            )
            logger.info(f"[{self.name}] Rate limits: {limits.rpm} RPM, {limits.tpm} TPM")
        except RateLimitError as e:
            logger.error(f"[{self.name}] {e}")
            raise
    
    def _setup_provider(self):
        """Setup the appropriate provider based on session type."""
        if self.session_type == SessionType.STATEFUL:
            if self.provider_name == 'openai' and OpenAIAssistantsProvider is not None:
                self.provider = OpenAIAssistantsProvider(
                    model_name=self.model,
                    **self.kwargs
                )
            elif self.provider_name == 'google' and GeminiChatProvider is not None:
                self.provider = GeminiChatProvider(
                    model_name=self.model,
                    system_instruction=self.system_prompt,
                    **self.kwargs
                )
            else:
                # Fallback to regular provider
                self.provider = create_provider(self.model, provider=self.provider_name, **self.kwargs)
        else:
            # Use regular provider for stateless/cached
            self.provider = create_provider(self.model, provider=self.provider_name, **self.kwargs)
    
    def prepare_for_forking(self) -> bool:
        """
        Prepare the agent for efficient forking.
        
        Returns:
            bool: True if preparation successful
        """
        if self.is_fork:
            logger.warning(f"[{self.name}] Cannot prepare fork for forking")
            return False
            
        if self.session_type == SessionType.STATEFUL:
            return self._prepare_stateful_session()
        elif self.session_type == SessionType.CACHED:
            return self._prepare_cached_session()
        else:
            # Stateless doesn't need preparation
            return True
    
    def _prepare_stateful_session(self) -> bool:
        """Prepare stateful session (OpenAI Assistants, Gemini Chat)."""
        try:
            if (self.provider_name == 'openai' and 
                OpenAIAssistantsProvider is not None and 
                isinstance(self.provider, OpenAIAssistantsProvider)):
                # Create assistant and initial thread
                self.assistant_id = self.provider.create_assistant(
                    instructions=self.system_prompt,
                    name=f"{self.name}_assistant"
                )
                
                # Create initial thread with preparation message
                self.thread_id = self.provider.create_thread([
                    {"role": "user", "content": "I will define specific roles for analysis tasks. Please acknowledge."}
                ])
                
                # Generate initial response to establish context
                response = self.provider.generate_response(
                    messages=[{"role": "user", "content": "Ready for role assignments."}]
                )
                
                logger.info(f"[{self.name}] OpenAI Assistant prepared: {self.assistant_id}")
                return True
                
            elif (self.provider_name == 'google' and 
                  GeminiChatProvider is not None and 
                  isinstance(self.provider, GeminiChatProvider)):
                # Start chat session with preparation
                self.session_id = self.provider.start_chat_session([
                    {"role": "user", "content": "I will assign you specific analysis roles. Please confirm readiness."}
                ])
                
                # Send initial message to establish context
                response = self.provider.send_message("Ready for role assignments.")
                
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
            
            self.memory.add_assistant_message(response.content)
            
            logger.info(f"[{self.name}] Cached session prepared")
            return True
            
        except Exception as e:
            logger.error(f"[{self.name}] Failed to prepare cached session: {e}")
            return False
    
    def fork(self, config: ForkConfig) -> 'ForkedAgentV2':
        """
        Create a specialized fork of this agent.
        
        Args:
            config: Fork configuration
            
        Returns:
            ForkedAgentV2: New fork instance
        """
        if not self.prepare_for_forking():
            raise RuntimeError(f"Agent {self.name} not prepared for forking")
        
        # Create fork instance
        fork = ForkedAgentV2(
            model=self.model,
            provider=self.provider_name,
            system_prompt=self.system_prompt,
            name=config.name,
            tier=config.tier or self.tier,
            enable_rate_limiting=self.enable_rate_limiting,
            **self.kwargs
        )
        
        fork.is_fork = True
        fork.parent_agent = self
        
        # Setup fork based on session type
        if self.session_type == SessionType.STATEFUL:
            fork = self._create_stateful_fork(fork, config)
        elif self.session_type == SessionType.CACHED:
            fork = self._create_cached_fork(fork, config)
        else:
            fork = self._create_stateless_fork(fork, config)
        
        # Track fork
        self.forks[config.name] = fork
        
        logger.info(f"[{self.name}] Created fork: {config.name}")
        return fork
    
    def _create_stateful_fork(self, fork: 'ForkedAgentV2', config: ForkConfig) -> 'ForkedAgentV2':
        """Create fork with stateful session."""
        if self.provider_name == 'openai':
            # Fork the thread
            role_message = f"You are now a specialized {config.role}. Focus your analysis on this domain."
            fork.thread_id = self.provider.fork_thread(self.thread_id, role_message)
            fork.assistant_id = self.assistant_id
            fork.provider.assistant_id = self.assistant_id
            fork.provider.thread_id = fork.thread_id
            
        elif self.provider_name == 'google':
            # Fork the chat session
            base_history = self.provider.get_chat_history()
            role_message = f"You are now a specialized {config.role}. Focus your analysis on this domain."
            fork.session_id = self.provider.fork_chat_session(base_history, role_message)
            
        return fork
    
    def _create_cached_fork(self, fork: 'ForkedAgentV2', config: ForkConfig) -> 'ForkedAgentV2':
        """Create fork with cached context."""
        # Copy memory up to preparation point
        fork.memory = ConversationMemory(self.system_prompt)
        for msg in self.memory.get_messages():
            if msg['role'] == 'system':
                continue
            elif msg['role'] == 'user':
                fork.memory.add_user_message(msg['content'])
            elif msg['role'] == 'assistant':
                fork.memory.add_assistant_message(msg['content'])
        
        # Add role-specific message
        fork.memory.add_user_message(
            f"You are now a specialized {config.role}. Focus your analysis and responses on this specific domain."
        )
        
        return fork
    
    def _create_stateless_fork(self, fork: 'ForkedAgentV2', config: ForkConfig) -> 'ForkedAgentV2':
        """Create fork with stateless provider."""
        # Copy full conversation state
        fork.memory = ConversationMemory(self.system_prompt)
        for msg in self.memory.get_messages():
            if msg['role'] == 'system':
                continue
            elif msg['role'] == 'user':
                fork.memory.add_user_message(msg['content'])
            elif msg['role'] == 'assistant':
                fork.memory.add_assistant_message(msg['content'])
        
        # Add role message
        fork.memory.add_user_message(
            f"You are now a specialized {config.role}. Focus your analysis on this domain."
        )
        
        return fork
    
    def send_message(self, message: str, **kwargs) -> str:
        """
        Send a message and get response.
        
        Args:
            message: User message
            **kwargs: Additional generation parameters
            
        Returns:
            str: Assistant response
        """
        if self.session_type == SessionType.STATEFUL:
            return self._send_stateful_message(message, **kwargs)
        else:
            return self._send_stateless_message(message, **kwargs)
    
    def _send_stateful_message(self, message: str, **kwargs) -> str:
        """Send message using stateful provider."""
        if self.provider_name == 'openai':
            self.provider.add_message(message, 'user')
            response = self.provider.generate_response([], **kwargs)
        elif self.provider_name == 'google':
            response = self.provider.send_message(message)
        else:
            raise ValueError(f"Stateful not supported for {self.provider_name}")
        
        return response.content
    
    def _send_stateless_message(self, message: str, **kwargs) -> str:
        """Send message using stateless provider."""
        self.memory.add_user_message(message)
        
        response = self._generate_response_with_rate_limiting(
            messages=self.memory.get_messages(),
            **kwargs
        )
        
        self.memory.add_assistant_message(response.content)
        return response.content
    
    def _generate_response_with_rate_limiting(self, messages: List[Dict[str, Any]], **kwargs) -> ProviderResponse:
        """Generate response with intelligent rate limiting."""
        # Estimate tokens for rate limiting
        estimated_tokens = sum(len(msg.get('content', '')) for msg in messages) // 4
        
        # Wait if needed
        if self.rate_limiter:
            wait_time = self.rate_limiter.wait_if_needed(
                provider=self.provider_name,
                model=self.model,
                tier=self.tier,
                estimated_tokens=estimated_tokens
            )
            
            if wait_time > 0:
                logger.info(f"[{self.name}] Waited {wait_time:.1f}s for rate limits")
        
        # Generate response
        try:
            response = self.provider.generate_response(messages, **kwargs)
            
            # Update rate limiter with actual usage
            if self.rate_limiter and response.usage:
                actual_tokens = response.usage.get('total_tokens', estimated_tokens)
                self.rate_limiter.consume_tokens(
                    provider=self.provider_name,
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
                tier=task.get('tier', self.tier)
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
                response = fork.send_message(message)
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
            limits = self.rate_limiter.get_rate_limit(
                provider=self.provider_name,
                model=self.model,
                tier=self.tier
            )
            
            # Conservative delay based on RPM limits
            min_delay = 60.0 / limits.rpm
            return min_delay * 2  # 2x safety factor
            
        except Exception:
            return 5.0  # Default 5 second delay
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        stats = {
            'agent_id': self.agent_id,
            'name': self.name,
            'model': self.model,
            'provider': self.provider_name,
            'session_type': self.session_type.value,
            'is_fork': self.is_fork,
            'num_forks': len(self.forks),
            'fork_names': list(self.forks.keys()),
            'session_id': self.session_id,
            'thread_id': self.thread_id,
            'assistant_id': self.assistant_id
        }
        
        if self.rate_limiter:
            stats['rate_limiter_stats'] = self.rate_limiter.get_usage_stats()
        
        return stats
    
    def cleanup(self):
        """Clean up resources."""
        # Clean up forks
        for fork in self.forks.values():
            fork.cleanup()
        
        # Clean up provider
        if self.provider and hasattr(self.provider, 'cleanup'):
            self.provider.cleanup()
        
        logger.info(f"[{self.name}] Cleaned up resources")