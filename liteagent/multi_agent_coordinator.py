"""
Multi-agent coordinator that integrates blackboard, registry, and async execution.

This module provides the main coordination system that brings together:
- Blackboard pattern for shared knowledge
- Agent registry for discovery and capability matching
- Asynchronous execution for parallel coordination
- Integration with ForkedAgents v2 for rate limiting
"""

import asyncio
import time
import uuid
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass
import logging

from .blackboard import Blackboard, KnowledgeItem
from .agent_registry import AgentRegistry, AgentCapability, AgentStatus
from .async_executor import AsyncCoordinator, AgentTask, TaskResult, TaskStatus
from .async_executor import WaitCondition, TaskCompletionCondition, KnowledgeCondition

logger = logging.getLogger(__name__)


@dataclass
class MultiAgentRequest:
    """Represents a request that may require multiple agents."""
    request_id: str
    description: str
    required_capabilities: List[str]
    input_data: Any
    priority: int = 0
    timeout: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class MultiAgentResponse:
    """Response from a multi-agent coordination."""
    request_id: str
    status: str  # "completed", "failed", "partial"
    results: Dict[str, Any]
    agent_contributions: Dict[str, Any]
    execution_time: float
    error: Optional[str] = None


class MultiAgentCoordinator:
    """
    Main coordinator for multi-agent collaboration using Blackboard pattern.
    
    Features:
    - Unified interface for multi-agent requests
    - Automatic capability-based agent selection
    - Blackboard-mediated agent collaboration
    - Integration with ForkedAgents v2 rate limiting
    - Comprehensive workflow orchestration
    """
    
    def __init__(self, 
                 max_concurrent_tasks: int = 10,
                 blackboard_ttl: Optional[float] = 3600.0,  # 1 hour
                 agent_heartbeat_timeout: float = 60.0,
                 default_task_timeout: float = 300.0):
        """
        Initialize the multi-agent coordinator.
        
        Args:
            max_concurrent_tasks: Maximum concurrent tasks across all agents
            blackboard_ttl: Time-to-live for blackboard knowledge items
            agent_heartbeat_timeout: Timeout for agent heartbeats
            default_task_timeout: Default timeout for individual tasks
        """
        # Initialize core components
        self.blackboard = Blackboard(default_ttl=blackboard_ttl)
        self.registry = AgentRegistry(heartbeat_timeout=agent_heartbeat_timeout)
        self.async_coordinator = AsyncCoordinator(
            registry=self.registry,
            blackboard=self.blackboard,
            max_concurrent_tasks=max_concurrent_tasks,
            default_timeout=default_task_timeout
        )
        
        # State management
        self._active_requests: Dict[str, MultiAgentRequest] = {}
        self._request_results: Dict[str, MultiAgentResponse] = {}
        self._is_started = False
        
        logger.info("MultiAgentCoordinator initialized")
    
    async def start(self) -> None:
        """Start the coordinator and all its components."""
        if self._is_started:
            return
        
        await self.async_coordinator.start()
        self._is_started = True
        
        logger.info("MultiAgentCoordinator started")
    
    async def shutdown(self) -> None:
        """Shutdown the coordinator and cleanup resources."""
        if not self._is_started:
            return
        
        await self.async_coordinator.shutdown()
        await self.registry.shutdown()
        self._is_started = False
        
        logger.info("MultiAgentCoordinator shutdown complete")
    
    async def register_agent(self, 
                           agent: Any,
                           capabilities: List[Union[str, AgentCapability]],
                           name: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Register an agent with the coordinator.
        
        Args:
            agent: The LiteAgent instance to register
            capabilities: List of capabilities (strings or AgentCapability objects)
            name: Optional human-readable name for the agent
            metadata: Optional metadata for the agent
            
        Returns:
            The assigned agent ID
        """
        agent_id = await self.registry.register_agent(
            agent=agent,
            capabilities=capabilities,
            name=name,
            metadata=metadata
        )
        
        # Write agent registration to blackboard for visibility
        await self.blackboard.write_knowledge(
            key=f"agent_registered_{agent_id}",
            data={
                "agent_id": agent_id,
                "name": name or f"Agent-{agent_id[:8]}",
                "capabilities": [cap.name if isinstance(cap, AgentCapability) else cap 
                              for cap in capabilities],
                "registration_time": time.time()
            },
            agent_id="coordinator",
            category="agent_lifecycle"
        )
        
        return agent_id
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the coordinator."""
        success = await self.registry.unregister_agent(agent_id)
        
        if success:
            # Write agent unregistration to blackboard
            await self.blackboard.write_knowledge(
                key=f"agent_unregistered_{agent_id}",
                data={
                    "agent_id": agent_id,
                    "unregistration_time": time.time()
                },
                agent_id="coordinator",
                category="agent_lifecycle"
            )
        
        return success
    
    async def execute_multi_agent_request(self, request: MultiAgentRequest) -> MultiAgentResponse:
        """
        Execute a request that may require coordination of multiple agents.
        
        Args:
            request: The MultiAgentRequest to process
            
        Returns:
            MultiAgentResponse with results from all involved agents
        """
        start_time = time.time()
        request_id = request.request_id
        
        # Store active request
        self._active_requests[request_id] = request
        
        logger.info(f"Starting multi-agent request: {request_id}")
        
        try:
            # Write request to blackboard for agent visibility
            await self.blackboard.write_knowledge(
                key=f"request_{request_id}",
                data={
                    "request_id": request_id,
                    "description": request.description,
                    "required_capabilities": request.required_capabilities,
                    "input_data": request.input_data,
                    "start_time": start_time
                },
                agent_id="coordinator",
                category="requests"
            )
            
            # Find agents for each required capability
            agent_assignments = {}
            for capability in request.required_capabilities:
                best_agent = await self.registry.select_best_agent(capability)
                if best_agent:
                    agent_assignments[capability] = best_agent
                else:
                    logger.warning(f"No agent found for capability: {capability}")
            
            if not agent_assignments:
                # No agents available
                response = MultiAgentResponse(
                    request_id=request_id,
                    status="failed",
                    results={},
                    agent_contributions={},
                    execution_time=time.time() - start_time,
                    error="No suitable agents found for required capabilities"
                )
                self._request_results[request_id] = response
                return response
            
            # Create tasks for each agent
            tasks = []
            for capability, agent in agent_assignments.items():
                task = AgentTask(
                    task_id=f"{request_id}_{capability}_{uuid.uuid4()}",
                    agent_id=agent.agent_id,
                    capability=capability,
                    input_data={
                        "request_id": request_id,
                        "capability": capability,
                        "input_data": request.input_data,
                        "description": request.description
                    },
                    priority=request.priority,
                    timeout=request.timeout,
                    metadata={"request_id": request_id, "capability": capability}
                )
                tasks.append(task)
            
            # Execute tasks in parallel
            task_results = await self.async_coordinator.execute_agents_parallel(tasks)
            
            # Collect results and contributions
            results = {}
            agent_contributions = {}
            has_failures = False
            
            for task_id, task_result in task_results.items():
                capability = task_result.metadata.get("capability") if task_result.metadata else "unknown"
                
                if task_result.status == TaskStatus.COMPLETED:
                    results[capability] = task_result.result
                    agent_contributions[task_result.agent_id] = {
                        "capability": capability,
                        "result": task_result.result,
                        "duration": task_result.duration
                    }
                else:
                    has_failures = True
                    results[capability] = None
                    agent_contributions[task_result.agent_id] = {
                        "capability": capability,
                        "error": task_result.error,
                        "duration": task_result.duration
                    }
            
            # Write results to blackboard
            await self.blackboard.write_knowledge(
                key=f"request_results_{request_id}",
                data={
                    "request_id": request_id,
                    "results": results,
                    "agent_contributions": agent_contributions,
                    "completion_time": time.time()
                },
                agent_id="coordinator",
                category="request_results"
            )
            
            # Create response
            execution_time = time.time() - start_time
            status = "completed" if not has_failures else "partial" if results else "failed"
            
            response = MultiAgentResponse(
                request_id=request_id,
                status=status,
                results=results,
                agent_contributions=agent_contributions,
                execution_time=execution_time
            )
            
            self._request_results[request_id] = response
            logger.info(f"Multi-agent request completed: {request_id} ({status}) in {execution_time:.2f}s")
            return response
            
        except Exception as e:
            # Handle execution error
            execution_time = time.time() - start_time
            error_msg = f"Multi-agent execution failed: {str(e)}"
            
            response = MultiAgentResponse(
                request_id=request_id,
                status="failed",
                results={},
                agent_contributions={},
                execution_time=execution_time,
                error=error_msg
            )
            
            self._request_results[request_id] = response
            logger.error(f"Multi-agent request failed: {request_id} - {error_msg}")
            return response
            
        finally:
            # Cleanup active request
            self._active_requests.pop(request_id, None)
    
    async def create_software_qa_workflow(self, 
                                        code_input: str,
                                        project_context: Optional[Dict[str, Any]] = None) -> MultiAgentResponse:
        """
        Create a Software QA workflow using specialized agents.
        
        This implements the primary success metric from the task specification.
        
        Args:
            code_input: The code to analyze and create tests for
            project_context: Optional context about the project
            
        Returns:
            MultiAgentResponse with comprehensive test results
        """
        request_id = f"software_qa_{uuid.uuid4()}"
        
        request = MultiAgentRequest(
            request_id=request_id,
            description="Software QA multi-agent workflow: break down code into dimensions, create testing categories, generate comprehensive tests",
            required_capabilities=[
                "code_analysis",
                "test_category_creation", 
                "unit_test_generation",
                "integration_test_generation",
                "requirement_test_generation",
                "conceptual_test_generation"
            ],
            input_data={
                "code": code_input,
                "project_context": project_context or {}
            },
            priority=1,  # High priority for QA workflows
            timeout=600.0  # 10 minutes for comprehensive analysis
        )
        
        logger.info(f"Starting Software QA workflow for request {request_id}")
        return await self.execute_multi_agent_request(request)
    
    async def wait_for_knowledge(self, 
                               knowledge_key: str,
                               timeout: Optional[float] = None) -> Optional[KnowledgeItem]:
        """
        Wait for specific knowledge to appear on the blackboard.
        
        Args:
            knowledge_key: The knowledge key to wait for
            timeout: Maximum time to wait
            
        Returns:
            The KnowledgeItem if found, None if timeout
        """
        condition = KnowledgeCondition(self.blackboard, knowledge_key)
        success = await self.async_coordinator.wait_for_condition(condition, timeout)
        
        if success:
            return await self.blackboard.read_knowledge(knowledge_key)
        return None
    
    async def coordinate_agent_handoff(self, 
                                     from_agent_id: str,
                                     to_agent_id: str,
                                     context: Any,
                                     handoff_reason: str = "workflow_continuation") -> bool:
        """
        Coordinate handoff between agents through the blackboard.
        
        Args:
            from_agent_id: ID of the agent handing off
            to_agent_id: ID of the agent receiving handoff
            context: Context data to pass
            handoff_reason: Reason for handoff
            
        Returns:
            True if handoff was successful
        """
        return await self.async_coordinator.coordinate_handoff(
            from_agent_id=from_agent_id,
            to_agent_id=to_agent_id,
            context=context,
            handoff_reason=handoff_reason
        )
    
    async def get_available_capabilities(self) -> List[str]:
        """Get all capabilities available across registered agents."""
        return await self.registry.get_available_capabilities()
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status across all components."""
        blackboard_stats = await self.blackboard.get_stats()
        registry_stats = await self.registry.get_registry_stats()
        coordination_stats = self.async_coordinator.get_coordination_stats()
        
        return {
            "coordinator": {
                "active_requests": len(self._active_requests),
                "completed_requests": len(self._request_results),
                "is_started": self._is_started
            },
            "blackboard": blackboard_stats,
            "registry": registry_stats,
            "coordination": coordination_stats,
            "timestamp": time.time()
        }
    
    async def subscribe_to_knowledge_updates(self, 
                                           pattern: str,
                                           callback: Callable[[KnowledgeItem], None],
                                           agent_id: str,
                                           categories: Optional[List[str]] = None) -> str:
        """
        Subscribe to knowledge updates on the blackboard.
        
        Args:
            pattern: Regex pattern to match knowledge keys
            callback: Function to call on updates
            agent_id: ID of the subscribing agent
            categories: Optional categories to filter by
            
        Returns:
            Subscription ID
        """
        return await self.blackboard.subscribe_to_pattern(
            pattern=pattern,
            callback=callback,
            agent_id=agent_id,
            categories=categories
        )
    
    async def unsubscribe_from_knowledge_updates(self, subscription_id: str) -> bool:
        """Unsubscribe from knowledge updates."""
        return await self.blackboard.unsubscribe(subscription_id)
    
    def get_request_result(self, request_id: str) -> Optional[MultiAgentResponse]:
        """Get the result of a completed multi-agent request."""
        return self._request_results.get(request_id)
    
    async def cleanup_expired_data(self) -> Dict[str, int]:
        """Clean up expired data across all components."""
        blackboard_cleaned = await self.blackboard.cleanup_expired()
        registry_cleaned = await self.registry._cleanup_unhealthy_agents()
        
        return {
            "blackboard_items_cleaned": blackboard_cleaned,
            "unhealthy_agents_cleaned": registry_cleaned
        }