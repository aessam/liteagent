"""
Asynchronous coordination system for multi-agent execution.

This module provides coordination mechanisms for:
- Parallel agent execution with task management
- Conditional waiting and synchronization
- Agent handoff and workflow coordination
- Resource management and rate limiting coordination
"""

import asyncio
import time
import uuid
from typing import Any, Dict, List, Optional, Callable, Union, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentTask:
    """Represents a task to be executed by an agent."""
    task_id: str
    agent_id: str
    capability: str
    input_data: Any
    priority: int = 0
    timeout: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    metadata: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def duration(self) -> Optional[float]:
        """Calculate task duration if completed."""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    agent_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    duration: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class HandoffContext:
    """Context for agent handoff operations."""
    from_agent_id: str
    to_agent_id: str
    context_data: Any
    handoff_reason: str
    timestamp: float = field(default_factory=time.time)
    metadata: Optional[Dict[str, Any]] = None


class WaitCondition:
    """Base class for wait conditions."""
    
    def __init__(self, condition_id: str):
        self.condition_id = condition_id
        self.created_at = time.time()
    
    async def check(self, coordinator: 'AsyncCoordinator') -> bool:
        """Check if the condition is met."""
        raise NotImplementedError


class TaskCompletionCondition(WaitCondition):
    """Wait for specific tasks to complete."""
    
    def __init__(self, task_ids: List[str]):
        super().__init__(f"task_completion_{uuid.uuid4()}")
        self.task_ids = set(task_ids)
    
    async def check(self, coordinator: 'AsyncCoordinator') -> bool:
        """Check if all specified tasks are completed."""
        completed_tasks = set()
        for task_id in self.task_ids:
            result = coordinator.get_task_result(task_id)
            if result and result.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                completed_tasks.add(task_id)
        
        return completed_tasks == self.task_ids


class KnowledgeCondition(WaitCondition):
    """Wait for specific knowledge to appear on the blackboard."""
    
    def __init__(self, blackboard, knowledge_key: str):
        super().__init__(f"knowledge_{knowledge_key}")
        self.blackboard = blackboard
        self.knowledge_key = knowledge_key
    
    async def check(self, coordinator: 'AsyncCoordinator') -> bool:
        """Check if the knowledge exists on the blackboard."""
        knowledge = await self.blackboard.read_knowledge(self.knowledge_key)
        return knowledge is not None


class AgentStatusCondition(WaitCondition):
    """Wait for agents to reach specific statuses."""
    
    def __init__(self, registry, agent_status_requirements: Dict[str, str]):
        super().__init__(f"agent_status_{uuid.uuid4()}")
        self.registry = registry
        self.agent_status_requirements = agent_status_requirements
    
    async def check(self, coordinator: 'AsyncCoordinator') -> bool:
        """Check if all agents have reached required statuses."""
        for agent_id, required_status in self.agent_status_requirements.items():
            current_status = await self.registry.get_agent_status(agent_id)
            if not current_status or current_status.value != required_status:
                return False
        return True


