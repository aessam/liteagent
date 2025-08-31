"""
Comprehensive unit tests for the UnifiedForkedAgent.

This consolidates tests from scattered files and provides comprehensive coverage
for the new unified ForkedAgent implementation.
"""

import pytest
import time
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

from liteagent.unified_forked_agent import (
    UnifiedForkedAgent, ForkConfig, SessionType, ForkEvent, UnifiedForkedMemory
)
from liteagent.agent_registry import AgentCapability
from liteagent.blackboard import Blackboard
from liteagent.multi_agent_coordinator import MultiAgentCoordinator


class TestSessionType:
    """Test SessionType enum."""
    
    def test_session_types(self):
        """Test all session types are defined."""
        assert SessionType.STATELESS.value == "stateless"
        assert SessionType.STATEFUL.value == "stateful"
        assert SessionType.CACHED.value == "cached"


class TestForkConfig:
    """Test ForkConfig dataclass."""
    
    def test_fork_config_creation(self):
        """Test creating a ForkConfig."""
        config = ForkConfig(
            name="test_fork",
            role="security_expert",
            tools=["scan_code", "check_vulnerabilities"],
            tier="premium",
            max_retries=5,
            capabilities=["security_analysis", "vulnerability_detection"]
        )
        
        assert config.name == "test_fork"
        assert config.role == "security_expert"
        assert config.tools == ["scan_code", "check_vulnerabilities"]
        assert config.tier == "premium"
        assert config.max_retries == 5
        assert config.capabilities == ["security_analysis", "vulnerability_detection"]
    
    def test_fork_config_defaults(self):
        """Test ForkConfig with default values."""
        config = ForkConfig(name="simple_fork", role="analyst")
        
        assert config.name == "simple_fork"
        assert config.role == "analyst"
        assert config.tools is None
        assert config.tier is None
        assert config.max_retries == 3
        assert config.capabilities is None


class TestUnifiedForkedMemory:
    """Test UnifiedForkedMemory functionality."""
    
    @pytest.fixture
    def parent_memory(self):
        """Create a parent memory with some messages."""
        from liteagent.memory import ConversationMemory
        memory = ConversationMemory("You are a helpful assistant.")
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi there!")
        memory.add_user_message("How are you?")
        return memory
    
    def test_forked_memory_creation(self, parent_memory):
        """Test creating forked memory."""
        prefill_messages = [{"role": "user", "content": "You are now a security expert."}]
        forked_memory = UnifiedForkedMemory(
            parent_memory, 
            prefill_messages, 
            SessionType.CACHED
        )
        
        assert forked_memory.session_type == SessionType.CACHED
        assert forked_memory._fork_point == 4  # 1 system + 2 user + 1 assistant
        assert len(forked_memory.messages) == 5  # Original 4 + 1 prefill
        assert forked_memory.messages[-1]["content"] == "You are now a security expert."
    
    def test_fork_point_messages(self, parent_memory):
        """Test getting messages at different points."""
        forked_memory = UnifiedForkedMemory(parent_memory, session_type=SessionType.CACHED)
        
        fork_point_messages = forked_memory.get_fork_point_messages()
        post_fork_messages = forked_memory.get_post_fork_messages()
        
        assert len(fork_point_messages) == 4
        assert len(post_fork_messages) == 0
        
        # Add post-fork message
        forked_memory.add_user_message("New message after fork")
        post_fork_messages = forked_memory.get_post_fork_messages()
        assert len(post_fork_messages) == 1
    
    def test_cache_key_generation(self, parent_memory):
        """Test cache key generation."""
        forked_memory = UnifiedForkedMemory(parent_memory, session_type=SessionType.CACHED)
        cache_key = forked_memory.get_cache_key()
        
        assert isinstance(cache_key, str)
        assert len(cache_key) == 64  # SHA256 hex digest length
        
        # Same content should produce same key
        forked_memory2 = UnifiedForkedMemory(parent_memory, session_type=SessionType.CACHED)
        cache_key2 = forked_memory2.get_cache_key()
        assert cache_key == cache_key2


