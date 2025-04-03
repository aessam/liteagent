"""
Example demonstrating how to use LiteAgents as MCP servers.

This example creates multiple LiteAgents with different tools and exposes them
as an MCP server that can be accessed by MCP clients like Claude Desktop.

To run this example:
1. Make sure you have the required API keys set in your environment variables
2. Run `python examples/mcp_example.py`
3. Connect to the MCP server using an MCP-compatible client like Claude Desktop

Command-line options:
  --transport {stdio,sse}  Transport protocol to use (default: sse)
  --host HOST              Host to bind the server to (default: 127.0.0.1)
  --port PORT              Port to bind the server to (default: 8000)
  --model MODEL            Model to use for the agents (default: gpt-4o-mini)
  --skip-tests             Skip testing the agents before starting the MCP server
  --debug                  Enable debug mode with verbose logging
"""

import os
import argparse
import sys
from dotenv import load_dotenv
from liteagent import LiteAgent, run_as_mcp, liteagent_tool, ConsoleObserver
from liteagent.utils import check_api_keys


# Define a class with tools
class CalculatorTools:
    def __init__(self):
        self.calc_count = 0
    
    @liteagent_tool
    def add_numbers(self, a: int, b: int) -> int:
        """Add two numbers together."""
        self.calc_count += 1
        return a + b
    
    @liteagent_tool
    def multiply_numbers(self, a: int, b: int) -> int:
        """Multiply two numbers together."""
        self.calc_count += 1
        return a * b
    
    @liteagent_tool
    def get_calculation_count(self) -> int:
        """Get the number of calculations performed so far."""
        return self.calc_count


# Define standalone tools
@liteagent_tool
def get_weather(location: str) -> str:
    """Get the weather for a location (simulated)."""
    return f"The weather in {location} is sunny and 72 degrees Fahrenheit."


@liteagent_tool
def search_database(query: str) -> str:
    """Search a database for information (simulated)."""
    results = {
        "renewable energy": "Renewable energy is energy derived from natural resources that are replenished at a higher rate than they are consumed.",
        "climate change": "Climate change refers to long-term shifts in temperatures and weather patterns, mainly caused by human activities.",
        "artificial intelligence": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to intelligence of humans and other animals.",
    }
    
    # Find the closest match in our simulated database
    for key in results:
        if key in query.lower():
            return results[key]
    
    return "No results found for your query."


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LiteAgent MCP Example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # MCP server configuration
    mcp_group = parser.add_argument_group("MCP Server Configuration")
    mcp_group.add_argument("--transport", choices=["stdio", "sse"], default=os.getenv("MCP_TRANSPORT", "sse"),
                        help="Transport protocol to use")
    mcp_group.add_argument("--host", default=os.getenv("MCP_HOST", "127.0.0.1"),
                        help="Host to bind the server to (for SSE transport)")
    mcp_group.add_argument("--port", type=int, default=int(os.getenv("MCP_PORT", "8000")),
                        help="Port to bind the server to (for SSE transport)")
    
    # Model configuration
    model_group = parser.add_argument_group("Model Configuration")
    model_group.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        help="Model to use for the agents")
    
    # Testing options
    test_group = parser.add_argument_group("Testing Options")
    test_group.add_argument("--skip-tests", action="store_true",
                        help="Skip testing the agents before starting the MCP server")
    
    # Debug options
    debug_group = parser.add_argument_group("Debug Options")
    debug_group.add_argument("--debug", action="store_true",
                        help="Enable debug mode with verbose logging")
    
    return parser.parse_args()


def main():
    """Run the example."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Load environment variables from .env file if present
    load_dotenv()
    
    # Check for API keys
    check_api_keys()
    
    # Enable console output for debugging
    console_observer = ConsoleObserver()
    
    # Initialize the calculator tools
    calculator_tools = CalculatorTools()
    
    # Create a Calculator Agent with class methods as tools
    calculator_agent = LiteAgent(
        model=args.model,
        name="Calculator",
        system_prompt="""You are a Calculator Agent specialized in mathematical operations.
You can add and multiply numbers, and keep track of how many calculations you've performed.
If asked about anything else, politely explain that you can only help with calculations.""",
        tools=[
            calculator_tools.add_numbers,
            calculator_tools.multiply_numbers,
            calculator_tools.get_calculation_count
        ],
        description="A specialized calculator agent that can perform basic mathematical operations like addition and multiplication. It keeps track of how many calculations it performs and can report this count.",
        observers=[console_observer]
    )
    
    # Create a Weather Agent
    weather_agent = LiteAgent(
        model=args.model,
        name="Weather",
        system_prompt="""You are a Weather Agent specialized in providing weather information.
You can only provide weather information for different locations.
If asked about anything else, politely explain that you can only help with weather.""",
        tools=[get_weather],
        description="A weather information agent that can provide simulated weather data for any location. It specializes in giving weather reports and forecasts.",
        observers=[console_observer]
    )
    
    # Create a Search Agent
    search_agent = LiteAgent(
        model=args.model,
        name="Search",
        system_prompt="""You are a Search Agent specialized in searching for information.
You can search for information on various topics like renewable energy, climate change, and artificial intelligence.
If asked about anything else, politely explain that you can only help with search.""",
        tools=[search_database],
        description="An information search agent that can look up facts and details about various topics including renewable energy, climate change, and artificial intelligence. It provides concise, relevant information from its knowledge base.",
        observers=[console_observer]
    )
    
    # Test direct agent use to verify functionality if not skipped
    if not args.skip_tests:
        print("\n=== Testing Calculator Agent ===")
        response = calculator_agent.chat("What is 23 + 45?")
        print(f"Response: {response}")
        
        response = calculator_agent.chat("What is 7 * 9?")
        print(f"Response: {response}")
        
        response = calculator_agent.chat("How many calculations have been performed?")
        print(f"Response: {response}")
        
        # Test error handling
        print("\n=== Testing Error Handling ===")
        response = calculator_agent.chat("What is the weather in Tokyo?")
        print(f"Response: {response}")
        
        print("\n=== Testing Weather Agent ===")
        response = weather_agent.chat("What's the weather in Tokyo?")
        print(f"Response: {response}")
        
        # Test error handling
        response = weather_agent.chat("What is 23 + 45?")
        print(f"Response: {response}")
        
        print("\n=== Testing Search Agent ===")
        response = search_agent.chat("Find information about renewable energy")
        print(f"Response: {response}")
        
        # Test error handling
        response = search_agent.chat("What is the weather in Tokyo?")
        print(f"Response: {response}")
    
    # Run all agents as MCP servers
    print("\n=== Starting MCP Server ===")
    print("This will expose all agents as an MCP server.")
    print("You can connect to this server using an MCP-compatible client like Claude Desktop.")
    
    if args.transport == "sse":
        print(f"The server will be available at http://{args.host}:{args.port}")
    else:
        print(f"Using {args.transport} transport mode")
    
    print("Press Ctrl+C to stop the server.")
    
    run_as_mcp(
        calculator_agent, 
        weather_agent, 
        search_agent, 
        server_name="LiteAgent MCP Demo",
        transport=args.transport,
        host=args.host,
        port=args.port
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1) 