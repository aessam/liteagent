"""
Agent registry for dynamic discovery and capability matching.

This module provides a registry system where agents can:
- Register themselves with their capabilities
- Discover other agents by capability
- Track agent status and availability
- Handle agent lifecycle management
"""

import asyncio
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
import logging

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration."""
    INITIALIZING = "initializing"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentCapability:
    """Represents a capability that an agent provides."""
    name: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def matches_requirement(self, requirement: str) -> bool:
        """Check if this capability matches a requirement string."""
        requirement_lower = requirement.lower()
        name_lower = self.name.lower()
        desc_lower = self.description.lower()
        
        # Exact name match
        if requirement_lower == name_lower:
            return True
        
        # Substring match in name or description
        if requirement_lower in name_lower or requirement_lower in desc_lower:
            return True
        
        # Check metadata keywords
        if self.metadata:
            keywords = self.metadata.get("keywords", [])
            if isinstance(keywords, list):
                for keyword in keywords:
                    if requirement_lower in keyword.lower():
                        return True
        
        return False


@dataclass
class RegisteredAgent:
    """Represents a registered agent in the registry."""
    agent_id: str
    name: str
    agent_instance: Any  # The actual LiteAgent instance
    capabilities: List[AgentCapability]
    status: AgentStatus = AgentStatus.IDLE
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Optional[Dict[str, Any]] = None
    registration_time: float = field(default_factory=time.time)
    task_count: int = 0
    success_count: int = 0
    error_count: int = 0
    
    def update_heartbeat(self):
        """Update the last heartbeat timestamp."""
        self.last_heartbeat = time.time()
    
    def is_healthy(self, timeout: float = 60.0) -> bool:
        """Check if agent is healthy based on heartbeat timeout."""
        return time.time() - self.last_heartbeat < timeout
    
    def increment_task_count(self):
        """Increment the task counter."""
        self.task_count += 1
    
    def increment_success_count(self):
        """Increment the success counter."""
        self.success_count += 1
    
    def increment_error_count(self):
        """Increment the error counter."""
        self.error_count += 1
    
    def get_success_rate(self) -> float:
        """Calculate success rate."""
        if self.task_count == 0:
            return 1.0
        return self.success_count / self.task_count


class AgentRegistry:
    """
    Registry for dynamic agent discovery and capability matching.
    
    Features:
    - Thread-safe agent registration and discovery
    - Capability-based agent matching
    - Agent health monitoring with heartbeats
    - Load balancing and status tracking
    - Automatic cleanup of offline agents
    """
    
    def __init__(self, heartbeat_timeout: float = 60.0):
        """
        Initialize the agent registry.
        
        Args:
            heartbeat_timeout: Timeout in seconds for agent heartbeats
        """
        self._agents: Dict[str, RegisteredAgent] = {}
        self._capabilities: Dict[str, Set[str]] = {}  # capability_name -> set of agent_ids
        self._lock = Lock()
        self._heartbeat_timeout = heartbeat_timeout
        self._cleanup_task: Optional[asyncio.Task] = None
        
        logger.info("AgentRegistry initialized")
    
    async def register_agent(self, 
                           agent: Any,
                           capabilities: List[Union[str, AgentCapability]],
                           name: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Register an agent with its capabilities.
        
        Args:
            agent: The LiteAgent instance to register
            capabilities: List of capabilities (strings or AgentCapability objects)
            name: Optional human-readable name for the agent
            metadata: Optional metadata for the agent
            
        Returns:
            The assigned agent ID
        """
        agent_id = str(uuid.uuid4())
        agent_name = name or getattr(agent, 'name', f"Agent-{agent_id[:8]}")
        
        # Convert string capabilities to AgentCapability objects
        capability_objects = []
        for cap in capabilities:
            if isinstance(cap, str):
                capability_objects.append(AgentCapability(
                    name=cap,
                    description=f"Capability: {cap}"
                ))
            elif isinstance(cap, AgentCapability):
                capability_objects.append(cap)
            else:
                raise ValueError(f"Invalid capability type: {type(cap)}")
        
        registered_agent = RegisteredAgent(
            agent_id=agent_id,
            name=agent_name,
            agent_instance=agent,
            capabilities=capability_objects,
            metadata=metadata
        )
        
        with self._lock:
            self._agents[agent_id] = registered_agent
            
            # Index capabilities
            for capability in capability_objects:
                cap_name = capability.name
                if cap_name not in self._capabilities:
                    self._capabilities[cap_name] = set()
                self._capabilities[cap_name].add(agent_id)
        
        logger.info(f"Agent registered: {agent_name} ({agent_id}) with {len(capability_objects)} capabilities")
        
        # Start cleanup task if not already running
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
        
        return agent_id
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from the registry.
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            True if agent was found and removed, False otherwise
        """
        with self._lock:
            agent = self._agents.pop(agent_id, None)
            if agent:
                # Remove from capability index
                for capability in agent.capabilities:
                    cap_name = capability.name
                    if cap_name in self._capabilities:
                        self._capabilities[cap_name].discard(agent_id)
                        # Remove empty capability sets
                        if not self._capabilities[cap_name]:
                            del self._capabilities[cap_name]
                
                logger.info(f"Agent unregistered: {agent.name} ({agent_id})")
                return True
            
            return False
    
    async def find_agents_by_capability(self, 
                                      capability: str,
                                      status_filter: Optional[List[AgentStatus]] = None,
                                      include_busy: bool = False) -> List[RegisteredAgent]:
        """
        Find agents that have a specific capability.
        
        Args:
            capability: The capability to search for
            status_filter: Optional list of statuses to filter by
            include_busy: Whether to include busy agents
            
        Returns:
            List of matching RegisteredAgent objects
        """
        matching_agents = []
        
        with self._lock:
            # Find agents with matching capabilities
            for agent in self._agents.values():
                # Check if agent is healthy
                if not agent.is_healthy(self._heartbeat_timeout):
                    continue
                
                # Check status filter
                if status_filter and agent.status not in status_filter:
                    continue
                
                # Skip busy agents unless explicitly included
                if not include_busy and agent.status == AgentStatus.BUSY:
                    continue
                
                # Check if any capability matches
                for agent_capability in agent.capabilities:
                    if agent_capability.matches_requirement(capability):
                        matching_agents.append(agent)
                        break
        
        # Sort by success rate and availability
        matching_agents.sort(
            key=lambda a: (a.status == AgentStatus.IDLE, a.get_success_rate()),
            reverse=True
        )
        
        logger.debug(f"Capability search: '{capability}' -> {len(matching_agents)} agents")
        return matching_agents
    
    async def get_agent(self, agent_id: str) -> Optional[RegisteredAgent]:
        """
        Get a specific agent by ID.
        
        Args:
            agent_id: The agent ID to look up
            
        Returns:
            The RegisteredAgent if found, None otherwise
        """
        with self._lock:
            return self._agents.get(agent_id)
    
    async def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """
        Get the status of a specific agent.
        
        Args:
            agent_id: The agent ID to check
            
        Returns:
            The agent's status if found, None otherwise
        """
        with self._lock:
            agent = self._agents.get(agent_id)
            return agent.status if agent else None
    
    async def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        """
        Update an agent's status.
        
        Args:
            agent_id: The agent ID to update
            status: The new status
            
        Returns:
            True if agent was found and updated, False otherwise
        """
        with self._lock:
            agent = self._agents.get(agent_id)
            if agent:
                old_status = agent.status
                agent.status = status
                agent.update_heartbeat()
                
                logger.debug(f"Agent status updated: {agent.name} ({agent_id}) {old_status} -> {status}")
                return True
            
            return False
    
    async def heartbeat(self, agent_id: str) -> bool:
        """
        Update an agent's heartbeat timestamp.
        
        Args:
            agent_id: The agent ID to update
            
        Returns:
            True if agent was found and updated, False otherwise
        """
        with self._lock:
            agent = self._agents.get(agent_id)
            if agent:
                agent.update_heartbeat()
                return True
            
            return False
    
    async def get_all_agents(self) -> List[RegisteredAgent]:
        """Get all registered agents."""
        with self._lock:
            return list(self._agents.values())
    
    async def get_available_capabilities(self) -> List[str]:
        """Get all available capabilities across all agents."""
        with self._lock:
            return list(self._capabilities.keys())
    
    async def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        with self._lock:
            total_agents = len(self._agents)
            status_counts = {}
            capability_counts = {}
            
            for agent in self._agents.values():
                # Count by status
                status = agent.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Count by capabilities
                for capability in agent.capabilities:
                    cap_name = capability.name
                    capability_counts[cap_name] = capability_counts.get(cap_name, 0) + 1
            
            # Calculate health statistics
            healthy_agents = sum(1 for agent in self._agents.values() 
                               if agent.is_healthy(self._heartbeat_timeout))
            
            return {
                "total_agents": total_agents,
                "healthy_agents": healthy_agents,
                "unhealthy_agents": total_agents - healthy_agents,
                "status_breakdown": status_counts,
                "capability_breakdown": capability_counts,
                "total_capabilities": len(self._capabilities)
            }
    
    async def select_best_agent(self, 
                              capability: str,
                              load_balancing: bool = True) -> Optional[RegisteredAgent]:
        """
        Select the best agent for a capability based on availability and performance.
        
        Args:
            capability: The required capability
            load_balancing: Whether to prefer agents with lower task counts
            
        Returns:
            The best available agent, or None if no suitable agent found
        """
        candidates = await self.find_agents_by_capability(capability)
        
        if not candidates:
            return None
        
        if load_balancing:
            # Prefer agents with lower task counts and higher success rates
            candidates.sort(
                key=lambda a: (
                    a.status != AgentStatus.IDLE,  # Idle agents first
                    a.task_count,  # Lower task count preferred
                    -a.get_success_rate()  # Higher success rate preferred
                )
            )
        
        best_agent = candidates[0]
        logger.debug(f"Selected agent: {best_agent.name} for capability '{capability}'")
        return best_agent
    
    async def record_task_start(self, agent_id: str) -> bool:
        """Record that an agent has started a task."""
        with self._lock:
            agent = self._agents.get(agent_id)
            if agent:
                agent.increment_task_count()
                agent.status = AgentStatus.BUSY
                agent.update_heartbeat()
                return True
            return False
    
    async def record_task_success(self, agent_id: str) -> bool:
        """Record that an agent has completed a task successfully."""
        with self._lock:
            agent = self._agents.get(agent_id)
            if agent:
                agent.increment_success_count()
                agent.status = AgentStatus.IDLE
                agent.update_heartbeat()
                return True
            return False
    
    async def record_task_error(self, agent_id: str) -> bool:
        """Record that an agent encountered an error during a task."""
        with self._lock:
            agent = self._agents.get(agent_id)
            if agent:
                agent.increment_error_count()
                agent.status = AgentStatus.ERROR
                agent.update_heartbeat()
                return True
            return False
    
    async def _periodic_cleanup(self) -> None:
        """Periodically clean up unhealthy agents."""
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                await self._cleanup_unhealthy_agents()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
    
    async def _cleanup_unhealthy_agents(self) -> int:
        """Remove agents that haven't sent heartbeats within the timeout."""
        unhealthy_agents = []
        
        with self._lock:
            for agent_id, agent in self._agents.items():
                if not agent.is_healthy(self._heartbeat_timeout):
                    unhealthy_agents.append(agent_id)
        
        # Remove unhealthy agents
        for agent_id in unhealthy_agents:
            await self.unregister_agent(agent_id)
        
        if unhealthy_agents:
            logger.info(f"Cleaned up {len(unhealthy_agents)} unhealthy agents")
        
        return len(unhealthy_agents)
    
    async def shutdown(self) -> None:
        """Shutdown the registry and cleanup resources."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        logger.info("AgentRegistry shutdown complete")