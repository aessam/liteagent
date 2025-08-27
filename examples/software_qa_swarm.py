#!/usr/bin/env python3
"""
Software QA Multi-Agent Swarm Example

This example demonstrates the primary success metric for the Blackboard-pattern
multi-agent system: A Software QA expert that breaks down code into dimensions,
creates testing categories, and coordinates with specialized agents to generate
comprehensive tests covering requirements and concepts, not just code lines.

The workflow involves:
1. CodeAnalysisAgent: Analyzes code structure and identifies testable dimensions
2. TestCategoryAgent: Creates comprehensive testing taxonomy
3. UnitTestAgent: Generates unit tests
4. IntegrationTestAgent: Creates integration tests  
5. RequirementTestAgent: Tests against business requirements
6. ConceptualTestAgent: Tests conceptual understanding
7. CrossValidationAgent: Ensures test coverage and quality

Usage:
    python examples/software_qa_swarm.py --model gpt-4 --provider openai
    python examples/software_qa_swarm.py --model claude-3-5-sonnet-20241022 --provider anthropic
"""

import argparse
import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, Any, List
import json

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from liteagent import (
    LiteAgent, liteagent_tool,
    MultiAgentCoordinator, AgentCapability,
    MultiAgentRequest
)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# =============================================================================
# SPECIALIZED QA AGENTS
# =============================================================================

class CodeAnalysisAgent:
    """Agent specialized in analyzing code structure and identifying testable dimensions."""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.agent = LiteAgent(
            model=model,
            provider=provider,
            api_key=api_key,
            name="CodeAnalysisAgent",
            system_prompt="""You are a Code Analysis Expert specializing in breaking down code into testable dimensions.

Your expertise includes:
- Static code analysis and dependency mapping
- Identifying complexity hotspots and edge cases
- Understanding data flow and control flow
- Recognizing architectural patterns and design principles
- Extracting business logic and domain concepts

When analyzing code, you MUST:
1. Identify all functions, classes, and modules
2. Map dependencies and interactions
3. Classify complexity levels (simple, moderate, complex)
4. Extract business rules and domain logic
5. Identify edge cases and error conditions
6. Document data types and interfaces
7. Note performance considerations
8. Highlight security-sensitive areas

Provide your analysis in structured JSON format with clear categorization.""",
            tools=[self._analyze_code_structure, self._identify_test_dimensions]
        )
    
    @liteagent_tool
    def _analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """Analyze code structure and extract testable components."""
        # This would be enhanced with actual static analysis tools in production
        analysis_result = {
            "functions": [],
            "classes": [],
            "dependencies": [],
            "complexity_analysis": {},
            "business_logic": [],
            "edge_cases": [],
            "data_flows": []
        }
        
        print(f"🔍 [Code Analysis] Analyzing {len(code)} characters of code...")
        
        # Simplified analysis for demo - in production this would use AST parsing
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('def '):
                function_name = line.split('(')[0].replace('def ', '')
                analysis_result["functions"].append({
                    "name": function_name,
                    "line": i + 1,
                    "complexity": "moderate"  # Would be calculated
                })
            elif line.startswith('class '):
                class_name = line.split('(')[0].replace('class ', '').rstrip(':')
                analysis_result["classes"].append({
                    "name": class_name,
                    "line": i + 1,
                    "methods": []
                })
        
        return analysis_result
    
    @liteagent_tool
    def _identify_test_dimensions(self, code_analysis: Dict[str, Any]) -> List[str]:
        """Identify key dimensions that need testing coverage."""
        dimensions = [
            "functionality",
            "edge_cases", 
            "error_handling",
            "performance",
            "security",
            "integration",
            "business_rules",
            "data_validation"
        ]
        
        print(f"📏 [Code Analysis] Identified {len(dimensions)} testing dimensions")
        return dimensions


