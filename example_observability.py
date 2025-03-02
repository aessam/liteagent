"""
Example demonstrating the observability features of LiteAgent.

This example shows how to use the observer pattern to track agent events,
including context IDs for tracing multi-agent interactions.
"""

import os
from dotenv import load_dotenv
import time
import argparse
import json
from typing import Dict, List, Optional

from liteagent import (
    LiteAgent, tool, liteagent_tool, 
    ConsoleObserver, FileObserver, TreeTraceObserver, generate_context_id,
    AgentObserver, AgentEvent
)
from liteagent.utils import setup_logging, logger

# Load environment variables
load_dotenv()

# Example tool functions
@tool
def get_weather(city: str) -> str:
    """Simulated weather information for a city."""
    return f"The weather in {city} is sunny with a high of 75°F."

@tool
def calculator(operation: str, a: float, b: float) -> float:
    """Perform a simple calculation."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply" or operation == "times" or operation == "x" or operation == "*" or operation == "multiplication":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Example demonstrating a multi-agent system with context tracking
def run_agent_example(model_name: str) -> None:
    """
    Run a demonstration of agent observability with context tracking.
    
    Args:
        model_name: The model to use for the agents
    """
    # Create observers
    console_observer = ConsoleObserver()
    file_observer = FileObserver("agent_events.jsonl")
    tree_observer = TreeTraceObserver()
    
    # Create a parent context ID for this run
    parent_context_id = generate_context_id()
    
    # Create the main agent
    main_agent = LiteAgent(
        model=model_name,
        name="MainAgent",
        system_prompt="You are a helpful assistant that can use tools to answer questions.",
        tools=[get_weather, calculator],
        context_id=parent_context_id,  # This is the root context
        observers=[console_observer, file_observer, tree_observer]
    )
    
    # Create a second agent (child of the main agent)
    secondary_agent = LiteAgent(
        model=model_name,
        name="SecondaryAgent",
        system_prompt="You are a specialized assistant that helps with calculations.",
        tools=[calculator],
        parent_context_id=parent_context_id,  # This links to the parent
        observers=[console_observer, file_observer, tree_observer]
    )
    
    # Create a third agent (also a child of the main agent)
    tertiary_agent = LiteAgent(
        model=model_name,
        name="WeatherAgent",
        system_prompt="You are a specialized assistant that provides weather information.",
        tools=[get_weather],
        parent_context_id=parent_context_id,  # This links to the parent
        observers=[console_observer, file_observer, tree_observer]
    )
    
    # Run the main agent
    print("\n=== Main Agent Interaction ===")
    main_response = main_agent.chat("What's the weather in Seattle and can you calculate 25 + 17?")
    print(f"Main Agent Response: {main_response}")
    
    # Run the secondary agent (in a real system, this might be called by the main agent)
    print("\n=== Secondary Agent Interaction ===")
    secondary_response = secondary_agent.chat("Calculate the square root of 144 by using the calculator to multiply 12 by 1.")
    print(f"Secondary Agent Response: {secondary_response}")
    
    # Run the tertiary agent
    print("\n=== Weather Agent Interaction ===")
    tertiary_response = tertiary_agent.chat("What's the weather in Tokyo?")
    print(f"Weather Agent Response: {tertiary_response}")
    
    # Print the trace in tree format
    tree_observer.print_trace()
    
    print("\nObservability data has been logged to 'agent_events.jsonl'")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="LiteAgent Observability Example")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                        help="Model to use for the agent (e.g., gpt-3.5-turbo, gpt-4)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    setup_logging(log_level=log_level)
    
    # Run the example
    run_agent_example(args.model) 