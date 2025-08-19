"""
Unit tests for ForkedAgent functionality.

This module tests the forking mechanism, memory inheritance, tool subsetting,
and cache optimization features of ForkedAgent.
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from liteagent.forked_agent import ForkedAgent, ForkedMemory, ForkEvent
from liteagent.memory import ConversationMemory
from liteagent.tools import liteagent_tool


# Sample tools for testing
@liteagent_tool(name="test_tool_1")
def test_tool_1(input: str) -> str:
    """Test tool 1."""
    return f"Tool 1 processed: {input}"


@liteagent_tool(name="test_tool_2")
def test_tool_2(input: str) -> str:
    """Test tool 2."""
    return f"Tool 2 processed: {input}"


@liteagent_tool(name="test_tool_3")
def test_tool_3(input: str) -> str:
    """Test tool 3."""
    return f"Tool 3 processed: {input}"


class TestForkedMemory:
    """Test ForkedMemory class functionality."""
    
    def test_forked_memory_initialization(self):
        """Test that ForkedMemory correctly inherits from parent memory."""
        # Create parent memory
        parent_memory = ConversationMemory(system_prompt="You are a helpful assistant.")
        parent_memory.add_user_message("Hello")
        parent_memory.messages.append({"role": "assistant", "content": "Hi there!"})
        
        # Create forked memory
        forked_memory = ForkedMemory(parent_memory)
        
        # Verify inheritance
        assert forked_memory.system_prompt == parent_memory.system_prompt
        assert len(forked_memory.messages) == len(parent_memory.messages)
        assert forked_memory.messages[0] == parent_memory.messages[0]
        assert forked_memory._fork_point == len(parent_memory.messages)
        
    def test_forked_memory_with_prefill(self):
        """Test ForkedMemory with prefill messages."""
        parent_memory = ConversationMemory(system_prompt="Base system prompt")
        parent_memory.add_user_message("Initial message")
        
        prefill_messages = [
            {"role": "user", "content": "You are now a specialist"},
            {"role": "assistant", "content": "Understood, I am now a specialist"}
        ]
        
        forked_memory = ForkedMemory(parent_memory, prefill_messages)
        
        # Verify prefill messages are added
        assert len(forked_memory.messages) == len(parent_memory.messages) + len(prefill_messages)
        assert forked_memory.messages[-2:] == prefill_messages
        
    def test_forked_memory_independence(self):
        """Test that forked memory is independent from parent."""
        parent_memory = ConversationMemory(system_prompt="Parent prompt")
        parent_memory.add_user_message("Parent message")
        
        forked_memory = ForkedMemory(parent_memory)
        
        # Modify forked memory
        forked_memory.add_user_message("Fork message")
        
        # Verify parent is not affected
        assert len(parent_memory.messages) == 2  # system + user
        assert len(forked_memory.messages) == 3  # system + user + new user
        
    def test_cache_key_generation(self):
        """Test cache key generation for forked memory."""
        parent_memory = ConversationMemory(system_prompt="Test prompt")
        parent_memory.add_user_message("Test message")
        
        forked_memory = ForkedMemory(parent_memory)
        cache_key = forked_memory.get_cache_key()
        
        assert isinstance(cache_key, str)
        assert len(cache_key) == 64  # SHA256 hex digest length
        
    def test_get_messages_for_api(self):
        """Test getting messages for API calls."""
        parent_memory = ConversationMemory(system_prompt="System")
        parent_memory.add_user_message("Message 1")
        parent_memory.messages.append({"role": "assistant", "content": "Response 1"})
        
        forked_memory = ForkedMemory(parent_memory)
        forked_memory.add_user_message("Message 2")
        
        # Test with cache
        all_messages = forked_memory.get_messages_for_api(include_cached=True)
        assert len(all_messages) == 4  # system + user + assistant + new user
        
        # Test without cache
        new_messages = forked_memory.get_messages_for_api(include_cached=False)
        assert len(new_messages) == 1  # only new user message


class TestForkedAgent:
    """Test ForkedAgent class functionality."""
    
    @patch('liteagent.forked_agent.create_model_interface')
    def test_forked_agent_initialization(self, mock_create_model):
        """Test ForkedAgent initialization."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        agent = ForkedAgent(
            model="test-model",
            name="test-agent",
            system_prompt="Test prompt",
            enable_caching=True
        )
        
        assert agent.enable_caching is True
        assert agent._fork_count == 0
        assert agent._child_agents == []
        assert agent._is_fork is False
        assert agent._allowed_tools is None
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_fork_creation_basic(self, mock_create_model):
        """Test basic fork creation."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent",
            system_prompt="Parent prompt",
            tools=[test_tool_1, test_tool_2, test_tool_3]
        )
        
        # Create a fork
        fork = parent.fork(name="child_fork")
        
        assert fork.name == "child_fork"
        assert fork._is_fork is True
        assert fork.parent_context_id == parent.context_id
        assert parent._fork_count == 1
        assert len(parent._child_agents) == 1
        assert parent._child_agents[0] == fork
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_fork_with_prefill_role(self, mock_create_model):
        """Test fork creation with prefill role."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent",
            system_prompt="Parent prompt"
        )
        
        fork = parent.fork(
            name="specialist",
            prefill_role="security expert"
        )
        
        # Verify prefill messages were generated
        assert isinstance(fork.memory, ForkedMemory)
        # Check that prefill messages were added
        assert len(fork.memory.messages) > len(parent.memory.messages)
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_fork_with_tool_subset(self, mock_create_model):
        """Test fork with tool subsetting."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent",
            tools=[test_tool_1, test_tool_2, test_tool_3]
        )
        
        # Create fork with tool subset
        fork = parent.fork(
            name="limited_fork",
            allowed_tools=["test_tool_1", "test_tool_3"]
        )
        
        assert fork._allowed_tools == {"test_tool_1", "test_tool_3"}
        assert len(fork.tools) == 2
        assert "test_tool_1" in fork.tools
        assert "test_tool_3" in fork.tools
        assert "test_tool_2" not in fork.tools
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_fork_with_system_prompt_suffix(self, mock_create_model):
        """Test fork with system prompt suffix."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent",
            system_prompt="Base prompt"
        )
        
        fork = parent.fork(
            name="enhanced_fork",
            system_prompt_suffix="Additional instructions"
        )
        
        assert "Base prompt" in fork.system_prompt
        assert "Additional instructions" in fork.system_prompt
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_multiple_forks(self, mock_create_model):
        """Test creating multiple forks."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent"
        )
        
        fork1 = parent.fork(name="fork1")
        fork2 = parent.fork(name="fork2")
        fork3 = parent.fork()  # Auto-named
        
        assert parent._fork_count == 3
        assert len(parent._child_agents) == 3
        assert fork3.name == "parent_fork_3"
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_fork_event_emission(self, mock_create_model):
        """Test that fork events are emitted to observers."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        mock_observer = MagicMock()
        
        parent = ForkedAgent(
            model="test-model",
            name="parent",
            observers=[mock_observer]
        )
        
        fork = parent.fork(
            name="child",
            prefill_role="specialist",
            allowed_tools=["tool1"]
        )
        
        # Verify observer was notified
        mock_observer.on_event.assert_called_once()
        event = mock_observer.on_event.call_args[0][0]
        assert isinstance(event, ForkEvent)
        assert event.event_data["child_agent_id"] == fork.agent_id
        assert event.event_data["prefill_role"] == "specialist"
        assert event.event_data["allowed_tools"] == ["tool1"]
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_generate_prefill_messages(self, mock_create_model):
        """Test prefill message generation."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        agent = ForkedAgent(
            model="test-model",
            name="agent"
        )
        
        messages = agent._generate_prefill_messages("security expert")
        
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert "security expert" in messages[0]["content"]
        assert messages[1]["role"] == "assistant"
        assert "security expert" in messages[1]["content"]
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_get_fork_tree(self, mock_create_model):
        """Test getting the fork tree structure."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent"
        )
        
        fork1 = parent.fork(name="fork1", allowed_tools=["tool1"])
        fork2 = parent.fork(name="fork2")
        
        # Create a nested fork
        fork1_1 = fork1.fork(name="fork1_1")
        
        tree = parent.get_fork_tree()
        
        assert tree["name"] == "parent"
        assert tree["fork_count"] == 2
        assert len(tree["children"]) == 2
        
        # Find fork1 in children
        fork1_tree = next(c for c in tree["children"] if c["name"] == "fork1")
        assert fork1_tree["allowed_tools"] == ["tool1"]
        assert len(fork1_tree["children"]) == 1
        assert fork1_tree["children"][0]["name"] == "fork1_1"
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_cache_savings_calculation(self, mock_create_model):
        """Test cache savings calculation."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent",
            system_prompt="x" * 4000  # ~1000 tokens
        )
        
        # Create multiple forks
        for i in range(3):
            parent.fork(name=f"fork_{i}")
            
        savings = parent.get_cache_savings()
        
        assert savings["total_forks"] == 3
        assert savings["cached_tokens"] > 0
        assert savings["tokens_saved"] == savings["cached_tokens"] * 3
        assert "$" in savings["estimated_cost_saved"]
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_cache_hit_rate_calculation(self, mock_create_model):
        """Test cache hit rate calculation."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        parent = ForkedAgent(
            model="test-model",
            name="parent"
        )
        
        # Simulate cache hits and misses
        parent._cache_stats["hits"] = 8
        parent._cache_stats["misses"] = 2
        
        fork = parent.fork(name="fork1")
        fork._cache_stats["hits"] = 5
        fork._cache_stats["misses"] = 0
        
        hit_rate = parent._calculate_cache_hit_rate()
        
        # Total: 13 hits, 2 misses = 13/15 = 0.867
        assert hit_rate == pytest.approx(0.867, rel=0.01)
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_create_message_with_cache(self, mock_create_model):
        """Test message preparation with cache control."""
        mock_provider = MagicMock()
        mock_provider.__class__.__name__ = 'AnthropicProvider'
        mock_provider.supports_caching.return_value = True
        
        mock_model_interface = MagicMock()
        mock_model_interface.provider = mock_provider
        mock_model_interface.supports_caching.return_value = True
        mock_create_model.return_value = mock_model_interface
        
        agent = ForkedAgent(
            model="claude-3",
            name="agent",
            enable_caching=True
        )
        agent.model_interface = mock_model_interface
        
        # Test with long message
        messages = [
            {"role": "user", "content": "x" * 2000}  # Long message
        ]
        
        cached_messages = agent._create_message_with_cache(messages)
        
        assert len(cached_messages) == 1
        assert isinstance(cached_messages[0]["content"], list)
        assert cached_messages[0]["content"][0]["type"] == "text"
        assert "cache_control" in cached_messages[0]["content"][0]
        
    @patch('liteagent.forked_agent.create_model_interface')
    def test_create_message_without_cache(self, mock_create_model):
        """Test message preparation without cache for short messages."""
        mock_model = MagicMock()
        mock_create_model.return_value = mock_model
        
        agent = ForkedAgent(
            model="test-model",
            name="agent",
            enable_caching=False
        )
        
        messages = [
            {"role": "user", "content": "Short message"}
        ]
        
        cached_messages = agent._create_message_with_cache(messages)
        
        # Should return unchanged for short message or disabled caching
        assert cached_messages == messages


class TestForkEvent:
    """Test ForkEvent class."""
    
    def test_fork_event_creation(self):
        """Test ForkEvent initialization."""
        event = ForkEvent(
            parent_agent_id="parent_123",
            child_agent_id="child_456",
            parent_context_id="ctx_parent",
            child_context_id="ctx_child",
            prefill_role="specialist",
            allowed_tools={"tool1", "tool2"}
        )
        
        assert event.agent_id == "parent_123"
        assert event.event_type == "fork"
        assert event.context_id == "ctx_parent"
        assert event.event_data["child_agent_id"] == "child_456"
        assert event.event_data["child_context_id"] == "ctx_child"
        assert event.event_data["prefill_role"] == "specialist"
        assert set(event.event_data["allowed_tools"]) == {"tool1", "tool2"}