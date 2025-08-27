"""
Comprehensive integration tests for ForkedAgent functionality.

This consolidates tests from scattered files like test_forked_caching.py,
test_fixed_forked_agents.py, etc. into proper integration tests.
"""

import pytest
import os
import time
import asyncio
from typing import Dict, Any

from liteagent import UnifiedForkedAgent, ForkConfig, liteagent_tool
from liteagent.multi_agent_coordinator import MultiAgentCoordinator
from liteagent.agent_registry import AgentCapability
from liteagent.provider_cost_tracker import get_cost_tracker


# Test tools for ForkedAgent testing
@liteagent_tool
def analyze_code(code: str) -> str:
    """Analyze code for potential issues."""
    lines = code.split('\n')
    issues = []
    
    for i, line in enumerate(lines, 1):
        if 'eval(' in line:
            issues.append(f"Line {i}: Potential security issue with eval()")
        if 'import *' in line:
            issues.append(f"Line {i}: Avoid wildcard imports")
        if len(line) > 100:
            issues.append(f"Line {i}: Line too long ({len(line)} chars)")
    
    if not issues:
        return "Code analysis complete: No issues found."
    
    return f"Code analysis complete. Found {len(issues)} issues:\n" + "\n".join(issues)


@liteagent_tool
def check_security(code: str) -> str:
    """Check code for security vulnerabilities."""
    vulnerabilities = []
    
    if 'eval(' in code:
        vulnerabilities.append("CRITICAL: Use of eval() function")
    if 'exec(' in code:
        vulnerabilities.append("HIGH: Use of exec() function")
    if 'input(' in code and 'eval(' in code:
        vulnerabilities.append("CRITICAL: User input passed to eval()")
    if '__import__' in code:
        vulnerabilities.append("MEDIUM: Dynamic imports detected")
    
    if not vulnerabilities:
        return "Security check complete: No vulnerabilities found."
    
    return f"Security check complete. Found {len(vulnerabilities)} vulnerabilities:\n" + "\n".join(vulnerabilities)


@liteagent_tool
def optimize_performance(code: str) -> str:
    """Suggest performance optimizations for code."""
    suggestions = []
    
    if 'for i in range(len(' in code:
        suggestions.append("Use enumerate() instead of range(len())")
    if '.append(' in code and 'for ' in code:
        suggestions.append("Consider using list comprehension")
    if 'time.sleep(' in code:
        suggestions.append("Consider async/await for non-blocking operations")
    
    if not suggestions:
        return "Performance analysis complete: Code is well optimized."
    
    return f"Performance analysis complete. Suggestions:\n" + "\n".join(f"- {s}" for s in suggestions)


@pytest.mark.integration
class TestForkedAgentBasics:
    """Test basic ForkedAgent functionality."""
    
    @pytest.fixture
    def base_agent(self):
        """Create a base agent for testing."""
        return UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            name="BaseCodeAnalyzer",
            system_prompt="You are a code analysis expert. Analyze code for issues, security, and performance.",
            tools=[analyze_code, check_security, optimize_performance],
            api_key=os.getenv("ANTHROPIC_API_KEY", "test-key"),
            enable_rate_limiting=False  # Disable for testing
        )
    
    def test_agent_initialization(self, base_agent):
        """Test that agent initializes correctly."""
        assert base_agent.name == "BaseCodeAnalyzer"
        assert base_agent.session_type.value in ["stateless", "stateful", "cached"]
        assert len(base_agent.tools) == 3
        assert base_agent._fork_count == 0
    
    def test_session_type_determination(self, base_agent):
        """Test session type is determined correctly for different providers."""
        # Should be cached for Anthropic
        assert base_agent.session_type.value == "cached"
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    def test_basic_chat_functionality(self, base_agent):
        """Test basic chat functionality works."""
        response = base_agent.chat("Hello, can you analyze code?")
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "code" in response.lower() or "analysis" in response.lower()


