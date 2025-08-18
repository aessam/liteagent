"""
Validation helper for integration tests.

This module provides helper functions for validating agent behavior in tests.
"""

import os
import re
from typing import Dict, List, Any, Optional, Union

from liteagent.capabilities import ModelCapabilities
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type


class ValidationTestHelper:
    """Helper class for validation in tests."""
    
    @staticmethod
    def has_api_key_for_model(model: str) -> bool:
        """
        Check if an API key is available for the model.
        
        Args:
            model: The model name
            
        Returns:
            True if an API key is available, False otherwise
        """
        # Normalize model name
        model_lower = model.lower()
        
        # OpenAI models
        if model_lower.startswith("gpt-") or model_lower.startswith("openai/"):
            if "OPENAI_API_KEY" not in os.environ:
                print(f"INFO: Skipping {model} - OPENAI_API_KEY not found")
                return False
            return True
            
        # Anthropic models
        elif model_lower.startswith("anthropic/") or model_lower.startswith("claude"):
            if "ANTHROPIC_API_KEY" not in os.environ:
                print(f"INFO: Skipping {model} - ANTHROPIC_API_KEY not found")
                return False
            return True
            
        # Groq models
        elif model_lower.startswith("groq/") or "llama" in model_lower:
            if "GROQ_API_KEY" not in os.environ:
                print(f"INFO: Skipping {model} - GROQ_API_KEY not found")
                return False
            return True
            
        # Mistral models
        elif model_lower.startswith("mistral/"):
            if "MISTRAL_API_KEY" not in os.environ:
                print(f"INFO: Skipping {model} - MISTRAL_API_KEY not found")
                return False
            return True
            
        # DeepSeek models
        elif model_lower.startswith("deepseek/"):
            if "DEEPSEEK_API_KEY" not in os.environ:
                print(f"INFO: Skipping {model} - DEEPSEEK_API_KEY not found")
                return False
            return True
            
        # Ollama models (local - no API key needed)
        elif model_lower.startswith("ollama/"):
            return True
            
        # Default case - unknown provider
        else:
            print(f"INFO: Skipping {model} - Unknown provider")
            return False
    
    @staticmethod
    def get_system_prompt_for_tools(tool_names: List[str]) -> str:
        """
        Get a system prompt for the specified tools.
        
        Args:
            tool_names: List of tool names
            
        Returns:
            A system prompt for the tools
        """
        tool_descriptions = {
            "get_weather": "Get the current weather for a city",
            "add_numbers": "Add two numbers together",
            "multiply_numbers": "Multiply two numbers together",
            "calculate_area": "Calculate the area of a rectangle",
            "get_user_data": "Retrieve user data for a specific user ID"
        }
        
        prompt = "You are a helpful assistant that can use tools to answer questions.\n\n"
        prompt += "Available tools:\n"
        
        for tool_name in tool_names:
            description = tool_descriptions.get(tool_name, f"Use the {tool_name} tool")
            prompt += f"- {tool_name}: {description}\n"
        
        prompt += "\nUse these tools to help answer the user's questions."
        return prompt
    
    @staticmethod
    def register_parsers_for_type(validation_observer: Any, tool_calling_type: ToolCallingType, tool_names: List[str]):
        """
        Register appropriate parsers for the tools based on the tool calling type.
        
        Args:
            validation_observer: The validation observer
            tool_calling_type: The tool calling type
            tool_names: List of tool names
        """
        # For provider-specific logic, we would need to derive provider from tool_calling_type
        # For now, we'll use generic parsing since we don't have model info here
        provider = "generic"
        
        for tool_name in tool_names:
            if tool_name == "get_weather":
                # Use generic weather response parsing for all providers
                validation_observer.register_response_parser(
                    "get_weather", ValidationTestHelper.parse_weather_response_default
                )
            elif tool_name == "add_numbers":
                validation_observer.register_response_parser(
                    r"(sum|add|total|addition).*?(\d+).*?(\d+).*?=?\s*(\d+)",
                    lambda m: {"a": int(m.group(2)), "b": int(m.group(3)), "result": int(m.group(4))}
                )
            elif tool_name == "multiply_numbers":
                validation_observer.register_response_parser(
                    r"(multiply|product|times|multiplication).*?(\d+).*?(\d+).*?=?\s*(\d+)",
                    lambda m: {"a": int(m.group(2)), "b": int(m.group(3)), "result": int(m.group(4))}
                )
            elif tool_name == "get_user_data":
                # Parse user data responses
                validation_observer.register_response_parser(
                    r"(email|e-mail).*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
                    lambda m: {"email": m.group(2)}
                )
                validation_observer.register_response_parser(
                    r"(subscription|tier).*?(premium|basic|enterprise)", 
                    lambda m: {"tier": m.group(2)}
                )
                validation_observer.register_response_parser(
                    r"(user|id).*?([a-zA-Z0-9]+)",
                    lambda m: {"user_id": m.group(2)}
                )
            elif tool_name == "calculate_area":
                validation_observer.register_response_parser(
                    "calculate_area", ValidationTestHelper.parse_area_response
                )
    
    @staticmethod
    def parse_weather_response_openai(response: str) -> Dict[str, Any]:
        """
        Parse a weather response from OpenAI.
        
        Args:
            response: The response string
            
        Returns:
            A dictionary with the parsed response
        """
        # Extract city name
        city_match = re.search(r"weather in ([A-Za-z\s]+)", response, re.IGNORECASE)
        city = city_match.group(1).strip() if city_match else ""
        
        # Extract temperature
        temp_match = re.search(r"(\d+)°C", response)
        temperature = int(temp_match.group(1)) if temp_match else None
        
        # Extract condition
        condition_patterns = ["sunny", "cloudy", "rainy", "foggy", "snowy", "windy"]
        condition = ""
        for pattern in condition_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                condition = pattern
                break
        
        return {
            "city": city,
            "temperature": temperature,
            "condition": condition
        }
    
    @staticmethod
    def parse_weather_response_anthropic(response: str) -> Dict[str, Any]:
        """
        Parse a weather response from Anthropic.
        
        Args:
            response: The response string
            
        Returns:
            A dictionary with the parsed response
        """
        # Similar to OpenAI but might have different patterns
        return ValidationTestHelper.parse_weather_response_openai(response)
    
    @staticmethod
    def parse_weather_response_default(response: str) -> Dict[str, Any]:
        """
        Parse a weather response with a default parser.
        
        Args:
            response: The response string
            
        Returns:
            A dictionary with the parsed response
        """
        # Extract city name
        city_match = re.search(r"weather in ([A-Za-z\s]+)", response, re.IGNORECASE)
        city = city_match.group(1).strip() if city_match else ""
        
        # Extract temperature if present
        temp_match = re.search(r"(\d+)°C", response)
        temperature = int(temp_match.group(1)) if temp_match else None
        
        return {
            "city": city,
            "temperature": temperature
        }
    
    @staticmethod
    def parse_number_response(response: str) -> Dict[str, Any]:
        """
        Parse a number response.
        
        Args:
            response: The response string
            
        Returns:
            A dictionary with the parsed response
        """
        # Extract numbers
        number_match = re.search(r"(\d+)", response)
        result = int(number_match.group(1)) if number_match else None
        
        # Look for written numbers
        written_numbers = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
            "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90, "hundred": 100
        }
        
        for word, value in written_numbers.items():
            if re.search(r"\b" + word + r"\b", response.lower()):
                result = value
                break
        
        return {
            "result": result
        }
    
    @staticmethod
    def parse_area_response(response: str) -> Dict[str, Any]:
        """
        Parse an area response.
        
        Args:
            response: The response string
            
        Returns:
            A dictionary with the parsed response
        """
        # Extract area
        area_match = re.search(r"area is (\d+)", response, re.IGNORECASE)
        area = int(area_match.group(1)) if area_match else None
        
        # Extract dimensions if present
        width_match = re.search(r"width (?:of|is) (\d+)", response, re.IGNORECASE)
        width = int(width_match.group(1)) if width_match else None
        
        height_match = re.search(r"height (?:of|is) (\d+)", response, re.IGNORECASE)
        height = int(height_match.group(1)) if height_match else None
        
        return {
            "area": area,
            "width": width,
            "height": height
        }
    
    @staticmethod
    def validate_weather_tool_usage(validation_observer: Any, response: str, city: str, tool_calling_type: Any = None):
        """
        Validate that the weather tool was used correctly.
        
        Args:
            validation_observer: The validation observer
            response: The response from the agent
            city: The expected city
            tool_calling_type: The tool calling type (optional)
        """
        validation_observer.assert_function_called("get_weather")
        validation_observer.assert_function_called_with("get_weather", city=city)
        
        # Check weather function result
        weather_result = validation_observer.get_last_function_result("get_weather")
        assert weather_result is not None, "Weather function result should not be None"
        assert city in weather_result, f"Result should mention {city}"
    
    @staticmethod
    def validate_number_tool_usage(validation_observer: Any, response: str, tool_name: str, a_b_dict: Dict[str, int], expected_result: int, tool_calling_type: Any = None):
        """
        Validate that a number tool was used correctly.
        
        Args:
            validation_observer: The validation observer
            response: The response from the agent
            tool_name: The name of the tool (add_numbers or multiply_numbers)
            a_b_dict: Dictionary containing 'a' and 'b' keys with their respective values
            expected_result: The expected result
            tool_calling_type: The tool calling type (optional)
        """
        validation_observer.assert_function_called(tool_name)
        validation_observer.assert_function_called_with(tool_name, **a_b_dict)
        
        # Check function result
        result = validation_observer.get_last_function_result(tool_name)
        assert result == expected_result, f"Expected {tool_name} result to be {expected_result}, got {result}" 