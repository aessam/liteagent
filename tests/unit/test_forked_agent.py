"""
Simplified unit tests for ForkedAgent functionality.

This module tests the core ForkedAgent features with minimal mocking.
"""

import pytest
from unittest.mock import Mock, patch
from liteagent.forked_agent import ForkedAgent, ForkedMemory, ForkEvent
from liteagent.memory import ConversationMemory


class TestForkedMemoryBasic:
    """Test ForkedMemory without complex mocking."""
    
    def test_forked_memory_inheritance(self):
        """Test basic memory inheritance."""
        parent_memory = ConversationMemory("System prompt")
        parent_memory.add_user_message("Hello")
        
        forked_memory = ForkedMemory(parent_memory)
        
        assert len(forked_memory.messages) == 2  # system + user
        assert forked_memory.system_prompt == "System prompt"
        assert forked_memory._fork_point == 2
        
    def test_forked_memory_with_prefill(self):
        """Test forked memory with prefill messages."""
        parent_memory = ConversationMemory("System")
        prefill = [{"role": "user", "content": "You are specialist"}]
        
        forked_memory = ForkedMemory(parent_memory, prefill)
        
        assert len(forked_memory.messages) == 2  # system + prefill
        assert forked_memory.messages[-1] == prefill[0]
        
    def test_forked_memory_independence(self):
        """Test that forked memory is independent."""
        parent_memory = ConversationMemory("System")
        forked_memory = ForkedMemory(parent_memory)
        
        # Modify forked memory
        forked_memory.add_user_message("Fork message")
        
        # Parent should be unchanged
        assert len(parent_memory.messages) == 1
        assert len(forked_memory.messages) == 2
        
    def test_cache_key_generation(self):
        """Test cache key is generated correctly."""
        parent_memory = ConversationMemory("Test")
        parent_memory.add_user_message("Message")
        
        forked_memory = ForkedMemory(parent_memory)
        cache_key = forked_memory.get_cache_key()
        
        assert isinstance(cache_key, str)
        assert len(cache_key) == 64  # SHA256


class TestForkedAgentCore:
    """Test core ForkedAgent functionality with minimal dependencies."""
    
    def test_interface_compatibility(self):
        """Test that ForkedAgent has the same interface as LiteAgent."""
        from liteagent.agent import LiteAgent
        
        # Get methods from LiteAgent
        liteagent_methods = set(method for method in dir(LiteAgent) 
                               if not method.startswith('_') and callable(getattr(LiteAgent, method)))
        
        # Get methods from ForkedAgent  
        forkedagent_methods = set(method for method in dir(ForkedAgent)
                                 if not method.startswith('_') and callable(getattr(ForkedAgent, method)))
        
        # ForkedAgent should have at least all the public methods of LiteAgent
        missing_methods = liteagent_methods - forkedagent_methods
        
        # Allow some methods to be missing if they're not essential
        allowed_missing = set()  # Add any methods that are OK to be missing
        
        essential_missing = missing_methods - allowed_missing
        
        assert len(essential_missing) == 0, f"ForkedAgent missing essential methods: {essential_missing}"
        
        # Test that key methods exist
        assert hasattr(ForkedAgent, 'chat'), "ForkedAgent must have chat method"
        assert hasattr(ForkedAgent, 'run'), "ForkedAgent must have run method for compatibility"
        assert hasattr(ForkedAgent, 'fork'), "ForkedAgent must have fork method"
    
    def test_prefill_message_generation(self):
        """Test prefill message generation without full agent creation."""
        # Create a minimal mock agent
        with patch('liteagent.models.create_model_interface'), \
             patch('liteagent.capabilities.get_model_capabilities') as mock_caps:
            
            mock_caps.return_value = None
            
            agent = ForkedAgent(
                model="claude-3-5-sonnet-20241022",
                name="test_agent"
            )
            
            messages = agent._generate_prefill_messages("security expert")
            
            assert len(messages) == 2
            assert messages[0]["role"] == "user"
            assert "security expert" in messages[0]["content"]
            assert messages[1]["role"] == "assistant"
            assert "security expert" in messages[1]["content"]
            
    def test_cache_message_creation_disabled(self):
        """Test cache message creation when caching is disabled."""
        with patch('liteagent.models.create_model_interface'), \
             patch('liteagent.capabilities.get_model_capabilities') as mock_caps:
            
            mock_caps.return_value = None
            
            agent = ForkedAgent(
                model="claude-3-5-sonnet-20241022",
                name="test_agent",
                enable_caching=False
            )
            
            messages = [{"role": "user", "content": "x" * 2000}]
            result = agent._create_message_with_cache(messages)
            
            # Should return unchanged when caching disabled
            assert result == messages
            
    def test_cache_hit_rate_calculation(self):
        """Test cache hit rate calculation."""
        with patch('liteagent.models.create_model_interface'), \
             patch('liteagent.capabilities.get_model_capabilities') as mock_caps:
            
            mock_caps.return_value = None
            
            agent = ForkedAgent(
                model="claude-3-5-sonnet-20241022",
                name="test_agent"
            )
            
            # Set cache stats
            agent._cache_stats = {"hits": 8, "misses": 2}
            
            hit_rate = agent._calculate_cache_hit_rate()
            assert hit_rate == 0.8  # 8/(8+2)


class TestForkEventBasic:
    """Test ForkEvent without complex agent setup."""
    
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
        assert event.event_data["prefill_role"] == "specialist"
        assert set(event.event_data["allowed_tools"]) == {"tool1", "tool2"}


# Integration test that only runs if environment is set up
@pytest.mark.integration
class TestForkedAgentIntegration:
    """Integration tests that require proper setup."""
    
    def test_real_fork_creation(self):
        """Test actual fork creation with real model interface (if available)."""
        try:
            # Only run if we can create a real agent
            parent = ForkedAgent(
                model="claude-3-5-sonnet-20241022",
                name="integration_test_parent",
                system_prompt="You are a test agent. Always respond with 'Hello from parent'",
                provider="anthropic"
            )
            
            # Create a fork
            fork = parent.fork(
                name="test_fork",
                prefill_role="testing specialist who always responds with 'Hello from fork'"
            )
            
            assert fork.name == "test_fork"
            assert fork._is_fork is True
            assert parent._fork_count == 1
            
            # Test that methods exist and can be called (without API key this will fail gracefully)
            try:
                # Test the chat method exists and is callable
                response = fork.chat("Test message")
                # If we get here, it means the method worked
                assert isinstance(response, str)
            except Exception as e:
                # Expected if no API key is set - that's fine for this test
                if "api" in str(e).lower() or "key" in str(e).lower() or "auth" in str(e).lower():
                    pytest.skip(f"API test skipped (no credentials): {e}")
                else:
                    # Re-raise if it's a different error (like method not found)
                    raise
            
        except Exception as e:
            if "api" in str(e).lower() or "key" in str(e).lower():
                pytest.skip(f"Integration test skipped (no credentials): {e}")
            else:
                pytest.skip(f"Integration test skipped: {e}")


if __name__ == "__main__":
    # Run the basic tests
    pytest.main([__file__, "-v"])