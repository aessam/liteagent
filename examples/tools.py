"""
Example tools for use with LiteAgent.

This module contains example tool implementations that can be used with LiteAgent.
"""

from liteagent.tools import liteagent_tool, FunctionTool, InstanceMethodTool

# Example standalone tools
@liteagent_tool
def get_weather(city: str) -> str:
    """Returns weather information for a city."""
    return f"The weather in {city} is 22°C and sunny."

@liteagent_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@liteagent_tool
def search_database(query: str, limit: int = 5) -> list:
    """
    Simulates searching a database for information.
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        
    Returns:
        List of search results
    """
    # Simulate database search
    results = [
        {"id": 1, "title": f"Result for {query} #1", "score": 0.95},
        {"id": 2, "title": f"Another match for {query}", "score": 0.87},
        {"id": 3, "title": f"Information about {query}", "score": 0.82},
        {"id": 4, "title": f"More data on {query}", "score": 0.76},
        {"id": 5, "title": f"Additional info for {query}", "score": 0.70},
        {"id": 6, "title": f"Supplementary data on {query}", "score": 0.65},
    ]
    return results[:limit]

# Example standalone function using the new liteagent_tool decorator
@liteagent_tool
def calculate_area(width: float, height: float) -> float:
    """Calculates the area of a rectangle."""
    return width * height

# Example class with methods that can be used as tools
class ToolsForAgents:
    """
    Example class with methods that can be used as tools.
    This demonstrates how to use class methods as tools.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.counter = 0
        
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        self.counter += 1
        return a + b
        
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        self.counter += 1
        return a * b
        
    def get_weather(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        self.counter += 1
        if self.api_key:
            # In a real implementation, this would use the API key
            return f"Weather in {city} retrieved with API key {self.api_key[:5]}..."
        else:
            return f"The weather in {city} is 22°C and sunny."
            
    def get_user_data(self, user_id: str) -> dict:
        """
        Retrieves user data from a fictional database.
        This is information an LLM couldn't possibly know without using the tool.
        
        Args:
            user_id: The unique identifier for the user
            
        Returns:
            Dictionary containing user information
        """
        self.counter += 1
        # Return fictional user data based on the ID
        if user_id == "user123":
            return {
                "email": "alex.j@example.com",
                "subscription_tier": "premium",
                "signup_date": "2023-04-15",
                "last_login": "2023-08-22"
            }
        elif user_id == "user456":
            return {
                "email": "sam.smith@example.com",
                "subscription_tier": "basic",
                "signup_date": "2022-11-30",
                "last_login": "2023-08-20"
            }
        else:
            return {
                "email": f"{user_id}@example.com",
                "subscription_tier": "free",
                "signup_date": "2023-01-01",
                "last_login": "2023-08-15"
            }
            
    def get_call_count(self) -> int:
        """Returns the number of times the tools have been called."""
        return self.counter

# Example class using the new liteagent_tool decorator
class SimplifiedToolsForAgents:
    """
    Example class with methods that use the liteagent_tool decorator.
    This demonstrates how to use the simplified tool registration.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.counter = 0
        
    @liteagent_tool
    def add_numbers(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        self.counter += 1
        return a + b
        
    @liteagent_tool
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        self.counter += 1
        return a * b
        
    @liteagent_tool
    def get_weather(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        self.counter += 1
        if self.api_key:
            # In a real implementation, this would use the API key
            return f"Weather in {city} retrieved with API key {self.api_key[:5]}..."
        else:
            return f"The weather in {city} is 22°C and sunny."
            
    @liteagent_tool
    def get_user_data(self, user_id: str) -> dict:
        """
        Retrieves user data from a fictional database.
        This is information an LLM couldn't possibly know without using the tool.
        
        Args:
            user_id: The unique identifier for the user
            
        Returns:
            Dictionary containing user information
        """
        self.counter += 1
        # Return fictional user data based on the ID
        if user_id == "user123":
            return {
                "email": "alex.j@example.com",
                "subscription_tier": "premium",
                "signup_date": "2023-04-15",
                "last_login": "2023-08-22"
            }
        elif user_id == "user456":
            return {
                "email": "sam.smith@example.com",
                "subscription_tier": "basic",
                "signup_date": "2022-11-30",
                "last_login": "2023-08-20"
            }
        else:
            return {
                "email": f"{user_id}@example.com",
                "subscription_tier": "free",
                "signup_date": "2023-01-01",
                "last_login": "2023-08-15"
            }
            
    def get_call_count(self) -> int:
        """Returns the number of times the tools have been called."""
        return self.counter 