class TestUnifiedForkedAgent:
    """Test UnifiedForkedAgent functionality."""
    
    @pytest.fixture
    def mock_model_interface(self):
        """Create a mock model interface."""
        mock_interface = MagicMock()
        mock_interface.provider_name = "anthropic"
        mock_interface.supports_tool_calling.return_value = True
        mock_interface.generate_response.return_value = "Test response"
        return mock_interface
    
    @pytest.fixture
    def base_agent(self, mock_model_interface):
        """Create a base agent for testing."""
        with patch('liteagent.unified_forked_agent.create_model_interface') as mock_create:
            mock_create.return_value = mock_model_interface
            agent = UnifiedForkedAgent(
                model="claude-3-5-sonnet-20241022",
                name="TestAgent",
                system_prompt="You are a test agent.",
                enable_rate_limiting=False  # Disable for testing
            )
            agent.model_interface = mock_model_interface
            return agent
    
    def test_session_type_determination(self, base_agent):
        """Test session type determination based on provider."""
        # Test Anthropic -> CACHED
        base_agent.model_interface.provider_name = "anthropic"
        assert base_agent._determine_session_type() == SessionType.CACHED
        
        # Test OpenAI -> STATEFUL
        base_agent.model_interface.provider_name = "openai"
        assert base_agent._determine_session_type() == SessionType.STATEFUL
        
        # Test Google -> STATEFUL
        base_agent.model_interface.provider_name = "google"
        assert base_agent._determine_session_type() == SessionType.STATEFUL
        
        # Test unknown -> STATELESS
        base_agent.model_interface.provider_name = "unknown"
        assert base_agent._determine_session_type() == SessionType.STATELESS
    
    def test_agent_initialization(self, base_agent):
        """Test agent initialization."""
        assert base_agent.name == "TestAgent"
        assert base_agent.enable_caching is True
        assert base_agent.enable_rate_limiting is False
        assert base_agent._fork_count == 0
        assert base_agent._is_fork is False
        assert len(base_agent._child_agents) == 0
        # Session type is STATELESS for unknown providers
        assert base_agent.session_type == SessionType.STATELESS
    
    def test_prepare_for_forking_cached(self, base_agent):
        """Test preparing for forking with cached session."""
        # Set session type to CACHED to test the cached preparation
        base_agent.session_type = SessionType.CACHED
        
        # Mock the response generation
        base_agent._generate_response_with_tools = MagicMock(return_value="Ready for forking.")
        
        # Should succeed for cached session
        result = base_agent.prepare_for_forking()
        assert result is True
        
        # Should have added preparation message for CACHED session
        messages = base_agent.memory.get_messages()
        assert len(messages) >= 3  # system + user + assistant
        assert "define your role and purpose" in messages[1]["content"]
    
    def test_prepare_for_forking_fork_fails(self, base_agent):
        """Test that forks cannot be prepared for forking."""
        base_agent._is_fork = True
        result = base_agent.prepare_for_forking()
        assert result is False
    
    def test_fork_creation_basic(self, base_agent):
        """Test basic fork creation."""
        # Mock preparation
        base_agent.prepare_for_forking = MagicMock(return_value=True)
        
        config = ForkConfig(name="security_fork", role="security_expert")
        fork = base_agent.fork(config)
        
        assert fork.name == "security_fork"
        assert fork._is_fork is True
        assert fork.parent_agent == base_agent
        assert base_agent._fork_count == 1
        assert len(base_agent._child_agents) == 1
        assert "security_fork" in base_agent.forks
    
    def test_fork_creation_with_tools(self, base_agent):
        """Test fork creation with tool filtering."""
        # Add some tools to base agent with __name__ attribute
        tool1 = MagicMock()
        tool1.__name__ = "tool1"
        tool2 = MagicMock()
        tool2.__name__ = "tool2"
        tool3 = MagicMock()
        tool3.__name__ = "tool3"
        
        base_agent.tool_instances = {
            "tool1": tool1,
            "tool2": tool2,
            "tool3": tool3
        }
        
        base_agent.prepare_for_forking = MagicMock(return_value=True)
        
        config = ForkConfig(
            name="filtered_fork", 
            role="specialist",
            tools=["tool1", "tool3"]
        )
        fork = base_agent.fork(config)
        
        assert fork._allowed_tools == {"tool1", "tool3"}
        # Should only have specified tools
        assert len(fork.tool_instances) == 2
    
    def test_fork_creation_with_dict_config(self, base_agent):
        """Test fork creation using dict configuration."""
        base_agent.prepare_for_forking = MagicMock(return_value=True)
        
        config_dict = {
            "name": "dict_fork",
            "role": "analyst",
            "tools": ["tool1"],
            "tier": "premium"
        }
        
        fork = base_agent.fork(config_dict)
        assert fork.name == "dict_fork"
        assert fork.tier == "premium"
    
    def test_fork_creation_preparation_fails(self, base_agent):
        """Test fork creation when preparation fails."""
        base_agent.prepare_for_forking = MagicMock(return_value=False)
        
        config = ForkConfig(name="failing_fork", role="expert")
        
        with pytest.raises(RuntimeError, match="could not be prepared for forking"):
            base_agent.fork(config)
    
    def test_multi_agent_coordinator_integration(self, base_agent):
        """Test integration with multi-agent coordinator."""
        # Mock coordinator
        mock_coordinator = MagicMock()
        mock_coordinator.register_agent = AsyncMock(return_value="agent_123")
        base_agent.multi_agent_coordinator = mock_coordinator
        
        capabilities = ["security_analysis", "code_review"]
        agent_id = base_agent.register_with_coordinator(capabilities)
        
        assert agent_id == "agent_123"
        assert base_agent._agent_registry_id == "agent_123"
    
    def test_blackboard_subscription(self, base_agent):
        """Test blackboard subscription functionality."""
        mock_coordinator = MagicMock()
        mock_coordinator.subscribe_to_knowledge_updates = AsyncMock(return_value="sub_123")
        base_agent.multi_agent_coordinator = mock_coordinator
        base_agent._agent_registry_id = "agent_123"
        
        subscription_id = base_agent.subscribe_to_blackboard("test_.*")
        
        assert subscription_id == "sub_123"
        assert "sub_123" in base_agent._blackboard_subscriptions
    
    def test_batch_analyze(self, base_agent):
        """Test batch analysis functionality."""
        base_agent.prepare_for_forking = MagicMock(return_value=True)
        
        # Mock fork behavior
        mock_fork = MagicMock()
        mock_fork.chat = MagicMock(return_value="Analysis result")
        mock_fork.name = "test_fork"
        
        base_agent.fork = MagicMock(return_value=mock_fork)
        
        tasks = [
            {
                "name": "task1",
                "role": "security_expert",
                "message": "Analyze security"
            },
            {
                "name": "task2", 
                "role": "performance_expert",
                "message": "Analyze performance"
            }
        ]
        
        results = base_agent.batch_analyze(tasks, max_parallel=2)
        
        assert len(results) == 2
        assert results["task1"]["success"] is True
        assert results["task1"]["response"] == "Analysis result"
        assert results["task2"]["success"] is True
    
    def test_fork_tree_generation(self, base_agent):
        """Test fork tree structure generation."""
        base_agent.prepare_for_forking = MagicMock(return_value=True)
        
        # Create some forks
        config1 = ForkConfig(name="fork1", role="expert1")
        config2 = ForkConfig(name="fork2", role="expert2")
        
        fork1 = base_agent.fork(config1)
        fork2 = base_agent.fork(config2)
        
        tree = base_agent.get_fork_tree()
        
        assert tree["name"] == "TestAgent"
        assert tree["is_fork"] is False
        assert tree["fork_count"] == 2
        assert tree["session_type"] == "stateless"  # Default for unknown provider
        assert len(tree["children"]) == 2
    
    def test_stats_generation(self, base_agent):
        """Test statistics generation."""
        base_agent._agent_registry_id = "agent_123"
        base_agent._blackboard_subscriptions = ["sub1", "sub2"]
        
        stats = base_agent.get_stats()
        
        assert stats["name"] == "TestAgent"
        assert stats["session_type"] == "stateless"  # Default for unknown provider
        assert stats["is_fork"] is False
        assert stats["num_forks"] == 0
        assert stats["multi_agent_registry_id"] == "agent_123"
        assert stats["blackboard_subscriptions"] == 2
    
    def test_cleanup(self, base_agent):
        """Test resource cleanup."""
        # Setup some resources to clean
        base_agent._agent_registry_id = "agent_123"
        base_agent._blackboard_subscriptions = ["sub1", "sub2"]
        
        mock_coordinator = MagicMock()
        mock_coordinator.unsubscribe_from_knowledge_updates = AsyncMock()
        mock_coordinator.unregister_agent = AsyncMock()
        base_agent.multi_agent_coordinator = mock_coordinator
        
        # Add a mock fork
        mock_fork = MagicMock()
        base_agent.forks["test_fork"] = mock_fork
        
        base_agent.cleanup()
        
        # Should have cleaned up fork
        mock_fork.cleanup.assert_called_once()


