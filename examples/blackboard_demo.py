#!/usr/bin/env python3
"""
Simple Blackboard Pattern Demonstration

This script demonstrates the core functionality of the new multi-agent
collaboration system without requiring API keys. It shows:

1. Blackboard shared workspace functionality
2. Agent registry and discovery
3. Asynchronous coordination
4. Basic multi-agent workflow

Usage:
    python examples/blackboard_demo.py
"""

import asyncio
import time
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from liteagent.blackboard import Blackboard, KnowledgeItem
from liteagent.agent_registry import AgentRegistry, AgentCapability, AgentStatus
from liteagent.async_executor import AsyncCoordinator, AgentTask, TaskStatus
from liteagent.multi_agent_coordinator import MultiAgentCoordinator, MultiAgentRequest


class MockAgent:
    """Mock agent for demonstration purposes."""
    
    def __init__(self, name: str, processing_time: float = 0.1):
        self.name = name
        self.processing_time = processing_time
    
    def chat(self, message: str) -> str:
        """Simulate agent processing."""
        time.sleep(self.processing_time)
        return f"[{self.name}] Processed: {message}"


async def demonstrate_blackboard():
    """Demonstrate blackboard functionality."""
    print("🔲 BLACKBOARD DEMONSTRATION")
    print("-" * 40)
    
    # Create blackboard
    blackboard = Blackboard()
    
    # Write some knowledge
    print("📝 Writing knowledge to blackboard...")
    await blackboard.write_knowledge(
        key="project_info",
        data={"name": "LiteAgent", "version": "0.1.0", "type": "AI Framework"},
        agent_id="demo_agent",
        category="project"
    )
    
    await blackboard.write_knowledge(
        key="task_status",
        data={"current_task": "multi_agent_demo", "progress": 50},
        agent_id="demo_agent",
        category="status"
    )
    
    # Read knowledge
    print("📖 Reading knowledge from blackboard...")
    project_info = await blackboard.read_knowledge("project_info")
    if project_info:
        print(f"   Found: {project_info.data}")
    
    # Get by category
    print("📂 Getting knowledge by category...")
    project_items = await blackboard.get_knowledge_by_category("project")
    print(f"   Project category has {len(project_items)} items")
    
    # Subscribe to updates
    notifications = []
    def callback(item: KnowledgeItem):
        notifications.append(f"Update: {item.key} = {item.data}")
    
    print("🔔 Subscribing to updates...")
    subscription_id = await blackboard.subscribe_to_pattern(
        pattern="task_.*",
        callback=callback,
        agent_id="subscriber"
    )
    
    # Write more knowledge (should trigger notification)
    await blackboard.write_knowledge(
        key="task_completion",
        data={"status": "completed", "duration": 2.5},
        agent_id="demo_agent",
        category="status"
    )
    
    # Check notifications
    await asyncio.sleep(0.1)
    print(f"📬 Received {len(notifications)} notifications:")
    for notification in notifications:
        print(f"   {notification}")
    
    # Get stats
    stats = await blackboard.get_stats()
    print(f"📊 Blackboard stats: {stats['total_items']} items, {stats['categories']} categories")
    
    # Cleanup
    await blackboard.unsubscribe(subscription_id)
    print("✅ Blackboard demonstration complete")
    print()


