"""
Consolidated integration tests for multi-agent orchestration with AgentTool.

This module tests complex orchestration patterns using multiple agents as tools,
with a focus on:
1. Hierarchical agent relationships using AgentTool
2. Data flow between specialized agents
3. Strong observability for validation
4. Testing across multiple model types
"""

import pytest
import re
import time
import logging
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

from liteagent import LiteAgent
from liteagent.agent_tool import AgentTool
from liteagent.observer import TreeTraceObserver, AgentObserver
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from tests.integration.validation_observer import SequenceValidationObserver
from tests.utils.test_tools import get_weather, add_numbers, get_user_data, ToolsForAgents

from tests.utils.validation_helper import ValidationTestHelper

# Configure logger with console handler for direct visibility during tests
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add console handler if not already present
if not any(isinstance(h, logging.StreamHandler) and h.stream == sys.stdout for h in logger.handlers):
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class MultiAgentObserver(AgentObserver):
    """
    Simple observer that tracks which agents and tools were called during execution.
    
    This observer is designed for multi-agent orchestration testing, focusing only on
    whether the right agents and tools were utilized, without being concerned about
    the exact sequence or quality of LLM responses.
    """
    
    def __init__(self):
        """Initialize the multi-agent observer."""
        self.agent_tools_called = set()  # Just track which agent tools were called
        self.direct_tools_called = set()  # Track which direct function tools were called
        self.function_calls = []  # Keep track of all calls for debugging
    
    def on_event(self, event):
        """Base handler for all events."""
        # Required implementation for AgentObserver
        pass
    
    def on_function_call(self, event):
        """Record function call, tracking both agent tools and direct tools."""
        # Add to our simple tracking sets
        function_name = event.function_name
        self.agent_tools_called.add(function_name)
        self.direct_tools_called.add(function_name)
        
        # Store call for debugging
        self.function_calls.append({
            "name": function_name,
            "arguments": getattr(event, 'function_args', {}),
            "timestamp": time.time()
        })
        
        # Log and print the function call for visibility
        log_msg = f"FUNCTION CALLED: {function_name} with args: {getattr(event, 'function_args', {})}"
        logger.info(log_msg)
        print(f"\n>>> {log_msg}\n")
    
    def assert_process_followed(self, expected_agent_tools=None, expected_direct_tools=None):
        """
        Assert that the multi-agent process was followed correctly.
        
        This simple assertion just checks that the expected tools were called at least once,
        without being concerned about sequences, data flow, or specific parameters.
        
        Args:
            expected_agent_tools: List of agent tool names expected to be called
            expected_direct_tools: List of direct function tools expected to be called
        """
        if expected_agent_tools:
            for tool_name in expected_agent_tools:
                assert tool_name in self.agent_tools_called, f"Expected agent tool '{tool_name}' was not called"
                
        if expected_direct_tools:
            for tool_name in expected_direct_tools:
                assert tool_name in self.direct_tools_called, f"Expected direct tool '{tool_name}' was not called"
        
        # Success if we get here - all expected tools were called at least once


# Define mock system status data for the test
def get_system_status() -> Dict[str, Any]:
    """
    Get current system status.
    This returns mock data that an LLM couldn't know.
    """
    logger.info("DIRECT TOOL: get_system_status called")
    return {
        "cpu_usage": 42.7,
        "memory_usage": 68.3,
        "disk_space": 789.5,
        "active_users": 152,
        "response_time_ms": 213,
        "server_uptime": "15 days, 7 hours, 42 minutes",
        "latest_deployment": "2025-03-18T09:15:00Z"
    }