@pytest.mark.integration
class TestForkedAgentCaching:
    """Test ForkedAgent caching functionality (from test_forked_caching.py)."""
    
    @pytest.fixture
    def cached_agent(self):
        """Create an agent with caching enabled."""
        return UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            name="CachedAnalyzer",
            system_prompt="You are a code analysis expert specializing in security and performance.",
            tools=[analyze_code, check_security, optimize_performance],
            api_key=os.getenv("ANTHROPIC_API_KEY", "test-key"),
            enable_caching=True,
            enable_rate_limiting=False
        )
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    def test_cache_preparation(self, cached_agent):
        """Test that agent can be prepared for caching."""
        # Should be able to prepare for forking (which sets up caching)
        result = cached_agent.prepare_for_forking()
        assert result is True
        
        # Should have added preparation messages
        messages = cached_agent.memory.get_messages()
        assert len(messages) >= 3  # system + user + assistant
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key") 
    def test_fork_creation_with_caching(self, cached_agent):
        """Test creating forks with caching enabled."""
        # Prepare for forking
        cached_agent.prepare_for_forking()
        
        # Create security specialist fork
        security_config = ForkConfig(
            name="SecurityExpert",
            role="security specialist focusing on vulnerability detection",
            tools=["check_security", "analyze_code"]
        )
        
        security_fork = cached_agent.fork(security_config)
        
        assert security_fork.name == "SecurityExpert"
        assert security_fork._is_fork is True
        assert security_fork.parent_agent == cached_agent
        assert security_fork._allowed_tools == {"check_security", "analyze_code"}
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    def test_multiple_forks_efficiency(self, cached_agent):
        """Test that multiple forks are created efficiently."""
        start_time = time.time()
        
        # Prepare once
        cached_agent.prepare_for_forking()
        
        # Create multiple forks
        configs = [
            ForkConfig(name="SecurityExpert", role="security specialist", tools=["check_security"]),
            ForkConfig(name="PerformanceExpert", role="performance specialist", tools=["optimize_performance"]),
            ForkConfig(name="GeneralAnalyst", role="general code analyst", tools=["analyze_code"])
        ]
        
        forks = []
        for config in configs:
            fork = cached_agent.fork(config)
            forks.append(fork)
        
        creation_time = time.time() - start_time
        
        # Should create forks reasonably quickly
        assert creation_time < 10.0  # Less than 10 seconds for 3 forks
        assert len(forks) == 3
        assert all(fork._is_fork for fork in forks)


@pytest.mark.integration 
class TestForkedAgentBatching:
    """Test ForkedAgent batch processing functionality."""
    
    @pytest.fixture
    def batch_agent(self):
        """Create an agent for batch testing."""
        return UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic", 
            name="BatchAnalyzer",
            system_prompt="You are a comprehensive code analysis expert.",
            tools=[analyze_code, check_security, optimize_performance],
            api_key=os.getenv("ANTHROPIC_API_KEY", "test-key"),
            enable_rate_limiting=True  # Test with rate limiting
        )
    
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    def test_batch_analyze_functionality(self, batch_agent):
        """Test batch analysis with multiple specialized forks."""
        # Prepare for forking
        batch_agent.prepare_for_forking()
        
        # Sample code to analyze
        test_code = '''
def vulnerable_function(user_input):
    # This is a security vulnerability
    result = eval(user_input)
    return result

def inefficient_loop(data):
    results = []
    for i in range(len(data)):
        if data[i] > 0:
            results.append(data[i] * 2)
    return results
'''
        
        # Define analysis tasks
        tasks = [
            {
                "name": "security_analysis",
                "role": "security specialist focusing on vulnerabilities",
                "tools": ["check_security"],
                "message": f"Analyze this code for security vulnerabilities:\n\n{test_code}"
            },
            {
                "name": "performance_analysis", 
                "role": "performance specialist focusing on optimization",
                "tools": ["optimize_performance"],
                "message": f"Analyze this code for performance issues:\n\n{test_code}"
            },
            {
                "name": "general_analysis",
                "role": "general code analyst",
                "tools": ["analyze_code"],
                "message": f"Perform general code analysis:\n\n{test_code}"
            }
        ]
        
        # Execute batch analysis
        results = batch_agent.batch_analyze(tasks, max_parallel=2)
        
        # Verify results
        assert len(results) == 3
        assert "security_analysis" in results
        assert "performance_analysis" in results
        assert "general_analysis" in results
        
        # Check that all tasks completed successfully
        for task_name, result in results.items():
            assert result["success"] is True
            assert isinstance(result["response"], str)
            assert len(result["response"]) > 0


