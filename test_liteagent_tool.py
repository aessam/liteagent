from liteagent import LiteAgent, liteagent_tool
from liteagent.utils import check_api_keys

# Example 1: Standalone function with type annotations
@liteagent_tool
def calculate_square(number: int) -> int:
    """Calculate the square of a number."""
    return number * number

# Example 2: Standalone function without type annotations
@liteagent_tool
def greet(name):
    """Greet a person by name."""
    return f"Hello, {name}! Nice to meet you."

# Example 3: Class with instance methods using the decorator
class MathTools:
    def __init__(self):
        self.operations_count = 0
    
    @liteagent_tool
    def add(self, a: int, b: int) -> int:
        """Add two numbers together."""
        self.operations_count += 1
        return a + b
    
    @liteagent_tool
    def subtract(self, a, b):
        """Subtract b from a."""
        self.operations_count += 1
        return a - b
    
    def get_operations_count(self):
        """Return the number of operations performed."""
        return self.operations_count

# Example 4: Class with static and class methods
class StringTools:
    @staticmethod
    @liteagent_tool
    def reverse_string(text: str) -> str:
        """Reverse a string."""
        return text[::-1]
    
    @classmethod
    @liteagent_tool
    def capitalize_words(cls, text: str) -> str:
        """Capitalize each word in a string."""
        return " ".join(word.capitalize() for word in text.split())

def main():
    # Check for API keys
    check_api_keys()
    
    print("\n=== Testing liteagent_tool decorator ===")
    
    # Create instances
    math_tools = MathTools()
    
    # Create an agent with all the tools
    agent = LiteAgent(
        model="gpt-4o-mini",
        name="TestAgent",
        system_prompt="You are a helpful assistant that can perform various operations.",
        tools=[
            calculate_square,
            greet,
            math_tools.add,
            math_tools.subtract,
            StringTools.reverse_string,
            StringTools.capitalize_words
        ],
        debug=True
    )
    
    # Print the available tools
    print("Available tools:", [name for name in agent.tools.keys()])
    
    # Test with a query that uses multiple tools
    print("\n--- Test Agent Response ---")
    response = agent.chat("Can you calculate the square of 7, add 10 and 15, subtract 5 from 20, reverse the string 'hello world', and capitalize 'this is a test'? Also, please greet Alice.")
    print("Agent Response:", response)
    
    # Show that the instance state is maintained
    print(f"Math operations count: {math_tools.get_operations_count()}")

if __name__ == "__main__":
    main() 