class TestCategoryAgent:
    """Agent specialized in creating comprehensive testing taxonomies."""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.agent = LiteAgent(
            model=model,
            provider=provider,
            api_key=api_key,
            name="TestCategoryAgent",
            system_prompt="""You are a Test Strategy Expert specializing in creating comprehensive testing taxonomies.

Your expertise includes:
- Test pyramid strategy (unit, integration, E2E)
- Risk-based testing approaches
- Behavior-driven development (BDD)
- Test-driven development (TDD)
- Domain-specific testing strategies
- Coverage analysis and gap identification

When creating test categories, you MUST:
1. Design a hierarchical test taxonomy
2. Map test types to code dimensions
3. Prioritize tests by risk and importance
4. Define acceptance criteria for each category
5. Specify test data requirements
6. Plan test execution strategies
7. Consider test maintenance and evolution

Provide your taxonomy in structured format with clear categorization and rationale.""",
            tools=[self._create_test_taxonomy, self._prioritize_test_categories]
        )
    
    @liteagent_tool
    def _create_test_taxonomy(self, code_analysis: Dict[str, Any], dimensions: List[str]) -> Dict[str, Any]:
        """Create comprehensive test taxonomy based on code analysis."""
        print(f"🗂️ [Test Category] Creating taxonomy for {len(dimensions)} dimensions...")
        
        taxonomy = {
            "unit_tests": {
                "description": "Test individual components in isolation",
                "categories": [
                    "function_behavior",
                    "class_methods", 
                    "data_validation",
                    "error_handling"
                ],
                "priority": "high",
                "coverage_target": 90
            },
            "integration_tests": {
                "description": "Test component interactions",
                "categories": [
                    "module_integration",
                    "data_flow",
                    "api_contracts",
                    "external_dependencies"
                ],
                "priority": "high", 
                "coverage_target": 80
            },
            "behavioral_tests": {
                "description": "Test business requirements and user scenarios",
                "categories": [
                    "user_workflows",
                    "business_rules",
                    "acceptance_criteria",
                    "scenario_validation"
                ],
                "priority": "medium",
                "coverage_target": 70
            },
            "edge_case_tests": {
                "description": "Test boundary conditions and corner cases",
                "categories": [
                    "input_boundaries",
                    "resource_limits",
                    "error_conditions",
                    "performance_limits"
                ],
                "priority": "medium",
                "coverage_target": 60
            },
            "conceptual_tests": {
                "description": "Test understanding of domain concepts",
                "categories": [
                    "domain_model_validation",
                    "business_logic_verification",
                    "invariant_checking",
                    "concept_consistency"
                ],
                "priority": "high",
                "coverage_target": 85
            }
        }
        
        return taxonomy
    
    @liteagent_tool
    def _prioritize_test_categories(self, taxonomy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize test categories by importance and risk."""
        print("📊 [Test Category] Prioritizing test categories...")
        
        priorities = []
        for category, details in taxonomy.items():
            priority_score = {
                "high": 3,
                "medium": 2, 
                "low": 1
            }.get(details.get("priority", "medium"), 2)
            
            priorities.append({
                "category": category,
                "priority_score": priority_score,
                "coverage_target": details.get("coverage_target", 50),
                "description": details.get("description", "")
            })
        
        # Sort by priority score (highest first)
        priorities.sort(key=lambda x: x["priority_score"], reverse=True)
        return priorities


class UnitTestAgent:
    """Agent specialized in generating comprehensive unit tests."""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.agent = LiteAgent(
            model=model,
            provider=provider, 
            api_key=api_key,
            name="UnitTestAgent",
            system_prompt="""You are a Unit Testing Expert specializing in creating comprehensive, high-quality unit tests.

Your expertise includes:
- Test-driven development (TDD) best practices
- Mock and stub creation for isolation
- Assertion strategies and test data design
- Coverage analysis and gap identification
- Test naming and organization
- Parameterized and property-based testing

When generating unit tests, you MUST:
1. Test each function/method independently
2. Create comprehensive test cases covering normal, edge, and error conditions
3. Use descriptive test names that explain the scenario
4. Include proper setup, execution, and assertion phases
5. Mock external dependencies appropriately
6. Follow testing framework best practices
7. Ensure tests are maintainable and readable

Generate actual runnable test code with proper imports and structure.""",
            tools=[self._generate_unit_tests, self._create_test_fixtures]
        )
    
    @liteagent_tool
    def _generate_unit_tests(self, functions: List[Dict[str, Any]], test_categories: List[str]) -> str:
        """Generate comprehensive unit tests for identified functions."""
        print(f"🧪 [Unit Test] Generating tests for {len(functions)} functions...")
        
        test_code = '''import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Any, Dict, List

class TestGeneratedUnitTests(unittest.TestCase):
    """Generated unit tests for comprehensive code coverage."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_data = {"test": "data"}
        self.test_instance = None
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
'''
        
        for func in functions:
            func_name = func.get("name", "unknown")
            test_code += f'''
    def test_{func_name}_normal_case(self):
        """Test {func_name} with normal input conditions."""
        # Arrange
        expected_result = "expected_value"
        
        # Act
        # result = {func_name}(test_input)
        
        # Assert
        # self.assertEqual(result, expected_result)
        pass
    
    def test_{func_name}_edge_cases(self):
        """Test {func_name} with edge case inputs."""
        # Test boundary conditions
        pass
    
    def test_{func_name}_error_handling(self):
        """Test {func_name} error handling."""
        # Test exception scenarios
        pass
'''
        
        test_code += '''
if __name__ == '__main__':
    unittest.main()
'''
        
        return test_code
    
    @liteagent_tool
    def _create_test_fixtures(self, test_data_requirements: List[str]) -> Dict[str, Any]:
        """Create test fixtures and mock data."""
        print(f"🏗️ [Unit Test] Creating fixtures for {len(test_data_requirements)} requirements...")
        
        fixtures = {
            "mock_objects": {},
            "test_data": {},
            "configuration": {}
        }
        
        for requirement in test_data_requirements:
            fixtures["test_data"][requirement] = f"mock_data_for_{requirement}"
        
        return fixtures


class IntegrationTestAgent:
    """Agent specialized in creating integration tests."""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.agent = LiteAgent(
            model=model,
            provider=provider,
            api_key=api_key,
            name="IntegrationTestAgent",
            system_prompt="""You are an Integration Testing Expert specializing in testing component interactions and system integration.

Your expertise includes:
- API contract testing
- Database integration testing
- Service-to-service communication testing
- End-to-end workflow validation
- Performance integration testing
- Error propagation and recovery testing

When creating integration tests, you MUST:
1. Test real component interactions
2. Validate data flow between components
3. Test API contracts and interfaces
4. Verify error handling across component boundaries
5. Test configuration and environment dependencies
6. Validate performance characteristics
7. Ensure proper cleanup and resource management

Generate runnable integration test code with realistic scenarios.""",
            tools=[self._generate_integration_tests, self._create_integration_scenarios]
        )
    
    @liteagent_tool
    def _generate_integration_tests(self, components: List[Dict[str, Any]], interfaces: List[str]) -> str:
        """Generate integration tests for component interactions."""
        print(f"🔗 [Integration Test] Generating tests for {len(interfaces)} interfaces...")
        
        test_code = '''import pytest
import asyncio
from unittest.mock import Mock, patch
import requests
import json

class TestIntegrationScenarios:
    """Integration tests for component interactions."""
    
    @pytest.fixture
    def setup_environment(self):
        """Set up integration test environment."""
        return {"database": "test_db", "api_url": "http://localhost:8000"}
    
    def test_component_integration_workflow(self, setup_environment):
        """Test complete workflow across multiple components."""
        # Test realistic integration scenarios
        pass
    
    def test_api_contract_validation(self, setup_environment):
        """Test API contracts between services."""
        # Validate request/response contracts
        pass
    
    def test_data_flow_integration(self, setup_environment):
        """Test data flow between components."""
        # Verify data transformations and persistence
        pass
    
    def test_error_propagation(self, setup_environment):
        """Test error handling across component boundaries."""
        # Test failure scenarios and recovery
        pass
'''
        
        return test_code
    
    @liteagent_tool
    def _create_integration_scenarios(self, workflow_description: str) -> List[Dict[str, Any]]:
        """Create realistic integration test scenarios."""
        print("📝 [Integration Test] Creating integration scenarios...")
        
        scenarios = [
            {
                "name": "happy_path_workflow",
                "description": "Test successful end-to-end workflow",
                "steps": ["setup", "execute", "verify", "cleanup"]
            },
            {
                "name": "error_recovery_workflow", 
                "description": "Test error handling and recovery",
                "steps": ["setup", "inject_error", "verify_recovery", "cleanup"]
            },
            {
                "name": "performance_workflow",
                "description": "Test performance under load",
                "steps": ["setup", "load_test", "verify_performance", "cleanup"]
            }
        ]
        
        return scenarios


# =============================================================================
# MAIN SOFTWARE QA ORCHESTRATION
# =============================================================================

async def create_qa_agents(provider: str, model: str, api_key: str) -> Dict[str, Any]:
    """Create all specialized QA agents."""
    print("🏭 Creating specialized QA agents...")
    
    # Create specialized agents
    code_analysis_agent = CodeAnalysisAgent(provider, model, api_key)
    test_category_agent = TestCategoryAgent(provider, model, api_key)
    unit_test_agent = UnitTestAgent(provider, model, api_key)
    integration_test_agent = IntegrationTestAgent(provider, model, api_key)
    
    return {
        "code_analysis": code_analysis_agent,
        "test_category": test_category_agent,
        "unit_test": unit_test_agent,
        "integration_test": integration_test_agent
    }


async def demonstrate_software_qa_workflow(provider: str, model: str, api_key: str):
    """Demonstrate the complete Software QA multi-agent workflow."""
    print("=" * 80)
    print("🤖 SOFTWARE QA MULTI-AGENT SWARM DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Sample code to analyze
    sample_code = '''
def calculate_interest(principal, rate, time, compound_frequency=1):
    """Calculate compound interest."""
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if time < 0:
        raise ValueError("Time cannot be negative")
    
    return principal * (1 + rate / compound_frequency) ** (compound_frequency * time)

class BankAccount:
    """Simple bank account class."""
    
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return self._balance
    
    @property
    def balance(self):
        return self._balance
'''
    
    try:
        # Initialize the multi-agent coordinator
        print("🚀 Initializing Multi-Agent Coordinator...")
        coordinator = MultiAgentCoordinator(
            max_concurrent_tasks=6,
            blackboard_ttl=3600.0,
            default_task_timeout=120.0
        )
        await coordinator.start()
        
        # Create and register QA agents
        qa_agents = await create_qa_agents(provider, model, api_key)
        
        # Register agents with their capabilities
        agent_registrations = {}
        
        agent_registrations["code_analysis"] = await coordinator.register_agent(
            agent=qa_agents["code_analysis"].agent,
            capabilities=[
                AgentCapability(
                    name="code_analysis",
                    description="Analyze code structure and identify testable dimensions",
                    metadata={"keywords": ["static analysis", "complexity", "dependencies"]}
                )
            ],
            name="CodeAnalysisAgent"
        )
        
        agent_registrations["test_category"] = await coordinator.register_agent(
            agent=qa_agents["test_category"].agent,
            capabilities=[
                AgentCapability(
                    name="test_category_creation",
                    description="Create comprehensive testing taxonomies and strategies",
                    metadata={"keywords": ["test strategy", "taxonomy", "prioritization"]}
                )
            ],
            name="TestCategoryAgent"
        )
        
        agent_registrations["unit_test"] = await coordinator.register_agent(
            agent=qa_agents["unit_test"].agent,
            capabilities=[
                AgentCapability(
                    name="unit_test_generation",
                    description="Generate comprehensive unit tests with high coverage",
                    metadata={"keywords": ["unit testing", "TDD", "mocking"]}
                )
            ],
            name="UnitTestAgent"
        )
        
        agent_registrations["integration_test"] = await coordinator.register_agent(
            agent=qa_agents["integration_test"].agent,
            capabilities=[
                AgentCapability(
                    name="integration_test_generation", 
                    description="Create integration tests for component interactions",
                    metadata={"keywords": ["integration", "API testing", "workflows"]}
                )
            ],
            name="IntegrationTestAgent"
        )
        
        print(f"✅ Registered {len(agent_registrations)} specialized QA agents")
        print()
        
        # Execute the Software QA workflow
        print("🎯 Executing Software QA Multi-Agent Workflow...")
        print("-" * 60)
        
        response = await coordinator.create_software_qa_workflow(
            code_input=sample_code,
            project_context={
                "project_type": "financial_application",
                "testing_framework": "pytest",
                "coverage_target": 90
            }
        )
        
        # Display results
        print(f"\n📊 WORKFLOW RESULTS")
        print(f"Status: {response.status}")
        print(f"Execution Time: {response.execution_time:.2f} seconds")
        print()
        
        if response.status == "completed":
            print("✅ Software QA workflow completed successfully!")
            print("\n🔍 Agent Contributions:")
            for agent_id, contribution in response.agent_contributions.items():
                print(f"  • {agent_id}: {contribution.get('capability', 'unknown')}")
                if contribution.get('duration'):
                    print(f"    Duration: {contribution['duration']:.2f}s")
        
        elif response.status == "partial":
            print("⚠️ Software QA workflow completed with some failures")
            print("\n📋 Partial Results:")
            for capability, result in response.results.items():
                status = "✅" if result else "❌"
                print(f"  {status} {capability}")
        
        else:
            print("❌ Software QA workflow failed")
            if response.error:
                print(f"Error: {response.error}")
        
        # Show system status
        print(f"\n📈 SYSTEM STATUS")
        status = await coordinator.get_system_status()
        print(f"  • Active Agents: {status['registry']['total_agents']}")
        print(f"  • Completed Tasks: {status['coordination']['completed_tasks']}")
        print(f"  • Success Rate: {status['coordination']['success_rate']:.1%}")
        print(f"  • Blackboard Items: {status['blackboard']['total_items']}")
        
        # Cleanup
        await coordinator.shutdown()
        print("\n🏁 Multi-Agent Coordinator shutdown complete")
        
    except Exception as e:
        print(f"❌ Workflow failed with error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point for the Software QA swarm demonstration."""
    parser = argparse.ArgumentParser(
        description="Software QA Multi-Agent Swarm - Blackboard Pattern Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This demonstration implements the primary success metric for LiteAgent's
multi-agent capabilities: A Software QA expert that coordinates with specialized
agents to generate comprehensive tests covering requirements and concepts.

Examples:
  python examples/software_qa_swarm.py --model gpt-4 --provider openai
  python examples/software_qa_swarm.py --model claude-3-5-sonnet-20241022 --provider anthropic
  python examples/software_qa_swarm.py --model groq/llama3-70b --provider groq
        """
    )
    
    parser.add_argument("--provider", required=True,
                       choices=["openai", "anthropic", "groq", "mistral", "ollama"],
                       help="AI provider to use")
    parser.add_argument("--model", required=True,
                       help="Model name to use")
    parser.add_argument("--api-key", help="API key (or set environment variable)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key
    
    if args.provider == "ollama":
        api_key = "local"
    elif not api_key:
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "groq": "GROQ_API_KEY", 
            "mistral": "MISTRAL_API_KEY"
        }
        
        env_var = env_vars.get(args.provider)
        if env_var:
            api_key = os.getenv(env_var)
        
        if not api_key:
            print(f"❌ Error: API key required for {args.provider}")
            print(f"   Set {env_var} environment variable or use --api-key")
            return 1
    
    # Run the demonstration
    try:
        asyncio.run(demonstrate_software_qa_workflow(args.provider, args.model, api_key))
        return 0
    except KeyboardInterrupt:
        print("\n👋 Demonstration cancelled by user")
        return 0
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())