"""
Secret validation tool for test self-verification.

This module provides a validation tool that LLMs can use to confirm
the correctness of their responses during testing.
"""

from liteagent.tools import liteagent_tool


@liteagent_tool
def validate_output(result_type: str, is_correct: bool, explanation: str = "") -> bool:
    """
    Validation tool for tests. The agent should call this to confirm answer correctness.
    
    Args:
        result_type: Type of result being validated (e.g., "arithmetic", "weather", "data_retrieval")
        is_correct: Whether the agent believes its answer is correct
        explanation: Optional explanation of why the answer is correct/incorrect
        
    Returns:
        The is_correct value (for test verification)
        
    Examples:
        - validate_output("arithmetic", True, "7 + 9 = 16")
        - validate_output("weather", True, "Successfully retrieved Tokyo weather")
        - validate_output("calculation", False, "Could not complete multiplication")
    """
    # This tool simply returns what the LLM provides
    # Tests will check both that this was called AND that is_correct=True
    return is_correct


@liteagent_tool 
def validate_tool_usage(tool_name: str, used_correctly: bool, reason: str = "") -> bool:
    """
    Validation tool for verifying correct tool usage.
    
    Args:
        tool_name: Name of the tool that was used
        used_correctly: Whether the tool was used correctly
        reason: Explanation of correct/incorrect usage
        
    Returns:
        The used_correctly value
        
    Examples:
        - validate_tool_usage("add_numbers", True, "Used with correct arguments a=7, b=9")
        - validate_tool_usage("get_weather", True, "Retrieved weather for requested city")
    """
    return used_correctly


@liteagent_tool
def validate_reasoning(reasoning_type: str, is_valid: bool, steps: str = "") -> bool:
    """
    Validation tool for multi-step reasoning verification.
    
    Args:
        reasoning_type: Type of reasoning performed (e.g., "multi_step", "chain_of_thought")
        is_valid: Whether the reasoning process was valid
        steps: Description of the reasoning steps taken
        
    Returns:
        The is_valid value
        
    Examples:
        - validate_reasoning("multi_step", True, "First got weather, then performed calculation")
        - validate_reasoning("chain_of_thought", True, "Broke down complex problem into steps")
    """
    return is_valid


# Convenience function to get all validation tools
def get_validation_tools():
    """
    Get all validation tools for adding to test agents.
    
    Returns:
        List of validation tool functions
    """
    return [validate_output, validate_tool_usage, validate_reasoning]