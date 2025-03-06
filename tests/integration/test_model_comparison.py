"""
Integration tests comparing different models using the same tools.

These tests run the same tasks across different models to compare their
performance and capabilities with tools.
"""

import pytest
import os
import time
from typing import List, Dict, Optional, Any
import statistics

from liteagent.agent import LiteAgent
from liteagent.tools import tool, liteagent_tool
from liteagent.examples import (
    get_weather, add_numbers, search_database, calculate_area
)

from tests.integration.validation_observer import ValidationObserver


# Skip tests if API key is not set
skip_if_no_api_key = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OpenAI API key not found in environment variables"
)

# Skip tests if Ollama is not available
skip_if_no_ollama = pytest.mark.skipif(
    os.system("which ollama > /dev/null 2>&1") != 0,
    reason="Ollama is not installed or not in PATH"
)


# More complex tool for testing model capabilities
@tool
def compute_statistics(numbers: List[float], operations: Optional[List[str]] = None) -> Dict[str, float]:
    """
    Compute statistical measures for a list of numbers.
    
    Args:
        numbers: List of numbers to analyze
        operations: List of operations to perform, can include 'mean', 'median', 'min', 'max', 'std' (standard deviation)
            If None, all operations are performed
            
    Returns:
        Dictionary with the computed statistics
    """
    result = {}
    
    if operations is None:
        operations = ['mean', 'median', 'min', 'max', 'std']
    
    for op in operations:
        if op == 'mean':
            result['mean'] = statistics.mean(numbers)
        elif op == 'median':
            result['median'] = statistics.median(numbers)
        elif op == 'min':
            result['min'] = min(numbers)
        elif op == 'max':
            result['max'] = max(numbers)
        elif op == 'std':
            if len(numbers) > 1:
                result['std'] = statistics.stdev(numbers)
            else:
                result['std'] = 0.0
    
    return result


