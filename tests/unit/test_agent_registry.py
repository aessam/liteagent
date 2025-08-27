"""
Unit tests for the AgentRegistry system.
"""

import pytest
import asyncio
import time
from unittest.mock import MagicMock

from liteagent.agent_registry import (
    AgentRegistry, AgentCapability, AgentStatus, RegisteredAgent
)


class TestAgentCapability:
    """Test AgentCapability functionality."""
    
    def test_capability_creation(self):
        """Test creating an AgentCapability."""
        capability = AgentCapability(
            name="test_capability",
            description="A test capability",
            metadata={"keywords": ["test", "demo"]}
        )
        
        assert capability.name == "test_capability"
        assert capability.description == "A test capability"
        assert capability.metadata["keywords"] == ["test", "demo"]
    
    def test_capability_matching_exact_name(self):
        """Test exact name matching."""
        capability = AgentCapability(
            name="code_analysis",
            description="Analyzes code structure"
        )
        
        assert capability.matches_requirement("code_analysis")
        assert capability.matches_requirement("CODE_ANALYSIS")  # Case insensitive
        assert not capability.matches_requirement("data_analysis")
    
    def test_capability_matching_description(self):
        """Test substring matching in description."""
        capability = AgentCapability(
            name="analyzer",
            description="Analyzes code structure and complexity"
        )
        
        assert capability.matches_requirement("code")
        assert capability.matches_requirement("structure")
        assert capability.matches_requirement("complexity")
        assert not capability.matches_requirement("database")
    
    def test_capability_matching_keywords(self):
        """Test keyword matching in metadata."""
        capability = AgentCapability(
            name="processor",
            description="Processes data",
            metadata={"keywords": ["nlp", "text processing", "analysis"]}
        )
        
        assert capability.matches_requirement("nlp")
        assert capability.matches_requirement("text")
        assert capability.matches_requirement("processing")
        assert not capability.matches_requirement("image")


class TestRegisteredAgent:
    """Test RegisteredAgent functionality."""
    
    def test_agent_creation(self):
        """Test creating a RegisteredAgent."""
        mock_agent = MagicMock()
        capabilities = [AgentCapability("test_cap", "Test capability")]
        
        agent = RegisteredAgent(
            agent_id="agent_123",
            name="TestAgent",
            agent_instance=mock_agent,
            capabilities=capabilities
        )
        
        assert agent.agent_id == "agent_123"
        assert agent.name == "TestAgent"
        assert agent.agent_instance == mock_agent
        assert len(agent.capabilities) == 1
        assert agent.status == AgentStatus.IDLE
        assert agent.task_count == 0
    
    def test_agent_heartbeat(self):
        """Test heartbeat functionality."""
        mock_agent = MagicMock()
        agent = RegisteredAgent(
            agent_id="agent_123",
            name="TestAgent",
            agent_instance=mock_agent,
            capabilities=[]
        )
        
        original_heartbeat = agent.last_heartbeat
        time.sleep(0.01)  # Small delay
        agent.update_heartbeat()
        
        assert agent.last_heartbeat > original_heartbeat
    
    def test_agent_health_check(self):
        """Test agent health checking."""
        mock_agent = MagicMock()
        agent = RegisteredAgent(
            agent_id="agent_123",
            name="TestAgent",
            agent_instance=mock_agent,
            capabilities=[]
        )
        
        # Should be healthy immediately
        assert agent.is_healthy(timeout=1.0)
        
        # Simulate old heartbeat
        agent.last_heartbeat = time.time() - 2.0
        assert not agent.is_healthy(timeout=1.0)
    
    def test_agent_counters(self):
        """Test task counting functionality."""
        mock_agent = MagicMock()
        agent = RegisteredAgent(
            agent_id="agent_123",
            name="TestAgent",
            agent_instance=mock_agent,
            capabilities=[]
        )
        
        # Initial state
        assert agent.task_count == 0
        assert agent.success_count == 0
        assert agent.error_count == 0
        assert agent.get_success_rate() == 1.0
        
        # Increment counters
        agent.increment_task_count()
        agent.increment_success_count()
        assert agent.task_count == 1
        assert agent.success_count == 1
        assert agent.get_success_rate() == 1.0
        
        agent.increment_task_count()
        agent.increment_error_count()
        assert agent.task_count == 2
        assert agent.error_count == 1
        assert agent.get_success_rate() == 0.5


