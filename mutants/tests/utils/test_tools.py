"""
Test tool functions for LiteAgent tests.

This module provides example tool functions that can be used in tests.
"""

import random
import math
from typing import Dict, Tuple


def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    temperatures = {
        "Tokyo": (15, 25),
        "New York": (10, 20),
        "London": (8, 18),
        "Paris": (12, 22),
        "Berlin": (7, 17),
        "Sydney": (20, 30),
        "Beijing": (5, 15),
        "Moscow": (0, 10),
        "Cairo": (25, 35),
        "Mumbai": (30, 40),
    }
    
    conditions = ["sunny", "cloudy", "rainy", "foggy", "snowy", "windy"]
    
    # Get temperature range for the city or use a default range
    temp_range = temperatures.get(city, (15, 25))
    temperature = random.randint(temp_range[0], temp_range[1])
    condition = random.choice(conditions)
    
    return f"The weather in {city} is {temperature}°C and {condition}."


def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


def calculate_area(width: float, height: float) -> float:
    """Calculate the area of a rectangle."""
    return width * height


def calculate_square_root(number: float) -> float:
    """Calculate the square root of a number with high precision."""
    return math.sqrt(number)


def get_user_data(user_id: str) -> Dict:
    """
    Retrieves user data for a specific user ID.
    This tool returns information the LLM couldn't possibly know.
    """
    
    # Predefined user data that an LLM wouldn't know
    user_database = {
        "user123": {
            "name": "Alex Johnson",
            "email": "alex.j@example.com",
            "account_created": "2023-04-15",
            "subscription_tier": "premium",
            "last_login": "2025-02-28T14:22:13Z"
        },
        "user456": {
            "name": "Taylor Smith",
            "email": "t.smith@example.net",
            "account_created": "2024-11-03",
            "subscription_tier": "basic",
            "last_login": "2025-03-01T09:45:22Z"
        },
        "user789": {
            "name": "Jamie Lee",
            "email": "jamie.lee@example.org",
            "account_created": "2022-07-19",
            "subscription_tier": "enterprise",
            "last_login": "2025-02-27T16:50:01Z"
        }
    }
    
    if user_id in user_database:
        return user_database[user_id]
    else:
        return {"error": f"No user found with ID: {user_id}"}


class ToolsForAgents:
    """A test class containing tools that can be used by agents in tests."""
    
    def __init__(self, api_key=None):
        """Initialize with an optional API key."""
        self.api_key = api_key
        self._call_count = 0
        
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        self._call_count += 1
        return a + b
        
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        self._call_count += 1
        return a * b
    
    def calculate_square_root(self, number: float) -> float:
        """Calculate the square root of a number with high precision."""
        self._call_count += 1
        return math.sqrt(number)
        
    def get_weather(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        self._call_count += 1
        if self.api_key:
            # Use API key to get real weather (simulated here)
            return f"Weather in {city} retrieved with API key {self.api_key[:5]}...: 22°C and sunny."
        else:
            # Generate random weather data if no API key
            return get_weather(city)
    
    def get_user_data(self, user_id: str) -> Dict:
        """
        Retrieves user data for a specific user ID.
        This tool returns information the LLM couldn't possibly know.
        """
        self._call_count += 1
        return get_user_data(user_id)
            
    def get_call_count(self) -> int:
        """Returns the number of times a tool was called."""
        return self._call_count 