class TestForkEvent:
    """Test ForkEvent functionality."""
    
    def test_fork_event_creation(self):
        """Test creating a fork event."""
        event = ForkEvent(
            parent_agent_id="parent_123",
            child_agent_id="child_456",
            parent_context_id="context_parent",
            child_context_id="context_child",
            prefill_role="security_expert",
            allowed_tools={"tool1", "tool2"},
            session_type="cached"
        )
        
        assert event.event_type == "fork"
        assert event.agent_id == "parent_123"
        assert event.context_id == "context_parent"
        assert event.event_data["child_agent_id"] == "child_456"
        assert event.event_data["child_context_id"] == "context_child"
        assert event.event_data["prefill_role"] == "security_expert"
        assert event.event_data["allowed_tools"] == ["tool1", "tool2"]
        assert event.event_data["session_type"] == "cached"


class TestRateLimitingIntegration:
    """Test rate limiting integration."""
    
    @pytest.fixture
    def agent_with_rate_limiting(self):
        """Create agent with rate limiting enabled."""
        with patch('liteagent.unified_forked_agent.get_rate_limiter') as mock_get_limiter:
            mock_limiter = MagicMock()
            mock_limiter.wait_if_needed.return_value = 0.5  # 500ms wait
            mock_limiter.consume_tokens.return_value = None
            mock_get_limiter.return_value = mock_limiter
            
            with patch('liteagent.unified_forked_agent.create_model_interface'):
                agent = UnifiedForkedAgent(
                    model="gpt-4",
                    name="RateLimitedAgent",
                    system_prompt="Test agent",
                    enable_rate_limiting=True
                )
                agent.rate_limiter = mock_limiter
                return agent, mock_limiter
    
    def test_rate_limiting_during_response_generation(self, agent_with_rate_limiting):
        """Test rate limiting during response generation."""
        agent, mock_limiter = agent_with_rate_limiting
        
        # Mock the parent method with usage information
        mock_response = MagicMock()
        mock_response.usage = {'total_tokens': 100}
        agent._generate_response_with_tools = MagicMock(return_value=mock_response)
        
        messages = [{"role": "user", "content": "Hello"}]
        
        with patch('time.sleep') as mock_sleep:
            response = agent._generate_response_with_rate_limiting(messages)
        
        # Should have waited for rate limits
        mock_limiter.wait_if_needed.assert_called_once()
        
        # Should have consumed tokens
        mock_limiter.consume_tokens.assert_called_once()
        
        assert response == mock_response  # Should return the mock response object, not string


class TestBackwardCompatibility:
    """Test backward compatibility features."""
    
    def test_forked_agent_alias(self):
        """Test that ForkedAgent is an alias for UnifiedForkedAgent."""
        from liteagent.unified_forked_agent import ForkedAgent, UnifiedForkedAgent
        assert ForkedAgent is UnifiedForkedAgent
    
    def test_legacy_import_warnings(self):
        """Test that legacy imports show deprecation warnings."""
        # The warnings are emitted during module import, so we need to reload
        import importlib
        import sys
        
        # Remove liteagent modules to force reimport
        modules_to_remove = [mod for mod in sys.modules.keys() if mod.startswith('liteagent')]
        for mod in modules_to_remove:
            if 'test' not in mod:  # Don't remove test modules
                del sys.modules[mod]
        
        with pytest.warns(DeprecationWarning):
            import liteagent