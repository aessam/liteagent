"""
Example of using the LiteCodeAgent to solve problems by writing and executing code.
"""

import os
import sys
from dotenv import load_dotenv
import tempfile

# Add the parent directory to the path so we can import liteagent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from liteagent import LiteCodeAgent, ContainerFactory, ConsoleObserver
from liteagent.utils import setup_logging


def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Set up logging
    setup_logging(level="INFO")
    
    # Create a temporary directory for code execution
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory for code execution: {temp_dir}")
        
        # Create the CodeAgent
        agent = LiteCodeAgent(
            model="gpt-4", 
            name="CodeExpert",
            debug=True,
            container_type="podman",  # Use podman as default
            container_config={
                "source_directory": temp_dir,
                "memory_limit": "1g",
                "timeout": 60
            }
        )
        
        # Add a console observer to see what's happening
        agent.add_observer(ConsoleObserver())
        
        # Example problems to solve
        problems = [
            "Write a Python function that calculates the Fibonacci sequence up to n. Then use it to print the first 10 Fibonacci numbers.",
            "Create a Python script that reads a text file and counts the frequency of each word. Then print the top 5 most frequent words."
        ]
        
        for i, problem in enumerate(problems, 1):
            print(f"\n\n===== Problem {i} =====")
            print(problem)
            print("=" * 40)
            
            # Get solution from the agent
            response = agent.chat(problem)
            
            print("\nResponse from agent:")
            print(response)
            
            print("\n" + "=" * 40)
            
        print("\nDemo completed!")


if __name__ == "__main__":
    main()