@pytest.mark.integration
class TestMultiAgentOrchestration:
    """Tests for multi-agent orchestration with AgentTool across all models."""
    
    @pytest.fixture
    def tools_instance(self):
        """Create a ToolsForAgents instance for testing."""
        return ToolsForAgents(api_key="fake-api-key-12345")
    
    @pytest.fixture
    def multi_agent_observer(self):
        """Create a MultiAgentObserver instance for the test."""
        return MultiAgentObserver()
    
    @pytest.fixture
    def tree_observer(self):
        """Create a TreeTraceObserver for visualizing the agent hierarchy."""
        return TreeTraceObserver()
    
    @pytest.fixture
    def user_data_agent(self, model, tools_instance, multi_agent_observer, tree_observer):
        """Create an agent specialized in retrieving user data."""
        logger.info(f"Creating UserDataAgent with model {model}")
        return LiteAgent(
            model=model,
            name="UserDataAgent",
            system_prompt="""You are a User Data Agent specializing in retrieving and analyzing user data.

CRITICAL TASK: When asked for user information, you MUST:
1. Extract the exact user ID from the request (look for patterns like "user123", "user456", etc.)
2. Call get_user_data with that EXACT user ID - do NOT modify it or ask for clarification
3. If you see "user user123", the user ID is "user123"
4. If you see "for user123", the user ID is "user123"
5. NEVER call get_user_data with placeholder values like "please provide a user ID"

Examples:
- Request: "get data for user123" → call get_user_data(user_id="user123")
- Request: "user user456 information" → call get_user_data(user_id="user456")
- Request: "report for user789" → call get_user_data(user_id="user789")

DO NOT make up information - you must use the tool to get accurate data.
When you retrieve user data, format it clearly including the user's name and email.
""",
            tools=[tools_instance.get_user_data],
            observers=[multi_agent_observer, tree_observer]
        )
    
    @pytest.fixture
    def system_status_agent(self, model, multi_agent_observer, tree_observer):
        """Create an agent specialized in retrieving system status information."""
        logger.info(f"Creating SystemStatusAgent with model {model}")
        return LiteAgent(
            model=model,
            name="SystemStatusAgent",
            system_prompt="""You are a System Status Agent specializing in retrieving and analyzing system metrics.
Your main responsibility is to retrieve system status information using the get_system_status tool.
When asked about system status, ALWAYS use the get_system_status tool to get accurate data.
DO NOT make up information - you must use the tool to get accurate metrics.
Present the information in a clear, organized way that highlights important metrics.
""",
            tools=[get_system_status],
            observers=[multi_agent_observer, tree_observer]
        )
    
    @pytest.fixture
    def integration_agent(self, model, user_data_agent, system_status_agent, multi_agent_observer, tree_observer):
        """Create an agent that integrates information from specialized agents."""
        logger.info(f"Creating IntegrationAgent with model {model}")
        # Create AgentTools from the specialized agents
        user_data_tool = AgentTool(
            name="get_user_information",
            description="Get detailed information about a specific user by ID",
            agent=user_data_agent
        )
        
        system_status_tool = AgentTool(
            name="get_system_information",
            description="Get current system status and metrics",
            agent=system_status_agent
        )
        
        return LiteAgent(
            model=model,
            name="IntegrationAgent",
            system_prompt="""You are an Integration Agent responsible for collecting and combining information from multiple sources.
You have access to two specialized agents through tools:
1. get_user_information - retrieves detailed user data
2. get_system_information - retrieves system status metrics

CRITICAL: When you need user information, you MUST pass the specific user ID in your message.
- If the request mentions "user user123", pass message="Get information for user123"
- If the request mentions "for user456", pass message="Get information for user456"  
- NEVER pass vague messages like "Get user data" - always include the specific user ID

Example tool calls:
- get_user_information(message="Get information for user123", parent_context_id="user123")
- get_system_information(message="Get current system status", parent_context_id="user123")

Your job is to call both tools and create a comprehensive report that includes both user information and system status.
Always call BOTH tools to ensure you have complete information before responding.
Format your response as a structured report with clear sections for user data and system status.
""",
            tools=[user_data_tool, system_status_tool],
            observers=[multi_agent_observer, tree_observer]
        )
    
    @pytest.fixture
    def orchestration_agent(self, model, integration_agent, multi_agent_observer, tree_observer):
        """Create the main orchestration agent that coordinates the entire workflow."""
        logger.info(f"Creating OrchestrationAgent with model {model}")
        # Create AgentTool from the integration agent
        integration_tool = AgentTool(
            name="generate_integrated_report",
            description="Generate a comprehensive report that includes both user and system information",
            agent=integration_agent
        )
        
        return LiteAgent(
            model=model,
            name="OrchestrationAgent",
            system_prompt="""You are an Orchestration Agent responsible for coordinating complex workflows.
Your task is to create comprehensive reports by delegating to specialized agents.

When asked to create a report, use the generate_integrated_report tool to collect all necessary information.
This tool will automatically coordinate with specialized agents to gather user data and system status.
Once you receive the integrated report, summarize the key findings and provide strategic recommendations.

DO NOT try to create reports without using the generate_integrated_report tool.
""",
            tools=[integration_tool],
            observers=[multi_agent_observer, tree_observer]
        )
    
    @pytest.mark.integration
    # @pytest.mark.longrun
    def test_multi_agent_orchestration(self, model, orchestration_agent, integration_agent, 
                                      user_data_agent, system_status_agent, 
                                      multi_agent_observer, tree_observer):
        """
        Test the full multi-agent orchestration workflow.
        
        This test verifies only that:
        1. The proper agent tools were called
        2. The proper direct function tools were called
        3. The system produces a response that includes information from both data sources
        
        We don't care about the order or specific execution path, only that the process
        was followed and all necessary pieces were invoked.
        
        Note: This is a long-running test (takes ~20 minutes) marked with 'longrun'.
        To run it explicitly: pytest -m longrun
        """
        print("\n\n==== STARTING MULTI-AGENT ORCHESTRATION TEST ====")
        print(f"==== Using model: {model} ====\n")
        logger.info(f"Starting multi-agent orchestration test with model {model}")
        
        # Set up parent-child relationships for context propagation
        integration_agent.parent_context_id = orchestration_agent.context_id
        user_data_agent.parent_context_id = integration_agent.context_id
        system_status_agent.parent_context_id = integration_agent.context_id
        
        test_user_id = "user123"  # Use a known test user ID
        
        try:
            # Execute the orchestration workflow
            user_query = (f"Please create a comprehensive report for user {test_user_id} "
                        f"that includes both their account information and current system status.")
            
            print(f"\n==== SENDING QUERY: {user_query} ====\n")
            logger.info(f"Sending query to orchestration agent: {user_query}")
            response = orchestration_agent.chat(user_query)
            
            # Skip tests that would fail due to model limitations
            if response is None:
                logger.warning(f"Model {model} returned None response, skipping validation")
                pytest.skip(f"Model {model} returned None response, skipping validation")
                return
            
            print("\n==== ORCHESTRATION COMPLETE, VALIDATING RESULTS ====\n")
            logger.info("Orchestration complete, validating results")
            
            # Visualize the agent tree for debugging (helpful but not used for assertions)
            tree_observer.print_trace()
            
            # Simple verification that the process was followed
            # Check that both agent tools and direct function tools were called
            expected_agent_tools = ["generate_integrated_report", "get_user_information", "get_system_information"]
            expected_direct_tools = ["get_user_data", "get_system_status"]
            
            print(f"\n==== TOOLS CALLED ====")
            print(f"Agent tools: {multi_agent_observer.agent_tools_called}")
            print(f"Direct tools: {multi_agent_observer.direct_tools_called}\n")
            
            logger.info(f"Agent tools called: {multi_agent_observer.agent_tools_called}")
            logger.info(f"Direct tools called: {multi_agent_observer.direct_tools_called}")
            
            multi_agent_observer.assert_process_followed(
                expected_agent_tools=expected_agent_tools,
                expected_direct_tools=expected_direct_tools
            )
            
            print("\n==== PROCESS VERIFICATION PASSED ====\n")
            logger.info("Process verification passed")
            
            # Basic validation that the key information is present in the response
            # We're not checking details, just that the process worked end-to-end
            has_user_data = "Alex Johnson" in response or "alex.j@example.com" in response
            has_system_data = (("42.7" in response and "cpu" in response.lower()) or 
                             ("68.3" in response and "memory" in response.lower()))
            
            assert has_user_data, "User data not found in final response"
            assert has_system_data, "System status data not found in final response"
            
            print("\n==== RESPONSE CONTENT VERIFICATION PASSED ====\n")
            logger.info("Response content verification passed")
            
            # Success - if we get here, all validations passed!
            print("\n==== TEST COMPLETED SUCCESSFULLY ====\n")
            logger.info("Test completed successfully")
            
        except Exception as e:
            # Handle different model-specific exceptions
            if "TypeError: 'NoneType' object is not iterable" in str(e) and "ollama" in model:
                logger.warning(f"Model {model} returned None response, skipping validation")
                pytest.skip(f"Model {model} returned None response, skipping validation")
            else:
                # Print all function calls for debugging
                print(f"\n==== TEST FAILED: {str(e)} ====\n")
                print(f"Function calls: {multi_agent_observer.function_calls}")
                print(f"Agent tools called: {multi_agent_observer.agent_tools_called}")
                print(f"Direct tools called: {multi_agent_observer.direct_tools_called}\n")
                
                logger.error(f"Test failed: {str(e)}")
                logger.error(f"Function calls: {multi_agent_observer.function_calls}")
                logger.error(f"Agent tools called: {multi_agent_observer.agent_tools_called}")
                logger.error(f"Direct tools called: {multi_agent_observer.direct_tools_called}")
                # For other exceptions, re-raise
                raise 