class AsyncCoordinator:
    """
    Asynchronous coordination system for multi-agent execution.
    
    Features:
    - Parallel task execution with priority queuing
    - Conditional waiting and synchronization
    - Agent handoff coordination
    - Resource management integration
    - Comprehensive error handling and recovery
    """
    
    def __init__(self, 
                 registry,
                 blackboard,
                 max_concurrent_tasks: int = 10,
                 default_timeout: float = 300.0):
        """
        Initialize the async coordinator.
        
        Args:
            registry: AgentRegistry instance for agent discovery
            blackboard: Blackboard instance for shared knowledge
            max_concurrent_tasks: Maximum number of concurrent tasks
            default_timeout: Default timeout for tasks in seconds
        """
        self.registry = registry
        self.blackboard = blackboard
        self.max_concurrent_tasks = max_concurrent_tasks
        self.default_timeout = default_timeout
        
        self._task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._task_results: Dict[str, TaskResult] = {}
        self._wait_conditions: Dict[str, WaitCondition] = {}
        self._handoff_history: List[HandoffContext] = []
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
        self._shutdown_event = asyncio.Event()
        self._worker_tasks: List[asyncio.Task] = []
        
        logger.info(f"AsyncCoordinator initialized with {max_concurrent_tasks} max concurrent tasks")
    
    async def start(self) -> None:
        """Start the coordinator workers."""
        # Start worker tasks
        for i in range(self.max_concurrent_tasks):
            worker_task = asyncio.create_task(self._worker_loop(f"worker-{i}"))
            self._worker_tasks.append(worker_task)
        
        logger.info(f"Started {len(self._worker_tasks)} coordinator workers")
    
    async def shutdown(self) -> None:
        """Shutdown the coordinator and cleanup resources."""
        self._shutdown_event.set()
        
        # Cancel all running tasks
        for task in self._running_tasks.values():
            task.cancel()
        
        # Wait for workers to finish
        if self._worker_tasks:
            await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        
        # Cleanup executor
        self._executor.shutdown(wait=True)
        
        logger.info("AsyncCoordinator shutdown complete")
    
    async def execute_task(self, task: AgentTask) -> str:
        """
        Submit a task for execution.
        
        Args:
            task: The AgentTask to execute
            
        Returns:
            The task ID for tracking
        """
        # Assign priority (lower number = higher priority)
        priority = task.priority
        
        # Add to queue
        await self._task_queue.put((priority, time.time(), task))
        
        logger.debug(f"Task queued: {task.task_id} for agent {task.agent_id}")
        return task.task_id
    
    async def execute_agents_parallel(self, 
                                    tasks: List[AgentTask],
                                    wait_for_all: bool = True) -> Dict[str, TaskResult]:
        """
        Execute multiple agent tasks in parallel.
        
        Args:
            tasks: List of tasks to execute
            wait_for_all: Whether to wait for all tasks to complete
            
        Returns:
            Dictionary mapping task IDs to TaskResults
        """
        task_ids = []
        
        # Submit all tasks
        for task in tasks:
            task_id = await self.execute_task(task)
            task_ids.append(task_id)
        
        logger.info(f"Submitted {len(tasks)} tasks for parallel execution")
        
        if wait_for_all:
            # Wait for all tasks to complete
            condition = TaskCompletionCondition(task_ids)
            await self.wait_for_condition(condition)
        
        # Collect results
        results = {}
        for task_id in task_ids:
            result = self.get_task_result(task_id)
            if result:
                results[task_id] = result
        
        return results
    
    async def wait_for_condition(self, 
                               condition: WaitCondition,
                               timeout: Optional[float] = None,
                               check_interval: float = 1.0) -> bool:
        """
        Wait for a specific condition to be met.
        
        Args:
            condition: The WaitCondition to wait for
            timeout: Maximum time to wait (None for no timeout)
            check_interval: How often to check the condition
            
        Returns:
            True if condition was met, False if timeout occurred
        """
        start_time = time.time()
        timeout_time = start_time + timeout if timeout else None
        
        # Store condition for potential cancellation
        self._wait_conditions[condition.condition_id] = condition
        
        try:
            while True:
                # Check if condition is met
                if await condition.check(self):
                    logger.debug(f"Wait condition met: {condition.condition_id}")
                    return True
                
                # Check timeout
                if timeout_time and time.time() >= timeout_time:
                    logger.warning(f"Wait condition timeout: {condition.condition_id}")
                    return False
                
                # Wait before next check
                await asyncio.sleep(check_interval)
                
        finally:
            # Clean up condition
            self._wait_conditions.pop(condition.condition_id, None)
    
    async def coordinate_handoff(self, 
                               from_agent_id: str,
                               to_agent_id: str,
                               context: Any,
                               handoff_reason: str = "workflow_continuation") -> bool:
        """
        Coordinate handoff between agents.
        
        Args:
            from_agent_id: ID of the agent handing off
            to_agent_id: ID of the agent receiving the handoff
            context: Context data to pass between agents
            handoff_reason: Reason for the handoff
            
        Returns:
            True if handoff was successful, False otherwise
        """
        # Verify both agents exist and are available
        from_agent = await self.registry.get_agent(from_agent_id)
        to_agent = await self.registry.get_agent(to_agent_id)
        
        if not from_agent or not to_agent:
            logger.error(f"Handoff failed: Agent not found (from: {from_agent_id}, to: {to_agent_id})")
            return False
        
        # Create handoff context
        handoff_context = HandoffContext(
            from_agent_id=from_agent_id,
            to_agent_id=to_agent_id,
            context_data=context,
            handoff_reason=handoff_reason
        )
        
        try:
            # Store handoff context on blackboard
            handoff_key = f"handoff_{from_agent_id}_{to_agent_id}_{int(time.time())}"
            await self.blackboard.write_knowledge(
                key=handoff_key,
                data=handoff_context,
                agent_id="coordinator",
                category="handoffs"
            )
            
            # Update agent statuses
            await self.registry.update_agent_status(from_agent_id, 
                                                  self.registry._agents[from_agent_id].status)
            await self.registry.update_agent_status(to_agent_id, 
                                                  self.registry._agents[to_agent_id].status)
            
            # Record handoff
            self._handoff_history.append(handoff_context)
            
            logger.info(f"Handoff coordinated: {from_agent_id} -> {to_agent_id} ({handoff_reason})")
            return True
            
        except Exception as e:
            logger.error(f"Handoff coordination failed: {e}")
            return False
    
    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """Get the result of a task by ID."""
        return self._task_results.get(task_id)
    
    def get_running_tasks(self) -> List[str]:
        """Get list of currently running task IDs."""
        return list(self._running_tasks.keys())
    
    def get_coordination_stats(self) -> Dict[str, Any]:
        """Get coordination statistics."""
        total_tasks = len(self._task_results)
        completed_tasks = sum(1 for r in self._task_results.values() 
                            if r.status == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for r in self._task_results.values() 
                         if r.status == TaskStatus.FAILED)
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "running_tasks": len(self._running_tasks),
            "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0.0,
            "handoff_count": len(self._handoff_history),
            "active_conditions": len(self._wait_conditions)
        }
    
    async def _worker_loop(self, worker_id: str) -> None:
        """Main worker loop for processing tasks."""
        logger.debug(f"Worker {worker_id} started")
        
        while not self._shutdown_event.is_set():
            try:
                # Get next task with timeout
                try:
                    priority, timestamp, task = await asyncio.wait_for(
                        self._task_queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue
                
                # Execute the task
                await self._execute_task(task, worker_id)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in worker {worker_id}: {e}")
        
        logger.debug(f"Worker {worker_id} stopped")
    
    async def _execute_task(self, task: AgentTask, worker_id: str) -> None:
        """Execute a single task."""
        task_id = task.task_id
        logger.debug(f"Worker {worker_id} executing task {task_id}")
        
        # Find the agent
        agent = await self.registry.get_agent(task.agent_id)
        if not agent:
            result = TaskResult(
                task_id=task_id,
                agent_id=task.agent_id,
                status=TaskStatus.FAILED,
                error="Agent not found"
            )
            self._task_results[task_id] = result
            return
        
        # Record task start
        await self.registry.record_task_start(task.agent_id)
        task.started_at = time.time()
        
        try:
            # Create async task for execution
            execution_task = asyncio.create_task(
                self._call_agent(agent.agent_instance, task)
            )
            self._running_tasks[task_id] = execution_task
            
            # Wait for completion with timeout
            timeout = task.timeout or self.default_timeout
            try:
                result_data = await asyncio.wait_for(execution_task, timeout=timeout)
                
                # Success
                task.completed_at = time.time()
                await self.registry.record_task_success(task.agent_id)
                
                result = TaskResult(
                    task_id=task_id,
                    agent_id=task.agent_id,
                    status=TaskStatus.COMPLETED,
                    result=result_data,
                    duration=task.duration()
                )
                
            except asyncio.TimeoutError:
                # Timeout
                execution_task.cancel()
                task.completed_at = time.time()
                await self.registry.record_task_error(task.agent_id)
                
                result = TaskResult(
                    task_id=task_id,
                    agent_id=task.agent_id,
                    status=TaskStatus.FAILED,
                    error=f"Task timeout after {timeout} seconds",
                    duration=task.duration()
                )
                
        except Exception as e:
            # Error
            task.completed_at = time.time()
            await self.registry.record_task_error(task.agent_id)
            
            result = TaskResult(
                task_id=task_id,
                agent_id=task.agent_id,
                status=TaskStatus.FAILED,
                error=str(e),
                duration=task.duration()
            )
            
        finally:
            # Cleanup
            self._running_tasks.pop(task_id, None)
        
        # Store result
        self._task_results[task_id] = result
        logger.debug(f"Task {task_id} completed with status {result.status}")
    
    async def _call_agent(self, agent_instance, task: AgentTask) -> Any:
        """Call the agent with the task input."""
        # This is a simplified version - in practice, you'd need to
        # properly format the input based on the agent's expected interface
        if hasattr(agent_instance, 'chat'):
            return agent_instance.chat(str(task.input_data))
        elif hasattr(agent_instance, 'execute'):
            return await agent_instance.execute(task.input_data)
        else:
            raise ValueError(f"Agent {task.agent_id} has no compatible execution method")