class TestAgentRegistry:
    """Test AgentRegistry functionality."""
    
    @pytest.fixture
    def registry(self):
        """Create a fresh registry for testing."""
        return AgentRegistry(heartbeat_timeout=1.0)
    
    @pytest.mark.asyncio
    async def test_agent_registration(self, registry):
        """Test agent registration."""
        mock_agent = MagicMock()
        capabilities = ["code_analysis", "test_generation"]
        
        agent_id = await registry.register_agent(
            agent=mock_agent,
            capabilities=capabilities,
            name="TestAgent"
        )
        
        assert agent_id is not None
        
        # Check that agent was registered
        registered_agent = await registry.get_agent(agent_id)
        assert registered_agent is not None
        assert registered_agent.name == "TestAgent"
        assert len(registered_agent.capabilities) == 2
    
    @pytest.mark.asyncio
    async def test_agent_registration_with_capability_objects(self, registry):
        """Test registration with AgentCapability objects."""
        mock_agent = MagicMock()
        capabilities = [
            AgentCapability("analysis", "Code analysis", metadata={"level": "expert"}),
            "simple_capability"  # Mix of objects and strings
        ]
        
        agent_id = await registry.register_agent(
            agent=mock_agent,
            capabilities=capabilities
        )
        
        registered_agent = await registry.get_agent(agent_id)
        assert len(registered_agent.capabilities) == 2
        assert registered_agent.capabilities[0].metadata["level"] == "expert"
    
    @pytest.mark.asyncio
    async def test_agent_unregistration(self, registry):
        """Test agent unregistration."""
        mock_agent = MagicMock()
        agent_id = await registry.register_agent(mock_agent, ["test_cap"])
        
        # Should exist
        agent = await registry.get_agent(agent_id)
        assert agent is not None
        
        # Unregister
        success = await registry.unregister_agent(agent_id)
        assert success
        
        # Should not exist
        agent = await registry.get_agent(agent_id)
        assert agent is None
        
        # Double unregister should fail
        success = await registry.unregister_agent(agent_id)
        assert not success
    
    @pytest.mark.asyncio
    async def test_find_agents_by_capability(self, registry):
        """Test finding agents by capability."""
        # Register multiple agents
        agent1 = MagicMock()
        agent2 = MagicMock()
        agent3 = MagicMock()
        
        id1 = await registry.register_agent(agent1, ["code_analysis", "testing"])
        id2 = await registry.register_agent(agent2, ["code_analysis", "documentation"])
        id3 = await registry.register_agent(agent3, ["data_processing"])
        
        # Find agents with code_analysis capability
        code_agents = await registry.find_agents_by_capability("code_analysis")
        assert len(code_agents) == 2
        agent_ids = [a.agent_id for a in code_agents]
        assert id1 in agent_ids
        assert id2 in agent_ids
        assert id3 not in agent_ids
        
        # Find agents with non-existent capability
        missing_agents = await registry.find_agents_by_capability("missing_capability")
        assert len(missing_agents) == 0
    
    @pytest.mark.asyncio
    async def test_agent_status_management(self, registry):
        """Test agent status updates."""
        mock_agent = MagicMock()
        agent_id = await registry.register_agent(mock_agent, ["test_cap"])
        
        # Initial status should be IDLE
        status = await registry.get_agent_status(agent_id)
        assert status == AgentStatus.IDLE
        
        # Update status
        success = await registry.update_agent_status(agent_id, AgentStatus.BUSY)
        assert success
        
        status = await registry.get_agent_status(agent_id)
        assert status == AgentStatus.BUSY
        
        # Update non-existent agent
        success = await registry.update_agent_status("fake_id", AgentStatus.IDLE)
        assert not success
    
    @pytest.mark.asyncio
    async def test_heartbeat_management(self, registry):
        """Test heartbeat management."""
        mock_agent = MagicMock()
        agent_id = await registry.register_agent(mock_agent, ["test_cap"])
        
        # Send heartbeat
        success = await registry.heartbeat(agent_id)
        assert success
        
        # Heartbeat for non-existent agent
        success = await registry.heartbeat("fake_id")
        assert not success
    
    @pytest.mark.asyncio
    async def test_select_best_agent(self, registry):
        """Test best agent selection."""
        # Register agents with different characteristics
        agent1 = MagicMock()
        agent2 = MagicMock() 
        agent3 = MagicMock()
        
        id1 = await registry.register_agent(agent1, ["analysis"], name="Agent1")
        id2 = await registry.register_agent(agent2, ["analysis"], name="Agent2")
        id3 = await registry.register_agent(agent3, ["other_cap"], name="Agent3")
        
        # Simulate different task counts
        await registry.record_task_start(id1)
        await registry.record_task_success(id1)
        await registry.record_task_start(id2)
        await registry.record_task_success(id2)
        await registry.record_task_start(id2)
        await registry.record_task_success(id2)
        
        # Select best agent for analysis (should prefer lower task count)
        best_agent = await registry.select_best_agent("analysis", load_balancing=True)
        assert best_agent is not None
        assert best_agent.agent_id == id1  # Should have fewer tasks
        
        # No agent for non-existent capability
        best_agent = await registry.select_best_agent("missing_cap")
        assert best_agent is None
    
    @pytest.mark.asyncio
    async def test_task_recording(self, registry):
        """Test task execution recording."""
        mock_agent = MagicMock()
        agent_id = await registry.register_agent(mock_agent, ["test_cap"])
        
        # Record task start
        success = await registry.record_task_start(agent_id)
        assert success
        
        agent = await registry.get_agent(agent_id)
        assert agent.task_count == 1
        assert agent.status == AgentStatus.BUSY
        
        # Record success
        success = await registry.record_task_success(agent_id)
        assert success
        
        agent = await registry.get_agent(agent_id)
        assert agent.success_count == 1
        assert agent.status == AgentStatus.IDLE
        
        # Record error
        await registry.record_task_start(agent_id)
        success = await registry.record_task_error(agent_id)
        assert success
        
        agent = await registry.get_agent(agent_id)
        assert agent.error_count == 1
        assert agent.status == AgentStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_registry_stats(self, registry):
        """Test registry statistics."""
        # Register some agents
        agent1 = MagicMock()
        agent2 = MagicMock()
        
        await registry.register_agent(agent1, ["cap1", "cap2"])
        await registry.register_agent(agent2, ["cap2", "cap3"])
        
        stats = await registry.get_registry_stats()
        
        assert stats["total_agents"] == 2
        assert stats["healthy_agents"] == 2
        assert stats["capability_breakdown"]["cap1"] == 1
        assert stats["capability_breakdown"]["cap2"] == 2
        assert stats["capability_breakdown"]["cap3"] == 1
    
    @pytest.mark.asyncio
    async def test_get_available_capabilities(self, registry):
        """Test getting available capabilities."""
        # Initially empty
        capabilities = await registry.get_available_capabilities()
        assert len(capabilities) == 0
        
        # Register agents
        await registry.register_agent(MagicMock(), ["cap1", "cap2"])
        await registry.register_agent(MagicMock(), ["cap2", "cap3"])
        
        capabilities = await registry.get_available_capabilities()
        assert len(capabilities) == 3
        assert "cap1" in capabilities
        assert "cap2" in capabilities
        assert "cap3" in capabilities
    
    @pytest.mark.asyncio
    async def test_get_all_agents(self, registry):
        """Test getting all registered agents."""
        # Initially empty
        agents = await registry.get_all_agents()
        assert len(agents) == 0
        
        # Register agents
        await registry.register_agent(MagicMock(), ["cap1"])
        await registry.register_agent(MagicMock(), ["cap2"])
        
        agents = await registry.get_all_agents()
        assert len(agents) == 2
    
    @pytest.mark.asyncio 
    async def test_agent_filtering_by_status(self, registry):
        """Test filtering agents by status."""
        agent1 = MagicMock()
        agent2 = MagicMock()
        
        id1 = await registry.register_agent(agent1, ["test_cap"])
        id2 = await registry.register_agent(agent2, ["test_cap"])
        
        # Set different statuses
        await registry.update_agent_status(id1, AgentStatus.IDLE)
        await registry.update_agent_status(id2, AgentStatus.BUSY)
        
        # Find only idle agents
        idle_agents = await registry.find_agents_by_capability(
            "test_cap", 
            status_filter=[AgentStatus.IDLE]
        )
        assert len(idle_agents) == 1
        assert idle_agents[0].agent_id == id1
        
        # Find only busy agents
        busy_agents = await registry.find_agents_by_capability(
            "test_cap",
            status_filter=[AgentStatus.BUSY],
            include_busy=True
        )
        assert len(busy_agents) == 1
        assert busy_agents[0].agent_id == id2
    
    @pytest.mark.asyncio
    async def test_registry_shutdown(self, registry):
        """Test registry shutdown."""
        await registry.shutdown()
        # Should complete without error