async def demonstrate_agent_registry():
    """Demonstrate agent registry functionality."""
    print("📋 AGENT REGISTRY DEMONSTRATION")
    print("-" * 40)
    
    # Create registry
    registry = AgentRegistry()
    
    # Create mock agents
    code_agent = MockAgent("CodeAnalyzer")
    test_agent = MockAgent("TestGenerator")
    doc_agent = MockAgent("DocumentationWriter")
    
    # Register agents
    print("📝 Registering agents...")
    code_id = await registry.register_agent(
        agent=code_agent,
        capabilities=[
            AgentCapability("code_analysis", "Analyze code structure and complexity"),
            AgentCapability("static_analysis", "Perform static code analysis")
        ],
        name="CodeAnalyzer"
    )
    
    test_id = await registry.register_agent(
        agent=test_agent,
        capabilities=["unit_testing", "test_generation"],
        name="TestGenerator"
    )
    
    doc_id = await registry.register_agent(
        agent=doc_agent,
        capabilities=["documentation", "markdown_generation"],
        name="DocumentationWriter"
    )
    
    print(f"   Registered {len([code_id, test_id, doc_id])} agents")
    
    # Find agents by capability
    print("🔍 Finding agents by capability...")
    code_agents = await registry.find_agents_by_capability("code_analysis")
    test_agents = await registry.find_agents_by_capability("testing")  # Partial match
    
    print(f"   Found {len(code_agents)} code analysis agents")
    print(f"   Found {len(test_agents)} testing agents")
    
    # Update agent status
    print("📊 Managing agent status...")
    await registry.update_agent_status(code_id, AgentStatus.BUSY)
    await registry.record_task_start(test_id)
    await registry.record_task_success(test_id)
    
    # Get registry stats
    stats = await registry.get_registry_stats()
    print(f"📈 Registry stats: {stats['total_agents']} agents, {stats['total_capabilities']} capabilities")
    print(f"   Status breakdown: {stats['status_breakdown']}")
    
    # Select best agent
    best_agent = await registry.select_best_agent("code_analysis")
    if best_agent:
        print(f"🏆 Best agent for code analysis: {best_agent.name}")
    
    # Cleanup
    await registry.shutdown()
    print("✅ Agent registry demonstration complete")
    print()
    
    return registry


async def demonstrate_async_coordination():
    """Demonstrate asynchronous coordination."""
    print("⚡ ASYNC COORDINATION DEMONSTRATION")
    print("-" * 40)
    
    # Create components
    registry = AgentRegistry()
    blackboard = Blackboard()
    coordinator = AsyncCoordinator(registry, blackboard, max_concurrent_tasks=3)
    
    # Start coordinator
    await coordinator.start()
    
    # Register mock agents
    agent1 = MockAgent("Agent1", 0.1)
    agent2 = MockAgent("Agent2", 0.2)
    agent3 = MockAgent("Agent3", 0.15)
    
    id1 = await registry.register_agent(agent1, ["task_a"], name="Agent1")
    id2 = await registry.register_agent(agent2, ["task_b"], name="Agent2")
    id3 = await registry.register_agent(agent3, ["task_c"], name="Agent3")
    
    print("📝 Creating tasks...")
    
    # Create tasks
    tasks = [
        AgentTask(
            task_id="task_1",
            agent_id=id1,
            capability="task_a",
            input_data="Process data A"
        ),
        AgentTask(
            task_id="task_2", 
            agent_id=id2,
            capability="task_b",
            input_data="Process data B"
        ),
        AgentTask(
            task_id="task_3",
            agent_id=id3,
            capability="task_c",
            input_data="Process data C"
        )
    ]
    
    # Execute tasks in parallel
    print("🚀 Executing tasks in parallel...")
    start_time = time.time()
    results = await coordinator.execute_agents_parallel(tasks)
    duration = time.time() - start_time
    
    print(f"⏱️ Completed {len(results)} tasks in {duration:.2f} seconds")
    
    # Check results
    successful_tasks = sum(1 for r in results.values() if r.status == TaskStatus.COMPLETED)
    print(f"✅ {successful_tasks}/{len(results)} tasks completed successfully")
    
    # Get coordination stats
    stats = coordinator.get_coordination_stats()
    print(f"📊 Coordination stats: {stats['success_rate']:.1%} success rate")
    
    # Cleanup
    await coordinator.shutdown()
    await registry.shutdown()
    print("✅ Async coordination demonstration complete")
    print()