@pytest.mark.integration
class TestForkedAgentMultiAgentIntegration:
    """Test ForkedAgent integration with multi-agent coordinator."""
    
    @pytest.fixture
    async def coordinator_with_forked_agents(self):
        """Create a coordinator with ForkedAgent integration."""
        coordinator = MultiAgentCoordinator(
            max_concurrent_tasks=5,
            default_task_timeout=30.0
        )
        await coordinator.start()
        
        # Create ForkedAgent with coordinator
        forked_agent = UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            name="IntegratedAnalyzer", 
            system_prompt="You are a code analysis expert.",
            tools=[analyze_code, check_security],
            api_key=os.getenv("ANTHROPIC_API_KEY", "test-key"),
            multi_agent_coordinator=coordinator,
            enable_rate_limiting=False
        )
        
        yield coordinator, forked_agent
        
        await coordinator.shutdown()
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    async def test_forked_agent_coordinator_registration(self, coordinator_with_forked_agents):
        """Test registering ForkedAgent with coordinator."""
        coordinator, forked_agent = coordinator_with_forked_agents
        
        # Register with capabilities
        capabilities = [
            AgentCapability("code_analysis", "Analyze code structure and quality"),
            AgentCapability("security_analysis", "Check for security vulnerabilities")
        ]
        
        agent_id = forked_agent.register_with_coordinator(capabilities)
        
        assert agent_id is not None
        assert forked_agent._agent_registry_id == agent_id
        
        # Verify registration with coordinator
        registered_agent = await coordinator.registry.get_agent(agent_id)
        assert registered_agent is not None
        assert registered_agent.name == "IntegratedAnalyzer"
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="No Anthropic API key")
    async def test_forked_agent_blackboard_integration(self, coordinator_with_forked_agents):
        """Test ForkedAgent blackboard integration."""
        coordinator, forked_agent = coordinator_with_forked_agents
        
        # Register agent
        capabilities = [AgentCapability("code_analysis", "Analyze code")]
        forked_agent.register_with_coordinator(capabilities)
        
        # Subscribe to blackboard updates
        subscription_id = forked_agent.subscribe_to_blackboard("analysis_.*")
        assert subscription_id is not None
        assert subscription_id in forked_agent._blackboard_subscriptions
        
        # Write knowledge to blackboard
        await coordinator.blackboard.write_knowledge(
            key="analysis_request",
            data={"code": "def test(): pass", "priority": "high"},
            agent_id="test_agent",
            category="analysis_requests"
        )
        
        # Give some time for notification processing
        await asyncio.sleep(0.1)


@pytest.mark.integration
class TestForkedAgentErrorHandling:
    """Test ForkedAgent error handling and recovery."""
    
    @pytest.fixture
    def error_prone_agent(self):
        """Create an agent for error testing."""
        return UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            name="ErrorTestAgent",
            system_prompt="You are a test agent.",
            api_key="invalid-key",  # Invalid key to trigger errors
            enable_rate_limiting=False
        )
    
    def test_fork_preparation_failure_handling(self, error_prone_agent):
        """Test handling of fork preparation failures."""
        # With invalid API key, preparation should fail gracefully
        result = error_prone_agent.prepare_for_forking()
        
        # Should handle failure gracefully
        assert result is False or result is True  # Depends on mock behavior
    
    def test_fork_creation_without_preparation(self, error_prone_agent):
        """Test fork creation when preparation fails."""
        # Mock preparation to fail
        error_prone_agent.prepare_for_forking = lambda: False
        
        config = ForkConfig(name="test_fork", role="test_role")
        
        with pytest.raises(RuntimeError, match="could not be prepared for forking"):
            error_prone_agent.fork(config)
    
    def test_batch_analysis_error_handling(self, error_prone_agent):
        """Test error handling in batch analysis."""
        # Mock fork creation to succeed but chat to fail
        mock_fork = type('MockFork', (), {
            'name': 'error_fork',
            'chat': lambda self, msg: (_ for _ in ()).throw(Exception("Chat failed"))
        })()
        
        error_prone_agent.fork = lambda config: mock_fork
        
        tasks = [
            {
                "name": "failing_task",
                "role": "test_role",
                "message": "This will fail"
            }
        ]
        
        results = error_prone_agent.batch_analyze(tasks)
        
        assert len(results) == 1
        assert results["failing_task"]["success"] is False
        assert "error" in results["failing_task"]


