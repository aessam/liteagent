"""
Validation helper for integration tests.

This module provides helper functions for validating agent behavior in tests.
"""

import os
import re
from typing import Dict, List, Any, Optional, Union

from liteagent.tool_calling_types import ToolCallingType


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
        if model.startswith("gpt-") or model.startswith("openai/"):
            return "OPENAI_API_KEY" in os.environ
        elif model.startswith("anthropic/") or model.startswith("claude"):
            return "ANTHROPIC_API_KEY" in os.environ
        elif model.startswith("groq/") or model.startswith("llama"):
            return "GROQ_API_KEY" in os.environ
        elif model.startswith("ollama/"):
            return True  # Ollama is local, no API key needed
        else:
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
        for tool_name in tool_names:
            if tool_name == "get_weather":
                if tool_calling_type == ToolCallingType.OPENAI_FUNCTION_CALLING:
                    validation_observer.register_response_parser(
                        r"weather\s+in\s+([A-Za-z\s]+).*?(\d+)[°℃C].*?(\w+)",
                        lambda m: {"city": m.group(1), "temperature": m.group(2), "condition": m.group(3)}
                    )
                elif tool_calling_type == ToolCallingType.ANTHROPIC_TOOL_CALLING:
                    validation_observer.register_response_parser(
                        r"weather\s+in\s+([A-Za-z\s]+).*?(\d+)[°℃C].*?(\w+)",
                        lambda m: {"city": m.group(1), "temperature": m.group(2), "condition": m.group(3)}
                    )
                else:
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