async def demonstrate_multi_agent_system():
    """Demonstrate the complete multi-agent system."""
    print("🤖 MULTI-AGENT SYSTEM DEMONSTRATION")
    print("-" * 40)
    
    # Create coordinator
    coordinator = MultiAgentCoordinator(
        max_concurrent_tasks=5,
        blackboard_ttl=300.0,  # 5 minutes
        default_task_timeout=10.0
    )
    
    await coordinator.start()
    
    # Create specialized mock agents
    print("🏭 Creating specialized agents...")
    
    agents = {
        "analyzer": MockAgent("CodeAnalyzer", 0.1),
        "tester": MockAgent("TestGenerator", 0.15),
        "optimizer": MockAgent("Optimizer", 0.12),
        "documenter": MockAgent("Documenter", 0.08)
    }
    
    # Register agents with capabilities
    agent_ids = {}
    
    agent_ids["analyzer"] = await coordinator.register_agent(
        agent=agents["analyzer"],
        capabilities=[
            AgentCapability("code_analysis", "Analyze code structure"),
            AgentCapability("complexity_analysis", "Analyze code complexity")
        ],
        name="CodeAnalyzer"
    )
    
    agent_ids["tester"] = await coordinator.register_agent(
        agent=agents["tester"],
        capabilities=[
            AgentCapability("test_generation", "Generate unit tests"),
            AgentCapability("test_validation", "Validate test coverage")
        ],
        name="TestGenerator"
    )
    
    agent_ids["optimizer"] = await coordinator.register_agent(
        agent=agents["optimizer"],
        capabilities=[
            AgentCapability("performance_optimization", "Optimize performance"),
            AgentCapability("code_optimization", "Optimize code structure")
        ],
        name="Optimizer"
    )
    
    agent_ids["documenter"] = await coordinator.register_agent(
        agent=agents["documenter"],
        capabilities=[
            AgentCapability("documentation_generation", "Generate documentation"),
            AgentCapability("api_documentation", "Document APIs")
        ],
        name="Documenter"
    )
    
    print(f"✅ Registered {len(agent_ids)} specialized agents")
    
    # Create a multi-agent request
    print("📋 Creating multi-agent request...")
    
    request = MultiAgentRequest(
        request_id="demo_request_001",
        description="Comprehensive code processing workflow",
        required_capabilities=[
            "code_analysis",
            "test_generation", 
            "performance_optimization",
            "documentation_generation"
        ],
        input_data={
            "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
            "context": "Algorithm optimization task"
        },
        priority=1
    )
    
    # Execute the request
    print("🚀 Executing multi-agent request...")
    start_time = time.time()
    response = await coordinator.execute_multi_agent_request(request)
    duration = time.time() - start_time
    
    # Display results
    print(f"📊 REQUEST RESULTS")
    print(f"   Status: {response.status}")
    print(f"   Execution Time: {duration:.2f} seconds")
    print(f"   Capabilities Processed: {len(response.results)}")
    
    if response.agent_contributions:
        print("👥 Agent Contributions:")
        for agent_id, contribution in response.agent_contributions.items():
            capability = contribution.get('capability', 'unknown')
            agent_name = next((name for name, aid in agent_ids.items() if aid == agent_id), 'unknown')
            print(f"   • {agent_name}: {capability}")
    
    # Get system status
    print("📈 Getting system status...")
    status = await coordinator.get_system_status()
    print(f"   Active Agents: {status['registry']['total_agents']}")
    print(f"   Blackboard Items: {status['blackboard']['total_items']}")
    print(f"   Completed Requests: {status['coordinator']['completed_requests']}")
    
    # Cleanup
    await coordinator.shutdown()
    print("✅ Multi-agent system demonstration complete")
    print()


async def main():
    """Run all demonstrations."""
    print("=" * 60)
    print("🎯 LITEAGENT MULTI-AGENT BLACKBOARD DEMONSTRATION")
    print("=" * 60)
    print()
    
    try:
        # Run individual component demonstrations
        await demonstrate_blackboard()
        await demonstrate_agent_registry()
        await demonstrate_async_coordination()
        await demonstrate_multi_agent_system()
        
        print("🎉 ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print()
        print("This demo showed:")
        print("✅ Blackboard pattern for shared knowledge")
        print("✅ Agent registry for dynamic discovery")
        print("✅ Asynchronous task coordination")
        print("✅ Complete multi-agent workflow orchestration")
        print()
        print("The multi-agent system is ready for integration with real LiteAgent instances!")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))