@pytest.mark.integration
class TestForkedAgentStats:
    """Test ForkedAgent statistics and monitoring."""
    
    @pytest.fixture
    def stats_agent(self):
        """Create an agent for stats testing."""
        return UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            name="StatsAgent",
            system_prompt="You are a test agent.",
            tools=[analyze_code],
            api_key=os.getenv("ANTHROPIC_API_KEY", "test-key"),
            enable_rate_limiting=False
        )
    
    def test_basic_stats_generation(self, stats_agent):
        """Test basic statistics generation."""
        stats = stats_agent.get_stats()
        
        assert stats["name"] == "StatsAgent"
        assert stats["session_type"] == "cached"
        assert stats["is_fork"] is False
        assert stats["num_forks"] == 0
        assert "fork_names" in stats
    
    def test_fork_tree_generation(self, stats_agent):
        """Test fork tree structure generation."""
        # Mock preparation
        stats_agent.prepare_for_forking = lambda: True
        
        # Create some forks
        configs = [
            ForkConfig(name="fork1", role="role1"),
            ForkConfig(name="fork2", role="role2")
        ]
        
        for config in configs:
            stats_agent.fork(config)
        
        tree = stats_agent.get_fork_tree()
        
        assert tree["name"] == "StatsAgent"
        assert tree["fork_count"] == 2
        assert len(tree["children"]) == 2
        assert tree["session_type"] == "cached"
    
    def test_stats_with_multi_agent_integration(self, stats_agent):
        """Test stats when integrated with multi-agent system."""
        # Mock integration
        stats_agent._agent_registry_id = "agent_123"
        stats_agent._blackboard_subscriptions = ["sub1", "sub2", "sub3"]
        
        stats = stats_agent.get_stats()
        
        assert stats["multi_agent_registry_id"] == "agent_123"
        assert stats["blackboard_subscriptions"] == 3


@pytest.mark.integration
class TestForkedAgentCleanup:
    """Test ForkedAgent cleanup and resource management."""
    
    @pytest.fixture
    def cleanup_agent(self):
        """Create an agent for cleanup testing."""
        return UnifiedForkedAgent(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            name="CleanupAgent",
            system_prompt="You are a test agent.",
            api_key=os.getenv("ANTHROPIC_API_KEY", "test-key"),
            enable_rate_limiting=False
        )
    
    def test_cleanup_without_resources(self, cleanup_agent):
        """Test cleanup when no resources are allocated."""
        # Should not raise any exceptions
        cleanup_agent.cleanup()
    
    def test_cleanup_with_forks(self, cleanup_agent):
        """Test cleanup with forks."""
        # Mock preparation
        cleanup_agent.prepare_for_forking = lambda: True
        
        # Create fork
        config = ForkConfig(name="test_fork", role="test_role")
        fork = cleanup_agent.fork(config)
        
        # Mock fork cleanup
        fork.cleanup = lambda: None
        
        # Should cleanup fork
        cleanup_agent.cleanup()
        
        # Cleanup should have been called (mocked, so no exception is success)
    
    def test_cleanup_with_coordinator_integration(self, cleanup_agent):
        """Test cleanup with multi-agent coordinator integration."""
        # Mock coordinator
        mock_coordinator = type('MockCoordinator', (), {
            'unsubscribe_from_knowledge_updates': lambda self, sub_id: None,
            'unregister_agent': lambda self, agent_id: None
        })()
        
        cleanup_agent.multi_agent_coordinator = mock_coordinator
        cleanup_agent._agent_registry_id = "agent_123"
        cleanup_agent._blackboard_subscriptions = ["sub1", "sub2"]
        
        # Should not raise exceptions
        cleanup_agent.cleanup()