@pytest.mark.integration
@pytest.mark.slow
class TestModelComparison:
    """Integration tests comparing different models using the same tools."""
    
    MODELS = {
        "gpt4o_mini": {
            "name": "gpt-4o-mini",
            "marker": skip_if_no_api_key
        },
        "ollama_phi": {
            "name": "ollama/phi4",
            "marker": skip_if_no_ollama
        }
    }
    
    @pytest.mark.parametrize("model_key", MODELS.keys())
    def test_basic_tool_usage(self, model_key, validation_observer):
        """Test basic tool usage across different models."""
        model_info = self.MODELS[model_key]
        model_name = model_info["name"]
        marker = model_info["marker"]
        
        # Skip test if requirements for this model aren't met
        if model_key == "gpt4o_mini" and "OPENAI_API_KEY" not in os.environ:
            pytest.skip("OpenAI API key not found in environment variables")
        elif model_key == "ollama_phi" and os.system("which ollama > /dev/null 2>&1") != 0:
            pytest.skip("Ollama is not installed or not in PATH")
        
        # Create agent with simple tools
        agent = LiteAgent(
            model=model_name,
            name=f"{model_key}_agent",
            system_prompt=(
                "You are a helpful assistant that can use tools to answer questions. "
                "Always use tools when appropriate to solve the user's request."
            ),
            tools=[add_numbers, get_weather],
            observers=[validation_observer]
        )
        
        # Test with add_numbers tool
        response = agent.chat("What is 13 + 29?")
        functions_called = list(validation_observer.called_functions)
        
        # Record test results but don't fail - we're just comparing
        result = {
            "model": model_name,
            "used_add_numbers": "add_numbers" in validation_observer.called_functions,
            "correct_answer": "42" in response,
            "functions_called": functions_called,
            "response": response
        }
        
        print(f"\nModel: {model_name}")
        print(f"Used add_numbers: {result['used_add_numbers']}")
        print(f"Correct answer: {result['correct_answer']}")
        print(f"Functions called: {result['functions_called']}")
        
        validation_observer.reset()
    
    @pytest.mark.parametrize("model_key", MODELS.keys())
    def test_complex_tool_usage(self, model_key, validation_observer):
        """Test usage of a more complex tool across different models."""
        model_info = self.MODELS[model_key]
        model_name = model_info["name"]
        marker = model_info["marker"]
        
        # Skip test if requirements for this model aren't met
        if model_key == "gpt4o_mini" and "OPENAI_API_KEY" not in os.environ:
            pytest.skip("OpenAI API key not found in environment variables")
        elif model_key == "ollama_phi" and os.system("which ollama > /dev/null 2>&1") != 0:
            pytest.skip("Ollama is not installed or not in PATH")
        
        # Create agent with more complex tools
        agent = LiteAgent(
            model=model_name,
            name=f"{model_key}_complex_agent",
            system_prompt=(
                "You are a data analysis assistant that can compute statistics. "
                "Always use the compute_statistics tool when asked to analyze numbers."
            ),
            tools=[compute_statistics],
            observers=[validation_observer]
        )
        
        # Test with compute_statistics tool
        query = "What are the mean, median, minimum, and maximum of these numbers: 5, 10, 15, 20, 25?"
        response = agent.chat(query)
        
        # Record test results but don't fail - we're just comparing
        result = {
            "model": model_name,
            "used_compute_statistics": "compute_statistics" in validation_observer.called_functions,
            "contains_mean": "15" in response and "mean" in response.lower(),
            "contains_median": "15" in response and "median" in response.lower(),
            "contains_min": "5" in response and ("min" in response.lower() or "minimum" in response.lower()),
            "contains_max": "25" in response and ("max" in response.lower() or "maximum" in response.lower()),
            "functions_called": list(validation_observer.called_functions),
            "response": response
        }
        
        print(f"\nModel: {model_name}")
        print(f"Used compute_statistics: {result['used_compute_statistics']}")
        print(f"Contains mean result: {result['contains_mean']}")
        print(f"Contains median result: {result['contains_median']}")
        print(f"Contains min result: {result['contains_min']}")
        print(f"Contains max result: {result['contains_max']}")
        
        validation_observer.reset()
    
    @pytest.mark.parametrize("model_key", MODELS.keys())
    def test_multi_step_problem(self, model_key, validation_observer):
        """Test multi-step problem solving across different models."""
        model_info = self.MODELS[model_key]
        model_name = model_info["name"]
        marker = model_info["marker"]
        
        # Skip test if requirements for this model aren't met
        if model_key == "gpt4o_mini" and "OPENAI_API_KEY" not in os.environ:
            pytest.skip("OpenAI API key not found in environment variables")
        elif model_key == "ollama_phi" and os.system("which ollama > /dev/null 2>&1") != 0:
            pytest.skip("Ollama is not installed or not in PATH")
        
        # Create agent with multiple tools
        agent = LiteAgent(
            model=model_name,
            name=f"{model_key}_multi_step_agent",
            system_prompt=(
                "You are a problem-solving assistant that can use multiple tools to solve complex problems. "
                "Break down problems into steps and use the appropriate tools for each step."
            ),
            tools=[add_numbers, calculate_area, compute_statistics],
            observers=[validation_observer]
        )
        
        # Test with multi-step problem
        query = (
            "I have a rectangle with width 4 and height 5. Calculate its area. "
            "Then, I have another rectangle with width 6 and height 3. Calculate its area too. "
            "Finally, compute the mean and maximum of these two areas."
        )
        response = agent.chat(query)
        
        # Record test results
        result = {
            "model": model_name,
            "used_calculate_area": "calculate_area" in validation_observer.called_functions,
            "used_compute_statistics": "compute_statistics" in validation_observer.called_functions,
            "contains_first_area": "20" in response,
            "contains_second_area": "18" in response,
            "contains_mean": "19" in response and "mean" in response.lower(),
            "contains_max": "20" in response and ("max" in response.lower() or "maximum" in response.lower()),
            "functions_called": list(validation_observer.called_functions),
            "response": response
        }
        
        print(f"\nModel: {model_name}")
        print(f"Used calculate_area: {result['used_calculate_area']}")
        print(f"Used compute_statistics: {result['used_compute_statistics']}")
        print(f"Contains first area (20): {result['contains_first_area']}")
        print(f"Contains second area (18): {result['contains_second_area']}")
        print(f"Contains mean result (19): {result['contains_mean']}")
        print(f"Contains max result (20): {result['contains_max']}")
        
        validation_observer.reset() 